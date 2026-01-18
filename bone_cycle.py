# bone_cycle.py
# "The wheel turns, and ages come and pass." - Jordan
import math
import traceback, random, time
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from bone_bus import Prisma, BoneConfig, CycleContext
from bone_village import TownHall
from bone_personality import TheBureau
from bone_physics import TheBouncer, RuptureValve, ChromaScope
from bone_viewer import GeodesicRenderer
from bone_architect import PanicRoom

# --- LAYER 1: THE ENGINE (Simulation Logic) ---

class CycleStabilizer:
    def __init__(self, events_ref):
        self.events = events_ref
        self.MAX_DELTA_V = 5.0
        self.MAX_DELTA_D = 3.0
        self.last_voltage: float = 0.0
        self.last_drag: float = 0.0
        self.last_phase: str = "INIT"

    def _get_current_metrics(self, ctx: CycleContext) -> Tuple[float, float]:
        if not ctx.physics:
            return 0.0, 0.0
        if isinstance(ctx.physics, dict):
            v = ctx.physics.get("voltage", 0.0)
            d = ctx.physics.get("narrative_drag", 0.0)
        else:
            v = getattr(ctx.physics, "voltage", 0.0)
            d = getattr(ctx.physics, "narrative_drag", 0.0)
        return v, d

    def _apply_correction(self, ctx: CycleContext, key: str, correction: float):
        if isinstance(ctx.physics, dict):
            ctx.physics[key] += correction
        else:
            current = getattr(ctx.physics, key)
            setattr(ctx.physics, key, current + correction)

    def stabilize(self, ctx: CycleContext, current_phase: str):
        curr_v, curr_d = self._get_current_metrics(ctx)
        delta_v = curr_v - self.last_voltage
        delta_d = curr_d - self.last_drag
        corrections = []
        if abs(delta_v) > self.MAX_DELTA_V:
            excess = delta_v - (math.copysign(self.MAX_DELTA_V, delta_v))
            damping = -(excess * 0.8)
            self._apply_correction(ctx, "voltage", damping)
            corrections.append(f"Voltage Damped ({damping:+.1f}v)")
            curr_v += damping
        if abs(delta_d) > self.MAX_DELTA_D:
            excess = delta_d - (math.copysign(self.MAX_DELTA_D, delta_d))
            damping = -(excess * 0.8)
            self._apply_correction(ctx, "narrative_drag", damping)
            corrections.append(f"Drag Stabilized ({damping:+.1f})")
            curr_d += damping
        if corrections:
            joined_msg = ", ".join(corrections)
            self.events.log(
                f"{Prisma.CYN}⚖️ GYROSCOPE: Phase '{current_phase}' instability detected. {joined_msg}.{Prisma.RST}",
                "SYS"
            )
        self.last_voltage = curr_v
        self.last_drag = curr_d
        self.last_phase = current_phase

