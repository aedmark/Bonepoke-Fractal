""" bone_genesis.py 'Simplicity is the ultimate sophistication.' - Vinci """

import sys, os, json, time, urllib.request, traceback, random
from typing import Optional, Dict, Any
from bone_main import BoneAmanita, SessionGuardian
from bone_brain import LLMInterface, TheCortex
from bone_village import Prisma
from bone_data import TheLore

CONFIG_FILE = "bone_config.json"

class GenesisProtocol:
    def __init__(self):
        self.tutorial_mode = False
        self.config: Dict[str, Any] = {
            "provider": "mock",
            "base_url": None,
            "api_key": "sk-dummy-key",
            "model": "local-model"}
        self.DISCOVERY_TARGETS = {
            "Ollama": {"url": "http://127.0.0.1:11434/v1/chat/completions", "check": "/api/tags"},
            "LM Studio": {"url": "http://127.0.0.1:1234/v1/chat/completions", "check": "/v1/models"},
            "LocalAI": {"url": "http://127.0.0.1:8080/v1/chat/completions", "check": "/v1/models"},}

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
        print(f"{Prisma.GRY}   [SYSTEM] Config saved to '{CONFIG_FILE}'.{Prisma.RST}")

    def scan_local_brains(self) -> list:
        found = []
        print(f"{Prisma.GRY}...Scanning local frequencies...{Prisma.RST}")
        for name, data in self.DISCOVERY_TARGETS.items():
            try:
                root = data['url'].rsplit('/', 3)[0]
                urllib.request.urlopen(f"{root}{data['check']}", timeout=0.2)
                found.append({"name": name, "url": data['url']})
                print(f"   {Prisma.GRN}[FOUND] {name}{Prisma.RST}")
            except Exception:
                pass
        return found

    def setup_uplink(self) -> bool:
        print(f"\n{Prisma.CYN}=== GENESIS PROTOCOL SETUP ==={Prisma.RST}")
        local_brains = self.scan_local_brains()
        while True:
            t_status = f"{Prisma.GRN}ON{Prisma.RST}" if self.tutorial_mode else f"{Prisma.RED}OFF{Prisma.RST}"
            print(f"\nSelect Neural Substrate:")
            print(f"   0. {Prisma.WHT}Toggle Boot Camp (Tutorial){Prisma.RST} [{t_status}]")
            opts = [{"name": "Mock Mode (Simulation Only)", "provider": "mock"}]
            opts += [{"name": b["name"], "provider": "openai", "url": b["url"]} for b in local_brains]
            opts.append({"name": "Manual / Cloud Configuration", "provider": "manual"})
            for idx, opt in enumerate(opts):
                print(f"   {idx+1}. {Prisma.WHT}{opt['name']}{Prisma.RST}")
            sel = input(f"{Prisma.paint('>', 'C')} ").strip()
            if sel == "0":
                self.tutorial_mode = not self.tutorial_mode
                print(f"{Prisma.GRY}   > Boot Camp toggled.{Prisma.RST}")
                continue
            if not sel.isdigit(): return False
            choice_idx = int(sel) - 1
            if choice_idx < 0 or choice_idx >= len(opts): return False
            choice = opts[choice_idx]
            if choice["provider"] == "mock":
                self.config.update({"provider": "mock"})
            elif choice["provider"] == "manual":
                print(f"{Prisma.OCHRE}--- Manual Override ---{Prisma.RST}")
                self.config["provider"] = input("Provider (openai/ollama/mock): ").strip() or "openai"
                self.config["base_url"] = input("Base URL (http://...): ").strip()
                self.config["api_key"] = input("API Key: ").strip() or "sk-dummy-key"
                self.config["model"] = input("Model Name: ").strip() or "gpt-3.5-turbo"
            else:
                self.config["provider"] = "openai"
                self.config["base_url"] = choice["url"]
                print(f"Target Model for {choice['name']} (default: local-model):")
                self.config["model"] = input(f"{Prisma.paint('>', 'C')} ").strip() or "local-model"
            break
        if self.config["provider"] != "mock":
            print(f"{Prisma.GRY}...Testing Uplink...{Prisma.RST}")
            try:
                test = LLMInterface(**self.config)
                test.generate("Ping.", {"max_tokens": 1})
                print(f"{Prisma.GRN}[SUCCESS] Signal Clear.{Prisma.RST}")
            except Exception as e:
                print(f"{Prisma.RED}[FAILURE] {e}{Prisma.RST}")
                if input("Save anyway? (y/N) ").lower() != 'y': return False
        self._save_config()
        return True

    def _get_user_identity(self, engine):
        if self.config.get("user_name"):
            engine.user_name = self.config["user_name"]
            return
        print(f"\n{Prisma.CYN}[IDENTITY REQUIRED]{Prisma.RST}")
        uid = input("Designation: ").strip()
        if uid:
            engine.user_name = uid
            self.config["user_name"] = uid
            self._save_config()

    def launch(self):
        if not os.path.exists(CONFIG_FILE):
            if not self.setup_uplink():
                print("Setup aborted. Launching in Mock Mode.")
        else:
            try:
                with open(CONFIG_FILE) as f: self.config = json.load(f)
            except:
                print("Config corrupt. Re-running setup.")
                self.setup_uplink()
        print(f"\n{Prisma.GRY}...Booting BoneAmanita Core...{Prisma.RST}")
        engine = BoneAmanita(tutorial_mode=self.tutorial_mode)
        self._get_user_identity(engine)
        if self.config["provider"] != "mock":
            try:
                client = LLMInterface(
                    events_ref=engine.events,
                    provider=self.config["provider"],
                    base_url=self.config.get("base_url"),
                    api_key=self.config.get("api_key"),
                    model=self.config.get("model"))
                engine.cortex = TheCortex(engine, llm_client=client)
                print(f"{Prisma.GRN}[SYSTEM] Cortex Online: {self.config['model']}{Prisma.RST}")
            except Exception as e:
                print(f"{Prisma.RED}[ERROR] Cortex Failed: {e}. Falling back to Mock.{Prisma.RST}")
        print(f"{Prisma.GRN}System Online. Welcome, {engine.user_name}.\n{Prisma.RST}")
        with SessionGuardian(engine) as session:
            if hasattr(engine, 'cortex'):
                scenarios = TheLore.get_instance().get("SCENARIOS")
                archetypes = scenarios.get("ARCHETYPES", []) if scenarios else []
                seed = random.choice(archetypes) if archetypes else "a vivid, specific location"
                if self.tutorial_mode:
                    boot_prompt = (
                        f"INIT_SEQUENCE. User: {engine.user_name}. "
                        f"LOCATION DATA LOADED: {seed}. "
                        "STATUS: Visual sensors are OFFLINE. Audio/Olfactory sensors: LOW POWER. "
                        "Do NOT describe the location yet. "
                        "Generate a system startup log describing a pitch-black void or static. "
                        "You may include a SINGLE, faint sound or smell that hints at the location, but keep it subtle. "
                        "End with: 'System blind. Awaiting command: LOOK.'")
                else:
                    boot_prompt = (
                        f"INIT_SEQUENCE. User: {engine.user_name}. "
                        f"IMMEDIATELY generate: {seed}. "
                        "Focus primarily on VISUAL atmosphere and lighting. "
                        "Do NOT treat senses as a checklist (e.g. don't force smell/taste unless critical). "
                        "Do NOT mention the user's inventory or equipment unless asked. "
                        "End with: 'What would you like to do?'")

                res = session.process_turn(boot_prompt)
                if res.get("ui"): print(res["ui"])

            while True:
                try:
                    u_in = input(f"{Prisma.paint('>', 'W')} ")
                    if u_in.strip() == "<<<":
                        print(f"{Prisma.GRY}   [Multi-line. Type '>>>' to send]{Prisma.RST}")
                        lines = []
                        while True:
                            l = input("... ")
                            if l.strip() == ">>>": break
                            lines.append(l)
                        u_in = "\n".join(lines)
                    if u_in.lower() in ["/exit", "exit", "quit"]: break
                    result = session.process_turn(u_in)
                    if result.get("ui"): print(result["ui"])
                except KeyboardInterrupt:
                    print("\nSignal Lost.")
                    break
                except Exception as e:
                    print(f"{Prisma.RED}CRASH: {e}{Prisma.RST}")
                    traceback.print_exc()

if __name__ == "__main__":
    GenesisProtocol().launch()