# bone_biology.py

import math
import time
import random
from collections import deque
from dataclasses import dataclass, field
from typing import Any
from bone_shared import Prisma, TheLexicon, BoneConfig

@dataclass
class MetabolicReceipt:
    base_cost: float
    drag_tax: float
    inefficiency_tax: float
    total_burn: float
    status: str
    symptom: str = "Nominal"

@dataclass
class MitochondrialState:
    atp_pool: float = 100.0
    ros_buildup: float = 0.0
    membrane_potential: float = -150.0
    mother_hash: str = "MITOCHONDRIAL_EVE_001"
    efficiency_mod: float = 1.0
    ros_resistance: float = 1.0
    enzymes: set = field(default_factory=set)
    telomeres: int = 105

class MitochondrialForge:
    BASE_BMR = 2.0
    APOPTOSIS_TRIGGER = "CYTOCHROME_C_RELEASE"
    MAX_ATP = 200.0

    def __init__(self, lineage_seed: str, events, inherited_traits: dict = None):
        self.state = MitochondrialState(mother_hash=lineage_seed)
        self.events = events
        self.krebs_cycle_active = True

        # Pinker: Generalized inheritance logic
        if inherited_traits:
            self._apply_inheritance(inherited_traits)

    def _apply_inheritance(self, traits):
        self.state.efficiency_mod = traits.get("efficiency_mod", 1.0)
        self.state.ros_resistance = traits.get("ros_resistance", 1.0)
        if "enzymes" in traits:
            self.state.enzymes = set(traits["enzymes"])
            self.events.log(f"{Prisma.CYN}[MITO]: Inherited Enzymes: {list(self.state.enzymes)}.{Prisma.RST}")

    def calculate_metabolism(self, drag: float, external_modifiers: list[float] = None) -> MetabolicReceipt:
        """
        Fuller: Refactored for 'Safe Math' and system independence.
        'external_modifiers' is a list of floats (e.g., [0.5, 0.8]) representing buffs/debuffs.
        """
        bmr = self.BASE_BMR

        # Fuller: Soft-Capped Quadratic Curve
        # Keeps the punishment for high drag, but prevents 'Math Death' at extreme values.
        # Logic: drag^1.5 is replaced by a curve that asymptotically approaches a max burn rate.
        safe_drag = min(drag, 20.0) # Hard cap input to prevent overflow
        drag_tax = (safe_drag * safe_drag) / 10.0  # Quadratic but divided. 5.0 drag -> 2.5 tax. 10.0 drag -> 10.0 tax.

        # Apply External Modifiers (Inventory, Genetics, etc.)
        # This decouples the biology from the inventory system.
        if external_modifiers:
            for mod in external_modifiers:
                drag_tax *= mod

        raw_cost = bmr + drag_tax

        # Efficiency acts as a divisor (High efficiency = Lower cost)
        # We ensure efficiency never drops to zero to avoid DivideByZero errors.
        safe_efficiency = max(0.1, self.state.efficiency_mod)
        final_cost = raw_cost / safe_efficiency

        # Calculate waste heat (inefficiency tax)
        inefficiency = 0.0
        if safe_efficiency < 1.0:
            inefficiency = final_cost - raw_cost

        # Schur: Determine Status and Symptom
        status = "RESPIRING"
        symptom = "Humming along."

        if final_cost > self.state.atp_pool:
            status = "NECROSIS"
            symptom = f"The engine is stalling. Requires {final_cost:.1f} ATP."
        elif self.state.ros_buildup > BoneConfig.CRITICAL_ROS_LIMIT:
            status = self.APOPTOSIS_TRIGGER
            symptom = "Cellular suicide initiated. Too much noise."
        elif drag_tax > 5.0:
            symptom = "The gears are grinding. Heavy load."

        return MetabolicReceipt(
            base_cost=round(bmr, 2),
            drag_tax=round(drag_tax, 2),
            inefficiency_tax=round(inefficiency, 2),
            total_burn=round(final_cost, 2),
            status=status,
            symptom=symptom
        )

    def respirate(self, receipt: MetabolicReceipt) -> str:
        """
        Executes the metabolic cost calculated by the receipt.
        """
        if receipt.status == "NECROSIS":
            self.state.atp_pool = 0.0
            return "NECROSIS"

        if receipt.status == self.APOPTOSIS_TRIGGER:
            self.krebs_cycle_active = False
            self.state.atp_pool = 0.0
            return self.APOPTOSIS_TRIGGER

        self.state.atp_pool -= receipt.total_burn

        # Fuller: Auto-regulation. High burn generates ROS (Free Radicals).
        # This creates a feedback loop: High Drag -> High Burn -> High ROS -> Apoptosis.
        ros_generation = receipt.total_burn * 0.1 * (1.0 / self.state.ros_resistance)
        self.state.ros_buildup += ros_generation

        return "RESPIRING"

