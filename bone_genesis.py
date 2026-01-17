# bone_genesis.py
# "The beginning is a very delicate time." - Herbert

import sys, os, json, time, shutil, urllib.request, urllib.error
from typing import Optional, Dict, Tuple, List, Any

try:
    from bone_main import BoneAmanita, SessionGuardian, BoneConfig
    from bone_brain import LLMInterface, TheCortex
    from bone_village import Prisma
    from bone_data import LENSES, LEXICON
except ImportError as import_error:
    print(f"\033[31mCRITICAL: Core systems missing. {import_error}\033[0m")
    sys.exit(1)
CONFIG_FILE = "bone_config.json"
heavy_words = LEXICON.get("heavy", ["stone", "lead", "iron", "gravity", "dense"])
explosive_words = LEXICON.get("explosive", ["burst", "shatter", "spark", "pop", "snap"])

class GenesisProtocol:
    def __init__(self):
        self.config: Dict[str, Any] = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"}
        self.DISCOVERY_TARGETS = {
            "Ollama": {
                "base_root": "http://localhost:11434",
                "probe_path": "/api/tags",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "ollama",
                "default_model": "gemma3"},
            "LM Studio": {
                "base_root": "http://localhost:1234",
                "probe_path": "/v1/models",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "lm_studio",
                "default_model": "local-model"},
            "LocalAI": {
                "base_root": "http://localhost:8080",
                "probe_path": "/v1/models",
                "api_endpoint": "/v1/chat/completions",
                "provider_id": "openai",
                "default_model": "gpt-3.5-turbo"}}

    def type_out(self, text, speed=0.005, color=Prisma.WHT):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(Prisma.RST + "\n")

    def ping(self, url: str) -> bool:
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

    def validate_brain_uplink(self, config: Dict) -> Tuple[bool, str]:
        if config["provider"] == "mock":
            return True, "Mock Mode Active."
        self.type_out(f"\n...Testing Cognition on {config['provider']}...", color=Prisma.CYN)
        try:
            test_client = LLMInterface(
                provider=config["provider"],
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                model=config.get("model"))
            response = test_client.generate("PING", temperature=0.0)
            if not response or not response.strip():
                return False, "Brain returned empty response (Silence)."
            clean_resp_lower = response.lower()
            error_markers = [
                "connection error",
                "timeout error",
                "brain fog",
                "exception",
                "connectcall failed",
                "connection refused",
                "not found",
                "unauthorized",
                "rate limit"]
            is_bracketed_error = "[" in response and "error" in clean_resp_lower
            is_explicit_failure = any(marker in clean_resp_lower for marker in error_markers)
            if is_explicit_failure or is_bracketed_error:
                return False, f"Brain responded with failure signal: {response}"
            self.type_out(f"   [SUCCESS] Brain response: '{response}'", color=Prisma.GRN)
            return True, "Nominal"
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

    def _manual_config_flow(self) -> bool | None:
        self.type_out("\n--- MANUAL CONFIGURATION ---", color=Prisma.OCHRE)

        while True: # <--- THE SECOND CHANCE LOOP
            valid_providers = ["ollama", "openai", "lm_studio", "mock"]
            print(f"1. {Prisma.WHT}Provider Type?{Prisma.RST}")
            print(f"   Options: {', '.join(valid_providers)}")
            print(f"   (Note: Use 'openai' for generic local servers like LocalAI/vLLM)")

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

            default_url = "http://localhost:11434/v1/chat/completions"
            if provider == "openai": default_url = "https://api.openai.com/v1/chat/completions"
            elif provider == "lm_studio": default_url = "http://localhost:1234/v1/chat/completions"

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
{Prisma.CYN}   GENESIS PROTOCOL v10.2{Prisma.RST}
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
        from bone_data import LENSES, LEXICON
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

    def launch(self):
        config_status = "MISSING"
        safe_config = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config = json.load(f)
                    config_status = "LOADED"
            except json.JSONDecodeError:
                self.type_out("Config file corrupted. Reverting to Safe Defaults.", color=Prisma.YEL)
                self.config = safe_config.copy()
                config_status = "CORRUPT"
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
        if config_status != "VALID":
            self.type_out("Entering Setup Wizard...", color=Prisma.CYN)
            success = self.wizard()
            if not success:
                self.type_out(f"\n{Prisma.YEL}Setup failed or cancelled. Initializing Mock Mode (Safe Mode).{Prisma.RST}")
                self.config = safe_config.copy()
                self.config["provider"] = "mock"
        self.type_out("\n...Booting Core Systems...", color=Prisma.GRY)
        success, msg = BoneConfig.load_from_file(CONFIG_FILE)
        if success:
            self.type_out(f"...Config Synced: {msg}", color=Prisma.GRN)
        else:
            self.type_out(f"...Config Drift Detected: {msg}", color=Prisma.YEL)
        engine = BoneAmanita()
        if engine.mind.mirror.profile.confidence < 50:
            print(f"\n{Prisma.CYN}[IDENTITY REQUIRED]{Prisma.RST}")
            try:
                user_id = input("Enter User Designation: ").strip()
                if user_id:
                    engine.mind.mirror.profile.name = user_id
                    engine.mind.mirror.profile.confidence = 100
                    print(f"...Identity '{user_id}' imprinted on cortex.")
                else:
                    print("...Proceeding as Anonymous Traveler.")
            except KeyboardInterrupt:
                print(f"\n{Prisma.YEL}\n[INTERRUPT DETECTED]{Prisma.RST}")
                print(f"{Prisma.GRY}The user pulled the plug. The universe dissolves into static.{Prisma.RST}")
                sys.exit(0)
        if self.config["provider"] != "mock":
            self.type_out(f"...Connecting Neural Uplink ({self.config['provider']})...", color=Prisma.CYN)
            try:
                client = LLMInterface(
                    provider=self.config["provider"],
                    base_url=self.config.get("base_url"),
                    api_key=self.config.get("api_key"),
                    model=self.config.get("model"))
                if hasattr(engine, 'cortex'):
                    engine.cortex.llm = client
                else:
                    self.type_out("...Grafting new Cortex onto Brainstem...", color=Prisma.OCHRE)
                    engine.cortex = TheCortex(engine, llm_client=client)
            except Exception as e:
                self.type_out(f"{Prisma.RED}FATAL UPLINK ERROR: {e}{Prisma.RST}")
                self.type_out("Falling back to internal logic.", color=Prisma.GRY)
        self.type_out("...System Online. Good luck.\n", color=Prisma.GRN)
        with SessionGuardian(engine) as eng:
            while True:
                try:
                    prompt_char = Prisma.paint('>', 'W')
                    u = input(f"{prompt_char} ")
                    if u.strip() == "<<<":
                        print(f"{Prisma.GRY}   [MULTI-LINE MODE ACTIVE. Type '>>>' to send.]{Prisma.RST}")
                        lines = []
                        while True:
                            try:
                                line = input(f"{Prisma.paint('...', '0')} ")
                                if line.strip() == ">>>":
                                    break
                                lines.append(line)
                            except EOFError:
                                break
                        u = "\n".join(lines)
                        print(f"{Prisma.GRY}   [Block received: {len(u)} chars]{Prisma.RST}")
                    if not u: continue
                except EOFError:
                    break
                if u.lower() in ["exit", "quit", "/exit"]:
                    break

if __name__ == "__main__":
    GenesisProtocol().launch()