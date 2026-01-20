# bone_cycle.py
# "The wheel turns, and ages come and pass." - Jordan

import traceback, random, time
from typing import Dict, Any, Tuple, List
from bone_bus import Prisma, BoneConfig, CycleContext
from bone_village import TownHall
from bone_personality import TheBureau
from bone_physics import TheBouncer, RuptureValve, ChromaScope
from bone_viewer import GeodesicRenderer
from bone_architect import PanicRoom

class PIDController:
    """A Proportional-Integral-Derivative controller w/Integral Windup Protection."""
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float = 0.0, output_limits: Tuple[float, float] = (-5.0, 5.0)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_min, self.output_max = output_limits
        self.prev_error = 0.0
        self.integral = 0.0
        self.last_time = time.time()

    def update(self, current_value: float, dt: float = None) -> float:
        now = time.time()
        if dt is None:
            dt = now - self.last_time
        self.last_time = now
        safe_dt = max(0.001, min(1.0, dt))
        error = self.setpoint - current_value
        self.integral += error * safe_dt
        self.integral = max(self.output_min, min(self.output_max, self.integral))
        derivative = (error - self.prev_error) / safe_dt
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        output = max(self.output_min, min(self.output_max, output))
        self.prev_error = error
        return output

    def reset(self):
        self.prev_error = 0.0
        self.integral = 0.0
        self.last_time = time.time()

class CycleStabilizer:
    """The Gyroscope. Keeps the narrative vehicle from flipping over. Now with 20% more sass."""
    def __init__(self, events_ref):
        self.events = events_ref
        self.voltage_pid = PIDController(kp=0.25, ki=0.05, kd=0.1, setpoint=10.0, output_limits=(-4.0, 4.0))
        self.drag_pid = PIDController(kp=0.4, ki=0.1, kd=0.05, setpoint=1.5, output_limits=(-3.0, 3.0))
        self.last_phase: str = "INIT"

    @staticmethod
    def _get_current_metrics(ctx: CycleContext) -> Tuple[float, float]:
        p = ctx.physics
        if isinstance(p, dict):
            return p.get("voltage", 0.0), p.get("narrative_drag", 0.0)
        return getattr(p, "voltage", 0.0), getattr(p, "narrative_drag", 0.0)

    @staticmethod
    def _apply_correction(ctx: CycleContext, key: str, correction: float):
        if abs(correction) < 0.05: return 0.0
        p = ctx.physics
        is_dict = isinstance(p, dict)
        if is_dict:
            old_val = p.get(key, 0.0)
            p[key] = max(0.0, old_val + correction)
        else:
            old_val = getattr(p, key, 0.0)
            setattr(p, key, max(0.0, old_val + correction))
        return correction

    def stabilize(self, ctx: CycleContext, current_phase: str):
        curr_v, curr_d = self._get_current_metrics(ctx)
        v_force = self.voltage_pid.update(curr_v)
        d_force = self.drag_pid.update(curr_d)
        corrections_made = False
        if abs(curr_v - self.voltage_pid.setpoint) > 6.0:
            applied_v = self._apply_correction(ctx, "voltage", v_force)
            if abs(applied_v) > 0.1:
                reason = "PID_DAMPENER" if applied_v < 0 else "PID_EXCITATION"
                ctx.record_flux(current_phase, "voltage", curr_v, curr_v + applied_v, reason)
                if abs(applied_v) > 1.0:
                    self.events.log(f"{Prisma.GRY}⚖️ STABILIZER: Voltage corrected ({applied_v:+.1f}v). Steady...{Prisma.RST}", "SYS")
                corrections_made = True
        if abs(curr_d - self.drag_pid.setpoint) > 2.5:
            applied_d = self._apply_correction(ctx, "narrative_drag", d_force)
            if abs(applied_d) > 0.1:
                reason = "PID_LUBRICATION" if applied_d < 0 else "PID_BRAKING"
                ctx.record_flux(current_phase, "narrative_drag", curr_d, curr_d + applied_d, reason)
                if applied_d < -1.0:
                    self.events.log(f"{Prisma.GRY}🛢️ STABILIZER: Grease applied. Drag reduced ({applied_d:+.1f}).{Prisma.RST}", "SYS")
                corrections_made = True
        self.last_phase = current_phase
        return corrections_made

