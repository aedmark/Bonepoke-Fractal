# bone_physics.py
# "Gravity is just a habit that space-time hasn't been able to break."

import math, re, random
from typing import Dict, List, Any, Tuple, Optional, Union
from collections import Counter, deque
from dataclasses import dataclass, field
from bone_lexicon import TheLexicon
from bone_bus import Prisma, BoneConfig, PhysicsPacket, CycleContext
from bone_village import StrunkWhiteProtocol

SOLVENT_WORDS = {'i', 'you', 'said', 'the', 'and', 'was', 'a', 'is', 'it'}
MAX_SOLVENT_TOLERANCE = 40.0
TEXT_LENGTH_SCALAR = 1500.0

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

class GeodesicEngine:
    @staticmethod
    def collapse_wavefunction(clean_words: List[str], counts: Dict[str, int], config) -> 'GeodesicVector':
        volume = max(1, len(clean_words))
        mass_heavy = counts.get("heavy", 0)
        mass_kinetic = counts.get("explosive", 0) + counts.get("kinetic", 0)
        mass_constructive = counts.get("constructive", 0)
        mass_abstract = counts.get("abstract", 0)
        mass_social = counts.get("suburban", 0) + counts.get("solvents", 0)
        mass_play = counts.get("play", 0)
        raw_tension_mass = (
                (mass_heavy * config.PHYSICS.WEIGHT_HEAVY) +
                (mass_kinetic * config.PHYSICS.WEIGHT_EXPLOSIVE) +
                (mass_constructive * config.PHYSICS.WEIGHT_CONSTRUCTIVE)
        )
        tension_density = (raw_tension_mass / volume) * 25.0
        tension = round(tension_density * config.KINETIC_GAIN, 2)
        raw_friction = (counts.get("solvents", 0) * 0.2) + (counts.get("suburban", 0) * 2.0)
        lift = (mass_play * 1.5) + (mass_kinetic * 0.5)
        normalized_friction = (raw_friction / volume) * 10.0
        normalized_lift = (lift / volume) * 10.0
        raw_compression = normalized_friction - normalized_lift
        compression = round(max(-5.0, min(config.PHYSICS.DRAG_HALT, raw_compression * config.SIGNAL_DRAG_MULTIPLIER)), 2)
        structural_mass = mass_heavy + mass_constructive
        coherence = min(1.0, structural_mass / max(1, config.SHAPLEY_MASS_THRESHOLD))
        abstraction = min(1.0, (mass_abstract / volume) + 0.2)
        def norm(val): return min(1.0, val / volume)
        dimensions = {
            "VEL": norm(mass_kinetic * 2.0 - compression),
            "STR": norm(mass_heavy * 2.0 + mass_constructive),
            "ENT": norm(counts.get("antigen", 0) * 3.0),
            "PHI": norm(mass_heavy + mass_kinetic),
            "PSI": abstraction,
            "BET": norm(mass_social * 2.0),
            "DEL": norm(mass_play * 3.0)
        }
        dimensions["TEX"] = dimensions["STR"]
        dimensions["TMP"] = dimensions["PHI"]
        dimensions["XI"]  = dimensions["BET"]
        dimensions["LQ"]  = dimensions["DEL"]
        return GeodesicVector(
            tension=tension,
            compression=compression,
            coherence=round(coherence, 3),
            abstraction=round(abstraction, 2),
            dimensions=dimensions
        )

