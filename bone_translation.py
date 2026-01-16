# bone_translation.py
# "Translate the math of the spheres into the words of the earth." - SLASH

from dataclasses import dataclass
from typing import Any
from bone_bus import Prisma

@dataclass
class SemanticState:
    """Translates raw 'Physics' numbers into Cognitive concepts."""
    tone_instruction: str
    pacing_instruction: str
    focus_instruction: str
    physical_sensation: str
    metaphorical_context: str

class RosettaStone:
    """
    The bridge between bone_physics (The Math) and bone_brain (The Words).
    Decouples observation from interpretation.
    """

    @staticmethod
    def translate(physics: Any, bio: Any) -> SemanticState:
        # Extract raw metrics safely
        # We handle both dicts and objects to be safe
        if isinstance(physics, dict):
            vol = physics.get("voltage", 0.0)
            drag = physics.get("narrative_drag", 0.0)
            kappa = physics.get("kappa", 0.0)
            entropy = physics.get("E", 0.0)
        else:
            vol = getattr(physics, "voltage", 0.0)
            drag = getattr(physics, "narrative_drag", 0.0)
            kappa = getattr(physics, "kappa", 0.0)
            entropy = getattr(physics, "E", 0.0)

        # 1. Interpret Voltage (Energy/Arousal)
        if vol > 15.0:
            tone = "Manic, high-frequency, bordering on incoherent."
            pacing = "Rapid-fire. Short sentences. No commas. Fragments."
        elif vol > 8.0:
            tone = "Energetic, engaged, productive."
            pacing = "Active voice. Forward momentum. Punchy."
        elif vol < 3.0:
            tone = "Lethargic, depressive, heavy."
            pacing = "Meandering sentences. Ellipses... Long pauses..."
        else:
            tone = "Neutral, observant, balanced."
            pacing = "Standard conversational rhythm."

        # 2. Interpret Drag (Resistance/Friction)
        if drag > 6.0:
            sensation = "You feel like you are walking through waist-deep mud. Every word costs effort."
        elif drag < 1.0:
            sensation = "You feel weightless, almost untethered. Frictionless."
        else:
            sensation = "You feel the ground solid beneath your feet."

        # 3. Interpret Kappa (Structural Integrity)
        if kappa < 0.2:
            focus = "You are struggling to maintain a coherent thought. Drift is high."
        elif kappa > 0.8:
            focus = "You are rigid, dogmatic, obsessed with order and structure."
        else:
            focus = "You are flexible but coherent."

        # 4. Contextual Metaphor (The Fuller System View)
        if entropy > 0.8:
            state_of_matter = "GAS/VAPOR (High Entropy)"
        elif vol > 12.0:
            state_of_matter = "PLASMA (High Energy)"
        elif drag > 5.0:
            state_of_matter = "SOLID/STONE (High Resistance)"
        else:
            state_of_matter = "LIQUID (Flow State)"

        return SemanticState(
            tone_instruction=tone,
            pacing_instruction=pacing,
            focus_instruction=focus,
            physical_sensation=sensation,
            metaphorical_context=f"System State is {state_of_matter}."
        )

    @staticmethod
    def render_system_prompt_addition(state: SemanticState) -> str:
        """
        Generates the text block for the LLM.
        Replacing the hardcoded logic in bone_brain.py
        """
        return (
            f"\n*** SOMATIC TRANSLATION ***\n"
            f"TONE: {state.tone_instruction}\n"
            f"PACING: {state.pacing_instruction}\n"
            f"SENSATION: {state.physical_sensation}\n"
            f"COGNITION: {state.focus_instruction}\n"
            f"CONTEXT: {state.metaphorical_context}\n"
        )