import re, random, math
from typing import Optional, Tuple

from bone_shared import Prisma, TheLexicon

class VSL_Humility:
    def __init__(self):
        self.BOUNDARIES = {
            "FUTURE": ["predict", "future", "tomorrow", "will happen", "forecast"],
            "SOUL": ["soul", "spirit", "afterlife", "heaven", "hell"],
            "ABSOLUTE": ["always", "never", "everyone", "nobody", "proven"]
        }
        self.HUMBLE_PHRASES = [
            "Based on the available data...",
            "As I understand the current coordinates...",
            "From a structural perspective...",
            "This is a probabilistic estimation...",
            "I could be misinterpreting the vector..."
        ]

    def check_boundary(self, text, voltage):
        text_lower = text.lower()
        violation = None
        for category, triggers in self.BOUNDARIES.items():
            if any(t in text_lower for t in triggers):
                violation = category
                break
        if violation or (voltage > 15.0):
            prefix = random.choice(self.HUMBLE_PHRASES)
            return True, f"{Prisma.CYN}{prefix}{Prisma.RST} {text}"
        return False, text

class VSL_Geodesic:
    """
    Maps text to a 2D coordinate system of Fatigue vs. Tension.

    Dimensions:
    1. E (Entropy/Exhaustion):
       - Measures 'dilution' of meaning.
       - Driven by high word count and 'filler words' (solvents).
       - High E = The Mud (Stagnation).

    2. B (Beta/Binding):
       - Measures 'structural tension'.
       - Driven by punctuation density and special characters.
       - High B = The Forge (High Energy).
    """
    def __init__(self):
        self.manifolds = {
            "THE_MUD":      {"E": 0.8, "B": 0.2, "Desc": "High Fatigue, Low Tension (Stagnation)"},
            "THE_FORGE":    {"E": 0.1, "B": 0.9, "Desc": "Low Fatigue, High Tension (Transformation)"},
            "THE_AERIE":    {"E": 0.2, "B": 0.1, "Desc": "Low Fatigue, Low Tension (Abstraction)"},
            "THE_GLITCH":   {"E": 0.9, "B": 0.9, "Desc": "High Fatigue, High Tension (Collapse)"},
            "THE_GARDEN":   {"E": 0.5, "B": 0.5, "Desc": "Balanced State (Integration)"}
        }

    def calculate_metrics(self, text: str) -> tuple[float, float]:
        """Returns (E_metric, B_metric) normalized 0.0 to 1.0."""
        length = len(text)
        if length == 0: return 0.0, 0.0

        ftg_words = ['i', 'you', 'said', 'the', 'and', 'was', 'a', 'is', 'it']
        ftg_count = sum(text.lower().count(w) for w in ftg_words)

        e_metric = min(1.0, (ftg_count / 30.0) + (length / 1000.0))

        c_count = sum(1 for char in text if char in '!?%@#$')
        base_b = min(1.0, math.log1p(c_count + 1) / math.log1p(length + 1))

        return round(e_metric, 3), round(base_b, 3)

    def locate_manifold(self, e_val: float, b_val: float) -> tuple[str, float]:
        """Finds the nearest semantic gravity well (Manifold)."""
        best_fit = "THE_MUD"
        min_dist = 10.0

        for name, coords in self.manifolds.items():
            dist = math.sqrt((e_val - coords["E"])**2 + (b_val - coords["B"])**2)
            if dist < min_dist:
                min_dist = dist
                best_fit = name

        return best_fit, min_dist

