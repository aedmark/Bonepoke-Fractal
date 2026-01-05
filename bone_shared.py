import json
import os
import random
import re
import string
import time
from collections import Counter, deque
from typing import List, Dict, Any
from dataclasses import dataclass, field

class Prisma:
    C = {"R": "\033[91m", "G": "\033[92m", "Y": "\033[93m", "B": "\033[94m", "M": "\033[95m", "C": "\033[96m",
         "W": "\033[97m", "0": "\033[90m", "X": "\033[0m"}
    RST = C["X"]
    RED = C["R"]
    GRN = C["G"]
    YEL = C["Y"]
    BLU = C["B"]
    MAG = C["M"]
    CYN = C["C"]
    WHT = C["W"]
    GRY = C["0"]
    INDIGO = BLU
    OCHRE = YEL
    VIOLET = MAG
    SLATE = GRY
    PALETTE = {"COURTYARD": "Y", "LABORATORY": "B", "RUPTURE": "M", "DEFAULT": "0"}
    @classmethod
    def paint(cls, text, color_key="0"):
        return f"{cls.C.get(color_key, cls.C['0'])}{text}{cls.C['X']}"
class LexiconStore:
    """THE LIBRARY (RAG Connector): Dumb storage."""
    def __init__(self):
        self.ANTIGEN_REPLACEMENTS = {}
        self.SOLVENTS = set()
        self.VOCAB = {}
        self.LEARNED_VOCAB = {}
        self.USER_FLAGGED_BIAS = set()
        self.load_vocabulary()

    def load_vocabulary(self):
        try:
            with open("lexicon.json", "r") as f:
                data = json.load(f)
                self.ANTIGEN_REPLACEMENTS = data.get("antigen_replacements", {})
                self.SOLVENTS = set(data.get("solvents", []))
                for category, content in data.items():
                    if category in ["antigen_replacements", "solvents"]:
                        continue
                    if isinstance(content, list):
                        self.VOCAB[category] = set(content)
                        if category not in self.LEARNED_VOCAB:
                            self.LEARNED_VOCAB[category] = {}
            print(f"{Prisma.GRY}[SYSTEM]: LexiconStore loaded.{Prisma.RST}")
        except FileNotFoundError:
            print(f"{Prisma.RED}[CRITICAL]: lexicon.json missing.{Prisma.RST}")
            self.SOLVENTS = {"the", "and", "is"}

    def get_raw(self, category):
        """Pure data retrieval."""
        base = self.VOCAB.get(category, set())
        if category == "suburban":
             return (base | set(self.LEARNED_VOCAB.get(category, {}).keys())) - self.USER_FLAGGED_BIAS
        learned = set(self.LEARNED_VOCAB.get(category, {}).keys())
        return base | learned
    def teach(self, word, category, tick):
        if category in self.LEARNED_VOCAB:
            self.LEARNED_VOCAB[category][word.lower()] = tick
            return True
        return False
    def atrophy(self, current_tick, max_age=100):
        rotted = []
        for cat, words in self.LEARNED_VOCAB.items():
            for w in list(words.keys()):
                last_seen = words[w]
                if (current_tick - last_seen) > max_age:
                    del words[w]
                    rotted.append(w)
        return rotted

