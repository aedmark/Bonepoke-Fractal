# bone_body.py - The Body

import math, random, time
from collections import deque
from dataclasses import dataclass, field
from typing import Set, Optional, Dict, List, Any, Tuple

from bone_personality import SynergeticLensArbiter
from bone_physics import PhysicsPacket
from bone_spores import MycotoxinFactory, LichenSymbiont, HyphalInterface, ParasiticSymbiont
from bone_lexicon import TheLexicon
from bone_bus import Prisma, BoneConfig

@dataclass
class Biometrics:
    health: float
    stamina: float
    stress_modifier: float = 1.0
    circadian_bias: Optional[Dict[str, float]] = None

@dataclass
class MetabolicReceipt:
    base_cost: float
    drag_tax: float
    inefficiency_tax: float
    total_burn: float
    status: str
    symptom: str = "Nominal"

@dataclass
class BioSystem:
    mito: 'MitochondrialForge'
    endo: 'EndocrineSystem'
    immune: MycotoxinFactory
    lichen: LichenSymbiont
    gut: HyphalInterface
    plasticity: Any
    governor: 'MetabolicGovernor'
    shimmer: Any
    parasite: ParasiticSymbiont

@dataclass
class MitochondrialState:
    atp_pool: float = 100.0
    ros_buildup: float = 0.0
    membrane_potential: float = -150.0
    mother_hash: str = "MITOCHONDRIAL_EVE_001"
    efficiency_mod: float = 1.0
    ros_resistance: float = 1.0
    enzymes: Set[str] = field(default_factory=set)

class MitochondrialForge:
    APOPTOSIS_TRIGGER = "CYTOCHROME_C_RELEASE"

    def __init__(self, lineage_seed: str, events, inherited_traits: Optional[Dict] = None):
        self.state = MitochondrialState(mother_hash=lineage_seed)
        self.events = events
        self.krebs_cycle_active = True
        self.BMR = BoneConfig.METABOLISM.BASE_RATE
        self.TAX_LOW = BoneConfig.METABOLISM.DRAG_TAX_LOW
        self.TAX_HIGH = BoneConfig.METABOLISM.DRAG_TAX_HIGH
        self.GRACE = BoneConfig.METABOLISM.DRAG_GRACE_BUFFER
        self.ROS_FACTOR = BoneConfig.METABOLISM.ROS_GENERATION_FACTOR
        if inherited_traits:
            self._apply_inheritance(inherited_traits)

    def _apply_inheritance(self, traits: Dict):
        self.state.efficiency_mod = traits.get("efficiency_mod", 1.0)
        self.state.ros_resistance = traits.get("ros_resistance", 1.0)
        if "enzymes" in traits:
            self.state.enzymes = set(traits["enzymes"])
            self.events.log(f"{Prisma.CYN}[MITO]: Inherited Enzymes: {list(self.state.enzymes)}.{Prisma.RST}")

    def adapt(self, final_health: float) -> Dict:
        traits = {
            "efficiency_mod": self.state.efficiency_mod,
            "ros_resistance": self.state.ros_resistance,
            "enzymes": list(self.state.enzymes)}
        if final_health <= 0 and random.random() < 0.3:
            traits["ros_resistance"] = round(traits.get("ros_resistance", 1.0) + 0.1, 2)
        return traits

    def calculate_metabolism(self, drag: float, external_modifiers: Optional[List[float]] = None) -> MetabolicReceipt:
        limit = BoneConfig.MAX_DRAG_LIMIT
        safe_drag = max(0.0, drag)
        taxable_drag = max(0.0, safe_drag - self.GRACE)
        if taxable_drag <= (limit - self.GRACE):
            drag_tax = taxable_drag * self.TAX_LOW
        else:
            base_tax = (limit - self.GRACE) * self.TAX_LOW
            excess_drag = taxable_drag - (limit - self.GRACE)
            drag_tax = base_tax + (excess_drag * self.TAX_HIGH)
        if external_modifiers:
            for mod in external_modifiers:
                drag_tax *= mod
        raw_cost = self.BMR + drag_tax
        safe_efficiency = max(0.1, self.state.efficiency_mod)
        final_cost = raw_cost / safe_efficiency
        inefficiency_tax = 0.0
        if safe_efficiency < 1.0:
            inefficiency_tax = final_cost - raw_cost
        status = "RESPIRING"
        symptom = "Humming along."
        if final_cost > self.state.atp_pool:
            status = "NECROSIS"
            symptom = f"The engine is stalling. Requires {final_cost:.1f} ATP (Available: {self.state.atp_pool:.1f})."
        elif self.state.ros_buildup > BoneConfig.CRITICAL_ROS_LIMIT:
            status = self.APOPTOSIS_TRIGGER
            symptom = "Cellular suicide initiated. Too much noise."
        elif drag_tax > 3.0:
            symptom = "The gears are grinding. Heavy metabolic load."
        return MetabolicReceipt(
            base_cost=round(self.BMR, 2),
            drag_tax=round(drag_tax, 2),
            inefficiency_tax=round(inefficiency_tax, 2),
            total_burn=round(final_cost, 2),
            status=status,
            symptom=symptom)

    def respirate(self, receipt: MetabolicReceipt) -> str:
        if receipt.status == "NECROSIS":
            self.state.atp_pool = 0.0
            return "NECROSIS"
        if receipt.status == self.APOPTOSIS_TRIGGER:
            self.krebs_cycle_active = False
            self.state.atp_pool = 0.0
            return self.APOPTOSIS_TRIGGER
        self.state.atp_pool -= receipt.total_burn
        ros_generation = receipt.total_burn * self.ROS_FACTOR * (1.0 / self.state.ros_resistance)
        self.state.ros_buildup += ros_generation
        return "RESPIRING"

