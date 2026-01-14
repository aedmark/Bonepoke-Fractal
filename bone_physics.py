# bone_physics.py - The Laws of Nature
# "Gravity is just a habit that space-time hasn't been able to break."

import math, re, random
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass, field

from bone_village import Prisma, BoneConfig, TheLexicon, CycleContext

SOLVENT_WORDS = {'i', 'you', 'said', 'the', 'and', 'was', 'a', 'is', 'it'}
MAX_SOLVENT_TOLERANCE = 30.0
TEXT_LENGTH_SCALAR = 1000.0

# --- THE DATA STRUCTURE ---

@dataclass
class PhysicsPacket:
    voltage: float = 0.0
    narrative_drag: float = 0.0
    repetition: float = 0.0
    clean_words: List[str] = field(default_factory=list)
    counts: Dict[str, int] = field(default_factory=dict)
    vector: Dict[str, float] = field(default_factory=dict)
    psi: float = 0.0
    kappa: float = 0.0
    geodesic_mass: float = 0.0
    beta_index: float = 1.0
    gamma: float = 0.0
    turbulence: float = 0.0
    flow_state: str = "LAMINAR"
    zone: str = "COURTYARD"
    zone_color: str = "OCHRE"
    truth_ratio: float = 0.0
    raw_text: str = ""
    antigens: int = 0
    perfection_streak: int = 0
    avg_viscosity: float = 0.0
    E: float = 0.0
    B: float = 0.0
    humility_flag: bool = False
    system_surge_event: bool = False
    pain_signal: float = 0.0
    manifold: str = "THE_MUD"

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def update(self, data: Dict):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__annotations__}

# --- THE CALCULATOR ---

class PhysicsResolver:
    @staticmethod
    def calculate_voltage(counts: dict, config) -> float:
        # Pinker: Explicit variable names replace "magic" multipliers
        heavy = counts.get("heavy", 0)
        explosive = counts.get("explosive", 0)
        constructive = counts.get("constructive", 0)
        
        # Using the new Physics Constitution
        raw_charge = (
            (heavy * config.PHYSICS.WEIGHT_HEAVY) + 
            (explosive * config.PHYSICS.WEIGHT_EXPLOSIVE) + 
            (constructive * config.PHYSICS.WEIGHT_CONSTRUCTIVE)
        )
        
        final_voltage = raw_charge * config.KINETIC_GAIN
        return round(final_voltage, 2)

    @staticmethod
    def calculate_drag(clean_words: List, counts: dict, config) -> float:
        volume = max(1, len(clean_words))
        solvents = counts.get("solvents", 0)
        suburban = counts.get("suburban", 0)
        play = counts.get("play", 0)
        
        # Friction Logic
        friction = (solvents * 1.0) + (suburban * 2.5)
        lift = play * 1.5
        
        net_drag = max(0.0, friction - lift)
        normalized_drag = (net_drag / volume) * 10.0
        final_drag = normalized_drag * config.SIGNAL_DRAG_MULTIPLIER
        
        # Using the config cap
        # Schur: "The universe has a speed limit."
        return round(min(config.PHYSICS.DRAG_HALT, final_drag), 2)

    @staticmethod
    def derive_vector_matrix(counts: dict, total_vol: int, voltage: float, drag: float) -> dict:
        safe_vol = max(1, total_vol)
        def d(cat): return counts.get(cat, 0) / safe_vol
        
        # The 12 Dimensions of the VSL
        return {
            "VEL": min(1.0, 0.5 + (d("explosive") * 2.0) + (d("kinetic") * 1.0) - (drag * 0.05)),
            "STR": min(1.0, 0.5 + (d("heavy") * 2.0) + (d("constructive") * 1.5)),
            "ENT": min(1.0, 0.5 + (d("antigen") * 3.0) + (d("toxin") * 2.0)),
            "TEX": min(1.0, 0.5 + (d("heavy") * 0.5) + (d("abstract") * 1.0)),
            "TMP": min(1.0, 0.5 + (d("thermal") * 2.0) - (d("cryo") * 2.0) + (voltage * 0.02)),
            "PHI": min(1.0, (d("heavy") + d("kinetic")) / max(1, d("abstract") + d("heavy"))), # Truth Ratio approximation
            "PSI": min(1.0, 0.5 + (d("abstract") * 2.0)),
            "DEL": min(1.0, 0.5 + (d("play") * 2.0) + (d("unknown") * 1.5)),
            "XI":  min(1.0, (d("suburban") + d("buffer")) * 2.0), # Complexity/Noise
            "BET": min(1.0, d("suburban") + d("buffer")),
            "E":   min(1.0, (d("solvents") * 0.4)),
            "LQ":  min(1.0, d("passive_watch") + d("mirror"))
        }

