# bone_village.py - "It takes a village..."

import json, os, random, re, time, string, unicodedata, math
from collections import Counter, deque
from typing import List, Dict, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from bone_personality import UserProfile

# --- DATA IMPORTS ---
# We use a try/except block here to allow the file to run even if bone_data isn't present yet,
# preventing immediate crashes during testing.
try:
    from bone_data import LEXICON, GENETICS, DEATH, NARRATIVE_DATA, RESONANCE
except ImportError:
    # Fallback empty data if bone_data.py is missing
    LEXICON = {"solvents": ["the", "is"]}
    GENETICS = {}
    DEATH = {}
    NARRATIVE_DATA = {}
    RESONANCE = {}

# --- VISUALS ---

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

# --- CONFIGURATION ---

# bone_village.py (Partial Update)

class BoneConfig:
    # --- CORE VITALS ---
    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    MAX_ATP = 200.0
    BASE_METABOLIC_RATE = 2.0
    
    # --- PHYSICS CONSTANTS ---
    class PHYSICS:
        # Voltage Thresholds (The "Energy" of the text)
        VOLTAGE_FLOOR = 2.0        # System is effectively dead/stagnant
        VOLTAGE_LOW = 5.0          # Mud/Rust territory
        VOLTAGE_MED = 8.0          # Active processing
        VOLTAGE_HIGH = 12.0        # The Forge / High Energy
        VOLTAGE_CRITICAL = 15.0    # Dangerous / Manic
        VOLTAGE_MAX = 20.0         # System Cap

        # Narrative Drag (The "Friction" of the text)
        DRAG_FLOOR = 1.0           # Frictionless / Slippery
        DRAG_IDEAL_MAX = 3.0       # Good resistance
        DRAG_HEAVY = 5.0           # Sluggish
        DRAG_CRITICAL = 8.0        # Stuck in the Mud
        DRAG_HALT = 10.0           # Absolute stoppage

        # Vector Weights (VSL Matrix)
        WEIGHT_HEAVY = 2.0
        WEIGHT_KINETIC = 1.5
        WEIGHT_EXPLOSIVE = 3.0
        WEIGHT_CONSTRUCTIVE = 1.5

        # Integrity
        SHAPLEY_MASS_THRESHOLD = 5.0
        GRAVITY_WELL_THRESHOLD = 15.0
        
    # --- BIOLOGICAL CONSTANTS ---
    class BIO:
        # Thresholds
        ATP_STARVATION = 10.0
        ROS_CRITICAL = 100.0
        STAMINA_EXHAUSTED = 20.0
        
        # Taxes & Costs
        COST_TURBULENCE = 5.0
        TAX_DRAG_BASE = 0.2
        GAIN_PHOTOSYNTHESIS = 2.0
        
        # Endocrine Rewards
        REWARD_SMALL = 0.05
        REWARD_MEDIUM = 0.10
        REWARD_LARGE = 0.15
        DECAY_RATE = 0.01

    # --- PROBABILITIES ---
    class CHANCE:
        RARE = 0.05
        UNCOMMON = 0.10
        COMMON = 0.20
        FREQUENT = 0.30
        
    # --- LEGACY / MISC ---
    # Kept for backward compatibility with older logic, but mapped to new structure where possible
    STAMINA_REGEN = 1.0
    MAX_DRAG_LIMIT = PHYSICS.DRAG_HEAVY
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
    CRITICAL_ROS_LIMIT = BIO.ROS_CRITICAL
    MAX_MEMORY_CAPACITY = 100
    ZONE_THRESHOLDS = {"LABORATORY": 1.5, "COURTYARD": 0.8}
    TOXIN_WEIGHT = 1.0
    ANTIGENS = ["basically", "actually", "literally", "utilize"]
    VERBOSE_LOGGING = True

    @staticmethod
    def check_pareidolia(words):
        # Implementation remains the same
        triggers = {"face", "ghost", "jesus", "cloud", "voice", "eyes"}
        hits = [w for w in words if w in triggers]
        if hits:
            return True, f"{Prisma.VIOLET}PAREIDOLIA: You see a {hits[0].upper()} in the noise. It blinks.{Prisma.RST}"
        return False, None

# --- LEXICON LOGIC ---

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

class SemanticsBioassay:
    def __init__(self, store_ref):
        self.store = store_ref
        self._TRANSLATOR = str.maketrans(string.punctuation, " " * len(string.punctuation))
        self.PHONETICS = {
            "PLOSIVE": set("bdgkpt"), "FRICATIVE": set("fthszsh"),
            "LIQUID": set("lr"), "NASAL": set("mn"),
            "VOWELS": set("aeiouy")
        }
        self.ROOTS = {
            "HEAVY": ("lith", "ferr", "petr", "dens", "grav", "struct", "base", "fund", "mound"),
            "KINETIC": ("mot", "mov", "ject", "tract", "pel", "crat", "dynam", "flux"),
            "ABSTRACT": ("tion", "ism", "ence", "ance", "ity", "ology", "ness", "ment", "idea"),
            "SUBURBAN": ("norm", "comm", "stand", "pol", "reg", "mod"),
            "VITAL": ("viv", "vita", "spir", "anim", "bio", "luc", "lum", "phot", "phon", "surg", "bloom")
        }

    def clean(self, text):
        if not text: return []
        # Fix: Ensure unicode data is processed safely
        try:
            normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        except Exception:
            normalized = text # Fallback if normalization fails
        
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
        vowel = sum(1 for c in w if c in self.PHONETICS["VOWELS"])
        density_score = (plosive * 1.5) + (nasal * 0.8)
        flow_score = liquid + sum(1 for c in w if c in self.PHONETICS["FRICATIVE"])
        vitality_score = (vowel * 1.2) + (flow_score * 0.8)
        compression_mod = 1.0 if clean_len > 5 else 1.5
        final_density = (density_score / clean_len) * compression_mod
        final_vitality = (vitality_score / clean_len) * compression_mod
        if final_density > 0.55: return "heavy", round(final_density, 2)
        if final_vitality > 0.6: return "play", round(final_vitality, 2)
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

