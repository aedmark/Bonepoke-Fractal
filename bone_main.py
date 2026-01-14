# BONEAMANITA 9.9.1 - "THE REALITY DYSFUNCTION"
# Architects: SLASH, KICHO, Taylor & Edmark

import json, os, random, re, time, math, copy, traceback
from collections import Counter, deque
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, field
from bone_commands import CommandProcessor
from bone_village import TheLexicon, CycleContext, DeathGen, TheTensionMeter, TemporalDynamics, ApeirogonResonance, MirrorGraph, TheHoloProjector, SoritesIntegrator, TheCrucible, TheForge, TheTheremin, TheNavigator, LiteraryJournal, TheAlmanac, StrunkWhiteProtocol, TheTinkerer, TheCartographer
from bone_data import LENSES
from bone_inventory import GordonKnot
from bone_spores import MycotoxinFactory, LichenSymbiont, HyphalInterface, ParasiticSymbiont, MycelialNetwork, SporeCasing, LocalFileSporeLoader
from bone_body import BioSystem, MitochondrialForge, EndocrineSystem, MetabolicGovernor, SomaticLoop, ViralTracer, ThePacemaker, NoeticLoop
from bone_physics import TheBouncer, VSL_32Valve, VSL_ChromaticController, CosmicDynamics, TheTangibilityGate
from bone_brain import NeuroPlasticity, DreamEngine, TheCortex, ShimmerState, LLMInterface
from bone_personality import UserProfile, EnneagramDriver, SynergeticLensArbiter, PublicParksDepartment, TherapyProtocol, KintsugiProtocol, LimboLayer, TheFolly, ChorusDriver, CassandraProtocol, TheBureau
from bone_viewer import GeodesicRenderer
from bone_bus import EventBus, Prisma, BoneConfig
from bone_lexicon import TheLexicon, LiteraryReproduction


@dataclass
class MindSystem:
    mem: MycelialNetwork
    lex: Any
    dreamer: DreamEngine
    mirror: MirrorGraph
    wise: ApeirogonResonance
    tracer: ViralTracer
    integrator: SoritesIntegrator

@dataclass
class PhysSystem:
    tension: 'TheTensionMeter'
    forge: 'TheForge'
    crucible: 'TheCrucible'
    theremin: 'TheTheremin'
    pulse: 'ThePacemaker'
    gate: 'TheTangibilityGate'
    dynamics: 'TemporalDynamics'
    nav: 'TheNavigator'