class SimulationPhase:
    """Base class for any step in the cycle."""
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.name = "GENERIC_PHASE"

    def run(self, ctx: CycleContext) -> CycleContext:
        raise NotImplementedError

class ObservationPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "OBSERVE"
        self.vsl_32v = RuptureValve(self.eng.mind.lex, self.eng.mind.mem)

    def run(self, ctx: CycleContext):
        gaze_result = self.eng.phys.tension.gaze(ctx.input_text, self.eng.mind.mem.graph)
        ctx.physics = gaze_result["physics"]
        ctx.clean_words = gaze_result["clean_words"]
        self.eng.tick_count += 1
        rupture = self.vsl_32v.analyze(ctx.physics)
        if rupture: ctx.log(rupture["log"])
        return ctx

class MaintenancePhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "MAINTENANCE"

    def run(self, ctx: CycleContext):
        if self.eng.tick_count % 10 != 0: return ctx
        try:
            rotted = self.eng.lex.atrophy(self.eng.tick_count, 100)
            if rotted:
                for w in rotted:
                    self.eng.limbo.ghosts.append(f"👻{w.upper()}_ECHO")
                example = rotted[0]
                ctx.log(f"{Prisma.GRY}NEURO-PRUNING: {len(rotted)} concepts decayed (e.g., '{example}').{Prisma.RST}")
            self.eng.mind.mem.enforce_limits(self.eng.tick_count)
        except Exception as e:
            if BoneConfig.VERBOSE_LOGGING: print(f"Maintenance Error: {e}")
        return ctx

class GatekeeperPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "GATEKEEP"
        self.bouncer = TheBouncer(self.eng)
        self.bureau = TheBureau()

    def run(self, ctx: CycleContext):
        is_allowed_entry, refusal_packet = self.bouncer.check_entry(ctx)
        if not is_allowed_entry:
            ctx.refusal_triggered = True
            ctx.refusal_packet = refusal_packet
            return ctx
        audit_result = self.bureau.audit(ctx.physics, getattr(ctx, "bio_result", {}))
        if audit_result:
            self.eng.bio.mito.state.atp_pool += audit_result.get("atp_gain", 0.0)
            ctx.log(audit_result["log"])
            status = audit_result.get("status")
            if status == "BLOCK":
                ctx.is_bureaucratic = True
                ctx.physics["narrative_drag"] = 10.0
                ctx.physics["voltage"] = 0.0
                ctx.bureau_ui = audit_result["ui"]
            elif status == "TAX":
                ctx.log(f"{Prisma.GRY}   (BUREAU TAX DEDUCTED...){Prisma.RST}")
        return ctx

class MetabolismPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "METABOLISM"

    def run(self, ctx: CycleContext):
        physics = ctx.physics
        gov_msg = self.eng.bio.governor.shift(
            physics, self.eng.phys.dynamics.voltage_history, self.eng.tick_count
        )
        if gov_msg:
            self.eng.events.log(gov_msg, "GOV")
        bio_feedback = self._generate_feedback(physics)
        stress_mod = self.eng.bio.governor.get_stress_modifier(self.eng.tick_count)
        circadian_bias = self._check_circadian_rhythm()
        ctx.bio_result = self.eng.soma.digest_cycle(
            ctx.input_text, physics, bio_feedback,
            self.eng.health, self.eng.stamina, stress_mod, self.eng.tick_count,
            circadian_bias=circadian_bias
        )
        ctx.is_alive = ctx.bio_result["is_alive"]
        for bio_item in ctx.bio_result["logs"]:
            if any(x in str(bio_item) for x in ["CRITICAL", "TAX", "Poison", "NECROSIS"]):
                ctx.log(bio_item)
        self._audit_hubris(ctx, physics)
        self._apply_healing(ctx)
        return ctx

    @staticmethod
    def _generate_feedback(physics):
        """Standardizes physics data for the bio-engine."""
        return {
            "INTEGRITY": physics.get("truth_ratio", 0.0),
            "STATIC": physics.get("repetition", 0.0),
            "FORCE": physics.get("voltage", 0.0) / 20.0,
            "BETA": physics.get("beta_index", 1.0)
        }

    def _check_circadian_rhythm(self):
        """Only checks the clock occasionally to save cycles."""
        if self.eng.tick_count % 10 == 0:
            bias, msg = self.eng.bio.endo.calculate_circadian_bias()
            if msg:
                self.eng.events.log(f"{Prisma.CYN}🕒 {msg}{Prisma.RST}", "BIO")
            return bias
        return None

    def _audit_hubris(self, ctx, physics):
        """Checks if the user is flying too close to the sun."""
        hubris_hit, hubris_msg, event_type = self.eng.phys.tension.audit_hubris(physics)
        if hubris_hit:
            ctx.log(hubris_msg)
            if event_type == "FLOW_BOOST":
                self.eng.bio.mito.state.atp_pool += 20.0
            elif event_type == "ICARUS_CRASH":
                damage = 15.0
                self.eng.health -= damage
                ctx.log(f"   {Prisma.RED}IMPACT TRAUMA: -{damage} HP.{Prisma.RST}")

    def _apply_healing(self, ctx):
        """Orchestrates Kintsugi (Repairing breaks with gold) and Therapy (Healing trauma vectors)."""
        is_cracked, koan = self.eng.kintsugi.check_integrity(self.eng.stamina)
        if is_cracked:
            ctx.log(f"{Prisma.YEL}🏺 KINTSUGI ACTIVATED: Vessel cracking.{Prisma.RST}")
            ctx.log(f"   {Prisma.WHT}KOAN: {koan}{Prisma.RST}")
        if self.eng.kintsugi.active_koan:
            repair = self.eng.kintsugi.attempt_repair(ctx.physics, self.eng.trauma_accum)
            if repair and repair["success"]:
                ctx.log(repair["msg"])
                self.eng.stamina = min(BoneConfig.MAX_STAMINA, self.eng.stamina + 20.0)
                ctx.log(f"   {Prisma.GRN}STAMINA RESTORED (+20.0){Prisma.RST}")
        healed = self.eng.therapy.check_progress(ctx.physics, self.eng.stamina, self.eng.trauma_accum)
        if healed:
            joined = ", ".join(healed)
            ctx.log(f"{Prisma.GRN}❤️ THERAPY STREAK: Healing [{joined}]. Health +5.{Prisma.RST}")
            self.eng.health = min(BoneConfig.MAX_HEALTH, self.eng.health + 5.0)

class RealityFilterPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "REALITY_FILTER"
        self.vsl_32v = RuptureValve(self.eng.mind.lex, self.eng.mind.mem)

    def run(self, ctx: CycleContext):
        reflection = self.eng.mind.mirror.get_reflection_modifiers()
        old_drag = ctx.physics["narrative_drag"]
        ctx.physics["narrative_drag"] *= reflection["drag_mult"]
        if old_drag != ctx.physics["narrative_drag"]:
            ctx.record_flux("SIMULATION", "narrative_drag", old_drag, ctx.physics["narrative_drag"], "MIRROR_DISTORTION")
        if reflection.get("atp_tax", 0) > 0:
            tax = reflection["atp_tax"]
            self.eng.bio.mito.state.atp_pool -= tax
            if random.random() < 0.2:
                ctx.log(f"{Prisma.RED}MIRROR TAX: -{tax:.1f} ATP applied.{Prisma.RST}")
        cap = reflection.get("voltage_cap", 999.0)
        if ctx.physics["voltage"] > cap:
            old_v = ctx.physics["voltage"]
            ctx.physics["voltage"] = cap
            ctx.record_flux("SIMULATION", "voltage", old_v, cap, "MIRROR_CAP")
            ctx.log(f"{Prisma.GRY}MIRROR: Voltage capped at {cap}.{Prisma.RST}")
        trigram_data = self.vsl_32v.geodesic.resolve_trigram(ctx.physics.get("vector", {}))
        ctx.world_state["trigram"] = trigram_data
        if random.random() < 0.05:
            t_sym, t_name = trigram_data["symbol"], trigram_data["name"]
            ctx.log(f"{trigram_data['color']}I CHING: {t_sym} {t_name} is in the ascendant.{Prisma.RST}")
        return ctx

class NavigationPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "NAVIGATION"

    def run(self, ctx: CycleContext):
        physics = ctx.physics
        if self.eng.tick_count == 3:
            ctx.log(self.eng.navigator.strike_root(physics.get("vector", {})))
        shock = self.eng.navigator.check_transplant_shock(physics.get("vector", {}))
        if shock:
            physics["narrative_drag"] += 1.0
            ctx.log(shock)
        new_drag, grav_log = self.eng.gordon.check_gravity(physics.get("narrative_drag", 0), physics.get("psi", 0))
        if grav_log: ctx.log(grav_log)
        physics["narrative_drag"] = new_drag
        did_flinch, flinch_msg, panic = self.eng.gordon.flinch(ctx.clean_words, self.eng.tick_count)
        if did_flinch:
            ctx.log(flinch_msg)
            if panic: physics.update(panic)
        current_loc, entry_msg = self.eng.navigator.locate(physics)
        if entry_msg: ctx.log(entry_msg)
        env_logs = self.eng.navigator.apply_environment(physics)
        for e_log in env_logs: ctx.log(e_log)
        orbit_state, drag_pen, orbit_msg = self.eng.cosmic.analyze_orbit(self.eng.mind.mem, ctx.clean_words)
        raw_zone = physics.get("zone", "COURTYARD")
        stabilized_zone = self.eng.stabilizer.stabilize(raw_zone, physics, (orbit_state, drag_pen))
        adjusted_drag = self.eng.stabilizer.override_cosmic_drag(drag_pen, stabilized_zone)
        physics["zone"] = stabilized_zone
        self.eng.apply_cosmic_physics(physics, orbit_state, adjusted_drag)
        ctx.world_state["orbit"] = orbit_state
        if orbit_msg: ctx.log(orbit_msg)
        return ctx

class MachineryPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "MACHINERY"

    def run(self, ctx: CycleContext):
        physics = ctx.physics
        eff_boost, zen_msg = self.eng.zen.raking_the_sand(physics, ctx.bio_result)
        if zen_msg: ctx.log(zen_msg)
        if eff_boost > 0:
            current_eff = self.eng.bio.mito.state.efficiency_mod
            self.eng.bio.mito.state.efficiency_mod = min(2.0, current_eff + (eff_boost * 0.1))
        if self.eng.gordon.inventory:
            is_craft, craft_msg, old_item, new_item = self.eng.phys.forge.attempt_crafting(physics, self.eng.gordon.inventory)
            if is_craft:
                ctx.log(craft_msg)
                if old_item in self.eng.gordon.inventory:
                    self.eng.gordon.inventory.remove(old_item)
                ctx.log(self.eng.gordon.acquire(new_item))
        transmute_msg = self.eng.phys.forge.transmute(physics)
        if transmute_msg: ctx.log(transmute_msg)
        _, forge_msg, new_item = self.eng.phys.forge.hammer_alloy(physics)
        if forge_msg: ctx.log(forge_msg)
        if new_item: ctx.log(self.eng.gordon.acquire(new_item))
        _, _, theremin_msg, t_crit = self.eng.phys.theremin.listen(physics, self.eng.bio.governor.mode)
        if theremin_msg: ctx.log(theremin_msg)
        if t_crit == "AIRSTRIKE":
            damage = 25.0
            self.eng.health -= damage
            ctx.log(f"{Prisma.RED}*** CRITICAL THEREMIN DISCHARGE *** -{damage} HP{Prisma.RST}")
        c_state, c_val, c_msg = self.eng.phys.crucible.audit_fire(physics)
        if c_msg: ctx.log(c_msg)
        if c_state == "MELTDOWN":
            self.eng.health -= c_val
        return ctx

class IntrusionPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "INTRUSION"

    def run(self, ctx: CycleContext):
        p_active, p_log = self.eng.bio.parasite.infect(ctx.physics, self.eng.stamina)
        if p_active: ctx.log(p_log)
        if self.eng.limbo.ghosts:
            if ctx.logs:
                ctx.logs[-1] = self.eng.limbo.haunt(ctx.logs[-1])
            else:
                ctx.log(self.eng.limbo.haunt("The air is heavy."))
        is_p, p_msg = self.eng.check_pareidolia(ctx.clean_words)
        if is_p:
            ctx.log(p_msg)
            ctx.physics["psi"] = min(1.0, ctx.physics["psi"] + 3.0)
        return ctx

class SoulPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "SOUL"

    def run(self, ctx: CycleContext):
        lesson = self.eng.soul.crystallize_memory(ctx.physics, ctx.bio_result, self.eng.tick_count)
        if lesson:
            ctx.log(f"{Prisma.VIOLET}   (The lesson '{lesson}' echoes in the chamber.){Prisma.RST}")
        if not self.eng.soul.current_obsession:
            self.eng.soul.find_obsession(self.eng.lex)
        self.eng.soul.pursue_obsession(ctx.physics)
        if self.eng.gordon.inventory:
            self.eng.tinkerer.audit_tool_use(ctx.physics, self.eng.gordon.inventory)
        council_advice, adjustments = self.eng.council.convene(ctx.input_text, ctx.physics)
        for advice in council_advice:
            ctx.log(advice)
        if adjustments:
            for param, delta in adjustments.items():
                if hasattr(ctx.physics, "__getitem__") or isinstance(ctx.physics, dict):
                    if param in ctx.physics:
                        old_val = ctx.physics[param]
                        ctx.physics[param] += delta
                        ctx.record_flux("SIMULATION", param, old_val, ctx.physics[param], "COUNCIL_MANDATE")
                elif hasattr(ctx.physics, param):
                    old_val = getattr(ctx.physics, param)
                    setattr(ctx.physics, param, old_val + delta)
                    ctx.record_flux("SIMULATION", param, old_val, old_val + delta, "COUNCIL_MANDATE")
        return ctx

class CognitionPhase(SimulationPhase):
    def __init__(self, engine_ref):
        super().__init__(engine_ref)
        self.name = "COGNITION"

    def run(self, ctx: CycleContext):
        self.eng.mind.mem.encode(ctx.clean_words, ctx.physics, "GEODESIC")
        ctx.mind_state = self.eng.noetic.think(
            ctx.physics,
            ctx.bio_result,
            self.eng.gordon.inventory,
            self.eng.phys.dynamics.voltage_history,
            self.eng.tick_count
        )
        return ctx


class CycleSimulator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.stabilizer = CycleStabilizer(self.eng.events)
        self.pipeline: List[SimulationPhase] = [
            ObservationPhase(engine_ref),
            MaintenancePhase(engine_ref),
            GatekeeperPhase(engine_ref),
            MetabolismPhase(engine_ref),
            RealityFilterPhase(engine_ref),
            NavigationPhase(engine_ref),
            MachineryPhase(engine_ref),
            IntrusionPhase(engine_ref),
            SoulPhase(engine_ref),
            CognitionPhase(engine_ref)
        ]

    def run_simulation(self, ctx: CycleContext) -> CycleContext:
        for phase in self.pipeline:
            if not self._check_circuit_breaker(phase.name):
                continue
            if ctx.refusal_triggered or (ctx.is_bureaucratic and phase.name not in ["OBSERVE", "GATEKEEP"]):
                break
            if not ctx.is_alive:
                break
            current_checkpoint = ctx.physics.snapshot()
            try:
                ctx = phase.run(ctx)
                self.stabilizer.stabilize(ctx, phase.name)
            except Exception as e:
                print(f"{Prisma.YEL}>>> ROLLING BACK TIME ({phase.name} Failed){Prisma.RST}")
                ctx.physics = current_checkpoint
                self._handle_phase_crash(ctx, phase.name, e)
                break
        return ctx

    def _check_circuit_breaker(self, phase_name: str) -> bool:
        """Returns False if a subsystem required for this phase is offline."""
        health = self.eng.system_health
        if phase_name == "OBSERVE" and not health.physics_online: return False
        if phase_name == "METABOLISM" and not health.bio_online: return False
        if phase_name == "COGNITION" and not health.mind_online: return False
        return True

    def _handle_phase_crash(self, ctx, phase_name, error):
        print(f"\n{Prisma.RED}!!! CRITICAL {phase_name} CRASH !!!{Prisma.RST}")
        traceback.print_exc()
        component_map = {
            "OBSERVE": "PHYSICS",
            "METABOLISM": "BIO",
            "COGNITION": "MIND"
        }
        comp = component_map.get(phase_name, "SIMULATION")
        self.eng.system_health.report_failure(comp, error)
        print(f"{Prisma.YEL}>>> STATE DRIFT DETECTED:{Prisma.RST}")
        print(ctx.physics.diff_view(current_checkpoint))
        if comp == "PHYSICS":
            ctx.physics = PanicRoom.get_safe_physics()
        elif comp == "BIO":
            ctx.bio_result = PanicRoom.get_safe_bio()
            ctx.is_alive = True
        elif comp == "MIND":
            ctx.mind_state = PanicRoom.get_safe_mind()
        ctx.log(f"{Prisma.RED}⚠ {phase_name} FAILURE: Switching to Panic Protocol.{Prisma.RST}")