class LiteraryReproduction:
    MUTATIONS = {}
    JOY_CLADE = {}

    @classmethod
    def load_genetics(cls):
        try:
            cls.MUTATIONS = GENETICS.get("MUTATIONS", {})
            cls.JOY_CLADE = GENETICS.get("JOY_CLADE", {})
        except ImportError:
            cls.MUTATIONS = {}
            cls.JOY_CLADE = {}

    @staticmethod
    def _extract_counts(physics_container):
        if hasattr(physics_container, "counts"):
            return physics_container.counts
        return physics_container.get("counts", {})

    @staticmethod
    def mutate_config(current_config):
        mutations = {}
        if random.random() < 0.3:
            mutations["MAX_DRAG_LIMIT"] = current_config.MAX_DRAG_LIMIT * random.uniform(0.9, 1.1)
        if random.random() < 0.3:
            mutations["TOXIN_WEIGHT"] = current_config.TOXIN_WEIGHT * random.uniform(0.9, 1.2)
        if random.random() < 0.1:
            mutations["MAX_HEALTH"] = current_config.MAX_HEALTH * random.uniform(0.8, 1.05)
        return mutations

    @staticmethod
    def mitosis(parent_id, bio_state, physics, memory):
        counts = LiteraryReproduction._extract_counts(physics)
        dominant = max(counts, key=counts.get) if counts else "VOID"
        mutation_data = LiteraryReproduction.MUTATIONS.get(
            dominant.upper(),
            {"trait": "NEUTRAL", "mod": {}})
        child_id = f"{parent_id}_({mutation_data['trait']})"
        config_mutations = LiteraryReproduction.mutate_config(BoneConfig)
        trauma_vec = bio_state.get("trauma_vector", {})
        child_genome = {
            "source": "MITOSIS",
            "parent_a": parent_id,
            "parent_b": None,
            "mutations": mutation_data["mod"],
            "config_mutations": config_mutations,
            "dominant_flavor": dominant,
            "trauma_inheritance": trauma_vec}
        return child_id, child_genome

    @staticmethod
    def crossover(parent_a_id, parent_a_bio, parent_b_path):
        try:
            with open(parent_b_path, "r") as f:
                parent_b_data = json.load(f)
        except (IOError, json.JSONDecodeError):
            return None, "Dead Spore (Corrupt File)."

        parent_b_id = parent_b_data.get("session_id", "UNKNOWN")
        trauma_a = parent_a_bio.get("trauma_vector", {})
        trauma_b = parent_b_data.get("trauma_vector", {})
        child_trauma = {}
        all_keys = set(trauma_a.keys()) | set(trauma_b.keys())
        for k in all_keys:
            child_trauma[k] = max(trauma_a.get(k, 0), trauma_b.get(k, 0))
        enzymes_a = set()
        if "mito" in parent_a_bio:
            if hasattr(parent_a_bio["mito"], "state"):
                enzymes_a = set(parent_a_bio["mito"].state.enzymes)
            elif isinstance(parent_a_bio["mito"], dict):
                enzymes_a = set(parent_a_bio["mito"].get("enzymes", []))
        enzymes_b = set(parent_b_data.get("mitochondria", {}).get("enzymes", []))
        child_enzymes = list(enzymes_a | enzymes_b)
        config_mutations = LiteraryReproduction.mutate_config(BoneConfig)
        short_a = parent_a_id[-4:] if len(parent_a_id) > 4 else parent_a_id
        short_b = parent_b_id[-4:] if len(parent_b_id) > 4 else parent_b_id
        child_id = f"HYBRID_{short_a}x{short_b}"
        child_genome = {
            "source": "CROSSOVER",
            "parent_a": parent_a_id,
            "parent_b": parent_b_id,
            "trauma_inheritance": child_trauma,
            "config_mutations": config_mutations,
            "inherited_enzymes": child_enzymes}
        return child_id, child_genome

    def attempt_reproduction(self, engine_ref, mode="MITOSIS", target_spore=None) -> Tuple[str, Dict]:
        mem = engine_ref.mind.mem
        phys = engine_ref.phys.tension.last_physics_packet
        genome = {}
        log_msg = []
        
        if mode == "MITOSIS":
            bio_state = {"trauma_vector": engine_ref.trauma_accum}
            child_id, genome = self.mitosis(mem.session_id, bio_state, phys, mem)
            log_msg = [f"   ► CHILD SPAWNED: {Prisma.WHT}{child_id}{Prisma.RST}"]
            log_msg.append(f"   ► TRAIT: {genome.get('mutations', 'None')}")
            
        elif mode == "CROSSOVER":
            if not target_spore:
                return f"{Prisma.RED}FERTILITY ERROR: No partner found.{Prisma.RST}", {}
            current_bio = {"trauma_vector": engine_ref.trauma_accum, "mito": engine_ref.bio.mito}
            child_id, genome = self.crossover(mem.session_id, current_bio, target_spore)
            if not child_id:
                return f"{Prisma.RED}CROSSOVER FAILED: {genome}{Prisma.RST}", {}
            log_msg = [f"   HYBRID SPAWNED: {Prisma.WHT}{child_id}{Prisma.RST}"]
            
        full_spore_data = {
            "session_id": child_id,
            "meta": {
                "timestamp": time.time(),
                "final_health": engine_ref.health,
                "final_stamina": engine_ref.stamina
            },
            "trauma_vector": genome.get("trauma_inheritance", {}),
            "config_mutations": genome.get("config_mutations", {}),
            "mitochondria": {"enzymes": list(genome.get("inherited_enzymes", []))},
            "core_graph": mem.graph,
            "antibodies": list(engine_ref.bio.immune.active_antibodies)
        }
        filename = f"{child_id}.json"
        saved_path = mem.loader.save_spore(filename, full_spore_data)
        if saved_path:
            log_msg.append(f"   {Prisma.GRN}SAVED: {saved_path}{Prisma.RST}")
        return "\n".join(log_msg), genome.get("mutations", {})

# --- UTILS ---

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

class ParadoxSeed:
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
        
        cause_list = DeathGen.CAUSES.get(cause, ["System Error"])
        flavor_text = random.choice(cause_list) if cause_list else "Unknown Error"
        
        prefix_list = DeathGen.PREFIXES
        prefix = random.choice(prefix_list) if prefix_list else "RIP."
        
        verdict = "You vanished."
        if physics["voltage"] > 15.0: 
            verdict_list = DeathGen.VERDICTS.get("HEAVY", [])
            if verdict_list: verdict = random.choice(verdict_list)
        elif physics["voltage"] < 2.0: 
            verdict_list = DeathGen.VERDICTS.get("LIGHT", [])
            if verdict_list: verdict = random.choice(verdict_list)
            
        return f"{prefix} Cause of Death: {flavor_text}. {verdict}"

class TheCartographer:
    GRID_SIZE = 7

    @staticmethod
    def _get_tile(x, y, center, physics, vectors):
        dist_from_center = ((x - center)**2 + (y - center)**2) ** 0.5
        entropy_threshold = 3.0 - (vectors.get("ENT", 0.5) * 2.0)
        if dist_from_center > entropy_threshold:
            return f"{Prisma.GRY} . {Prisma.RST}"
        structure_noise = (x * 3 + y * 7) % 10 / 10.0
        if structure_noise < vectors.get("STR", 0.0):
            return f"{Prisma.OCHRE} ▲ {Prisma.RST}"
        if vectors.get("VEL", 0) > 0.6:
            if x == center or y == center:
                return f"{Prisma.CYN} = {Prisma.RST}"
        if vectors.get("BET", 0) > 0.5:
            return f"{Prisma.SLATE} ∷ {Prisma.RST}"
        return "   "

    @classmethod
    def weave(cls, _text, _graph, _bio_metrics, _limbo, physics=None):
        if not physics:
            return "MAP ERROR: No Physics Data", []
        vectors = physics.get("vector", {})
        center = cls.GRID_SIZE // 2
        rows = []
        border = f"{Prisma.GRY}+{'-' * (cls.GRID_SIZE * 3)}+{Prisma.RST}"
        rows.append(border)
        anchors = []
        for y in range(cls.GRID_SIZE):
            row_str = f"{Prisma.GRY}|{Prisma.RST}"
            for x in range(cls.GRID_SIZE):
                if x == center and y == center:
                    row_str += f"{Prisma.WHT} @ {Prisma.RST}"
                else:
                    row_str += cls._get_tile(x, y, center, physics, vectors)
            row_str += f"{Prisma.GRY}|{Prisma.RST}"
            rows.append(row_str)
        rows.append(border)
        if vectors.get("STR", 0) > 0.7: anchors.append("MOUNTAIN")
        if vectors.get("ENT", 0) > 0.7: anchors.append("VOID_EDGE")
        if vectors.get("VEL", 0) > 0.7: anchors.append("HIGHWAY")
        map_display = "\n".join(rows)
        return map_display, anchors

    @staticmethod
    def detect_voids(packet):
        return [w for w in packet["clean_words"] if w in TheLexicon.get("abstract")]

    @staticmethod
    def spin_web(_graph, inventory, _gordon):
        if "TIME_BRACELET" in inventory:
            return True, "WEB SPUN: The bracelet helps you tie the knots."
        return False, "WEAVE FAILED: You lack the tools to bind these concepts."

@dataclass
class CycleContext:
    input_text: str
    clean_words: List[str] = field(default_factory=list)
    physics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    is_alive: bool = True
    refusal_triggered: bool = False
    refusal_packet: Optional[Dict] = None
    is_bureaucratic: bool = False
    bio_result: Dict = field(default_factory=dict)
    world_state: Dict = field(default_factory=dict)
    mind_state: Dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    bureau_ui: str = "" # Added to support bureau packet

    def log(self, message: str):
        self.logs.append(message)

