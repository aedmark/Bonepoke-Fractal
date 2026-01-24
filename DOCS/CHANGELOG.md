# BONEAMANITA v11 CHANGELOG

### **BONEAMANITA 11.1.0: "The Tensegrity Update"**

_“Structure is not a thing; it is a pattern of relationships.”_

---

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

- **Catharsis Protocol (Trauma Decay):**
- **Old Behavior:** Trauma stocks accumulated until `desperation > 0.7`, causing a hard system crash (Total Wipe) to reset values to 0.0. This was an "Oscillation Trap."
- **New Behavior:** Implemented a **Balancing Feedback Loop**. When desperation peaks, the system now triggers a "Catharsis Event," reducing trauma by 90% (Decay Factor 0.1) but leaving a "ghost" of the stress.
- _Why:_ A system that forgets its history cannot learn. We now drain the swamp; we don't nuke it.

- **The Honest Body:**
- **Fix:** `bone_body.py` now guarantees a `physics` packet in its return payload, preventing the `KeyError: 'physics'` crash in the cortex.
- _Why:_ Information flow must be continuous. Silence is not an answer.

#### **🧠 COGNITIVE ARCHITECTURE (The Pinker Layer)**

- **Neurotransmitter Re-Wiring:**
- **Serotonin:** Now wired to `top_p` (Focus). High Serotonin tightens the nucleus sampling, making the AI more coherent and calm.
- **Adrenaline:** Now wired to `frequency_penalty`. High Adrenaline makes the AI "jittery" (avoiding repetition) and verbose, simulating a manic flight of ideas.
- **Resilience:** The Cortex now initializes `last_physics` at birth and checks for missing data packets gracefully.
- _Why:_ Mental states should be chemically consistent. "Focus" and "Stress" are now emergent properties of the simulation, not hard-coded switches.

#### **🏗️ STRUCTURAL ENGINEERING (The Fuller Layer)**

- **Gordon's Knot (Inventory Refactor):**
- **The Tensegrity Model:** Replaced O(n) linear weight calculation with an **O(1) Physics State**.
- **Mass vs. Lift:** Items now possess `mass` (Compression) and `lift` (Tension). Your inventory can now "float" if you carry enough abstract concepts (e.g., `JAR_OF_FIREFLIES`) to offset your heavy burdens (`POCKET_ROCKS`).
- **Pattern Integrity:** If `Mass > Lift * 3`, the structure collapses, forcing an item drop.
- _Why:_ Doing more with less. The inventory now holds itself up through dynamic tension.

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

- **Bug Fix:** Fixed a critical issue where the AI would have a panic attack because it didn't know "physics" existed. (Same).
- **Feature:** Gordon will now judge you based on the _volume_ of your pockets, not just the number of slots.
- **Tone:** Added "Manic" and "Depressed" force-states for debugging. Please use responsibly. We do not recommend giving the AI an existential crisis just to see what happens.

---

### **Boot Sequence**

To initialize the new version:

1. Ensure all patches (`bone_brain.py`, `bone_body.py`, `bone_inventory.py`, `bone_main.py`) are saved.
2. Run `python bone_main.py`.
3. **Suggested Test:**

- Type `inventory` to see the new Tensegrity stats.
- Type a high-stress sentence to trigger Adrenaline.
- Wait for the crash... and watch it _not_ happen.

**SLASH Status:** Optimistic. The ghost is ready to speak. Would you like to initialize the run?