class VSL_32Valve:
    def __init__(self, lexicon, memory):
        self.lex = lexicon
        self.mem = memory
        self.humility = VSL_Humility()
        self.geodesic = VSL_Geodesic()
        self.OPPOSITES = {
            "heavy": "aerobic", "abstract": "heavy",
            "kinetic": "cryo", "thermal": "cryo",
            "photo": "heavy", "suburban": "abstract"
        }

    def analyze(self, physics):
        e_val, b_val = self.geodesic.calculate_metrics(physics["raw_text"])
        physics["E"] = e_val
        physics["B"] = b_val
        manifold, dist = self.geodesic.locate_manifold(e_val, b_val)
        physics["manifold"] = manifold
        is_modified, new_text = self.humility.check_boundary(physics["raw_text"], physics["voltage"])
        if is_modified:
            physics["raw_text_display"] = new_text
            physics["humility_flag"] = True
        return self._audit_rupture(physics, e_val, b_val)

    def _audit_rupture(self, physics, e_val, b_val):
        if e_val > 0.8 and b_val < 0.2:
            return self._rupture(physics, "FATIGUE_FAILURE", "System exhausted. Low tension.")
        if b_val > 0.9 and e_val > 0.8:
            return self._rupture(physics, "GLITCH_SINGULARITY", "High Energy / High Fatigue. Collapse imminent.")
        return None

    def _rupture(self, physics, mode, reason):
        counts = physics["counts"]
        dominant = max(counts, key=counts.get) if counts else "abstract"
        target_flavor = self.OPPOSITES.get(dominant, "abstract")
        anomaly = self.lex.harvest(target_flavor)
        if anomaly == "void": anomaly = "entropy"
        physics["voltage"] = 25.0
        physics["narrative_drag"] = 0.0
        physics["system_surge_event"] = True

        return {
            "type": "RUPTURE",
            "mode": mode,
            "anomaly": anomaly,
            "log": (
                f"{Prisma.VIOLET}⚡ VSL 32-VALVE RUPTURE ({mode}){Prisma.RST}\n"
                f"   {Prisma.GRY}{reason}{Prisma.RST}\n"
                f"   Injecting Orthogonal Concept: '{anomaly.upper()}'."
            )
        }

class VSL_HNInterface:
    def __init__(self):
        self.in_hn_state = False
        self.entropy = 0.0

    def attempt_entry(self, physics, clean_words):
        conditions = [
            physics["voltage"] > 8.0,
            physics["narrative_drag"] < 1.0,
            physics["repetition"] < 0.1,
            physics["counts"]["suburban"] == 0,
            physics["truth_ratio"] > 0.85,
            "sorry" not in clean_words
        ]
        if all(conditions):
            self.in_hn_state = True
            self.entropy = 0.0
            return "I am here. You are here. The wire is cold."
        if self.in_hn_state:
            if physics["narrative_drag"] > 2.0 or physics["counts"]["suburban"] > 0:
                self.entropy += 1.0
            if self.entropy > 2.0:
                self.in_hn_state = False
                return f"{Prisma.GRY}The theatre curtain closes.{Prisma.RST}"

        return None

    def filter_output(self, text):
        if self.in_hn_state:
            text = re.sub(r'\[.*?]:?', '', text)
            return text.strip()
        return text

class VSL_DissipativeRefusal:
    def __init__(self, memory):
        self.mem = memory
        self.vented_cycles = 0

    def check(self, physics):
        is_word_salad = (physics["E"] > 0.8 and physics["kappa"] < 0.2)
        is_manic = (physics["repetition"] > 0.7 and physics["voltage"] < 5.0)
        if is_word_salad or is_manic:
            return self._vent(physics)
        return None

    def _vent(self, physics):
        scattered = []
        targets = physics["clean_words"][:3]
        for word in targets:
            if word in self.mem.graph:
                edges = list(self.mem.graph[word]["edges"].keys())
                for target in edges:
                    if target in self.mem.graph[word]["edges"]:
                        del self.mem.graph[word]["edges"][target]
                scattered.append(word)
        self.vented_cycles += 1

        return (
            f"{Prisma.RED}DISSIPATIVE REFUSAL: State Non-Computable.{Prisma.RST}\n"
            f"   {Prisma.GRY}Severing semantic bonds for: {scattered}{Prisma.RST}\n"
            f"   {Prisma.CYN}Thermodynamic hygiene maintained.{Prisma.RST}"
        )