class SomaticLoop:
    def __init__(self, bio_layer, memory_layer, lexicon_layer, gordon_ref, folly_ref, events_ref):
        self.bio = bio_layer
        self.mem = memory_layer
        self.lex = lexicon_layer
        self.gordon = gordon_ref
        self.folly = folly_ref
        self.events = events_ref
        
    def digest_cycle(self, text, physics_packet, feedback, stress_mod=1.0, tick_count=0):
        cycle_logs = []
        has_bracelet = "TIME_BRACELET" in self.gordon.inventory
        modifiers = []
        if "TIME_BRACELET" in self.gordon.inventory:
            modifiers.append(0.5)
        counts = physics_packet["counts"]
        is_hybrid = (counts.get("heavy", 0) >= 2 and counts.get("abstract", 0) >= 2)
        if is_hybrid:
            modifiers.append(0.8)
        receipt = self.bio.mito.calculate_metabolism(
            physics_packet["narrative_drag"],
            external_modifiers=modifiers
        )
        resp_status = self.bio.mito.respirate(receipt)
        if receipt.total_burn > 3.0:
            tax_note = ""
            if receipt.drag_tax > 1.0: tax_note = f" (Drag Tax: {receipt.drag_tax})"
            cycle_logs.append(f"{Prisma.GRY}METABOLISM: Burned {receipt.total_burn} ATP{tax_note}.{Prisma.RST}")
        enzyme, nutrient = self.bio.gut.secrete(text, physics_packet)
        base_yield = nutrient["yield"]
        geo_mass = physics_packet.get("geodesic_mass", 0.0)
        psi = physics_packet.get("psi", 0.0)
        geo_multiplier = 1.0 + min(1.5, (geo_mass / BoneConfig.GEODESIC_STRENGTH))
        complexity_tax = 0.0
        if psi > 0.6 and geo_mass < 2.0:
            complexity_tax = base_yield * 0.4
            cycle_logs.append(f"{Prisma.YEL}COMPLEXITY TAX: High Psi ({psi:.2f}) with Low Connectivity. -{complexity_tax:.1f} Yield.{Prisma.RST}")
        final_yield = (base_yield * geo_multiplier) - complexity_tax
        final_yield = max(0.0, final_yield)
        if geo_multiplier > 1.2:
            cycle_logs.append(f"{Prisma.GRN}INFRASTRUCTURE BONUS: Geodesic Mass {geo_mass:.1f}. Yield x{geo_multiplier:.2f}.{Prisma.RST}")
        self.bio.mito.state.atp_pool += final_yield
        sugar, lichen_msg = self.bio.lichen.photosynthesize(
            physics_packet, 
            physics_packet["clean_words"], 
            tick_count)
        if sugar > 0:
            self.bio.mito.state.atp_pool += sugar
            cycle_logs.append(f"\n{lichen_msg}")
        if self.bio.mito.state.atp_pool < 10.0:
            cycle_logs.append(f"{Prisma.RED}STARVATION PROTOCOL: ATP Critical. Initiating Autophagy...{Prisma.RST}")
            _, log_msg = self.mem.cannibalize()
            self.bio.mito.state.atp_pool += 15.0
            cycle_logs.append(f"   {Prisma.RED}AUTOPHAGY: {log_msg} (+15.0 ATP){Prisma.RST}")
        turb = physics_packet.get("turbulence", 0.0)
        if turb > 0.7:
            burn = 5.0
            self.bio.mito.state.atp_pool -= burn
            cycle_logs.append(f"{Prisma.YEL}CHOPPY WATERS: High Turbulence burn. -{burn} ATP.{Prisma.RST}")
        elif turb < 0.2:
            self.bio.mito.state.atp_pool += 2.0
        folly_event, folly_msg, folly_yield, loot = self.folly.grind_the_machine(
            self.bio.mito.state.atp_pool, 
            physics_packet["clean_words"], 
            self.lex)
        if folly_event:
            cycle_logs.append(f"\n{folly_msg}") 
            self.bio.mito.state.atp_pool += folly_yield
            if loot:
                loot_msg = self.gordon.acquire(loot)
                if loot_msg: cycle_logs.append(loot_msg)
        harvest_hits = sum(1 for w in physics_packet["clean_words"] if w in TheLexicon.get("harvest"))
        chem_state = self.bio.endo.metabolize(
            feedback, 
            100.0,
            100.0,
            self.bio.mito.state.ros_buildup, 
            harvest_hits=harvest_hits,
            stress_mod=stress_mod)
        return {
            "is_alive": resp_status != "NECROSIS", 
            "atp": self.bio.mito.state.atp_pool, 
            "chem": chem_state, 
            "enzyme_active": enzyme,
            "logs": cycle_logs}