class TheAlmanac:
    def __init__(self):
        self.forecasts = {
            "HIGH_VOLTAGE": [
                "The wire is hot. Write immediately, without editing.",
                "Burn the fuel before it explodes. Speed is your friend.",
                "Do not seek structure. Seek impact."
            ],
            "HIGH_DRAG": [
                "The mud is deep. Stop trying to run.",
                "Focus on texture. Describe the weight of things.",
                "Slow down. The obstacle *is* the path."
            ],
            "HIGH_ENTROPY": [
                "The center is not holding. Find one true sentence.",
                "Simplify. Cut the adjectives. Locate the noun.",
                "Anchor yourself. Pick a physical object and describe it."
            ],
            "HIGH_TRAUMA": [
                "The wound is open. Treat it with care.",
                "Write what hurts, but write it in the third person.",
                "Use the pain as fuel, but filter it through the lens."
            ],
            "BALANCED": [
                "The Garden is growing. Tend to the edges.",
                "Structure and flow are aligned. Build something tall.",
                "You are in the zone. Maintain the rhythm."
            ]
        }

    def diagnose_condition(self, session_data: dict) -> Tuple[str, str]:
        meta = session_data.get("meta", {})
        trauma = session_data.get("trauma_vector", {})
        final_health = meta.get("final_health", 0)
        final_stamina = meta.get("final_stamina", 0)

        condition = "BALANCED"
        advice = "System nominal."

        max_trauma = max(trauma, key=trauma.get) if trauma else "NONE"
        trauma_val = trauma.get(max_trauma, 0)

        if final_health < 30 or trauma_val > 0.6:
            condition = "HIGH_TRAUMA"
            advice = f"Warning: High levels of {max_trauma} residue detected."
        elif final_stamina < 20:
            condition = "HIGH_DRAG"
            advice = "System exhaustion imminent. Semantic drag is heavy."
        elif meta.get("avg_voltage", 0) > 12.0:
            condition = "HIGH_VOLTAGE"
            advice = "The capacitor is overcharged."

        return condition, advice

    def get_seed(self, condition):
        strategies = {
            "HIGH_VOLTAGE": "What if you whispered instead of screamed?",
            "HIGH_DRAG": "Honor the error as a hidden intention.",
            "HIGH_ENTROPY": "Repetition is a form of change.",
            "HIGH_TRAUMA": "Turn it into a wallpaper pattern.",
            "BALANCED": "Discard the first idea. Trust the third."
        }
        return strategies.get(condition, "Look closely at the most boring thing in the room.")

    def compile_forecast(self, session_data: dict) -> str:
        condition, advice = self.diagnose_condition(session_data)
        forecast_text = random.choice(self.forecasts.get(condition, self.forecasts["BALANCED"]))
        seed_text = self.get_seed(condition)

        border = f"{Prisma.OCHRE}{'='*40}{Prisma.RST}"
        report = [
            "\n",
            border,
            f"{Prisma.CYN}   THE ALMANAC: CREATIVE WEATHER REPORT{Prisma.RST}",
            border,
            f"Condition: {Prisma.WHT}{condition}{Prisma.RST}",
            f"Observation: {Prisma.GRY}{advice}{Prisma.RST}",
            f"{Prisma.SLATE}---{Prisma.RST}",
            f"{Prisma.MAG}PRESCRIPTION:{Prisma.RST}",
            f"   {forecast_text}",
            "",
            f"{Prisma.GRN}Seed for Next Session:{Prisma.RST}",
            f"   {seed_text}",
            border,
            "\n"
        ]
        return "\n".join(report)

# --- PHYSICS CALCULATIONS (INTERNAL HELPER) ---

class _PhysicsCalc:
    """
    Internal helper to avoid circular imports with bone_physics.py
    Contains the logic from PhysicsResolver.
    """
    @staticmethod
    def calculate_voltage(counts: dict, config) -> float:
        heavy = counts.get("heavy", 0)
        explosive = counts.get("explosive", 0)
        constructive = counts.get("constructive", 0)
        raw_charge = (heavy * 2.0) + (explosive * 3.0) + (constructive * 1.5)
        final_voltage = raw_charge * config.KINETIC_GAIN
        return round(final_voltage, 2)

    @staticmethod
    def calculate_drag(clean_words: List, counts: dict, config) -> float:
        volume = max(1, len(clean_words))
        solvents = counts.get("solvents", 0)
        suburban = counts.get("suburban", 0)
        play = counts.get("play", 0)
        friction = (solvents * 1.0) + (suburban * 2.5)
        lift = play * 1.5
        net_drag = max(0.0, friction - lift)
        normalized_drag = (net_drag / volume) * 10.0
        final_drag = normalized_drag * config.SIGNAL_DRAG_MULTIPLIER
        return round(min(config.MAX_DRAG_LIMIT * 2, final_drag), 2)

    @staticmethod
    def derive_vector_matrix(counts: dict, total_vol: int, voltage: float, drag: float) -> dict:
        safe_vol = max(1, total_vol)
        def d(cat): return counts.get(cat, 0) / safe_vol
        return {
            "VEL": min(1.0, 0.5 + (d("explosive") * 2.0) + (d("kinetic") * 1.0) - (drag * 0.05)),
            "STR": min(1.0, 0.5 + (d("heavy") * 2.0) + (d("constructive") * 1.5)),
            "ENT": min(1.0, 0.5 + (d("antigen") * 3.0) + (d("toxin") * 2.0)),
            "TEX": min(1.0, 0.5 + (d("heavy") * 0.5) + (d("abstract") * 1.0)),
            "TMP": min(1.0, 0.5 + (d("thermal") * 2.0) - (d("cryo") * 2.0) + (voltage * 0.02)),
            "PHI": min(1.0, (d("heavy") + d("kinetic")) / max(1, d("abstract") + d("heavy"))),
            "PSI": min(1.0, 0.5 + (d("abstract") * 2.0)),
            "DEL": min(1.0, 0.5 + (d("play") * 2.0) + (d("unknown", 0) * 1.5)),
            "XI":  min(1.0, (d("suburban") + d("buffer")) * 2.0),
            "BET": min(1.0, d("suburban") + d("buffer")),
            "E":   min(1.0, (d("solvents") * 0.4)),
            "LQ":  min(1.0, d("passive_watch", 0) + d("mirror", 0))
        }