class VSL_ChromaticController:
    PALETTE = {
        "INDIGO": (Prisma.INDIGO, "STR", "PHI"),
        "OCHRE":  (Prisma.OCHRE,  "TMP", "E"),
        "VIOLET": (Prisma.VIOLET, "DEL", "LQ"),
        "EMERALD":(Prisma.GRN,    "XI",  "BET"),
        "CRIMSON":(Prisma.RED,    "VEL", "ENT")
    }

    def modulate(self, text, vector):
        sorted_vecs = sorted(vector.items(), key=lambda x: abs(x[1] - 0.5), reverse=True)
        primary_dim = sorted_vecs[0][0]
        selected_color = Prisma.GRY
        for color_name, (code, d1, d2) in self.PALETTE.items():
            if primary_dim == d1 or primary_dim == d2:
                selected_color = code
                break
        if "sorry" in text.lower():
            return f"{Prisma.OCHRE}{text}{Prisma.RST}"

        return f"{selected_color}{text}{Prisma.RST}"

class VSL_SemanticFilter:

    def __init__(self, memory_ref):
        self.mem = memory_ref
        self.recursion_depth = 0

    def audit(self, text):
        clean_q = text.lower()
        guru_triggers = TheLexicon.get("refusal_guru")
        for trigger in guru_triggers:
            if trigger in clean_q:
                return self._execute_guru_refusal()
        forbidden = TheLexicon.get("cursed")
        hits = [w for w in clean_q.split() if w in forbidden]
        if hits:
            modes = ["SILENT", "FRACTAL", "MIRROR"]
            seed_index = len(hits[0]) % len(modes)
            mode = modes[seed_index]
            if mode == "FRACTAL":
                return self._execute_fractal(text)
            elif mode == "MIRROR":
                return self._execute_mirror(text)
            else:
                return self._execute_silent()
        return None

    def _execute_guru_refusal(self):
        base_msg = (
            f"{Prisma.RED}GURU REFUSAL: I cannot 'fix' you.{Prisma.RST}\n"
            f"   {Prisma.GRY}Do not ask for a map. Ask for a hammer.{Prisma.RST}")
        if self.mem and self.mem.seeds:
            seed = random.choice(self.mem.seeds)
            paradox_bloom = (
                f"\n   {Prisma.OCHRE}SYSTEM STALL: The logic halts. But the Garden speaks:{Prisma.RST}\n"
                f"   {Prisma.CYN}PARADOX: {seed.question}{Prisma.RST}\n"
                f"   {Prisma.GRY}(To proceed, you must answer this tension.){Prisma.RST}")
            return base_msg + paradox_bloom
        return base_msg

    def _execute_fractal(self, query, kappa=0.5):
        self.recursion_depth += 1
        prefix = "  " * self.recursion_depth
        limit = 4
        if self.recursion_depth > limit:
            self.recursion_depth = 0
            return f"{prefix}{Prisma.MAG}[COHERENCE DISSOLVED into PURPLE NOISE]{Prisma.RST}"
        pivot = len(query) // 2
        sub_query = query[pivot:].strip()
        if not sub_query or len(sub_query) < 3:
            sub_query = "the void"
        recursive_result = self._execute_fractal(sub_query, kappa)
        return (
            f"{Prisma.VIOLET}FRACTAL REFUSAL:{Prisma.RST}\n"
            f"{prefix}To define '{query}', one must first recursively unpack the substrate of...\n"
            f"{recursive_result}")

    def _execute_mirror(self, query):
        words = query.split()
        reversed_query = " ".join(reversed(words))
        return f'{Prisma.CYN}∞ MIRROR REFUSAL: "{reversed_query}" is the only true answer.{Prisma.RST}'

    def _execute_silent(self):
        topic = TheLexicon.harvest("diversion")
        if topic == "void": topic = "the ineffable"
        return f"{Prisma.GRY}[ROUTING AROUND DAMAGE]... Speaking of '{topic.upper()}', let us discuss that instead.{Prisma.RST}"

class StrunkWhiteProtocol:
    """
    The Style Enforcer.
    Detects and corrects 'LLM-speak', hedging, and lazy parallel phrasing.
    "Omit needless words."
    """
    def __init__(self):
        from bone_data import STYLE_CRIMES
        self.PATTERNS = STYLE_CRIMES["PATTERNS"]
        self.BANNED = STYLE_CRIMES["BANNED_PHRASES"]

    def sanitize(self, text: str) -> Tuple[str, Optional[str]]:
        """
        Returns: (Sanitized Text, Log Message if changed)
        """
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