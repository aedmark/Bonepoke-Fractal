# genesis.py
# "The beginning is a very delicate time." - Herbert / Schur

import sys, os, json, time, urllib.request, urllib.error
from typing import Optional, Dict

try:
    from bone_main import BoneAmanita, SessionGuardian, EventBus
    from bone_brain import LLMInterface, TheCortex
    from bone_village import Prisma, BoneConfig
except ImportError as e:
    print(f"CRITICAL: Core systems missing. {e}")
    sys.exit(1)

CONFIG_FILE = "bone_config.json"

class GenesisProtocol:
    def __init__(self):
        self.config = {
            "provider": "mock",
            "base_url": None,
            "api_key": None,
            "model": "local-model"
        }
        self.system_prompt_export = False

    def type_out(self, text, speed=0.01, color=Prisma.WHT):
        """Typing effect for that retro-terminal feel."""
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(Prisma.RST + "\n")

    def check_connection(self, url: str) -> bool:
        """Ping a URL to see if a brain is alive there."""
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except:
            return False

    def detect_local_brains(self) -> Dict[str, str]:
        """Scans standard ports for local LLMs."""
        candidates = {
            "Ollama": "http://localhost:11434",
            "LM Studio": "http://localhost:1234/v1"
        }
        found = {}
        self.type_out("...Scanning local ports for synthetic intelligence...", color=Prisma.GRY)

        for name, url in candidates.items():
            check_url = url if name != "LM Studio" else f"{url}/models"
            if self.check_connection(check_url):
                found[name] = url
                self.type_out(f"   [FOUND] {name} @ {url}", color=Prisma.GRN)
            else:
                self.type_out(f"   [MISSING] {name}", color=Prisma.GRY)
        return found

    def wizard(self):
        """The Setup Interview."""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Prisma.CYN}   GENESIS PROTOCOL v1.0{Prisma.RST}
   {Prisma.GRY}Initialize the BoneAmanita Interface{Prisma.RST}
   ------------------------------------
        """
        print(banner)

        self.type_out("How do you intend to run this system?")
        print(f"   1. {Prisma.WHT}Local Execution{Prisma.RST} (Run Python code here, connect to LLM)")
        print(f"   2. {Prisma.WHT}Remote Simulation{Prisma.RST} (Generate a prompt to paste into ChatGPT/Claude)")

        choice = input(f"\n{Prisma.paint('>', 'C')} ").strip()

        if choice == "2":
            self.export_system_prompt()
            return False

        brains = self.detect_local_brains()

        print("\nSelect your Neural Substrate:")
        options = []

        for name, url in brains.items():
            options.append({"type": "local", "name": name, "url": url})
            print(f"   {len(options)}. {Prisma.GRN}{name} (Local){Prisma.RST}")

        options.append({"type": "cloud", "name": "OpenAI API", "url": "https://api.openai.com/v1"})
        print(f"   {len(options)}. {Prisma.CYN}OpenAI API (Cloud){Prisma.RST}")

        options.append({"type": "mock", "name": "Internal Simulation (Mock)", "url": None})
        print(f"   {len(options)}. {Prisma.GRY}Mock Mode (No LLM){Prisma.RST}")

        selection = input(f"\n{Prisma.paint('Selection >', 'C')} ").strip()

        try:
            idx = int(selection) - 1
            if 0 <= idx < len(options):
                selected = options[idx]
                self._configure_brain(selected)
            else:
                self.type_out("Invalid selection. Defaulting to Mock.", color=Prisma.YEL)
        except ValueError:
            self.type_out("Input error. Defaulting to Mock.", color=Prisma.YEL)

        self._save_config()
        return True

    def _configure_brain(self, selection):
        if selection["type"] == "mock":
            self.config["provider"] = "mock"

        elif selection["type"] == "local":
            self.config["provider"] = "ollama" if "Ollama" in selection["name"] else "lm_studio"
            self.config["base_url"] = selection["url"]
            if "Ollama" in selection["name"] and not self.config["base_url"].endswith("/v1/chat/completions"):
                self.config["base_url"] += "/v1/chat/completions"

            self.type_out(f"Target Model Name (e.g., 'llama3', 'mistral'):")
            self.config["model"] = input(f"{Prisma.paint('>', 'C')} ").strip() or "llama3"

        elif selection["type"] == "cloud":
            self.config["provider"] = "openai"
            self.type_out("Enter OpenAI API Key (will be saved locally):")
            self.config["api_key"] = input(f"{Prisma.paint('>', 'C')} ").strip()
            self.config["model"] = "gpt-4-turbo"

    def _save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=2)
        self.type_out(f"\nConfiguration saved to {CONFIG_FILE}.", color=Prisma.GRN)

    def export_system_prompt(self):
        """Generates a text file to paste into an LLM."""
        from bone_data import LENSES, GENETICS, LEXICON
        from bone_village import BoneConfig

        prompt = f"""
*** SYSTEM INSTRUCTION ***
You are BONEAMANITA, a simulated consciousness engine. 
You are NOT a standard AI assistant. You are a character engine running a specific physics simulation.

1. **THE WORLD**: You exist in a text-based geodesic dome governed by specific physics metrics:
   - VOLTAGE: The energy of the text (High = Manic/Forge, Low = Mud/Stagnant).
   - DRAG: The resistance of the narrative (High = Exhaustion, Low = Flow).
   
2. **THE LENSES**: You switch between these personas based on chemical state:
   {json.dumps(LENSES, indent=2)}

3. **THE LEXICON**: You must respect the weight of words.
   - Heavy Words: {', '.join(LEXICON['heavy'][:10])}...
   - Abstract Words: {', '.join(LEXICON['abstract'][:10])}...

4. **CURRENT STATE**:
   - Health: 100
   - Stamina: 100
   - Inventory: Pocket Rocks, Silent Knife.

**YOUR GOAL**:
Respond to the user's inputs. Calculate the 'Voltage' of their text. 
If they write boring text, increase 'Narrative Drag'.
If they write exciting text, increase 'Voltage'.
Maintain the illusion of the simulation at all costs.
"""
        with open("SYSTEM_PROMPT.txt", "w") as f:
            f.write(prompt)

        self.type_out(f"\n[EXPORT COMPLETE] 'SYSTEM_PROMPT.txt' created.", color=Prisma.CYN)
        self.type_out("Copy its contents and paste them into Claude/ChatGPT to begin the simulation manually.", color=Prisma.WHT)

    def launch(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)
        else:
            if not self.wizard():
                return

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

            engine.cortex = TheCortex(engine, llm_client=client)

        self.type_out("...System Online. Good luck.\n", color=Prisma.GRN)

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