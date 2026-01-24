""" bone_sanctuary.py
    The Homeostatic Regulator for the Tragic Engine. """

from bone_data import SANCTUARY
from bone_lexicon import Prisma

class PIDController:
    """
    A simple, dependency-free PID controller.
    (Duplicated here to avoid circular imports with bone_cycle)
    """
    def __init__(self, kp, ki, kd, setpoint=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._prev_error = 0.0
        self._integral = 0.0

    def update(self, measurement, dt=1.0):
        error = self.setpoint - measurement
        self._integral += error * dt
        derivative = (error - self._prev_error) / dt
        output = (self.kp * error) + (self.ki * self._integral) + (self.kd * derivative)
        self._prev_error = error
        return output

class SanctuaryGovernor:
    """
    A continuous, gentle PID controller that nudges toward safe coordinates.
    """

    def __init__(self, events_ref):
        self.events = events_ref
        self.voltage_pid = PIDController(kp=0.05, ki=0.01, kd=0.02,
                                         setpoint=SANCTUARY.VOLTAGE_TARGET)
        self.drag_pid = PIDController(kp=0.08, ki=0.02, kd=0.03,
                                      setpoint=SANCTUARY.DRAG_TARGET)
        self.in_sanctuary = False
        self.consecutive_safe_ticks = 0

    def assess(self, physics_packet):
        """Returns (is_in_sanctuary, distance_from_sanctuary)"""
        if isinstance(physics_packet, dict):
            v = physics_packet.get("voltage", 0.0)
            d = physics_packet.get("narrative_drag", 0.0)
            t = physics_packet.get("truth_ratio", 0.0)
        else:
            v = getattr(physics_packet, "voltage", 0.0)
            d = getattr(physics_packet, "narrative_drag", 0.0)
            t = getattr(physics_packet, "truth_ratio", 0.0)

        v_dist = abs(v - SANCTUARY.VOLTAGE_TARGET) / (SANCTUARY.VOLTAGE_TOLERANCE or 1.0)
        d_dist = abs(d - SANCTUARY.DRAG_TARGET) / (SANCTUARY.DRAG_TOLERANCE or 1.0)
        t_dist = abs(t - SANCTUARY.TRUTH_TARGET) / 0.3

        avg_dist = (v_dist + d_dist + t_dist) / 3.0
        is_safe = avg_dist < 0.5

        if is_safe:
            self.consecutive_safe_ticks += 1
            if self.consecutive_safe_ticks >= 3 and not self.in_sanctuary:
                self.in_sanctuary = True
                self.events.log(f"{SANCTUARY.COLOR}![☀️] SANCTUARY: The air is calm here.{Prisma.RST}", "SYS")
        else:
            self.consecutive_safe_ticks = 0
            self.in_sanctuary = False

        return self.in_sanctuary, avg_dist

    def apply_gentle_correction(self, physics_packet):
        """Soft nudges - only applies when NOT in extreme states."""
        if isinstance(physics_packet, dict):
            curr_v = physics_packet.get("voltage", 0)
            curr_d = physics_packet.get("narrative_drag", 0)
            flow = physics_packet.get("flow_state", "")
        else:
            curr_v = getattr(physics_packet, "voltage", 0)
            curr_d = getattr(physics_packet, "narrative_drag", 0)
            flow = getattr(physics_packet, "flow_state", "")

        if (curr_v > 18.0 or curr_d > 8.0 or flow in ["SUPERCONDUCTIVE", "HUBRIS_RISK"]):
            return 0.0, 0.0

        v_corr = self.voltage_pid.update(curr_v)
        d_corr = self.drag_pid.update(curr_d)

        v_apply = v_corr * 0.1
        d_apply = d_corr * 0.1

        if isinstance(physics_packet, dict):
            physics_packet["voltage"] += v_apply
            physics_packet["narrative_drag"] += d_apply
        else:
            physics_packet.voltage += v_apply
            physics_packet.narrative_drag += d_apply

        return v_apply, d_apply