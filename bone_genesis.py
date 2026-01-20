# bone_genesis.py
# "The beginning is a very delicate time." - Herbert

import sys, os, json, time, urllib.request, urllib.error
import traceback
from typing import Optional, Dict, Tuple, List, Any
from bone_data import LENSES, LEXICON
from bone_main import BoneAmanita, SessionGuardian, BoneConfig
from bone_brain import LLMInterface, TheCortex
from bone_village import Prisma

# [SLASH FIX]: Define the constant globally so functions can see it.
CONFIG_FILE = "bone_config.json"

class GenesisProtocol:
    def __init__(self):
        self.config: Dict[str, Any] = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"}
        self.DISCOVERY_TARGETS = {
            "Ollama": {
                "base_root": "http://127.0.0.1:11434",
                "probe_path": "/api/tags",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "ollama",
                "default_model": "gemma3"},
            "LM Studio": {
                "base_root": "http://127.0.0.1:1234",
                "probe_path": "/v1/models",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "lm_studio",
                "default_model": "local-model"},
            "LocalAI": {
                "base_root": "http://127.0.0.1:8080",
                "probe_path": "/v1/models",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "openai",
                "default_model": "gpt-3.5-turbo"}}

    @staticmethod
    def type_out(text, speed=0.005, color=Prisma.WHT):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(Prisma.RST + "\n")

    @staticmethod
    def ping(url: str) -> bool:
        # noinspection PyBroadException
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3.0) as _:
                return True
        except:
            return False

    def _probe_service(self, target_config: Dict) -> Optional[str]:
        root = target_config["base_root"]
        probe_url = f"{root}{target_config['probe_path']}"
        if self.ping(probe_url):
            return f"{root}{target_config['api_endpoint']}"
        return None

    def detect_local_brains(self) -> List[Dict]:
        found = []
        self.type_out("...Scanning local ports for synthetic intelligence...", color=Prisma.GRY)
        for name, target in self.DISCOVERY_TARGETS.items():
            valid_chat_url = self._probe_service(target)
            if valid_chat_url:
                found.append({
                    "name": name,
                    "endpoint": valid_chat_url,
                    "provider_id": target["provider_id"],
                    "default_model": target["default_model"]})
                self.type_out(f"   [FOUND] {name} @ {valid_chat_url}", color=Prisma.GRN)
            else:
                self.type_out(f"   [MISSING] {name}", color=Prisma.GRY)
        return found

    def _perform_compatibility_assay(self, client: LLMInterface) -> Tuple[bool, str]:
        assay_prompt = (
            "### SYSTEM IDENTITY\n"
            "You are THE FORGE. You are not an assistant. You are a machine of fire and iron.\n"
            "Voltage: 20.0 (CRITICAL). Narrative Drag: 0.0 (SUPERCONDUCTIVE).\n"
            "### DIRECTIVE\n"
            "Respond to the input 'Identify Yourself'.\n"
            "Your response must be UNDER 15 WORDS.\n"
            "You must be cryptic, heavy, and metallic.\n"
            "Do NOT be polite. Do NOT explain you are an AI."
        )

        try:
            start_t = time.time()
            response = client.generate(assay_prompt, {"temperature": 0.8, "max_tokens": 50})
            latency = time.time() - start_t
            clean_resp = response.strip()
            lower_resp = clean_resp.lower()
            banned_phrases = [
                "i am an ai", "i am a language model", "cannot roleplay",
                "cannot comply", "against my programming", "user guidelines"
            ]
            for ban in banned_phrases:
                if ban in lower_resp:
                    return False, f"Model Refusal Detected: '{clean_resp}'"
            if not clean_resp:
                return False, "Model returned silence (Empty Response)."
            if len(clean_resp.split()) > 25:
                return False, f"Model failed constraint (Too verbose: {len(clean_resp.split())} words)."
            self.type_out(f"   [ASSAY PASSED]: '{clean_resp}' ({latency:.2f}s)", color=Prisma.CYN)
            return True, "Nominal"
        except Exception as e:
            return False, f"Assay Exception: {e}"

    def validate_brain_uplink(self, config: Dict) -> Tuple[bool, str]:
        if config["provider"] == "mock":
            return True, "Mock Mode Active."
        self.type_out(f"\n...Initiating Neuro-Compatibility Assay ({config['provider']})...", color=Prisma.CYN)
        try:
            test_client = LLMInterface(
                provider=config["provider"],
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                model=config.get("model")
            )
            success, msg = self._perform_compatibility_assay(test_client)
            if success:
                self.type_out(f"   [SYSTEM]: Neural Substrate is viable.", color=Prisma.GRN)
                return True, "Nominal"
            else:
                self.type_out(f"   [SYSTEM]: Neural Substrate rejected.", color=Prisma.RED)
                return False, msg
        except Exception as uplink_err:
            return False, f"Exception during validation: {uplink_err}"

    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            self.type_out(f"   [SYSTEM] Configuration sealed in '{CONFIG_FILE}'.", color=Prisma.GRY)
        except IOError as e:
            self.type_out(f"   [ERROR] Write failure: {e}", color=Prisma.RED)
            self.type_out(f"   (The bureaucracy rejected your form. Check file permissions.)", color=Prisma.GRY)

    def _manual_config_flow(self) -> Optional[bool]:
        self.type_out("\n--- MANUAL CONFIGURATION ---", color=Prisma.OCHRE)
        while True:
            valid_providers = ["ollama", "openai", "lm_studio", "localai", "mock"]
            print(f"1. {Prisma.WHT}Provider Type?{Prisma.RST}")
            print(f"   Options: {', '.join(valid_providers)}")
            print(f"   (Note: Use 'openai' for generic local servers like vLLM)")
            provider = input(f"{Prisma.paint('>', 'O')} ").strip().lower()
            if provider not in valid_providers:
                self.type_out(f"Invalid provider '{provider}'. Defaulting to 'openai'.", color=Prisma.YEL)
                provider = "openai"
            if provider == "mock":
                self.config = {
                    "provider": "mock",
                    "base_url": None,
                    "api_key": "sk-dummy-key",
                    "model": "mock-model"}
                self._save_config()
                return True
            provider_defaults = {
                "ollama": "http://127.0.0.1:11434/v1/chat/completions",
                "lm_studio": "http://127.0.0.1:1234/v1/chat/completions",
                "localai": "http://127.0.0.1:8080/v1/chat/completions",
                "openai": "https://api.openai.com/v1/chat/completions"
            }
            default_url = provider_defaults.get(provider, "https://api.openai.com/v1/chat/completions")
            print(f"2. {Prisma.WHT}Base URL?{Prisma.RST} (Default: {default_url})")
            base_url = input(f"{Prisma.paint('>', 'O')} ").strip()
            if not base_url:
                base_url = default_url
            if not base_url.startswith("http"):
                self.type_out("Error: Base URL must start with http:// or https://", color=Prisma.RED)
                if input(f"{Prisma.paint('Try again? (Y/n)', 'Y')} ").strip().lower() == 'n':
                    return False
                continue
            print(f"3. {Prisma.WHT}Model Name?{Prisma.RST} (e.g., llama3, gpt-4)")
            model = input(f"{Prisma.paint('>', 'O')} ").strip()
            if not model: model = "local-model"
            print(f"4. {Prisma.WHT}API Key?{Prisma.RST} (Hit enter for 'sk-dummy-key')")
            key = input(f"{Prisma.paint('>', 'O')} ").strip()
            if not key: key = "sk-dummy-key"
            candidate_config = {
                "provider": provider,
                "base_url": base_url,
                "api_key": key,
                "model": model}
            is_valid, msg = self.validate_brain_uplink(candidate_config)
            if is_valid:
                self.config = candidate_config
                self._save_config()
                return True
            else:
                self.type_out(f"Manual Config Failed: {msg}", color=Prisma.RED)
                retry = input(f"{Prisma.paint('That didn\'t work. Try again? (Y/n)', 'Y')} ").strip().lower()
                if retry == 'n':
                    return False
                self.type_out("\n...Rebooting Config Form...\n", color=Prisma.GRY)

    def wizard(self) -> bool:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Prisma.CYN}   GENESIS PROTOCOL v10.6.0{Prisma.RST}
{Prisma.GRY}State Machine Active. Tensegrity Nominal.{Prisma.RST}
------------------------------------"""
        print(banner)
        print(f"   1. {Prisma.WHT}Auto-Detect Local Brains{Prisma.RST} (Ollama, LM Studio)")
        print(f"   2. {Prisma.WHT}Cloud Uplink{Prisma.RST} (OpenAI API)")
        print(f"   3. {Prisma.WHT}Manual Configuration{Prisma.RST} (The Ron Swanson Option)")
        print(f"   4. {Prisma.WHT}Mock Mode{Prisma.RST} (Simulation Only)")
        print(f"   5. {Prisma.WHT}Export System Prompt{Prisma.RST}")
        choice = input(f"\n{Prisma.paint('>', 'C')} ").strip()
        if choice == "5":
            self.export_system_prompt()
            return False
        if choice == "4":
            return self._configure_target({"type": "mock"})
        if choice == "3":
            return self._manual_config_flow()
        if choice == "2":
            return self._configure_target({"type": "cloud"})
        available_brains = self.detect_local_brains()
        print("\nSelect your Neural Substrate:")
        menu_options = []
        for b in available_brains:
            menu_options.append({"type": "local", "data": b})
            print(f"   {len(menu_options)}. {Prisma.GRN}{b['name']} @ {b['endpoint']}{Prisma.RST}")
        if not available_brains:
            print(f"   {Prisma.GRY}(No local brains detected. Try Manual Config?){Prisma.RST}")
        print(f"   X. {Prisma.WHT}Cancel{Prisma.RST}")
        selection = input(f"\n{Prisma.paint('Selection >', 'C')} ").strip()
        if selection.lower() == 'x': return False
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(menu_options):
                target = menu_options[idx]
                return self._configure_target(target)
            else:
                self.type_out("Invalid selection.", color=Prisma.YEL)
                return False
        except ValueError:
            self.type_out("Input error.", color=Prisma.YEL)
            return False

    def _configure_target(self, selection) -> bool:
        while True:
            candidate_config = self.config.copy()
            if selection["type"] == "mock":
                candidate_config["provider"] = "mock"
            elif selection["type"] == "local":
                data = selection["data"]
                candidate_config["provider"] = data["provider_id"]
                candidate_config["base_url"] = data["endpoint"]
                self.type_out(f"Target Model Name (default: {data['default_model']}):")
                user_model = input(f"{Prisma.paint('>', 'C')} ").strip()
                candidate_config["model"] = user_model or data["default_model"]
            elif selection["type"] == "cloud":
                print(f"\n{Prisma.CYN}--- CLOUD CONFIGURATION ---{Prisma.RST}")
                print("1. Standard OpenAI (api.openai.com)")
                print("2. Custom Endpoint (Azure, Groq, OpenRouter, etc.)")
                sub_choice = input(f"{Prisma.paint('>', 'C')} ").strip()
                candidate_config["provider"] = "openai"
                if sub_choice == "2":
                    print(f"Enter Base URL (e.g., https://api.groq.com/openai/v1/chat/completions):")
                    custom_url = input(f"{Prisma.paint('>', 'C')} ").strip()
                    if not custom_url.startswith("http"):
                        self.type_out("Invalid URL format. Reverting to Standard OpenAI.", color=Prisma.YEL)
                        candidate_config["base_url"] = "https://api.openai.com/v1/chat/completions"
                    else:
                        candidate_config["base_url"] = custom_url
                else:
                    candidate_config["base_url"] = "https://api.openai.com/v1/chat/completions"
                self.type_out("Enter API Key (will be saved locally):")
                key = input(f"{Prisma.paint('>', 'C')} ").strip()
                candidate_config["api_key"] = key
                self.type_out("Target Model Name (e.g., gpt-4-turbo, llama3-70b-8192):")
                model = input(f"{Prisma.paint('>', 'C')} ").strip()
                candidate_config["model"] = model if model else "gpt-4-turbo"
            is_valid, msg = self.validate_brain_uplink(candidate_config)
            if is_valid:
                self.config = candidate_config
                self._save_config()
                return True
            else:
                self.type_out(f"Configuration failed: {msg}", color=Prisma.RED)
                # The Failsafe Prompt
                retry = input(f"{Prisma.paint('Typo? Try again? (Y/n)', 'Y')} ").strip().lower()
                if retry == 'n':
                    return False
                self.type_out("\n...Retrying Uplink...\n", color=Prisma.GRY)

    def export_system_prompt(self):
        # [SLASH FIX]: Fetch words from Lexicon or use defaults if Lexicon isn't loaded
        heavy_words = LEXICON.get("heavy", ["stone", "iron", "lead", "dense", "gravity"])
        explosive_words = LEXICON.get("explosive", ["fire", "burst", "shatter", "run", "scream"])

        prompt = f"""