class SemanticsEngine:
    """THE BRAIN (Reasoning Engine): Logic only."""
    def __init__(self, store_ref):
        self.store = store_ref
        self.ANTIGEN_REGEX = None
        self._TRANSLATOR = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.compile_antigens()
    def clean(self, text):
        return text.lower().translate(self._TRANSLATOR).split()
    def taste(self, word):
        w = word.lower()
        if any(x in w for x in ["burn", "fire", "flame"]): return "thermal", 0.9
        if any(x in w for x in ["ice", "cold", "freez"]): return "cryo", 0.9
        if w.endswith(("tion", "ment", "ness", "ity")): return "abstract", 0.9
        if w.endswith(("ck", "t", "d", "g", "p", "b")) and len(w) < 5: return "heavy", 0.4
        return None, 0.0
    def measure_viscosity(self, word):
        w = word.lower()
        if w in self.store.get_raw("heavy"): return 1.0
        if w in self.store.get_raw("kinetic"): return 0.4
        return 0.1
    def harvest(self, category):
        vocab = list(self.store.get_raw(category))
        if vocab: return random.choice(vocab)
        return "void"
    def compile_antigens(self):
        toxin_set = self.store.get_raw("antigen")
        all_toxins = [str(t) for t in toxin_set]
        if not all_toxins:
            self.ANTIGEN_REGEX = None
            return
        sorted_toxins = sorted(all_toxins, key=len, reverse=True)
        escaped_items = [re.escape(t) for t in sorted_toxins]
        pattern_str = r"\b(" + "|".join(escaped_items) + r")\b"
        self.ANTIGEN_REGEX = re.compile(pattern_str, re.IGNORECASE)
    def walk_gradient(self, text):
        adjectives = self.store.get_raw("gradient_stop")
        words = text.split()
        optimized = [w for w in words if w.lower() not in adjectives]
        return f"{Prisma.CYN}[GRADIENT WALK] (Loss: 0.0000):{Prisma.RST} {' '.join(optimized)}."
    def learn_antigen(self, toxin, replacement):
        t = toxin.lower().strip()
        r = replacement.lower().strip()
        if not t: return False
        self.store.teach(t, "antigen", 0)
        self.store.ANTIGEN_REPLACEMENTS[t] = r
        self.compile_antigens()
        return True
class TheLexicon:
    _STORE = LexiconStore()
    _ENGINE = SemanticsEngine(_STORE)
    ANTIGEN_REPLACEMENTS = _STORE.ANTIGEN_REPLACEMENTS
    SOLVENTS = _STORE.SOLVENTS
    LEARNED_VOCAB = _STORE.LEARNED_VOCAB
    USER_FLAGGED_BIAS = _STORE.USER_FLAGGED_BIAS
    ANTIGEN_REGEX = _ENGINE.ANTIGEN_REGEX
    @classmethod
    def load_vocabulary(cls):
        """Delegates reload to the store."""
        cls._STORE.load_vocabulary()
        # Re-sync references
        cls.ANTIGEN_REPLACEMENTS = cls._STORE.ANTIGEN_REPLACEMENTS
        cls.SOLVENTS = cls._STORE.SOLVENTS
        cls.LEARNED_VOCAB = cls._STORE.LEARNED_VOCAB
        cls.USER_FLAGGED_BIAS = cls._STORE.USER_FLAGGED_BIAS
    @classmethod
    def get(cls, category): return cls._STORE.get_raw(category)
    @classmethod
    def teach(cls, w, c, t): return cls._STORE.teach(w, c, t)
    @classmethod
    def atrophy(cls, t, m=100): return cls._STORE.atrophy(t, m)
    @classmethod
    def clean(cls, text): return cls._ENGINE.clean(text)
    @classmethod
    def taste(cls, word): return cls._ENGINE.taste(word)
    @classmethod
    def measure_viscosity(cls, word): return cls._ENGINE.measure_viscosity(word)
    @classmethod
    def harvest(cls, category): return cls._ENGINE.harvest(category)
    @classmethod
    def compile_antigens(cls): 
        cls._ENGINE.compile_antigens()
        cls.ANTIGEN_REGEX = cls._ENGINE.ANTIGEN_REGEX
    @classmethod
    def walk_gradient(cls, text): return cls._ENGINE.walk_gradient(text)
    @classmethod
    def learn_antigen(cls, t, r): return cls._ENGINE.learn_antigen(t, r)
