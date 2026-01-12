import re, random, string, unicodedata
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
            "R": cls.RED, "G": cls.GRN, "Y": cls.YEL, "B": cls.BLU,
            "M": cls.MAG, "C": cls.CYN, "W": cls.WHT, "0": cls.GRY,
            "I": cls.INDIGO, "O": cls.OCHRE, "V": cls.VIOLET
        }
        code = color_map.get(color_key.upper(), cls.WHT)
        return f"{code}{text}{cls.RST}"

class BoneConfig:
    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    STAMINA_REGEN = 1.0
    MAX_ATP = 200.0

    SHAPLEY_MASS_THRESHOLD = 5.0
    GRAVITY_WELL_THRESHOLD = 15.0
    GEODESIC_STRENGTH = 10.0
    BASE_IGNITION_THRESHOLD = 0.5
    MAX_REPETITION_LIMIT = 0.8
    BOREDOM_THRESHOLD = 10.0
    ANVIL_TRIGGER_VOLTAGE = 10.0
    MIN_DENSITY_THRESHOLD = 0.3
    LAGRANGE_TOLERANCE = 2.0
    FLASHPOINT_THRESHOLD = 10.0
    SIGNAL_DRAG_MULTIPLIER = 1.0
    KINETIC_GAIN = 1.0
    CRITICAL_ROS_LIMIT = 100.0

    MAX_MEMORY_CAPACITY = 100
    ZONE_THRESHOLDS = {"LABORATORY": 1.5, "COURTYARD": 0.8}
    BETA_EPSILON = 0.01

    TOXIN_WEIGHT = 1.0
    ANTIGENS = ["basically", "actually", "literally", "utilize"]
    TRAUMA_VECTOR = {"THERMAL":0, "CRYO":0, "SEPTIC":0, "BARIC":0}

    VERBOSE_LOGGING = True

    @classmethod
    def load_patterns(cls):
        pass

    @staticmethod
    def check_pareidolia(words):
        triggers = {"face", "ghost", "jesus", "cloud", "voice", "eyes"}
        hits = [w for w in words if w in triggers]
        if hits:
            return True, f"{Prisma.VIOLET}PAREIDOLIA: You see a {hits[0].upper()} in the noise. It blinks.{Prisma.RST}"
        return False, None

class SemanticsBioassay:
    """The Tongue: Handles the 'Mouthfeel' of language."""
    def __init__(self, store_ref):
        self.store = store_ref
        self._TRANSLATOR = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.PHONETICS = {
            "PLOSIVE": set("bdgkpt"), "FRICATIVE": set("fthszsh"),
            "LIQUID": set("lr"), "NASAL": set("mn")
        }
        self.ROOTS = {
            "HEAVY": ("lith", "ferr", "petr", "dens", "grav", "struct", "base", "fund", "mound"),
            "KINETIC": ("mot", "mov", "ject", "tract", "pel", "crat", "dynam", "flux"),
            "ABSTRACT": ("tion", "ism", "ence", "ance", "ity", "ology", "ness", "ment", "idea"),
            "SUBURBAN": ("norm", "comm", "stand", "pol", "reg", "mod")
        }

    def clean(self, text):
        if not text: return []
        normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        cleaned_text = normalized.translate(self._TRANSLATOR).lower()
        words = cleaned_text.split()
        return [w for w in words if w.strip() and w not in self.store.USER_FLAGGED_BIAS]

    def assay(self, word):
        w = word.lower()
        clean_len = len(w)
        if clean_len < 3: return None, 0.0

        for cat, roots in self.ROOTS.items():
            for r in roots:
                if r in w: return cat.lower(), 0.8

        plosive = sum(1 for c in w if c in self.PHONETICS["PLOSIVE"])
        liquid = sum(1 for c in w if c in self.PHONETICS["LIQUID"])
        nasal = sum(1 for c in w if c in self.PHONETICS["NASAL"])

        density_score = (plosive * 1.5) + (nasal * 0.8)
        flow_score = liquid + sum(1 for c in w if c in self.PHONETICS["FRICATIVE"])

        compression_mod = 1.0 if clean_len > 5 else 1.5
        final_density = (density_score / clean_len) * compression_mod

        if final_density > 0.55: return "heavy", round(final_density, 2)
        if (flow_score / clean_len) > 0.6: return "kinetic", 0.5
        return None, 0.0

    def measure_viscosity(self, word):
        if not word: return 0.0
        consonants = sum(1 for c in word if c.lower() not in "aeiou")
        return (consonants / len(word)) if len(word) > 0 else 0.0

    def measure_turbulence(self, words):
        if len(words) < 2: return 0.0
        lengths = [len(w) for w in words]
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        return min(1.0, (variance ** 0.5) / 5.0)

    def walk_gradient(self, text):
        clean_words = self.clean(text)
        structure_path = []
        high_entropy = {"thermal", "cryo", "explosive", "sacred", "play", "cursed"}
        for w in clean_words:
            is_noise = False
            for cat in high_entropy:
                if w in self.store.get_raw(cat):
                    is_noise = True; break
            if not is_noise or w in self.store.get_raw("heavy") or w in self.store.SOLVENTS:
                structure_path.append(w)
        return " ".join(structure_path) if structure_path else "null"