class TheTensionMeter:
    HEAVY_WEIGHT = 2.0
    KINETIC_WEIGHT = 1.5

    # Fix: Type hint fixed for generic EventBus to avoid import error
    def __init__(self, events):
        self.events = events
        self.perfection_streak = 0
        self.last_physics_packet = {}

    def audit_hubris(self, physics, lexicon_class):
        streak = physics.get("perfection_streak", 0)
        # Fix: Unused variable 'voltage' removed
        if streak >= 5:
            return (
                True,
                f"{Prisma.CYN}✨ FLOW STATE DETECTED: You are walking on air (Streak {streak}).{Prisma.RST}\n"
                f"   The Narrator is impressed. {Prisma.GRN}ATP +20.0.{Prisma.RST}",
                "FLOW_BOOST"
            )
        if streak == 4:
            return (
                True,
                f"{Prisma.VIOLET}WOBBLE: You are almost perfect. That is dangerous.{Prisma.RST}\n"
                f"   Don't look down.",
                None
            )
        if streak >= 3:
            return (
                True,
                f"{Prisma.CYN}MOMENTUM BUILDING: You are walking a tightrope (Streak {streak}).{Prisma.RST}\n"
                f"   The air is thin, but clear. Keep going.",
                None
            )
        return False, None, None

    def gaze(self, text: str, graph: Dict = None) -> Dict:
        graph = graph or {} # Fix: Safety check for None graph
        clean_words = TheLexicon.clean(text)
        counts, unknowns = self._tally_categories(clean_words, text)
        if unknowns:
            self._trigger_neuroplasticity(unknowns, counts, text)
        
        # Fix: Use local _PhysicsCalc instead of missing PhysicsResolver
        voltage = _PhysicsCalc.calculate_voltage(counts, BoneConfig)
        drag = _PhysicsCalc.calculate_drag(clean_words, counts, BoneConfig)
        integrity = self._measure_integrity(clean_words, graph, counts)
        vectors = _PhysicsCalc.derive_vector_matrix(counts, len(clean_words), voltage, drag)
        
        metrics = self._derive_complex_metrics(
            counts, clean_words, voltage, drag, integrity, vectors)
        packet = self._package_physics(text, clean_words, counts, voltage, drag, integrity, metrics)

        self.last_physics_packet = packet["physics"] 
        return packet

    def _tally_categories(self, clean_words: List[str], raw_text: str) -> Tuple[Counter, List[str]]:
        counts = Counter()
        unknowns = []
        if TheLexicon.ANTIGEN_REGEX:
            hits = TheLexicon.ANTIGEN_REGEX.findall(raw_text)
            counts["antigen"] = len(hits)
            counts["toxin"] = len(hits)
        target_cats = ["heavy", "explosive", "constructive", "abstract", "photo", "aerobic",
                       "thermal", "cryo", "suburban", "play", "sacred", "buffer", "antigen"]
        solvents = getattr(TheLexicon._STORE, "SOLVENTS", {"the", "is", "a"})
        for w in clean_words:
            if w in solvents:
                counts["solvents"] += 1
                continue
            found = False
            for cat in target_cats:
                if w in TheLexicon.get(cat):
                    counts[cat] += 1
                    found = True
            if not found:
                flavor, confidence = TheLexicon.taste(w)
                if flavor and confidence > 0.5:
                    counts[flavor] += 1
                else:
                    unknowns.append(w)
        return counts, unknowns

    def _trigger_neuroplasticity(self, unknowns: List[str], counts: Counter, raw_text: str):
        voltage = (counts["heavy"] * 2.0) + (counts["kinetic"] * 1.5)
        if voltage > 5.0 and unknowns:
            dominant_cat = max(counts, key=counts.get) if counts else "kinetic"
            for stranger in unknowns:
                if len(stranger) < 3:
                    continue
                if not self._is_structurally_sound(stranger):
                    if voltage < 15.0: continue
                flavor, confidence = TheLexicon.taste(stranger)
                if flavor and confidence > 0.6:
                    assigned_cat = flavor
                    method = "Phonetic Analysis"
                else:
                    assigned_cat = dominant_cat
                    method = "Context Association"
                TheLexicon.teach(stranger, assigned_cat, 0)
                self.events.log(
                    f"{Prisma.MAG}NEUROPLASTICITY: '{stranger}' tasted like [{assigned_cat.upper()}] ({method}).{Prisma.RST}",
                    "MISC"
                )
                counts[assigned_cat] += 1

    def _measure_integrity(self, words: List[str], graph: Dict, counts: Counter) -> Dict:
        if not words:
            return {"kappa": 0.0, "psi": 0.0, "mass": 0.0}
        anchors = [w for w in words if w in graph]
        mass = sum(sum(graph[w]["edges"].values()) for w in anchors)
        artificial_mass = counts["constructive"] * 0.5
        kappa = min(1.0, (mass + artificial_mass) / BoneConfig.SHAPLEY_MASS_THRESHOLD)
        total = len(words)
        abstract_count = counts["abstract"]
        heavy_count = counts["heavy"]
        psi = min(1.0, (abstract_count / total) + 0.2)
        if heavy_count > abstract_count:
            base_psi = (abstract_count * 0.7 + heavy_count * 0.3) / total
            psi = min(1.0, max(0.1, base_psi + 0.1))
        return {"kappa": round(kappa, 3), "psi": round(psi, 2), "mass": round(mass, 1)}

    def _derive_complex_metrics(self, counts, words, voltage, drag, integrity, vectors):
        total_vol = max(1, len(words))
        turbulence = TheLexicon.get_turbulence(words)
        flow_state = "LAMINAR" if turbulence < 0.3 else "TURBULENT"
        mass_words = counts["heavy"] + counts["kinetic"] + counts["thermal"] + counts["cryo"]
        cohesion_words = counts["suburban"] + counts["buffer"] + counts["antigen"] + (counts["abstract"] * 0.5)
        E_val = mass_words / total_vol
        B_val = cohesion_words / total_vol
        beta_index = vectors["BET"] * 5.0
        truth_ratio = vectors["PHI"]
        total_viscosity = sum(TheLexicon.measure_viscosity(w) for w in words)
        avg_viscosity = total_viscosity / total_vol
        if total_vol <= 1 and not words:
            avg_viscosity = 0.1
        repetition_score = round(1.0 - (len(set(words)) / total_vol), 2)
        bond_strength = max(0.1, integrity["kappa"] + (repetition_score * 0.5))
        voltage_load = max(0.1, voltage / 10.0)
        gamma = round((bond_strength * avg_viscosity) / (1.0 + voltage_load), 2)
        gamma = max(0.01, gamma)
        if truth_ratio > 0.85 and voltage > 12.0:
            self.perfection_streak += 1
        else:
            self.perfection_streak = 0
        if self.perfection_streak == 4:
            flow_state = "HUBRIS_RISK"
        zone, zone_color = self._determine_zone(beta_index, truth_ratio)
        return {
            "beta_index": round(beta_index, 2),
            "vector": vectors,
            "gamma": gamma,
            "turbulence": turbulence,
            "flow_state": flow_state,
            "truth_ratio": round(truth_ratio, 2),
            "repetition": repetition_score,
            "avg_viscosity": round(avg_viscosity, 2),
            "E": round(E_val, 2),
            "B": round(B_val, 2),
            "zone": zone,
            "zone_color": zone_color
        }

    def _determine_zone(self, beta, truth):
        if beta > 2.0 and truth > 0.8:
            return "AERIE", "WHT"
        elif beta > BoneConfig.ZONE_THRESHOLDS["LABORATORY"]:
            return "BASEMENT", "VIOLET"
        elif beta > BoneConfig.ZONE_THRESHOLDS["COURTYARD"]:
            return "LABORATORY", "INDIGO"
        return "COURTYARD", "OCHRE"

    def _package_physics(self, text, clean_words, counts, voltage, drag, integrity, metrics):
        physics_bridge = {
            "voltage": voltage,
            "narrative_drag": drag,
            "kappa": integrity["kappa"],
            "psi": integrity["psi"],
            "geodesic_mass": integrity["mass"],
            "beta_index": metrics["beta_index"],
            "gamma": metrics["gamma"],
            "turbulence": metrics["turbulence"],
            "flow_state": metrics["flow_state"],
            "zone": metrics["zone"],
            "zone_color": metrics["zone_color"],
            "truth_ratio": metrics["truth_ratio"],
            "counts": counts,
            "clean_words": clean_words,
            "raw_text": text,
            "vector": metrics["vector"],
            "antigens": counts.get("antigen", 0),
            "repetition": metrics["repetition"],
            "perfection_streak": self.perfection_streak,
            "avg_viscosity": metrics["avg_viscosity"],
            "E": metrics["E"],
            "B": metrics["B"]}
        return {
            "physics": physics_bridge,
            "clean_words": clean_words,
            "raw_text": text,
            "glass": {
                "prosody": {"arousal": voltage},
                "resonance": voltage
            }
        }

    @staticmethod
    def _is_structurally_sound(word):
        if not re.search(r"[aeiouy]", word): return False
        if re.search(r"(.)\1{2,}", word): return False
        return True

class TemporalDynamics:
    def __init__(self):
        self.voltage_history = []
        self.window = 3
    def commit(self, voltage):
        self.voltage_history.append(voltage)
        if len(self.voltage_history) > self.window:
            self.voltage_history.pop(0)
    def get_velocity(self):
        if len(self.voltage_history) < 2:
            return 0.0
        return round(
            (self.voltage_history[-1] - self.voltage_history[0])
            / len(self.voltage_history),
            2,)