# --- THE SENSORS ---

class TheTensionMeter:
    """
    The Eye of the System. 
    It looks at the text and collapses the wave function into numbers.
    """
    def __init__(self, events):
        self.events = events
        self.perfection_streak = 0
        self.last_physics_packet = {}

    def audit_hubris(self, physics, lexicon_class):
        streak = physics.get("perfection_streak", 0)
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
        graph = graph or {} 
        clean_words = TheLexicon.clean(text)
        counts, unknowns = self._tally_categories(clean_words, text)
        
        # Neuroplasticity: Learn new words on the fly if voltage is high enough
        if unknowns:
            self._trigger_neuroplasticity(unknowns, counts, text)
        
        # Calculate Base Metrics
        voltage = PhysicsResolver.calculate_voltage(counts, BoneConfig)
        drag = PhysicsResolver.calculate_drag(clean_words, counts, BoneConfig)
        integrity = self._measure_integrity(clean_words, graph, counts)
        vectors = PhysicsResolver.derive_vector_matrix(counts, len(clean_words), voltage, drag)
        
        # Derive Complex Metrics (Zone, Flow State, Gamma)
        metrics = self._derive_complex_metrics(
            counts, clean_words, voltage, drag, integrity, vectors)
            
        # Package it up
        packet = self._package_physics(text, clean_words, counts, voltage, drag, integrity, metrics)

        self.last_physics_packet = packet["physics"] 
        return packet

    def _tally_categories(self, clean_words: List[str], raw_text: str) -> Tuple[Counter, List[str]]:
        counts = Counter()
        unknowns = []
        
        # 1. Regex checks (Antigens)
        if TheLexicon.ANTIGEN_REGEX:
            hits = TheLexicon.ANTIGEN_REGEX.findall(raw_text)
            counts["antigen"] = len(hits)
            counts["toxin"] = len(hits)
            
        target_cats = ["heavy", "explosive", "constructive", "abstract", "photo", "aerobic",
                       "thermal", "cryo", "suburban", "play", "sacred", "buffer", "antigen"]
        
        # 2. Iterate words
        solvents = getattr(TheLexicon._STORE, "SOLVENTS", {"the", "is", "a"})
        for w in clean_words:
            if w in solvents:
                counts["solvents"] += 1
                continue
            
            found = False
            # Check known lists
            for cat in target_cats:
                if w in TheLexicon.get(cat):
                    counts[cat] += 1
                    found = True
            
            # If not found, try the phonetic "taster"
            if not found:
                flavor, confidence = TheLexicon.taste(w)
                if flavor and confidence > 0.5:
                    counts[flavor] += 1
                else:
                    unknowns.append(w)
        return counts, unknowns

    def _trigger_neuroplasticity(self, unknowns: List[str], counts: Counter, raw_text: str):
        voltage = (counts["heavy"] * 2.0) + (counts["kinetic"] * 1.5)
        # Only learn if the user is putting in effort (Voltage > 5.0)
        if voltage > 5.0 and unknowns:
            dominant_cat = max(counts, key=counts.get) if counts else "kinetic"
            for stranger in unknowns:
                if len(stranger) < 3:
                    continue
                if not self._is_structurally_sound(stranger):
                    # Gibberish check, but High Voltage overrides syntax rules
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
        """
        Measures the structural strength of the thought based on connections in the graph.
        """
        if not words:
            return {"kappa": 0.0, "psi": 0.0, "mass": 0.0}
            
        anchors = [w for w in words if w in graph]
        # Mass = sum of edge weights
        mass = sum(sum(graph[w]["edges"].values()) for w in anchors)
        
        # Artificial Mass (Constructive words create temporary scaffolding)
        artificial_mass = counts["constructive"] * 0.5
        
        # Kappa: Structural Integrity (0.0 to 1.0)
        kappa = min(1.0, (mass + artificial_mass) / BoneConfig.SHAPLEY_MASS_THRESHOLD)
        
        # Psi: Abstract/Metaphysical Integrity
        total = len(words)
        abstract_count = counts["abstract"]
        heavy_count = counts["heavy"]
        psi = min(1.0, (abstract_count / total) + 0.2)
        
        # Adjustment: Heavy words ground the abstract ones
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
        
        # Gamma: The "Surface Tension" of the narrative
        bond_strength = max(0.1, integrity["kappa"] + (repetition_score * 0.5))
        voltage_load = max(0.1, voltage / 10.0)
        gamma = round((bond_strength * avg_viscosity) / (1.0 + voltage_load), 2)
        gamma = max(0.01, gamma)
        
        # Perfection Streak Logic (The Hubris Mechanic)
        if truth_ratio > 0.85 and voltage > BoneConfig.PHYSICS.VOLTAGE_HIGH:
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
            "physics": PhysicsPacket(**physics_bridge), # Using the Dataclass now!
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

