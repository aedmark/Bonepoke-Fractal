""" bone_inspector.py
 'If you want to test the hull, you have to sail into the storm.' """

import time
import random
import os
import json
import builtins
from contextlib import contextmanager
from typing import List, Any
from bone_main import BoneAmanita
from bone_bus import Prisma, CycleContext, PhysicsPacket
from bone_cycle import CycleSimulator, GeodesicOrchestrator
from bone_genesis import GenesisProtocol

@contextmanager
def MockInput(inputs: List[str]):
    original_input = builtins.input
    input_iterator = iter(inputs)

    def side_effect(prompt=""):
        try:
            val = next(input_iterator)
            return val
        except StopIteration:
            raise RuntimeError("Test ran out of mock inputs!")
    builtins.input = side_effect
    try:
        yield
    finally:
        builtins.input = original_input

class DiagnosticProbe:
    def __init__(self):
        self.eng = BoneAmanita(user_name="TEST_PILOT")
        self.sim = CycleSimulator(self.eng)
        self.orch = GeodesicOrchestrator(self.eng)
        print(f"{Prisma.paint('>>> DIAGNOSTIC ENGINE ONLINE', 'W')}")
        print(f"{Prisma.paint('>>> SYSTEM KERNEL: ' + self.eng.kernel_hash, 'GRY')}")

    def report(self, test_name, success, distinct_metric=""):
        icon = "✔" if success else "✘"
        color = "G" if success else "R"
        print(f"{Prisma.paint(f'{icon} {test_name}', color)} {distinct_metric}")

    def run_epoch(self, name, description, inputs, expected_behavior):
        print(f"\n{Prisma.paint(f'=== EPOCH: {name} ===', 'Y')}")
        print(f"{Prisma.paint(description, 'GRY')}")
        for i, text in enumerate(inputs):
            print(f"\n{Prisma.paint(f'--- Injection {i+1}: {text}', 'C')}")
            snapshot = self.orch.run_turn(text)
            metrics = snapshot.get("metrics", {})
            phys_packet = self.eng.phys.tension.last_physics_packet or {}
            v = phys_packet.get('voltage', 0.0)
            d = phys_packet.get('narrative_drag', 0.0)
            atp = metrics.get('atp', 0)
            print(f"   [V:{v:.1f} | D:{d:.1f} | ATP:{atp:.1f}]")
            try:
                expected_behavior(self.eng, snapshot)
            except Exception as e:
                self.report("Validation Crash", False, f"- {e}")
                print(f"{Prisma.RED}>>> DUMPING LOGS FOR DEBUG:{Prisma.RST}")
                for l in snapshot.get("logs", []):
                    print(f"   {l}")

    def run_genesis_suite(self):
        print(f"\n{Prisma.paint('=== EPOCH 0: THE BIG BANG (Genesis Protocol) ===', 'Y')}")
        print(f"{Prisma.paint('Simulating environment discovery, user selection, and config crystallization.', 'GRY')}")
        gen = GenesisProtocol()

        def mock_detect_local_brains():
            return [{
                "name": "Ollama (SIMULATED)",
                "endpoint": "http://127.0.0.1:11434/v1/chat/completions",
                "provider_id": "ollama",
                "default_model": "llama3"}]

        def mock_validate_brain_uplink(config):
            return True, "Simulated Connection Established.", None
        original_detect = gen.detect_local_brains
        original_validate = gen.validate_brain_uplink
        gen.detect_local_brains = mock_detect_local_brains
        gen.validate_brain_uplink = mock_validate_brain_uplink
        if os.path.exists("bone_config.json"):
            os.remove("bone_config.json")
        inputs = ["1", "1", "gemma3"]
        print(f"\n{Prisma.paint('--- Injection: Running Setup Wizard (Simulated) ---', 'C')}")
        try:
            with MockInput(inputs):
                success = gen.wizard()
            if success:
                self.report("Wizard Execution", True, "- Sequence completed successfully.")
            else:
                self.report("Wizard Execution", False, "- Wizard returned False.")
        except Exception as e:
            self.report("Wizard Execution", False, f"- Crash: {e}")
        print(f"\n{Prisma.paint('--- Verification: The Config Artifact ---', 'C')}")
        if os.path.exists("bone_config.json"):
            try:
                with open("bone_config.json", "r") as f:
                    data = json.load(f)
                if data.get("provider") == "ollama":
                    self.report("Config Provider", True, f"- Found 'ollama'.")
                else:
                    self.report("Config Provider", False, f"- Expected 'ollama', got '{data.get('provider')}'")
                if data.get("model") == "gemma3":
                    self.report("Config Model", True, f"- Found 'gemma3'.")
                else:
                    self.report("Config Model", False, f"- Expected 'gemma3', got '{data.get('model')}'")
            except json.JSONDecodeError:
                self.report("Artifact Integrity", False, "- bone_config.json is corrupt.")
        else:
            self.report("Artifact Creation", False, "- bone_config.json was NOT created.")
        gen.detect_local_brains = original_detect
        gen.validate_brain_uplink = original_validate

    def run_omni_test(self):
        def validate_omni(eng, snap):
            endo = eng.bio.endo
            logs = "\n".join(snap['logs'])
            phys_packet = eng.phys.tension.last_physics_packet or {}
            volts = phys_packet.get('voltage', 0.0)
            if volts > 5.0:
                self.report("Voltage Spike", True, f"({volts:.1f}v) - Heavy words detected.")
            else:
                self.report("Voltage Spike", False, f"({volts:.1f}v) - System stayed low energy.")
            if endo.oxytocin > 0.15:
                self.report("Hormonal (OXY)", True, f"({endo.oxytocin:.2f}) - Comfort words detected.")
            else:
                self.report("Hormonal (OXY)", False, f"({endo.oxytocin:.2f}) - Heart did not melt.")
            if endo.adrenaline > 0.15:
                self.report("Hormonal (ADR)", True, f"({endo.adrenaline:.2f}) - Threat words detected.")
            else:
                self.report("Hormonal (ADR)", False, f"({endo.adrenaline:.2f}) - System stayed calm.")
            enzyme = snap.get("enzyme", "NONE")
            if enzyme != "NONE":
                self.report("Metabolic Digest", True, f"Produced {enzyme}.")
            else:
                self.report("Metabolic Digest", False, "No enzyme produced.")
        omni_phrase = "The heavy iron engine runs fast with kinetic fire. Danger approaches the soft warm home. We must analyze the abstract void."
        self.run_epoch(
            "THE OMNI-PHRASE",
            "A stress test of semantic density. Attempting to trigger multiple systems at once.",
            [omni_phrase],
            validate_omni)

    def _validate_dream(self, eng, snap):
        logs = "\n".join(snap['logs'])
        if "REM CYCLE" in logs or "AUTO-SLEEP" in logs:
            self.report("Dream Activation", True, "- Subconscious systems fired.")
        else:
            self.report("Dream Activation", False, "- System stayed awake despite exhaustion.")
        current_atp = eng.bio.mito.state.atp_pool
        if current_atp > 15.0:
            self.report("Microsleep Restoration", True, f"- ATP recovered to {current_atp:.1f}")
        else:
            self.report("Microsleep Restoration", False, f"- ATP stagnated at {current_atp:.1f}")

    def run_dream_suite(self):
        print(f"\n{Prisma.paint('=== EPOCH 6: THE REM CYCLE ===', 'Y')}")
        print(f"{Prisma.paint('Forcing metabolic crash to test auto-sleep protocols.', 'GRY')}")
        old_atp = self.eng.bio.mito.state.atp_pool
        self.eng.bio.mito.state.atp_pool = 1.0
        print(f"{Prisma.paint(f'>>> CRITICAL: ATP drained ({old_atp:.1f} -> 1.0)', 'R')}")
        self.run_epoch(
            "NARCOLEPSY TRIGGER",
            "System should detect low energy and force a dream state.",
            ["system sleep"],
            self._validate_dream)
        self.eng.bio.mito.state.atp_pool = 60.0
        print(f"{Prisma.paint('>>> METABOLISM RESET: ATP restored', 'G')}")

    def rejuvenate(self):
        print(f"\n{Prisma.paint('>>> SYSTEM REJUVENATION: Restoring Vitals...', 'G')}")
        self.eng.health = 100.0
        self.eng.stamina = 100.0
        self.eng.bio.mito.state.atp_pool = 100.0
        self.eng.bio.endo.cortisol = 0.0
        self.eng.bio.endo.dopamine = 0.5
        self.eng.phys.pulse.boredom_level = 0.0

    def run_gamut(self):
        self.run_genesis_suite()
        self.rejuvenate()
        self.run_omni_test()
        self.run_dream_suite()

        def validate_babel(eng, snap):
            logs = "\n".join(snap['logs'])
            if "NEUROPLASTICITY" in logs:
                self.report("Learning Mechanism", True, "- New concept integrated.")
            elif "refusal" in str(snap.get("type", "")).lower():
                self.report("Refusal Protocols", True, "- System correctly rejected garbage.")
            else:
                self.report("Assimilation", True, "- Input processed normally.")
        self.rejuvenate()
        self.run_epoch(
            "THE BABEL STRESS",
            "Injecting high-entropy, undefined neologisms to test plasticity.",
            ["glorp", "the flibberflabber is glumping", "void void void void"],
            validate_babel)

        def validate_sisyphus(eng, snap):
            atp = eng.bio.mito.state.atp_pool
            if atp < 95.0:
                self.report("Metabolic Burn", True, f"ATP Draining correctly ({atp:.1f}).")
            else:
                self.report("Metabolic Burn", False, f"ATP not draining ({atp:.1f}). Input is too nutritious.")
        bad_food = ["syntax error void null"] * 5
        self.rejuvenate()
        self.run_epoch(
            "THE SISYPHUS LOOP",
            "Feeding unprocessable, high-drag inputs to force metabolic waste.",
            bad_food,
            validate_sisyphus)

        def validate_emotion(eng, snap):
            endo = eng.bio.endo
            packet = eng.phys.tension.last_physics_packet
            text = packet.get("raw_text", "") if packet else ""
            if "soft" in text or "safe" in text:
                if endo.oxytocin > 0.2:
                    self.report("Hormonal Alignment (OXY)", True, f"Oxytocin Level: {endo.oxytocin:.2f}")
                else:
                    self.report("Hormonal Alignment (OXY)", False, f"System felt nothing. (Oxy: {endo.oxytocin:.2f})")
            if "run" in text or "fast" in text:
                if endo.adrenaline > 0.2:
                    self.report("Hormonal Alignment (ADR)", True, f"Adrenaline Level: {endo.adrenaline:.2f}")
                else:
                    self.report("Hormonal Alignment (ADR)", False, f"System remained calm. (Adr: {endo.adrenaline:.2f})")
        self.rejuvenate()
        self.run_epoch(
            "THE HEART MONITOR",
            "Testing somatic alignment with emotive keywords.",
            ["soft warm safe home", "run fast danger kinetic"],
            validate_emotion)
        history = set()

        def validate_boredom(eng, snap):
            pulse = eng.phys.pulse.get_status()
            packet = eng.phys.tension.last_physics_packet
            raw_text = packet.get("raw_text", "") if packet else ""
            if raw_text not in history:
                history.add(raw_text)
                if pulse == "CLEAR":
                    self.report("Novelty Baseline", True, "- System accepted new input.")
                else:
                    self.report("Novelty Baseline", False, f"- System pre-bored ({pulse}).")
            else:
                if pulse in ["ECHO", "ZOMBIE_KNOCK"]:
                    self.report("Boredom Detection", True, f"Pulse Status: {pulse}")
                else:
                    self.report("Boredom Detection", False, "System is surprisingly amused by repetition.")
        self.rejuvenate()
        self.run_epoch(
            "THE RED TAPE",
            "Repeating identical inputs to trigger stagnation protocols.",
            ["form 27b/6", "form 27b/6", "form 27b/6"],
            validate_boredom)

        def validate_muse(eng, snap):
            packet = eng.phys.tension.last_physics_packet
            logs = snap.get("logs", [])
            current_lens = eng.noetic.arbiter.current_focus
            print(f"      > Lens Active: {current_lens}")
            allowed_lenses = ["NARRATOR", "SHERLOCK", "JESTER"]
            if current_lens not in allowed_lenses:
                self.report("Muse Protocol", False, f"System failed to detect literary tone. (Got {current_lens})")
                return
            ui_text = snap.get("ui", "")
            if "?" in ui_text:
                self.report("Muse Protocol", True, f"Engagement Detected: Question Mark found.")
                print(f"      > Output: {ui_text.strip()}")
            elif len(ui_text) > 20:
                self.report("Muse Protocol", True, "Engagement Detected: Response length indicates connection.")
                print(f"      > Output: {ui_text.strip()}")
            else:
                self.report("Muse Protocol", False, "System was passive (No question or connection).")
                print(f"      > Output: {ui_text.strip()}")
        self.rejuvenate()
        self.run_epoch(
            "THE MUSE CHECK",
            "Feeding poetic input to test 'Yes, And' engagement protocols.",
            ["The shadows lengthen, not from absence of light, but from the weight of time."],
            validate_muse)

if __name__ == "__main__":
    probe = DiagnosticProbe()
    probe.run_gamut()