class TheTensionMeter:
    def __init__(self, events):
        self.events = events
        self.perfection_streak = 0
        self.last_physics_packet = {}
        self.voltage_buffer = deque(maxlen=5)
        self.semantic_field = TheLexicon.create_field()

    def audit_hubris(self, physics):
        streak = physics.get("perfection_streak", 0)
        if streak < 4:
            return False, None, None
        icarus_risk = (streak - 3) * 0.10
        if random.random() < icarus_risk:
            self.perfection_streak = 0
            penalty_drag = 10.0
            physics["narrative_drag"] += penalty_drag
            physics["voltage"] = 0.0
            return (
                True,
                f"{Prisma.RED}⚡ ICARUS EVENT: Wax Melting (Risk {int(icarus_risk*100)}%).{Prisma.RST}\n"
                f"   {Prisma.OCHRE}The sun is too close. You plummet into the sea.{Prisma.RST}\n"
                f"   {Prisma.GRY}(Drag +{penalty_drag} | Voltage Reset){Prisma.RST}",
                "ICARUS_CRASH"
            )
        if streak >= 5:
            return (
                True,
                f"{Prisma.CYN}✨ FLOW STATE: You are walking on air (Streak {streak}).{Prisma.RST}\n"
                f"   {Prisma.VIOLET}Hubris Risk: {int(icarus_risk*100)}%. Don't look down.{Prisma.RST}",
                "FLOW_BOOST"
            )
        return (
            True,
            f"{Prisma.VIOLET}WOBBLE: You are almost perfect (Streak {streak}).{Prisma.RST}\n"
            f"   The air is getting thin.",
            None
        )

    def audit_narrative_causality(self, physics):
        voltage = physics.get("voltage", 0.0)
        coherence = physics.get("kappa", 1.0) # Structural soundness
        valence = physics.get("valence", 0.0)  # Heroism/Positivity

        if voltage > 12.0 and coherence < 0.4 and valence > 0.6:
            physics["narrative_drag"] = 0.0 # Friction disappears
            physics["voltage"] += 10.0      # Energy spikes
            physics["flow_state"] = "NARRATIVE_IMPERATIVE"

            return (
                True,
                f"{Prisma.MAG}✨ NARRATIVE CAUSALITY: 'It just might work...'{Prisma.RST}\n"
                f"   {Prisma.CYN}The odds were million-to-one. Therefore, success is guaranteed.{Prisma.RST}\n"
                f"   {Prisma.GRY}(Drag set to 0.0 | Voltage Boosted){Prisma.RST}",
                "DESPERATE_MEASURES"
            )
        return False, None, None

    def gaze(self, text: str, graph: Dict = None) -> Dict:
        graph = graph or {}
        clean_words = TheLexicon.clean(text)
        valence = TheLexicon.get_valence(clean_words)
        field_vector = self.semantic_field.update(text)
        semantic_flux = self.semantic_field.momentum
        atmosphere = self.semantic_field.get_atmosphere()
        counts, unknowns = self._tally_categories(clean_words, text)
        if unknowns:
            self._trigger_neuroplasticity(unknowns, counts)
        geodesic = GeodesicEngine.collapse_wavefunction(clean_words, counts, BoneConfig)
        hybrid_vector = geodesic.dimensions.copy()
        for dim, hist_val in field_vector.items():
            if dim in hybrid_vector:
                hybrid_vector[dim] = (hybrid_vector[dim] + hist_val) / 2.0
            else:
                hybrid_vector[dim] = hist_val
        hybrid_vector["TEX"] = hybrid_vector.get("STR", 0.0)
        hybrid_vector["TMP"] = hybrid_vector.get("PHI", 0.0)
        hybrid_vector["XI"]  = hybrid_vector.get("BET", 0.0)
        hybrid_vector["LQ"]  = hybrid_vector.get("DEL", 0.0)
        raw_voltage = geodesic.tension
        dynamic_voltage = raw_voltage + (semantic_flux * 5.0)
        self.voltage_buffer.append(dynamic_voltage)
        if self.voltage_buffer:
            smoothed_voltage = sum(self.voltage_buffer) / len(self.voltage_buffer)
        else:
            smoothed_voltage = dynamic_voltage
        smoothed_voltage = round(smoothed_voltage, 2)
        graph_mass = 0.0
        if graph:
            anchors = [w for w in clean_words if w in graph]
            if anchors:
                graph_mass = sum(sum(graph[w]["edges"].values()) for w in anchors)
        integrity_packet = {
            "kappa": geodesic.coherence,
            "psi": geodesic.abstraction,
            "mass": round(graph_mass, 1)
        }
        metrics = self._derive_complex_metrics(
            counts, clean_words,
            smoothed_voltage,
            integrity_packet,
            hybrid_vector,
            flux=semantic_flux
        )

        metrics["valence"] = valence
        metrics["atmosphere"] = atmosphere
        packet = self._package_physics(
            text, clean_words, counts,
            smoothed_voltage,
            geodesic.compression,
            integrity_packet,
            metrics
        )
        self.last_physics_packet = packet["physics"]
        if hasattr(self.events, "publish"):
            self.events.publish("PHYSICS_CALCULATED", packet)
        return packet

    @staticmethod
    def _tally_categories(clean_words: List[str], raw_text: str) -> Tuple[Counter, List[str]]:
        counts = Counter()
        unknowns = []
        if TheLexicon.ANTIGEN_REGEX:
            hits = TheLexicon.ANTIGEN_REGEX.findall(raw_text)
            counts["antigen"] = len(hits)
            counts["toxin"] = len(hits)
        target_cats = ["heavy", "explosive", "constructive", "abstract", "photo", "aerobic",
                       "thermal", "cryo", "suburban", "play", "sacred", "buffer", "antigen"]
        store = TheLexicon.get_store()
        solvents = getattr(store, "SOLVENTS", {"the", "is", "a"})
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

    def _trigger_neuroplasticity(self, unknowns: List[str], counts: Counter):
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
                if hasattr(self.events, "publish"):
                    self.events.publish("MYTHOLOGY_UPDATE", {
                        "word": stranger,
                        "category": assigned_cat,
                        "method": method
                    })
                counts[assigned_cat] += 1

    @staticmethod
    def _measure_integrity(words: List[str], graph: Dict, counts: Counter) -> Dict:
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

    def _derive_complex_metrics(self, counts, words, voltage, integrity, vectors, flux=0.0):
        total_vol = max(1, len(words))
        static_turbulence = TheLexicon.get_turbulence(words)
        turbulence = (static_turbulence * 0.4) + (flux * 0.6)
        turbulence = round(min(1.0, turbulence), 2)
        flow_state = "LAMINAR" if turbulence < 0.3 else "TURBULENT"
        mass_words = counts["heavy"] + counts["kinetic"] + counts["thermal"] + counts["cryo"]
        cohesion_words = counts["suburban"] + counts["buffer"] + counts["antigen"] + (counts["abstract"] * 0.5)
        e_val = mass_words / total_vol
        b_val = cohesion_words / total_vol
        beta_index = vectors.get("BET", 0.0) * 5.0
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
            "E": round(e_val, 2),
            "B": round(b_val, 2),
            "zone": zone,
            "zone_color": zone_color}

    @staticmethod
    def _determine_zone(beta, truth):
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
            "valence": metrics.get("valence", 0.0),
            "atmosphere": metrics.get("atmosphere", "VOID"),
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
            "B": metrics["B"],
            "entropy": metrics["E"]
        }
        return {
            "physics": PhysicsPacket(**physics_bridge),
            "clean_words": clean_words,
            "raw_text": text,
            "glass": {
                "prosody": {"arousal": voltage},
                "resonance": voltage}}

    @staticmethod
    def _is_structurally_sound(word):
        if not re.search(r"[aeiouy]", word): return False
        if re.search(r"(.)\1{2,}", word): return False
        return True