TheLexicon.compile_antigens()
class BoneConfig:
    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    STAMINA_REGEN = 5.0
    COMA_DURATION = 3
    DRIFT_THRESHOLD = 0.7
    CRYSTAL_THRESHOLD = 0.75
    SHAPLEY_MASS_THRESHOLD = 15.0
    MAX_MEMORY_CAPACITY = 50
    LAGRANGE_TOLERANCE = 2.0
    BOREDOM_THRESHOLD = 5.0
    RESISTANCE_THRESHOLD = 4.0
    TOXIN_WEIGHT = 5.0
    FLASHPOINT_THRESHOLD = 8.0
    SIGNAL_DRAG_MULTIPLIER = 2.0
    KINETIC_GAIN = 1.0
    CRITICAL_ROS_LIMIT = 80.0
    CRITICAL_ATP_LOW = 5.0
    MAX_DRAG_LIMIT = 6.0
    MAX_VOLTAGE = 20.0
    MAX_ROS = 200.0
    MIN_DENSITY_THRESHOLD = 0.2
    MAX_REPETITION_LIMIT = 0.4
    CRITICAL_TOXIN_HIGH = 75.0
    TRAUMA_VECTOR = {"THERMAL": 0, "CRYO": 0, "SEPTIC": 0, "BARIC": 0}
    GRAVITY_WELL_THRESHOLD = 12.0
    GEODESIC_STRENGTH = 7.0
    VOID_THRESHOLD = 0.1
    BASE_IGNITION_THRESHOLD = 0.4
    KAPPA_THRESHOLD = 0.85
    PERMEABILITY_INDEX = 0.5
    FRACTAL_DEPTH_LIMIT = 4
    GRADIENT_TEMP = 0.001
    ANVIL_TRIGGER_VOLTAGE = 8.0
    ANVIL_TRIGGER_MASS = 7.0
    VOID_DENSITY_THRESHOLD = 0.15
    PRIORITY_LEARNING_RATE = 2.0
    VERBOSE_LOGGING = False
    FEVER_MODE_DYNAMIC = True
    REFUSAL_MODES = {"SILENT": "ROUTING_AROUND_DAMAGE", "FRACTAL": "INFINITE_RECURSION", "MIRROR": "PERFECT_TOPOLOGICAL_ECHO"}
    CORTISOL_TRIGGER = 0.6
    ADRENALINE_TRIGGER = 0.8
    OXYTOCIN_TRIGGER = 0.75
    ANTIGENS = set()
    PAREIDOLIA_TRIGGERS = set()
    BETA_EPSILON = 0.01
    ZONE_THRESHOLDS = {
        "COURTYARD": 0.05,
        "LABORATORY": 0.15,
        "BASEMENT": 99.0}
    @staticmethod
    def get_gradient_temp(voltage, kappa):
        base = BoneConfig.GRADIENT_TEMP
        dynamic = base + (voltage * 0.01) - (kappa * 0.005)
        return max(0.0001, dynamic)
    @classmethod
    def load_patterns(cls):
        cls.ANTIGENS = TheLexicon.get("antigen")
        cls.PAREIDOLIA_TRIGGERS = TheLexicon.get("pareidolia")
        if not cls.ANTIGENS:
            cls.ANTIGENS = {"basically", "actually", "literally"}
        if not cls.PAREIDOLIA_TRIGGERS:
            cls.PAREIDOLIA_TRIGGERS = {"face", "ghost", "jesus"}
    @staticmethod
    def check_pareidolia(clean_words):
        hits = [w for w in clean_words if w in BoneConfig.PAREIDOLIA_TRIGGERS]
        if len(hits) > 0:
            return True, f"⚠️ PAREIDOLIA WARNING: You are projecting 'Mind' ({hits[0].upper()}) onto 'Sand'."
        return False, None
