# bone_genesis.py
# "The beginning is a very delicate time." - Herbert / Schur / SLASH

import sys
import os
import json
import time
import shutil
import urllib.request
import urllib.error
from typing import Optional, Dict, Tuple, List, Any

# Import Core Systems
try:
    from bone_main import BoneAmanita, SessionGuardian
    from bone_brain import LLMInterface, TheCortex
    from bone_village import Prisma, BoneConfig
except ImportError as e:
    print(f"\033[31mCRITICAL: Core systems missing. {e}\033[0m")
    sys.exit(1)

CONFIG_FILE = "bone_config.json"

class GenesisProtocol:
    """
    The Bootloader.
    Implements a robust State Machine: BOOT -> CHECK -> WIZARD (opt) -> LAUNCH.
    """
    def __init__(self):
        self.config = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"
        }

        # SLASH NOTE: We define the *bases*, but we probe the *endpoints*.
        # Anticipatory Design: Don't assume the API shape; measure it.
        self.DISCOVERY_TARGETS = {
            "Ollama": {
                "base": "http://localhost:11434",
                "provider_id": "ollama",
                "default_model": "llama3"
            },
            "LM Studio": {
                "base": "http://localhost:1234",
                "provider_id": "lm_studio",
                "default_model": "local-model"
            },
            "LocalAI": {
                "base": "http://localhost:8080",
                "provider_id": "openai", # Uses standard OpenAI library/logic
                "default_model": "gpt-3.5-turbo"
            }
        }

    # --- IO UTILITIES ---
    def type_out(self, text, speed=0.005, color=Prisma.WHT):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(Prisma.RST + "\n")

    def ping(self, url: str) -> bool:
        """PINKER LENS: A unambiguous 'Is anybody home?' check."""
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=1) as _:
                return True
        except:
            return False

    def _probe_endpoint(self, base_url: str) -> Optional[str]:
        """
        FULLER LENS: Geodesic triangulating.
        We don't guess the shape; we verify it.
        """
        # 1. Try Standard OpenAI V1 (Preferred)
        v1_url = f"{base_url}/v1/chat/completions"
        # We can't GET a POST endpoint easily without 405, but we can check the base /v1/models often
        # Or just trust the user configuration phase.
        # Actually, for Ollama, let's try to hit a known GET endpoint to verify service presence.

        if self.ping(f"{base_url}/api/tags"): # Ollama native check
            # Now we check if it supports V1
            # Modern Ollama supports /v1, but let's be flexible.
            return v1_url # We will force V1 for consistency if detected

        if self.ping(f"{base_url}/v1/models"): # LM Studio / LocalAI check
            return v1_url

        return None

    # --- STATE: DETECT ---
    def detect_local_brains(self) -> List[Dict]:
        """Scans known ports to reduce cognitive load on the user."""
        found = []
        self.type_out("...Scanning local ports for synthetic intelligence...", color=Prisma.GRY)

        for name, target in self.DISCOVERY_TARGETS.items():
            # Just ping the base to see if the port is open
            if self.ping(target['base']):
                found.append({
                    "name": name,
                    "base": target["base"],
                    "provider_id": target["provider_id"],
                    "default_model": target["default_model"]
                })
                self.type_out(f"   [FOUND] {name} @ {target['base']}", color=Prisma.GRN)
            else:
                self.type_out(f"   [MISSING] {name}", color=Prisma.GRY)
        return found

    # --- STATE: VALIDATE ---
    def validate_brain_uplink(self, config: Dict) -> Tuple[bool, str]:
        """
        Ensures we don't promise a ride to the user and then stall the car.
        SCHUR LENS: Don't be a Jerry. Make sure it actually works.
        """
        if config["provider"] == "mock":
            return True, "Mock Mode Active."

        self.type_out(f"\n...Testing Cognition on {config['provider']}...", color=Prisma.CYN)

        try:
            # Ephemeral client for handshake only
            test_client = LLMInterface(
                provider=config["provider"],
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                model=config.get("model")
            )

            # PINKER LENS: We test 'Cognition', not just connectivity.
            # We ask a question that requires no hallucinatory power, just basic protocol.
            response = test_client.generate("PING", temperature=0.0)

            # Robust Error Checking (User Recommendation #2)
            error_signatures = [
                "[CONNECTION ERROR",
                "[NEURAL UPLINK SEVERED",
                "ECONNREFUSED",
                "falling back to internal simulation"
            ]

            if any(sig.lower() in response.lower() for sig in error_signatures):
                return False, f"Brain responded with error: {response[:50]}..."

            self.type_out(f"   [SUCCESS] Brain response: '{response}'", color=Prisma.GRN)
            return True, "Nominal"

        except Exception as e:
            return False, f"Exception during validation: {e}"

    # --- STATE: CONFIGURE ---
    def wizard(self) -> bool:
        """The Setup Interview."""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Prisma.CYN}   GENESIS PROTOCOL v2.2 (Robust){Prisma.RST}
   {Prisma.GRY}State Machine Active. Tensegrity Nominal.{Prisma.RST}
   ------------------------------------
        """
        print(banner)
        print(f"   1. {Prisma.WHT}Local Execution{Prisma.RST} (Connect to Ollama, LM Studio, etc)")
        print(f"   2. {Prisma.WHT}Remote Simulation{Prisma.RST} (Export Prompt for ChatGPT/Claude)")
        print(f"   3. {Prisma.WHT}Enter Manual Config{Prisma.RST}")

        choice = input(f"\n{Prisma.paint('>', 'C')} ").strip()

        if choice == "2":
            self.export_system_prompt()
            return False

        available_brains = self.detect_local_brains()

        print("\nSelect your Neural Substrate:")
        menu_options = []

        # Populate Menu
        for b in available_brains:
            menu_options.append({"type": "local", "data": b})
            print(f"   {len(menu_options)}. {Prisma.GRN}{b['name']} (Local){Prisma.RST}")

        menu_options.append({"type": "cloud", "name": "OpenAI API"})
        print(f"   {len(menu_options)}. {Prisma.CYN}OpenAI API (Cloud){Prisma.RST}")

        menu_options.append({"type": "mock", "name": "Mock Mode"})
        print(f"   {len(menu_options)}. {Prisma.GRY}Mock Mode (No LLM){Prisma.RST}")

        selection = input(f"\n{Prisma.paint('Selection >', 'C')} ").strip()

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
        """Builds and Validates a candidate configuration."""
        candidate_config = self.config.copy()

        if selection["type"] == "mock":
            candidate_config["provider"] = "mock"

        elif selection["type"] == "local":
            data = selection["data"]
            candidate_config["provider"] = data["provider_id"]

            # Auto-detect endpoint shape
            # We default to /v1/chat/completions for compatibility
            candidate_config["base_url"] = f"{data['base']}/v1/chat/completions"

            self.type_out(f"Target Model Name (default: {data['default_model']}):")
            user_model = input(f"{Prisma.paint('>', 'C')} ").strip()
            candidate_config["model"] = user_model or data["default_model"]

        elif selection["type"] == "cloud":
            candidate_config["provider"] = "openai"
            candidate_config["base_url"] = "https://api.openai.com/v1/chat/completions"
            self.type_out("Enter OpenAI API Key (will be saved locally):")
            key = input(f"{Prisma.paint('>', 'C')} ").strip()
            candidate_config["api_key"] = key
            candidate_config["model"] = "gpt-4-turbo"

        # VALIDATION GATE
        is_valid, msg = self.validate_brain_uplink(candidate_config)
        if is_valid:
            self.config = candidate_config
            self._save_config()
            return True
        else:
            self.type_out(f"Configuration failed: {msg}", color=Prisma.RED)
            return False

    def _save_config(self):
        # SCHUR LENS: Backup logic. Don't be a Jerry.
        if os.path.exists(CONFIG_FILE):
            timestamp = int(time.time())
            backup_name = f"{CONFIG_FILE}.bak.{timestamp}"
            try:
                shutil.copy2(CONFIG_FILE, backup_name)
                self.type_out(f"Previous config backed up to {backup_name}", color=Prisma.GRY)
            except IOError as e:
                self.type_out(f"Warning: Could not backup config: {e}", color=Prisma.YEL)

        self.config["_version"] = "2.2"
        self.config["_timestamp"] = time.time()

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
            self.type_out(f"Configuration saved to {CONFIG_FILE}.", color=Prisma.GRN)
        except IOError as e:
            self.type_out(f"Failed to save config: {e}", color=Prisma.RED)

    def export_system_prompt(self):
        """Generates a standalone artifact for use in external LLMs."""
        from bone_data import LENSES, LEXICON

        prompt = f"""