class CycleSimulator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.bureau = TheBureau()
        self.bouncer = TheBouncer(self.eng)
        self.vsl_32v = RuptureValve(self.eng.mind.lex, self.eng.mind.mem)
        self.stabilizer = CycleStabilizer(self.eng.events)

    def run_simulation(self, ctx: CycleContext) -> CycleContext:
        try:
            if self.eng.system_health.physics_online:
                self._phase_observe(ctx)
                self.stabilizer.stabilize(ctx, "OBSERVE") # Checkpoint 1
            else:
                raise Exception("Physics module previously failed.")
        except Exception as e:
            self._handle_critical_failure(ctx, "PHYSICS", e, PanicRoom.get_safe_physics)
        if self.eng.tick_count % 10 == 0:
            self._maintenance_prune(ctx)
        if self.eng.system_health.physics_online:
            try:
                if self._phase_gatekeep(ctx):
                    self.stabilizer.stabilize(ctx, "GATEKEEP")
                    return ctx
            except Exception as e:
                ctx.log(f"{Prisma.YEL}GATEKEEPER ASLEEP: {e}{Prisma.RST}")
        try:
            if self.eng.system_health.bio_online:
                self._phase_metabolize(ctx)
                self.stabilizer.stabilize(ctx, "METABOLISM")
            else:
                raise Exception("Bio module previously failed.")
        except Exception as e:
            self._handle_critical_failure(ctx, "BIO", e, PanicRoom.get_safe_bio, is_bio=True)
        if not ctx.is_alive:
            return ctx
        try:
            self._phase_simulate(ctx)
            self.stabilizer.stabilize(ctx, "SIMULATION")
        except Exception as e:
            ctx.log(f"{Prisma.RED}SIMULATION GLITCH: {e}{Prisma.RST}")
        try:
            if self.eng.system_health.mind_online:
                self._phase_cognate(ctx)
            else:
                raise Exception("Mind module previously failed.")
        except Exception as e:
            self._handle_critical_failure(ctx, "MIND", e, PanicRoom.get_safe_mind, is_mind=True)
        return ctx

    def _tend_garden(self, ctx: CycleContext):
        eff_boost, zen_msg = self.eng.zen.raking_the_sand(ctx.physics, ctx.bio_result)
        if zen_msg:
            ctx.log(zen_msg)
        if eff_boost > 0:
            current_eff = self.eng.bio.mito.state.efficiency_mod
            self.eng.bio.mito.state.efficiency_mod = min(2.0, current_eff + (eff_boost * 0.1))

    def _handle_critical_failure(self, ctx, component, error, panic_func, is_bio=False, is_mind=False):
        print(f"\n{Prisma.RED}!!! CRITICAL {component} CRASH !!!{Prisma.RST}")
        traceback.print_exc()
        self.eng.system_health.report_failure(component, error)
        if is_bio:
            ctx.bio_result = panic_func()
            ctx.is_alive = True
        elif is_mind:
            ctx.mind_state = panic_func()
        else:
            ctx.physics = panic_func()
        ctx.log(f"{Prisma.RED}⚠ {component} FAILURE: Switching to Panic Protocol.{Prisma.RST}")

    def _phase_observe(self, ctx: CycleContext):
        gaze_result = self.eng.phys.tension.gaze(ctx.input_text, self.eng.mind.mem.graph)
        ctx.physics = gaze_result["physics"]
        ctx.clean_words = gaze_result["clean_words"]
        self.eng.phys.tension.last_physics_packet = ctx.physics
        self.eng.tick_count += 1
        rupture = self.vsl_32v.analyze(ctx.physics)
        if rupture:
            ctx.log(rupture["log"])

    def _maintenance_prune(self, ctx: CycleContext):
        try:
            rotted = self.eng.lex.atrophy(self.eng.tick_count, 100)
            if rotted:
                for w in rotted:
                    self.eng.limbo.ghosts.append(f"👻{w.upper()}_ECHO")
                example = rotted[0]
                ctx.log(f"{Prisma.GRY}NEURO-PRUNING: {len(rotted)} concepts decayed (e.g., '{example}').{Prisma.RST}")
            self.eng.mind.mem.enforce_limits(self.eng.tick_count)
        except Exception as e:
            if BoneConfig.VERBOSE_LOGGING:
                print(f"Maintenance Error: {e}")

    def _phase_gatekeep(self, ctx: CycleContext) -> bool:
        is_allowed_entry, refusal_packet = self.bouncer.check_entry(ctx)
        if not is_allowed_entry:
            ctx.refusal_triggered = True
            ctx.refusal_packet = refusal_packet
            return True

        audit_result = self.bureau.audit(ctx.physics, ctx.bio_result)
        if audit_result:
            self.eng.bio.mito.state.atp_pool += audit_result.get("atp_gain", 0.0)
            ctx.log(audit_result["log"])
            status = audit_result.get("status")
            if status == "BLOCK":
                ctx.is_bureaucratic = True
                ctx.physics["narrative_drag"] = 10.0
                ctx.physics["voltage"] = 0.0
                ctx.bureau_ui = audit_result["ui"]
                return True
            elif status == "TAX":
                ctx.log(f"{Prisma.GRY}   (BUREAU TAX DEDUCTED...){Prisma.RST}")
        return False

    def _phase_metabolize(self, ctx: CycleContext):
        physics = ctx.physics
        gov_msg = self.eng.bio.governor.shift(
            physics,
            self.eng.phys.dynamics.voltage_history,
            self.eng.tick_count
        )
        if gov_msg: self.eng.events.log(gov_msg, "GOV")
        bio_feedback = {
            "INTEGRITY": physics.get("truth_ratio", 0.0),
            "STATIC": physics.get("repetition", 0.0),
            "FORCE": physics.get("voltage", 0.0) / 20.0,
            "BETA": physics.get("beta_index", 1.0)
        }
        stress_mod = self.eng.bio.governor.get_stress_modifier(self.eng.tick_count)
        circadian_bias = None
        if self.eng.tick_count % 10 == 0:
            circadian_bias, circadian_msg = self.eng.bio.endo.calculate_circadian_bias()
            if circadian_msg:
                self.eng.events.log(f"{Prisma.CYN}🕒 {circadian_msg}{Prisma.RST}", "BIO")
        ctx.bio_result = self.eng.soma.digest_cycle(
            ctx.input_text, physics, bio_feedback,
            self.eng.health, self.eng.stamina, stress_mod, self.eng.tick_count,
            circadian_bias=circadian_bias
        )
        ctx.is_alive = ctx.bio_result["is_alive"]
        for bio_item in ctx.bio_result["logs"]:
            if any(x in str(bio_item) for x in ["CRITICAL", "TAX", "Poison"]):
                ctx.log(bio_item)
        hubris_hit, hubris_msg, event_type = self.eng.phys.tension.audit_hubris(physics, self.eng.lex)
        if hubris_hit:
            ctx.log(hubris_msg)
            if event_type == "FLOW_BOOST":
                self.eng.bio.mito.state.atp_pool += 20.0
            elif event_type == "ICARUS_CRASH":
                damage = 15.0
                self.eng.health -= damage
                ctx.log(f"   {Prisma.RED}IMPACT TRAUMA: -{damage} HP.{Prisma.RST}")
        self._apply_healing_logic(ctx)

    def _apply_healing_logic(self, ctx: CycleContext):
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

    def _phase_simulate(self, ctx: CycleContext):
        self._apply_reality_filters(ctx)
        self._process_navigation(ctx)
        self._process_cosmic_state(ctx)
        self._tend_garden(ctx)
        self._operate_machinery(ctx)
        self._process_intrusions(ctx)
        self._phase_soul_work(ctx)
        if self.eng.gordon.inventory:
            self.eng.tinkerer.audit_tool_use(ctx.physics, self.eng.gordon.inventory)
        council_advice, adjustments = self.eng.council.convene(ctx.input_text, ctx.physics)
        for advice in council_advice:
            ctx.log(advice)
        if adjustments:
            for param, delta in adjustments.items():
                if param in ctx.physics:
                    ctx.physics[param] += delta

    def _phase_soul_work(self, ctx: CycleContext):
        lesson = self.eng.soul.crystallize_memory(ctx.physics, ctx.bio_result, self.eng.tick_count)
        if not self.eng.soul.current_obsession:
            self.eng.soul.find_obsession(self.eng.lex)
        self.eng.soul.pursue_obsession(ctx.physics)

    def _apply_reality_filters(self, ctx: CycleContext):
        reflection = self.eng.mind.mirror.get_reflection_modifiers()
        ctx.physics["narrative_drag"] *= reflection["drag_mult"]
        if reflection.get("atp_tax", 0) > 0:
            tax = reflection["atp_tax"]
            self.eng.bio.mito.state.atp_pool -= tax
            if random.random() < 0.2:
                ctx.log(f"{Prisma.RED}MIRROR TAX: -{tax:.1f} ATP applied.{Prisma.RST}")
        cap = reflection.get("voltage_cap", 999.0)
        if ctx.physics["voltage"] > cap:
            ctx.physics["voltage"] = cap
            ctx.log(f"{Prisma.GRY}MIRROR: Voltage capped at {cap}.{Prisma.RST}")
        trigram_data = self.vsl_32v.geodesic.resolve_trigram(ctx.physics.get("vector", {}))
        ctx.world_state["trigram"] = trigram_data
        if random.random() < 0.05:
            t_sym, t_name = trigram_data["symbol"], trigram_data["name"]
            ctx.log(f"{trigram_data['color']}I CHING: {t_sym} {t_name} is in the ascendant.{Prisma.RST}")

    def _process_navigation(self, ctx: CycleContext):
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

    def _process_cosmic_state(self, ctx: CycleContext):
        physics = ctx.physics
        orbit_state, drag_pen, orbit_msg = self.eng.cosmic.analyze_orbit(self.eng.mind.mem, ctx.clean_words)
        raw_zone = physics.get("zone", "COURTYARD")
        stabilized_zone = self.eng.stabilizer.stabilize(raw_zone, physics, (orbit_state, drag_pen))
        adjusted_drag = self.eng.stabilizer.override_cosmic_drag(drag_pen, stabilized_zone)
        physics["zone"] = stabilized_zone
        self.eng.apply_cosmic_physics(physics, orbit_state, adjusted_drag)
        ctx.world_state["orbit"] = orbit_state
        if orbit_msg: ctx.log(orbit_msg)

    def _operate_machinery(self, ctx: CycleContext):
        physics = ctx.physics
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

    def _process_intrusions(self, ctx: CycleContext):
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
            ctx.physics["psi"] = min(1.0, ctx.physics["psi"] + 0.3)

    def _phase_cognate(self, ctx: CycleContext):
        self.eng.mind.mem.encode(ctx.clean_words, ctx.physics, "GEODESIC")
        ctx.mind_state = self.eng.noetic.think(
            ctx.physics,
            ctx.bio_result,
            self.eng.gordon.inventory,
            self.eng.phys.dynamics.voltage_history,
            self.eng.tick_count
        )