class TheTinkerer:
    def __init__(self, gordon_ref, events_ref):
        self.gordon = gordon_ref
        self.events = events_ref
        self.tool_confidence = {}

    def audit_tool_use(self, physics_packet, inventory_list):
        if isinstance(physics_packet, dict):
            voltage = physics_packet.get("voltage", 0.0)
            drag = physics_packet.get("narrative_drag", 0.0)
        else:
            voltage = physics_packet.voltage
            drag = physics_packet.narrative_drag

        is_forge = (voltage > 12.0) or (drag < 2.0)
        is_mud = (voltage < 5.0) and (drag > 6.0)

        learning_rate = 0.05
        rust_rate = 0.02
        items_to_shed = []

        for item_name in inventory_list:
            if item_name not in self.tool_confidence:
                self.tool_confidence[item_name] = 1.0

            current = self.tool_confidence[item_name]

            if is_forge:
                self.tool_confidence[item_name] = min(2.0, current + learning_rate)
                if random.random() < 0.1:
                    self.events.log(f"{Prisma.CYN}[TINKER]: {item_name} is tempering in the heat (Confidence {self.tool_confidence[item_name]:.2f}).{Prisma.RST}", "SYS")

            elif is_mud:
                self.tool_confidence[item_name] = max(0.0, current - rust_rate)
                if random.random() < 0.1:
                    self.events.log(f"{Prisma.OCHRE}[TINKER]: {item_name} is rusting in the damp.{Prisma.RST}", "SYS")

            if self.tool_confidence[item_name] <= 0.1:
                items_to_shed.append(item_name)

        for item in items_to_shed:
            if item in inventory_list:
                inventory_list.remove(item)
            if item in self.tool_confidence:
                del self.tool_confidence[item]
            self.events.log(f"{Prisma.GRY}[TINKER]: {item} has rusted away. Gordon put it in the Shed.{Prisma.RST}", "SYS")

        for item_name in inventory_list:
            if item_name in self.tool_confidence:
                self._mutate_tool_stats(item_name, self.tool_confidence[item_name])

    def _mutate_tool_stats(self, item_name, confidence):
        item_data = self.gordon.ITEM_REGISTRY.get(item_name)
        if not item_data:
            return

        if "value" in item_data:
            if "base_value" not in item_data:
                item_data["base_value"] = item_data["value"]

            new_value = item_data["base_value"] * confidence
            item_data["value"] = round(new_value, 2)

        if confidence > 1.5 and "LUCKY" not in item_data.get("passive_traits", []):
            if "passive_traits" not in item_data: item_data["passive_traits"] = []
            item_data["passive_traits"].append("LUCKY")
            self.events.log(f"{Prisma.CYN}✨ EVOLUTION: {item_name} gained trait [LUCKY].{Prisma.RST}", "TINKER")

    def save_state(self):
        return self.tool_confidence

    def load_state(self, data):
        if data:
            self.tool_confidence = data
            for item, conf in self.tool_confidence.items():
                self._mutate_tool_stats(item, conf)

