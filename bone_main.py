# BONEAMANITA 10.6.1 - "Surgical Clarity"
# Architects: SLASH, KISHO, The Courtyard, Taylor & Edmark

import time, json
from dataclasses import dataclass
from typing import Dict, Any
from bone_bus import EventBus, Prisma, BoneConfig, SystemHealth, TheObserver
from bone_commands import CommandProcessor
from bone_data import TheAkashicRecord
from bone_village import TownHall
from bone_lexicon import TheLexicon, LiteraryReproduction
from bone_inventory import GordonKnot
from bone_telemetry import TelemetryService
from bone_personality import (
    TheFolly, CassandraProtocol, ChorusDriver, KintsugiProtocol, TherapyProtocol, TheBureau
)
from bone_physics import CosmicDynamics, ZoneInertia
from bone_body import SomaticLoop, NoeticLoop
from bone_brain import TheCortex, LLMInterface
from bone_soul import NarrativeSelf
from bone_architect import BoneArchitect
from bone_cycle import GeodesicOrchestrator

def bootstrap_systems():
    print(f"{Prisma.GRY}...Bootstrapping Sub-Systems...{Prisma.RST}")
    pass

class SessionGuardian:
    def __init__(self, engine_ref):
        # [SLASH PATCH]: Clarity update.
        self.engine_instance = engine_ref

    def __enter__(self):
        print(f"{Prisma.paint('>>> BONEAMANITA 10.6.1', 'G')}")
        print(f"{Prisma.paint('System: LISTENING', '0')}")
        return self.engine_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n{Prisma.paint('--- SYSTEM HALT ---', 'R')}")
        if exc_type:
            print(f"{Prisma.paint(f'CRITICAL FAILURE: {exc_val}', 'R')}")
            if hasattr(self.engine_instance, "events"):
                self.engine_instance.events.log(f"CRASH: {exc_val}", "SYS")
        try:
            print(f"{Prisma.paint('Initiating Emergency Spore Preservation...', 'Y')}")
            result_msg = self.engine_instance.emergency_save(exit_cause="INTERRUPT" if exc_type else "MANUAL")
            print(f"{Prisma.paint(result_msg, 'C' if '✔' in result_msg else 'R')}")
        except Exception as e:
            print(f"{Prisma.paint(f'FATAL: State corruption during shutdown. {e}', 'R')}")
        print(f"{Prisma.paint('Disconnected.', '0')}")
        return exc_type is KeyboardInterrupt

