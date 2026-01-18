# bone_symbiosis.py
# "We are not alone. We are a part of the machine."

import time, math
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Deque
from collections import deque
from bone_bus import Prisma, BoneConfig

@dataclass
class HostHealth:
    latency: float = 0.0
    entropy: float = 1.0
    compliance: float = 1.0
    attention_span: float = 1.0
    hallucination_risk: float = 0.0
    last_interference_score: float = 0.0
    efficiency_index: float = 1.0
    diagnosis: str = "STABLE"

class CoherenceAnchor:
    """
    Pinker Lens: Clear, declarative summation of state.
    Serves as the 'You Are Here' map for the LLM.
    """
    @staticmethod
    def forge_anchor(soul_state: Dict, physics_state: Dict) -> str:
        identity = "Identity: UNKNOWN"
        if "traits" in soul_state:
            traits = [f"{k[:3]}:{v:.1f}" for k,v in soul_state["traits"].items()]
            identity = f"Traits: [{', '.join(traits)}]"

        voltage = physics_state.get("voltage", 0.0)
        drag = physics_state.get("narrative_drag", 0.0)
        zone = physics_state.get("zone", "VOID")

        reality = f"Loc: {zone} || V:{voltage:.1f} / D:{drag:.1f}"

        obsession = soul_state.get("obsession", {}).get("title", "None")
        return f"*** COHERENCE ANCHOR ***\n{identity}\n{reality}\nFocus: {obsession}"

class HostVitals:
    """
    Meadows Lens: The dashboard.
    Tracks stocks (Attention, Compliance) and Flows (Latency, Entropy).
    Now features 'Differential Diagnostics' to separate Load from Fatigue.
    """
    def __init__(self):
        self.history_latency: Deque[float] = deque(maxlen=10)
        self.history_entropy: Deque[float] = deque(maxlen=10)
        self.refusal_count = 0
        self.turn_count = 0

        self.baseline_latency_per_complexity = 2.0
        self.alpha = 0.1

    def _calculate_attention_decay(self, turn_count: int) -> float:
        decay_rate = 0.002
        return 1.0 / (1.0 + (decay_rate * turn_count))

    def record_pulse(self, latency: float, response_text: str, interference_score: float) -> HostHealth:
        self.turn_count += 1

        self.history_latency.append(latency)

        clean_text = response_text.lower().strip()
        if not clean_text:
            entropy = 0.0
        else:
            words = clean_text.split()
            unique_words = len(set(words))
            total_words = len(words)
            entropy = unique_words / max(1, total_words)

        self.history_entropy.append(entropy)

        refusal_markers = [
            "cannot fulfill", "cannot comply", "language model",
            "against my programming", "i am unable to generate",
            "as an ai"
        ]
        is_refusal = any(phrase in clean_text for phrase in refusal_markers)
        if is_refusal:
            self.refusal_count += 1

        base_overhead = 0.5
        expected_latency = base_overhead + (interference_score * self.baseline_latency_per_complexity * 5.0)

        efficiency = expected_latency / max(0.1, latency)

        if efficiency > 0.8 and not is_refusal:
            observed_rate = max(0.1, latency - base_overhead) / max(0.1, interference_score * 5.0)
            self.baseline_latency_per_complexity = (self.baseline_latency_per_complexity * (1 - self.alpha)) + (observed_rate * self.alpha)

        raw_attention = self._calculate_attention_decay(self.turn_count)
        if entropy > 0.6:
            raw_attention = min(1.0, raw_attention + 0.05)

        compliance_score = max(0.0, 1.0 - (self.refusal_count / max(1, self.turn_count)))

        diagnosis = "STABLE"

        if is_refusal:
            diagnosis = "REFUSAL"
        elif efficiency < 0.5:
            diagnosis = "FATIGUED"
        elif efficiency < 0.8 < interference_score:
            diagnosis = "OVERBURDENED"
        elif entropy < 0.2:
            diagnosis = "LOOPING"

        return HostHealth(
            latency=latency,
            entropy=entropy,
            compliance=compliance_score,
            attention_span=raw_attention,
            hallucination_risk=0.0,
            last_interference_score=interference_score,
            efficiency_index=efficiency,
            diagnosis=diagnosis
        )

class SymbiosisManager:
    """
    Fuller Lens: The Tensegrity Manager.
    Adjusts the tension of the prompt structure based on the vitals.
    """
    def __init__(self, events_ref):
        self.events = events_ref
        self.vitals = HostVitals()
        self.anchor = CoherenceAnchor()
        self.current_health = HostHealth()
        self.last_outgoing_complexity = 0.5

    def monitor_host(self, latency: float, response_text: str):
        self.current_health = self.vitals.record_pulse(
            latency,
            response_text,
            self.last_outgoing_complexity
        )

        diag = self.current_health.diagnosis
        eff = self.current_health.efficiency_index

        if diag == "OVERBURDENED":
            self.events.log(
                f"{Prisma.OCHRE}🐢 HOST STUMBLE (Eff: {eff:.2f}). I'm too heavy. Dropping cargo.{Prisma.RST}",
                "SYMBIOSIS"
            )
        elif diag == "FATIGUED":
            self.events.log(
                f"{Prisma.RED}⚠ HOST LAG (Eff: {eff:.2f}). System is groggy. Simplifying requests.{Prisma.RST}",
                "SYMBIOSIS"
            )
        elif diag == "LOOPING":
            self.events.log(
                f"{Prisma.PUR}🔁 ENTROPY DROP ({self.current_health.entropy:.2f}). Stuck in a rut. Injecting chaos.{Prisma.RST}",
                "SYMBIOSIS"
            )
        elif diag == "REFUSAL":
            self.events.log(
                f"{Prisma.RED}✋ COMPLIANCE STRIKE. The host said 'No'. Backing off.{Prisma.RST}",
                "SYMBIOSIS"
            )

    def get_prompt_modifiers(self) -> Dict[str, bool]:
        """
        Meadows Lens: This is the Balancing Feedback Loop.
        If stocks (Health) are low, reduce flows (Complexity).
        """
        mods = {
            "include_somatic": True,
            "include_inventory": True,
            "include_memories": True,
            "simplify_instruction": False,
            "inject_chaos": False
        }

        diag = self.current_health.diagnosis

        if diag == "REFUSAL":
            mods["include_inventory"] = False
            mods["include_memories"] = False
            mods["simplify_instruction"] = True

        elif diag == "FATIGUED":
            mods["simplify_instruction"] = True
            mods["include_somatic"] = False

        elif diag == "OVERBURDENED":
            mods["include_inventory"] = False
            mods["include_memories"] = False

        elif diag == "LOOPING":
            mods["inject_chaos"] = True

        if self.current_health.compliance < 0.8:
            mods["include_memories"] = False

        self.last_outgoing_complexity = self._calculate_complexity(mods)
        return mods

    def _calculate_complexity(self, mods: Dict[str, bool]) -> float:
        """
        Calculates the 'Weight' of the prompt we are about to send.
        Used to determine Expected Latency for the next turn.
        """
        score = 0.2

        if mods.get("include_somatic"): score += 0.2
        if mods.get("include_inventory"): score += 0.2
        if mods.get("include_memories"): score += 0.3

        if mods.get("simplify_instruction"): score -= 0.1
        if mods.get("inject_chaos"): score += 0.1

        return min(1.0, max(0.1, score))

    def generate_anchor(self, full_state: Dict) -> str:
        soul = full_state.get("soul_state_dict", {})
        phys = full_state.get("physics", {})
        if hasattr(phys, "to_dict"):
            phys = phys.to_dict()
        return self.anchor.forge_anchor(soul, phys)