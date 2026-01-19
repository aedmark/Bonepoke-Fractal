# bone_bus.py - All aboard the Magic Bone Bus!

import json, os, time, random
from collections import deque
from dataclasses import dataclass, field, fields
from typing import List, Dict, Any, Optional, Counter, Callable, Tuple


class Prisma:
    RST = "\033[0m"
    RED = "\033[31m"
    GRN = "\033[32m"
    YEL = "\033[33m"
    BLU = "\033[34m"
    MAG = "\033[35m"
    CYN = "\033[36m"
    WHT = "\033[97m"
    GRY = "\033[90m"
    INDIGO = "\033[34;1m"
    OCHRE = "\033[33;2m"
    VIOLET = "\033[35;2m"
    SLATE = "\033[30;1m"
    PUR = "\033[35m"

    @classmethod
    def paint(cls, text, color_key="0"):
        color_map = {
            "R": cls.RED, "G": cls.GRN, "Y": cls.YEL, "B": cls.BLU,
            "M": cls.MAG, "C": cls.CYN, "W": cls.WHT, "0": cls.GRY,
            "I": cls.INDIGO, "O": cls.OCHRE, "V": cls.VIOLET,
            "P": cls.PUR
        }
        code = color_map.get(str(color_key).upper(), cls.WHT)
        safe_text = str(text).replace(cls.RST, cls.RST + code)
        return f"{code}{safe_text}{cls.RST}"

    @classmethod
    def tie_dye(cls, text):
        colors = [cls.RED, cls.GRN, cls.YEL, cls.CYN, cls.MAG, cls.VIOLET, cls.OCHRE, cls.PUR]
        words = text.split()
        painted = []
        for w in words:
            c = random.choice(colors)
            painted.append(f"{c}{w}{cls.RST}")
        return " ".join(painted)

class EventBus:
    def __init__(self, max_memory=1024):
        self.buffer = deque(maxlen=max_memory)
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, data=None):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event Bus Error: {e}")

    def log(self, text: str, category: str = "SYSTEM"):
        entry = {
            "text": text,
            "category": category,
            "timestamp": time.time()
        }
        self.buffer.append(entry)

    def flush(self) -> List[Dict]:
        current_logs = list(self.buffer)
        self.buffer.clear()
        return current_logs

    def get_recent_logs(self, count=10):
        return list(self.buffer)[-count:]