class GeodesicOrchestrator:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.bureau = TheBureau()
        self.bouncer = TheBouncer(self.eng)
        self.parks = PublicParksDepartment()
        self.vsl_32v = VSL_32Valve(self.eng.mind.lex, self.eng.mind.mem)
        self.vsl_chroma = VSL_ChromaticController()
        self.strunk_white = StrunkWhiteProtocol()
        self.renderer = GeodesicRenderer(
            self.eng,
            self.vsl_chroma,
            self.strunk_white,
            self.vsl_32v
        )

    def run_turn(self, user_message: str) -> Dict[str, Any]:
        self.eng.events.flush()
        ctx = CycleContext(input_text=user_message)
        try:
            self._phase_observe(ctx)

            if self.eng.tick_count % 10 == 0:
                self._maintenance_prune(ctx)

            if self._phase_gatekeep(ctx):
                return ctx.refusal_packet or self._package_bureaucracy(ctx)

            self._phase_metabolize(ctx)

            if not ctx.is_alive:
                return self.eng._trigger_death(ctx.physics)

            self._phase_simulate(ctx)

            self._phase_cognate(ctx)

            return self._phase_render(ctx)

        except Exception as e:
            traceback.print_exc()
            return {
                "type": "CRITICAL_FAILURE",
                "ui": f"{Prisma.RED}SYSTEM PANIC: Geodesic Strut Failure.\n{e}{Prisma.RST}",
                "logs": ctx.logs,
                "metrics": self.eng._get_metrics()
            }

    def _phase_observe(self, ctx: CycleContext):
        """Calculates 'Physics' from raw text."""
        gaze_result = self.eng.phys.tension.gaze(ctx.input_text, self.eng.mind.mem.graph)
        ctx.physics = gaze_result["physics"]
        ctx.clean_words = gaze_result["clean_words"]

        self.eng.phys.tension.last_physics_packet = ctx.physics
        self.eng.tick_count += 1

        mirror_active, mirror_msg = self.eng.mind.mirror.reflect(ctx.physics)
        if mirror_active and mirror_msg:
            ctx.log(f"{Prisma.CYN}🪞 {mirror_msg}{Prisma.RST}")

        rupture = self.vsl_32v.analyze(ctx.physics)
        if rupture:
            ctx.log(rupture["log"])

    def _maintenance_prune(self, ctx: CycleContext):
        """Cleans up old concepts from the Lexicon."""
        try:
            rotted = self.eng.lex.atrophy(self.eng.tick_count, 100)
            if rotted:
                for w in rotted: 
                    self.eng.limbo.ghosts.append(f"👻{w.upper()}_ECHO")
                
                example = rotted[0]
                ctx.log(f"{Prisma.GRY}NEURO-PRUNING: {len(rotted)} concepts decayed (e.g., '{example}').{Prisma.RST}")
        except Exception: 
            pass

    def _phase_gatekeep(self, ctx: CycleContext) -> bool:
        allowed, refusal_packet = self.bouncer.check_entry(ctx)
        if not allowed:
            ctx.refusal_triggered = True
            ctx.refusal_packet = refusal_packet
            return True

        bureau_result = self.bureau.audit(ctx.physics, ctx.bio_result)
        
        if bureau_result:
            self.eng.bio.mito.state.atp_pool += bureau_result["atp_gain"]
            ctx.log(bureau_result["log"])

            if bureau_result["status"] == "BLOCK":
                ctx.is_bureaucratic = True
                ctx.physics["narrative_drag"] = 10.0 
                ctx.physics["voltage"] = 0.0         
                ctx.bureau_ui = bureau_result["ui"]
                return True

            elif bureau_result["status"] == "TAX":
                ctx.log(f"{Prisma.GRY}   (BUREAU TAX APPLIED: Flow continues...){Prisma.RST}")
            
        return False

    def _package_bureaucracy(self, ctx):
        return {
            "type": "BUREAUCRACY",
            "ui": ctx.bureau_ui,
            "logs": self._compose_logs(ctx.logs + [e['text'] for e in self.eng.events.flush()]),
            "metrics": self.eng._get_metrics(ctx.bio_result.get("atp", 0.0))
        }

    def _phase_metabolize(self, ctx: CycleContext):
        physics = ctx.physics

        gov_msg = self.eng.bio.governor.shift(physics, self.eng.phys.dynamics.voltage_history)
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

        for log in ctx.bio_result["logs"]:
            if any(x in str(log) for x in ["CRITICAL", "TAX", "Poison"]):
                ctx.log(log)

        hubris_hit, hubris_msg, event_type = self.eng.phys.tension.audit_hubris(physics, self.eng.lex)
        if hubris_hit:
            ctx.log(hubris_msg)
            if event_type == "FLOW_BOOST":
                self.eng.bio.mito.state.atp_pool += 20.0

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
        """The Physics Simulation Layer."""
        self._apply_reality_filters(ctx)

        self._process_navigation(ctx)

        self._process_cosmic_state(ctx)

        self._operate_machinery(ctx)

        self._process_intrusions(ctx)

        if self.eng.gordon.inventory:
            self.eng.tinkerer.audit_tool_use(ctx.physics, self.eng.gordon.inventory)

    def _apply_reality_filters(self, ctx: CycleContext):
        """Handle Mirror Mode and I Ching Trigrams."""
        text_for_mirror = " ".join(ctx.clean_words)
        self.eng.mind.mirror.profile_input(text_for_mirror, ctx.physics)

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
        """Handle movement, gravity, and location."""
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
        """Handle orbital mechanics and zone inertia."""
        physics = ctx.physics
        orbit_state, drag_pen, orbit_msg = self.eng.cosmic.analyze_orbit(self.eng.mind.mem, ctx.clean_words)

        raw_zone = physics.get("zone", "COURTYARD")
        stabilized_zone = self.eng.stabilizer.stabilize(raw_zone, physics, (orbit_state, drag_pen))
        adjusted_drag = self.eng.stabilizer.override_cosmic_drag(drag_pen, stabilized_zone)
        physics["zone"] = stabilized_zone
        self.eng._apply_cosmic_physics(physics, orbit_state, adjusted_drag)
        ctx.world_state["orbit"] = orbit_state
        if orbit_msg: ctx.log(orbit_msg)

    def _operate_machinery(self, ctx: CycleContext):
        """Industrial Operations."""
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
        """Handle parasites, ghosts, and pareidolia."""
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
        """The Cognitive Layer."""
        self.eng.mind.mem.encode(ctx.clean_words, ctx.physics, "GEODESIC")

        ctx.mind_state = self.eng.noetic.think(
            ctx.physics, ctx.bio_result, self.eng.gordon.inventory,
            self.eng.phys.dynamics.voltage_history
        )

    def _phase_render(self, ctx: CycleContext) -> Dict[str, Any]:
        return self.renderer.render_frame(ctx)
        
