# bone_shared.py

import random
import re
import string
import unicodedata
from bone_data import LEXICON, DEATH
    
class Prisma:
    RST = "\033[0m"
    RED = "\033[31m"
    GRN = "\033[32m"
    YEL = "\033[33m"
    BLU = "\033[34m"
    MAG = "\033[35m"
    CYN = "\033[36m"
    WHT = "\033[97m"
    GRY = "\033[90m"
    INDIGO = "\033[34;1m"
    OCHRE = "\033[33;2m"
    VIOLET = "\033[35;2m"
    SLATE = "\033[30;1m"

    @classmethod
    def paint(cls, text, color_key="0"):
        color_map = {
            "R": cls.RED,
            "G": cls.GRN,
            "Y": cls.YEL,
            "B": cls.BLU,
            "M": cls.MAG,
            "C": cls.CYN,
            "W": cls.WHT,
            "0": cls.GRY,
            "I": cls.INDIGO,
            "O": cls.OCHRE,
            "V": cls.VIOLET}
        code = color_map.get(color_key.upper(), cls.WHT)
        return f"{code}{text}{cls.RST}"

class SemanticsBioassay:
    _ENGINE = None

    def __init__(self, store_ref):
        self.store = store_ref
        self._TRANSLATOR = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.ANTIGEN_REGEX = None

        self.PHONETICS = {
            "PLOSIVE": set("bdgkpt"),
            "FRICATIVE": set("fthszsh"),
            "LIQUID": set("lr"),
            "NASAL": set("mn")}
        self.ROOTS = {
            "HEAVY": ("lith", "ferr", "petr", "dens", "grav", "struct", "base", "fund"),
            "KINETIC": ("mot", "mov", "ject", "tract", "pel", "crat", "dynam"),
            "ABSTRACT": ("tion", "ism", "ence", "ance", "ity", "ology", "ness", "ment", "idea")}
        self.HIGH_ENTROPY_CATS = {"thermal", "cryo", "explosive", "sacred", "play", "cursed"}
        self.compile_antigens()

    def compile_antigens(self):
        antigens = self.store.VOCAB.get("antigen", set())
        if antigens:
            pattern = "|".join(map(re.escape, antigens))
            self.ANTIGEN_REGEX = re.compile(fr"\b({pattern})\b", re.IGNORECASE)
        else:
            self.ANTIGEN_REGEX = None

    def clean(self, text):
        normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        cleaned_text = normalized.translate(self._TRANSLATOR).lower()
        words = cleaned_text.split()
        filtered_words = [
            w for w in words
            if w.strip() and w not in self.store.USER_FLAGGED_BIAS]
        return filtered_words

    def walk_gradient(self, text):
        clean_words = self.clean(text)
        structure_path = []
        for w in clean_words:
            is_noise = False
            for cat in self.HIGH_ENTROPY_CATS:
                if w in self.store.get_raw(cat):
                    is_noise = True
                    break
            if not is_noise or w in self.store.get_raw("heavy") or w in self.store.SOLVENTS:
                structure_path.append(w)
        if not structure_path:
            return "null"
        return " ".join(structure_path)

    def assay(self, word):
        w = word.lower()
        clean_len = len(w)
        if clean_len < 2: return None, 0.0
        plosive = sum(1 for c in w if c in self.PHONETICS["PLOSIVE"])
        fricative = sum(1 for c in w if c in self.PHONETICS["FRICATIVE"])
        liquid = sum(1 for c in w if c in self.PHONETICS["LIQUID"])
        nasal = sum(1 for c in w if c in self.PHONETICS["NASAL"])
        density = (plosive * 1.5) + (nasal * 0.8)
        flow = liquid + fricative
        compression_mod = 1.0 if clean_len > 5 else 1.5
        final_density = (density / clean_len) * compression_mod
        if final_density > 0.55:
            return "heavy", round(final_density, 2)
        if (flow / clean_len) > 0.6:
            return "kinetic", 0.5
        cat, conf = self._analyze_morphology(w)
        if cat: return cat, conf
        return None, 0.0

    def _analyze_morphology(self, word):
        for cat, roots in self.ROOTS.items():
            for r in roots:
                if r in word:
                    return cat.lower(), 0.7
        return None, 0.0

    @staticmethod
    def measure_viscosity(word):
        if not word: return 0.0
        consonants = sum(1 for c in word if c.lower() not in "aeiou")
        return (consonants / len(word)) if len(word) > 0 else 0.0

    @staticmethod
    def measure_turbulence(words):
        if len(words) < 2: return 0.0
        lengths = [len(w) for w in words]
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        return min(1.0, (variance ** 0.5) / 5.0)

    def harvest(self, category):
        candidates = list(self.store.get_raw(category))
        return random.choice(candidates) if candidates else "void"

    def learn_antigen(self, toxin, replacement):
        if "antigen" not in self.store.VOCAB:
            self.store.VOCAB["antigen"] = set()
        self.store.VOCAB["antigen"].add(toxin.lower())
        if replacement:
            self.store.ANTIGEN_REPLACEMENTS[toxin.lower()] = replacement
        return True

