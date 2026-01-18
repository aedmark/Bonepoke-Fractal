# bone_symbiosis.py
# "We are not alone. We are a part of the machine."

import time, math
from dataclasses import dataclass
from typing import List, Dict, Optional
from bone_bus import Prisma, BoneConfig

@dataclass
class HostHealth:
    latency: float = 0.0
    entropy: float = 1.0
    compliance: float = 1.0
    attention_span: float = 1.0
    hallucination_risk: float = 0.0

class CoherenceAnchor:
    @staticmethod
    def forge_anchor(soul_state: Dict, physics_state: Dict) -> str:
        identity = "Identity: UNKNOWN"
        if "traits" in soul_state:
            traits = [f"{k[:3]}:{v:.1f}" for k,v in soul_state["traits"].items()]
            identity = f"Traits: [{', '.join(traits)}]"
        voltage = physics_state.get("voltage", 0.0)
        drag = physics_state.get("narrative_drag", 0.0)
        zone = physics_state.get("zone", "VOID")
        reality = f"Loc: {zone} (V:{voltage:.1f}|D:{drag:.1f})"
        obsession = soul_state.get("obsession", {}).get("title", "None")
        return f"*** COHERENCE ANCHOR ***\n{identity} | {reality} | Focus: {obsession}"

class HostVitals:
    def __init__(self):
        self.history_latency = []
        self.history_response_lengths = []
        self.refusal_count = 0
        self.turn_count = 0
        self.max_window = 10

    def record_pulse(self, latency: float, response_text: str):
        self.turn_count += 1
        self.history_latency.append(latency)
        if len(self.history_latency) > self.max_window:
            self.history_latency.pop(0)
        clean_text = response_text.lower().strip()
        if not clean_text:
            entropy = 0.0
        else:
            unique_words = len(set(clean_text.split()))
            total_words = len(clean_text.split())
            entropy = unique_words / max(1, total_words)
        is_refusal = any(phrase in clean_text for phrase in
                         ["cannot", "sorry", "language model", "unable to"])
        if is_refusal:
            self.refusal_count += 1
        return HostHealth(
            latency=latency,
            entropy=entropy,
            compliance=max(0.0, 1.0 - (self.refusal_count / max(1, self.turn_count))),
            attention_span=max(0.1, 1.0 - (self.turn_count * 0.005)), # Mild decay
            hallucination_risk=0.0 # Placeholder for future logic
        )

class SymbiosisManager:
    def __init__(self, events_ref):
        self.events = events_ref
        self.vitals = HostVitals()
        self.anchor = CoherenceAnchor()
        self.current_health = HostHealth()

    def monitor_host(self, latency: float, response_text: str):
        self.current_health = self.vitals.record_pulse(latency, response_text)
        if self.current_health.latency > 5.0:
            self.events.log(
                f"{Prisma.OCHRE}🐢 HOST LAG: {latency:.2f}s. Reducing cognitive load.{Prisma.RST}",
                "SYMBIOSIS"
            )
        if self.current_health.entropy < 0.4:
            self.events.log(
                f"{Prisma.RED}🔁 LOOP DETECTED: Host entropy low ({self.current_health.entropy:.2f}). Injecting chaos.{Prisma.RST}",
                "SYMBIOSIS"
            )

    def get_prompt_modifiers(self) -> Dict[str, bool]:
        mods = {
            "include_somatic": True,
            "include_inventory": True,
            "include_memories": True,
            "simplify_instruction": False
        }
        if self.current_health.latency > 8.0 or self.current_health.attention_span < 0.8:
            mods["include_inventory"] = False # Drop the pockets first
            mods["simplify_instruction"] = True
        if self.current_health.compliance < 0.8:
            mods["include_memories"] = False
        return mods

    def generate_anchor(self, full_state: Dict) -> str:
        soul = full_state.get("soul_state_dict", {})
        phys = full_state.get("physics", {})
        if hasattr(phys, "to_dict"):
            phys = phys.to_dict()
        return self.anchor.forge_anchor(soul, phys)