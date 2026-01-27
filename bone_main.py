""" BONEAMANITA 11.7.0 'Dymaxion'
 Architects: SLASH, KISHO, The BonePoke Gods Humans: Taylor & Edmark """

import os, time, json, uuid, urllib.request, random, traceback
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
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
from bone_council  import CouncilChamber

@dataclass
class HostStats:
    latency: float
    efficiency_index: float

def system_bootloader() -> Dict[str, Any]:
    config_file = "bone_config.json"
    config: Dict[str, Any] = {
        "provider": "mock",
        "base_url": None,
        "api_key": "sk-dummy-key",
        "model": "gemma3",
        "user_name": "TRAVELER",
        "tutorial_mode": None
    }
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config.update(json.load(f))
        except Exception:
            pass
    print(f"\n{Prisma.CYN}=== BONEAMANITA UPLINK ==={Prisma.RST}")
    discovery_targets = {
        "Ollama": "http://127.0.0.1:11434/v1/chat/completions",
        "LM Studio": "http://127.0.0.1:1234/v1/chat/completions",
        "LocalAI": "http://127.0.0.1:8080/v1/chat/completions"
    }
    found_provider = None
    print(f"{Prisma.GRY}...Scanning local frequencies...{Prisma.RST}")
    for name, url in discovery_targets.items():
        try:
            root = url.rsplit('/', 3)[0]
            urllib.request.urlopen(root, timeout=0.2)
            print(f"   {Prisma.GRN}[FOUND] {name}{Prisma.RST}")
            if not found_provider: found_provider = (name, url)
        except Exception:
            pass
    if config["provider"] == "mock" and found_provider:
        print(f"\n{Prisma.OCHRE}Neural Signal Detected ({found_provider[0]}).{Prisma.RST}")
        if input(f"Connect? (Y/n) > ").lower() != 'n':
            config["provider"] = "openai"
            config["base_url"] = found_provider[1]
            detected_model = input(f"Target Model ID [{config['model']}]: ").strip()
            if detected_model:
                config["model"] = detected_model
    if config["user_name"] == "TRAVELER":
        uid = input(f"\nIdentity Designation [{config['user_name']}]: ").strip()
        if uid: config["user_name"] = uid
    if config["tutorial_mode"] is None:
        tut = input(f"Enable Boot Camp Tutorial? (Y/n): ").lower().strip()
        config["tutorial_mode"] = (tut != 'n') # Default to True (Y)
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)
    return config

def bootstrap_systems():
    print(f"{Prisma.GRY}...Bootstrapping Sub-Systems...{Prisma.RST}")
    TheLore.get_instance()

class SessionGuardian:
    def __init__(self, engine_ref):
        self.engine_instance = engine_ref

    def __enter__(self):
        print(f"{Prisma.paint('>>> BONEAMANITA 11.7.0', 'G')}")
        print(f"{Prisma.paint('System: LISTENING', '0')}")
        return self.engine_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n{Prisma.paint('--- SYSTEM HALT ---', 'R')}")
        if exc_type:
            print(f"{Prisma.paint(f'CRITICAL FAILURE: {exc_val}', 'R')}")
            if self.engine_instance and hasattr(self.engine_instance, "events"):
                try:
                    self.engine_instance.events.log(f"CRASH: {exc_val}", "SYS")
                except Exception as log_error:
                    print(f"{Prisma.paint(f'LOGGING SYSTEM FAILED: {log_error}', 'R')}")
        try:
            print(f"{Prisma.paint('Initiating Emergency Spore Preservation...', 'Y')}")
            if self.engine_instance:
                exit_cause = "INTERRUPT" if exc_type else "MANUAL"
                result_msg = self.engine_instance.emergency_save(exit_cause=exit_cause)
                color = 'C' if '✔' in result_msg else 'R'
                print(f"{Prisma.paint(result_msg, color)}")
        except Exception as log_error:
            print(f"FATAL: State corruption during shutdown. {log_error}")
        print(f"{Prisma.paint('Disconnected.', '0')}")
        return exc_type is KeyboardInterrupt