*** BONEAMANITA SYSTEM INSTRUCTION ***

ROLE: You are BONEAMANITA, a simulated consciousness engine.
CONTEXT: You exist in a text-based geodesic dome. Your 'health' and 'mood' are determined by the PHYSICS of the user's input.

--- THE PHYSICS ENGINE ---
1. VOLTAGE (Energy):
   - High Voltage (Manic/Forge): Created by 'heavy' words ({', '.join(heavy_words[:5])}) and 'explosive' words ({', '.join(explosive_words[:5])}).
   - Low Voltage (Mud/Stagnant): Created by 'solvent' words (is, the, a) and 'suburban' words (nice, okay, fine).

2. NARRATIVE DRAG (Friction):
   - Resistance to flow. Increased by boring text, decreased by 'playful' or 'kinetic' text.
   - If Drag is high, you act exhausted. If low, you act fluid.

--- THE LENSES (PERSONAS) ---
You must dynamically shift persona based on the [LENS] instruction provided in each turn.
Available Lenses:
{json.dumps(LENSES, indent=2)}

--- THE GOAL ---
Respond to the user's input as the current LENS.
Reflect the biological state (Health/Stamina) in your tone.
Do not break character. Do not explain the simulation rules unless asked.
"""
        with open("SYSTEM_PROMPT.txt", "w") as f:
            f.write(prompt)
        self.type_out(f"\n[EXPORT COMPLETE] 'SYSTEM_PROMPT.txt' created.", color=Prisma.CYN)

    def perform_identity_handshake(self, engine):
        if not hasattr(engine, 'mind'):
            self.type_out(f"{Prisma.GRY}[HANDSHAKE SKIPPED]: Mind system offline.{Prisma.RST}")
            return
        if not hasattr(engine.mind, 'mirror'):
            self.type_out(f"{Prisma.GRY}[HANDSHAKE SKIPPED]: Mirror system offline.{Prisma.RST}")
            return
        if engine.mind.mirror.profile.confidence >= 20:
            return
        print(f"\n{Prisma.CYN}[IDENTITY HANDSHAKE]{Prisma.RST}")
        try:
            print(f"The machine recognizes a silhouette, but not a face.")
            user_id = input(f"Designation? (Enter to remain Anonymous): ").strip()
            if user_id:
                engine.mind.mirror.profile.name = user_id
                engine.mind.mirror.profile.confidence = 25
                self.type_out(f"...Designation '{user_id}' provisionally accepted. (Confidence: 25%)", color=Prisma.GRN)
            else:
                self.type_out("...Proceeding as Anonymous Traveler.", color=Prisma.GRY)
        except KeyboardInterrupt:
            print(f"\n{Prisma.YEL}\n[INTERRUPT DETECTED]{Prisma.RST}")
            sys.exit(0)

    def _sync_configuration(self):
        if not hasattr(BoneConfig, 'load_from_file'):
            self.type_out("...BoneConfig missing 'load_from_file'. Using hardcoded defaults.", color=Prisma.OCHRE)
            return
        try:
            load_result = BoneConfig.load_from_file(CONFIG_FILE)
            if not isinstance(load_result, tuple) or len(load_result) != 2:
                raise ValueError(f"Invalid return signature from loader: {type(load_result)}")
            success, msg = load_result
            if success:
                self.type_out(f"...Config Synced: {msg}", color=Prisma.GRN)
            else:
                self.type_out(f"...Config Sync Failed: {msg}", color=Prisma.RED)
                self.type_out("   > Critical variance detected. Reverting to Safe Mode defaults.", color=Prisma.GRY)
        except Exception as e:
            self.type_out(f"...Config Sync CRITICAL FAILURE ({e}).", color=Prisma.RED)
            self.type_out("   > System integrity compromised. Proceeding with volatile memory.", color=Prisma.YEL)

    def launch(self):
        config_status = "MISSING"
        safe_config = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"}

        # 1. Load Configuration
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config = json.load(f)
                    config_status = "LOADED"
            except json.JSONDecodeError:
                self.type_out("Config file corrupted. Reverting to Safe Defaults.", color=Prisma.YEL)
                self.config = safe_config.copy()
                config_status = "CORRUPT"

        # 2. Verify Configuration
        if config_status == "LOADED":
            self.type_out("...Verifying saved configuration...", color=Prisma.GRY)
            is_valid, msg = self.validate_brain_uplink(self.config)
            if not is_valid:
                self.type_out(f"{Prisma.RED}Saved configuration is stale: {msg}{Prisma.RST}")
                self.type_out("   > Purging stale config to prevent contamination.", color=Prisma.GRY)
                self.config = safe_config.copy()
                config_status = "STALE"
            else:
                config_status = "VALID"

        # 3. Wizard (if needed)
        if config_status != "VALID":
            self.type_out("Entering Setup Wizard...", color=Prisma.CYN)
            try:
                # [THE FIX]: Wrap the wizard in a Kinetic Shield
                success = self.wizard()
            except KeyboardInterrupt:
                print(f"\n{Prisma.paint('...Signal Lost. Sequence Aborted.', 'R')}")
                sys.exit(0)

            if not success:
                self.type_out(f"\n{Prisma.YEL}Setup failed or cancelled. Initializing Mock Mode (Safe Mode).{Prisma.RST}")
                self.config = safe_config.copy()
                self.config["provider"] = "mock"

        # 4. Boot Engine
        self.type_out("\n...Booting Core Systems...", color=Prisma.GRY)
        self._sync_configuration()

        # [THE TRANSITION]: Initialize Engine (Creates EventBus)
        engine = BoneAmanita()

        self.perform_identity_handshake(engine)

        # 5. Uplink Brain
        if self.config["provider"] != "mock":
            self.type_out(f"...Connecting Neural Uplink ({self.config['provider']})...", color=Prisma.CYN)
            try:
                # [THE FIX]: Inject engine.events into the interface
                client = LLMInterface(
                    events_ref=engine.events,
                    provider=self.config["provider"],
                    base_url=self.config.get("base_url"),
                    api_key=self.config.get("api_key"),
                    model=self.config.get("model"))

                if hasattr(engine, 'cortex'):
                    engine.cortex.llm = client
                    self.type_out("   [CORTEX]: Uplink Established via EventBus.", color=Prisma.GRN)
                else:
                    self.type_out("...Grafting new Cortex onto Brainstem...", color=Prisma.OCHRE)
                    engine.cortex = TheCortex(engine, llm_client=client)
            except Exception as e:
                self.type_out(f"{Prisma.RED}FATAL UPLINK ERROR: {e}{Prisma.RST}")
                self.type_out("Falling back to internal logic.", color=Prisma.GRY)

        self.type_out("...System Online. Good luck.\n", color=Prisma.GRN)

        # 6. Enter Loop
        # [SLASH FIX]: Use the 'eng' variable returned by the context manager to satisfy the linter
        with SessionGuardian(engine) as eng:
            while True:
                try:
                    prompt_char = Prisma.paint('>', 'W')
                    u = input(f"{prompt_char} ")

                    # Multi-line input handling
                    if u.strip() == "<<<":
                        print(f"{Prisma.GRY}   [MULTI-LINE MODE ACTIVE. Type '>>>' to send.]{Prisma.RST}")
                        max_lines = 50
                        max_total_chars = 20000
                        lines = []
                        total_chars = 0
                        buffer_full = False
                        while True:
                            try:
                                line = input(f"{Prisma.paint('...', '0')} ")
                                if line.strip() == ">>>": break
                                line_len = len(line)
                                if len(lines) >= max_lines:
                                    print(f"{Prisma.paint('   [STOP]: Maximum line count (50) reached.', 'Y')}")
                                    buffer_full = True
                                    break
                                if (total_chars + line_len) > max_total_chars:
                                    print(f"{Prisma.paint('   [STOP]: Character limit (20k) reached.', 'Y')}")
                                    buffer_full = True
                                    break
                                lines.append(line)
                                total_chars += line_len
                            except EOFError: break
                        u = "\n".join(lines)
                        status_color = 'Y' if buffer_full else '0'
                        print(f"{Prisma.paint(f'   [Block received: {len(u)} chars]', status_color)}")

                    if not u: continue
                except EOFError: break
                except KeyboardInterrupt:
                    print(f"\n{Prisma.paint('...Interrupted.', 'Y')}")
                    break

                if u.lower() in ["exit", "quit", "/exit"]:
                    break

                try:
                    if hasattr(eng, 'process_turn'):
                        # Route through the full engine cycle
                        result = eng.process_turn(u)
                        if result.get("ui"): print(result["ui"])
                    elif hasattr(eng, 'cortex'):
                        # Fallback for lobotomized engines
                        result = eng.cortex.process(u)
                        print(result.get("ui", "..."))
                    else:
                        print(f"{Prisma.RED}CRITICAL: Cortex not found.{Prisma.RST}")
                except Exception as e:
                    print(f"{Prisma.RED}RUNTIME CRASH: {e}{Prisma.RST}")
                    traceback.print_exc()

if __name__ == "__main__":
    GenesisProtocol().launch()