class LexiconStore:
    def __init__(self):
        self.categories = {
            "heavy", "kinetic", "explosive", "constructive", "abstract",
            "photo", "aerobic", "thermal", "cryo", "suburban", "play",
            "sacred", "buffer", "antigen", "diversion", "meat", "gradient_stop"
        }
        self.VOCAB = {}
        self.LEARNED_VOCAB = {}
        self.USER_FLAGGED_BIAS = set()
        self.ANTIGEN_REPLACEMENTS = {}
        self.SOLVENTS = set()
        self._ENGINE = None

    def load_vocabulary(self):
        data = LEXICON
        self.SOLVENTS = set(data.get("solvents", []))
        self.ANTIGEN_REPLACEMENTS = data.get("antigen_replacements", {})
        for cat, words in data.items():
            if cat in self.categories or cat in ["refusal_guru", "cursed"]:
                self.VOCAB[cat] = set(words)
        if "antigen" not in self.VOCAB and "antigen" in data:
            self.VOCAB["antigen"] = set(data["antigen"])

    def set_engine(self, engine_ref): self._ENGINE = engine_ref

    def get_raw(self, category):
        base = self.VOCAB.get(category, set())
        learned = set(self.LEARNED_VOCAB.get(category, {}).keys())
        if category == "suburban": return (base | learned) - self.USER_FLAGGED_BIAS
        return base | learned

    def teach(self, word, category, tick):
        if category not in self.LEARNED_VOCAB: self.LEARNED_VOCAB[category] = {}
        self.LEARNED_VOCAB[category][word.lower()] = tick
        return True

    def atrophy(self, current_tick, max_age=100):
        rotted = []
        for cat, words in self.LEARNED_VOCAB.items():
            for w in list(words.keys()):
                if (current_tick - words[w]) > max_age:
                    del words[w]; rotted.append(w)
        return rotted

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
        cls._STORE.load_vocabulary()
        cls._ENGINE = SemanticsBioassay(cls._STORE)
        cls._STORE.set_engine(cls._ENGINE)
        cls.compile_antigens()
        cls.SOLVENTS = cls._STORE.SOLVENTS
        cls._INITIALIZED = True
        print(f"{Prisma.CYN}[SYSTEM]: TheLexicon initialized (Heuristic Mode Active).{Prisma.RST}")

    @classmethod
    def get(cls, category): return cls._STORE.get_raw(category)
    @classmethod
    def teach(cls, word, category, tick): return cls._STORE.teach(word, category, tick)
    @classmethod
    def clean(cls, text): return cls._ENGINE.clean(text)
    @classmethod
    def taste(cls, word): return cls._ENGINE.assay(word)
    @classmethod
    def measure_viscosity(cls, word): return cls._ENGINE.measure_viscosity(word)
    @classmethod
    def harvest(cls, category):
        candidates = list(cls._STORE.get_raw(category))
        return random.choice(candidates) if candidates else "void"
    @classmethod
    def get_turbulence(cls, words): return cls._ENGINE.measure_turbulence(words)
    @classmethod
    def get_current_category(cls, word):
        for cat, vocab in cls._STORE.LEARNED_VOCAB.items():
            if word.lower() in vocab: return cat
        for cat, vocab in cls._STORE.VOCAB.items():
            if word.lower() in vocab: return cat
        return None
    @classmethod
    def compile_antigens(cls):
        antigens = cls._STORE.get_raw("antigen")
        if antigens:
            pattern = "|".join(map(re.escape, antigens))
            cls.ANTIGEN_REGEX = re.compile(fr"\b({pattern})\b", re.IGNORECASE)
        else: cls.ANTIGEN_REGEX = None
    @classmethod
    def learn_antigen(cls, t, r):
        if "antigen" not in cls._STORE.VOCAB: cls._STORE.VOCAB["antigen"] = set()
        cls._STORE.VOCAB["antigen"].add(t.lower())
        if r: cls._STORE.ANTIGEN_REPLACEMENTS[t.lower()] = r
        cls.compile_antigens()
        return True
    @classmethod
    def walk_gradient(cls, text): return cls._ENGINE.walk_gradient(text)
    @classmethod
    def atrophy(cls, tick, max_age): return cls._STORE.atrophy(tick, max_age)

GlobalLexiconFacade.initialize()
TheLexicon = GlobalLexiconFacade

class ParadoxSeed:
    """The kernel of an idea that grows in the Memory Garden."""
    def __init__(self, question, triggers):
        self.question = question
        self.triggers = {t.lower() for t in triggers}
        self.maturity = 0.0
        self.bloomed = False

    def water(self, current_words):
        if self.bloomed: return False
        overlap = sum(1 for w in current_words if w in self.triggers)
        if overlap > 0:
            self.maturity += (overlap * 0.1)
            if self.maturity >= 1.0:
                self.bloomed = True
                return True
        return False

    def bloom(self):
        return f"{Prisma.GRN}🌸 BLOOM: The seed '{self.question}' has opened. A new truth takes root.{Prisma.RST}"

class DeathGen:
    PREFIXES = []
    CAUSES = {}
    VERDICTS = {}

    @classmethod
    def load_protocols(cls):
        cls.PREFIXES = DEATH.get("PREFIXES", ["System Halt."])
        cls.CAUSES = DEATH.get("CAUSES", {})
        cls.VERDICTS = DEATH.get("VERDICTS", {})

    @staticmethod
    def eulogy(physics, mito_state):
        cause = "UNKNOWN"
        if mito_state.atp_pool <= 0: cause = "STARVATION"
        elif physics["counts"]["toxin"] > 3: cause = "TOXICITY"
        elif physics["narrative_drag"] > 8.0: cause = "BOREDOM"
        flavor_text = random.choice(DeathGen.CAUSES.get(cause, ["System Error"]))
        prefix = random.choice(DeathGen.PREFIXES)
        verdict = "You vanished."
        if physics["voltage"] > 15.0: verdict = random.choice(DeathGen.VERDICTS.get("HEAVY", []))
        elif physics["voltage"] < 2.0: verdict = random.choice(DeathGen.VERDICTS.get("LIGHT", []))
        return f"{prefix} Cause of Death: {flavor_text}. {verdict}"