class ApeirogonResonance:
    def __init__(self, events):
        self.events = events
        self.DIMENSIONS = {}
        self.NOUNS = {}
        self.load_resonances()
    def load_resonances(self):
        self.DIMENSIONS = RESONANCE.get("DIMENSIONS", {})
        self.NOUNS = RESONANCE.get("NOUNS", {})
    def _resolve_term(self, val, scale):
        if val >= 0.85: return scale[-1][1]
        if val <= 0.15: return scale[0][1]
        best_fit = min(scale, key=lambda x: abs(x[0] - val))
        return best_fit[1]
    def architect(self, metrics, station, is_bored):
        phys = metrics.get("physics", {})
        vec = phys.get("vector", {})
        if is_bored:
            return {
                "title": "THE FRACTAL BLOOM",
                "color": Prisma.VIOLET,
                "desc": "Boredom Threshold exceeded. Entropy is high.",
                "context": "CHAOS"}
        if station:
            role_color = Prisma.CYN
            if station[0] == "GORDON": role_color = Prisma.OCHRE
            elif station[0] == "SHERLOCK": role_color = Prisma.INDIGO
            elif station[0] == "JESTER": role_color = Prisma.VIOLET
            return {
                "title": station[2].upper().replace('THE ', 'THE '),
                "color": role_color,
                "desc": station[1],
                "context": station[0]}
        
        # Safe handling for incomplete vector data
        if not vec or len(vec) < 2:
             return {"title": "THE VOID", "color": Prisma.GRY, "desc": "No data.", "context": "VOID"}

        sorted_dims = sorted(vec.items(), key=lambda x: abs(x[1] - 0.5), reverse=True)
        p_dim, p_val = sorted_dims[0]
        s_dim, s_val = sorted_dims[1]
        noun_list = self.NOUNS.get(p_dim, ["THING"])
        idx = int(p_val * (len(noun_list) - 1))
        idx = max(0, min(len(noun_list) - 1, idx))
        noun = noun_list[idx]
        adj_scale = self.DIMENSIONS.get(s_dim, [[0.0, "NEUTRAL"]])
        adj = self._resolve_term(s_val, adj_scale)
        title = f"THE {adj} {noun}"
        color = Prisma.WHT
        if p_dim == "TMP": color = Prisma.RED if p_val > 0.5 else Prisma.CYN
        elif p_dim == "VEL": color = Prisma.GRN
        elif p_dim == "STR": color = Prisma.OCHRE
        elif p_dim == "ENT": color = Prisma.VIOLET
        return {
            "title": title,
            "color": color,
            "desc": f"Vector Lock: {p_dim}({p_val:.2f}) + {s_dim}({s_val:.2f})",
            "context": "APEIROGON"}

