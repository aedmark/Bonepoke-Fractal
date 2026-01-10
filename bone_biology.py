# bone_biology.py

import math
import time
import random
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Any

from bone_shared import Prisma, TheLexicon, BoneConfig
from bone_pipeline import PhysicsPacket

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
    """
    The Body's Main Loop.
    Refactored for cognitive clarity and separation of concerns.
    """
    def __init__(self, bio_layer, memory_layer, lexicon_layer, gordon_ref, folly_ref, events_ref):
        self.bio = bio_layer
        self.mem = memory_layer
        self.lex = lexicon_layer
        self.gordon = gordon_ref
        self.folly = folly_ref
        self.events = events_ref

    def digest_cycle(self, text: str, physics_data: Any, feedback: Dict,
                     current_health: float, current_stamina: float,
                     stress_mod: float = 1.0, tick_count: int = 0) -> Dict:
        """
        Processes the metabolic cost of a single turn.
        """
        # 1. Normalize Input (Pinker Lens: sanitation first)
        if isinstance(physics_data, dict):
            # Graceful degradation if passed a dict
            try:
                phys = PhysicsPacket.from_dict(physics_data)
            except NameError:
                # If you haven't implemented PhysicsPacket yet, this fallback
                # allows the code to run with the dict (but warns you).
                phys = physics_data
        else:
            phys = physics_data

        cycle_logs = []

        # 2. Calculate Base Metabolic Cost
        # (How much energy does it cost to exist in this narrative drag?)
        receipt = self._calculate_burn(phys, self.gordon.inventory)
        resp_status = self.bio.mito.respirate(receipt)

        if receipt.total_burn > 3.0:
            tax_note = f" (Drag Tax: {receipt.drag_tax:.1f})" if receipt.drag_tax > 1.0 else ""
            cycle_logs.append(f"{Prisma.GRY}METABOLISM: Burned {receipt.total_burn:.1f} ATP{tax_note}.{Prisma.RST}")

        # 3. Audit Desire (The Folly)
        # Sometimes the machine refuses to work because it's tired of your nonsense.
        if hasattr(self.folly, 'audit_desire'):
            event, msg, _, _ = self.folly.audit_desire(phys.__dict__ if hasattr(phys, '__dict__') else phys, current_stamina)
            if event == "MAUSOLEUM_CLAMP":
                cycle_logs.append(msg)
                return self._package_result(resp_status, cycle_logs, enzyme="NONE")

        # 4. Digestion (Extracting value from words)
        enzyme, nutrient_yield = self._process_digestion(text, phys, cycle_logs)
        self.bio.mito.state.atp_pool += nutrient_yield

        # 5. Photosynthesis (Lichen) & Starvation Checks
        self._process_photosynthesis(phys, cycle_logs, tick_count)
        self._handle_turbulence(phys, cycle_logs)
        self._handle_starvation(cycle_logs, tick_count)

        # 6. The Folly (Gambling ATP for loot)
        self._process_folly(phys, cycle_logs)

        # 7. Endocrine Response (Hormones)
        chem_state = self.bio.endo.metabolize(
            feedback, current_health, current_stamina,
            self.bio.mito.state.ros_buildup,
            harvest_hits=self._count_harvest_hits(phys),
            stress_mod=stress_mod
        )

        return self._package_result(resp_status, cycle_logs, chem_state, enzyme)

    # --- Sub-Routines (The "Paragraphs" of our Logic) ---

    def _calculate_burn(self, phys, inventory):
        """Calculates ATP cost based on drag and items."""
        modifiers = []
        if "TIME_BRACELET" in inventory:
            modifiers.append(0.5)

        # Access safely depending on if phys is object or dict
        counts = phys.counts if hasattr(phys, 'counts') else phys['counts']
        drag = phys.narrative_drag if hasattr(phys, 'narrative_drag') else phys['narrative_drag']

        is_hybrid = (counts.get("heavy", 0) >= 2 and counts.get("abstract", 0) >= 2)
        if is_hybrid:
            modifiers.append(0.8) # Hybrid vigor reduces cost

        return self.bio.mito.calculate_metabolism(drag, external_modifiers=modifiers)

    def _process_digestion(self, text, phys, logs):
        """Extracts nutrients from text via HyphalInterface."""
        # Note: calling secret with dict version if needed
        p_dict = phys.__dict__ if hasattr(phys, '__dict__') else phys
        enzyme, nutrient = self.bio.gut.secrete(text, p_dict)

        base_yield = nutrient["yield"]

        # Geodesic Bonus (Fuller Lens: Structure adds value)
        geo_mass = p_dict.get("geodesic_mass", 0.0)
        psi = p_dict.get("psi", 0.0)

        geo_multiplier = 1.0 + min(1.5, (geo_mass / BoneConfig.GEODESIC_STRENGTH))

        # Complexity Tax (Pinker Lens: Too abstract = hard to digest)
        complexity_tax = 0.0
        if psi > 0.6 and geo_mass < 2.0:
            complexity_tax = base_yield * 0.4
            logs.append(f"{Prisma.YEL}COMPLEXITY TAX: High Psi, Low Structure. -{complexity_tax:.1f} Yield.{Prisma.RST}")

        final_yield = max(0.0, (base_yield * geo_multiplier) - complexity_tax)

        if geo_multiplier > 1.2:
            logs.append(f"{Prisma.GRN}INFRASTRUCTURE BONUS: Mass {geo_mass:.1f}. Yield x{geo_multiplier:.2f}.{Prisma.RST}")

        return enzyme, final_yield

    def _process_photosynthesis(self, phys, logs, tick):
        """Lichen converts Light words into Sugar."""
        p_dict = phys.__dict__ if hasattr(phys, '__dict__') else phys
        clean = p_dict.get("clean_words", [])
        sugar, msg = self.bio.lichen.photosynthesize(p_dict, clean, tick)
        if sugar > 0:
            self.bio.mito.state.atp_pool += sugar
            logs.append(f"\n{msg}")

    def _handle_turbulence(self, phys, logs):
        """Rough waters cost energy."""
        turb = phys.turbulence if hasattr(phys, 'turbulence') else phys.get('turbulence', 0)
        if turb > 0.7:
            burn = 5.0
            self.bio.mito.state.atp_pool -= burn
            logs.append(f"{Prisma.YEL}CHOPPY WATERS: High Turbulence burn. -{burn} ATP.{Prisma.RST}")
        elif turb < 0.2:
            self.bio.mito.state.atp_pool += 2.0

    def _handle_starvation(self, logs, tick):
        """Autophagy protocol."""
        if self.bio.mito.state.atp_pool < 10.0:
            logs.append(f"{Prisma.RED}STARVATION PROTOCOL: ATP Critical. Initiating Autophagy...{Prisma.RST}")
            victim, log_msg = self.mem.cannibalize(current_tick=tick)
            if victim:
                self.bio.mito.state.atp_pool += 15.0
                logs.append(f"   {Prisma.RED}AUTOPHAGY: {log_msg} (+15.0 ATP){Prisma.RST}")
            else:
                logs.append(f"   {Prisma.RED}AUTOPHAGY FAILED: {log_msg}{Prisma.RST}")

    def _process_folly(self, phys, logs):
        """The Folly machine grinds words for items."""
        p_dict = phys.__dict__ if hasattr(phys, '__dict__') else phys
        event, msg, yield_val, loot = self.folly.grind_the_machine(
            self.bio.mito.state.atp_pool,
            p_dict["clean_words"],
            self.lex
        )
        if event:
            logs.append(f"\n{msg}")
            self.bio.mito.state.atp_pool += yield_val
            if loot:
                loot_msg = self.gordon.acquire(loot)
                if loot_msg: logs.append(loot_msg)

    def _count_harvest_hits(self, phys):
        clean = phys.clean_words if hasattr(phys, 'clean_words') else phys.get('clean_words', [])
        return sum(1 for w in clean if w in TheLexicon.get("harvest"))

    def _package_result(self, status, logs, chem=None, enzyme="NONE"):
        return {
            "is_alive": status != "NECROSIS",
            "atp": self.bio.mito.state.atp_pool,
            "chem": chem if chem else self.bio.endo.get_state(),
            "enzyme_active": enzyme,
            "logs": logs
        }

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
            "DECRYPTASE": self._digest_encrypted
        }
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

        clean = physics.get("clean_words", [])
        cipher_hits = sum(1 for w in clean if w in self.WEATHER_CIPHER)
        if cipher_hits >= 2:
            enzyme_type = "DECRYPTASE"

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

    # [SLASH 9.6.5 Repair]: Added missing method to satisfy __init__ contract
    @staticmethod
    def _digest_encrypted(_text=None):
        return {"type": "ENCRYPTED", "yield": 25.0, "toxin": 2.0, "desc": "Cipher Text (High Density / Puzzle Logic)", }

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
    """
    Regulates the system's operational mode based on stress and energy.
    Refactored by SLASH 9.6.4 to fix the 'Voltage/Cortisol' type mismatch.
    """
    mode: str = "COURTYARD"
    psi_mod: float = 0.2
    kappa_target: float = 0.0
    drag_floor: float = 2.0
    manual_override: bool = False
    birth_tick: float = field(default_factory=time.time)

    @staticmethod
    def get_stress_modifier(tick_count):
        # [Pinker Lens]: Simple ramping stress mechanic.
        if tick_count <= 2: return 0.0
        if tick_count <= 5: return 0.5
        return 1.0

    def set_override(self, target_mode):
        valid = {"COURTYARD", "LABORATORY", "FORGE", "SANCTUARY"}
        if target_mode in valid:
            self.mode = target_mode
            self.manual_override = True
            return f"MANUAL OVERRIDE: System locked to {target_mode}."
        return "INVALID MODE."

    def shift(self, physics: Dict, voltage_history: List[float]) -> Optional[str]:
        """
        Determines the metabolic mode for the next turn.
        Fixed to handle voltage_history as a list of floats safely.
        """
        if self.manual_override:
            return None

        # 1. Analyze Trends (Fuller Lens: Look at the vector, not just the point)
        avg_voltage = 0.0
        if voltage_history and len(voltage_history) > 0:
            avg_voltage = sum(voltage_history) / len(voltage_history)

        current_voltage = physics.get("voltage", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        beta = physics.get("beta_index", 0.0)
        sacred_count = physics["counts"].get("sacred", 0)

        # 2. Critical Safety Interventions (Schur Lens: "Don't die.")
        if current_voltage > 15.0 and beta > 1.5:
            # High Energy + High Structure = Sanctuary
            if self.mode != "SANCTUARY":
                self.mode = "SANCTUARY"
                physics["narrative_drag"] = 0.0 # Sanctuary creates space
                return f"{Prisma.GRN}GOVERNOR: VSL Critical (β: {beta:.2f}). Entering SANCTUARY.{Prisma.RST}"

        if current_voltage > 10.0:
            if self.mode != "FORGE":
                self.mode = "FORGE"
                return f"{Prisma.RED}GOVERNOR: High Voltage ({current_voltage:.1f}v). Locking to FORGE.{Prisma.RST}"

        if drag > 4.0 and current_voltage < 4.0:
            if self.mode != "LABORATORY":
                self.mode = "LABORATORY"
                return f"{Prisma.CYN}GOVERNOR: High Drag detected. Restricting to LABORATORY.{Prisma.RST}"

        # 3. Relaxation (Return to Homeostasis)
        if self.mode != "COURTYARD":
            # If we are calm and stable, go home.
            if current_voltage < 5.0 and drag < 2.0:
                self.mode = "COURTYARD"
                return f"{Prisma.GRN}GOVERNOR: All Clear. Relaxing to COURTYARD.{Prisma.RST}"

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