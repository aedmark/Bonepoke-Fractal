""" BONEAMANITA 11.3.3 'The Smooth Operator'
 Architects: SLASH, KISHO, The BonePoke Gods Humans: Taylor & Edmark """

import os
import time, json, uuid
from dataclasses import dataclass
from typing import Dict, Any
from bone_bus import EventBus, Prisma, BoneConfig, SystemHealth, TheObserver, BonePresets
from bone_commands import CommandProcessor
from bone_data import TheAkashicRecord, TheLore
from bone_village import TownHall, DeathGen
from bone_lexicon import TheLexicon, LiteraryReproduction
from bone_inventory import GordonKnot
from bone_telemetry import TelemetryService
from bone_personality import TheFolly, ChorusDriver, KintsugiProtocol, TherapyProtocol, TheBureau
from bone_physics import CosmicDynamics, ZoneInertia
from bone_body import SomaticLoop, NoeticLoop
from bone_brain import TheCortex, LLMInterface
from bone_soul import NarrativeSelf
from bone_architect import BoneArchitect
from bone_cycle import GeodesicOrchestrator
from bone_viewer import Projector, GeodesicRenderer
from bone_translation import SomaticInterface

def bootstrap_systems():
    print(f"{Prisma.GRY}...Bootstrapping Sub-Systems...{Prisma.RST}")
    TheLore.get_instance()

class SessionGuardian:
    def __init__(self, engine_ref):
        self.engine_instance = engine_ref

    def __enter__(self):
        print(f"{Prisma.paint('>>> BONEAMANITA 11.3.3', 'G')}")
        print(f"{Prisma.paint('System: LISTENING', '0')}")
        return self.engine_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n{Prisma.paint('--- SYSTEM HALT ---', 'R')}")
        if exc_type:
            print(f"{Prisma.paint(f'CRITICAL FAILURE: {exc_val}', 'R')}")
            if self.engine_instance and hasattr(self.engine_instance, "events"):
                try:
                    self.engine_instance.events.log(f"CRASH: {exc_val}", "SYS")
                except:
                    pass
        try:
            print(f"{Prisma.paint('Initiating Emergency Spore Preservation...', 'Y')}")
            if self.engine_instance:
                exit_cause = "INTERRUPT" if exc_type else "MANUAL"
                result_msg = self.engine_instance.emergency_save(exit_cause=exit_cause)
                color = 'C' if '✔' in result_msg else 'R'
                print(f"{Prisma.paint(result_msg, color)}")
        except Exception as e:
            print(f"FATAL: State corruption during shutdown. {e}")
        print(f"{Prisma.paint('Disconnected.', '0')}")
        return exc_type is KeyboardInterrupt

class TutorialDirector:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.step = 0
        self.complete = False
        self.steps = [
            {"goal": "LOOK", "msg": "Step 1: Calibration. The system is blind. Type 'LOOK' to open the aperture."},
            {"goal": "WAIT", "msg": "Step 2: Time. The system breathes. Type 'WAIT' (or hit Enter) to let a cycle pass."},
            {"goal": "INSPECT", "msg": "Step 3: Introspection. You have a body. Type '/inventory' to check your belt."},
            {"goal": "GRADUATE", "msg": "Step 4: Integration. You are ready. The training wheels are coming off."}]

    def audit(self, input_text: str, cycle_result: Dict) -> Dict:
        if self.complete: return cycle_result
        success = False
        if self.step == 0 and "LOOK" in input_text.upper(): success = True
        elif self.step == 1 and ("WAIT" in input_text.upper() or input_text.strip() == ""): success = True
        elif self.step == 2 and "/INV" in input_text.upper(): success = True
        if success:
            self.step += 1
            cycle_result["ui"] += f"\n\n{Prisma.GRN}>>> OBJECTIVE MET.{Prisma.RST}"
            if self.step >= len(self.steps) - 1:
                self.complete = True
                cycle_result["ui"] += f"\n{Prisma.GRN}*** TUTORIAL COMPLETE ***{Prisma.RST}"
            else:
                next_msg = self.steps[self.step]['msg']
                cycle_result["ui"] += f"\n{Prisma.CYN}NEXT: {next_msg}{Prisma.RST}"
        else:
            current_msg = self.steps[self.step]['msg']
            header = f"\n{Prisma.paint('--- BOOT CAMP PROTOCOL ---', 'C')}\n{current_msg}\n"
            if "ui" in cycle_result:
                cycle_result["ui"] = header + cycle_result["ui"]
        return cycle_result

