# bone_translation.py
# "Translate the math of the spheres into the words of the earth." - SLASH

from dataclasses import dataclass
from typing import Any
from bone_bus import BoneConfig
from bone_data import SOMATIC_LIBRARY

@dataclass
class SemanticState:
    tone_instruction: str
    pacing_instruction: str
    focus_instruction: str
    physical_sensation: str
    metaphorical_context: str

class RosettaStone:
    VOLTAGE_THRESHOLDS = {
        "TRANSITION_UP": 6.0,
        "NEUTRAL": 3.0,
        "TRANSITION_DOWN": 1.5
    }
    KAPPA_THRESHOLDS = {
        "LOCKED": 0.8,
        "DRIFT": 0.2
    }
    CHEM_THRESHOLDS = {
        "COR_DEFENSIVE": 0.7,
        "ADR_URGENT": 0.7,
        "DOP_CRAVING": 0.8,
        "OXY_WARM": 0.7
    }

    @staticmethod
    def _safe_get(obj: Any, keys: list, default: float) -> float:
        if not obj: return default
        is_dict = isinstance(obj, dict)
        for k in keys:
            if is_dict and k in obj:
                return obj[k]
            if not is_dict and hasattr(obj, k):
                return getattr(obj, k)
        return default

    @staticmethod
    def translate(physics: Any, bio: Any) -> SemanticState:
        if physics is None or (isinstance(physics, dict) and not physics):
            return SemanticState(
                tone_instruction=SOMATIC_LIBRARY["TONE"]["VOID"],
                pacing_instruction=SOMATIC_LIBRARY["PACING"]["VOID"],
                focus_instruction=SOMATIC_LIBRARY["FOCUS"]["VOID"],
                physical_sensation=SOMATIC_LIBRARY["SENSATION"]["VOID"],
                metaphorical_context=f"System State is {SOMATIC_LIBRARY['MATTER']['VOID']}."
            )
        vol = RosettaStone._safe_get(physics, ["voltage", "vol"], 0.0)
        drag = RosettaStone._safe_get(physics, ["narrative_drag", "drag"], 0.0)
        kappa = RosettaStone._safe_get(physics, ["kappa", "k"], 0.0)
        entropy = RosettaStone._safe_get(physics, ["E", "entropy"], 0.0)
        chem = {}
        atp = 100.0
        if isinstance(bio, dict):
            chem = bio.get("chem", {})
            atp = bio.get("atp", 100.0)
        elif hasattr(bio, "endo") and hasattr(bio, "mito"):
            chem = bio.endo.get_state()
            atp = bio.mito.state.atp_pool
        if vol >= BoneConfig.PHYSICS.VOLTAGE_CRITICAL:
            tone = SOMATIC_LIBRARY["TONE"]["CRITICAL_HIGH"]
            pacing = SOMATIC_LIBRARY["PACING"]["CRITICAL_HIGH"]
        elif vol >= BoneConfig.PHYSICS.VOLTAGE_MED:
            tone = SOMATIC_LIBRARY["TONE"]["HIGH"]
            pacing = SOMATIC_LIBRARY["PACING"]["HIGH"]
        elif vol >= 6.0:
            tone = SOMATIC_LIBRARY["TONE"]["TRANSITION_UP"]
            pacing = SOMATIC_LIBRARY["PACING"]["NEUTRAL"]
        elif vol >= 3.0:
            tone = SOMATIC_LIBRARY["TONE"]["NEUTRAL"]
            pacing = SOMATIC_LIBRARY["PACING"]["NEUTRAL"]
        elif vol >= 1.5:
            tone = SOMATIC_LIBRARY["TONE"]["TRANSITION_DOWN"]
            pacing = SOMATIC_LIBRARY["PACING"]["LOW"]
        else:
            tone = SOMATIC_LIBRARY["TONE"]["LOW"]
            pacing = SOMATIC_LIBRARY["PACING"]["LOW"]
        if drag > BoneConfig.PHYSICS.DRAG_HEAVY:
            sensation = SOMATIC_LIBRARY["SENSATION"]["MUD"]
        elif drag < BoneConfig.PHYSICS.DRAG_FLOOR:
            sensation = SOMATIC_LIBRARY["SENSATION"]["FLOAT"]
        else:
            sensation = SOMATIC_LIBRARY["SENSATION"]["SOLID"]
        if kappa < 0.2:
            focus = SOMATIC_LIBRARY["FOCUS"]["DRIFT"]
        elif kappa > 0.8:
            focus = SOMATIC_LIBRARY["FOCUS"]["LOCKED"]
        else:
            focus = SOMATIC_LIBRARY["FOCUS"]["COHERENT"]
        cor = chem.get("COR", 0.0)
        if cor > 0.7:
            tone = f"Defensive, paranoid. {tone}"
            focus += " You feel threatened."
        adr = chem.get("ADR", 0.0)
        if adr > 0.7:
            pacing = "Staccato. Breathless. Urgent."
            sensation += " Your heart is hammering against your ribs."
        dop = chem.get("DOP", 0.0)
        if dop > 0.8:
            tone = f"Obsessive, craving. {tone}"
            focus += " You are fixated on the next reward."
        oxy = chem.get("OXY", 0.0)
        if oxy > 0.7:
            tone = f"Warm, communal. {tone}"
            metaphor_suffix = "Connected."
        else:
            metaphor_suffix = ""
        if atp < BoneConfig.BIO.ATP_STARVATION:
            tone = "Desperate, starving, hollow."
            sensation = "You are starving. The engine is sputtering. You need words with nutritional value."
            pacing = "Broken. Gasping."
        is_high_energy = vol >= BoneConfig.PHYSICS.VOLTAGE_HIGH
        is_low_energy = vol <= RosettaStone.VOLTAGE_THRESHOLDS["TRANSITION_DOWN"]
        is_high_drag = drag >= BoneConfig.PHYSICS.DRAG_HEAVY
        is_high_entropy = entropy > 0.8
        if is_high_energy and is_high_drag:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["MAGMA"]
        elif is_high_energy and is_high_entropy:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["PLASMA"]
        elif is_high_drag and is_high_entropy:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["SUBLIMATION"]
        elif is_high_entropy:
            if is_low_energy:
                state_of_matter = "DECAY (Rotting)" # Schur: Spooky!
            else:
                state_of_matter = SOMATIC_LIBRARY["MATTER"]["GAS"]
        elif is_high_drag:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["SOLID"]
        elif is_high_energy:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["ENERGY"]
        else:
            state_of_matter = SOMATIC_LIBRARY["MATTER"]["LIQUID"]
        full_context = f"System State is {state_of_matter}. {metaphor_suffix}"
        return SemanticState(
            tone_instruction=tone,
            pacing_instruction=pacing,
            focus_instruction=focus,
            physical_sensation=sensation,
            metaphorical_context=full_context
        )
    @staticmethod
    def render_system_prompt_addition(state: SemanticState) -> str:
        return (
            f"\n*** SOMATIC TRANSLATION ***\n"
            f"TONE: {state.tone_instruction}\n"
            f"PACING: {state.pacing_instruction}\n"
            f"SENSATION: {state.physical_sensation}\n"
            f"COGNITION: {state.focus_instruction}\n"
            f"CONTEXT: {state.metaphorical_context}\n"
        )