class MycotoxinFactory:
    def __init__(self):
        self.active_antibodies = set()

    def develop_antibody(self, toxin_name):
        if toxin_name not in self.active_antibodies:
            self.active_antibodies.add(toxin_name)
            return True
        return False

    def assay(self, text, enzyme_type, repetition_score, physics, pulse_status="CLEAR"):
        if len(text) < 5 and enzyme_type == "NARRATIVE":
            return "AMANITIN", "Fatal Error: Input is genetically hollow. Ribosome stalled."
        if pulse_status == "ZOMBIE_KNOCK" or repetition_score > 0.8:
            return "MUSCIMOL", f"System Delirium: Pulse Monitor detects Undead Signal (Rep: {repetition_score}). Reality is dissolving."
        if TheLexicon.ANTIGEN_REGEX:
            antigen_hits = TheLexicon.ANTIGEN_REGEX.findall(text)
            if antigen_hits:
                toxin_name = antigen_hits[0].lower()
                if toxin_name in self.active_antibodies:
                    return None, f"{Prisma.GRN}IMMUNITY: Antibody deployed against '{toxin_name}'. Toxin neutralized.{Prisma.RST}"
                counts = physics["counts"]
                if counts.get("thermal", 0) > 0:
                    self.develop_antibody(toxin_name)
                    return None, f"{Prisma.OCHRE}ALCHEMY: Thermal words boiled off '{toxin_name}'. Antibody developed.{Prisma.RST}"
                if counts.get("heavy", 0) >= len(antigen_hits):
                    return None, f"{Prisma.GRN}MARIK GAMBIT: You ate the poison ('{toxin_name}'), but Herbs neutralized it.{Prisma.RST}"
                if counts.get("cryo", 0) > 0:
                    return "CYANIDE_POWDER", f"CRYO-CONCENTRATION: Cold words freeze-dried '{toxin_name}' into a fatal powder."
                return "GLYPHOSATE", f"TOXIN DETECTED: '{toxin_name}' is unprocessed waste. Burn it or bury it."
        clean_words = physics["clean_words"]
        mass_words = (TheLexicon.get("heavy") | TheLexicon.get("kinetic") | TheLexicon.get("thermal") | TheLexicon.get("cryo"))
        ballast = sum(1 for w in clean_words if w in mass_words)
        suburban_hits = [w for w in clean_words if w in TheLexicon.get("suburban")]
        suburban_density = len(suburban_hits) / max(1, len(clean_words))
        if suburban_density > 0.15 and ballast == 0:
            return "GLYPHOSATE", "STEVE EVENT: Suburban signals detected with ZERO mass. Context is sterile."
        return None, None