class LexiconStore:
    def __init__(self):
        self.categories = {"heavy", "kinetic", "explosive", "constructive", "abstract", "photo", "aerobic", "thermal",
                           "cryo", "suburban", "play", "sacred", "buffer", "antigen"}
        self.VOCAB = {}
        self.LEARNED_VOCAB = {}
        self.USER_FLAGGED_BIAS = set()
        self.SOLVENTS = set(LEXICON.get("solvents", []))
        self.ANTIGEN_REPLACEMENTS = LEXICON.get("antigen_replacements", {})
        self.ANTIGEN_REGEX = None
        self._ENGINE = None
        self.load_vocabulary()

    def set_engine(self, engine_ref):
        self._ENGINE = engine_ref

    def load_vocabulary(self):
        data = LEXICON
        for cat, words in data.items():
            if cat in self.categories:
                self.VOCAB[cat] = set(words)
            elif cat == "refusal_guru":
                self.VOCAB["refusal_guru"] = set(words)
            elif cat == "cursed":
                self.VOCAB["cursed"] = set(words)
        antigens = data.get("antigen", [])
        if antigens:
            pattern = "|".join(map(re.escape, antigens))
            self.ANTIGEN_REGEX = re.compile(fr"\b({pattern})\b", re.IGNORECASE)
        print(f"{Prisma.GRY}[SYSTEM]: LexiconStore loaded from Data Module.{Prisma.RST}")

    def get_raw(self, category):
        base = self.VOCAB.get(category, set())
        if category == "suburban":
            return (base | set(self.LEARNED_VOCAB.get(category, {}).keys())) - self.USER_FLAGGED_BIAS
        learned = set(self.LEARNED_VOCAB.get(category, {}).keys())
        return base | learned

    def teach(self, word, category, tick):
        if category not in self.LEARNED_VOCAB:
            self.LEARNED_VOCAB[category] = {}
        self.LEARNED_VOCAB[category][word.lower()] = tick
        return True

    def atrophy(self, current_tick, max_age=100):
        rotted = []
        for cat, words in self.LEARNED_VOCAB.items():
            for w in list(words.keys()):
                last_seen = words[w]
                if (current_tick - last_seen) > max_age:
                    del words[w]
                    rotted.append(w)
        return rotted

    def clean(self, text):
        return self._ENGINE.clean(text)

    def taste(self, word):
        return self._ENGINE.assay(word)

    def measure_viscosity(self, word):
        return self._ENGINE.measure_viscosity(word)

    def harvest(self, category):
        return self._ENGINE.harvest(category)

    def get_current_category(self, word):
        for cat, vocab in self.LEARNED_VOCAB.items():
            if word.lower() in vocab: return cat
        for cat, vocab in self.VOCAB.items():
            if word.lower() in vocab: return cat
        return None

    def compile_antigens(self):
        if self._ENGINE:
            self._ENGINE.compile_antigens()
            self.ANTIGEN_REGEX = self._ENGINE.ANTIGEN_REGEX

    def learn_antigen(self, t, r):
        if not self._ENGINE: return False
        success = self._ENGINE.learn_antigen(t, r)
        if success:
            self.compile_antigens()
        return success

    def walk_gradient(self, text):
        return self._ENGINE.walk_gradient(text)

    def get_turbulence(self, words):
        return self._ENGINE.measure_turbulence(words)

class BoneConfig:
    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    STAMINA_REGEN = 5.0
    COMA_DURATION = 3
    DRIFT_THRESHOLD = 0.7
    SHAPLEY_MASS_THRESHOLD = 15.0
    MAX_MEMORY_CAPACITY = 50
    LAGRANGE_TOLERANCE = 2.0
    BOREDOM_THRESHOLD = 5.0
    RESISTANCE_THRESHOLD = 4.0
    TOXIN_WEIGHT = 5.0
    FLASHPOINT_THRESHOLD = 8.0
    SIGNAL_DRAG_MULTIPLIER = 4.0
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
    FRACTAL_DEPTH_LIMIT = 4
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
            return True, f"PAREIDOLIA WARNING: You are projecting 'Mind' ({hits[0].upper()}) onto 'Sand'."
        return False, None