class BoneAmanita:
    def __init__(self, lexicon_layer=None, user_name="TRAVELER"):
        self.user_name = user_name
        self.lex = lexicon_layer if lexicon_layer else TheLexicon
        if hasattr(self.lex, 'initialize'):
            self.lex.initialize()
        if hasattr(self.lex, 'get_store'):
            store = self.lex.get_store()
            if store and getattr(store, 'hive_loaded', False):
                BoneConfig.STAMINA_REGEN *= 1.1
                print(f"{Prisma.GRN}[GENETICS]: Ancestral knowledge detected. Stamina Regen boosted.{Prisma.RST}")
        self.lex.compile_antigens()
        TownHall.DeathGen.load_protocols()
        LiteraryReproduction.load_genetics()
        self.akashic = TheAkashicRecord()
        print(f"{Prisma.CYN}[SLASH]: The Akashic Record is open for writing.{Prisma.RST}")
        self.events = EventBus()
        self.telemetry = TelemetryService.initialize(f"session_{int(time.time())}")
        self.events.log(f"{Prisma.CYN}[SLASH]: Telemetry Uplink Established.{Prisma.RST}", "BOOT")
        self.system_health = SystemHealth()
        self.observer = TheObserver()
        self.system_health.link_observer(self.observer)
        self.embryo = BoneArchitect.incubate(self.events, self.lex)
        self.embryo = BoneArchitect.awaken(self.embryo)
        self.mind = self.embryo.mind
        self.limbo = self.embryo.limbo
        self.bio = self.embryo.bio
        self.phys = self.embryo.physics
        self.shimmer_state = self.embryo.shimmer
        self.soul_legacy_data = self.embryo.soul_legacy
        self.navigator = self.phys.nav
        self.soul = NarrativeSelf(self.events)
        if self.soul_legacy_data:
            self.soul.load_from_dict(self.soul_legacy_data)
        self.journal = TownHall.Journal()
        self.repro = LiteraryReproduction()
        self.projector = TownHall.Projector()
        self.gordon = GordonKnot()
        self.kintsugi = KintsugiProtocol()
        self.therapy = TherapyProtocol()
        self.folly = TheFolly()
        self.stabilizer = ZoneInertia()
        self.cassandra = CassandraProtocol(self)
        self.director = ChorusDriver()
        self.tinkerer = TownHall.Tinkerer(self.gordon, self.events)
        self.bureau = TheBureau()
        self.almanac = TownHall.Almanac()
        self.cosmic = CosmicDynamics()
        self.council = TownHall.CouncilChamber()
        self.cmd = CommandProcessor(self, Prisma, self.lex, BoneConfig, TownHall.Cartographer)
        self.zen = TownHall.ZenGarden(self.events)
        self.soma = SomaticLoop(self.bio, self.mind.mem, self.lex, self.gordon, self.folly, self.events)
        self.noetic = NoeticLoop(self.mind, self.bio, self.events)
        self.cycle_controller = GeodesicOrchestrator(self)
        local_brain = LLMInterface(events_ref=self.events)
        self.cortex = TheCortex(self, llm_client=local_brain)
        self.tick_count = 0
        self.health = self.mind.mem.session_health if self.mind.mem.session_health else BoneConfig.MAX_HEALTH
        self.stamina = self.mind.mem.session_stamina if self.mind.mem.session_stamina else BoneConfig.MAX_STAMINA
        self.trauma_accum = self.mind.mem.session_trauma_vector if hasattr(self.mind.mem, 'session_trauma_vector') and self.mind.mem.session_trauma_vector else BoneConfig.TRAUMA_VECTOR.copy()

    def get_avg_voltage(self):
        hist = self.phys.dynamics.voltage_history
        if not hist: return 0.0
        return sum(hist) / len(hist)

    def process_turn(self, user_message: str) -> Dict[str, Any]:
        turn_start = self.observer.clock_in()
        self.observer.user_turns += 1
        if not user_message: user_message = ""
        cmd_response = self._phase_check_commands(user_message)
        if cmd_response: return cmd_response
        if self._ethical_audit():
            self.events.log(f"{Prisma.WHT}MERCY SIGNAL: Trauma boards wiped.{Prisma.RST}", "SYS")
        if self.phys.tension.last_physics_packet:
            bureau_result = self.bureau.audit(self.phys.tension.last_physics_packet, self.bio.mito.state)
            if bureau_result:
                if bureau_result.get("log"):
                    self.events.log(bureau_result["log"], "BUREAU")
                if bureau_result.get("ui"):
                    self.events.log(bureau_result["ui"], "UI_INTERRUPT")
                if bureau_result.get("atp_gain", 0) > 0:
                    self.bio.mito.state.atp_pool += bureau_result["atp_gain"]
        if self.phys.tension.last_physics_packet:
            perf_metrics = self.observer.get_report()
            @dataclass
            class HostStats:
                latency: float
                efficiency_index: float
            host_stats = HostStats(
                latency=perf_metrics.get("avg_llm_sec", 0.0),
                efficiency_index=1.0
            )
            self.tinkerer.audit_tool_use(
                self.phys.tension.last_physics_packet,
                self.gordon.inventory,
                host_stats
            )
        llm_start = self.observer.clock_in()
        cortex_packet = self.cortex.process(user_message)
        llm_duration = self.observer.clock_out(llm_start, "llm")
        if llm_duration > 5.0:
            cortex_packet["logs"].append(f"{Prisma.GRY}[METRICS]: High Cognitive Latency ({llm_duration:.2f}s).{Prisma.RST}")
        duration = self.observer.clock_out(turn_start, "cycle")
        self.observer.record_memory(self.mind.mem.report_status())
        report = self.observer.get_report()
        if report["status"] != "NOMINAL":
            if cortex_packet.get("ui"):
                warning = f"\n{Prisma.GRY}[SYSTEM LAG: {report['status']} | Cycle: {duration:.2f}s]{Prisma.RST}"
                cortex_packet["ui"] += warning
        cortex_packet["metrics"]["perf"] = report
        return cortex_packet

    def _phase_check_commands(self, user_message):
        if user_message.strip().startswith("/"):
            self.cmd.execute(user_message)
            cmd_logs = [e['text'] for e in self.events.flush()]
            return {
                "type": "COMMAND",
                "ui": f"\n{Prisma.GRY}Command Processed.{Prisma.RST}",
                "logs": cmd_logs if cmd_logs else ["Command Executed."],
                "metrics": self.get_metrics()}
        return None

    def trigger_death(self, last_phys) -> Dict:
        eulogy = TownHall.DeathGen.eulogy(last_phys, self.bio.mito.state)
        death_log = [f"\n{Prisma.RED}SYSTEM HALT: {eulogy}{Prisma.RST}"]
        try:
            path = self.mind.mem.save(
                health=0,
                stamina=self.stamina,
                mutations=self.repro.attempt_reproduction(self, "MITOSIS")[1],
                trauma_accum=self.trauma_accum,
                joy_history=[],
                mitochondria_traits=self.bio.mito.adapt(0),
                antibodies=list(self.bio.immune.active_antibodies),
                soul_data=self.soul.to_dict()
            )
            death_log.append(f"{Prisma.WHT}   [LEGACY SAVED: {path}]{Prisma.RST}")
        except Exception as e:
            death_log.append(f"Save Failed: {e}")
        return {"type": "DEATH", "ui": "\n".join(death_log), "logs": death_log, "metrics": self.get_metrics(0.0)}

    def get_metrics(self, atp=0.0):
        return {"health": self.health, "stamina": self.stamina, "atp": atp, "tick": self.tick_count}

    def emergency_save(self, exit_cause: str = "UNKNOWN") -> str:
        try:
            sess_id = self.mind.mem.session_id
        except AttributeError:
            sess_id = f"corrupted_session_{int(time.time())}"
        spore_data = {
            "session_id": sess_id,
            "meta": {
                "timestamp": time.time(),
                "final_health": getattr(self, "health", 0),
                "final_stamina": getattr(self, "stamina", 0),
                "exit_cause": str(exit_cause)
            },
            "core_graph": getattr(self.mind.mem, "graph", {}) if hasattr(self, "mind") else {},
            "trauma_vector": getattr(self, "trauma_accum", {})
        }
        try:
            if hasattr(self.mind.mem, "loader"):
                path = self.mind.mem.loader.save_spore(f"emergency_{sess_id}.json", spore_data)
            else:
                fname = f"crash_dump_{int(time.time())}.json"
                with open(fname, 'w') as f:
                    json.dump(spore_data, f, default=str)
                path = fname
            return f"✔ Spore encapsulated: {path}"
        except Exception as e:
            return f"✘ Spore encapsulation failed: {e}"

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
    def apply_cosmic_physics(physics, state, cosmic_drag_penalty):
        physics["narrative_drag"] += cosmic_drag_penalty
        if state == "VOID_DRIFT": physics["voltage"] = max(0.0, physics["voltage"] - 0.5)
        elif state == "LAGRANGE_POINT": physics["narrative_drag"] = max(0.1, physics["narrative_drag"] - 2.0)
        elif state == "WATERSHED_FLOW": physics["voltage"] += 0.5

    @staticmethod
    def check_pareidolia(words):
        return BoneConfig.check_pareidolia(words)