class SomaticLoop:
    def __init__(self, bio_system_ref: BioSystem, memory_ref=None, lexicon_ref=None, gordon_ref=None, folly_ref=None, events_ref=None):
        self.bio = bio_system_ref
        self.mem = memory_ref
        self.lex = lexicon_ref
        self.gordon = gordon_ref
        self.folly = folly_ref
        self.events = events_ref
        self.taxes = {
            "existential_drag": 0.05,
            "metabolic_base": 0.1
        }

    def process_turn(self, text: str, physics: Any, feedback: Dict, tick_count: int,
                     health: float = 100.0, stamina: float = 100.0) -> Dict:
        stress_modifier = self.bio.governor.calculate_stress(
            health,
            self.bio.mito.state.ros_buildup
        )
        circadian_bias = self.bio.shimmer.get_bias() if self.bio.shimmer else None
        return self.digest_cycle(
            text, physics, feedback,
            health, stamina, stress_modifier, tick_count,
            circadian_bias=circadian_bias
        )

    def digest_cycle(self, text: str, physics_data: Any, feedback: Dict,
                     health: float, stamina: float, stress_mod: float,
                     tick_count: int = 0, circadian_bias: Dict = None) -> Dict:
        if hasattr(physics_data, "dimensions"):
            phys = {
                "voltage": physics_data.tension,
                "drag": physics_data.compression,
                "counts": {},
                "vector": physics_data
            }
        else:
            phys = self._normalize_physics(physics_data)
        logs = []
        receipt = self._calculate_taxes(phys, logs)
        resp_status = self.bio.mito.respirate(receipt)
        if self._audit_folly_desire(phys, stamina, logs) == "MAUSOLEUM_CLAMP":
            return self._package_result(resp_status, logs, enzyme="NONE")
        enzyme, total_yield = self._harvest_resources(text, phys, logs, tick_count)
        self.bio.mito.state.atp_pool += total_yield
        self._perform_maintenance(phys, logs, tick_count)
        chem_state = self.bio.endo.metabolize(
            feedback,
            health,
            stamina,
            self.bio.mito.state.ros_buildup,
            harvest_hits=self._count_harvest_hits(phys),
            stress_mod=stress_mod,
            enzyme_type=enzyme,
            circadian_bias=circadian_bias
        )
        return self._package_result(resp_status, logs, chem_state, enzyme)

    def _normalize_physics(self, physics_packet: Any) -> Dict:
        if isinstance(physics_packet, dict):
            return {
                "voltage": physics_packet.get("voltage", 0.0),
                "drag": physics_packet.get("narrative_drag", 0.0),
                "counts": physics_packet.get("counts", {})
            }
        return {"voltage": 0.0, "drag": 0.0, "counts": {}}

    def _calculate_taxes(self, phys, logs) -> MetabolicReceipt:
        base = self.taxes["metabolic_base"]
        drag_tax = phys.get("drag", 0.0) * 0.5
        inefficiency = 0.0
        if phys.get("voltage", 0) > 10.0:
            inefficiency += 0.2
            logs.append(f"{Prisma.RED}High Voltage Tax{Prisma.RST}")
        total = base + drag_tax + inefficiency
        return MetabolicReceipt(base, drag_tax, inefficiency, total, "CALCULATED")

    def _audit_folly_desire(self, phys, stamina, logs) -> str:
        if stamina <= 0:
            logs.append(f"{Prisma.RED}SYSTEM EXHAUSTION{Prisma.RST}")
            return "MAUSOLEUM_CLAMP"
        return "CLEAR"

    def _harvest_resources(self, text, phys, logs, tick) -> Tuple[str, float]:
        if "voltage" in phys and phys["voltage"] > 5.0:
            return "ADRENALINE", 5.0
        return "NONE", 0.0

    def _perform_maintenance(self, phys, logs, tick):
        pass

    def _count_harvest_hits(self, phys):
        return 0

    def _package_result(self, resp_status, logs, chem_state=None, enzyme="NONE"):
        return {
            "respiration": resp_status,
            "logs": logs,
            "chemistry": chem_state or {},
            "enzyme": enzyme
        }

