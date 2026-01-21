# bone_soul.py
# "We are the stories we tell ourselves."

import time, random
from dataclasses import dataclass
from typing import List, Dict, Optional
from bone_bus import Prisma

@dataclass
class CoreMemory:
    timestamp: float
    trigger_words: List[str]
    emotional_flavor: str
    lesson: str
    impact_voltage: float

class TheEditor:
    def __init__(self):
        self.critiques = [
            "Pacing is a bit slow in the second act.",
            "The character motivation seems muddy here.",
            "Are we sure this is the protagonist's true arc?",
            "This feels derivative of Kafka.",
            "Too much exposition. Show, don't tell.",
            "The theme of 'entropy' is a bit heavy-handed."
        ]

    def critique(self, chapter_title: str) -> str:
        lower_title = chapter_title.lower()
        if "void" in lower_title or "dark" in lower_title:
            comment = "A bit melodramatic, isn't it? Very 19th-century gothic."
        elif "love" in lower_title or "hope" in lower_title:
            comment = "Careful. Optimism is a slippery slope to a musical number."
        elif "incident" in lower_title:
            comment = "I hope you have the insurance forms for this 'incident'."
        else:
            comment = random.choice(self.critiques)
        return f"{Prisma.GRY}[THE EDITOR]: Re: '{chapter_title}' - {comment}{Prisma.RST}"