# --- THE GATEKEEPERS & SYSTEMS ---

class TheBouncer:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.hn = VSL_HNInterface()
        self.semantic = VSL_SemanticFilter(self.eng.mind.mem)
        self.vent = VSL_DissipativeRefusal(self.eng.mind.mem)

    def check_entry(self, ctx: CycleContext) -> Tuple[bool, Optional[Dict]]:
        phys = ctx.physics
        clean = ctx.clean_words
        
        # 1. HN Interface Check
        hn_output = self.hn.attempt_entry(phys, clean)
        if hn_output and self.hn.in_hn_state:
            return False, self._pack_refusal(ctx, "HN_SINGLETON", hn_output)
            
        # 2. Tangibility Check (Do you have enough mass?)
        passed, gate_msg = self.eng.phys.gate.weigh(phys, self.eng.stamina)
        if gate_msg: ctx.log(gate_msg)
        if not passed:
            self.eng.stamina = max(0.0, self.eng.stamina - 2.0)
            return False, self._pack_refusal(ctx, "REFUSAL")
            
        # 3. Toxicity Check
        repetition_val = self.eng.phys.pulse.check_pulse(clean)
        phys["repetition"] = repetition_val 
        pulse_status = self.eng.phys.pulse.get_status()
        
        toxin_type, toxin_msg = self.eng.bio.immune.assay(
            ctx.input_text, "NARRATIVE", repetition_val, phys, pulse_status
        )
        if toxin_type:
            ctx.log(f"{Prisma.RED}{toxin_msg}{Prisma.RST}")
            if toxin_type in ["AMANITIN", "CYANIDE_POWDER"]:
                self.eng.health -= 20.0
                scar_log = self.eng.gordon.learn_scar(clean, 20.0)
                if scar_log: ctx.log(scar_log)
                return False, self._pack_refusal(ctx, "TOXICITY")
            return False, self._pack_refusal(ctx, "TOXICITY")
            
        # 4. Semantic Filter
        semantic_refusal = self.semantic.audit(ctx.input_text, phys)
        if semantic_refusal:
            ctx.logs.append(semantic_refusal)
            return False, self._pack_refusal(ctx, "REFUSAL")
            
        # 5. Dissipative Vent
        vent_msg = self.vent.check(phys)
        if vent_msg:
            ctx.logs.append(vent_msg)
            return False, self._pack_refusal(ctx, "REFUSAL")
            
        return True, None

    def _pack_refusal(self, ctx, type_str, specific_ui=None):
        logs = ctx.logs[:] 
        ui = specific_ui if specific_ui else "\n".join(logs)
        return {
            "type": type_str,
            "ui": ui,
            "logs": logs,
            "metrics": self.eng._get_metrics()
        }

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
    def __init__(self):
        self.manifolds = {
            "THE_MUD":      {"E": 0.8, "B": 0.2, "Desc": "High Fatigue, Low Tension (Stagnation)"},
            "THE_FORGE":    {"E": 0.1, "B": 0.9, "Desc": "Low Fatigue, High Tension (Transformation)"},
            "THE_AERIE":    {"E": 0.2, "B": 0.1, "Desc": "Low Fatigue, Low Tension (Abstraction)"},
            "THE_GLITCH":   {"E": 0.9, "B": 0.9, "Desc": "High Fatigue, High Tension (Collapse)"},
            "THE_GARDEN":   {"E": 0.5, "B": 0.5, "Desc": "Balanced State (Integration)"}
        }

        self.TRIGRAM_MAP = {
            "VEL": ("☳", "ZHEN",  "Thunder",  Prisma.GRN),
            "STR": ("☶", "GEN",   "Mountain", Prisma.SLATE),
            "ENT": ("☵", "KAN",   "Water",    Prisma.BLU),
            "PHI": ("☲", "LI",    "Fire",     Prisma.RED),
            "PSI": ("☰", "QIAN",  "Heaven",   Prisma.WHT),
            "BET": ("☴", "XUN",   "Wind",     Prisma.CYN),
            "E":   ("☷", "KUN",   "Earth",    Prisma.OCHRE),
            "DEL": ("☱", "DUI",   "Lake",     Prisma.MAG)
        }
        self.TRIGRAM_MAP["TMP"] = self.TRIGRAM_MAP["PHI"]
        self.TRIGRAM_MAP["TEX"] = self.TRIGRAM_MAP["STR"]
        self.TRIGRAM_MAP["XI"]  = self.TRIGRAM_MAP["BET"]
        self.TRIGRAM_MAP["LQ"]  = self.TRIGRAM_MAP["DEL"]

    def calculate_metrics(self, text: str) -> Tuple[float, float]:
        length = len(text)
        if length == 0: return 0.0, 0.0
        text_lower = text.lower()
        solvent_count = sum(text_lower.count(w) for w in SOLVENT_WORDS)
        e_metric = min(1.0, (solvent_count / MAX_SOLVENT_TOLERANCE) + (length / TEXT_LENGTH_SCALAR))
        c_count = sum(1 for char in text if char in '!?%@#$')
        base_b = min(1.0, math.log1p(c_count + 1) / math.log1p(length + 1))
        return round(e_metric, 3), round(base_b, 3)

    def locate_manifold(self, e_val: float, b_val: float) -> Tuple[str, float]:
        best_fit = "THE_MUD"
        min_dist = 10.0
        for name, coords in self.manifolds.items():
            dist = math.sqrt((e_val - coords["E"])**2 + (b_val - coords["B"])**2)
            if dist < min_dist:
                min_dist = dist
                best_fit = name
        return best_fit, min_dist

    def resolve_trigram(self, vector: Dict[str, float]) -> Dict[str, Any]:
        if not vector:
            return {"symbol": "☷", "name": "KUN", "color": Prisma.OCHRE, "vector": "E"}
        dominant_vec = max(vector, key=vector.get)
        if vector[dominant_vec] < 0.2:
            dominant_vec = "E"
        symbol, name, concept, color = self.TRIGRAM_MAP.get(dominant_vec, self.TRIGRAM_MAP["E"])
        return {
            "symbol": symbol,
            "name": name,
            "concept": concept,
            "color": color,
            "vector": dominant_vec
        }

