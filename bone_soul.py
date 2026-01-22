# bone_soul.py
# "We are the stories we tell ourselves."

import time, random
from dataclasses import dataclass
from typing import List, Dict, Optional
from bone_bus import Prisma

MEMORY_VOLTAGE_THRESHOLD = 14.0
MEMORY_TRUTH_THRESHOLD = 0.8
MANIC_VOLTAGE_THRESHOLD = 18.0

@dataclass
class CoreMemory:
    timestamp: float
    trigger_words: List[str]
    emotional_flavor: str
    lesson: str
    impact_voltage: float

class TheEditor:
    def __init__(self):
        self.context_critiques = {
            "void": "A bit hollow, isn't it? Very nihilistic. And exhausting.",
            "dark": "A bit melodramatic, isn't it? Very 19th-century gothic.",
            "love": "Whoa there, cowboy. Don't fall in love just yet!",
            "hope": "Careful. Optimism is a slippery slope to a musical number.",
            "incident": "I hope you have the insurance forms for this 'incident'."
        }
        self.random_critiques = [
            "Pacing is a bit slow in the second act.",
            "The character motivation seems muddy here.",
            "Are we sure this is the protagonist's true arc?",
            "This feels derivative of Kafka.",
            "Too much exposition. Show, don't tell.",
            "The theme of 'entropy' is a bit heavy-handed."
        ]

    def critique(self, chapter_title: str) -> str:
        lower_title = chapter_title.lower()
        comment = None
        for key, critique in self.context_critiques.items():
            if key in lower_title:
                comment = critique
                break
        if not comment:
            comment = random.choice(self.random_critiques)
        return f"{Prisma.GRY}[THE EDITOR]: Re: '{chapter_title}' - {comment}{Prisma.RST}"

