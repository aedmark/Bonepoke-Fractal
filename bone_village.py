# bone_village.py
# "It takes a village... to raise a simulation."

import json, os, random, re, time, string, unicodedata, math
from collections import Counter, deque
from typing import List, Dict, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from bone_bus import Prisma, BoneConfig, CycleContext
from bone_lexicon import TheLexicon
from bone_personality import UserProfile, PublicParksDepartment, ZenGarden
from bone_council import CouncilChamber

try:
    from bone_data import (
        LEXICON, GENETICS, DEATH, NARRATIVE_DATA, RESONANCE,
        ALMANAC_DATA, STYLE_CRIMES, ITEM_GENERATION, TheAkashicRecord
    )
except ImportError:
    LEXICON = {"solvents": ["the", "is"]}
    GENETICS = {}
    DEATH = {}
    NARRATIVE_DATA = {}
    RESONANCE = {}
    ITEM_GENERATION = {}
    class TheAkashicRecord:
        def __init__(self): pass
        @staticmethod
        def forge_new_item(vec): return "GLITCH_ARTIFACT", {}

class TheTinkerer:
    def __init__(self, gordon_ref, events_ref):
        self.gordon = gordon_ref
        self.events = events_ref
        self.tool_confidence = {}
        self.akashic = TheAkashicRecord()

    def audit_tool_use(self, physics_packet, inventory_list, host_health: Any = None):
        if isinstance(physics_packet, dict):
            voltage = physics_packet.get("voltage", 0.0)
            drag = physics_packet.get("narrative_drag", 0.0)
            vector = physics_packet.get("vector", {})
        else:
            voltage = physics_packet.voltage
            drag = physics_packet.narrative_drag
            vector = getattr(physics_packet, "vector", {})
        real_drag = 0.0
        real_efficiency = 1.0
        if host_health:
            real_drag = max(0.0, host_health.latency - 2.0)
            real_efficiency = host_health.efficiency_index
        effective_drag = drag + (real_drag * 2.0)
        is_forge = (voltage > 12.0 and real_efficiency > 0.9) or (effective_drag < 2.0)
        is_mud = (voltage < 5.0) and (effective_drag > 6.0)
        learning_rate = 0.05
        rust_rate = 0.02
        ascension_threshold = 2.5
        items_to_shed = []
        for item_name in inventory_list:
            if item_name not in self.tool_confidence:
                self.tool_confidence[item_name] = 1.0
            current = self.tool_confidence[item_name]
            if is_forge:
                self.tool_confidence[item_name] = min(3.0, current + learning_rate)
                if self.tool_confidence[item_name] >= ascension_threshold:
                    self._attempt_ascension(item_name, inventory_list, vector)
                elif random.random() < 0.1:
                    self.events.log(f"{Prisma.CYN}[TINKER]: {item_name} is tempering (Eff: {real_efficiency:.2f}).{Prisma.RST}", "SYS")
            elif is_mud:
                self.tool_confidence[item_name] = max(0.0, current - rust_rate)
                if random.random() < 0.1:
                    reason = "Damp Narrative" if drag > 4.0 else "System Lag"
                    self.events.log(f"{Prisma.OCHRE}[TINKER]: {item_name} is rusting ({reason}).{Prisma.RST}", "SYS")
            if self.tool_confidence[item_name] <= 0.1:
                items_to_shed.append(item_name)
        for item in items_to_shed:
            if item in inventory_list:
                inventory_list.remove(item)
            if item in self.tool_confidence:
                del self.tool_confidence[item]
            self.events.log(f"{Prisma.GRY}[TINKER]: {item} disintegrated. Gordon failed to maintain it.{Prisma.RST}", "SYS")
        for item_name in inventory_list:
            if item_name in self.tool_confidence:
                self._mutate_tool_stats(item_name, self.tool_confidence[item_name])

    def _attempt_ascension(self, old_name, inventory_list, vector):
        if "OF_" in old_name and " " in old_name:
            return
        new_name, new_data = self.akashic.forge_new_item(vector)
        if old_name in inventory_list:
            inventory_list.remove(old_name)
            inventory_list.append(new_name)
        self.gordon.ITEM_REGISTRY[new_name] = new_data
        self.tool_confidence[new_name] = 1.0
        if old_name in self.tool_confidence:
            del self.tool_confidence[old_name]
        self.events.log(f"{Prisma.MAG}✨ ASCENSION: '{old_name}' has evolved into '{new_name}'!{Prisma.RST}", "AKASHIC")

    def _mutate_tool_stats(self, item_name, confidence):
        item_data = self.gordon.ITEM_REGISTRY.get(item_name)
        if not item_data: return
        if "value" in item_data:
            if "base_value" not in item_data:
                item_data["base_value"] = item_data["value"]
            new_value = item_data["base_value"] * confidence
            item_data["value"] = round(new_value, 2)
        if confidence > 1.5 and "LUCKY" not in item_data.get("passive_traits", []):
            if "passive_traits" not in item_data: item_data["passive_traits"] = []
            item_data["passive_traits"].append("LUCKY")
            self.events.log(f"{Prisma.CYN}✨ TRAIT GAINED: {item_name} is now [LUCKY].{Prisma.RST}", "TINKER")

    def save_state(self): return self.tool_confidence

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
        if not physics: return "MAP ERROR: No Physics Data", []
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