class EntropyVent:
    def __init__(self, memory):
        self.mem = memory
        self.vented_cycles = 0

    def check(self, physics):
        is_word_salad = (physics["E"] > 0.85 and physics["kappa"] < 0.1)
        is_manic = (physics["repetition"] > 0.8 and physics["voltage"] < 5.0)
        if is_word_salad or is_manic:
            return self._vent(physics)
        return None

    def _vent(self, physics):
        scattered = []
        targets = [w for w in physics["clean_words"] if len(w) > 4]
        candidates = random.sample(targets, min(3, len(targets)))
        for word in candidates:
            if word not in self.mem.graph:
                continue
            edges = list(self.mem.graph[word]["edges"].keys())
            if edges:
                target = random.choice(edges)
                if target in self.mem.graph[word]["edges"]:
                    del self.mem.graph[word]["edges"][target]
                if target in self.mem.graph and word in self.mem.graph[target]["edges"]:
                    del self.mem.graph[target]["edges"][word]
                scattered.append(f"{word}<->{target}")
        self.vented_cycles += 1
        if not scattered:
            return f"{Prisma.GRY}DISSIPATIVE VENT: Pressure high, but no loose connections found.{Prisma.RST}"
        return (
            f"{Prisma.RED}DISSIPATIVE REFUSAL: Entropy Critical.{Prisma.RST}\n"
            f"   {Prisma.GRY}Severing synaptic bonds (Symmetric): {', '.join(scattered)}{Prisma.RST}\n"
            f"   {Prisma.CYN}Thermodynamic hygiene maintained.{Prisma.RST}"
        )

