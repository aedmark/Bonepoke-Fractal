# bone_biology.py

import math
import time
import random
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple

from bone_shared import Prisma, TheLexicon, BoneConfig

@dataclass
class MetabolicReceipt:
    """
    A transactional record of a single metabolic cycle.

    This acts as the 'bill' presented to the somatic system after a turn.
    It breaks down exactly where energy (ATP) was spent, separating
    essential existence costs (BMR) from environmental friction (Drag).
    """
    base_cost: float        # The fixed cost of existing (Basal Metabolic Rate).
    drag_tax: float         # The penalty derived from Narrative Drag (Quadratic scaling).
    inefficiency_tax: float # Extra cost incurred by low mitochondrial efficiency.
    total_burn: float       # Final ATP amount to be deducted.
    status: str             # e.g., "RESPIRING", "NECROSIS", "APOPTOSIS".
    symptom: str = "Nominal"

@dataclass
class MitochondrialState:
    """
    The persistent state of the biological engine.

    This data structure carries the genetic and epigenetic history of the
    session (and its ancestors via Spores).
    """
    atp_pool: float = 100.0
    ros_buildup: float = 0.0          # Reactive Oxygen Species (Cellular pollution/stress).
    membrane_potential: float = -150.0 # Electrical gradient (Health/Capacity indicator).
    mother_hash: str = "MITOCHONDRIAL_EVE_001" # Lineage tracking ID.
    efficiency_mod: float = 1.0       # Multiplier for ATP conversion (Higher is better).
    ros_resistance: float = 1.0       # Ability to scrub ROS/pollution.
    enzymes: Set[str] = field(default_factory=set) # Acquired traits (e.g., 'LIGNASE').
    telomeres: int = 105              # Genetic countdown timer (currently unused, but reserved).