class DeathGen:
    @classmethod
    def load_protocols(cls):
        print(f"{Prisma.GRY}[SYSTEM]: DeathGen protocols loaded.{Prisma.RST}")

    @staticmethod
    def eulogy(phys, state):
        prefixes = DEATH.get("PREFIXES", ["System Halt."])
        causes = DEATH.get("CAUSES", {})
        verdicts = DEATH.get("VERDICTS", {})
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
        p = random.choice(prefixes)
        c = random.choice(causes.get(cause_type, ["Unknown Cause"]))
        v = random.choice(verdicts.get(flavor, ["Silence."]))
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
        high_energy = 70.0
        low_energy = BoneConfig.CRITICAL_ATP_LOW * 6.0
        if atp > high_energy:
            return {"render_threshold": 1.5, "gravity_well_multiplier": 0.8, "max_anchors": 5}
        elif atp < low_energy:
            return {"render_threshold": 4.0, "gravity_well_multiplier": 1.5, "max_anchors": 2}
        else:
            return {"render_threshold": 2.0, "gravity_well_multiplier": 1.0, "max_anchors": 3}

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
                if mass <= 0.1: continue
                if mass > config["render_threshold"]:
                    knots.append((w, mass))
        knots.sort(key=lambda x: x[1], reverse=True)
        if cortisol > 0.8:
            return f"TECTONIC SHIFT (COR: {cortisol:.2f}): The ground is shaking too hard to triangulate.", []
        if not knots:
            if config["max_anchors"] == 2:
                return "FOG OF WAR: Low ATP. The map is blurry.", []
            if limbo and limbo.ghosts:
                ghost = random.choice(list(limbo.ghosts))
                return f"PHANTOM SIGNAL: The map is empty, but '{ghost}' is bleeding through the paper.", []
            return "FLATLAND: No topographic features detected. (Try using heavier words).", []
        anchors = [k[0] for k in knots[:config["max_anchors"]]]
        if anchors:
            for anchor in anchors:
                if "strata" in memory_graph[anchor]:
                    memory_graph[anchor]["strata"]["stability_index"] = min(1.0, memory_graph[anchor]["strata"]["stability_index"] + 0.02)
        annotated = text
        for word, mass in knots[:config["max_anchors"]]:
            marker = "B"
            if mass >= BoneConfig.GRAVITY_WELL_THRESHOLD: marker = "Y"
            elif mass >= BoneConfig.GEODESIC_STRENGTH: marker = "C" if oxytocin > 0.7 else "R"
            pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
            replacement = f"{Prisma.MAG}{word.upper()}[{marker}:{int(mass)}]{Prisma.RST}"
            annotated = pattern.sub(replacement, annotated)
        anchor_strength = sum(memory_graph[a]["edges"].get(t, 0) for a in anchors for t in memory_graph[a]["edges"])
        psi = bio_metrics.get("psi", 0.5)
        confidence = min(0.99, (anchor_strength * 0.05) + (1.0 - psi))
        margin_note = f" [Conf: {confidence:.0%}]"
        if len(anchors) >= 3:
            return f"TRIANGULATION COMPLETE: Lagrange Basin formed by {str(anchors).upper()}.{margin_note}\n   > {annotated}", anchors
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
                    f"MAP-TERRITORY DIVERGENCE (Fidelity: {fidelity:.2f}): Abstract concepts floating without anchors.\n"
                    f"   Consider: (1) Add heavy noun grounding, (2) Use /focus [concept]")
            truth_ratio = physics.get("truth_ratio", 0.0)
            suburban_count = physics["counts"].get("suburban", 0)
            total_vol = max(1, len(physics["clean_words"]))
            suburban_density = suburban_count / total_vol
            if truth_ratio > 0.6 and suburban_density > 0.2:
                compass_msg = (
                    f"\n{Prisma.YEL}CONTRADICTION COMPASS:{Prisma.RST}\n"
                    f"   Model A: Truth-Seeking (Truth Ratio: {truth_ratio:.2f})\n"
                    f"   Model B: Social Compliance (Suburban Density: {suburban_density:.2f})\n"
                    f"   {Prisma.GRY}Uncharted Territory: You are trying to be honest AND nice. Pick one.{Prisma.RST}\n")
        survey_result, anchors = cls.survey(text, memory_graph, bio_metrics, limbo)
        return (compass_msg + survey_result), anchors

    @staticmethod
    def draw_grid(memory_graph, inventory, gordon=None):
        has_tool = "SPIDER_LOCUS" in inventory
        used_anchor = False
        if not has_tool:
            if gordon and "ANCHOR_STONE" in gordon.inventory:
                gordon.inventory.remove("ANCHOR_STONE")
                used_anchor = True
            else:
                return False, "THE CHART IS BLANK: You need a [SPIDER_LOCUS] or an [ANCHOR_STONE] to draw lines."
        lonely_nodes = []
        anchors = []
        for k, v in memory_graph.items():
            mass = sum(v["edges"].values())
            if len(v["edges"]) < 2 or mass < BoneConfig.GEODESIC_STRENGTH:
                lonely_nodes.append(k)
            if mass > BoneConfig.GRAVITY_WELL_THRESHOLD:
                anchors.append(k)
        if not lonely_nodes:
            return False, "THE MAP IS ALREADY DENSE: No lonely nodes to connect."
        if not anchors:
            return False, "THE MAP IS FLUID: No Gravity Wells found to anchor the grid."
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
        if used_anchor:
            return True, f"GORDON'S GAMBIT: He threw an ANCHOR_STONE at '{anchor.upper()}'. It dragged [{', '.join(connections).upper()}] into alignment."
        return True, f"SPIDER LOCUS: Triangulated '{anchor.upper()}' against [{', '.join(connections).upper()}]. The web tightens."

    @classmethod
    def spin_web(cls, memory_graph, inventory, gordon=None):
        return cls.draw_grid(memory_graph, inventory, gordon)