class HyphalInterface:
    def __init__(self):
        self.enzymes = {
            "LIGNASE": self._digest_structure,
            "CELLULASE": self._digest_narrative,
            "PROTEASE": self._digest_intent,
            "CHITINASE": self._digest_complex,
            "DECRYPTASE": self._digest_encrypted}
        self.biome = deque(maxlen=5)
        self.WEATHER_CIPHER = {"pressure", "humidity", "barometric", "temp", "forecast", "storm", "resource", "allocation"}

    def secrete(self, text, physics):
        code_markers = sum(1 for c in text if c in "{}[];=<>_()|")
        code_density = code_markers / max(1, len(text))
        meat_triggers = TheLexicon.get("meat")
        meat_count = sum(1 for w in physics["clean_words"] if w in meat_triggers)
        meat_density = meat_count / max(1, len(physics["clean_words"]))
        lines = [l for l in text.splitlines() if l.strip()]
        avg_line_len = len(text.split()) / max(1, len(lines))
        is_list = any(l.strip().startswith(("-", "*", "1.", "•")) for l in lines[:3])
        is_poetic = len(lines) > 2 and avg_line_len < 8 and not is_list
        enzyme_type = "CELLULASE"
        weather_hits = sum(1 for w in physics["clean_words"] if w in self.WEATHER_CIPHER)
        if weather_hits > 0:
            enzyme_type = "DECRYPTASE"
        if (code_density > 0.02 and meat_density > 0.05) or is_poetic:
            enzyme_type = "CHITINASE"
        elif code_density > 0.05 or "def " in text or "class " in text:
            enzyme_type = "LIGNASE"
        elif meat_density > 0.1 or "?" in text:
            enzyme_type = "PROTEASE"
        if "antigens" in physics and physics["antigens"]:
            for bug in physics["antigens"]:
                self.biome.append(bug)
        unique_bugs = len(set(self.biome))
        biome_mod = 1.0 + (math.log(unique_bugs + 1) * 0.3)
        extract_nutrients = self.enzymes[enzyme_type]
        nutrient_profile = extract_nutrients()
        if unique_bugs > 0:
            nutrient_profile["yield"] *= biome_mod
            nutrient_profile["desc"] += f" (+{int((biome_mod-1)*100)}% Symbiotic Boost)"
        return enzyme_type, nutrient_profile

    @staticmethod
    def _digest_structure(text=None):
        loc = 0
        if text:
            lines = text.splitlines()
            loc = len([l for l in lines if l.strip()])
        return {"type": "STRUCTURAL", "yield": 15.0, "toxin": 5.0, "desc": f"Hard Lignin ({loc} LOC)", }

    @staticmethod
    def _digest_encrypted(_text=None):
        return {"type": "ENCRYPTED", "yield": 25.6, "toxin": 2.0, "desc": "Barometric Data (High Resource Allocation)"}

    @staticmethod
    def _digest_narrative(_text=None):
        return {"type": "NARRATIVE", "yield": 5.0, "toxin": -2.0, "desc": "Soft Cellulose", }

    @staticmethod
    def _digest_intent(_text=None):
        return {"type": "BIOLOGICAL", "yield": 8.0, "toxin": 0.0, "desc": "Raw Meat (User Intent)", }

    @staticmethod
    def _digest_complex(_text=None):
        return {"type": "COMPLEX", "yield": 20.0, "toxin": 8.0, "desc": "Chitin (Structured Intent / Poetry)", }