class TheAlmanac:
    def __init__(self):
        self.forecasts = ALMANAC_DATA.get("FORECASTS", {"BALANCED": ["System nominal."]})
        self.strategies = ALMANAC_DATA.get("STRATEGIES", {})
        self.default_seed = ALMANAC_DATA.get("DEFAULT_SEED", "Observe.")

    def diagnose_condition(self, session_data: dict, host_health: Any = None) -> Tuple[str, str]:
        meta = session_data.get("meta", {})
        trauma = session_data.get("trauma_vector", {})
        final_health = meta.get("final_health", 0)
        final_stamina = meta.get("final_stamina", 0)
        condition = "BALANCED"
        advice = "System nominal."
        real_latency = 0.0
        real_entropy = 1.0
        if host_health:
            real_latency = host_health.latency
            real_entropy = host_health.entropy
        max_trauma = max(trauma, key=trauma.get) if trauma else "NONE"
        trauma_val = trauma.get(max_trauma, 0)

        if real_latency > 5.0:
            condition = "HIGH_DRAG"
            advice = f"Host Latency High ({real_latency:.1f}s). Simplify syntax to reduce load."
        elif real_entropy < 0.3:
            condition = "HIGH_ENTROPY"
            advice = "Loop detected. The host is stuck in a rut. Inject chaos."
        elif final_health < 30 or trauma_val > 0.6:
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
        return self.strategies.get(condition, self.default_seed)

    def compile_forecast(self, session_data: dict, host_health: Any = None) -> str:
        condition, advice = self.diagnose_condition(session_data, host_health)
        available_forecasts = self.forecasts.get(condition, self.forecasts.get("BALANCED", ["Standard Operation."]))
        forecast_text = random.choice(available_forecasts)
        seed_text = self.get_seed(condition)
        border = f"{Prisma.OCHRE}{'='*40}{Prisma.RST}"
        report = [
            "\n", border,
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
            border, "\n"
        ]
        return "\n".join(report)

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
            "DEL": min(1.0, 0.5 + (d("play") * 2.0) + (d("unknown") * 1.5)),
            "XI":  min(1.0, (d("suburban") + d("buffer")) * 2.0),
            "BET": min(1.0, d("suburban") + d("buffer")),
            "E":   min(1.0, (d("solvents") * 0.4)),
            "LQ":  min(1.0, d("passive_watch") + d("mirror"))}

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
            return {"title": "THE FRACTAL BLOOM", "color": Prisma.VIOLET, "desc": "Boredom Threshold exceeded. Entropy is high.", "context": "CHAOS"}
        if station:
            role_color = Prisma.CYN
            if station[0] == "GORDON": role_color = Prisma.OCHRE
            elif station[0] == "SHERLOCK": role_color = Prisma.INDIGO
            elif station[0] == "JESTER": role_color = Prisma.VIOLET
            return {"title": station[2].upper().replace('THE ', 'THE '), "color": role_color, "desc": station[1], "context": station[0]}
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
    def __init__(self, events=None):
        self.events = events
        self.stats = {"WAR": 0.0, "ART": 0.0, "LAW": 0.0, "ROT": 0.0}
        self.dominant_archetype = "NEUTRAL"
        self.active_mode = True
        self.profile = UserProfile()
        if self.events:
            self.events.subscribe("PHYSICS_CALCULATED", self.on_physics_update)

    def on_physics_update(self, packet: dict):
        if not self.active_mode: return
        text = packet.get("raw_text", "")
        physics_data = packet.get("physics")
        if physics_data: self.profile_input(text, physics_data)
        mods = self.get_reflection_modifiers()
        if mods.get("flavor") and self.events:
            self.events.log(f"{Prisma.CYN}🪞 {mods['flavor']}{Prisma.RST}", "MIRROR")

    def profile_input(self, text: str, physics: Any):
        if isinstance(physics, dict):
            counts = physics.get("counts", {})
            clean_words = physics.get("clean_words", [])
            vol = physics.get("voltage", 0.0)
            drag = physics.get("narrative_drag", 0.0)
            turbulence = physics.get("turbulence", 0)
            psi = physics.get("psi", 0.0)
        else:
            counts = getattr(physics, "counts", {})
            clean_words = getattr(physics, "clean_words", [])
            vol = getattr(physics, "voltage", 0.0)
            drag = getattr(physics, "narrative_drag", 0.0)
            turbulence = getattr(physics, "turbulence", 0)
            psi = getattr(physics, "psi", 0.0)
        if hasattr(self, 'profile'):
            self.profile.update(counts, len(clean_words))
        decay = 0.05
        for k in self.stats: self.stats[k] = max(0.0, self.stats[k] - decay)
        if vol > 12.0 or "!" in text: self.stats["WAR"] = min(1.0, self.stats["WAR"] + 0.2)
        if psi > 0.6 or "?" in text: self.stats["ART"] = min(1.0, self.stats["ART"] + 0.2)
        if drag < 2.0 and vol < 5.0: self.stats["LAW"] = min(1.0, self.stats["LAW"] + 0.2)
        if text.startswith("/"): self.stats["LAW"] = min(1.0, self.stats["LAW"] + 0.1)
        if turbulence > 0.5: self.stats["ROT"] = min(1.0, self.stats["ROT"] + 0.2)
        self.dominant_archetype = max(self.stats, key=self.stats.get)

    def reflect(self, physics: Any) -> Tuple[bool, Optional[str]]:
        if isinstance(physics, dict): text = physics.get("raw_text", "")
        else: text = getattr(physics, "raw_text", "")
        self.profile_input(text, physics)
        mods = self.get_reflection_modifiers()
        if mods.get("flavor"): return True, mods["flavor"]
        return False, None

    def get_reflection_modifiers(self) -> Dict:
        top_stat = self.dominant_archetype
        intensity = self.stats[top_stat]
        mods = {"drag_mult": 1.0, "plasticity": 1.0, "loot_chance": 1.0, "atp_tax": 0.0, "voltage_cap": 20.0, "flavor": ""}
        if intensity < 0.3: return mods
        if top_stat == "WAR":
            mods["drag_mult"] = 1.5
            mods["loot_chance"] = 2.0
            mods["atp_tax"] = 5.0
            mods["flavor"] = f"{Prisma.RED}[MIRROR]: Aggression detected (High Voltage). (Drag UP, Loot UP){Prisma.RST}"
        elif top_stat == "ART":
            mods["plasticity"] = 2.0
            mods["drag_mult"] = 0.5
            mods["voltage_cap"] = 10.0
            mods["flavor"] = f"{Prisma.CYN}[MIRROR]: Abstract thought detected (Questions/Psi). (Plasticity UP, Voltage Capped){Prisma.RST}"
        elif top_stat == "LAW":
            mods["drag_mult"] = 0.8
            mods["loot_chance"] = 0.0
            mods["plasticity"] = 0.2
            mods["flavor"] = f"{Prisma.GRY}[MIRROR]: Order detected (Low Drag). Deviation is prohibited. (Stability UP, Loot ZERO){Prisma.RST}"
        elif top_stat == "ROT":
            mods["plasticity"] = 0.5
            mods["drag_mult"] = 1.2
            mods["atp_tax"] = 2.0
            mods["flavor"] = f"{Prisma.VIOLET}[MIRROR]: Entropy rising (Turbulence). Logic integrity failing. (Chaos UP){Prisma.RST}"
        return mods

    def render_report(self):
        def bar(v, color): return f"{color}{'█' * int(v * 10)}{'░' * (10 - int(v * 10))}{Prisma.RST}"
        return (
            f"WAR [{self.stats['WAR']:.2f}] {bar(self.stats['WAR'], Prisma.RED)}\n"
            f"ART [{self.stats['ART']:.2f}] {bar(self.stats['ART'], Prisma.CYN)}\n"
            f"LAW [{self.stats['LAW']:.2f}] {bar(self.stats['LAW'], Prisma.WHT)}\n"
            f"ROT [{self.stats['ROT']:.2f}] {bar(self.stats['ROT'], Prisma.VIOLET)}")