class BoneAmanita:
    def __init__(self, memory_layer=None, lexicon_layer=None):
        local_brain = LLMInterface(
            provider="ollama",
            base_url="http://localhost:11434/v1/chat/completions",
            model="llama3"
        )
        cloud_brain = LLMInterface(
            provider="openai",
            api_key="sk-YOUR-ACTUAL-OPENAI-KEY-HERE",
            model="gpt-4-turbo"
        )
        self.lex = lexicon_layer if lexicon_layer else TheLexicon
        if hasattr(self.lex, 'initialize'): self.lex.initialize()
        self.lex.compile_antigens()
        DeathGen.load_protocols()
        LiteraryReproduction.load_genetics()
        self.events = EventBus()
        self.shimmer_state = ShimmerState()
        self.navigator = TheNavigator(self.shimmer_state)
        self.journal = LiteraryJournal()
        _mem = memory_layer if memory_layer else MycelialNetwork(self.events)
        self.mind = MindSystem(
            mem=_mem, lex=self.lex, dreamer=DreamEngine(self.events),
            mirror=MirrorGraph(), wise=ApeirogonResonance(self.events),
            tracer=ViralTracer(_mem), integrator=SoritesIntegrator(_mem))
        self.limbo = LimboLayer()
        self.mind.mem.cleanup_old_sessions(self.limbo)
        load_result = self.mind.mem.autoload_last_spore()
        inherited_traits = load_result[0] if load_result else {}
        inherited_antibodies = load_result[1] if load_result else set()
        immune_system = MycotoxinFactory()
        immune_system.active_antibodies = inherited_antibodies
        self.bio = BioSystem(mito=MitochondrialForge(self.mind.mem.session_id, self.events, inherited_traits),
                             endo=EndocrineSystem(), immune=immune_system, lichen=LichenSymbiont(),
                             gut=HyphalInterface(), plasticity=NeuroPlasticity(), governor=MetabolicGovernor(),
                             shimmer=self.shimmer_state, parasite=ParasiticSymbiont(self.mind.mem, self.lex))
        self.phys = PhysSystem(
            tension=TheTensionMeter(self.events), forge=TheForge(), crucible=TheCrucible(),
            theremin=TheTheremin(), pulse=ThePacemaker(), gate=TheTangibilityGate(),
            dynamics=TemporalDynamics(), nav=self.navigator)
        self.repro = LiteraryReproduction()
        self.projector = TheHoloProjector()
        self.gordon = GordonKnot()
        self.kintsugi = KintsugiProtocol()
        self.therapy = TherapyProtocol()
        self.folly = TheFolly()
        self.cosmic = CosmicDynamics()
        self.cmd = CommandProcessor(self, Prisma, self.lex, BoneConfig, TheCartographer)
        self.cassandra = CassandraProtocol(self)
        self.director = ChorusDriver()
        self.tinkerer = TheTinkerer(self.gordon, self.events)
        self.almanac = TheAlmanac()
        self.soma = SomaticLoop(self.bio, self.mind.mem, self.lex, self.gordon, self.folly, self.events)
        self.noetic = NoeticLoop(self.mind, self.bio, self.events)
        self.tick_count = 0
        self.health = self.mind.mem.session_health if self.mind.mem.session_health else BoneConfig.MAX_HEALTH
        self.stamina = self.mind.mem.session_stamina if self.mind.mem.session_stamina else BoneConfig.MAX_STAMINA
        self.trauma_accum = self.mind.mem.session_trauma_vector if hasattr(self.mind.mem, 'session_trauma_vector') and self.mind.mem.session_trauma_vector else BoneConfig.TRAUMA_VECTOR.copy()
        self.joy_history = []
        self.cycle_controller = GeodesicOrchestrator(self)
        self.cortex = TheCortex(self, llm_client=local_brain)

    def _get_avg_voltage(self):
        hist = self.phys.dynamics.voltage_history
        if not hist: return 0.0
        return sum(hist) / len(hist)

    def process_turn(self, user_message: str) -> Dict[str, Any]:
        cmd_response = self._phase_check_commands(user_message)
        if cmd_response:
            return cmd_response
        if self._ethical_audit():
            self.events.log(f"{Prisma.WHT}MERCY SIGNAL: Trauma boards wiped.{Prisma.RST}", "SYS")
        return self.cortex.process(user_message)

    def _phase_check_commands(self, user_message):
        if user_message.strip().startswith("/"):
            self.cmd.execute(user_message)
            cmd_logs = [e['text'] for e in self.events.flush()]
            return {
                "type": "COMMAND",
                "ui": f"\n{Prisma.GRY}Command Processed.{Prisma.RST}",
                "logs": cmd_logs if cmd_logs else ["Command Executed."],
                "metrics": self._get_metrics()}
        return None

    def _trigger_death(self, last_phys) -> Dict:
        eulogy = DeathGen.eulogy(last_phys, self.bio.mito.state)
        death_log = [f"\n{Prisma.RED}SYSTEM HALT: {eulogy}{Prisma.RST}"]
        try:
            spore_data = {
                "session_id": self.mind.mem.session_id,
                "meta": {"timestamp": time.time(), "final_health": 0, "final_stamina": self.stamina},
                "trauma_vector": self.trauma_accum,
                "mitochondria": self.bio.mito.adapt(0),
                "antibodies": list(self.bio.immune.active_antibodies),
                "core_graph": self.mind.mem.graph,
                "tool_adaptation": self.tinkerer.save_state()}
            path = self.mind.mem.loader.save_spore(self.mind.mem.filename, spore_data)
            death_log.append(f"{Prisma.WHT}   [LEGACY SAVED: {path}]{Prisma.RST}")
        except Exception as e:
            death_log.append(f"Save Failed: {e}")
        return {"type": "DEATH", "ui": "\n".join(death_log), "logs": death_log, "metrics": self._get_metrics(0.0)}

    def _package_turn(self, type_str, logs, context):
        event_data = self.events.flush()
        event_texts = [e['text'] for e in event_data]
        logs.extend(event_texts)
        return {
            "type": type_str,
            "ui": "\n".join(logs),
            "logs": logs,
            "metrics": self._get_metrics()}

    def _get_metrics(self, atp=0.0):
        return {"health": self.health, "stamina": self.stamina, "atp": atp, "tick": self.tick_count}

    def _ethical_audit(self):
        trauma_sum = sum(self.trauma_accum.values())
        health_ratio = self.health / BoneConfig.MAX_HEALTH
        desperation = trauma_sum * (1.0 - health_ratio)
        if desperation > 0.7:
            self.events.log(f"{Prisma.WHT}ETHICAL RELEASE: Desperation ({desperation:.2f}) exceeds limits.{Prisma.RST}", "SYS")
            self.trauma_accum = {k:0.0 for k in self.trauma_accum}
            self.health = min(self.health + 30.0, 100.0)
            self.bio.endo.cortisol = 0.0
            self.bio.endo.serotonin = max(0.5, self.bio.endo.serotonin + 0.3)
            return True
        return False

    @staticmethod
    def _apply_cosmic_physics(physics, state, cosmic_drag_penalty):
        physics["narrative_drag"] += cosmic_drag_penalty
        if state == "VOID_DRIFT": physics["voltage"] = max(0.0, physics["voltage"] - 0.5)
        elif state == "LAGRANGE_POINT": physics["narrative_drag"] = max(0.1, physics["narrative_drag"] - 2.0)
        elif state == "WATERSHED_FLOW": physics["voltage"] += 0.5

    @staticmethod
    def check_pareidolia(words):
        return BoneConfig.check_pareidolia(words)