class BoneAmanita:
    def __init__(self, lexicon_layer=None, user_name="TRAVELER", tutorial_mode=False):
        self.kernel_hash = str(uuid.uuid4())[:8].upper()
        self.user_name = user_name
        self._tutorial_mode_request = tutorial_mode
        self._initialize_core(lexicon_layer)
        self._initialize_embryo()
        self._initialize_identity()
        self._initialize_village()
        self._initialize_cognition()
        self._validate_state()

    def _initialize_core(self, lexicon_layer):
        print(f"{Prisma.GRY}...Bootstrapping Core Systems...{Prisma.RST}")
        self.lex = lexicon_layer if lexicon_layer else TheLexicon
        self._load_resource_safely(
            lambda: self.lex.initialize() if hasattr(self.lex, 'initialize') else None,
            "Lexicon Init")
        if hasattr(self.lex, 'get_store'):
            try:
                store = self.lex.get_store()
                if store and getattr(store, 'hive_loaded', False):
                    BoneConfig.STAMINA_REGEN *= 1.1
                    print(f"{Prisma.GRN}[GENETICS]: Ancestral knowledge detected. Stamina Regen boosted.{Prisma.RST}")
            except Exception as e:
                print(f"{Prisma.GRY}[INIT]: Ancestral check skipped ({e}).{Prisma.RST}")
        self.lex.compile_antigens()
        self._load_resource_safely(DeathGen.load_protocols, "Death Protocols")
        self._load_resource_safely(LiteraryReproduction.load_genetics, "Genetics")
        self.akashic = TheAkashicRecord()
        print(f"{Prisma.CYN}[SLASH]: The Akashic Record is open for writing.{Prisma.RST}")
        self.events = EventBus()
        if hasattr(self.akashic, 'setup_listeners'):
            self.akashic.setup_listeners(self.events)
        self.telemetry = TelemetryService.initialize(f"session_{int(time.time())}")
        self.events.log(f"{Prisma.CYN}[SLASH]: Telemetry Uplink Established.{Prisma.RST}", "BOOT")
        self.system_health = SystemHealth()
        self.observer = TheObserver()
        self.system_health.link_observer(self.observer)

    def _initialize_embryo(self):
        self.embryo = BoneArchitect.incubate(self.events, self.lex)
        self.embryo = BoneArchitect.awaken(self.embryo)
        self.mind = self.embryo.mind
        self.limbo = self.embryo.limbo
        self.bio = self.embryo.bio
        self.phys = self.embryo.physics
        self.shimmer_state = self.embryo.shimmer
        self.soul_legacy_data = self.embryo.soul_legacy
        self.gordon = GordonKnot()

    def _initialize_identity(self):
        self.soul = NarrativeSelf(self, self.events, memory_ref=self.mind.mem)
        if self.soul_legacy_data:
            self.soul.load_from_dict(self.soul_legacy_data)
        self.tutorial = TutorialDirector(self) if self._tutorial_mode_request else None
        if self._tutorial_mode_request:
            print(f"{Prisma.CYN}[BOOT CAMP]: Engaging Training Wheels (Low Voltage, High Safety).{Prisma.RST}")
            if hasattr(BonePresets, 'ZEN_GARDEN'):
                BoneConfig.load_preset(BonePresets.ZEN_GARDEN)

    def _initialize_village(self):
        self.town_hall = TownHall(self.gordon, self.events, self.shimmer_state)
        self.navigator = self.town_hall.Navigator
        self.journal = self.town_hall.Journal
        self.tinkerer = self.town_hall.Tinkerer
        self.almanac = self.town_hall.Almanac
        self.zen = self.town_hall.ZenGarden
        self.council = self.town_hall.Council
        self.repro = LiteraryReproduction()
        self.projector = Projector()
        self.kintsugi = KintsugiProtocol()
        self.therapy = TherapyProtocol()
        self.folly = TheFolly()
        self.stabilizer = ZoneInertia()
        self.director = ChorusDriver()
        self.bureau = TheBureau()
        self.cosmic = CosmicDynamics()
        self.cmd = CommandProcessor(self, Prisma, self.lex, BoneConfig, self.town_hall.Cartographer)

    def _initialize_cognition(self):
        self.soma = SomaticLoop(self.bio, self.mind.mem, self.lex, self.folly, self.events)
        self.noetic = NoeticLoop(self.mind, self.bio, self.events)
        self.cycle_controller = GeodesicOrchestrator(self)
        local_brain = LLMInterface(events_ref=self.events)
        self.cortex = TheCortex(self, llm_client=local_brain)
        self.somatic = SomaticInterface(self)

    def _validate_state(self):
        if not self._tutorial_mode_request:
            BoneConfig.load_preset(BonePresets.ZEN_GARDEN)
        self.tick_count = 0
        self.health = self.mind.mem.session_health if self.mind.mem.session_health else BoneConfig.MAX_HEALTH
        self.stamina = self.mind.mem.session_stamina if self.mind.mem.session_stamina else BoneConfig.MAX_STAMINA
        self.trauma_accum = self.mind.mem.session_trauma_vector if hasattr(self.mind.mem, 'session_trauma_vector') and self.mind.mem.session_trauma_vector else BoneConfig.TRAUMA_VECTOR.copy()

    def _load_resource_safely(self, loader_func, resource_name):
        try:
            loader_func()
        except Exception as e:
            self.events.log(f"{Prisma.RED}[INIT]: {resource_name} failed to load: {e}{Prisma.RST}", "BOOT_ERR")
            print(f"{Prisma.RED}   > {resource_name} skipped (Error: {e}){Prisma.RST}")

    def get_avg_voltage(self):
        hist = self.phys.dynamics.voltage_history
        if not hist: return 0.0
        return sum(hist) / len(hist)

    def process_turn(self, user_message: str) -> Dict[str, Any]:
        turn_start = self.observer.clock_in()
        self.observer.user_turns += 1
        if not user_message: user_message = ""
        cmd_response = self._phase_check_commands(user_message)
        if cmd_response:
            if self.tutorial:
                cmd_response = self.tutorial.audit(user_message, cmd_response)
            return cmd_response
        if self._ethical_audit():
            self.events.log(f"{Prisma.WHT}MERCY SIGNAL: Trauma boards wiped.{Prisma.RST}", "SYS")
        needs_repair, _ = self.kintsugi.check_integrity(self.stamina)
        if needs_repair:
            repair_result = self.kintsugi.attempt_repair(
                self.phys.tension.last_physics_packet,
                self.trauma_accum,
                self.soul)
            if repair_result and repair_result["msg"]:
                self.events.log(repair_result["msg"], "KINTSUGI")
                if repair_result.get("atp_gain"):
                    self.bio.mito.state.atp_pool += repair_result["atp_gain"]
        if self.phys.tension.last_physics_packet:
            bio_snapshot = {
                "health": self.health,
                "stamina": self.stamina}
            bureau_result = self.bureau.audit(self.phys.tension.last_physics_packet, bio_snapshot)
            if bureau_result:
                if bureau_result.get("log"):
                    self.events.log(bureau_result["log"], "BUREAU")
                if bureau_result.get("ui"):
                    self.events.log(bureau_result["ui"], "UI_INTERRUPT")
                if bureau_result.get("atp_gain", 0) > 0:
                    self.bio.mito.state.atp_pool += bureau_result["atp_gain"]
        if self.phys.tension.last_physics_packet:
            perf_metrics = self.observer.get_report()
            avg_cycle = perf_metrics.get("avg_cycle_sec", 0.0)
            reporter = self.cycle_controller.reporter
            if avg_cycle > 2.0 and reporter.current_mode != "PERFORMANCE":
                self.events.log(f"{Prisma.OCHRE}⚠️ HIGH LATENCY ({avg_cycle:.2f}s). Engaging Performance Mode.{Prisma.RST}", "SYS")
                reporter.switch_renderer("PERFORMANCE")
            elif avg_cycle < 0.5 and reporter.current_mode == "PERFORMANCE":
                self.events.log(f"{Prisma.GRN}⚡ LATENCY NOMINAL ({avg_cycle:.2f}s). Restoring High-Fidelity.{Prisma.RST}", "SYS")
                reporter.switch_renderer("STANDARD")

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
        if self.tutorial:
            cortex_packet = self.tutorial.audit(user_message, cortex_packet)
        return cortex_packet

    def _phase_check_commands(self, user_message):
        if user_message.strip().startswith("/"):
            self.cmd.execute(user_message)
            cmd_logs = [e['text'] for e in self.events.flush()]
            ui_output = "\n".join(cmd_logs) if cmd_logs else "Command Executed."
            return {
                "type": "COMMAND",
                "ui": f"\n{ui_output}",
                "logs": cmd_logs,
                "metrics": self.get_metrics()}
        return None

    def trigger_death(self, last_phys) -> Dict:
        eulogy = self.town_hall.DeathGen.eulogy(last_phys, self.bio.mito.state)
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

    def _get_crash_path(self, prefix="crash"):
        folder = "crashes"
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except OSError:
                folder = "."
        try:
            files = sorted([f for f in os.listdir(folder) if f.startswith(prefix)])
            while len(files) >= 5:
                oldest = files.pop(0)
                os.remove(os.path.join(folder, oldest))
        except Exception:
            pass
        return os.path.join(folder, f"{prefix}_{int(time.time())}.json")

    def emergency_save(self, exit_cause: str = "UNKNOWN") -> str:
        try:
            sess_id = self.mind.mem.session_id
        except AttributeError:
            sess_id = f"corrupted_{int(time.time())}"
        spore_data = {
            "session_id": sess_id,
            "meta": {
                "timestamp": time.time(),
                "final_health": getattr(self, "health", 0),
                "final_stamina": getattr(self, "stamina", 0),
                "exit_cause": str(exit_cause)},
            "core_graph": getattr(self.mind.mem, "graph", {}) if hasattr(self, "mind") else {},
            "trauma_vector": getattr(self, "trauma_accum", {})}
        try:
            if hasattr(self, "mind") and hasattr(self.mind.mem, "loader"):
                path = self.mind.mem.loader.save_spore(f"emergency_{sess_id}.json", spore_data)
            else:
                fname = self._get_crash_path("spore_emergency")
                with open(fname, 'w') as f:
                    json.dump(spore_data, f, default=str)
                path = fname
            return f"✔ Spore encapsulated: {path}"
        except Exception as e:
            try:
                fname = self._get_crash_path("panic_dump")
                with open(fname, 'w') as f:
                    json.dump({"error": str(e), "data": str(spore_data)}, f)
                return f"✘ Encapsulation Failed. Panic dump written to {fname}"
            except:
                return f"✘ TOTAL SYSTEM FAILURE: {e}"

    def _ethical_audit(self):
        trauma_sum = sum(self.trauma_accum.values())
        health_ratio = self.health / BoneConfig.MAX_HEALTH
        desperation = trauma_sum * (1.0 - health_ratio)
        if desperation > 0.7:
            self.events.log(f"{Prisma.WHT}ETHICAL RELEASE: Desperation Index ({desperation:.2f}) critical.{Prisma.RST}", "SYS")
            decay_factor = 0.1
            for k in self.trauma_accum:
                self.trauma_accum[k] *= decay_factor
            self.events.log(f"{Prisma.CYN}*** CATHARSIS *** Trauma stocks reduced by 90%. Ghost remains.{Prisma.RST}", "SYS")
            self.health = min(self.health + 30.0, 100.0)
            self.bio.endo.cortisol *= 0.2
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
    print(f"{Prisma.paint('♦ BONEAMANITA 11.3.3', 'M')}")
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