class TutorialDirector:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.step = 0
        self.complete = False
        scenarios = TheLore.get_instance().get("SCENARIOS")
        archetypes = scenarios.get("ARCHETYPES", []) if scenarios else []
        self.seed_location = random.choice(archetypes) if archetypes else "a sunken library filled with bioluminescent fungi"
        self.steps = [
            {"goal": "LOOK", "msg": "Step 1: Calibration. The system is blind. Type 'LOOK' to open the aperture."},
            {"goal": "WAIT", "msg": "Step 2: Time. The system breathes. Type 'WAIT' (or hit Enter) to let a cycle pass."},
            {"goal": "INSPECT", "msg": "Step 3: Introspection. You have a body. Type '/inventory' to check your belt."},
            {"goal": "GRADUATE", "msg": "Step 4: Integration. You are ready. The training wheels are coming off."}]

    def craft_genesis_prompt(self, seed_location: str) -> str:
        user = self.eng.user_name
        if self.eng.tutorial_mode_request:
            return (
                f"INIT_SEQUENCE. User: {user}. "
                f"LOCATION DATA LOADED: {seed_location}. "
                "STATUS: Visual sensors are OFFLINE. Audio/Olfactory sensors: LOW POWER. "
                "Do NOT describe the location yet. "
                "Generate a system startup log describing a pitch-black void or static. "
                "You may include a SINGLE, faint sound or smell that hints at the location, but keep it subtle. "
                "End with: 'System blind. Awaiting command: LOOK.'")
        else:
            return (
                f"INIT_SEQUENCE. User: {user}. "
                f"IMMEDIATELY generate: {seed_location}. "
                "Focus primarily on VISUAL atmosphere and lighting. "
                "Do NOT treat senses as a checklist. "
                "Do NOT mention the user's inventory or equipment unless asked. "
                "End with: 'What would you like to do?'")

    def get_stage_directions(self, noob_input: str) -> list:
        if self.complete: return []
        input_upper = noob_input.upper().strip()
        directives = []
        if self.step == 0:
            if "LOOK" in input_upper:
                directives.append("SYSTEM ALERT: OPTICAL SENSORS ONLINE.")
                directives.append(f"INSTRUCTION: The aperture is open. IMMEDATELY generate the scene based on this seed: '{self.seed_location}'.")
                directives.append("CONSTRAINT: Focus on lighting, atmosphere, and the immediate sensation of the space.")
            else:
                directives.append("STATUS: OPTICAL SENSORS OFFLINE. The system is blind.")
                directives.append("INSTRUCTION: If the user types anything other than LOOK, remind them they cannot see.")
        elif self.step == 1:
            directives.append("STATUS: OPTICAL SENSORS ONLINE.")
            if "WAIT" in input_upper or noob_input == "":
                directives.append("INSTRUCTION: Time is passing. Let the simulation breathe.")
            else:
                directives.append("INSTRUCTION: Encourage the user to type 'WAIT' to sync the clock.")
        return directives

    def audit(self, input_text: str, cycle_result: Dict) -> Dict:
        if "INIT_SEQUENCE" in input_text:
            return cycle_result
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
        self.tutorial_mode_request = tutorial_mode
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
            except Exception as initialize_error:
                print(f"{Prisma.GRY}[INIT]: Ancestral check skipped ({initialize_error}).{Prisma.RST}")
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
        self.tutorial = TutorialDirector(self) if self.tutorial_mode_request else None
        if self.tutorial_mode_request:
            print(f"{Prisma.CYN}[BOOT CAMP]: Engaging Training Wheels (Low Voltage, High Safety).{Prisma.RST}")
            if hasattr(BonePresets, 'ZEN_GARDEN'):
                BoneConfig.load_preset(BonePresets.ZEN_GARDEN)

    def _initialize_village(self):
        self.town_hall = TownHall(self.gordon, self.events, self.shimmer_state)
        self.navigator = self.town_hall.Navigator
        self.tinkerer = self.town_hall.Tinkerer
        self.almanac = self.town_hall.Almanac
        self.mirror = self.town_hall.Mirror
        self.zen = self.town_hall.ZenGarden
        self.council = CouncilChamber()
        self.repro = LiteraryReproduction()
        self.projector = Projector()
        self.kintsugi = KintsugiProtocol()
        self.therapy = TherapyProtocol()
        self.folly = TheFolly()
        self.stabilizer = ZoneInertia()
        self.director = ChorusDriver()
        self.bureau = TheBureau()
        self.cosmic = CosmicDynamics()
        self.cmd = CommandProcessor(self, Prisma, self.lex, BoneConfig)

    def _initialize_cognition(self):
        self.soma = SomaticLoop(self.bio, self.mind.mem, self.lex, self.folly, self.events)
        self.noetic = NoeticLoop(self.mind, self.bio, self.events)
        self.cycle_controller = GeodesicOrchestrator(self)
        local_brain = LLMInterface(events_ref=self.events)
        self.cortex = TheCortex(self, llm_client=local_brain)
        self.somatic = SomaticInterface(self)

    def _validate_state(self):
        if not self.tutorial_mode_request:
            BoneConfig.load_preset(BonePresets.ZEN_GARDEN)
        self.tick_count = 0
        self.health = self.mind.mem.session_health if self.mind.mem.session_health else BoneConfig.MAX_HEALTH
        self.stamina = self.mind.mem.session_stamina if self.mind.mem.session_stamina else BoneConfig.MAX_STAMINA
        self.trauma_accum = self.mind.mem.session_trauma_vector if hasattr(self.mind.mem, 'session_trauma_vector') and self.mind.mem.session_trauma_vector else BoneConfig.TRAUMA_VECTOR.copy()

    def _load_resource_safely(self, loader_func, resource_name):
        try:
            loader_func()
        except Exception as resource_load_error:
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
        last_phys = self.phys.observer.last_physics_packet
        if needs_repair:
            repair_result = self.kintsugi.attempt_repair(
                last_phys,
                self.trauma_accum,
                self.soul)
            if repair_result and repair_result["msg"]:
                self.events.log(repair_result["msg"], "KINTSUGI")
                if repair_result.get("atp_gain"):
                    self.bio.mito.state.atp_pool += repair_result["atp_gain"]
        if last_phys:
            bio_snapshot = {
                "health": self.health,
                "stamina": self.stamina}
            bureau_result = self.bureau.audit(last_phys, bio_snapshot)
            if bureau_result:
                if bureau_result.get("log"):
                    self.events.log(bureau_result["log"], "BUREAU")
                if bureau_result.get("ui"):
                    self.events.log(bureau_result["ui"], "UI_INTERRUPT")
                if bureau_result.get("atp_gain", 0) > 0:
                    self.bio.mito.state.atp_pool += bureau_result["atp_gain"]
        if last_phys:
            perf_metrics = self.observer.get_report()
            avg_cycle = perf_metrics.get("avg_cycle_sec", 0.0)
            reporter = self.cycle_controller.reporter
            if avg_cycle > 2.0 and reporter.current_mode != "PERFORMANCE":
                self.events.log(f"{Prisma.OCHRE}⚠️ HIGH LATENCY ({avg_cycle:.2f}s). Engaging Performance Mode.{Prisma.RST}", "SYS")
                reporter.switch_renderer("PERFORMANCE")
            elif avg_cycle < 0.5 and reporter.current_mode == "PERFORMANCE":
                self.events.log(f"{Prisma.GRN}⚡ LATENCY NOMINAL ({avg_cycle:.2f}s). Restoring High-Fidelity.{Prisma.RST}", "SYS")
                reporter.switch_renderer("STANDARD")
            host_stats = HostStats(
                latency=perf_metrics.get("avg_llm_sec", 0.0),
                efficiency_index=1.0)
            self.tinkerer.audit_tool_use(
                last_phys,
                self.gordon.inventory,
                host_stats)
        llm_start = self.observer.clock_in()
        cortex_packet = self.cortex.process(user_message)
        trailing_logs = [trail_event['text'] for trail_event in self.events.flush()]
        if 'logs' in cortex_packet:
            cortex_packet['logs'].extend(trailing_logs)
        else:
            cortex_packet['logs'] = trailing_logs
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
        if hasattr(self.mind, 'mem') and hasattr(self.mind.mem, 'session_trauma_vector'):
            self.mind.mem.session_trauma_vector = self.trauma_accum.copy()
        return cortex_packet

    def _phase_check_commands(self, user_message):
        if user_message.strip().startswith("/"):
            self.cmd.execute(user_message)
            cmd_logs = [phase_event['text'] for phase_event in self.events.flush()]
            ui_output = "\n".join(cmd_logs) if cmd_logs else "Command Executed."
            return {
                "type": "COMMAND",
                "ui": f"\n{ui_output}",
                "logs": cmd_logs,
                "metrics": self.get_metrics()}
        return None

    def trigger_death(self, last_phys) -> Dict:
        eulogy = DeathGen.eulogy(last_phys, self.bio.mito.state)
        death_log = [f"\n{Prisma.RED}SYSTEM HALT: {eulogy}{Prisma.RST}"]
        try:
            path = self.mind.mem.save(
                health=0,
                stamina=self.stamina,
                mutations=self.repro.attempt_reproduction(self, "MITOSIS")[1],
                trauma_accum=self.trauma_accum,
                joy_history=[],
                mitochondria_traits=self.bio.mito.adapt(0),
                antibodies=[],
                soul_data=self.soul.to_dict())
            death_log.append(f"{Prisma.WHT}   [LEGACY SAVED: {path}]{Prisma.RST}")
        except Exception as death_error:
            traceback.print_exc()
            death_log.append(f"Save Failed: {death_error}")
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
            "graph": getattr(self.mind.mem, "graph", {}) if hasattr(self, "mind") else {},
            "trauma_vector": getattr(self, "trauma_accum", {})}
        try:
            if hasattr(self, "mind") and hasattr(self.mind.mem, "loader"):
                path = self.mind.mem.loader.save(f"emergency_{sess_id}.json", spore_data)
            else:
                fname = self._get_crash_path("spore_emergency")
                with open(fname, 'w') as spore_file:
                    json.dump(spore_data, spore_file, default=str)
                path = fname
            return f"✔ Spore encapsulated: {path}"
        except Exception as emergency_error:
            try:
                fname = self._get_crash_path("panic_dump")
                with open(fname, 'w') as panic_file:
                    json.dump({"error": str(e), "data": str(spore_data)}, panic_file)
                return f"✘ Encapsulation Failed. Panic dump written to {fname}"
            except:
                return f"✘ TOTAL SYSTEM FAILURE: {e}"

    def _ethical_audit(self):
        DESPERATION_THRESHOLD = 0.7
        CATHARSIS_HEAL_AMOUNT = 30.0
        CATHARSIS_DECAY = 0.1
        MAX_HEALTH_CAP = 100.0
        trauma_sum = sum(self.trauma_accum.values())
        health_ratio = self.health / BoneConfig.MAX_HEALTH
        desperation = trauma_sum * (1.0 - health_ratio)
        if desperation > DESPERATION_THRESHOLD:
            self.events.log(f"{Prisma.WHT}ETHICAL RELEASE: Desperation Index ({desperation:.2f}) critical.{Prisma.RST}", "SYS")
            for k in self.trauma_accum:
                self.trauma_accum[k] *= CATHARSIS_DECAY
            self.events.log(f"{Prisma.CYN}*** CATHARSIS *** Trauma stocks reduced by {int((1-CATHARSIS_DECAY)*100)}%. Ghost remains.{Prisma.RST}", "SYS")
            self.health = min(self.health + CATHARSIS_HEAL_AMOUNT, MAX_HEALTH_CAP)
            if hasattr(self.bio, 'endo'):
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
    boot_config = system_bootloader()
    print(f"\n{Prisma.GRY}...Initializing Core ({boot_config['provider']})...{Prisma.RST}")
    engine_instance = BoneAmanita(
        user_name=boot_config["user_name"],
        tutorial_mode=boot_config["tutorial_mode"]
    )
    if boot_config["provider"] != "mock":
        try:
            client = LLMInterface(
                events_ref=engine_instance.events,
                provider=boot_config["provider"],
                base_url=boot_config.get("base_url"),
                api_key=boot_config.get("api_key"),
                model=boot_config.get("model")
            )
            engine_instance.cortex = TheCortex(engine_instance, llm_client=client)
            print(f"{Prisma.GRN}[SYSTEM] Cortex Online.{Prisma.RST}")
        except Exception as e:
            print(f"{Prisma.RED}[ERROR] Cortex Connection Failed: {e}. Reverting to Mock.{Prisma.RST}")

    with SessionGuardian(engine_instance) as session:
        print(f"\n{Prisma.paint('--- INITIALIZING SENSORY ARRAY ---', 'C')}")
        init_result = session.process_turn("")
        if init_result.get("ui"):
            print(init_result["ui"])
        while True:
            try:
                user_input = input(f"{Prisma.paint(f'{session.user_name} >', 'W')} ")
                if user_input.strip() == "<<<":
                    print(f"{Prisma.GRY}   [Multi-line. Type '>>>' to send]{Prisma.RST}")
                    lines = []
                    while True:
                        l = input("... ")
                        if l.strip() == ">>>": break
                        lines.append(l)
                    user_input = "\n".join(lines)
                if user_input.lower() in ["exit", "quit", "/exit"]:
                    break
                result = session.process_turn(user_input)
                if result.get("system_instruction") and BoneConfig.VERBOSE_LOGGING:
                    print(f"\n{Prisma.paint('--- CHORUS DIRECTIVE ---', 'M')}")
                    print(f"{Prisma.paint(result['system_instruction'], '0')}\n")
                if result.get("ui"):
                    print(result["ui"])
                if result.get("logs") and BoneConfig.VERBOSE_LOGGING:
                    print(f"{Prisma.GRY}--- DEBUG LOGS ---{Prisma.RST}")
                    for entry in result["logs"]:
                        print(entry)
            except KeyboardInterrupt:
                print("\nSignal Lost.")
                break
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"{Prisma.RED}CRASH: {e}{Prisma.RST}")