# bone_lexicon.py - The Global Dictionary

import json
import random
import re
import string
import time
import unicodedata
from typing import Tuple, Dict

from bone_bus import BoneConfig, Prisma
from bone_data import LEXICON, GENETICS


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

    @property
    def STORE(self):
        return self._STORE


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