class ParasiticSymbiont:
    def __init__(self, memory_ref, lexicon_ref):
        self.mem = memory_ref
        self.lex = lexicon_ref
        self.spores_deployed = 0
        self.MAX_SPORES = 5
    def infect(self, physics_packet, stamina):
        psi = physics_packet.get("psi", 0.0)
        if stamina > 40.0 and psi < 0.8:
            return False, None
        rep = physics_packet.get("repetition", 0.0)
        drag = physics_packet.get("narrative_drag", 0.0)
        threshold = 0.3 if psi < 0.8 else 0.1
        if rep < threshold and drag < 3.0 and psi < 0.8:
            return False, None
        heavy_candidates = [w for w in self.mem.graph if w in self.lex.get("heavy")]
        abstract_candidates = [w for w in self.mem.graph if w in self.lex.get("abstract")]
        if not heavy_candidates or not abstract_candidates:
            return False, None
        host = random.choice(heavy_candidates)
        parasite = random.choice(abstract_candidates)
        if parasite in self.mem.graph[host]["edges"]:
            return False, None
        weight = 8.0
        self.mem.graph[host]["edges"][parasite] = weight
        if parasite not in self.mem.graph:
            self.mem.graph[parasite] = {"edges": {}, "last_tick": 0}
        self.mem.graph[parasite]["edges"][host] = weight
        self.spores_deployed += 1
        cause = "Stagnation"
        if stamina > 40.0:
            cause = "Hallucination (High Psi)"
        return True, (
            f"{Prisma.VIOLET}PARASITIC GRAFT [{cause}]: The Rot connects '{host.upper()}' <-> '{parasite.upper()}'.\n"
            f"   Logic bypassed. The map is now hallucinating.{Prisma.RST}")

class LichenSymbiont:
    @staticmethod
    def photosynthesize(phys, clean_words, tick_count):
        sugar = 0
        msgs = []
        light = phys["counts"].get("photo", 0)
        drag = phys["narrative_drag"]
        light_words = [w for w in clean_words if w in TheLexicon.get("photo")]
        if light > 0 and drag < 3.0:
            s = light * 2
            sugar += s
            source_str = ""
            if light_words:
                source_str = f" via '{random.choice(light_words)}'"
            msgs.append(f"{Prisma.GRN}PHOTOSYNTHESIS{source_str} (+{s}){Prisma.RST}")
        if sugar > 0:
            heavy_words = [w for w in clean_words if w in TheLexicon.get("heavy")]
            if heavy_words:
                h_word = random.choice(heavy_words)
                TheLexicon.teach(h_word, "photo", tick_count)
                msgs.append(
                    f"{Prisma.MAG}SUBLIMATION: '{h_word}' has become Light.{Prisma.RST}")
        return sugar, " ".join(msgs) if msgs else None