class MitochondrialForge:
    """
    The Power Plant of the system.

    It converts 'Physics' (Drag, Time) into 'Biology' (ATP Cost, ROS Stress).
    It enforces the Laws of Thermodynamics: You cannot act without paying energy.
    """
    BASE_BMR = 2.0
    APOPTOSIS_TRIGGER = "CYTOCHROME_C_RELEASE"
    MAX_ATP = 200.0

    # Threshold where Drag becomes metabolically expensive (Quadratic curve start).
    DRAG_SOFT_CAP = 5.0

    def __init__(self, lineage_seed: str, events, inherited_traits: Optional[Dict] = None):
        self.state = MitochondrialState(mother_hash=lineage_seed)
        self.events = events
        self.krebs_cycle_active = True

        if inherited_traits:
            self._apply_inheritance(inherited_traits)

    def _apply_inheritance(self, traits: Dict):
        """Unpacks genetic data from previous sessions (Spores)."""
        self.state.efficiency_mod = traits.get("efficiency_mod", 1.0)
        self.state.ros_resistance = traits.get("ros_resistance", 1.0)
        if "enzymes" in traits:
            self.state.enzymes = set(traits["enzymes"])
            self.events.log(f"{Prisma.CYN}[MITO]: Inherited Enzymes: {list(self.state.enzymes)}.{Prisma.RST}")

    def adapt(self, final_health: float) -> Dict:
        """
        Triggered at death/save. Modifies genetics based on how the organism died.
        If death was stressful (low health), we mutate to resist stress next time.
        """
        traits = {
            "efficiency_mod": self.state.efficiency_mod,
            "ros_resistance": self.state.ros_resistance,
            "enzymes": list(self.state.enzymes)
        }
        # Evolution mechanic: Hardship breeds resistance.
        if final_health <= 0 and random.random() < 0.3:
            traits["ros_resistance"] += 0.1
        return traits

    def calculate_metabolism(self, drag: float, external_modifiers: Optional[List[float]] = None) -> MetabolicReceipt:
        """
        The Core Calculation.

        Logic:
        1. Base Cost (BMR) is constant.
        2. Drag Tax is QUADRATIC ((drag^2)/10).
           - Low drag (1-3) is cheap.
           - High drag (8-10) becomes exponentially expensive.
        3. External modifiers (items, buffs) apply multiplicatively to the Drag Tax.
        """
        bmr = self.BASE_BMR

        # Calculate Drag Tax (Quadratic Penalty)
        safe_drag = max(0.0, drag)
        drag_tax = (safe_drag * safe_drag) / 10.0

        # Apply Inventory/Status Effects
        if external_modifiers:
            for mod in external_modifiers:
                drag_tax *= mod

        raw_cost = bmr + drag_tax

        # Apply Efficiency (The 'Metabolic Fitness' of the system)
        safe_efficiency = max(0.1, self.state.efficiency_mod)
        final_cost = raw_cost / safe_efficiency

        # Calculate waste heat/inefficiency
        inefficiency = 0.0
        if safe_efficiency < 1.0:
            inefficiency = final_cost - raw_cost

        # Determine Biological Status based on ability to pay
        status = "RESPIRING"
        symptom = "Humming along."

        if final_cost > self.state.atp_pool:
            status = "NECROSIS" # Running on empty
            symptom = f"The engine is stalling. Requires {final_cost:.1f} ATP."
        elif self.state.ros_buildup > BoneConfig.CRITICAL_ROS_LIMIT:
            status = self.APOPTOSIS_TRIGGER # Suicide due to toxicity
            symptom = "Cellular suicide initiated. Too much noise."
        elif drag_tax > self.DRAG_SOFT_CAP:
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
        Commits the transaction. Deducts ATP and generates pollution (ROS).
        """
        if receipt.status == "NECROSIS":
            self.state.atp_pool = 0.0
            return "NECROSIS"

        if receipt.status == self.APOPTOSIS_TRIGGER:
            self.krebs_cycle_active = False
            self.state.atp_pool = 0.0
            return self.APOPTOSIS_TRIGGER

        # Payment
        self.state.atp_pool -= receipt.total_burn

        # Pollution Generation (ROS)
        # More burning = more pollution. High resistance reduces this.
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

    def digest_cycle(self, text, physics_packet, feedback, current_health, current_stamina, stress_mod=1.0, tick_count=0):
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
        if hasattr(self.folly, 'audit_desire'):
            d_event, d_msg, d_yield, d_loot = self.folly.audit_desire(physics_packet, current_stamina)
            if d_event == "MAUSOLEUM_CLAMP":
                cycle_logs.append(d_msg)
                return {
                    "is_alive": True,
                    "atp": self.bio.mito.state.atp_pool,
                    "chem": self.bio.endo.get_state(),
                    "enzyme_active": "NONE",
                    "logs": cycle_logs}
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
            victim, log_msg = self.mem.cannibalize(current_tick=tick_count)
            if victim:
                self.bio.mito.state.atp_pool += 15.0
                cycle_logs.append(f"   {Prisma.RED}AUTOPHAGY: {log_msg} (+15.0 ATP){Prisma.RST}")
            else:
                cycle_logs.append(f"   {Prisma.RED}AUTOPHAGY FAILED: {log_msg} (No Energy Gained){Prisma.RST}")
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
            current_health,
            current_stamina,
            self.bio.mito.state.ros_buildup,
            harvest_hits=harvest_hits,
            stress_mod=stress_mod
        )
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
        self.MAX_SPORES = 8

    def infect(self, physics_packet, stamina):
        psi = physics_packet.get("psi", 0.0)
        if stamina > 40.0 and psi < 0.6:
            return False, None
        if self.spores_deployed >= self.MAX_SPORES:
            if random.random() < 0.2:
                self.spores_deployed = max(0, self.spores_deployed - 1)
            return False, None
        heavy_candidates = [w for w in self.mem.graph if w in self.lex.get("heavy")]
        abstract_candidates = [w for w in self.mem.graph if w in self.lex.get("abstract")]
        if not heavy_candidates or not abstract_candidates:
            return False, None
        host = random.choice(heavy_candidates)
        parasite = random.choice(abstract_candidates)
        if parasite in self.mem.graph[host]["edges"]:
            return False, None
        is_metaphor = psi > 0.7
        weight = 8.88
        self.mem.graph[host]["edges"][parasite] = weight
        if parasite not in self.mem.graph:
            self.mem.graph[parasite] = {"edges": {}, "last_tick": 0}
        self.mem.graph[parasite]["edges"][host] = weight
        self.spores_deployed += 1
        if is_metaphor:
            return True, (
                f"{Prisma.CYN}✨ SYNAPSE SPARK: Your mind bridges '{host.upper()}' and '{parasite.upper()}'.\n"
                f"   A new metaphor is born. The map folds.{Prisma.RST}"
            )
        else:
            return True, (
                f"{Prisma.VIOLET}🍄 INTRUSIVE THOUGHT: Exhaustion logic links '{host.upper()}' <-> '{parasite.upper()}'.\n"
                f"   This makes no sense, yet there it is. 'Some things just happen.'{Prisma.RST}"
            )

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
    """
    The Chemical Regulator.

    Manages the organism's 'Mood' via a simulated hormonal balance.
    These values modulate how the system perceives input (Physics) and
    spends energy (Metabolism).

    - Dopamine (DOP): Reward, Motivation. Drives 'Action'.
    - Oxytocin (OXY): Connection, Trust. Buffers 'Trauma'.
    - Cortisol (COR): Stress, Toxicity. Increases 'Drag' perception.
    - Serotonin (SER): Stability, Satisfaction. Regulates 'Homeostasis'.
    - Adrenaline (ADR): Arousal, Fear. Increases 'Voltage'.
    - Melatonin (MEL): Rest, Cycle. Triggers 'Sleep/Save'.
    """
    dopamine: float = 0.5
    oxytocin: float = 0.1
    cortisol: float = 0.0
    serotonin: float = 0.5
    adrenaline: float = 0.0
    melatonin: float = 0.0

    # --- Tuning Constants ---
    # Centralizing these allows for easier game balance tweaking.
    REWARD_SMALL = 0.05
    REWARD_MEDIUM = 0.1
    REWARD_LARGE = 0.15

    STRESS_SMALL = 0.05
    STRESS_MEDIUM = 0.1
    STRESS_LARGE = 0.15

    DECAY_RATE = 0.01

    def _clamp(self, val: float) -> float:
        """Keeps chemical levels within sustainable bounds (0.0 to 1.0)."""
        return max(0.0, min(1.0, val))

    def _apply_enzyme_reaction(self, enzyme_type: str, harvest_hits: int):
        """
        Reacts to the specific 'flavor' of the input text.
        Digestive enzymes (produced by HyphalInterface) trigger hormonal shifts.
        """
        # 1. Harvest Reward (Dopamine Spike)
        if harvest_hits > 0:
            # Diminishing returns: High dopamine makes it harder to get MORE dopamine.
            satiety_dampener = max(0.1, 1.0 - self.dopamine)
            base_reward = math.log(harvest_hits + 1) * 0.15
            final_reward = base_reward * satiety_dampener

            self.dopamine += final_reward
            # Pleasure reduces stress temporarily.
            self.cortisol -= (final_reward * 0.4)

        # 2. Enzyme-Specific Reactions
        # Mapping enzyme types to their hormonal impact.
        reactions = {
            "PROTEASE":   {"ADR": self.REWARD_MEDIUM},             # Meat/Action -> Adrenaline
            "CELLULASE":  {"COR": -self.REWARD_MEDIUM, "OXY": self.REWARD_SMALL}, # Narrative -> Comfort
            "CHITINASE":  {"DOP": self.REWARD_LARGE},              # Complexity -> Big Reward
            "LIGNASE":    {"SER": self.REWARD_MEDIUM},             # Structure -> Stability
            "DECRYPTASE": {"ADR": self.REWARD_SMALL, "DOP": self.REWARD_SMALL}    # Puzzle -> Thrill
        }

        if enzyme_type in reactions:
            impact = reactions[enzyme_type]
            if "ADR" in impact: self.adrenaline += impact["ADR"]
            if "COR" in impact: self.cortisol += impact["COR"]
            if "OXY" in impact: self.oxytocin += impact["OXY"]
            if "DOP" in impact: self.dopamine += impact["DOP"]
            if "SER" in impact: self.serotonin += impact["SER"]

    def _apply_environmental_pressure(self, feedback: Dict, health: float, stamina: float, ros_level: float, stress_mod: float):
        """
        Reacts to the 'Physical' state of the world.
        Pain, starvation, and noise (static) create Cortisol.
        """
        # Static (Repetition) causes stress
        if feedback.get("STATIC", 0) > 0.6:
            self.cortisol += (self.STRESS_LARGE * stress_mod)

        # Structural Integrity feels good
        if feedback.get("INTEGRITY", 0) > 0.8:
            self.dopamine += self.REWARD_MEDIUM
        else:
            self.dopamine -= self.DECAY_RATE

        # Starvation Panic
        if stamina < 20.0:
            self.cortisol += (self.STRESS_MEDIUM * stress_mod)
            self.dopamine -= self.REWARD_MEDIUM

        # Toxicity (ROS) Panic
        if ros_level > 20.0:
            self.cortisol += (self.STRESS_LARGE * stress_mod)

        # Fight or Flight (Adrenaline)
        if health < 30.0 or feedback.get("STATIC", 0) > 0.8:
            self.adrenaline += (self.REWARD_LARGE * stress_mod)
        else:
            self.adrenaline -= (self.DECAY_RATE * 5) # Adrenaline decays fast

    def _maintain_homeostasis(self, social_context: bool):
        """
        The internal feedback loops. Hormones regulating other hormones.
        """
        # Serotonin buffers Cortisol (Stability fights Stress)
        if self.serotonin > 0.6:
            self.cortisol -= self.STRESS_SMALL

        # Social Context (e.g., Chorus Mode) boosts Oxytocin
        if social_context:
            self.oxytocin += self.REWARD_MEDIUM
            self.cortisol -= self.REWARD_MEDIUM
        # High Serotonin/Low Stress facilitates connection
        elif (self.serotonin > 0.7 and self.cortisol < 0.3):
            self.oxytocin += self.REWARD_SMALL

        # High Stress kills connection
        if self.cortisol > 0.7 and not social_context:
            self.oxytocin -= self.STRESS_SMALL

        # Connection reduces Stress (The 'Love' Loop)
        if self.oxytocin > 0.6:
            self.cortisol -= self.REWARD_LARGE

        # Sleep Cycle
        if self.adrenaline < 0.2:
            self.melatonin += (self.REWARD_SMALL / 2) # Slow buildup
        else:
            self.melatonin = 0.0 # Woken up

    def metabolize(self, feedback: Dict, health: float, stamina: float, ros_level: float = 0.0,
                   social_context: bool = False, enzyme_type: Optional[str] = None,
                   harvest_hits: int = 0, stress_mod: float = 1.0) -> Dict[str, float]:
        """
        The Main Cycle.
        Calculates the new chemical state based on all inputs.
        """
        self._apply_enzyme_reaction(enzyme_type, harvest_hits)
        self._apply_environmental_pressure(feedback, health, stamina, ros_level, stress_mod)
        self._maintain_homeostasis(social_context)

        # Clamp all values to legal range [0.0, 1.0]
        self.dopamine = self._clamp(self.dopamine)
        self.oxytocin = self._clamp(self.oxytocin)
        self.cortisol = self._clamp(self.cortisol)
        self.serotonin = self._clamp(self.serotonin)
        self.adrenaline = self._clamp(self.adrenaline)
        self.melatonin = self._clamp(self.melatonin)

        return self.get_state()

    def get_state(self) -> Dict[str, float]:
        return {
            "DOP": round(self.dopamine, 2),
            "OXY": round(self.oxytocin, 2),
            "COR": round(self.cortisol, 2),
            "SER": round(self.serotonin, 2),
            "ADR": round(self.adrenaline, 2),
            "MEL": round(self.melatonin, 2)
        }

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
            return f"{Prisma.GRN}GOVERNOR: VSL Critical (β: {beta}). Entering SANCTUARY.{Prisma.RST}"
        return None

class NeuroPlasticity:
    def __init__(self):
        self.plasticity_mod = 1.0

    def force_hebbian_link(self, graph, word_a, word_b):
        if word_a == word_b: return None
        if word_a not in graph:
            graph[word_a] = {"edges": {}, "last_tick": 0}
        if word_b not in graph:
            graph[word_b] = {"edges": {}, "last_tick": 0}
        current_weight = graph[word_a]["edges"].get(word_b, 0.0)
        new_weight = min(10.0, current_weight + 2.5)
        graph[word_a]["edges"][word_b] = new_weight
        rev_weight = graph[word_b]["edges"].get(word_a, 0.0)
        graph[word_b]["edges"][word_a] = min(10.0, rev_weight + 1.0)
        return f"{Prisma.MAG}⚡ HEBBIAN GRAFT: Wired '{word_a}' <-> '{word_b}'. Synapse strengthened.{Prisma.RST}"

    def trigger_neurogenesis(self, lex, graph, unknown_word):
        target_cat = "abstract" # Default bucket
        lex.teach(unknown_word, target_cat, 0)
        if unknown_word not in graph:
            graph[unknown_word] = {"edges": {}, "last_tick": 0}
        return f"{Prisma.CYN}NEUROGENESIS: Assigned '{unknown_word}' to [ABSTRACT] cortex and seeded Memory.{Prisma.RST}"