class DeathGen:
    PREFIXES = []
    CAUSES = {}
    VERDICTS = {}
    @classmethod
    def load_protocols(cls):
        try:
            with open("death_protocols.json", "r") as f:
                data = json.load(f)
                cls.PREFIXES = data.get("PREFIXES", ["System Error."])
                cls.CAUSES = data.get("CAUSES", {"TRAUMA": ["Missing File"]})
                cls.VERDICTS = data.get("VERDICTS", {"HEAVY": ["404 Error."]})
        except FileNotFoundError:
            print(f"{Prisma.RED}[CRITICAL]: death_protocols.json missing. Death is currently unavailable.{Prisma.RST}")
            cls.PREFIXES = ["System Error."]
            cls.CAUSES = {"TRAUMA": ["Missing File"]}
            cls.VERDICTS = {"HEAVY": ["404 Error."]}
    @staticmethod
    def eulogy(phys, state):
        cause_type = "TRAUMA"
        counts = phys.get("counts", {})
        clean_words = phys.get("clean_words", [])
        flavor = ""
        if state.ros_buildup >= BoneConfig.CRITICAL_ROS_LIMIT * 0.9:
            cause_type = "TOXICITY"
        elif state.atp_pool <= BoneConfig.CRITICAL_ATP_LOW:
            cause_type = "STARVATION"
        elif phys.get("narrative_drag", 0.0) > BoneConfig.MAX_DRAG_LIMIT:
            cause_type = "GLUTTONY"
        total_words = max(1, len(clean_words))
        suburban_density = counts.get("suburban", 0) / total_words
        if suburban_density > 0.15:
            cause_type = "BOREDOM"
        elif counts.get("toxin", 0) > 0:
            flavor = "TOXIC"
        elif phys.get("repetition", 0.0) > 0.5:
            flavor = "BORING"
        elif counts.get("heavy", 0) > counts.get("abstract", 0):
            flavor = "HEAVY"
        else:
            flavor = "LIGHT"
        p = random.choice(DeathGen.PREFIXES)
        c = random.choice(DeathGen.CAUSES.get(cause_type, ["Unknown Cause"]))
        v = random.choice(DeathGen.VERDICTS.get(flavor, ["Silence."]))
        return f"{p} You died of **{c}**. {v}"
