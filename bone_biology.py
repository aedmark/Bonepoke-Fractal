# bone_biology.py
# Subsystems for BONEAMANITA 9.4.5
# Extracted during Operation Cell Division

import math
import time
import random
from collections import deque
from dataclasses import dataclass, field
from bone_shared import Prisma, TheLexicon, BoneConfig

# --- MITOCHONDRIA ---
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
    BASE_EFFICIENCY = 0.85
    APOPTOSIS_TRIGGER = "CYTOCHROME_C_RELEASE"

    def __init__(self, lineage_seed: str, events, inherited_traits: dict = None):
        self.state = MitochondrialState(mother_hash=lineage_seed)
        self.events = events
        self.krebs_cycle_active = True
        if inherited_traits:
            self.state.efficiency_mod = inherited_traits.get("efficiency_mod", 1.0) 
            self.state.ros_resistance = inherited_traits.get("ros_resistance", 1.0)
            if "enzymes" in inherited_traits:
                self.state.enzymes = set(inherited_traits["enzymes"])
                self.events.log(f"{Prisma.CYN}[MITOCHONDRIA]: Inherited Enzymes for {list(self.state.enzymes)}.{Prisma.RST}")
            if self.state.efficiency_mod > 1.0:
                self.events.log(f"{Prisma.GRN}[MITOCHONDRIA]: Inherited High-Efficiency Matrix ({self.state.efficiency_mod:.2f}x).{Prisma.RST}")
            if self.state.ros_resistance > 1.0:
                self.events.log(f"{Prisma.CYN}[MITOCHONDRIA]: Inherited Thickened Membrane (Resist: {self.state.ros_resistance:.2f}x).{Prisma.RST}")

    def develop_enzyme(self, word, current_tick): 
        if word not in self.state.enzymes:
            self.state.enzymes.add(word)
            self.state.efficiency_mod = min(2.5, self.state.efficiency_mod + 0.05)
            TheLexicon.teach(word, "enzyme", current_tick)
            self.events.log(f"{Prisma.MAG}ADRENALINE BRIDGE: '{word.upper()}' Synthesized. Timestamped: {current_tick}.{Prisma.RST}")
            return True
        return False

    def adapt(self, current_health, kappa=1.0):
        mutations = {"hypertrophy_event": False}
        evolution_threshold = 85.0 
        growth_threshold = 70.0
        if self.state.atp_pool > evolution_threshold:
            cost = 30.0
            self.state.atp_pool -= cost
            mutations["hypertrophy_event"] = True
            self.events.log(f"{Prisma.MAG}MITOCHONDRIAL HYPERTROPHY: Burning {cost} ATP to force Evolutionary Growth.{Prisma.RST}")
        if self.state.atp_pool > growth_threshold and kappa > 0.5:
            self.state.efficiency_mod = min(3.0, self.state.efficiency_mod * 1.02)
        else:
            self.state.efficiency_mod = max(0.5, self.state.efficiency_mod * 0.995)
        if self.state.ros_buildup > 40.0 and current_health > 60.0:
            self.state.ros_resistance = min(2.5, self.state.ros_resistance + 0.05)
        mutations["efficiency_mod"] = self.state.efficiency_mod
        mutations["ros_resistance"] = self.state.ros_resistance
        mutations["enzymes"] = list(self.state.enzymes)
        return mutations

    def spend(self, cost: float) -> bool:
        if self.state.atp_pool >= cost:
            self.state.atp_pool -= cost
            return True
        return False

    def mitigate(self, antioxidant_level: float):
        cleansed = min(self.state.ros_buildup, antioxidant_level)
        self.state.ros_buildup -= cleansed
        return f"ANTIOXIDANT FLUSH: -{cleansed:.1f} ROS"

    def prune_dead_enzymes(self, active_lexicon: set):
        dead = [e for e in self.state.enzymes if e not in active_lexicon]
        if dead:
            for d in dead:
                self.state.enzymes.remove(d)
                self.state.efficiency_mod = max(0.8, self.state.efficiency_mod - 0.05)
            self.events.log(f"{Prisma.GRY}METABOLIC GRIEF: Forgot enzymes {dead}. Efficiency dropped to {self.state.efficiency_mod:.2f}x.{Prisma.RST}")

    def check_senescence(self, voltage):
        burn = 1
        if voltage > 15.0:
            burn = 5
            self.state.efficiency_mod = min(3.0, self.state.efficiency_mod * 1.05)
        self.state.telomeres -= burn 
        if self.state.telomeres <= 20 and self.state.telomeres > 0:
            if self.state.telomeres % 5 == 0:
                self.events.log(f"{Prisma.YEL}SENESCENCE WARNING: Telomeres at {self.state.telomeres}%. The end is close.{Prisma.RST}")
        if self.state.telomeres <= 0:
            return "APOPTOSIS_SENESCENCE"
        return None

    def _trigger_apoptosis(self):
        self.krebs_cycle_active = False
        self.state.atp_pool = 0.0
        return self.APOPTOSIS_TRIGGER

    def respirate(self, drag, has_bracelet=False, is_hybrid=False):
        tuned_multiplier = 1.5 
        base_cost = 2.0 + (drag * tuned_multiplier)
        if has_bracelet:
            base_cost *= 0.5
        if is_hybrid:
            base_cost *= 0.8
        final_cost = base_cost / self.state.efficiency_mod
        final_cost = min(30.0, final_cost)
        if self.state.atp_pool < final_cost:
            self.state.atp_pool = 0
            return "NECROSIS"
        self.state.atp_pool -= final_cost
        if self.state.ros_buildup > BoneConfig.CRITICAL_ROS_LIMIT:
            return self._trigger_apoptosis()
        return "RESPIRING"

# --- DIGESTION & IMMUNITY ---
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
            original_yield = nutrient_profile["yield"]
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
    def _digest_encrypted(text=None):
        return {"type": "ENCRYPTED", "yield": 25.6, "toxin": 2.0, "desc": "Barometric Data (High Resource Allocation)"}

    @staticmethod
    def _digest_narrative(text=None):
        return {"type": "NARRATIVE", "yield": 5.0, "toxin": -2.0, "desc": "Soft Cellulose", }

    @staticmethod
    def _digest_intent(text=None):
        return {"type": "BIOLOGICAL", "yield": 8.0, "toxin": 0.0, "desc": "Raw Meat (User Intent)", }

    @staticmethod
    def _digest_complex(text=None):
        return {"type": "COMPLEX", "yield": 20.0, "toxin": 8.0, "desc": "Chitin (Structured Intent / Poetry)", }

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

# --- SYMBIONTS ---
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

# --- HORMONES ---
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
    
    def get_stress_modifier(self, tick_count):
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