@dataclass
class EndocrineSystem:
    dopamine: float = 0.5
    oxytocin: float = 0.1
    cortisol: float = 0.0
    serotonin: float = 0.5
    adrenaline: float = 0.0
    melatonin: float = 0.0
    glimmers: int = 0

    def _clamp(self, val: float) -> float:
        return max(0.0, min(1.0, val))

    def calculate_circadian_bias(self) -> Tuple[Dict[str, float], Optional[str]]:
        hour = time.localtime().tm_hour
        bias = {"COR": 0.0, "SER": 0.0, "MEL": 0.0}
        msg = None
        if 6 <= hour < 10:
            bias["COR"] = 0.1
            msg = "Dawn Protocol: Cortisol rising."
        elif 10 <= hour < 18:
            bias["SER"] = 0.1
            msg = "Solar Cycle: Serotonin dominant."
        elif 18 <= hour < 23:
            bias["MEL"] = 0.1
            msg = "Twilight Protocol: Melatonin rising."
        else:
            bias["MEL"] = 0.3
            bias["COR"] = -0.1
            msg = "Lunar Cycle: Melatonin max."
        return bias, msg

    def _apply_enzyme_reaction(self, enzyme_type: str, harvest_hits: int):
        if harvest_hits > 0:
            satiety_dampener = max(0.1, 1.0 - self.dopamine)
            base_reward = math.log(harvest_hits + 1) * 0.15
            final_reward = base_reward * satiety_dampener
            self.dopamine += final_reward
            self.cortisol -= (final_reward * 0.4)

        reactions = {
            "PROTEASE":   {"ADR": BoneConfig.BIO.REWARD_MEDIUM},
            "CELLULASE":  {"COR": -BoneConfig.BIO.REWARD_MEDIUM, "OXY": BoneConfig.BIO.REWARD_SMALL},
            "CHITINASE":  {"DOP": BoneConfig.BIO.REWARD_LARGE},
            "LIGNASE":    {"SER": BoneConfig.BIO.REWARD_MEDIUM},
            "DECRYPTASE": {"ADR": BoneConfig.BIO.REWARD_SMALL, "DOP": BoneConfig.BIO.REWARD_SMALL},
            "AMYLASE":    {"SER": BoneConfig.BIO.REWARD_LARGE, "OXY": BoneConfig.BIO.REWARD_MEDIUM}
        }
        if enzyme_type in reactions:
            impact = reactions[enzyme_type]
            if "ADR" in impact: self.adrenaline += impact["ADR"]
            if "COR" in impact: self.cortisol += impact["COR"]
            if "OXY" in impact: self.oxytocin += impact["OXY"]
            if "DOP" in impact: self.dopamine += impact["DOP"]
            if "SER" in impact: self.serotonin += impact["SER"]

    def _apply_environmental_pressure(self, feedback: Dict, health: float, stamina: float, ros_level: float, stress_mod: float):
        if feedback.get("STATIC", 0) > 0.6:
            self.cortisol += (BoneConfig.BIO.REWARD_LARGE * stress_mod)

        if feedback.get("INTEGRITY", 0) > 0.8:
            self.dopamine += BoneConfig.BIO.REWARD_MEDIUM
        else:
            self.dopamine -= BoneConfig.BIO.DECAY_RATE

        if stamina < 20.0:
            self.cortisol += (BoneConfig.BIO.REWARD_MEDIUM * stress_mod)
            self.dopamine -= BoneConfig.BIO.REWARD_MEDIUM

        if ros_level > 20.0:
            self.cortisol += (BoneConfig.BIO.REWARD_LARGE * stress_mod)

        if health < 30.0 or feedback.get("STATIC", 0) > 0.8:
            self.adrenaline += (BoneConfig.BIO.REWARD_LARGE * stress_mod)
        else:
            self.adrenaline -= (BoneConfig.BIO.DECAY_RATE * 5)

    def _maintain_homeostasis(self, social_context: bool):
        if self.serotonin > 0.6:
            self.cortisol -= BoneConfig.BIO.REWARD_SMALL

        if social_context:
            self.oxytocin += BoneConfig.BIO.REWARD_MEDIUM
            self.cortisol -= BoneConfig.BIO.REWARD_MEDIUM
        elif self.serotonin > 0.7 and self.cortisol < 0.3:
            self.oxytocin += BoneConfig.BIO.REWARD_SMALL

        if self.cortisol > 0.7 and not social_context:
            self.oxytocin -= BoneConfig.BIO.REWARD_SMALL

        if self.oxytocin > 0.6:
            self.cortisol -= BoneConfig.BIO.REWARD_LARGE

        if self.adrenaline < 0.2:
            self.melatonin += (BoneConfig.BIO.REWARD_SMALL / 2)
        else:
            self.melatonin = 0.0

    def check_for_glimmer(self, feedback: Dict, harvest_hits: int) -> Optional[str]:
        if feedback.get("INTEGRITY", 0) > 0.9 and feedback.get("STATIC", 0) < 0.2:
            self.glimmers += 1
            self.serotonin += 0.2
            return "GLIMMER: Perfect structural integrity detected. A moment of zen."
        if harvest_hits > 2 and self.dopamine > 0.8:
            self.glimmers += 1
            self.oxytocin += 0.2
            return "GLIMMER: Infectious enthusiasm detected. The work is good."
        return None

    def metabolize(self, feedback: Dict, health: float, stamina: float, ros_level: float = 0.0,
                   social_context: bool = False, enzyme_type: Optional[str] = None,
                   harvest_hits: int = 0, stress_mod: float = 1.0,
                   circadian_bias: Dict[str, float] = None) -> Dict[str, Any]:
        self._apply_enzyme_reaction(enzyme_type, harvest_hits)
        self._apply_environmental_pressure(feedback, health, stamina, ros_level, stress_mod)
        self._maintain_homeostasis(social_context)
        if circadian_bias:
            self.cortisol += circadian_bias.get("COR", 0.0)
            self.serotonin += circadian_bias.get("SER", 0.0)
            self.melatonin += circadian_bias.get("MEL", 0.0)
        glimmer_msg = self.check_for_glimmer(feedback, harvest_hits)
        self.dopamine = self._clamp(self.dopamine)
        self.oxytocin = self._clamp(self.oxytocin)
        self.cortisol = self._clamp(self.cortisol)
        self.serotonin = self._clamp(self.serotonin)
        self.adrenaline = self._clamp(self.adrenaline)
        self.melatonin = self._clamp(self.melatonin)
        state: Dict[str, Any] = self.get_state()
        if glimmer_msg:
            state["glimmer_msg"] = glimmer_msg
        return state

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
    GRACE_PERIOD: int = 5
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

    def calculate_stress(self, health: float, ros_buildup: float) -> float:
        base_stress = 1.0
        if health < 50.0:
            base_stress += (50.0 - health) * 0.02
        if ros_buildup > 50.0:
            base_stress += (ros_buildup - 50.0) * 0.01
        return round(min(3.0, base_stress), 2)

    def set_override(self, target_mode):
        valid = {"COURTYARD", "LABORATORY", "FORGE", "SANCTUARY"}
        if target_mode in valid:
            self.mode = target_mode
            self.manual_override = True
            return f"MANUAL OVERRIDE: System locked to {target_mode}."
        return "INVALID MODE."

    def shift(self, physics: Dict, _voltage_history: List[float], current_tick: int = 0) -> Optional[str]:
        if current_tick <= 5:
            physics["voltage"] = min(physics.get("voltage", 0.0), 8.0)
            physics["narrative_drag"] = min(physics.get("narrative_drag", 0.0), 3.0)
            physics["system_surge_event"] = False
            if self.mode != "COURTYARD":
                self.mode = "COURTYARD"
            return None
        current_voltage = physics.get("voltage", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        beta = physics.get("beta_index", 0.0)
        if current_voltage > 15.0 and beta > 1.5:
            if self.mode != "SANCTUARY":
                self.mode = "SANCTUARY"
                physics["narrative_drag"] = 0.0
                return f"{Prisma.GRN}GOVERNOR: VSL Critical (β: {beta:.2f}). Entering SANCTUARY.{Prisma.RST}"
        if current_voltage > 10.0:
            if self.mode != "FORGE":
                self.mode = "FORGE"
                return f"{Prisma.RED}GOVERNOR: High Voltage ({current_voltage:.1f}v). Locking to FORGE.{Prisma.RST}"
        if drag > 4.0 > current_voltage:
            if self.mode != "LABORATORY":
                self.mode = "LABORATORY"
                return f"{Prisma.CYN}GOVERNOR: High Drag detected. Restricting to LABORATORY.{Prisma.RST}"
        if self.mode != "COURTYARD":
            if current_voltage < 5.0 and drag < 2.0:
                self.mode = "COURTYARD"
                return f"{Prisma.GRN}GOVERNOR: All Clear. Relaxing to COURTYARD.{Prisma.RST}"
        return None

class ViralTracer:
    def __init__(self, mem):
        self.mem = mem
        self.max_depth = 4

    @staticmethod
    def _is_ruminative(word):
        return (word in TheLexicon.get("abstract")) or (
                word in TheLexicon.get("antigen"))

    def inject(self, start_node):
        if start_node not in self.mem.graph:
            return None
        if not self._is_ruminative(start_node):
            return None
        path = [start_node]
        return self._walk(start_node, path, self.max_depth)

    def _walk(self, current, path, moves_left, visited=None):
        if visited is None:
            visited = set()
        if moves_left == 0 or current in visited:
            return None
        visited.add(current)
        edges = self.mem.graph.get(current, {}).get("edges", {})
        ruminative_edges = [
            n for n, w in edges.items() if w >= 1 and self._is_ruminative(n)]
        for next_node in ruminative_edges:
            if next_node in path:
                return path + [next_node]
            result = self._walk(next_node, path + [next_node], moves_left - 1)
            if result:
                return result
        return None

    def psilocybin_rewire(self, loop_path):
        if len(loop_path) < 2:
            return None
        node_a = loop_path[0]
        node_b = loop_path[1]
        if node_b in self.mem.graph[node_a]["edges"]:
            self.mem.graph[node_a]["edges"][node_b] = 0
        sensory = TheLexicon.harvest("photo")
        action = TheLexicon.harvest("kinetic")
        if sensory == "void" or action == "void":
            return "GRAFT FAILED: Missing Lexicon Data."
        if node_a not in self.mem.graph:
            self.mem.graph[node_a] = {"edges": {}, "last_tick": 0}
        self.mem.graph[node_a]["edges"][sensory] = 5
        if sensory not in self.mem.graph:
            self.mem.graph[sensory] = {"edges": {}, "last_tick": 0}
        self.mem.graph[sensory]["edges"][action] = 5
        if action not in self.mem.graph:
            self.mem.graph[action] = {"edges": {}, "last_tick": 0}
        self.mem.graph[action]["edges"][node_b] = 5
        return f"PSILOCYBIN REWIRE: Broken Loop '{node_a}↔{node_b}'. Grafted '{sensory}'(S) -> '{action}'(A)."

class ThePacemaker:
    def __init__(self):
        self.history = deque(maxlen=5)
        self.repetition_score = 0.0
        self.last_tick_time = time.time()
        self.boredom_level = 0.0

    def check_pulse(self, clean_words: List[str]) -> float:
        if not clean_words: return 0.0
        current_set = set(clean_words)
        overlaps = 0
        for old_words in self.history:
            old_set = set(old_words)
            intersection = len(current_set & old_set)
            union = len(current_set | old_set)
            if union > 0: overlaps += (intersection / union)
        self.history.append(clean_words)
        self.repetition_score = min(1.0, overlaps / max(1, len(self.history)))
        now = time.time()
        delta = now - self.last_tick_time
        self.last_tick_time = now
        if self.repetition_score > 0.3:
            self.boredom_level += 2.0
        elif delta > 60:
            self.boredom_level += 5.0
        else:
            self.boredom_level = max(0.0, self.boredom_level - 1.0)
        return self.repetition_score

    def get_status(self):
        if self.repetition_score > BoneConfig.MAX_REPETITION_LIMIT: return "ZOMBIE_KNOCK"
        elif self.repetition_score > 0.2: return "ECHO"
        return "CLEAR"

    def is_bored(self):
        return self.boredom_level > BoneConfig.BOREDOM_THRESHOLD

class NoeticLoop:
    def __init__(self, mind_layer, bio_layer, events):
        self.mind = mind_layer
        self.bio = bio_layer
        self.arbiter = SynergeticLensArbiter(events)

    def think(self, physics_packet, bio_result_dict, inventory, voltage_history, tick_count):
        volts = physics_packet.get("voltage", 0.0)
        drag = physics_packet.get("narrative_drag", 0.0)
        if volts < 1.5 and drag < 1.5:
            stripped_thought = TheLexicon.walk_gradient(physics_packet["raw_text"])
            return {
                "mode": "COGNITIVE",
                "lens": "GRADIENT_WALKER",
                "thought": f"ECHO: {stripped_thought}",
                "role": "The Reducer",
                "ignition": 0.0,
                "hebbian_msg": None}
        ignition_score, _, _ = self.mind.integrator.measure_ignition(
            physics_packet["clean_words"],
            voltage_history)
        lens_name, lens_msg, lens_role = self.arbiter.consult(
            physics_packet,
            self.bio,
            inventory,
            tick_count,
            ignition_score)
        hebbian_msg = None
        if physics_packet["voltage"] > 12.0 and len(physics_packet["clean_words"]) >= 2:
            if random.random() < 0.15:
                w1, w2 = random.sample(physics_packet["clean_words"], 2)
                hebbian_msg = self.bio.plasticity.force_hebbian_link(self.mind.mem.graph, w1, w2)
        return {
            "mode": "COGNITIVE",
            "lens": lens_name,
            "thought": lens_msg,
            "role": lens_role,
            "ignition": ignition_score,
            "hebbian_msg": hebbian_msg}