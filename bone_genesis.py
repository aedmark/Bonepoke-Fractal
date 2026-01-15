# bone_genesis.py
# "The beginning is a very delicate time." - Herbert / Schur / SLASH

import sys
import os
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, Tuple, List

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

        self.API_SHAPES = {
            "Ollama": {
                "base": "http://localhost:11434",
                "check": "/api/tags",
                "endpoint": "/v1/chat/completions",
                "provider_id": "ollama"
            },
            "LM Studio": {
                "base": "http://localhost:1234",
                "check": "/v1/models",
                "endpoint": "/v1/chat/completions",
                "provider_id": "lm_studio"
            },
            "LocalAI": {
                "base": "http://localhost:8080",
                "check": "/readyz",
                "endpoint": "/v1/chat/completions",
                "provider_id": "ollama"
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
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=1) as _:
                return True
        except:
            return False

    # --- STATE: DETECT ---
    def detect_local_brains(self) -> List[Dict]:
        """Scans known ports to reduce cognitive load on the user."""
        found = []
        self.type_out("...Scanning local ports for synthetic intelligence...", color=Prisma.GRY)

        for name, shape in self.API_SHAPES.items():
            check_url = f"{shape['base']}{shape['check']}"
            if self.ping(check_url):
                full_endpoint = f"{shape['base']}{shape['endpoint']}"
                found.append({
                    "name": name,
                    "url": full_endpoint,
                    "base": shape["base"],
                    "provider_id": shape["provider_id"]
                })
                self.type_out(f"   [FOUND] {name} @ {shape['base']}", color=Prisma.GRN)
            else:
                self.type_out(f"   [MISSING] {name}", color=Prisma.GRY)
        return found

    # --- STATE: VALIDATE ---
    def validate_brain_uplink(self, config: Dict) -> bool:
        """
        Ensures we don't promise a ride to the user and then stall the car.
        """
        if config["provider"] == "mock":
            return True

        self.type_out(f"\n...Testing Uplink to {config['provider']}...", color=Prisma.CYN)

        try:
            # Ephemeral client for handshake only
            test_client = LLMInterface(
                provider=config["provider"],
                base_url=config.get("base_url"),
                api_key=config.get("api_key"),
                model=config.get("model")
            )

            response = test_client.generate("PING", temperature=0.0)

            # Check for the specific fallback signature from bone_brain.py
            if response.startswith("[NEURAL UPLINK SEVERED"):
                self.type_out(f"   [FAILURE] Brain refused connection: {response}", color=Prisma.RED)
                return False

            self.type_out(f"   [SUCCESS] Brain responded.", color=Prisma.GRN)
            return True
        except Exception as e:
            self.type_out(f"   [ERROR] Connection failed: {e}", color=Prisma.RED)
            return False

    # --- STATE: CONFIGURE ---
    def wizard(self) -> bool:
        """The Setup Interview. Returns True if a valid config is created."""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Prisma.CYN}   GENESIS PROTOCOL v2.1 (Patched){Prisma.RST}
   {Prisma.GRY}State Machine Active. Tensegrity Nominal.{Prisma.RST}
   ------------------------------------
        """
        print(banner)
        print(f"   1. {Prisma.WHT}Local Execution{Prisma.RST} (Connect to Ollama, LM Studio, etc)")
        print(f"   2. {Prisma.WHT}Remote Simulation{Prisma.RST} (Export Prompt for ChatGPT/Claude)")

        choice = input(f"\n{Prisma.paint('>', 'C')} ").strip()

        if choice == "2":
            self.export_system_prompt()
            return False

        # 1. Detection Phase
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
            candidate_config["base_url"] = data["url"]

            self.type_out(f"Target Model Name (e.g., 'llama3', 'mistral'):")
            user_model = input(f"{Prisma.paint('>', 'C')} ").strip()
            candidate_config["model"] = user_model or "local-model"

        elif selection["type"] == "cloud":
            candidate_config["provider"] = "openai"
            candidate_config["base_url"] = "https://api.openai.com/v1/chat/completions"
            self.type_out("Enter OpenAI API Key (will be saved locally):")
            key = input(f"{Prisma.paint('>', 'C')} ").strip()
            candidate_config["api_key"] = key
            candidate_config["model"] = "gpt-4-turbo"

        # VALIDATION GATE
        if self.validate_brain_uplink(candidate_config):
            self.config = candidate_config
            self._save_config()
            return True
        else:
            self.type_out("Configuration failed validation. Falling back...", color=Prisma.YEL)
            return False

    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
            self.type_out(f"Configuration saved to {CONFIG_FILE}.", color=Prisma.GRN)
        except IOError as e:
            self.type_out(f"Failed to save config: {e}", color=Prisma.RED)

    def export_system_prompt(self):
        """
        Generates a standalone artifact for use in external LLMs.
        This allows the system's 'Soul' to be portable.
        """
        from bone_data import LENSES, LEXICON

        # Safe extraction of lists for string formatting to prevent index errors
        heavy_words = LEXICON.get('heavy', ["stone", "iron", "lead"])
        explosive_words = LEXICON.get('explosive', ["run", "break", "burst"])

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
        self.type_out("Copy contents to Claude/ChatGPT to run Remote Simulation.", color=Prisma.WHT)

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
            if not self.validate_brain_uplink(self.config):
                self.type_out(f"{Prisma.RED}Saved configuration is stale.{Prisma.RST}")
                config_status = "STALE"
            else:
                config_status = "VALID"

        # 3. RECOVERY PHASE (If needed)
        if config_status != "VALID":
            self.type_out("Entering Setup Wizard...", color=Prisma.CYN)
            success = self.wizard()
            if not success:
                # SCHUR LENS: The "Janet" Fallback.
                # Don't just die. Offer a safe playground.
                self.type_out(f"\n{Prisma.YEL}Setup failed. Initializing Mock Mode (Safe Mode).{Prisma.RST}")
                self.config["provider"] = "mock"

        # 4. INJECTION PHASE
        self.type_out("\n...Booting Core Systems...", color=Prisma.GRY)
        engine = BoneAmanita()

        if self.config["provider"] != "mock":
            self.type_out(f"...Connecting Neural Uplink ({self.config['provider']})...", color=Prisma.CYN)

            # Create the persistent client
            client = LLMInterface(
                provider=self.config["provider"],
                base_url=self.config.get("base_url"),
                api_key=self.config.get("api_key"),
                model=self.config.get("model")
            )

            # Surgical Injection
            if hasattr(engine, 'cortex'):
                engine.cortex.llm = client
            else:
                engine.cortex = TheCortex(engine, llm_client=client)

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

                # UI Rendering Logic (Preserved)
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