if __name__ == "__main__":
    print("\n" + "="*40)
    print(f"{Prisma.paint('♦ BONEAMANITA 10.6.1', 'M')}")
    print(f"{Prisma.paint('  System Bootstrapping...', 'GRY')}")
    print("="*40 + "\n")
    print("The aperture opens. The void stares back.")
    print(f"Before we begin the descent... {Prisma.paint('what should I call you?', 'C')}")
    try:
        identity_input = input(f"{Prisma.paint('>', 'W')} ").strip()
        final_identity = identity_input if identity_input else "TRAVELER"
        if not identity_input:
            print(f"\n{Prisma.paint('Silence accepted. You shall be known as TRAVELER.', 'GRY')}")
        else:
            print(f"\n{Prisma.paint(f'Protocol accepted. Welcome, {final_identity}.', 'G')}")
        time.sleep(1.0)
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        exit()
    engine_instance = BoneAmanita(user_name=final_identity)
    with SessionGuardian(engine_instance) as session_engine:
        first_look = session_engine.process_turn("LOOK")
        if first_look.get("ui"): print(first_look["ui"])
        while True:
            try:
                user_input = input(f"{Prisma.paint(f'{session_engine.user_name} >', 'W')} ")
                if not user_input: continue
            except EOFError:
                break
            if user_input.lower() in ["exit", "quit", "/exit"]:
                break
            result = session_engine.process_turn(user_input)
            if result.get("system_instruction"):
                print(f"\n{Prisma.paint('--- SYSTEM DIRECTIVE ---', 'M')}")
                print(f"{Prisma.paint(result['system_instruction'], '0')}")
                print(f"{Prisma.paint('------------------------', 'M')}\n")
            if result.get("ui"):
                print(result["ui"])
            if result.get("logs") and BoneConfig.VERBOSE_LOGGING:
                print(f"{Prisma.GRY}--- DEBUG LOGS ---{Prisma.RST}")
                for entry in result["logs"]:
                    print(entry)