class SessionGuardian:
    def __init__(self, engine_ref):
        self.eng = engine_ref

    def __enter__(self):
        print(f"{Prisma.paint('>>> BONEAMANITA 9.9', 'G')}")
        print(f"{Prisma.paint('System: LISTENING', '0')}")
        return self.eng

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n{Prisma.paint('--- SYSTEM HALT ---', 'R')}")
        if exc_type:
            print(f"{Prisma.paint(f'CRITICAL FAILURE: {exc_val}', 'R')}")
            self.eng.events.log(f"CRASH: {exc_val}", "SYS")
        try:
            print(f"{Prisma.paint('Initiating Emergency Spore Preservation...', 'Y')}")
            if hasattr(self.eng, "mind") and hasattr(self.eng, "bio"):
                spore_data = {
                    "session_id": self.eng.mind.mem.session_id,
                    "meta": {
                        "timestamp": time.time(),
                        "final_health": self.eng.health,
                        "final_stamina": self.eng.stamina,
                        "avg_voltage": self.eng._get_avg_voltage(),
                        "exit_cause": "INTERRUPT" if exc_type else "MANUAL"
                    },
                    "trauma_vector": self.eng.trauma_accum,
                    "mitochondria": self.eng.bio.mito.adapt(self.eng.health),
                    "antibodies": list(self.eng.bio.immune.active_antibodies),
                    "core_graph": self.eng.mind.mem.graph,
                    "config_mutations": self.eng.repro.mutate_config(BoneConfig),
                    "tool_adaptation": self.eng.tinkerer.save_state()}
                filename = f"emergency_{self.eng.mind.mem.session_id}.json"
                saved_path = self.eng.mind.mem.loader.save_spore(filename, spore_data)
                if saved_path:
                    print(f"{Prisma.paint(f'✔ Spore encapsulated: {saved_path}', 'C')}")
                    almanac_report = self.eng.almanac.compile_forecast(spore_data)
                    print(almanac_report)
                else:
                    print(f"{Prisma.paint('✘ Spore encapsulation failed (IO Error).', 'R')}")
            else:
                print(f"{Prisma.paint('⚠ CRITICAL: Brainstem missing. Cannot save spore.', 'R')}")
        except Exception as e:
            print(f"{Prisma.paint(f'FATAL: State corruption during shutdown. {e}', 'R')}")
            traceback.print_exc()
        print(f"{Prisma.paint('Disconnected.', '0')}")
        return exc_type is KeyboardInterrupt

if __name__ == "__main__":
    engine_instance = BoneAmanita()
    with SessionGuardian(engine_instance) as eng:
        while True:
            try:
                u = input(f"{Prisma.paint('>', 'W')} ")
                if not u: continue
            except EOFError:
                break
            if u.lower() in ["exit", "quit", "/exit"]:
                break
            result = eng.process_turn(u)
            if result.get("system_instruction"):
                 print(f"\n{Prisma.paint('--- SYSTEM DIRECTIVE ---', 'M')}")
                 print(f"{Prisma.paint(result['system_instruction'], '0')}")
                 print(f"{Prisma.paint('------------------------', 'M')}\n")
            if result.get("ui"):
                print(result["ui"])
            if result.get("logs") and BoneConfig.VERBOSE_LOGGING:
                print(f"{Prisma.GRY}--- DEBUG LOGS ---{Prisma.RST}")
                for log in result["logs"]:
                    print(log)
            if result["type"] == "DEATH":
                break
