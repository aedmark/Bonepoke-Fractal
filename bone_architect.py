# bone_architect.py
# "We shape our buildings; thereafter they shape us." - Churchill

import time
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
from bone_bus import Prisma, BoneConfig, MindSystem, PhysSystem
from bone_data import LENSES
from bone_village import TownHall
from bone_inventory import GordonKnot
from bone_spores import (
    MycotoxinFactory, LichenSymbiont, HyphalInterface,
    ParasiticSymbiont, MycelialNetwork, LocalFileSporeLoader
)
from bone_body import (
    BioSystem, MitochondrialForge, EndocrineSystem,
    MetabolicGovernor, ViralTracer, ThePacemaker
)
from bone_brain import (
    DreamEngine, ShimmerState, LLMInterface, NeuroPlasticity
)
from bone_personality import LimboLayer
from bone_physics import (
    TheTensionMeter, TheTangibilityGate, TemporalDynamics
)
from bone_machine import TheCrucible, TheForge, TheTheremin

@dataclass
class SystemEmbryo:
    mind: MindSystem
    limbo: LimboLayer
    bio: BioSystem
    physics: PhysSystem
    shimmer: Any
    soul_legacy: Optional[Dict] = None

class PanicRoom:
    @staticmethod
    def get_safe_physics():
        from bone_bus import PhysicsPacket
        return PhysicsPacket(
            voltage=5.0,
            narrative_drag=5.0,
            clean_words=["system", "error"],
            vector={"STR": 0.5, "VEL": 0.5},
            counts={"heavy": 0, "kinetic": 0},
            raw_text="[SYSTEM FAILURE: PHYSICS BYPASSED]",
            psi=0.5,
            kappa=0.5
        )

    @staticmethod
    def get_safe_bio():
        return {
            "is_alive": True,
            "atp": 10.0,
            "chem": {"DOP": 0.0, "COR": 0.0, "OXY": 0.0, "SER": 0.0},
            "logs": [f"{Prisma.RED}BIO FAIL: Life support active.{Prisma.RST}"],
            "respiration": "NECROSIS",
            "enzyme": "NONE"
        }

    @staticmethod
    def get_safe_mind():
        return {
            "lens": "NARRATOR",
            "role": "The Backup System",
            "thought": "I cannot think clearly, therefore I still am, but barely.",
        }

class BoneArchitect:
    @staticmethod
    def incubate(events, lex) -> SystemEmbryo:
        _mem = MycelialNetwork(events)
        limbo = LimboLayer()
        _mem.cleanup_old_sessions(limbo)
        mind = MindSystem(
            mem=_mem,
            lex=lex,
            dreamer=DreamEngine(events),
            mirror=TownHall.Mirror(events),
            wise=TownHall.Apeirogon(events),
            tracer=ViralTracer(_mem),
            integrator=TownHall.Sorites(_mem)
        )
        immune_system = MycotoxinFactory()
        bio = BioSystem(
            mito=MitochondrialForge("PENDING_ACTIVATION", events),
            endo=EndocrineSystem(),
            immune=immune_system,
            lichen=LichenSymbiont(),
            gut=HyphalInterface(),
            plasticity=NeuroPlasticity(),
            governor=MetabolicGovernor(),
            shimmer=ShimmerState(),
            parasite=ParasiticSymbiont(mind.mem, lex)
        )
        physics = PhysSystem(
            tension=TheTensionMeter(events),
            forge=TheForge(),
            crucible=TheCrucible(),
            theremin=TheTheremin(),
            pulse=ThePacemaker(),
            gate=TheTangibilityGate(),
            dynamics=TemporalDynamics(),
            nav=TownHall.Navigator(bio.shimmer)
        )
        return SystemEmbryo(mind, limbo, bio, physics, bio.shimmer)

    @staticmethod
    def awaken(embryo: SystemEmbryo) -> SystemEmbryo:
        # 1. Load Ancestral Spore
        load_result = embryo.mind.mem.autoload_last_spore()
        inherited_traits = {}
        inherited_antibodies = set()
        soul_legacy = {}
        if load_result:
            if len(load_result) == 3:
                inherited_traits, inherited_antibodies, soul_legacy = load_result
            else:
                inherited_traits = load_result[0]
                inherited_antibodies = load_result[1]
        embryo.bio.mito.state.mother_hash = embryo.mind.mem.session_id
        embryo.bio.mito.apply_inheritance(inherited_traits)
        embryo.bio.immune.active_antibodies = inherited_antibodies
        embryo.soul_legacy = soul_legacy
        return embryo