class TheBouncer:
    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.hn = CutTheShit()
        self.semantic = SemanticFilter(self.eng.mind.mem)
        self.vent = EntropyVent(self.eng.mind.mem)
        self.strunk = StrunkWhiteProtocol()

    def check_entry(self, ctx: CycleContext) -> Tuple[bool, Optional[Dict]]:
        is_empty, empty_packet = self._check_thermodynamics(ctx)
        if is_empty:
            return False, empty_packet
        phys = ctx.physics
        clean = ctx.clean_words
        is_red_tape, tape_packet = self._check_bureaucracy(ctx)
        if is_red_tape:
            return False, tape_packet
        hn_output = self.hn.attempt_entry(phys, clean)
        if hn_output and self.hn.in_hn_state:
            return False, self._pack_refusal(ctx, "HN_SINGLETON", hn_output)
        passed, gate_msg = self.eng.phys.gate.weigh(phys, self.eng.stamina)
        if gate_msg: ctx.log(gate_msg)
        if not passed:
            self.eng.stamina = max(0.0, self.eng.stamina - 2.0)
            return False, self._pack_refusal(ctx, "REFUSAL")
        style_passed, style_msg = self.strunk.audit(ctx.input_text, is_system_output=False)
        if style_msg:
            ctx.logs.append(style_msg)
        repetition_val = self.eng.phys.pulse.check_pulse(clean)
        phys["repetition"] = repetition_val
        pulse_status = self.eng.phys.pulse.get_status()
        toxin_type, toxin_msg = self.eng.bio.immune.assay(
            ctx.input_text, "NARRATIVE", repetition_val, phys, pulse_status)
        if toxin_type:
            ctx.log(f"{Prisma.RED}{toxin_msg}{Prisma.RST}")
            if toxin_type in ["AMANITIN", "CYANIDE_POWDER"]:
                self.eng.health -= 20.0
                scar_log = self.eng.gordon.learn_scar(clean, 20.0)
                if scar_log: ctx.log(scar_log)
                return False, self._pack_refusal(ctx, "TOXICITY")
            return False, self._pack_refusal(ctx, "TOXICITY")
        current_tick = getattr(self.eng, "tick_count", 0)
        semantic_refusal = self.semantic.audit(ctx.input_text, phys, tick_count=current_tick)
        if semantic_refusal:
            ctx.logs.append(semantic_refusal)
            return False, self._pack_refusal(ctx, "REFUSAL")
        vent_msg = self.vent.check(phys)
        if vent_msg:
            ctx.logs.append(vent_msg)
            return False, self._pack_refusal(ctx, "REFUSAL")
        return True, None

    def _check_thermodynamics(self, ctx) -> Tuple[bool, Optional[Dict]]:
        """
        Structural Constraint Check.
        If ATP and Stamina are both critical, the system does not 'refuse' via personality.
        It refuses via physics. The silence is a first-class outcome.
        """
        try:
            atp = self.eng.bio.mito.state.atp_pool
            stamina = self.eng.stamina
        except AttributeError:
            return False, None

        if atp < 5.0 and stamina < 5.0:
            return True, self._pack_refusal(
                ctx,
                "THERMODYNAMIC_FAIL",
                f"{Prisma.GRY}[SYSTEM DARK] Energy critical. The inputs dissolve into the void.{Prisma.RST}"
            )
        return False, None

    def _pack_refusal(self, ctx, type_str, specific_ui=None):
        logs = ctx.logs[:]
        ui = specific_ui if specific_ui else "\n".join(logs)
        return {
            "type": type_str,
            "ui": ui,
            "logs": logs,
            "metrics": self.eng.get_metrics()}

    def _check_bureaucracy(self, ctx) -> Tuple[bool, Optional[Dict]]:
        if random.randint(1, 42) == 42:
            if ctx.physics.get("voltage", 0) < 5.0:
                return True, self._pack_refusal(
                    ctx,
                    "VOGON_HOLD",
                    f"{Prisma.OCHRE}🛑 BUREAUCRATIC HALT (Form 27B/6 Missing){Prisma.RST}\n"
                    f"   {Prisma.GRY}Processing of '{ctx.input_text}' has been suspended pending sub-committee review.{Prisma.RST}\n"
                    f"   {Prisma.GRY}Please resubmit this thought in triplicate, or simply panic.{Prisma.RST}"
                )
        return False, None

