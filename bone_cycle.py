# bone_cycle.py
# "The wheel turns, and ages come and pass." - Jordan

import traceback, random
from typing import Dict, Any
from bone_bus import Prisma, BoneConfig, CycleContext
from bone_village import TownHall
from bone_personality import TheBureau
from bone_physics import TheBouncer, RuptureValve, ChromaScope
from bone_viewer import GeodesicRenderer
from bone_architect import PanicRoom

class GeodesicOrchestrator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.bureau = TheBureau()
        self.bouncer = TheBouncer(self.eng)
        self.parks = TownHall.PublicParksDepartment()
        self.vsl_32v = RuptureValve(self.eng.mind.lex, self.eng.mind.mem)
        self.vsl_chroma = ChromaScope()
        self.strunk_white = TownHall.StrunkWhite()
        self.renderer = GeodesicRenderer(
            self.eng,
            self.vsl_chroma,
            self.strunk_white,
            self.vsl_32v
        )

    def run_turn(self, user_message: str) -> Dict[str, Any]:
        self.eng.events.flush()
        ctx = CycleContext(input_text=user_message)
        ctx.user_name = self.eng.user_name
        try:
            if self.eng.system_health.physics_online:
                self._phase_observe(ctx)
            else:
                raise Exception("Physics module previously failed.")
        except Exception as e:
            print(f"\n{Prisma.RED}!!! CRITICAL PHYSICS CRASH !!!{Prisma.RST}")
            traceback.print_exc()
            self.eng.system_health.report_failure("PHYSICS", e)
            ctx.physics = PanicRoom.get_safe_physics()
            ctx.log(f"{Prisma.RED}⚠ PHYSICS FAILURE: Switching to Newtonian Defaults.{Prisma.RST}")
        if self.eng.tick_count % 10 == 0:
            try:
                self._maintenance_prune(ctx)
            except Exception:
                pass
        if self.eng.system_health.physics_online:
            try:
                if self._phase_gatekeep(ctx):
                    return ctx.refusal_packet or self._package_bureaucracy(ctx)
            except Exception as e:
                ctx.log(f"{Prisma.YEL}GATEKEEPER ASLEEP: {e}{Prisma.RST}")
        try:
            if self.eng.system_health.bio_online:
                self._phase_metabolize(ctx)
            else:
                raise Exception("Bio module previously failed.")
        except Exception as e:
            self.eng.system_health.report_failure("BIO", e)
            ctx.bio_result = PanicRoom.get_safe_bio()
            ctx.is_alive = True
        if not ctx.is_alive:
            return self.eng.trigger_death(ctx.physics)
        try:
            self._phase_simulate(ctx)
        except Exception as e:
            ctx.log(f"{Prisma.RED}SIMULATION GLITCH: {e}{Prisma.RST}")
        try:
            if self.eng.system_health.mind_online:
                self._phase_cognate(ctx)
            else:
                raise Exception("Mind module previously failed.")
        except Exception as e:
            self.eng.system_health.report_failure("MIND", e)
            ctx.mind_state = PanicRoom.get_safe_mind()
        try:
            return self._phase_render(ctx)
        except Exception as e:
            return {
                "type": "CRITICAL_RENDER_FAIL",
                "ui": f"{Prisma.RED}REALITY FRACTURE.{Prisma.RST}\nRaw Output: {ctx.logs}",
                "logs": ctx.logs,
                "metrics": self.eng.get_metrics()
            }

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

    def _package_bureaucracy(self, ctx):
        return {
            "type": "BUREAUCRACY",
            "ui": ctx.bureau_ui,
            "logs": self.renderer.compose_logs(ctx.logs, self.eng.events.flush(), self.eng.tick_count),
            "metrics": self.eng.get_metrics(ctx.bio_result.get("atp", 0.0))
        }

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

    def _phase_render(self, ctx: CycleContext) -> Dict[str, Any]:
        captured_events = self.eng.events.flush()
        return self.renderer.render_frame(ctx, self.eng.tick_count, captured_events)