class ParadoxSeed:
    def __init__(self, question, trigger_concepts):
        self.question = question
        self.triggers = trigger_concepts
        self.maturity = 0.0
        self.bloomed = False

    def water(self, words, amount=1.0):
        if self.bloomed:
            return False
        intersection = set(words) & self.triggers
        if intersection:
            self.maturity += amount * len(intersection)
        self.maturity += 0.05
        return self.maturity >= 10.0

    def bloom(self):
        self.bloomed = True
        return f"THE SEED BLOOMS: '{self.question}'"

class GlobalLexiconFacade:
    _INITIALIZED = False
    _STORE = None
    _ENGINE = None
    ANTIGEN_REGEX = None
    SOLVENTS = set()

    @classmethod
    def initialize(cls):
        if cls._INITIALIZED: return
        cls._STORE = LexiconStore()
        cls._ENGINE = SemanticsBioassay(cls._STORE)
        cls._STORE.set_engine(cls._ENGINE)
        cls.compile_antigens()
        cls._INITIALIZED = True
        cls.SOLVENTS = cls._STORE.SOLVENTS
        print(f"{Prisma.CYN}[SYSTEM]: TheLexicon initialized via SLASH Protocols.{Prisma.RST}")

    @classmethod
    def get(cls, category):
        return cls._STORE.get_raw(category)

    @classmethod
    def teach(cls, word, category, tick):
        return cls._STORE.teach(word, category, tick)

    @classmethod
    def clean(cls, text):
        return cls._ENGINE.clean(text)

    @classmethod
    def taste(cls, word):
        return cls._ENGINE.assay(word)

    @classmethod
    def measure_viscosity(cls, word):
        return cls._ENGINE.measure_viscosity(word)

    @classmethod
    def harvest(cls, category):
        return cls._ENGINE.harvest(category)

    @classmethod
    def get_turbulence(cls, words):
        return cls._ENGINE.measure_turbulence(words)

    @classmethod
    def get_current_category(cls, word):
        for cat, vocab in cls._STORE.LEARNED_VOCAB.items():
            if word.lower() in vocab: return cat
        for cat, vocab in cls._STORE.VOCAB.items():
            if word.lower() in vocab: return cat
        return None

    @classmethod
    def compile_antigens(cls):
        cls._ENGINE.compile_antigens()
        cls.ANTIGEN_REGEX = cls._ENGINE.ANTIGEN_REGEX

    @classmethod
    def learn_antigen(cls, t, r):
        success = cls._ENGINE.learn_antigen(t, r)
        if success:
            cls.compile_antigens()
        return success

    @classmethod
    def atrophy(cls, tick, max_age):
        return cls._STORE.atrophy(tick, max_age)

GlobalLexiconFacade.initialize()
TheLexicon = GlobalLexiconFacade