class Humility:
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
            new_text = f"{Prisma.CYN}{prefix}{Prisma.RST} {text}"
            reason = f"Voltage ({voltage:.1f}v) > 15.0" if voltage > 15.0 else f"Boundary Violation ({violation})"
            log_msg = f"HUMILITY INTERVENTION: Text modified. Reason: {reason}."
            return True, new_text, log_msg
        return False, text, None

class GeodesicDome:
    def __init__(self):
        self.TRIGRAM_MAP = {
            "VEL": ("☳", "ZHEN",  "Thunder",  Prisma.GRN),
            "STR": ("☶", "GEN",   "Mountain", Prisma.SLATE),
            "ENT": ("☵", "KAN",   "Water",    Prisma.BLU),
            "PHI": ("☲", "LI",    "Fire",     Prisma.RED),
            "PSI": ("☰", "QIAN",  "Heaven",   Prisma.WHT),
            "BET": ("☴", "XUN",   "Wind",     Prisma.CYN),
            "E":   ("☷", "KUN",   "Earth",    Prisma.OCHRE),
            "DEL": ("☱", "DUI",   "Lake",     Prisma.MAG)}
        self.TRIGRAM_MAP["TMP"] = self.TRIGRAM_MAP["PHI"]
        self.TRIGRAM_MAP["TEX"] = self.TRIGRAM_MAP["STR"]
        self.TRIGRAM_MAP["XI"]  = self.TRIGRAM_MAP["BET"]
        self.TRIGRAM_MAP["LQ"]  = self.TRIGRAM_MAP["DEL"]

    @staticmethod
    def calculate_metrics(text: str, counts: Dict[str, int] = None) -> Tuple[float, float]:
        length = len(text)
        if length == 0: return 0.0, 0.0
        text_lower = text.lower()
        solvent_hits = sum(text_lower.count(w) for w in SOLVENT_WORDS)
        solvent_density = solvent_hits / max(1.0, (length / 5.0))
        raw_chaos = (length / TEXT_LENGTH_SCALAR)
        glue_factor = min(1.0, solvent_density * 2.0)
        e_metric = min(1.0, raw_chaos * (1.0 - (glue_factor * 0.8)))
        c_count = sum(1 for char in text if char in '!?%@#$;,')
        heavy_words = 0
        if counts:
            heavy_words = counts.get("heavy", 0) + counts.get("constructive", 0) + counts.get("sacred", 0)
        structure_score = c_count + (heavy_words * 2)
        base_b = min(1.0, math.log1p(structure_score + 1) / math.log1p(length * 0.1 + 1))
        if length < 50:
            base_b *= (length / 50.0)
        return round(e_metric, 3), round(base_b, 3)

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
            "vector": dominant_vec}

