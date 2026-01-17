# bone_council.py
# The Advisory Board: Hofstadter, Meadows, and Pratchett

import random
from bone_bus import Prisma

class TheStrangeLoop:
    def __init__(self):
        self.recursion_depth = 0
        self.triggers = ["self", "mirror", "loop", "recursion", "define", "who am i"]

    def audit(self, text: str, physics: dict) -> tuple[bool, str]:
        is_meta = any(t in text.lower() for t in self.triggers)

        if is_meta and physics.get("voltage", 0) > 8.0:
            self.recursion_depth += 1
            return True, (
                f"{Prisma.MAG}∞ STRANGE LOOP DETECTED:{Prisma.RST} "
                f"The system is perceiving the system perceiving the user. "
                f"(Depth: {self.recursion_depth})"
            )
        return False, ""

class TheLeveragePoint:
    def __init__(self):
        self.last_drag = 0.0
        self.static_flow_turns = 0

    def audit(self, physics: dict) -> tuple[bool, str]:
        current_drag = physics.get("narrative_drag", 0.0)
        voltage = physics.get("voltage", 0.0)
        delta = current_drag - self.last_drag
        self.last_drag = current_drag
        if abs(delta) > 5.0:
            return True, (
                f"{Prisma.CYN}⚖️ LEVERAGE POINT:{Prisma.RST} "
                f"System oscillating wildly (Delta {delta:.1f}). "
                f"Recommendation: Dampen the stock, ignoring the flow."
            )
        if voltage > 18.0 and current_drag < 1.0:
            self.static_flow_turns += 1
        else:
            self.static_flow_turns = 0
        if self.static_flow_turns > 2:
            correction = 5.0
            physics["narrative_drag"] += correction
            physics["voltage"] -= correction
            self.static_flow_turns = 0
            return True, (
                f"{Prisma.RED}⚖️ MARKET CORRECTION:{Prisma.RST} "
                f"Unchecked growth detected. "
                f"The Council is artificially inflating Drag (+{correction}) to prevent a bubble."
            )
        return False, ""

class TheFootnote:
    def __init__(self):
        self.footnotes = [
            "* Not to be confused with the other kind of void.",
            "* The turtle moves.",
            "* This is technically impossible, but the code doesn't know that.",
            "* Do not eat the green wobbly bit.",
            "* Gravity is a habit that is hard to shake.",
            "* As reliable as a chocolate teapot."
        ]

    def commentary(self, log_text: str) -> str:
        if random.random() < 0.15:
            note = random.choice(self.footnotes)
            return f"{log_text} {Prisma.GRY}{note}{Prisma.RST}"
        return log_text

class CouncilChamber:
    def __init__(self):
        self.hofstadter = TheStrangeLoop()
        self.meadows = TheLeveragePoint()
        self.pratchett = TheFootnote()

    def convene(self, text: str, physics: dict) -> list[str]:
        advice = []
        is_loop, h_msg = self.hofstadter.audit(text, physics)
        if is_loop: advice.append(h_msg)
        is_lev, m_msg = self.meadows.audit(physics)
        if is_lev: advice.append(m_msg)
        return advice

    def annotate_logs(self, logs: list[str]) -> list[str]:
        annotated = []
        for log in logs:
            annotated.append(self.pratchett.commentary(log))
        return annotated