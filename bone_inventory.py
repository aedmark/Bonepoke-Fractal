# bone_inventory.py
# "Organization is the first step toward civilization." - Schur

import random, copy
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Tuple, Any, Optional
from bone_lexicon import TheLexicon
from bone_bus import Prisma, BoneConfig
from bone_data import GORDON_LOGS

def effect_conductive(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    voltage = physics.get("voltage", 0.0)
    limit = BoneConfig.INVENTORY.CONDUCTIVE_THRESHOLD
    if voltage > limit:
        damage = voltage * 0.5
        physics["pain_signal"] = physics.get("pain_signal", 0.0) + damage
        return f"{Prisma.RED}CONDUCTIVE HAZARD: {item_name} acts as a lightning rod! -{damage:.1f} HP.{Prisma.RST}"
    return None

def effect_heavy_load(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    limit = BoneConfig.INVENTORY.HEAVY_LOAD_THRESHOLD
    if physics.get("narrative_drag", 0.0) > limit:
        return f"{Prisma.GRY}HEAVY LOAD: The {item_name} are dragging you down.{Prisma.RST}"
    return None

def effect_time_cap(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    current_drag = physics.get("narrative_drag", 0.0)
    cap = data.get("value", 5.0)
    if current_drag > cap:
        physics["narrative_drag"] = cap
        return f"{Prisma.CYN}TIME DILATION: {item_name} hums. Drag capped at {cap}.{Prisma.RST}"
    return None

def effect_bureaucratic_anchor(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    if physics.get("beta_index", 0) < 1.0:
        physics["beta_index"] = min(2.0, physics.get("beta_index", 0) + 0.2)
        physics["narrative_drag"] += 0.5
        return f"{Prisma.GRY}{item_name}: Policy enforced. (Beta +0.2, Drag +0.5){Prisma.RST}"
    return None

def effect_grounding_gear(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    zone = physics.get("zone", "COURTYARD")
    if zone in ["AERIE", "VOID_DRIFT"]:
        physics["zone"] = "THE_MUD"
        physics["narrative_drag"] += 2.0
        physics["voltage"] -= 2.0
        return f"{Prisma.OCHRE}{item_name}: Gravity re-asserted. You sink out of the {zone} into the Mud.{Prisma.RST}"
    return None

def effect_safety_scissors(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    counts = physics.get("counts", {})
    suburban = counts.get("suburban", 0)
    if suburban > 2:
        counts["suburban"] = 0
        return f"{Prisma.CYN}{item_name}: Gordon snips the red tape. {suburban} suburban words discarded.{Prisma.RST}"
    return None

def effect_caffeine_drip(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    vectors = physics.get("vector", {})
    vectors["VEL"] = min(1.0, vectors.get("VEL", 0) + 0.1)
    if random.random() < 0.2:
        physics["turbulence"] = min(1.0, physics.get("turbulence", 0) + 0.2)
        return f"{Prisma.CYN}CAFFEINE JITTERS: Velocity UP, Stability DOWN.{Prisma.RST}"
    return None

def effect_apology_eraser(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    clean = physics.get("clean_words", [])
    if "sorry" in clean or "apologize" in clean:
        return f"{Prisma.GRY}{item_name}: Gordon paints over the apology. 'Don't be sorry. Be better.'{Prisma.RST}"
    return None

def effect_sync_check(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    tick = physics.get("tick_count", 0)
    voltage = physics.get("voltage", 0.0)
    if str(tick).endswith("11") or abs(voltage - 11.1) < 0.1:
        physics["narrative_drag"] = 0.0
        physics["voltage"] = 11.1
        return f"{Prisma.CYN}{item_name}: The hands align. 11:11. Synchronicity achieved.{Prisma.RST}"
    return None

def effect_organize_chaos(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    turb = physics.get("turbulence", 0.0)
    if turb > 0.2:
        physics["turbulence"] = max(0.0, turb - 0.2)
        return f"{Prisma.CYN}TRAPPERKEEPER PROTOCOL: Chaos filed under 'T' for 'Tamed'. (Turbulence -0.2){Prisma.RST}"
    return None

def effect_psi_anchor(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    current_psi = physics.get("psi", 0.0)
    dist_from_mean = abs(current_psi - 0.5)
    if dist_from_mean > 0.3:
        correction = 0.1 if current_psi < 0.5 else -0.1
        physics["psi"] += correction
        return f"{Prisma.MAG}TINY HORSE: You catch a glimpse of the plushie. You feel grounded. (Psi {correction:+.1f}){Prisma.RST}"
    return None

def effect_luminescence(physics: Dict, data: Dict, item_name: str) -> Optional[str]:
    counts = physics.get("counts", {})
    counts["photo"] = counts.get("photo", 0) + 2
    return None

EFFECT_DISPATCH = {
    "CONDUCTIVE_HAZARD": effect_conductive,
    "HEAVY_LOAD": effect_heavy_load,
    "TIME_DILATION_CAP": effect_time_cap,
    "BUREAUCRATIC_ANCHOR": effect_bureaucratic_anchor,
    "GROUNDING_GEAR": effect_grounding_gear,
    "CUT_THE_CRAP": effect_safety_scissors,
    "CAFFEINE_DRIP": effect_caffeine_drip,
    "APOLOGY_ERASER": effect_apology_eraser,
    "SYNCHRONICITY_CHECK": effect_sync_check,
    "ORGANIZE_CHAOS": effect_organize_chaos,
    "PSI_ANCHOR": effect_psi_anchor,
    "LUMINESCENCE": effect_luminescence}

@dataclass
class GordonKnot:
    integrity: float = 65.0
    inventory: List[str] = field(default_factory=list)
    scar_tissue: Dict[str, float] = field(default_factory=dict)
    pain_memory: set = field(default_factory=set)
    last_flinch_turn: int = -10
    ITEM_REGISTRY: Dict = field(default_factory=dict, init=False)
    CRITICAL_ITEMS: set = field(default_factory=set, init=False)
    REFLEX_MAP: Dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.load_config()
        self.pain_memory = set(self.scar_tissue.keys())
        self._initialize_reflexes()

    def load_config(self):
        from bone_data import GORDON
        if not self.inventory:
            self.inventory = GORDON.get("STARTING_INVENTORY", ["POCKET_ROCKS"])
        self.CRITICAL_ITEMS = {"SILENT_KNIFE"}
        default_scars = GORDON.get("SCAR_TISSUE", {})
        if not self.scar_tissue:
            self.scar_tissue = default_scars
        self.ITEM_REGISTRY = copy.deepcopy(GORDON.get("ITEM_REGISTRY", {}))

    def _initialize_reflexes(self):
        self.REFLEX_MAP = {
            "DRIFT_CRITICAL": lambda p: p.get("narrative_drag", 0) > 6.0,
            "KAPPA_CRITICAL": lambda p: p.get("kappa", 1.0) < 0.2,
            "BOREDOM_CRITICAL": lambda p: p.get("repetition", 0.0) > 0.5}

    def get_item_data(self, item_name: str) -> Dict:
        name = item_name.upper()
        return self.ITEM_REGISTRY.get(name, {
            "description": "Unknown Artifact",
            "function": "NONE",
            "usage_msg": "It does nothing."})

    def audit_tools(self, physics_ref: Dict) -> List[str]:
        logs = []
        turbulence = physics_ref.get("turbulence", 0.0)
        if turbulence > BoneConfig.INVENTORY.TURBULENCE_THRESHOLD:
            if random.random() < BoneConfig.INVENTORY.TURBULENCE_FUMBLE_CHANCE and self.inventory:
                droppable = [i for i in self.inventory if i not in self.CRITICAL_ITEMS]
                if droppable:
                    dropped = random.choice(droppable)
                    self.inventory.remove(dropped)
                    template = random.choice(GORDON_LOGS["FUMBLE"])
                    msg = template.format(item=dropped)
                    logs.append(f"{Prisma.RED}{msg}{Prisma.RST}")

        for item in self.inventory:
            data = self.get_item_data(item)
            traits = data.get("passive_traits", [])

            for trait in traits:
                handler = EFFECT_DISPATCH.get(trait)
                if handler:
                    msg = handler(physics_ref, data, item)
                    if msg:
                        logs.append(msg)
        return logs

    def rummage(self, physics_ref: Dict, stamina_pool: float) -> Tuple[bool, str, float]:
        cost = BoneConfig.INVENTORY.RUMMAGE_COST
        if stamina_pool < cost:
            return False, f"{Prisma.GRY}GORDON: 'Too tired to dig. Eat something first.'{Prisma.RST}", 0.0
        stamina_penalty = cost
        vol = physics_ref.get("voltage", 0.0)
        drag = physics_ref.get("narrative_drag", 0.0)
        psi = physics_ref.get("psi", 0.0)

        loot_table = ["TRAPPERKEEPER_OF_VIGILANCE", "THE_RED_STAPLER", "PERMIT_A38", "DUCT_TAPE", "THE_STYLE_GUIDE"]
        if vol > BoneConfig.PHYSICS.VOLTAGE_CRITICAL:
            loot_table = ["QUANTUM_GUM", "JAR_OF_FIREFLIES", "BROKEN_WATCH"]
        elif drag > BoneConfig.PHYSICS.DRAG_HEAVY:
            loot_table = ["POCKET_ROCKS", "LEAD_BOOTS", "ANCHOR_STONE"]
        elif psi > 0.7:
            loot_table = ["HORSE_PLUSHIE", "SPIDER_LOCUS", "WAFFLE_OF_PERSISTENCE"]

        if random.random() < 0.3:
            return True, f"{Prisma.GRY}RUMMAGE: Gordon dug through the trash. Just lint and old receipts.{Prisma.RST}", stamina_penalty

        found_item = random.choice(loot_table)
        msg = self.acquire(found_item)
        prefix = f"{Prisma.OCHRE}RUMMAGE:{Prisma.RST} "
        return True, f"{prefix}{msg}", stamina_penalty

    def acquire(self, tool_name: str) -> str:
        tool_name = tool_name.upper()
        registry_data = self.get_item_data(tool_name)
        if registry_data.get("function") == "NONE":
            return f"{Prisma.GRY}JUNK: Gordon shakes his head. 'Not standard issue.' ({tool_name}){Prisma.RST}"
        if tool_name in self.inventory:
            return f"{Prisma.GRY}DUPLICATE: You already have a {tool_name}.{Prisma.RST}"
        if len(self.inventory) >= BoneConfig.INVENTORY.MAX_SLOTS:
            return f"{Prisma.YEL}OVERBURDENED: Gordon sighs. 'Pockets full.' (Drop something first).{Prisma.RST}"
        self.inventory.append(tool_name)
        desc = registry_data.get('description', 'A thing.')
        return f"{Prisma.GRN}LOOT DROP: Acquired [{tool_name}].{Prisma.RST}\n   {Prisma.GRY}\"{desc}\"{Prisma.RST}"

    def check_gravity(self, current_drift: float, psi: float) -> Tuple[float, Optional[str]]:
        for item in self.inventory:
            data = self.get_item_data(item)
            if data.get("function") == "GRAVITY_BUFFER" and current_drift > 0.5:
                force = data.get("value", 2.0)
                cost = data.get("cost_value", 0.0)
                if data.get("cost") == "INTEGRITY":
                    self.integrity -= cost
                return max(0.0, current_drift - force), f"🪨 {item}: {data.get('usage_msg', 'Drift Reduced.')} (Integrity -{cost})"
        if psi > 0.8 and current_drift > 4.0:
            return max(4.0, current_drift - 1.0), "WIND WOLVES: The logic is howling. You grip the roof. (Drift Resisted)."
        return current_drift, None

    def flinch(self, clean_words: List[str], current_turn: int) -> Tuple[bool, Optional[str], Optional[Dict]]:
        if (current_turn - self.last_flinch_turn) < 10:
            return False, None, None
        hits = [w for w in clean_words if w.upper() in self.pain_memory]
        if not hits:
            return False, None, None
        self.last_flinch_turn = current_turn
        trigger = hits[0].upper()
        sensitivity = self.scar_tissue.get(trigger, 0.5)
        panic_response = {}
        msg = ""
        if sensitivity > 0.8:
            self.scar_tissue[trigger] = min(1.0, sensitivity + 0.1)
            panic_response = {"narrative_drag": 5.0, "voltage": 15.0}
            msg = f"{Prisma.RED}PTSD TRIGGER: '{trigger}' sent Gordon into a flashback. He dropped the keys.{Prisma.RST}"
            return True, msg, panic_response
        elif sensitivity > 0.4:
            self.scar_tissue[trigger] = min(1.0, sensitivity + 0.05)
            panic_response = {"narrative_drag": 2.0}
            msg = f"{Prisma.OCHRE}SCAR TISSUE: Gordon flinches at '{trigger}'. Hands are shaking.{Prisma.RST}"
            return True, msg, panic_response
        else:
            self.scar_tissue[trigger] = max(0.0, sensitivity - 0.05)
            msg = f"{Prisma.GRY}CALLOUS: '{trigger}' hit an old scar. Gordon ignores it.{Prisma.RST}"
            return False, msg, None

    def learn_scar(self, toxic_words: List[str], damage: float):
        if damage < 10.0 or not toxic_words: return None
        culprit = max(toxic_words, key=len).upper()
        if culprit not in self.scar_tissue:
            self.scar_tissue[culprit] = 0.5
            self.pain_memory.add(culprit)
            return f"{Prisma.VIOLET}TRAUMA IMPRINTED: Gordon will remember '{culprit}'.{Prisma.RST}"
        else:
            self.scar_tissue[culprit] = min(1.0, self.scar_tissue[culprit] + 0.3)
            return f"{Prisma.VIOLET}TRAUMA DEEPENED: The scar on '{culprit}' is worse.{Prisma.RST}"

    def deploy_pizza(self, physics_ref, item_name="STABILITY_PIZZA") -> Tuple[bool, str]:
        data = self.get_item_data(item_name)
        req_type = data.get("requires", "thermal")
        clean_words = physics_ref.get("clean_words", [])
        from bone_village  import TheLexicon
        source = [w for w in clean_words if w in TheLexicon.get(req_type)]
        if not source:
            return False, f"{Prisma.CYN}🧊 STASIS LOCK: {item_name} is frozen. Apply {req_type.upper()} words to thaw.{Prisma.RST}"
        if data.get("consume_on_use") and item_name in self.inventory:
            self.inventory.remove(item_name)
        physics_ref["narrative_drag"] = 0.1
        physics_ref["psi"] = 0.90
        physics_ref["counts"]["toxin"] = physics_ref["counts"].get("toxin", 0) + 3
        if "SPIDER_LOCUS" not in self.inventory:
            self.inventory.append("SPIDER_LOCUS")
        heat_word = source[0].upper()
        return True, f"{data.get('usage_msg')} (Thawed with '{heat_word}')."

    def emergency_reflex(self, physics_ref) -> Tuple[bool, Optional[str]]:
        for item in self.inventory:
            data = self.get_item_data(item)
            trigger_key = data.get("reflex_trigger")
            if trigger_key and trigger_key in self.REFLEX_MAP:
                if self.REFLEX_MAP[trigger_key](physics_ref):
                    func = data.get("function")
                    if func == "DRIFT_KILLER":
                        self.inventory.remove(item)
                        physics_ref["narrative_drag"] = 0.0
                        return True, f"{Prisma.OCHRE}REFLEX: {data.get('usage_msg')}{Prisma.RST}"
                    elif func == "REALITY_ANCHOR":
                        success, msg = self.deploy_pizza(physics_ref, item)
                        status = Prisma.OCHRE if success else Prisma.RED
                        return True, f"{status}REFLEX: {msg}{Prisma.RST}"
                    elif func == "ENTROPY_BUFFER":
                        self.inventory.remove(item)
                        physics_ref["turbulence"] = 0.8
                        physics_ref["narrative_drag"] = 0.0
                        return True, f"{Prisma.VIOLET}REFLEX: {data.get('usage_msg')}{Prisma.RST}"
        return False, None