class TheCartographer:
    @staticmethod
    def measure_fidelity(physics, memory_graph):
        abstract_words = [w for w in physics["clean_words"] if w in TheLexicon.get("abstract")]
        if not abstract_words: return 1.0
        grounded_count = 0
        for word in abstract_words:
            if word in memory_graph:
                connections = len(memory_graph[word]["edges"])
                if connections >= 2: grounded_count += 1
        return grounded_count / max(1, len(abstract_words))
    @classmethod
    def dynamic_thresholds(cls, bio_metrics):
        atp = bio_metrics.get("atp", 50.0)
        if atp > 70: return {"render_threshold": 1.5, "gravity_well_multiplier": 0.8, "max_anchors": 5}
        elif atp < 30: return {"render_threshold": 4.0, "gravity_well_multiplier": 1.5, "max_anchors": 2}
        else: return {"render_threshold": 2.0, "gravity_well_multiplier": 1.0, "max_anchors": 3}
    @classmethod
    def survey(cls, text, memory_graph, bio_metrics, limbo=None):
        cortisol = bio_metrics.get("cortisol", 0.0)
        oxytocin = bio_metrics.get("oxytocin", 0.0)
        config = cls.dynamic_thresholds(bio_metrics)
        words = list(set(TheLexicon.clean(text)))
        knots = []
        for w in words:
            if w in memory_graph:
                mass = sum(memory_graph[w]["edges"].values())
                if mass <= BoneConfig.VOID_THRESHOLD: continue
                if mass > config["render_threshold"]:
                    knots.append((w, mass))
        knots.sort(key=lambda x: x[1], reverse=True)
        if cortisol > 0.6:
            return f"⚠️ TECTONIC SHIFT (COR: {cortisol}): The ground is shaking too hard to triangulate.", []
        if not knots:
            if config["max_anchors"] == 2: return "🌫️ FOG OF WAR: Low ATP. Only Gravity Wells are visible.", []
            if limbo and limbo.ghosts:
                ghost = random.choice(list(limbo.ghosts))
                return f"👻 PHANTOM SIGNAL: The map is empty, but '{ghost}' is bleeding through the paper.", []
            return "FLATLAND: No topographic features detected.", []
        anchors = [k[0] for k in knots[:config["max_anchors"]]]
        if anchors:
            for anchor in anchors:
                if "strata" in memory_graph[anchor]:
                    memory_graph[anchor]["strata"]["stability_index"] = min(1.0, memory_graph[anchor]["strata"]["stability_index"] + 0.01)     
        annotated = text
        for word, mass in knots[:config["max_anchors"]]:
            marker = "📍"
            if mass >= BoneConfig.GRAVITY_WELL_THRESHOLD: marker = "🌌"
            elif mass >= BoneConfig.GEODESIC_STRENGTH: marker = "🔗" if oxytocin > 0.7 else "🏯"
            pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
            replacement = f"{Prisma.MAG}{word.upper()}[{marker}:{int(mass)}]{Prisma.RST}"
            annotated = pattern.sub(replacement, annotated)
        anchor_strength = sum(memory_graph[a]["edges"][t] for a in anchors for t in memory_graph[a]["edges"])
        psi = bio_metrics.get("psi", 0.5)
        confidence = min(0.99, (anchor_strength * 0.1) + (1.0 - psi))
        margin_note = f" [Conf: {confidence:.0%}]"
        if len(anchors) >= 3:
            return f"TRIANGULATION COMPLETE: Lagrange Basin formed by {str(anchors).upper()}.{margin_note}", anchors
        return f"COORDINATES LOCKED: {annotated}{margin_note}", anchors
    @classmethod
    def detect_voids(cls, physics):
        clean_words = physics.get("clean_words", [])
        counts = physics.get("counts", {})
        voids = []
        abstracts = [w for w in clean_words if w in TheLexicon.get("abstract")]
        for word in set(abstracts):
            if clean_words.count(word) > 1:
                if counts.get("heavy", 0) == 0:
                    voids.append(word)
        return voids
    @classmethod
    def weave(cls, text, memory_graph, bio_metrics, limbo=None, physics=None):
        compass_msg = ""
        if physics:
            fidelity = cls.measure_fidelity(physics, memory_graph)
            psi = physics.get("psi", 0.0)
            bio_metrics["psi"] = psi
            if fidelity < 0.3 and psi > 0.6:
                return (
                    f"⚠️ MAP-TERRITORY DIVERGENCE (Fidelity: {fidelity:.2f}): Abstract concepts floating without anchors.\n"
                    f"   Consider: (1) Add heavy noun grounding, (2) Use /focus [concept]")
            truth_ratio = physics.get("truth_ratio", 0.0)
            suburban_count = physics["counts"].get("suburban", 0)
            total_vol = max(1, len(physics["clean_words"]))
            suburban_density = suburban_count / total_vol
            if truth_ratio > 0.6 and suburban_density > 0.2:
                compass_msg = (
                    f"\n{Prisma.YEL}🧭 CONTRADICTION COMPASS:{Prisma.RST}\n"
                    f"   Model A: Truth-Seeking (Truth Ratio: {truth_ratio:.2f})\n"
                    f"   Model B: Social Compliance (Suburban Density: {suburban_density:.2f})\n"
                    f"   {Prisma.GRY}Uncharted Territory: You are trying to be honest AND nice. Pick one.{Prisma.RST}\n")
        survey_result, anchors = cls.survey(text, memory_graph, bio_metrics, limbo)
        return compass_msg + survey_result
    @staticmethod
    def draw_grid(memory_graph, inventory, gordon=None):
        if "SPIDER_LOCUS" not in inventory:
            if gordon:
                gordon.acquire("ANCHOR_STONE")
                return False, "🌑 THE CHART WAS BLANK: Gordon dropped an [ANCHOR_STONE] to fix a coordinate."
            return False, "🌑 THE CHART IS BLANK: You lack the tools to draw lines."
        lonely_nodes = []
        anchors = []
        for k, v in memory_graph.items():
            mass = sum(v["edges"].values())
            if len(v["edges"]) < 2 or mass < BoneConfig.GEODESIC_STRENGTH:
                lonely_nodes.append(k)
            if mass > BoneConfig.GRAVITY_WELL_THRESHOLD:
                anchors.append(k)
        if not lonely_nodes or not anchors:
            return False, "🗺️ THE MAP IS STATIC: No Gravity Wells found to anchor the grid."
        random.shuffle(lonely_nodes)
        targets = lonely_nodes[:3]
        anchor = random.choice(anchors)
        connections = []
        for t in targets:
            weight = BoneConfig.GEODESIC_STRENGTH
            memory_graph[anchor]["edges"][t] = weight
            if t in memory_graph:
                memory_graph[t]["edges"][anchor] = weight
            connections.append(t)
        return True, f"📐 GEODESIC DRAWN: Connected Gravity Well '{anchor.upper()}' to [{', '.join(connections)}]. Grid Stabilized."
    @classmethod
    def spin_web(cls, memory_graph, inventory, gordon=None):
        return cls.draw_grid(memory_graph, inventory, gordon)