class BoneConfig:
    GRAVITY_WELL_THRESHOLD = 15.0
    SHAPLEY_MASS_THRESHOLD = 5.0
    TRAUMA_VECTOR = {"THERMAL": 0.0, "CRYO": 0.0, "SEPTIC": 0.0, "BARIC": 0.0}
    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    MAX_ATP = 200.0
    STAMINA_REGEN = 1.0
    MAX_DRAG_LIMIT = 5.0
    GEODESIC_STRENGTH = 10.0
    BASE_IGNITION_THRESHOLD = 0.5
    MAX_REPETITION_LIMIT = 0.8
    BOREDOM_THRESHOLD = 10.0
    ANVIL_TRIGGER_VOLTAGE = 10.0
    MIN_DENSITY_THRESHOLD = 0.3
    LAGRANGE_TOLERANCE = 2.0
    FLASHPOINT_THRESHOLD = 10.0
    SIGNAL_DRAG_MULTIPLIER = 1.0
    KINETIC_GAIN = 1.0
    CRITICAL_ROS_LIMIT = 100.0
    MAX_MEMORY_CAPACITY = 100
    ZONE_THRESHOLDS = {"LABORATORY": 1.5, "COURTYARD": 0.8}
    TOXIN_WEIGHT = 1.0
    ANTIGENS = ["basically", "actually", "literally", "utilize"]
    MAX_OUTPUT_TOKENS = 4096
    VERBOSE_LOGGING = True
    PROVIDER = "openai"
    BASE_URL = None
    API_KEY = None
    MODEL = "gpt-4"
    OLLAMA_MODEL_ID = "llama3"

    class WHIMSY:
        ABSURDITY_CONSTANT = 42
        MAX_SARCASM_LEVEL = 11
        LUDICROUS_SPEED = True
        DEPARTMENT_NAME = "The Ministry of Silly Hats & Semantic Vectors"

    class METABOLISM:
        BASE_RATE = 2.0
        DRAG_TAX_LOW = 0.15
        DRAG_TAX_HIGH = 0.4
        DRAG_GRACE_BUFFER = 1.0
        ROS_GENERATION_FACTOR = 0.08
        PHOTOSYNTHESIS_GAIN = 3.0
        TURBULENCE_TAX = 4.0

    class PHYSICS:
        VOLTAGE_FLOOR = 2.0
        VOLTAGE_LOW = 5.0
        VOLTAGE_MED = 8.0
        VOLTAGE_HIGH = 12.0
        VOLTAGE_CRITICAL = 15.0
        VOLTAGE_MAX = 20.0
        DRAG_FLOOR = 1.0
        DRAG_IDEAL_MAX = 3.0
        DRAG_HEAVY = 5.0
        DRAG_CRITICAL = 8.0
        DRAG_HALT = 10.0
        WEIGHT_HEAVY = 2.0
        WEIGHT_KINETIC = 1.5
        WEIGHT_EXPLOSIVE = 3.0
        WEIGHT_CONSTRUCTIVE = 1.5

    class INVENTORY:
        CONDUCTIVE_THRESHOLD = 12.0
        HEAVY_LOAD_THRESHOLD = 8.0
        TURBULENCE_FUMBLE_CHANCE = 0.15
        TURBULENCE_THRESHOLD = 0.6
        MAX_SLOTS = 8
        RUMMAGE_COST = 15.0

    class COUNCIL:
        STRANGE_LOOP_VOLTAGE = 8.0
        OSCILLATION_DELTA = 5.0
        MANIC_VOLTAGE_TRIGGER = 18.0
        MANIC_DRAG_FLOOR = 1.0
        MANIC_TURN_LIMIT = 2
        FOOTNOTE_CHANCE = 0.15

    class BIO:
        ATP_STARVATION = 10.0
        ROS_CRITICAL = 100.0
        STAMINA_EXHAUSTED = 20.0
        REWARD_SMALL = 0.05
        REWARD_MEDIUM = 0.10
        REWARD_LARGE = 0.15
        DECAY_RATE = 0.01

    class CHANCE:
        RARE = 0.05
        UNCOMMON = 0.10
        COMMON = 0.20
        FREQUENT = 0.30

    @staticmethod
    def check_pareidolia(words):
        triggers = {"face", "ghost", "jesus", "cloud", "voice", "eyes"}
        hits = [w for w in words if w in triggers]
        if hits:
            return True, f"{Prisma.VIOLET}PAREIDOLIA: You see a {hits[0].upper()} in the noise. It blinks.{Prisma.RST}"
        return False, None

    @classmethod
    def load_from_file(cls, filepath="bone_config.json"):
        if not os.path.exists(filepath):
            return False, "Config file not found. Using defaults."
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            valid_data, log = cls._validate_ranges(data)
            for key, value in valid_data.items():
                if hasattr(cls, key):
                    setattr(cls, key, value)
            return True, f"Configuration loaded. {log}"
        except Exception as e:
            return False, f"Config load failed: {e}"

    @classmethod
    def _validate_ranges(cls, data: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        sanitized = {}
        logs = []
        constraints = {
            "MAX_HEALTH": (1.0, 1000.0, float),
            "MAX_STAMINA": (1.0, 1000.0, float),
            "VOLTAGE_MAX": (10.0, 100.0, float),
            "GRAVITY_WELL_THRESHOLD": (1.0, 100.0, float),
            "STAMINA_REGEN": (0.1, 10.0, float),
            "MAX_MEMORY_CAPACITY": (10, 1000, int),
            "VERBOSE_LOGGING": (0, 1, bool)
        }
        for key, value in data.items():
            if key in constraints:
                min_val, max_val, expected_type = constraints[key]
                if expected_type == float and isinstance(value, int):
                    value = float(value)
                if not isinstance(value, expected_type):
                    logs.append(f"Skipped {key}: Invalid type {type(value)}.")
                    continue
                if expected_type in [int, float]:
                    if min_val <= value <= max_val:
                        sanitized[key] = value
                    else:
                        clamped = max(min_val, min(max_val, value))
                        sanitized[key] = clamped
                        logs.append(f"Clamped {key} ({value} -> {clamped}).")
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
        return sanitized, "; ".join(logs) if logs else "Values Nominal."

@dataclass
class ErrorLog:
    component: str
    error_msg: str
    timestamp: float = field(default_factory=time.time)
    severity: str = "WARNING"


class TheObserver:
    def __init__(self):
        self.start_time = time.time()
        self.cycle_times = deque(maxlen=20)
        self.llm_latencies = deque(maxlen=20)
        self.memory_snapshots = deque(maxlen=20)
        self.error_counts = Counter()
        self.user_turns = 0
        self.LATENCY_WARNING = 5.0
        self.CYCLE_WARNING = 8.0

    def clock_in(self):
        return time.time()

    def clock_out(self, start_time, metric_type="cycle"):
        duration = time.time() - start_time
        if metric_type == "cycle":
            self.cycle_times.append(duration)
        elif metric_type == "llm":
            self.llm_latencies.append(duration)
        return duration

    def log_error(self, module_name):
        self.error_counts[module_name] += 1

    def record_memory(self, node_count):
        self.memory_snapshots.append(node_count)

    def pass_judgment(self, avg_cycle, avg_llm):
        if avg_cycle == 0.0 and avg_llm == 0.0:
            return "ASLEEP (WAKE UP)"
        if avg_cycle < 0.1 and avg_llm < 0.5:
            return "SUSPICIOUSLY EFFICIENT (Did we skip the math?)"
        if avg_llm > self.LATENCY_WARNING:
            jokes = [
                "BRAIN FOG (The neural net is buffering)",
                "DEGRADED (Thinking... thinking...)",
                "PONDEROUS (Is the LLM on a coffee break?)"
            ]
            return random.choice(jokes)
        if avg_cycle > self.CYCLE_WARNING:
            return "SLUGGISH (The gears need oil)"
        return "NOMINAL (Boringly adequate)"

    def get_report(self):
        avg_cycle = sum(self.cycle_times) / max(1, len(self.cycle_times))
        avg_llm = sum(self.llm_latencies) / max(1, len(self.llm_latencies))
        uptime = time.time() - self.start_time
        status_msg = self.pass_judgment(avg_cycle, avg_llm)
        return {
            "uptime_sec": int(uptime),
            "turns": self.user_turns,
            "avg_cycle_sec": round(avg_cycle, 2),
            "avg_llm_sec": round(avg_llm, 2),
            "status": status_msg,
            "errors": dict(self.error_counts),
            "graph_size": self.memory_snapshots[-1] if self.memory_snapshots else 0
        }

@dataclass
class SystemHealth:
    physics_online: bool = True
    bio_online: bool = True
    mind_online: bool = True
    cortex_online: bool = True
    errors: List[ErrorLog] = field(default_factory=list)
    observer: Optional['TheObserver'] = None

    def link_observer(self, observer_ref):
        self.observer = observer_ref

    def report_failure(self, component: str, error: Exception, severity="ERROR"):
        msg = str(error)
        self.errors.append(ErrorLog(component, msg, severity=severity))
        if self.observer:
            self.observer.log_error(component)
        if component == "PHYSICS": self.physics_online = False
        elif component == "BIO": self.bio_online = False
        elif component == "MIND": self.mind_online = False
        elif component == "CORTEX": self.cortex_online = False
        return f"[{component} OFFLINE]: {msg}"

@dataclass
class PhysicsPacket:
    voltage: float = 0.0
    narrative_drag: float = 0.0
    valence: float = 0.0
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
    audit_trail: List[str] = field(default_factory=list)
    raw_text_display: str = ""
    entropy: float = 0.0

    def __getitem__(self, key): return getattr(self, key)

    def __setitem__(self, key, value): setattr(self, key, value)

    def __contains__(self, key): return hasattr(self, key)

    def get(self, key, default=None): return getattr(self, key, default)

    def update(self, data: Dict):
        for k, v in data.items():
            if hasattr(self, k): setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    def to_dict(self):
        return {f.name: getattr(self, f.name) for f in fields(self)}

@dataclass
class CycleContext:
    input_text: str
    clean_words: List[str] = field(default_factory=list)
    physics: Any = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    flux_log: List[Dict[str, Any]] = field(default_factory=list)
    is_alive: bool = True
    refusal_triggered: bool = False
    refusal_packet: Optional[Dict] = None
    is_bureaucratic: bool = False
    bio_result: Dict = field(default_factory=dict)
    world_state: Dict = field(default_factory=dict)
    mind_state: Dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    bureau_ui: str = ""
    user_profile: Dict = field(default_factory=lambda: {"name": "TRAVELER", "confidence": 0})

    @property
    def user_name(self):
        return self.user_profile.get("name", "TRAVELER")

    @user_name.setter
    def user_name(self, value):
        self.user_profile["name"] = value

    def log(self, message: str):
        self.logs.append(message)
    def record_flux(self, phase: str, metric: str, initial: float, final: float, reason: str = ""):
        delta = final - initial
        if abs(delta) > 0.001:
            self.flux_log.append({
                "phase": phase,
                "metric": metric,
                "initial": initial,
                "final": final,
                "delta": delta,
                "reason": reason,
                "timestamp": time.time()
            })

@dataclass
class MindSystem:
    mem: Any
    lex: Any
    dreamer: Any
    mirror: Any
    wise: Any
    tracer: Any
    integrator: Any

@dataclass
class PhysSystem:
    tension: Any
    forge: Any
    crucible: Any
    theremin: Any
    pulse: Any
    gate: Any
    dynamics: Any
    nav: Any