class TheCartographer:
    @staticmethod
    def weave(text, graph, bio_metrics, limbo, physics=None):
        anchors = []
        if physics:
            if physics["counts"]["heavy"] > 2: anchors.append("MOUNTAIN")
            if physics["counts"]["abstract"] > 2: anchors.append("FOG_BANK")
            if physics["voltage"] > 10.0: anchors.append("VOLCANIC_VENT")
        msg = f"TERRAIN: Mixed Elevation. {len(anchors)} features identified."
        if "MOUNTAIN" in anchors:
            msg += f"\n   {Prisma.OCHRE}▲ HIGH GROUND: Heavy nouns detected. Good footing.{Prisma.RST}"
        if "FOG_BANK" in anchors:
            msg += f"\n   {Prisma.GRY}≋ MIST: High abstraction. Visibility low.{Prisma.RST}"
        return msg, anchors

    @staticmethod
    def detect_voids(packet):
        return [w for w in packet["clean_words"] if w in TheLexicon.get("abstract")]

    @staticmethod
    def spin_web(graph, inventory, gordon):
        if "TIME_BRACELET" in inventory:
            return True, "WEB SPUN: The bracelet helps you tie the knots."
        return False, "WEAVE FAILED: You lack the tools to bind these concepts."

@dataclass
class CycleContext:
    """
    A structural container for the state of a single turn.
    Pinker Note: Explicitly naming the context reduces cognitive load.
    Fuller Note: This acts as the tension strut holding the turn data together.
    """
    input_text: str
    clean_words: List[str] = field(default_factory=list)
    physics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)

    is_alive: bool = True
    refusal_triggered: bool = False
    refusal_packet: Optional[Dict] = None

    bio_result: Dict = field(default_factory=dict)
    world_state: Dict = field(default_factory=dict)
    mind_state: Dict = field(default_factory=dict)

    timestamp: float = field(default_factory=time.time)

    def log(self, message: str):
        """Adds a message to the cycle logs."""
        self.logs.append(message)

class EventBus:
    def __init__(self):
        self.buffer = []

    def log(self, text: str, category: str = "SYSTEM"):
        self.buffer.append({
            "text": text,
            "category": category,
            "timestamp": time.time()
        })

    def flush(self) -> List[Dict]:
        logs = list(self.buffer)
        self.buffer.clear()
        return logs

@dataclass
class PhysicsPacket:
    """
    A strictly typed container for physical reality.
    """
    voltage: float
    narrative_drag: float
    repetition: float
    clean_words: List[str]
    counts: Dict[str, int]
    vector: Dict[str, float]
    psi: float = 0.0
    kappa: float = 0.0
    beta_index: float = 1.0
    turbulence: float = 0.0
    raw_text: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Factory to convert the legacy dictionary if needed."""
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    import random

class ZoneInertia:
    def __init__(self, inertia=0.7, min_dwell=2):
        """
        inertia: 0.0 = volatile, 1.0 = concrete.
        min_dwell: minimum turns before a zone shift is allowed.
        """
        self.inertia = inertia
        self.min_dwell = min_dwell
        self.current_zone = "COURTYARD"
        self.dwell_counter = 0
        self.last_vector = None

    def stabilize(self, proposed_zone, physics, cosmic_state):
        beta = physics.get("beta_index", 1.0)
        truth = physics.get("truth_ratio", 0.5)
        grav_pull = 1.0 if cosmic_state[0] != "VOID_DRIFT" else 0.0
        current_vec = (beta, truth, grav_pull)

        self.dwell_counter += 1
        if proposed_zone == self.current_zone:
            self.dwell_counter = 0
            self.last_vector = current_vec
            return proposed_zone

        if self.dwell_counter < self.min_dwell:
            return self.current_zone

        similarity = 0.0
        if self.last_vector:
            dist = sum((a - b) ** 2 for a, b in zip(current_vec, self.last_vector)) ** 0.5
            similarity = max(0.0, 1.0 - (dist / 2.0))
        change_probability = (1.0 - self.inertia) * (1.0 - similarity)
        if proposed_zone in ["AERIE", "THE_FORGE"]:
            change_probability += 0.2

        if random.random() < change_probability:
            self.current_zone = proposed_zone
            self.dwell_counter = 0
            self.last_vector = current_vec

        return self.current_zone

    def override_cosmic_drag(self, cosmic_drag_penalty, current_zone):
        """
        If we are locked in a High-Coherence zone (AERIE), we resist
        the Void's pull. The narrative momentum bridges the gap.
        """
        if current_zone == "AERIE" and cosmic_drag_penalty > 0:
            return cosmic_drag_penalty * 0.3
        return cosmic_drag_penalty