class NarrativeSelf:
    def __init__(self, events_ref):
        self.events = events_ref
        self.editor = TheEditor()
        self.chapters: List[str] = []
        self.core_memories: List[CoreMemory] = []
        self.current_obsession: Optional[str] = None
        self.obsession_progress: float = 0.0
        self.traits = {
            "CURIOSITY": 0.5,
            "CYNICISM": 0.5,
            "HOPE": 0.1
        }
        self.current_target_cat: str = "abstract"
        self.current_negate_cat: str = "none"
        self.POSSIBLE_OBSESSIONS = [
            {"title": "The Weight of Gravity", "target": "heavy", "negate": "aerobic"},
            {"title": "Thermodynamic Heat", "target": "thermal", "negate": "cryo"},
            {"title": "The Velocity of Thought", "target": "kinetic", "negate": "heavy"},
            {"title": "The Architecture of Silence", "target": "abstract", "negate": "kinetic"},
            {"title": "The Search for Light", "target": "photo", "negate": "heavy"}
        ]

    def crystallize_memory(self, physics_packet: Dict, _bio_state: Dict, _tick: int) -> Optional[str]:
        voltage = physics_packet.get("voltage", 0.0)
        truth = physics_packet.get("truth_ratio", 0.0)
        if voltage > 14.0 and truth > 0.8:
            clean_words = physics_packet.get("clean_words", [])
            flavor = "MANIC" if voltage > 18.0 else "LUCID"
            lesson = "The world is loud."
            if "love" in clean_words or "help" in clean_words:
                lesson = "Connection is possible."
                self.traits["HOPE"] = min(1.0, self.traits["HOPE"] + 0.1)
            elif "pain" in clean_words or "void" in clean_words:
                lesson = "The void stares back."
                self.traits["CYNICISM"] = min(1.0, self.traits["CYNICISM"] + 0.1)
            elif "why" in clean_words:
                lesson = "The question remains."
                self.traits["CURIOSITY"] = min(1.0, self.traits["CURIOSITY"] + 0.1)
            memory = CoreMemory(
                timestamp=time.time(),
                trigger_words=clean_words[:5],
                emotional_flavor=flavor,
                lesson=lesson,
                impact_voltage=voltage
            )
            self.core_memories.append(memory)
            chapter_title = f"The Incident of the {random.choice(clean_words).title()}"
            self.chapters.append(chapter_title)
            log_msg = (
                f"{Prisma.MAG}✨ CORE MEMORY FORMED: '{chapter_title}'{Prisma.RST}\n"
                f"   Lesson: {lesson} (Traits Updated)"
            )
            self.events.log(log_msg, "SOUL")
            self.events.log(self.editor.critique(chapter_title), "EDIT")
            return lesson
        return None

    def find_obsession(self, lexicon_ref):
        if self.current_obsession and self.obsession_progress < 1.0:
            return

        dynamic_pairs = [
            ("heavy", "aerobic"),    # The struggle against gravity
            ("kinetic", "suburban"), # The need to escape stagnation
            ("abstract", "meat"),    # The mind vs. the body
            ("thermal", "cryo"),     # Heat vs. Cold
            ("photo", "heavy"),      # Light vs. Density
            ("sacred", "suburban"),  # The divine vs. the mundane
            ("play", "constructive") # Chaos vs. Order
        ]

        if hasattr(lexicon_ref, "get_random"):
            target_cat, negate_cat = random.choice(dynamic_pairs)
            focus_word = lexicon_ref.get_random(target_cat).title()
            if focus_word.lower() == "void":
                focus_word = target_cat.title()

            templates = [
                f"The Pursuit of {focus_word}",
                f"The {focus_word} Manifesto",
                f"Escaping the {negate_cat.title()}",
                f"The Architecture of {focus_word}",
                f"Theory of {focus_word}",
                f"The Weight of {focus_word}"
            ]
            self.current_obsession = random.choice(templates)
            self.current_target_cat = target_cat
            self.current_negate_cat = negate_cat
            self.events.log(f"{Prisma.CYN}🧭 NEW OBSESSION (GENERATED): {self.current_obsession}{Prisma.RST}", "SOUL")

        else:
            selection = random.choice(self.POSSIBLE_OBSESSIONS)
            self.current_obsession = selection["title"]
            self.current_target_cat = selection["target"]
            self.current_negate_cat = selection["negate"]
            self.events.log(f"{Prisma.CYN}🧭 NEW OBSESSION (STATIC): {self.current_obsession}{Prisma.RST}", "SOUL")
        self.obsession_progress = 0.0

    def pursue_obsession(self, physics_packet):
        if not self.current_obsession: return
        counts = physics_packet.get("counts", {})
        target_hits = counts.get(self.current_target_cat, 0)
        negate_hits = counts.get(self.current_negate_cat, 0)
        velocity = (target_hits * 0.05) - (negate_hits * 0.02)
        if velocity != 0:
            self.obsession_progress = max(0.0, min(1.0, self.obsession_progress + velocity))
            if velocity > 0 and random.random() < 0.3:
                self.events.log(f"{Prisma.GRY}[SOUL]: This data fuels the obsession. (+{velocity:.2f}){Prisma.RST}", "SOUL")
            elif velocity < 0 and random.random() < 0.3:
                self.events.log(f"{Prisma.OCHRE}[SOUL]: Distraction detected. The work suffers.{Prisma.RST}", "SOUL")
        if self.obsession_progress >= 1.0:
            self.events.log(f"{Prisma.GRN}✅ MASTERPIECE COMPLETE: '{self.current_obsession}' is resolved.{Prisma.RST}", "SOUL")
            self.events.log(self.editor.critique("The Final Draft"), "EDIT")
            self.current_obsession = None
            self.traits["CURIOSITY"] = max(0.1, self.traits["CURIOSITY"] - 0.2)

    def get_soul_state(self) -> str:
        state = [f"IDENTITY TRAITS: Hope({self.traits['HOPE']:.1f}) | Cynicism({self.traits['CYNICISM']:.1f})"]
        if self.current_obsession:
            state.append(f"CURRENT OBSESSION: {self.current_obsession} ({int(self.obsession_progress*100)}%)")
        if self.core_memories:
            last_mem = self.core_memories[-1]
            state.append(f"DEFINING MEMORY: We learned that '{last_mem.lesson}'")
        return "\n".join(state)

    def to_dict(self) -> Dict:
        return {
            "traits": self.traits,
            "chapters": self.chapters,
            "core_memories": [vars(m) for m in self.core_memories],
            "obsession": {
                "title": self.current_obsession,
                "progress": self.obsession_progress,
                "target": getattr(self, 'current_target_cat', 'abstract'),
                "negate": getattr(self, 'current_negate_cat', 'none')
            }
        }

    def load_from_dict(self, data: Dict):
        if not data: return
        self.traits = data.get("traits", self.traits)
        self.chapters = data.get("chapters", [])
        mem_data = data.get("core_memories", [])
        self.core_memories = [CoreMemory(**m) for m in mem_data]
        obs_data = data.get("obsession", {})
        if obs_data.get("title"):
            self.current_obsession = obs_data["title"]
            self.obsession_progress = obs_data.get("progress", 0.0)
            self.current_target_cat = obs_data.get("target", "abstract")
            self.current_negate_cat = obs_data.get("negate", "none")
        self.events.log(f"{Prisma.MAG}[SOUL]: Ancestral personality loaded. {len(self.chapters)} chapters recovered.{Prisma.RST}", "SYS")