class MirrorGraph:
    def __init__(self):
        self.stats = {
            "WAR": 0.0,
            "ART": 0.0,
            "LAW": 0.0,
            "ROT": 0.0
        }
        self.dominant_archetype = "NEUTRAL"
        self.active_mode = True
        self.profile = UserProfile()

    def profile_input(self, text: str, physics: Dict):
        if hasattr(self, 'profile'):
            self.profile.update(physics.get("counts", {}), len(physics.get("clean_words", [])))
        vol = physics.get("voltage", 0.0)
        ent = physics.get("entropy", 0.0) # Assuming E from VSL
        psi = physics.get("psi", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        decay = 0.05
        for k in self.stats:
            self.stats[k] = max(0.0, self.stats[k] - decay)
        if vol > 12.0 or "!" in text:
            self.stats["WAR"] = min(1.0, self.stats["WAR"] + 0.2)
        if psi > 0.6 or "?" in text:
            self.stats["ART"] = min(1.0, self.stats["ART"] + 0.2)
        if drag < 2.0 and vol < 5.0:
            self.stats["LAW"] = min(1.0, self.stats["LAW"] + 0.2)
        if text.startswith("/"):
            self.stats["LAW"] = min(1.0, self.stats["LAW"] + 0.1)
        if physics.get("turbulence", 0) > 0.5:
            self.stats["ROT"] = min(1.0, self.stats["ROT"] + 0.2)
        self.dominant_archetype = max(self.stats, key=self.stats.get)

    def get_reflection_modifiers(self) -> Dict:
        top_stat = self.dominant_archetype
        intensity = self.stats[top_stat]
        mods = {
            "drag_mult": 1.0,
            "plasticity": 1.0,
            "loot_chance": 1.0,
            "atp_tax": 0.0,
            "voltage_cap": 20.0,
            "flavor": ""
        }
        if intensity < 0.3:
            return mods
        if top_stat == "WAR":
            mods["drag_mult"] = 1.5
            mods["loot_chance"] = 2.0
            mods["atp_tax"] = 5.0 # War is expensive
            mods["flavor"] = f"{Prisma.RED}[MIRROR]: Aggression detected. The simulation hardens its shell. (Drag UP, Loot UP){Prisma.RST}"
        elif top_stat == "ART":
            mods["plasticity"] = 2.0
            mods["drag_mult"] = 0.5
            mods["voltage_cap"] = 10.0
            mods["flavor"] = f"{Prisma.CYN}[MIRROR]: Abstract thought dominant. Physics are permeable. (Plasticity UP, Voltage Capped){Prisma.RST}"
        elif top_stat == "LAW":
            mods["drag_mult"] = 0.8
            mods["loot_chance"] = 0.0
            mods["plasticity"] = 0.2
            mods["flavor"] = f"{Prisma.GRY}[MIRROR]: Forms filed in triplicate. Deviation is prohibited. (Stability UP, Loot ZERO){Prisma.RST}"
        elif top_stat == "ROT":
            mods["plasticity"] = 0.5
            mods["drag_mult"] = 1.2
            mods["atp_tax"] = 2.0
            mods["flavor"] = f"{Prisma.VIOLET}[MIRROR]: Entropy rising. Logic integrity failing. (Chaos UP){Prisma.RST}"
        return mods

    def render_report(self):
        """For the /mirror command."""
        def bar(v, color): return f"{color}{'█' * int(v * 10)}{'░' * (10 - int(v * 10))}{Prisma.RST}"
        return (
            f"WAR [{self.stats['WAR']:.2f}] {bar(self.stats['WAR'], Prisma.RED)}\n"
            f"ART [{self.stats['ART']:.2f}] {bar(self.stats['ART'], Prisma.CYN)}\n"
            f"LAW [{self.stats['LAW']:.2f}] {bar(self.stats['LAW'], Prisma.WHT)}\n"
            f"ROT [{self.stats['ROT']:.2f}] {bar(self.stats['ROT'], Prisma.VIOLET)}"
        )

class StrunkWhiteProtocol:
    def __init__(self):
        # Fallback to empty if missing
        from bone_data import STYLE_CRIMES
        self.PATTERNS = STYLE_CRIMES.get("PATTERNS", [])
        self.BANNED = STYLE_CRIMES.get("BANNED_PHRASES", [])

    def sanitize(self, text: str) -> Tuple[str, Optional[str]]:
        original = text
        log_msg = None
        for ban in self.BANNED:
            if ban in text.lower():
                text = re.sub(f"(?i){ban}", "", text)
                text = re.sub(r"\s{2,}", " ", text)
                log_msg = f"{Prisma.GRY}[STYLE]: Pruned cliche '{ban}'.{Prisma.RST}"
        for p in self.PATTERNS:
            match = re.search(p["regex"], text)
            if match:
                if p["action"] == "STRIP_PREFIX":
                    parts = text.split(" but ")
                    if len(parts) > 1:
                        substance = parts[-1].strip()
                        substance = substance[0].upper() + substance[1:]
                        text = substance
                        log_msg = f"{Prisma.CYN}[STYLE]: Collapsed Negative Comparison ('Not X, but Y').{Prisma.RST}"
                elif p["action"] == "KEEP_TAIL":
                    text = match.group(1).strip()
                    text = text[0].upper() + text[1:]
                    log_msg = f"{Prisma.CYN}[STYLE]: Decoupled Hedging Clause.{Prisma.RST}"
        if text != original:
            return text.strip(), log_msg
        return text, None

class TheHoloProjector:
    def __init__(self):
        self.BAR_CHARS = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    def _draw_bar(self, value, max_val=1.0, width=5):
        ratio = max(0.0, min(1.0, value / max(1.0, max_val)))
        idx = int(ratio * (len(self.BAR_CHARS) - 1))
        return self.BAR_CHARS[idx] * width

    def _draw_vector_compass(self, vector_data):
        pairs = [
            ("VEL", vector_data.get("VEL", 0), "STR", vector_data.get("STR", 0)),
            ("ENT", vector_data.get("ENT", 0), "PHI", vector_data.get("PHI", 0)),
            ("TMP", vector_data.get("TMP", 0), "PSI", vector_data.get("PSI", 0)),]
        display = []
        for l1, v1, l2, v2 in pairs:
            bar1 = self._draw_bar(v1, 1.0, 3)
            bar2 = self._draw_bar(v2, 1.0, 3)
            display.append(f"{Prisma.CYN}{l1} {bar1}{Prisma.RST} | {Prisma.MAG}{bar2} {l2}{Prisma.RST}")
        return "   ".join(display)

    def render(self, m: Dict, signals: Dict, lens_data: Tuple) -> str:
        p = m["physics"]
        bio = signals.get("bio", {})
        chem = bio.get("chem", {})
        atp = bio.get("atp", 0.0)
        voltage = p.get("voltage", 0.0)
        drag = p.get("narrative_drag", 0.0)
        lens_name = lens_data[0]
        lens_thought = lens_data[1]
        header_color = Prisma.GRY
        world = signals.get("world", {})
        trigram = world.get("trigram", {})
        t_display = ""
        if trigram:
            sym = trigram.get("symbol", "")
            name = trigram.get("name", "")
            col = trigram.get("color", Prisma.WHT)
            t_display = f"{col}{sym} {name}{Prisma.RST} "
        if voltage > 15.0: header_color = Prisma.RED
        elif voltage < 5.0: header_color = Prisma.CYN
        health_bar = self._draw_bar(signals.get("health", 0), 100.0, 5)
        stamina_bar = self._draw_bar(signals.get("stamina", 0), 100.0, 5)
        atp_indicator = f"{int(atp)}J"
        flow_state = p.get("flow_state", "LAMINAR")
        hubris_indicator = ""
        if flow_state == "HUBRIS_RISK":
            hubris_indicator = f" {Prisma.YEL}[⚠ HUBRIS IMMINENT]{Prisma.RST}"
        elif p.get("perfection_streak", 0) >= 5:
            hubris_indicator = f" {Prisma.CYN}[∞ FLOW STATE]{Prisma.RST}"
        dashboard_top = (
            f"{t_display}"
            f"{Prisma.GRY}[HP: {health_bar}] [STM: {stamina_bar}] "
            f"[ATP: {atp_indicator}] [V:{voltage:.1f}⚡] [D:{drag:.1f}⚓]{Prisma.RST}"
            f"{hubris_indicator}")
        dop = chem.get("DOP", 0)
        cor = chem.get("COR", 0)
        chem_readout = (
            f"   {Prisma.GRN}DOP:{dop:.2f}{Prisma.RST} "
            f"{Prisma.RED}COR:{cor:.2f}{Prisma.RST} "
            f"{Prisma.CYN}OXY:{chem.get('OXY',0):.2f}{Prisma.RST}")
        vectors = self._draw_vector_compass(p.get("vector", {}))
        clean_thought = lens_thought or "..."
        if lens_name == "NARRATOR":
            clean_thought = clean_thought.replace("You are [The Witness]...", "")
        separator = f"{Prisma.SLATE}{'—'*40}{Prisma.RST}"
        
        lens_display = lens_name.upper() if lens_name else "UNKNOWN"
        ui_block = [
            separator,
            f"{header_color}♦ {lens_display}{Prisma.RST}  {dashboard_top}",
            f"{vectors}",
            separator,
            f"{Prisma.WHT}{clean_thought}{Prisma.RST}",
            ""]
        world = signals.get("world", {})
        orbit = world.get("orbit")
        if orbit and orbit[0] != "VOID_DRIFT":
            ui_block.insert(3, f"   🪐 {Prisma.OCHRE}{orbit[2]}{Prisma.RST}")
        return "\n".join(ui_block)

class SoritesIntegrator:
    def __init__(self, memory_network):
        self.mem = memory_network
        self.active_constellations = set()

    def measure_ignition(self, clean_words, voltage_history):
        if not self.mem.graph:
            return 0.0, set(), 999.0
        if voltage_history:
            avg_volts = sum(voltage_history) / len(voltage_history)
        else:
            avg_volts = 0.0
        sliding_threshold = BoneConfig.BASE_IGNITION_THRESHOLD + (avg_volts * 0.03)
        echoes = 0
        self.active_constellations.clear()
        for w in clean_words:
            if w in self.mem.graph:
                node = self.mem.graph[w]
                edge_mass = sum(node["edges"].values())
                if edge_mass > (2.5 * sliding_threshold * 2):
                    echoes += 1
                    self.active_constellations.add(w)
        total_vol = max(1, len(clean_words))
        ignition_score = round(echoes / total_vol, 2)
        return ignition_score, self.active_constellations, sliding_threshold

    @staticmethod
    def get_readout(score, threshold):
        if score > threshold:
            return (
                "IGNITED",
                f"HEAP IGNITION ({int(score*100)}%): The Ancestors are speaking.",)
        return "INERT", f"⏳ INERT SAND ({int(score*100)}%): Building mass..."

class TheCrucible:
    def __init__(self):
        self.max_voltage_cap = 20.0
        self.active_state = "COLD"
        self.dampener_charges = 3
        self.dampener_tolerance = 15.0
        self.target_pressure = 10.0
        self.osmotic_memory = 0.0
        self.last_pressure_diff = 0.0
        self.sensitivity = 0.5
        self.saturation = 0.1
        self.anticipation = 0.2

    def dampen(self, voltage_spike, stability_index):
        if self.dampener_charges <= 0:
            return False, "The Damper is empty.", 0.0
        if voltage_spike > self.dampener_tolerance:
            self.dampener_charges -= 1
            reduction = voltage_spike * 0.7
            return True, f"CRUCIBLE DAMPENER: Circuit Breaker. Reduced {voltage_spike}v by {reduction:.1f}v.", reduction
        elif voltage_spike > 8.0 and stability_index < 0.4:
            self.dampener_charges -= 1
            return True, f"CRUCIBLE DAMPENER: Tipped. High Voltage ({voltage_spike}v) on Unstable Ground. Dampening.", 0.0
        return False, "Structure is holding the charge.", 0.0

    def audit_fire(self, physics):
        voltage = physics.get("voltage", 0.0)
        structure = physics.get("kappa", 0.0)
        lignin_signal = self._regulate_turgor(voltage)
        current_drag = physics.get("narrative_drag", 0.0)
        adjustment = lignin_signal * 0.5
        if current_drag < 1.0 and adjustment > 0:
            adjustment *= 0.1
        new_drag = max(0.0, min(10.0, current_drag + adjustment))
        physics["narrative_drag"] = round(new_drag, 2)
        msg = None
        if abs(adjustment) > 1.0:
            if adjustment > 0:
                action = "LIGNIFYING"
                desc = "Cell Walls hardening under High Voltage."
            else:
                action = "EXPANDING"
                desc = "Turgor pressure relaxing. Membrane permeability up."
            msg = f"{Prisma.CYN}HOMEOSTASIS: {action}: {desc} (Drag {current_drag:.1f} -> {new_drag:.1f}).{Prisma.RST}"
        if physics.get("system_surge_event", False):
            self.active_state = "SURGE"
            return "SURGE", 0.0, f"{Prisma.CYN}CRUCIBLE: Absorbing System Surge ({voltage}v). No structural damage.{Prisma.RST}"
        if voltage > 18.0:
            if structure > 0.5:
                return self._sublimate(voltage)
            else:
                return self._meltdown(voltage)
        self.active_state = "REGULATED"
        return "REGULATED", 0.0, msg

    def _regulate_turgor(self, current_voltage):
        stress = current_voltage - self.target_pressure
        self.osmotic_memory = max(-5.0, min(5.0, self.osmotic_memory + stress))
        velocity = stress - self.last_pressure_diff
        self.last_pressure_diff = stress
        signal = (self.sensitivity * stress) + \
                 (self.saturation * self.osmotic_memory) + \
                 (self.anticipation * velocity)
        return signal

    def _sublimate(self, voltage):
        self.active_state = "RITUAL"
        gain = voltage * 0.1
        self.max_voltage_cap += gain
        return "RITUAL", gain, f"CRUCIBLE RITUAL: Voltage ({voltage}v) contained. Capacity expanded to {self.max_voltage_cap:.1f}v."

    def _meltdown(self, voltage):
        self.active_state = "MELTDOWN"
        damage = voltage * 0.5
        return "MELTDOWN", damage, f"CRUCIBLE CRACKED: Fire lacks Structure (Kappa Low). Hull Breach. -{damage:.1f} Health."

class TheForge:
    def hammer_alloy(self, physics):
        voltage = physics["voltage"]
        clean_words = physics["clean_words"]
        counts = physics["counts"]
        total_mass = (counts.get("heavy", 0) * 2.0) + (counts.get("kinetic", 0) * 0.5)
        avg_density = total_mass / max(1, len(clean_words))
        if voltage > BoneConfig.ANVIL_TRIGGER_VOLTAGE and avg_density > 0.4:
            if counts.get("heavy", 0) > 3 and physics.get("vector", {}).get("VEL", 0) < 0.3:
                return True, f"{Prisma.OCHRE}THE ANVIL THUDS: You forged gravity itself.{Prisma.RST}", "LEAD_BOOTS"
            if counts.get("kinetic", 0) > 3 and voltage < 12.0:
                return True, f"{Prisma.CYN}THE ANVIL CLICKS: Cold steel, safe for children.{Prisma.RST}", "SAFETY_SCISSORS"
            return True, f"{Prisma.GRY}THE ANVIL RINGS: Mass condensed into form.{Prisma.RST}", "ANCHOR_STONE"
        return False, None, None

    @staticmethod
    def transmute(physics):
        counts = physics["counts"]
        voltage = physics["voltage"]
        gamma = physics.get("gamma", 0.0)
        if gamma < 0.15 and counts.get("abstract", 0) > 1:
            oil = TheLexicon.harvest("abstract")
            binder = TheLexicon.harvest("heavy")
            return (
                f"{Prisma.OCHRE}THE EMULSIFIER: The emulsion is breaking (Tension: {gamma}).{Prisma.RST}\n"
                f"   You are pouring Oil ('{oil}') into Water without a Binder.\n"
                f"   {Prisma.WHT}Try this: Use '{binder.upper()}' to suspend the concept.{Prisma.RST}")
        if voltage > 8.5:
            coolant = TheLexicon.harvest("aerobic")
            return (
                f"{Prisma.CYN}THERMAL SPIKE ({voltage}v). Structure is brittle.{Prisma.RST}\n"
                f"   Injecting Coolant: '{coolant}'. Breathe. Add space.")
        return None



class TheTheremin:
    def __init__(self):
        self.resonance_log = deque(maxlen=5)
        self.resin_buildup = 0.0
        self.calcification_turns = 0
        self.AMBER_THRESHOLD = 20.0
        self.SHATTER_POINT = 80.0
        self.is_stuck = False

    def listen(self, physics, governor_mode="COURTYARD"):
        clean = physics["clean_words"]
        voltage = physics.get("voltage", 0.0)
        ancient_mass = sum(1 for w in clean if w in TheLexicon.get("heavy") or w in TheLexicon.get("thermal") or w in TheLexicon.get("cryo"))
        modern_mass = sum(1 for w in clean if w in TheLexicon.get("abstract"))
        thermal_hits = sum(1 for w in clean if w in TheLexicon.get("thermal"))
        solvent_active = False
        solvent_msg = ""
        if thermal_hits > 0 and self.resin_buildup > 5.0:
            dissolved = thermal_hits * 15.0
            self.resin_buildup = max(0.0, self.resin_buildup - dissolved)
            self.calcification_turns = 0
            solvent_active = True
            solvent_msg = f"{Prisma.OCHRE}SOLVENT APPLIED: Thermal words melted the Amber (-{dissolved:.1f} Resin).{Prisma.RST}"
            if self.is_stuck and self.resin_buildup < self.AMBER_THRESHOLD:
                self.is_stuck = False
                solvent_msg += f" {Prisma.GRN}RELEASE: You burned your way out.{Prisma.RST}"
        raw_mix = min(ancient_mass, modern_mass)
        resin_flow = raw_mix * 2.0
        if governor_mode == "LABORATORY":
            resin_flow *= 0.5
        if voltage > 5.0:
            resin_flow = max(0.0, resin_flow - (voltage * 0.6))
        rep = physics.get("repetition", 0.0)
        complexity = physics.get("truth_ratio", 0.0)
        theremin_msg = None
        critical_event = None
        if rep > 0.5:
            self.calcification_turns += 1
            slag = self.calcification_turns * 4.0
            self.resin_buildup += slag
            theremin_msg = f"{Prisma.OCHRE}CALCIFICATION: Repetition detected (Turn {self.calcification_turns}). Resin hardening (+{slag}).{Prisma.RST}"
        elif complexity > 0.4 and self.calcification_turns > 0:
            self.calcification_turns = 0
            relief = 15.0
            self.resin_buildup = max(0.0, self.resin_buildup - relief)
            theremin_msg = f"{Prisma.GRN}PERCUSSIVE MAINTENANCE: Calcification Shattered. Flow restored. (-{relief} Resin){Prisma.RST}"
        if solvent_active:
            theremin_msg = f"{theremin_msg} | {solvent_msg}" if theremin_msg else solvent_msg
        elif resin_flow > 0.5:
            self.resin_buildup += resin_flow
            if not theremin_msg:
                theremin_msg = f"{Prisma.OCHRE}RESIN FLOW: Hybrid complexity (+{resin_flow:.1f}). Keep it hot to prevent sticking.{Prisma.RST}"
        if resin_flow == 0 and self.calcification_turns == 0:
            self.resin_buildup = max(0.0, self.resin_buildup - 2.0)
        if self.resin_buildup > self.SHATTER_POINT:
            self.resin_buildup = 0.0
            self.calcification_turns = 0
            return False, resin_flow, f"{Prisma.RED}SHATTER EVENT: Resin overflow. System is solid amber. INITIATING AIRSTRIKE.{Prisma.RST}", "AIRSTRIKE"
        if self.calcification_turns > 3:
            critical_event = "CORROSION"
            theremin_msg = f"{theremin_msg} | {Prisma.YEL}FOSSILIZATION IMMINENT{Prisma.RST}"
        if self.resin_buildup > self.AMBER_THRESHOLD:
            self.is_stuck = True
            if not theremin_msg:
                theremin_msg = f"{Prisma.RED}AMBER TRAP: You are stuck in the resin. Increase Voltage to melt it.{Prisma.RST}"
        if self.is_stuck and self.resin_buildup < 5.0:
            self.is_stuck = False
            if not solvent_active:
                theremin_msg = f"{Prisma.GRN}LIQUEFACTION: The Amber melts. You are free.{Prisma.RST}"
        turb = physics.get("turbulence", 0.0)
        if turb > 0.6 and self.resin_buildup > 0:
            shatter_amt = turb * 10.0
            self.resin_buildup = max(0.0, self.resin_buildup - shatter_amt)
            theremin_msg = f"{Prisma.CYN}TURBULENCE: Jagged rhythm broke the resin (-{shatter_amt:.1f}).{Prisma.RST}"
            self.calcification_turns = 0
        if turb < 0.2:
            physics["narrative_drag"] = max(0.0, physics["narrative_drag"] - 1.0)
        return self.is_stuck, resin_flow, theremin_msg, critical_event

    def get_readout(self):
        return f"{Prisma.GRY}[THEREMIN]: Resin={self.resin_buildup:.1f} | Calcification={self.calcification_turns}{Prisma.RST}"

@dataclass
class Manifold:
    name: str
    center_vector: tuple
    radius: float
    description: str
    modifiers: Dict[str, float] = field(default_factory=dict)
    entry_msg: str = "You have entered a new space."

class TheNavigator:
    def __init__(self, shimmer_ref):
        self.shimmer = shimmer_ref
        self.current_location = "THE_MUD"
        self.root_system = None
        self.root_tolerance = 0.4
        self.manifolds = {
            "THE_MUD": Manifold(
                "THE_MUD", (0.8, 0.2), 0.2,
                "High Fatigue, Low Tension (Stagnation)",
                {"narrative_drag": 2.0, "voltage": -2.0},
                f"{Prisma.OCHRE}THE MUD: The ground is sticky. Movement costs double.{Prisma.RST}"
            ),
            "THE_FORGE": Manifold(
                "THE_FORGE", (0.1, 0.9), 0.2,
                "Low Fatigue, High Tension (Transformation)",
                {"voltage": 5.0, "narrative_drag": -1.0, "psi": -0.1},
                f"{Prisma.RED}THE FORGE: Sparks fly. Your words are heating up.{Prisma.RST}"
            ),
            "THE_AERIE": Manifold(
                "THE_AERIE", (0.2, 0.1), 0.2,
                "Low Fatigue, Low Tension (Abstraction)",
                {"narrative_drag": -3.0, "psi": 0.3, "voltage": -1.0},
                f"{Prisma.CYN}THE AERIE: The air is thin. Concepts float freely here.{Prisma.RST}"
            ),
            "THE_GLITCH": Manifold(
                "THE_GLITCH", (0.9, 0.9), 0.1,
                "High Fatigue, High Tension (Collapse)",
                {"turbulence": 0.5, "beta_index": 2.0},
                f"{Prisma.VIOLET}THE GLITCH: Reality is buffering...{Prisma.RST}"
            ),
            "THE_GARDEN": Manifold(
                "THE_GARDEN", (0.5, 0.5), 0.3,
                "Balanced State (Integration)",
                {"kappa": 0.2, "truth_ratio": 0.1},
                f"{Prisma.GRN}THE GARDEN: The soil is rich. Roots go deep.{Prisma.RST}"
            )
        }

    def strike_root(self, vector_data):
        self.root_system = vector_data
        return f"{Prisma.CYN}NAVIGATOR: Rhizome Rooted. Mycelial network established.{Prisma.RST}"

    def report_position(self, physics: Dict) -> str:
        drag = min(10.0, max(0.0, physics.get("narrative_drag", 0.0)))
        volt = min(20.0, max(0.0, physics.get("voltage", 0.0)))
        my_vec = (round(drag / 10.0, 2), round(volt / 20.0, 2))
        lines = [
            f"{Prisma.CYN}--- MANIFOLD NAVIGATION ---{Prisma.RST}",
            f"Current Loc: {Prisma.WHT}{self.current_location}{Prisma.RST}",
            f"Coordinates: [Drag: {drag:.1f} | Voltage: {volt:.1f}]",
            f"Shimmer Reserves: {self.shimmer.current:.1f}\n",
            f"{Prisma.GRY}Nearby Manifolds:{Prisma.RST}"
        ]
        for name, data in self.manifolds.items():
            dist = math.dist(my_vec, data.center_vector)
            bar_len = int((1.0 - min(1.0, dist)) * 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)
            highlight = Prisma.GRN if name == self.current_location else Prisma.GRY
            lines.append(f"   {highlight}{name:<12}{Prisma.RST} {bar} {dist:.2f} AU")
        return "\n".join(lines)

    def check_transplant_shock(self, current_vector):
        if not self.root_system: return None
        stress_sum = 0.0
        dims = 0
        for dim, val in current_vector.items():
            if dim in self.root_system:
                stress_sum += abs(val - self.root_system[dim])
                dims += 1
        avg_stress = stress_sum / max(1, dims)
        if avg_stress > self.root_tolerance:
            return f"{Prisma.OCHRE}TRANSPLANT SHOCK: You are pulling away from the root ({avg_stress:.2f}). Return to the source.{Prisma.RST}"
        return None

    def locate(self, physics_packet: dict) -> Tuple[str, Optional[str]]:
        old_loc = self.current_location
        if self.check_anomaly(physics_packet.get("raw_text", "")):
            self.current_location = "THE_GLITCH"
            if old_loc != "THE_GLITCH":
                return self.current_location, self.manifolds["THE_GLITCH"].entry_msg
            return self.current_location, None
        drag = min(10.0, max(0.0, physics_packet.get("narrative_drag", 0.0)))
        volt = min(20.0, max(0.0, physics_packet.get("voltage", 0.0)))
        current_vec = (round(drag / 10.0, 2), round(volt / 20.0, 2))
        best_fit = "THE_MUD"
        min_dist = 999.0
        for name, manifold in self.manifolds.items():
            dist = math.dist(current_vec, manifold.center_vector)
            if dist < manifold.radius and dist < min_dist:
                min_dist = dist
                best_fit = name
        
        self.current_location = best_fit # Fix: Actually update location
        
        if self.current_location != old_loc:
            return self.current_location, self.manifolds[self.current_location].entry_msg
        return self.current_location, None

    def apply_environment(self, physics_packet: dict) -> List[str]:
        manifold = self.manifolds.get(self.current_location)
        if not manifold: return []
        logs = []
        for stat, mod in manifold.modifiers.items():
            if stat in physics_packet:
                original = physics_packet[stat]
                physics_packet[stat] += mod
                if stat == "narrative_drag": physics_packet[stat] = max(0.0, physics_packet[stat])
                if stat == "voltage": physics_packet[stat] = max(0.0, physics_packet[stat])
        if self.current_location == "THE_MUD":
            logs.append(f"{Prisma.GRY}   (Environment: Drag +2.0, Voltage -2.0){Prisma.RST}")
        elif self.current_location == "THE_FORGE":
            logs.append(f"{Prisma.RED}   (Environment: Voltage +5.0){Prisma.RST}")
        return logs

    def check_anomaly(self, text: str) -> bool:
        triggers = ["glitch", "timeline", "reset", "reboot", "admin"]
        if any(t in text.lower() for t in triggers):
            return True
        return False

    def plot_course(self, target_name: str) -> list[str] | tuple[list[str], float]:
        if target_name not in self.manifolds:
            return ["ERROR: Unknown Destination"]
        start = self.manifolds.get(self.current_location, self.manifolds["THE_MUD"]).center_vector
        end = self.manifolds[target_name].center_vector
        effort = math.dist(start, end)
        cost = 5.0
        if not self.shimmer.spend(cost):
            return [f"COURSE PLOTTED to {target_name}. Warning: Low Shimmer."], 0.0
        return [f"COURSE PLOTTED to {target_name}."], 0.0

class LiteraryJournal:
    def __init__(self, output_file="journal_of_the_void.txt"):
        self.output_file = output_file
        self.reviews = NARRATIVE_DATA.get("LITERARY_REVIEWS", {
            "POSITIVE": ["Good."], "NEGATIVE": ["Bad."], "CONFUSED": ["Huh?"]
        })

    def publish(self, text, physics, bio_state):
        voltage = physics.get("voltage", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        truth = physics.get("truth_ratio", 0.0)
        if voltage > 8.0 and drag < 3.0:
            verdict = "POSITIVE"
            reward = "SEROTONIN_BOOST"
        elif drag > 5.0 or truth < 0.2:
            verdict = "NEGATIVE"
            reward = "CORTISOL_SPIKE"
        else:
            verdict = "CONFUSED"
            reward = "NONE"
        review = random.choice(self.reviews.get(verdict, ["Interesting."]))
        timestamp = time.ctime()
        entry = (
            f"\n--- ENTRY: {timestamp} ---\n"
            f"TEXT: {text}\n"
            f"METRICS: V:{voltage:.1f} | D:{drag:.1f} | Truth:{truth:.2f}\n"
            f"REVIEW: '{review}'\n"
            f"---------------------------\n")
        try:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(entry)
            return True, review, reward
        except IOError:
            return False, "The printing press is jammed.", "NONE"