class CycleReporter:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.vsl_chroma = ChromaScope()
        self.strunk_white = TownHall.StrunkWhite()
        self.renderer = GeodesicRenderer(
            self.eng,
            self.vsl_chroma,
            self.strunk_white,
            RuptureValve(self.eng.mind.lex, self.eng.mind.mem)
        )

    def render_snapshot(self, ctx: CycleContext) -> Dict[str, Any]:
        try:
            if ctx.refusal_triggered and ctx.refusal_packet:
                return ctx.refusal_packet
            if ctx.is_bureaucratic:
                return self._package_bureaucracy(ctx)
            self._inject_flux_readout(ctx)
            captured_events = self.eng.events.flush()
            return self.renderer.render_frame(ctx, self.eng.tick_count, captured_events)
        except Exception as e:
            return {
                "type": "CRITICAL_RENDER_FAIL",
                "ui": f"{Prisma.RED}REALITY FRACTURE (Renderer Crash): {e}{Prisma.RST}\nRaw Output: {ctx.logs}",
                "logs": ctx.logs,
                "metrics": self.eng.get_metrics()
            }

    @staticmethod
    def _inject_flux_readout(ctx: CycleContext):
        if not ctx.flux_log:
            return
        flux_lines = []
        for entry in ctx.flux_log[-5:]:
            m = entry['metric'].upper()
            d = entry['delta']
            r = entry['reason']
            icon = "⚡" if m == "VOLTAGE" else "⚓"
            color = Prisma.GRN if d > 0 else Prisma.RED
            arrow = "▲" if d > 0 else "▼"
            line = (
                f"{Prisma.GRY}[FLUX]{Prisma.RST} "
                f"{icon} {m[:3]} {entry['initial']:.1f} "
                f"{color}{arrow} {abs(d):.1f}{Prisma.RST} -> "
                f"{Prisma.WHT}{entry['final']:.1f}{Prisma.RST} "
                f"({r})"
            )
            flux_lines.append(line)
        if flux_lines:
            ctx.logs.insert(0, "")
            for line in reversed(flux_lines):
                ctx.logs.insert(0, line)
            ctx.logs.insert(0, f"{Prisma.CYN}--- LIVE STATE MIRROR ---{Prisma.RST}")

    def _package_bureaucracy(self, ctx: CycleContext):
        return {
            "type": "BUREAUCRACY",
            "ui": ctx.bureau_ui,
            "logs": self.renderer.compose_logs(ctx.logs, self.eng.events.flush(), self.eng.tick_count),
            "metrics": self.eng.get_metrics(ctx.bio_result.get("atp", 0.0))
        }

class GeodesicOrchestrator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.simulator = CycleSimulator(engine_ref)
        self.reporter = CycleReporter(engine_ref)

    def run_turn(self, user_message: str) -> Dict[str, Any]:
        ctx = CycleContext(input_text=user_message)
        ctx.user_name = self.eng.user_name
        self.eng.events.flush()
        ctx = self.simulator.run_simulation(ctx)
        if not ctx.is_alive:
            return self.eng.trigger_death(ctx.physics)
        return self.reporter.render_snapshot(ctx)