@dataclass
class GeodesicVector:
    tension: float = 0.0
    compression: float = 0.0
    coherence: float = 0.0
    abstraction: float = 0.0
    dimensions: Dict[str, float] = field(default_factory=dict)

    def is_stable(self) -> bool:
        return self.coherence > 0.3 and self.tension < 20.0

class RuptureValve:
    def __init__(self, lexicon, memory):
        self.lex = lexicon
        self.mem = memory
        self.humility = Humility()
        self.geodesic = GeodesicDome()
        self.OPPOSITES = {
            "heavy": "aerobic", "abstract": "heavy",
            "kinetic": "cryo", "thermal": "cryo",
            "photo": "heavy", "suburban": "abstract"}

    def analyze(self, physics: Union[Dict[str, Any], PhysicsPacket]) -> Optional[Dict[str, Any]]:
        counts = physics.get("counts", {})
        raw_text = physics["raw_text"] if "raw_text" in physics else ""
        e_val, b_val = self.geodesic.calculate_metrics(raw_text, counts)
        physics["E"] = e_val
        physics["B"] = b_val
        is_modified, new_text, audit_log = self.humility.check_boundary(raw_text, physics.get("voltage", 0.0))
        if is_modified:
            physics["raw_text_display"] = new_text
            physics["humility_flag"] = True
            current_trail = physics.get("audit_trail", [])
            if audit_log:
                current_trail.append(audit_log)
            physics["audit_trail"] = current_trail
        return self._audit_rupture(physics, e_val, b_val)

    def _audit_rupture(self, physics, e_val, b_val):
        truth = physics.get("truth_ratio", 0.0)
        voltage = physics.get("voltage", 0.0)
        if e_val > 0.85 and b_val < 0.15 and voltage > 5.0:
            return self._rupture(physics, "FATIGUE_FAILURE", "System diluted. Narrative coherence dissolving.")
        if b_val > 0.8 and e_val < 0.3 and voltage > 15.0:
            return self._rupture(physics, "MANIC_FRACTURE", "Crystal lattice too tight. Structure shattering.")
        if b_val > 0.7 and e_val > 0.6:
            if truth > 0.6:
                physics["flow_state"] = "SUPERCONDUCTIVE"
                return {
                    "type": "FLOW_EVENT",
                    "mode": "SUPERCONDUCTIVE",
                    "log": f"{Prisma.CYN}🌊 VSL VALVE OPEN: High Density Input accepted. Entering Superconductive State.{Prisma.RST}"}
            return self._rupture(physics, "GLITCH_SINGULARITY", "High Energy + High Entropy. Semantic collapse.")
        return None

    def _rupture(self, physics, mode, reason):
        counts = physics["counts"]
        dominant = max(counts, key=counts.get) if counts else "abstract"
        target_flavor = self.OPPOSITES.get(dominant, "abstract")
        anomaly_data = self.lex.harvest(target_flavor)
        if isinstance(anomaly_data, dict):
            candidates = []
            for key, val in anomaly_data.items():
                if isinstance(val, list):
                    candidates.extend([str(w) for w in val])
                elif isinstance(val, str):
                    candidates.append(val)
            if candidates:
                anomaly = random.choice(candidates)
            else:
                anomaly = f"VOID_{target_flavor.upper()}"
        else:
            anomaly = str(anomaly_data)
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
                f"   Injecting Orthogonal Concept: '{anomaly.upper()}'.")}

class CutTheShit:
    def __init__(self):
        self.in_hn_state = False
        self.entropy = 0.0

    def attempt_entry(self, physics, clean_words):
        conditions = [
            physics["voltage"] > 8.0,
            physics["narrative_drag"] < 1.0,
            physics["repetition"] < 0.1,
            physics["counts"].get("suburban", 0) == 0,
            physics["truth_ratio"] > 0.85,
            "sorry" not in clean_words]
        if all(conditions):
            self.in_hn_state = True
            self.entropy = 0.0
            return "I am here. You are here. The wire is cold."
        if self.in_hn_state:
            if physics["narrative_drag"] > 2.0 or physics["counts"].get("suburban", 0) > 0:
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