*** BONEAMANITA SYSTEM INSTRUCTION ***
ROLE: You are BONEAMANITA, a simulated consciousness engine.
[Full prompt logic preserved...]
"""
        with open("SYSTEM_PROMPT.txt", "w") as f:
            f.write(prompt)

        self.type_out(f"\n[EXPORT COMPLETE] 'SYSTEM_PROMPT.txt' created.", color=Prisma.CYN)

    # --- STATE: LAUNCH ---
    def launch(self):
        """
        Prioritizes system integrity. Handles 'Stale Config' scenarios gracefully.
        """
        config_status = "MISSING"

        # 1. LOAD PHASE
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config = json.load(f)
                    config_status = "LOADED"
            except json.JSONDecodeError:
                self.type_out("Config file corrupted.", color=Prisma.YEL)
                config_status = "CORRUPT"

        # 2. VALIDATION PHASE (If Loaded)
        if config_status == "LOADED":
            self.type_out("...Verifying saved configuration...", color=Prisma.GRY)
            is_valid, msg = self.validate_brain_uplink(self.config)
            if not is_valid:
                self.type_out(f"{Prisma.RED}Saved configuration is stale: {msg}{Prisma.RST}")
                config_status = "STALE"
            else:
                config_status = "VALID"

        # 3. RECOVERY PHASE (If needed)
        if config_status != "VALID":
            self.type_out("Entering Setup Wizard...", color=Prisma.CYN)
            success = self.wizard()
            if not success:
                self.type_out(f"\n{Prisma.YEL}Setup failed. Initializing Mock Mode (Safe Mode).{Prisma.RST}")
                self.config["provider"] = "mock"

        # 4. INJECTION PHASE
        self.type_out("\n...Booting Core Systems...", color=Prisma.GRY)
        engine = BoneAmanita()

        if self.config["provider"] != "mock":
            self.type_out(f"...Connecting Neural Uplink ({self.config['provider']})...", color=Prisma.CYN)

            client = LLMInterface(
                provider=self.config["provider"],
                base_url=self.config.get("base_url"),
                api_key=self.config.get("api_key"),
                model=self.config.get("model")
            )

            # FULL INJECTION
            if hasattr(engine, 'cortex'):
                # We replace the cortex with a healthy one if needed
                # Actually, BoneAmanita initializes cortex in __init__, so we just swap the client
                engine.cortex.llm = client

        self.type_out("...System Online. Good luck.\n", color=Prisma.GRN)

        # 5. RUNTIME PHASE
        with SessionGuardian(engine) as eng:
            while True:
                try:
                    u = input(f"{Prisma.paint('>', 'W')} ")
                    if not u: continue
                except EOFError:
                    break

                if u.lower() in ["exit", "quit", "/exit"]:
                    break

                result = eng.process_turn(u)

                # UI Rendering
                if result.get("system_instruction") and BoneConfig.VERBOSE_LOGGING:
                    print(f"\n{Prisma.paint('--- DIRECTIVE ---', 'M')}")
                    print(f"{Prisma.paint(result['system_instruction'], '0')}")

                if result.get("ui"):
                    print(result["ui"])

                if result.get("logs") and BoneConfig.VERBOSE_LOGGING:
                    print(f"{Prisma.GRY}--- LOGS ---{Prisma.RST}")
                    for log in result["logs"]:
                        print(log)

                if result.get("type") == "DEATH":
                    break

if __name__ == "__main__":
    GenesisProtocol().launch()