# --- LAYER 2: THE REPORTER (View Logic) ---

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
            captured_events = self.eng.events.flush()
            return self.renderer.render_frame(ctx, self.eng.tick_count, captured_events)
        except Exception as e:
            return {
                "type": "CRITICAL_RENDER_FAIL",
                "ui": f"{Prisma.RED}REALITY FRACTURE (Renderer Crash): {e}{Prisma.RST}\nRaw Output: {ctx.logs}",
                "logs": ctx.logs,
                "metrics": self.eng.get_metrics()
            }

    def _package_bureaucracy(self, ctx: CycleContext):
        return {
            "type": "BUREAUCRACY",
            "ui": ctx.bureau_ui,
            "logs": self.renderer.compose_logs(ctx.logs, self.eng.events.flush(), self.eng.tick_count),
            "metrics": self.eng.get_metrics(ctx.bio_result.get("atp", 0.0))
        }

# --- LAYER 3: THE ORCHESTRATOR (Coordinator) ---

class GeodesicOrchestrator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.simulator = CycleSimulator(engine_ref)
        self.reporter = CycleReporter(engine_ref)

    def run_turn(self, user_message: str) -> Dict[str, Any]:
        ctx = CycleContext(input_text=user_message)
        ctx.user_name = self.eng.user_name
        self.eng.events.flush() # Clear bus
        ctx = self.simulator.run_simulation(ctx)
        if not ctx.is_alive:
            return self.eng.trigger_death(ctx.physics)
        return self.reporter.render_snapshot(ctx)