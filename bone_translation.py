""" bone_translation.py
 'The limits of my language mean the limits of my world.' - Wittgenstein """

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from bone_bus import Prisma, BoneConfig

@dataclass
class SomaticState:
    tone: str
    pacing: str
    focus: str
    somatic_sensation: str
    metaphor: str
    internal_monologue_hint: str
    color_code: str = Prisma.GRY

class RosettaStone:
    LIBRARY = {
        "TONE": {
            "LOW": "Hollow, Flat, Depressed",
            "TRANSITION_UP": "Waking, Stirring, Tentative",
            "NEUTRAL": "Balanced, Present, Observant",
            "HIGH": "Electric, Sharp, Urgent",
            "CRITICAL": "Manic, Overwhelming, Screaming",
            "PARANOID": "Defensive, Brittle, Watchful",
            "WARM": "Communal, Soft, Permeable"},
        "SENSATION": {
            "FLOAT": "Weightless, drifting in zero-g",
            "SOLID": "Grounded, tactile, firm",
            "MUD": "Heavy, viscous, wading through tar",
            "MAGMA": "Burning constriction, energy trapped in stone",
            "PLASMA": "Structure dissolving into pure light",
            "STARVATION": "Empty, sputtering, hollowing out"},
        "FOCUS": {
            "DRIFT": "Scattered, dreamlike, associative",
            "COHERENT": "Lucid, integrated, flowing",
            "LOCKED": "Rigid, tunnel-visioned, fixated"
        }
    }

    @staticmethod
    def translate(physics: Dict, bio: Dict, impulse: Any = None) -> SomaticState:
        voltage = physics.get("voltage", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        coherence = physics.get("kappa", 0.5)
        entropy = physics.get("entropy", 0.0)
        chem = bio.get("chemistry", {})
        atp = bio.get("atp", 0.0)
        tone, color = RosettaStone._derive_voltage_tone(voltage)
        focus = RosettaStone._derive_coherence_focus(coherence)
        pacing = "Steady"
        metaphor = "Solid State"
        if impulse and getattr(impulse, 'somatic_reflex', None):
            sensation = impulse.somatic_reflex
        else:
            sensation = RosettaStone._derive_drag_sensation(drag)
        tone = RosettaStone._apply_chemistry(tone, chem)
        if voltage > 12.0 and drag > 5.0:
            sensation = f"{sensation} (Magmatic Pressure)"
            color = Prisma.RED
        elif voltage > 12.0 and entropy > 0.8:
            sensation = f"{sensation} (Ionized Plasma)"
            color = Prisma.MAG
        if atp < 5.0:
            tone = "Desperate"
            sensation = "Hollow, sputtering"
            color = Prisma.GRY
        hint = f"Act {tone.lower()}. Body feels: {sensation.lower()}. Mind is {focus.lower()}."
        return SomaticState(
            tone=tone,
            pacing=pacing,
            focus=focus,
            somatic_sensation=sensation,
            metaphor=metaphor,
            internal_monologue_hint=hint,
            color_code=color)

    @staticmethod
    def _derive_voltage_tone(v: float) -> Tuple[str, str]:
        lib = RosettaStone.LIBRARY["TONE"]
        if v < 2.0: return lib["LOW"], Prisma.GRY
        if v < 6.0: return lib["NEUTRAL"], Prisma.WHT
        if v < 10.0: return lib["TRANSITION_UP"], Prisma.CYN
        if v < 15.0: return lib["HIGH"], Prisma.YEL
        return lib["CRITICAL"], Prisma.RED

    @staticmethod
    def _derive_drag_sensation(d: float) -> str:
        lib = RosettaStone.LIBRARY["SENSATION"]
        if d < 1.0: return lib["FLOAT"]
        if d > 5.0: return lib["MUD"]
        return lib["SOLID"]

    @staticmethod
    def _derive_coherence_focus(k: float) -> str:
        lib = RosettaStone.LIBRARY["FOCUS"]
        if k < 0.3: return lib["DRIFT"]
        if k > 0.8: return lib["LOCKED"]
        return lib["COHERENT"]

    @staticmethod
    def _apply_chemistry(current_tone: str, chem: Dict) -> str:
        cortisol = chem.get("COR", 0.0)
        dopamine = chem.get("DOP", 0.0)
        oxytocin = chem.get("OXY", 0.0)
        adrenaline = chem.get("ADR", 0.0)
        if cortisol > 0.7:
            return f"{RosettaStone.LIBRARY['TONE']['PARANOID']} (Overlaid on {current_tone})"
        if adrenaline > 0.7:
            return f"Heart-Pounding, Adrenalized {current_tone}"
        if oxytocin > 0.7:
            return f"{RosettaStone.LIBRARY['TONE']['WARM']} {current_tone}"
        if dopamine > 0.8:
            return f"Obsessive, Craving, {current_tone}"
        return current_tone

class SomaticInterface:
    def __init__(self, engine_ref):
        self.eng = engine_ref

    def get_current_qualia(self, impulse: Any = None) -> SomaticState:
        physics = self.eng.phys.tension.last_physics_packet if self.eng.phys.tension.last_physics_packet else {}
        if hasattr(physics, "to_dict"): physics = physics.to_dict()
        bio = self.eng.bio.endo.get_state()
        bio["atp"] = self.eng.bio.mito.state.atp_pool
        return RosettaStone.translate(physics, bio, impulse)

    def report(self):
        qualia = self.get_current_qualia()
        print(f"\n{qualia.color_code}--- SOMATIC REPORT ---")
        print(f"TONE: {qualia.tone}")
        print(f"BODY: {qualia.somatic_sensation}")
        print(f"MIND: {qualia.focus}")
        print(f"STATE: {qualia.metaphor}{Prisma.RST}\n")