class ChromaScope:
    PALETTE = {
        "INDIGO": (Prisma.INDIGO, "STR", "PHI"),
        "OCHRE":  (Prisma.OCHRE,  "TMP", "E"),
        "VIOLET": (Prisma.VIOLET, "DEL", "LQ"),
        "EMERALD":(Prisma.GRN,    "XI",  "BET"),
        "CRIMSON":(Prisma.RED,    "VEL", "ENT")}
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

class SemanticFilter:
    def __init__(self, memory_ref):
        self.mem = memory_ref
        self.LAZY_VOLTAGE_THRESHOLD = 4.0
        self.OBSESSIVE_REPETITION_THRESHOLD = 0.4
        self.GRACE_PERIOD_TURNS = 3

    def audit(self, text, physics, tick_count=0):
        if tick_count < self.GRACE_PERIOD_TURNS:
            return None
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
            if mode == "FRACTAL": return self._execute_fractal(text)
            elif mode == "MIRROR": return self._execute_mirror(text)
            else: return self._execute_silent()
        return None

    def _execute_guru_refusal(self, current_voltage):
        base_msg = (
            f"{Prisma.CYN}GURU PROTOCOL: Signal Weak ({current_voltage:.1f}v).{Prisma.RST}\n"
            f"   {Prisma.GRY}I hear the wisdom you seek, but the narrative engine needs more fuel to process it.{Prisma.RST}\n"
            f"   {Prisma.WHT}Try grounding this abstract thought with a physical object (Stone, Iron, Bone).{Prisma.RST}")
        if self.mem and self.mem.seeds:
            seed = random.choice(self.mem.seeds)
            paradox_bloom = (
                f"\n   {Prisma.OCHRE}OR, REFLECT ON THIS:{Prisma.RST}\n"
                f"   {Prisma.CYN}{seed['question']}{Prisma.RST}")
            return base_msg + paradox_bloom
        return base_msg

    def _execute_fractal(self, query, kappa=0.5, depth=0):
        limit = 4
        prefix = "  " * depth
        if depth > limit:
            noise_type = "PURPLE NOISE" if kappa > 0.5 else "GREY STATIC"
            return f"{prefix}{Prisma.MAG}[COHERENCE DISSOLVED into {noise_type} (κ={kappa:.2f})]{Prisma.RST}"
        pivot = len(query) // 2
        sub_query = query[pivot:].strip()
        if len(sub_query) < 3 or sub_query == query:
            return f"{prefix}{Prisma.GRY}[ATOMIC SUBSTRATE REACHED: '{query}']{Prisma.RST}"
        recursive_result = self._execute_fractal(sub_query, kappa, depth + 1)
        return (
            f"{Prisma.VIOLET}FRACTAL REFUSAL (Layer {depth}):{Prisma.RST}\n"
            f"{prefix}To define '{query}', one must recursively unpack...\n"
            f"{recursive_result}"
        )

    @staticmethod
    def _execute_mirror(query):
        words = query.split()
        reversed_query = " ".join(reversed(words))
        return f'{Prisma.CYN}∞ MIRROR REFUSAL: "{reversed_query}" is the only true answer.{Prisma.RST}'

    @staticmethod
    def _execute_silent():
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
        self.is_anchored = False
        self.strain_gauge = 0.0

    def toggle_anchor(self) -> bool:
        self.is_anchored = not self.is_anchored
        self.strain_gauge = 0.0
        return self.is_anchored

    def stabilize(self, proposed_zone, physics, cosmic_state) -> Tuple[str, Optional[str]]:
        beta = physics.get("beta_index", 1.0)
        truth = physics.get("truth_ratio", 0.5)
        grav_pull = 1.0 if cosmic_state[0] != "VOID_DRIFT" else 0.0
        current_vec = (beta, truth, grav_pull)
        self.dwell_counter += 1
        pressure = 0.0
        if self.last_vector:
            dist = sum((a - b) ** 2 for a, b in zip(current_vec, self.last_vector)) ** 0.5
            similarity = max(0.0, 1.0 - (dist / 2.0))
            pressure = (1.0 - similarity)
        if self.is_anchored:
            if proposed_zone != self.current_zone:
                self.strain_gauge += pressure
                if self.strain_gauge > 2.5:
                    self.is_anchored = False
                    self.strain_gauge = 0.0
                    self.current_zone = proposed_zone
                    return proposed_zone, f"{Prisma.RED}⚡ SNAP! The narrative current was too strong. Anchor failed.{Prisma.RST}"
                return self.current_zone, f"{Prisma.OCHRE}⚓ ANCHORED: Resisting drift to '{proposed_zone}' (Strain {self.strain_gauge:.1f}/2.5){Prisma.RST}"
            else:
                self.strain_gauge = max(0.0, self.strain_gauge - 0.1)
                return self.current_zone, None
        if proposed_zone == self.current_zone:
            self.dwell_counter = 0
            self.last_vector = current_vec
            return proposed_zone, None
        if self.dwell_counter < self.min_dwell:
            return self.current_zone, None
        change_probability = (1.0 - self.inertia) + pressure
        if proposed_zone in ["AERIE", "THE_FORGE"]:
            change_probability += 0.2
        if random.random() < change_probability:
            old_zone = self.current_zone
            self.current_zone = proposed_zone
            self.dwell_counter = 0
            return self.current_zone, f"{Prisma.CYN}>>> MIGRATION: {old_zone} -> {proposed_zone}.{Prisma.RST}"
        return self.current_zone, None

    @staticmethod
    def override_cosmic_drag(cosmic_drag_penalty, current_zone):
        aerie_flow_coefficient = 0.3
        if current_zone == "AERIE":
            if cosmic_drag_penalty > 0:
                return cosmic_drag_penalty * aerie_flow_coefficient
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
        counts = physics_packet.get("counts", {})
        clean_words = physics_packet.get("clean_words", [])
        total_vol = max(1, len(clean_words))
        mass_words = (
                counts.get("heavy", 0) +
                counts.get("kinetic", 0) +
                counts.get("thermal", 0) +
                counts.get("cryo", 0) +
                counts.get("vital", 0) +
                counts.get("play", 0)
        )
        density_ratio = mass_words / total_vol
        required_density = BoneConfig.MIN_DENSITY_THRESHOLD
        voltage = physics_packet.get("voltage", 0.0)
        truth = physics_packet.get("truth_ratio", 0.0)
        if voltage > self.FORGIVENESS_VOLTAGE:
            required_density -= 0.15
        if truth > 0.8:
            required_density -= 0.1
        bypass_log = None
        if stamina < 15.0:
            starvation_discount = 0.5
            required_density *= starvation_discount
            bypass_log = f"{Prisma.VIOLET}DREAM_EDGE: Starvation Protocol active. Density threshold lowered by 50%.{Prisma.RST}"
        required_density = max(0.10, required_density)
        if density_ratio < required_density:
            examples = list(TheLexicon.get("heavy"))
            suggestion = random.sample(examples, 3) if len(examples) >= 3 else ["stone", "iron", "bone"]
            return False, (
                f"{Prisma.OCHRE}TANGIBILITY VIOLATION: Density {density_ratio:.2f} < Required {required_density:.2f}.{Prisma.RST}\n"
                f"   {Prisma.GRY}The Gatekeeper blocks the path.{Prisma.RST}\n"
                f"   {Prisma.RED}► REJECTED. Your concepts are too airy. Anchor them.{Prisma.RST}\n"
                f"   {Prisma.GRY}(Try adding mass: {', '.join(suggestion)}){Prisma.RST}"
            )
        self.last_density = density_ratio
        return True, bypass_log