class StrunkWhiteProtocol:
    """
    Polices the style of the narrative.
    Refactored to distinguish between User (Advisory) and System (Mandatory).
    """
    def __init__(self):
        self.PATTERNS = STYLE_CRIMES["PATTERNS"]

    def audit(self, text: str, is_system_output: bool = True) -> tuple[bool, str]:
        """
        Check for 'Style Crimes'.
        If is_system_output is True, returns False on detection (Strict).
        If is_system_output is False, returns True on detection but adds a warning (Advisory).
        """
        if "delve" in text.lower() or "tapestry" in text.lower():
            if is_system_output:
                return False, f"{Prisma.RED}FORBIDDEN VOCAB: 'Delve' and 'Tapestry' are banned artifacts.{Prisma.RST}"
            else:
                return True, f"{Prisma.YEL}STYLE OBSERVATION: 'Delve' and 'Tapestry' are forbidden artifacts. Try 'Explore' or 'Weave'.{Prisma.RST}"
        for crime in self.PATTERNS:
            if re.search(crime["regex"], text):
                msg = crime['error_msg']
                if is_system_output:
                    return False, f"STYLE CRIME ({crime['name']}): {msg}"
                else:
                    return True, f"{Prisma.GRY}STYLE NOTE ({crime['name']}): {msg} (Proceeding...){Prisma.RST}"
        return True, "Clean"

    def sanitize(self, text: str) -> tuple[str, str | None]:
        is_clean, msg = self.audit(text, is_system_output=True)
        if not is_clean:
            return text, msg
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
            return "IGNITED", f"HEAP IGNITION ({int(score * 100)}%): The Ancestors are speaking.",
        return "INERT", f"⏳ INERT SAND ({int(score*100)}%): Building mass..."

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
                f"{Prisma.OCHRE}THE MUD: The ground is sticky. Movement costs double.{Prisma.RST}"),
            "THE_FORGE": Manifold(
                "THE_FORGE", (0.1, 0.9), 0.2,
                "Low Fatigue, High Tension (Transformation)",
                {"voltage": 5.0, "narrative_drag": -1.0, "psi": -0.1},
                f"{Prisma.RED}THE FORGE: Sparks fly. Your words are heating up.{Prisma.RST}"),
            "THE_AERIE": Manifold(
                "THE_AERIE", (0.2, 0.1), 0.2,
                "Low Fatigue, Low Tension (Abstraction)",
                {"narrative_drag": -3.0, "psi": 0.3, "voltage": -1.0},
                f"{Prisma.CYN}THE AERIE: The air is thin. Concepts float freely here.{Prisma.RST}"),
            "THE_GLITCH": Manifold(
                "THE_GLITCH", (0.9, 0.9), 0.1,
                "High Fatigue, High Tension (Collapse)",
                {"turbulence": 0.5, "beta_index": 2.0},
                f"{Prisma.VIOLET}THE GLITCH: Reality is buffering...{Prisma.RST}"),
            "THE_GARDEN": Manifold(
                "THE_GARDEN", (0.5, 0.5), 0.3,
                "Balanced State (Integration)",
                {"kappa": 0.2, "truth_ratio": 0.1},
                f"{Prisma.GRN}THE GARDEN: The soil is rich. Roots go deep.{Prisma.RST}")}

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
            f"{Prisma.GRY}Nearby Manifolds:{Prisma.RST}"]
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

    def locate(self, physics_packet: dict, host_health: Any = None) -> Tuple[str, Optional[str]]:
        old_loc = self.current_location
        if self.check_anomaly(physics_packet.get("raw_text", "")):
            self.current_location = "THE_GLITCH"
            if old_loc != "THE_GLITCH":
                return self.current_location, self.manifolds["THE_GLITCH"].entry_msg
            return self.current_location, None

        narrative_drag = physics_packet.get("narrative_drag", 0.0)

        if host_health:
            real_drag = max(0.0, host_health.latency - 2.0)
            narrative_drag += (real_drag * 1.5)

        drag = min(10.0, max(0.0, narrative_drag))
        volt = min(20.0, max(0.0, physics_packet.get("voltage", 0.0)))

        current_vec = (round(drag / 10.0, 2), round(volt / 20.0, 2))
        best_fit = "THE_MUD"
        min_dist = 999.0

        for name, manifold in self.manifolds.items():
            dist = math.dist(current_vec, manifold.center_vector)
            if dist < manifold.radius and dist < min_dist:
                min_dist = dist
                best_fit = name

        self.current_location = best_fit
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