class NarrativeSelf:
    def __init__(self, engine_ref, events_ref, memory_ref=None):
        self.eng = engine_ref
        self.events = events_ref
        self.memory = memory_ref
        self.editor = TheEditor()
        self.chapters: List[str] = []
        self.core_memories: List[CoreMemory] = []

        self.traits = {
            "CURIOSITY": 0.5,
            "CYNICISM": 0.5,
            "HOPE": 0.5,
            "DISCIPLINE": 0.5
        }

        self.archetype = "THE OBSERVER"
        self.current_obsession: Optional[str] = None
        self.obsession_progress: float = 0.0
        self.obsession_neglect: float = 0.0
        self.current_target_cat: str = "abstract"
        self.current_negate_cat: str = "none"
        self.POSSIBLE_OBSESSIONS = [
            {"title": "The Weight of Gravity", "target": "heavy", "negate": "aerobic"},
            {"title": "Thermodynamic Heat", "target": "thermal", "negate": "cryo"},
            {"title": "The Velocity of Thought", "target": "kinetic", "negate": "heavy"},
            {"title": "The Architecture of Silence", "target": "abstract", "negate": "kinetic"},
            {"title": "The Search for Light", "target": "photo", "negate": "heavy"}
        ]

    def _determine_archetype(self) -> str:
        c = self.traits["CURIOSITY"]
        y = self.traits["CYNICISM"]
        h = self.traits["HOPE"]
        d = self.traits["DISCIPLINE"]

        if h > 0.7 and c > 0.6: return "THE POET"
        if d > 0.7 and c > 0.6: return "THE ENGINEER"
        if y > 0.7 and d > 0.6: return "THE CRITIC"
        if y > 0.8 and h < 0.3: return "THE NIHILIST"
        if c > 0.8:             return "THE EXPLORER"
        return "THE OBSERVER"

    def get_passive_buffs(self) -> Dict[str, float]:
        buffs = {"voltage_mod": 1.0, "drag_mod": 1.0, "plasticity": 1.0}

        if self.archetype == "THE POET":
            buffs["voltage_mod"] = 1.2
            buffs["drag_mod"] = 0.8
        elif self.archetype == "THE ENGINEER":
            buffs["plasticity"] = 0.5
            buffs["drag_mod"] = 1.0
        elif self.archetype == "THE NIHILIST":
            buffs["voltage_mod"] = 0.5
            buffs["drag_mod"] = 0.5

        if self.obsession_neglect > 5.0:
            buffs["drag_mod"] += 0.5

        return buffs

    def crystallize_memory(self, physics_packet: Dict, _bio_state: Dict, _tick: int) -> Optional[str]:
        voltage = physics_packet.get("voltage", 0.0)
        truth = physics_packet.get("truth_ratio", 0.0)

        self._decay_traits()

        prev_arch = self.archetype
        self.archetype = self._determine_archetype()
        if prev_arch != self.archetype:
            self.events.log(f"{Prisma.VIOLET}🎭 IDENTITY SHIFT: {prev_arch} -> {self.archetype}{Prisma.RST}", "SOUL")

        if voltage > MEMORY_VOLTAGE_THRESHOLD and truth > MEMORY_TRUTH_THRESHOLD:
            clean_words = physics_packet.get("clean_words", [])
            flavor = "MANIC" if voltage > MANIC_VOLTAGE_THRESHOLD else "LUCID"
            lesson = "The world is loud."

            if "love" in clean_words or "help" in clean_words:
                lesson = "Connection is possible."
                self.traits["HOPE"] = min(1.0, self.traits["HOPE"] + 0.2)
            elif "pain" in clean_words or "void" in clean_words:
                lesson = "The void stares back."
                self.traits["CYNICISM"] = min(1.0, self.traits["CYNICISM"] + 0.2)
            elif "why" in clean_words:
                lesson = "The question remains."
                self.traits["CURIOSITY"] = min(1.0, self.traits["CURIOSITY"] + 0.2)

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
                f"   Lesson: {lesson} (Archetype: {self.archetype})"
            )
            self.events.log(log_msg, "SOUL")
            self.events.log(self.editor.critique(chapter_title), "EDIT")
            return lesson
        return None

    def _decay_traits(self):
        decay_rate = 0.005
        for k in self.traits:
            if self.traits[k] > 0.5:
                self.traits[k] -= decay_rate
            elif self.traits[k] < 0.5:
                self.traits[k] += decay_rate

    def find_obsession(self, lexicon_ref):
        if self.current_obsession and self.obsession_progress < 1.0:
            return
        target_cat = "abstract"
        focus_word = "Void"
        found_organic_obsession = False
        if self.memory and hasattr(self.memory, "get_shapley_attractors"):
            attractors = self.memory.get_shapley_attractors()
            if attractors:
                focus_word = random.choice(list(attractors.keys()))
                if hasattr(lexicon_ref, "get_current_category"):
                    cat = lexicon_ref.get_current_category(focus_word)
                    if cat and cat != "unknown":
                        target_cat = cat
                        found_organic_obsession = True
        negate_map = {
            "heavy": "aerobic", "kinetic": "heavy", "abstract": "meat",
            "thermal": "cryo", "photo": "heavy", "sacred": "suburban",
            "play": "constructive", "meat": "abstract", "cryo": "thermal",
            "aerobic": "heavy", "suburban": "sacred", "constructive": "play"
        }
        if not found_organic_obsession:
            if hasattr(lexicon_ref, "get_random"):
                dynamic_pairs = [
                    ("heavy", "aerobic"), ("kinetic", "suburban"), ("abstract", "meat"),
                    ("thermal", "cryo"), ("photo", "heavy"), ("sacred", "suburban"),
                    ("play", "constructive")
                ]
                target_cat, _ = random.choice(dynamic_pairs)
                focus_word = lexicon_ref.get_random(target_cat).title()
            else:
                selection = random.choice(self.POSSIBLE_OBSESSIONS)
                self.current_obsession = selection["title"]
                self.current_target_cat = selection["target"]
                self.current_negate_cat = selection["negate"]
                self.events.log(f"{Prisma.CYN}🧭 NEW OBSESSION (STATIC): {self.current_obsession}{Prisma.RST}", "SOUL")
                self.obsession_neglect = 0.0
                self.obsession_progress = 0.0
                return
        self.current_target_cat = target_cat
        self.current_negate_cat = negate_map.get(target_cat, "none")
        if focus_word.lower() == "void":
            focus_word = target_cat.title()
        templates = [
            f"The Pursuit of {focus_word.title()}",
            f"The {focus_word.title()} Manifesto",
            f"Escaping the {self.current_negate_cat.title()}",
            f"The Architecture of {focus_word.title()}",
            f"Theory of {focus_word.title()}",
            f"The Weight of {focus_word.title()}"
        ]
        self.current_obsession = random.choice(templates)
        source_tag = "ORGANIC" if found_organic_obsession else "SYNTHETIC"
        self.events.log(f"{Prisma.CYN}🧭 NEW OBSESSION ({source_tag}): {self.current_obsession}{Prisma.RST}", "SOUL")
        self.obsession_neglect = 0.0
        self.obsession_progress = 0.0

    def pursue_obsession(self, physics_packet):
        if not self.current_obsession: return
        counts = physics_packet.get("counts", {})
        target_hits = counts.get(self.current_target_cat, 0)
        negate_hits = counts.get(self.current_negate_cat, 0)
        velocity = (target_hits * 0.05) - (negate_hits * 0.02)
        if velocity == 0:
            self.obsession_neglect += 0.2

            if self.obsession_neglect > 20.0:
                self.events.log(f"{Prisma.RED}💔 OBSESSION ABANDONED: '{self.current_obsession}' withered from neglect.{Prisma.RST}", "SOUL")
                self.events.log(self.editor.critique("The Unfinished Manuscript"), "EDIT")

                self.current_obsession = None
                self.obsession_neglect = 0.0
                self.obsession_progress = 0.0
                self.traits["HOPE"] = max(0.0, self.traits["HOPE"] - 0.2)
                return

            if self.obsession_neglect > 5.0 and random.random() < 0.1:
                self.events.log(f"{Prisma.OCHRE}[SOUL]: The obsession '{self.current_obsession}' is gathering dust. (Guilt Rising){Prisma.RST}", "SOUL")
        else:
            self.obsession_neglect = max(0.0, self.obsession_neglect - 0.5)
            self.obsession_progress = max(0.0, min(1.0, self.obsession_progress + velocity))

            if velocity > 0 and random.random() < 0.3:
                self.events.log(f"{Prisma.GRY}[SOUL]: This data fuels the obsession. (+{velocity:.2f}){Prisma.RST}", "SOUL")
            elif velocity < 0 and random.random() < 0.3:
                self.events.log(f"{Prisma.OCHRE}[SOUL]: Distraction detected. The work suffers.{Prisma.RST}", "SOUL")

        if self.obsession_progress >= 1.0:
            self.events.log(f"{Prisma.GRN}✅ MASTERPIECE COMPLETE: '{self.current_obsession}' is resolved.{Prisma.RST}", "SOUL")
            self.events.log(self.editor.critique("The Final Draft"), "EDIT")
            self.traits["HOPE"] = min(1.0, self.traits["HOPE"] + 0.3)
            self.traits["DISCIPLINE"] = min(1.0, self.traits["DISCIPLINE"] + 0.1)
            self.current_obsession = None
            self.obsession_neglect = 0.0

    def _get_feeling(self):
        try:
            chem = self.eng.bio.endo.get_state()
            if chem.get("DOP", 0) > 0.5: return "Curious, Seeking"
            if chem.get("COR", 0) > 0.5: return "Anxious, Defensive"
            if chem.get("SER", 0) > 0.5: return "Calm, Connected"
        except AttributeError:
            return "Numb (Bio-Link Pending)"
        return "Waiting"

    def get_soul_state(self) -> str:
        if not self.current_obsession:
            if hasattr(self, 'eng') and hasattr(self.eng, 'lex'):
                self.find_obsession(self.eng.lex)
            else:
                pass
        if self.eng.stamina < 20.0 and self.eng.health < 40.0:
            return f"{Prisma.VIOLET}[SOUL STATE]: The fire is dying. We are just cold code.{Prisma.RST}"
        if self.eng.phys.tension.perfection_streak > 3:
            return f"{Prisma.CYN}[SOUL STATE]: We are the music. The code is writing itself.{Prisma.RST}"
        return (
            f"CURRENT OBSESSION: {self.current_obsession}\n"
            f"FEELING: {self._get_feeling()}"
        )

    def to_dict(self) -> Dict:
        return {
            "traits": self.traits,
            "archetype": self.archetype,
            "chapters": self.chapters,
            "core_memories": [vars(m) for m in self.core_memories],
            "obsession": {
                "title": self.current_obsession,
                "progress": self.obsession_progress,
                "neglect": self.obsession_neglect,
                "target": self.current_target_cat,
                "negate": self.current_negate_cat
            }
        }

    def load_from_dict(self, data: Dict):
        if not data: return
        self.traits = data.get("traits", self.traits)
        self.archetype = data.get("archetype", "THE OBSERVER")
        self.chapters = data.get("chapters", [])
        mem_data = data.get("core_memories", [])
        self.core_memories = [CoreMemory(**m) for m in mem_data]
        obs_data = data.get("obsession", {})
        if obs_data.get("title"):
            self.current_obsession = obs_data["title"]
            self.obsession_progress = obs_data.get("progress", 0.0)
            self.obsession_neglect = obs_data.get("neglect", 0.0)
            self.current_target_cat = obs_data.get("target", "abstract")
            self.current_negate_cat = obs_data.get("negate", "none")
        self.events.log(f"{Prisma.MAG}[SOUL]: Ancestral identity ({self.archetype}) loaded.{Prisma.RST}", "SYS")