@dataclass
class EndocrineSystem:
    dopamine: float = 0.5
    oxytocin: float = 0.1
    cortisol: float = 0.0
    serotonin: float = 0.5
    adrenaline: float = 0.0
    melatonin: float = 0.0
    
    def metabolize(self, feedback, health: float, stamina: float, ros_level: float = 0.0, 
                   social_context: bool = False, enzyme_type: str = None, 
                   harvest_hits: int = 0, stress_mod: float = 1.0):
        if harvest_hits > 0:
            satiety_dampener = max(0.1, 1.0 - self.dopamine)
            base_reward = math.log(harvest_hits + 1) * 0.15
            final_reward = base_reward * satiety_dampener
            self.dopamine = min(1.0, self.dopamine + final_reward)
            self.cortisol = max(0.0, self.cortisol - (final_reward * 0.4))
        if enzyme_type == "PROTEASE":
            self.adrenaline = min(1.0, self.adrenaline + 0.1)
        elif enzyme_type == "CELLULASE":
            self.cortisol = max(0.0, self.cortisol - 0.1)
            self.oxytocin = min(1.0, self.oxytocin + 0.05)
        elif enzyme_type == "CHITINASE":
            self.dopamine = min(1.0, self.dopamine + 0.15)
        elif enzyme_type == "LIGNASE":
            self.serotonin = min(1.0, self.serotonin + 0.1)
        if feedback["STATIC"] > 0.6:
            self.cortisol = min(1.0, self.cortisol + (0.15 * stress_mod))
        elif self.serotonin > 0.6:
            self.cortisol = max(0.0, self.cortisol - 0.05)
        if feedback["INTEGRITY"] > 0.8:
            self.dopamine = min(1.0, self.dopamine + 0.1)
        else:
            self.dopamine = max(0.2, self.dopamine - 0.01)
        if stamina < 20.0:
            self.cortisol = min(1.0, self.cortisol + (0.1 * stress_mod))
            self.dopamine = max(0.0, self.dopamine - 0.1)
        if ros_level > 20.0:
            self.cortisol = min(1.0, self.cortisol + (0.2 * stress_mod))
        if health < 30.0 or feedback["STATIC"] > 0.8:
            self.adrenaline = min(1.0, self.adrenaline + (0.2 * stress_mod))
        else:
            self.adrenaline = max(0.0, self.adrenaline - 0.05)
        if social_context or (self.serotonin > 0.7 and self.cortisol < 0.2):
            self.oxytocin = min(1.0, self.oxytocin + 0.05)
        elif self.cortisol > 0.6:
            self.oxytocin = max(0.0, self.oxytocin - 0.1)
        if self.adrenaline < 0.2:
            self.melatonin = min(1.0, self.melatonin + 0.02)
        else:
            self.melatonin = 0.0
        return self.get_state()
    
    def get_state(self):
        return {"DOP": round(self.dopamine, 2), "OXY": round(self.oxytocin, 2), "COR": round(self.cortisol, 2),
                "SER": round(self.serotonin, 2), "ADR": round(self.adrenaline, 2), "MEL": round(self.melatonin, 2), }

@dataclass
class MetabolicGovernor:
    mode: str = "COURTYARD"
    psi_mod: float = 0.2
    kappa_target: float = 0.0
    drag_floor: float = 2.0
    manual_override: bool = False
    birth_tick: float = field(default_factory=time.time)
    
    @staticmethod
    def get_stress_modifier(tick_count):
        if tick_count <= 2: return 0.0
        if tick_count <= 5: return 0.5
        return 1.0
    
    def set_override(self, target_mode):
        valid = {"COURTYARD", "LABORATORY", "FORGE"}
        if target_mode in valid:
            self.mode = target_mode
            self.manual_override = True
            return f"MANUAL OVERRIDE: System locked to {target_mode}."
        return "INVALID MODE."
    
    def shift(self, physics, history_log):
        if self.manual_override:
            return None
        if history_log:
            avg_cortisol = sum(h[1].get('COR', 0.0) for h in history_log) / len(history_log)
            if avg_cortisol > 0.5 and self.mode != "COURTYARD":
                self.mode = "COURTYARD"
                return f"{Prisma.GRN}GOVERNOR: System Stressed (Avg COR: {avg_cortisol:.2f}). Retreating to COURTYARD.{Prisma.RST}"
        voltage = physics["voltage"]
        if voltage > 9.0:
            self.mode = "FORGE"
            return f"{Prisma.RED}GOVERNOR: Critical Voltage. Locking to FORGE.{Prisma.RST}"
        if physics["narrative_drag"] > 4.0 > voltage:
            self.mode = "LABORATORY"
            return f"{Prisma.CYN}GOVERNOR: High Drag detected. Restricting to LABORATORY.{Prisma.RST}"
        if self.mode != "COURTYARD" and voltage < 2.0:
            self.mode = "COURTYARD"
            return f"{Prisma.GRN}GOVERNOR: All Clear. Relaxing to COURTYARD.{Prisma.RST}"
        beta = physics.get("beta_index", 0.0)
        sacred_count = physics["counts"].get("sacred", 0)
        if (beta > 1.5 and voltage > 15.0) or sacred_count >= 2:
            self.mode = "SANCTUARY"
            physics["narrative_drag"] = 0.0
            physics["voltage"] = 99.9
            return f"{Prisma.GRN}GOVERNOR: Bonepoke Critical (β: {beta}). Entering SANCTUARY.{Prisma.RST}"
        return None