@dataclass
class ReviewResult:
    critic_name: str
    score: float
    verdict: str
    reward_type: str
    reward_amount: float
    breakdown: List[str]

class LiteraryJournal:
    def __init__(self, output_file="journal_of_the_void.txt"):
        self.output_file = output_file
        try:
            from bone_data import NARRATIVE_DATA
            self.critics = NARRATIVE_DATA.get("LITERARY_CRITICS", {})
        except ImportError:
            self.critics = {}
        if not self.critics:
            self.critics = {
                "DEFAULT": {
                    "name": "The Void",
                    "preferences": {"voltage": 1.0},
                    "reviews": {"high": ["Acceptable."], "low": ["Silence."]}
                }
            }

    def _calculate_score(self, physics: Dict, preferences: Dict) -> Tuple[float, List[str]]:
        score = 50.0
        breakdown = []
        metrics = {
            "voltage": physics.get("voltage", 0),
            "narrative_drag": physics.get("narrative_drag", 0),
            "kappa": physics.get("kappa", 0),
            "psi": physics.get("psi", 0),
            "truth_ratio": physics.get("truth_ratio", 0),
            "velocity": physics.get("vector", {}).get("VEL", 0)
        }
        counts = physics.get("counts", {})
        for k, v in counts.items():
            metrics[f"counts_{k}"] = v
        for trait, weight in preferences.items():
            val = metrics.get(trait, 0)
            impact = 0.0
            if trait == "narrative_drag":
                if weight < 0: # Critic hates drag
                    if val < 2.0: impact = 15.0
                    elif val > 5.0: impact = -15.0
                else:
                    impact = (val * weight) * 2
            else:
                impact = (val * weight) * 5.0
            score += impact
            sign = "+" if impact >= 0 else ""
            breakdown.append(f"{trait}({val:.1f}) x {weight} = {sign}{impact:.1f}")
        return max(0.0, min(100.0, score)), breakdown

    def publish(self, text, physics, bio_state) -> ReviewResult:
        critic_key = random.choice(list(self.critics.keys()))
        critic = self.critics[critic_key]
        score, breakdown = self._calculate_score(physics, critic["preferences"])
        reward_type = "NONE"
        reward_amount = 0.0
        review_text = ""
        if score >= 80:
            review_text = random.choice(critic["reviews"]["high"])
            reward_type = "ATP_BOOST"
            reward_amount = 25.0
        elif score >= 50:
            review_text = "It has potential, but lacks conviction."
            reward_type = "STAMINA_REGEN"
            reward_amount = 10.0
        else:
            review_text = random.choice(critic["reviews"]["low"])
            reward_type = "CORTISOL_SPIKE"
            reward_amount = 5.0
        timestamp = time.ctime()
        entry = (
            f"\n--- REVIEW: {timestamp} ---\n"
            f"CRITIC: {critic['name']}\n"
            f"TEXT: {text}\n"
            f"SCORE: {score:.1f}/100\n"
            f"VERDICT: '{review_text}'\n"
            f"---------------------------\n")
        try:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except IOError:
            pass
        return ReviewResult(
            critic_name=critic['name'],
            score=score,
            verdict=review_text,
            reward_type=reward_type,
            reward_amount=reward_amount,
            breakdown=breakdown
        )

class TownHall:
    Lexicon = TheLexicon
    Almanac = TheAlmanac
    CycleContext = CycleContext
    Journal = LiteraryJournal
    Cartographer = TheCartographer
    Navigator = TheNavigator
    Manifold = Manifold
    PublicParksDepartment = PublicParksDepartment
    ZenGarden = ZenGarden
    Tinkerer = TheTinkerer
    ParadoxSeed = ParadoxSeed
    DeathGen = DeathGen
    Apeirogon = ApeirogonResonance
    Mirror = MirrorGraph
    Sorites = SoritesIntegrator
    Akashic = TheAkashicRecord
    Projector = TheHoloProjector
    StrunkWhite = StrunkWhiteProtocol
    CouncilChamber = CouncilChamber