class VSL_32Valve:
    def __init__(self, lexicon, memory):
        self.lex = lexicon
        self.mem = memory
        self.humility = VSL_Humility()
        self.geodesic = VSL_Geodesic()
        self.OPPOSITES = {
            "heavy": "aerobic", "abstract": "heavy",
            "kinetic": "cryo", "thermal": "cryo",
            "photo": "heavy", "suburban": "abstract"}

    def analyze(self, physics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # VSL-specific metrics
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
        if e_val > 0.75 and b_val < 0.15:
            return self._rupture(physics, "FATIGUE_FAILURE", "System diluted. Narrative coherence dissolving.")
        if b_val > 0.8 and e_val < 0.3:
            return self._rupture(physics, "MANIC_FRACTURE", "Crystal lattice too tight. Structure shattering.")
        if b_val > 0.7 and e_val > 0.6:
            return self._rupture(physics, "GLITCH_SINGULARITY", "High Energy + High Entropy. Semantic collapse.")
        return None

    def _rupture(self, physics, mode, reason):
        counts = physics["counts"]
        dominant = max(counts, key=counts.get) if counts else "abstract"
        target_flavor = self.OPPOSITES.get(dominant, "abstract")
        anomaly = self.lex.harvest(target_flavor)
        if anomaly == "void":
            anomaly = "something_completely_different"
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
        self.LAZY_VOLTAGE_THRESHOLD = 8.0
        self.OBSESSIVE_REPETITION_THRESHOLD = 0.4

    def audit(self, text, physics):
        clean_q = text.lower()
        guru_triggers = TheLexicon.get("refusal_guru")
        voltage = physics.get("voltage", 0.0)
        for trigger in guru_triggers:
            if trigger in clean_q:
                if voltage > self.LAZY_VOLTAGE_THRESHOLD:
                    return None
                return self._execute_guru_refusal(voltage)
        forbidden = TheLexicon.get("cursed")
        hits = [w for w in clean_q.split() if w in forbidden]
        repetition = physics.get("repetition", 0.0)
        if hits:
            if repetition < self.OBSESSIVE_REPETITION_THRESHOLD and voltage > 5.0:
                return None
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

    def _execute_guru_refusal(self, current_voltage):
        base_msg = (
            f"{Prisma.RED}GURU REFUSAL: Voltage Low ({current_voltage:.1f}v).{Prisma.RST}\n"
            f"   {Prisma.GRY}I cannot 'fix' you when the signal is this weak.{Prisma.RST}\n"
            f"   {Prisma.WHT}Try again with heavier words.{Prisma.RST}")
        if self.mem and self.mem.seeds:
            seed = random.choice(self.mem.seeds)
            paradox_bloom = (
                f"\n   {Prisma.OCHRE}INSTEAD, CONSIDER THIS SEED:{Prisma.RST}\n"
                f"   {Prisma.CYN}PARADOX: {seed.question}{Prisma.RST}")
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

class ZoneInertia:
    def __init__(self, inertia=0.7, min_dwell=2):
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
        if current_zone == "AERIE" and cosmic_drag_penalty > 0:
            return cosmic_drag_penalty * 0.3
        return cosmic_drag_penalty
        
class CosmicDynamics:
    @staticmethod
    def analyze_orbit(network, clean_words):
        if not clean_words or not network.graph:
            return "VOID_DRIFT", 3.0, "VOID: Deep Space. No connection."
        gravity_wells = {}
        geodesic_hubs = {}
        for node in network.graph:
            mass = network.calculate_mass(node)
            if mass >= BoneConfig.GRAVITY_WELL_THRESHOLD:
                gravity_wells[node] = mass
            elif mass >= BoneConfig.GEODESIC_STRENGTH:
                geodesic_hubs[node] = mass
        basin_pulls = {k: 0.0 for k in gravity_wells}
        active_filaments = 0
        for w in clean_words:
            if w in gravity_wells:
                basin_pulls[w] += gravity_wells[w] * 2.0
                active_filaments += 1
            for well in gravity_wells:
                if w in network.graph.get(well, {}).get("edges", {}):
                    basin_pulls[well] += gravity_wells[well] * 0.5
                    active_filaments += 1
        total_pull = sum(basin_pulls.values())
        if total_pull == 0:
            for w in clean_words:
                if w in geodesic_hubs:
                    return "PROTO_COSMOS", 1.0, f"NEBULA: Floating near '{w.upper()}' (Mass {int(geodesic_hubs[w])}). Not enough mass for orbit."
            return "VOID_DRIFT", 3.0, "VOID: Drifting outside the filaments."
        sorted_basins = sorted(basin_pulls.items(), key=lambda x: x[1], reverse=True)
        primary_node, primary_str = sorted_basins[0]
        if len(sorted_basins) > 1:
            secondary_node, secondary_str = sorted_basins[1]
            if secondary_str > 0 and (primary_str - secondary_str) < BoneConfig.LAGRANGE_TOLERANCE:
                return (
                    "LAGRANGE_POINT",
                    0.0,
                    f"LAGRANGE: Caught between '{primary_node.upper()}' and '{secondary_node.upper()}'")
        flow_ratio = active_filaments / max(1, len(clean_words))
        if flow_ratio > 0.5 and primary_str < (BoneConfig.GRAVITY_WELL_THRESHOLD * 2):
            return (
                "WATERSHED_FLOW",
                0.0,
                f"FLOW: Streaming towards '{primary_node.upper()}'")
        return "ORBITAL", 0.0, f"ORBIT: Circling '{primary_node.upper()}' (Mass {int(gravity_wells[primary_node])})"

class TheTangibilityGate:
    FORGIVENESS_VOLTAGE = BoneConfig.PHYSICS.VOLTAGE_LOW + 1.0
    def __init__(self):
        self.last_density = 0.0

    def weigh(self, physics_packet: dict, stamina: float) -> tuple:
        if stamina < 15.0:
            return True, f"{Prisma.VIOLET}DREAM_EDGE: Starvation bypass. Tangibility ignored.{Prisma.RST}"

        counts = physics_packet.get("counts", {})
        clean_words = physics_packet.get("clean_words", [])
        total_vol = max(1, len(clean_words))

        # Calculate Density (Mass / Volume)
        mass_words = (
                counts.get("heavy", 0) +
                counts.get("kinetic", 0) +
                counts.get("thermal", 0) +
                counts.get("cryo", 0) +
                counts.get("vital", 0) +
                counts.get("play", 0))

        density_ratio = mass_words / total_vol
        voltage = physics_packet.get("voltage", 0.0)
        truth = physics_packet.get("truth_ratio", 0.0)

        required_density = BoneConfig.MIN_DENSITY_THRESHOLD 
        
        modifier = 1.0
        if voltage > self.FORGIVENESS_VOLTAGE:
            modifier -= 0.2
        if truth > 0.8:
            modifier -= 0.1

        required_density *= modifier
        
        # The Hard Floor 
        required_density = max(0.15, required_density)

        if density_ratio < required_density:
            gas_words = counts.get("abstract", 0) + counts.get("antigen", 0)
            
            examples = list(TheLexicon.get("heavy")) 
            suggestion = random.sample(examples, 3) if len(examples) >= 3 else ["stone", "iron", "bone"]

            return False, (
                f"{Prisma.OCHRE}TANGIBILITY VIOLATION: Density {density_ratio:.2f} < Required {required_density:.2f}.{Prisma.RST}\n"
                f"   {Prisma.GRY}The Gatekeeper blocks the path.{Prisma.RST}\n"
                f"   {Prisma.RED}► REJECTED. Your concepts are too airy. Anchor them.{Prisma.RST}\n"
                f"   {Prisma.GRY}(Try adding mass: {', '.join(suggestion)}){Prisma.RST}")

        self.last_density = density_ratio
        return True, None
