# bone_bus.py
import time
from typing import List, Dict

class EventBus:
    def __init__(self):
        self.buffer = []

    def log(self, text: str, category: str = "SYSTEM"):
        self.buffer.append({
            "text": text,
            "category": category,
            "timestamp": time.time()
        })

    def flush(self) -> List[Dict]:
        logs = list(self.buffer)
        self.buffer.clear()
        return logs

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

    @classmethod
    def paint(cls, text, color_key="0"):
        color_map = {
            "R": cls.RED, "G": cls.GRN, "Y": cls.YEL, "B": cls.BLU,
            "M": cls.MAG, "C": cls.CYN, "W": cls.WHT, "0": cls.GRY,
            "I": cls.INDIGO, "O": cls.OCHRE, "V": cls.VIOLET
        }
        code = color_map.get(color_key.upper(), cls.WHT)
        return f"{code}{text}{cls.RST}"

class BoneConfig:
    # --- CORE VITALS ---
    # Moved thresholds here for centralized "Physics of Existence"
    GRAVITY_WELL_THRESHOLD = 15.0
    SHAPLEY_MASS_THRESHOLD = 5.0
    TRAUMA_VECTOR = {"THERMAL": 0.0, "CRYO": 0.0, "SEPTIC": 0.0, "BARIC": 0.0}

    MAX_HEALTH = 100.0
    MAX_STAMINA = 100.0
    MAX_ATP = 200.0

    # --- METABOLIC CONSTITUTION (The Grounding) ---
    class METABOLISM:
        BASE_RATE = 2.0             # Cost to exist per turn (BMR)
        DRAG_TAX_LOW = 0.15         # Cost per unit of Drag (Low Friction) - Reduced from 0.2
        DRAG_TAX_HIGH = 0.4         # Cost per unit of Drag (High Friction) - Reduced from 0.5
        DRAG_GRACE_BUFFER = 1.0     # The first 1.0 units of drag are free. (Schur's Rule)
        ROS_GENERATION_FACTOR = 0.08 # % of burn that becomes Toxic Waste (ROS)
        PHOTOSYNTHESIS_GAIN = 3.0   # Energy gained from Light words
        TURBULENCE_TAX = 4.0        # ATP cost for chaotic text

    # --- PHYSICS CONSTANTS ---
    class PHYSICS:
        # Voltage Thresholds (The "Energy" of the text)
        VOLTAGE_FLOOR = 2.0        # System is effectively dead/stagnant
        VOLTAGE_LOW = 5.0          # Mud/Rust territory
        VOLTAGE_MED = 8.0          # Active processing
        VOLTAGE_HIGH = 12.0        # The Forge / High Energy
        VOLTAGE_CRITICAL = 15.0    # Dangerous / Manic
        VOLTAGE_MAX = 20.0         # System Cap

        # Narrative Drag (The "Friction" of the text)
        DRAG_FLOOR = 1.0           # Frictionless / Slippery
        DRAG_IDEAL_MAX = 3.0       # Good resistance
        DRAG_HEAVY = 5.0           # Sluggish
        DRAG_CRITICAL = 8.0        # Stuck in the Mud
        DRAG_HALT = 10.0           # Absolute stoppage

        # Vector Weights (VSL Matrix)
        WEIGHT_HEAVY = 2.0
        WEIGHT_KINETIC = 1.5
        WEIGHT_EXPLOSIVE = 3.0
        WEIGHT_CONSTRUCTIVE = 1.5

    # --- BIOLOGICAL CONSTANTS ---
    class BIO:
        # Thresholds
        ATP_STARVATION = 10.0
        ROS_CRITICAL = 100.0
        STAMINA_EXHAUSTED = 20.0

        # Endocrine Rewards
        REWARD_SMALL = 0.05
        REWARD_MEDIUM = 0.10
        REWARD_LARGE = 0.15
        DECAY_RATE = 0.01

    # --- PROBABILITIES ---
    class CHANCE:
        RARE = 0.05
        UNCOMMON = 0.10
        COMMON = 0.20
        FREQUENT = 0.30

    # --- LEGACY MAPPINGS (Backward Compatibility) ---
    STAMINA_REGEN = 1.0
    MAX_DRAG_LIMIT = PHYSICS.DRAG_HEAVY
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
    CRITICAL_ROS_LIMIT = BIO.ROS_CRITICAL
    MAX_MEMORY_CAPACITY = 100
    ZONE_THRESHOLDS = {"LABORATORY": 1.5, "COURTYARD": 0.8}
    TOXIN_WEIGHT = 1.0
    ANTIGENS = ["basically", "actually", "literally", "utilize"]
    VERBOSE_LOGGING = True

    @staticmethod
    def check_pareidolia(words):
        triggers = {"face", "ghost", "jesus", "cloud", "voice", "eyes"}
        hits = [w for w in words if w in triggers]
        if hits:
            return True, f"{Prisma.VIOLET}PAREIDOLIA: You see a {hits[0].upper()} in the noise. It blinks.{Prisma.RST}"
        return False, None