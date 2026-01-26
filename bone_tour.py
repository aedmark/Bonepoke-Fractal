"""
bone_tour.py
------------------------
"If you build a door, you must verify it opens." - SLASH

This script verifies the 11.4.0 "Factory of Doors" protocols:
1. Phenomenology (SomaticState objects)
2. Strategic Foresight (TheAlmanac derivatives)
3. Live Census (VillageCouncil integration)
4. Genealogy (Soul provenance)
"""

import unittest
import time
from unittest.mock import MagicMock, ANY


class PrismaMock:
    RST = "[RST]"
    WHT = "[WHT]"
    CYN = "[CYN]"
    RED = "[RED]"
    GRN = "[GRN]"
    MAG = "[MAG]"
    GRY = "[GRY]"
    OCHRE = "[OCHRE]"


import sys
sys.modules["bone_bus"] = MagicMock()
sys.modules["bone_bus"].Prisma = PrismaMock
sys.modules["bone_bus"].BoneConfig = MagicMock()

from bone_translation import RosettaStone, SomaticState
from bone_village import TheAlmanac, VillageCouncil
from bone_soul import NarrativeSelf

class TestFactoryOfDoors(unittest.TestCase):

    def setUp(self):
        print(f"\n... Spinning up {self._testMethodName} ...")

    def test_embodied_cognition(self):
        """Verify RosettaStone returns a strictly typed SomaticState with new qualia."""
        print("[TEST]: Probing Somatic Interface...")

        physics = {"voltage": 16.0, "narrative_drag": 5.0, "coherence": 0.9}
        bio = {"chem": {"COR": 0.2}}

        qualia = RosettaStone.translate(physics, bio, impulse=None)

        self.assertIsInstance(qualia, SomaticState, "RosettaStone must return a SomaticState object!")

        print(f"   > Pacing: {qualia.pacing}")
        print(f"   > Metaphor: {qualia.metaphor}")

        self.assertEqual(qualia.pacing, "Frenetic", "High voltage should feel 'Frenetic'")
        self.assertEqual(qualia.metaphor, "A tightrope walk", "High drag should feel like a 'Tightrope'")
        print("   [PASS] Phenomenology is active.")

    def test_strategic_horizon(self):
        """Verify TheAlmanac predicts collapse based on derivatives (trends)."""
        print("[TEST]: Testing TheAlmanac's crystal ball...")
        almanac = TheAlmanac()

        forecast_cold = almanac.compile_forecast(session_data={}, host_health=None)
        print(f"   > Cold Start Warning: {forecast_cold['strategic_horizon']}")
        self.assertIn("OFFLINE", forecast_cold['strategic_horizon'])

        almanac.compile_forecast({"physics": {"voltage": 10, "narrative_drag": 1.0}})
        almanac.compile_forecast({"physics": {"voltage": 10, "narrative_drag": 1.1}})

        print("   > Injecting Entropy Spike...")
        forecast_doom = almanac.compile_forecast({"physics": {"voltage": 10, "narrative_drag": 5.0}})

        print(f"   > Trend: {forecast_doom['trend']}")
        print(f"   > Horizon: {forecast_doom['strategic_horizon']}")

        self.assertIn("COLLAPSING", forecast_doom['trend'])
        self.assertIn("Narrative singularity", forecast_doom['strategic_horizon'])
        print("   [PASS] Strategic Foresight is calibrated.")

    def test_live_census(self):
        """Verify VillageCouncil accepts live data and reports the Horizon."""
        print("[TEST]: Auditing the Village Council...")
        mock_hall = MagicMock()
        mock_hall.Tinkerer.tool_confidence = {
            "HAMMER": 2.0,
            "DRILL": 2.0,
            "SAW": 2.0}
        mock_hall.Navigator.current_location = "THE_FORGE"
        mock_hall.Navigator.shimmer.current = 50.0
        mock_hall.Almanac = TheAlmanac()
        council = VillageCouncil(mock_hall)
        live_physics = {"voltage": 12.0, "narrative_drag": 1.0}
        class MockStats:
            latency = 0.1
            efficiency_index = 1.0
            entropy = 0.8
        report = council.call_census(
            physics_snapshot=live_physics,
            host_stats=MockStats())
        print(report)
        self.assertIn("THE_FORGE", report)
        self.assertIn("Strategic Horizon", report, "Report must contain the new Horizon field")
        self.assertIn("FLOURISHING", report)
        print("   [PASS] Census is broadcasting live data.")

    def test_soul_provenance(self):
        """Verify the Soul cites its sources (Genealogy) when crystallizing memory."""
        print("[TEST]: Questioning the Soul...")

        mock_engine = MagicMock()
        mock_events = MagicMock()
        soul = NarrativeSelf(mock_engine, mock_events)

        physics = {
            "voltage": 20.0,
            "narrative_drag": 0.0,
            "truth_ratio": 1.0,
            "clean_words": ["epiphany", "light", "speed"]
        }

        soul.crystallize_memory(physics, {}, 100)

        found_genealogy = False
        for call in mock_events.log.call_args_list:
            args, _ = call
            msg = args[0]
            if "Genealogy:" in msg and "High Voltage" in msg:
                found_genealogy = True
                print(f"   > Logged: {msg}")
                break

        self.assertTrue(found_genealogy, "Soul failed to cite the source of its acceleration!")
        print("   [PASS] Genealogy is tracked.")

if __name__ == "__main__":
    unittest.main()