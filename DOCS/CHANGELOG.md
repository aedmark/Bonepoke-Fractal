# BONEAMANITA v11 CHANGELOG


### **BONEAMANITA 11.2.2: "The Silent Belt & The PID Governor"**

*“We taught the ghost to stop reading the grocery list, and we taught the machine to stop kicking the driver when the engine starts.”*

---

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

* **Refactor: The Homeostatic Regulator (`bone_sanctuary.py`)**
* **Old Behavior:** The Sanctuary Governor was a "blind" regulator that started every session with zero error, causing a violent correction "kick" upon initialization.
* **New Behavior:** The PID Controller now "seeds" itself with the current system error on startup.
* **Why:** You don't slam the brakes the moment you get in the car; you ease into the flow.

* **Fix: The Phantom Feedback Loop (`bone_brain.py`)**
* **Critical Fix:** The Cortex was trying to apply a "Divergence Penalty" (increasing voltage when the LLM hallucinated) to a physics packet that didn't exist in the snapshot view.
* **Result:** The feedback loop is now closed. If the ghost wanders, the machine *actually* gets hotter.

#### **🏗️ TENSEGRITY (The Fuller Layer)**

* **Architecture: Single Source of Truth (`bone_cycle.py`)**
* **Deleted:** The duplicate `PIDController` class in the cycle engine.
* **Unified:** `bone_sanctuary.py` is now the sole authority on control theory. One part, used twice.
* **Effect:** Code ephemeralization achieved. Less code, more stability.

* **Data Flow: explicit State Injection (`bone_cycle.py`)**
* **Fix:** The `GeodesicOrchestrator` now explicitly injects the `physics` state into the render snapshot. No more `KeyError: 'physics'` when the brain tries to read the body.

#### **🧠 COGNITIVE ERGONOMICS (The Pinker Layer)**

* **UX: The Inventory Clerk (`bone_brain.py`)**
* **Old Prompt:** "Holding: Pocket_Rocks, Silent_Knife." (Result: LLM describes holding rocks).
* **New Prompt:** "Belt (Accessible): Pocket_Rocks, Silent_Knife." (Result: LLM ignores them until needed).
* **Why:** "Holding" is a verb that implies action. "Belt" is a noun that implies availability. Language shapes behavior.

* **DevOps: The Unmasked Wizard (`bone_genesis.py`, `bone_inspector.py`)**
* **Fix:** The setup wizard was swallowing critical errors with a broad `try...except`. We narrowed the scope so crashes actually crash (as they should).
* **Fix:** Updated the Inspector's mock objects to match the new 3-tuple signature of the neural uplink.

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

* **Quality of Life:** The "Sanctuary" phase no longer secretly modifies your variables in the background. It calculates a "Gentle Nudge" and hands you the bill, which the system then chooses to pay. Transparency is polite.
* 

### **BONEAMANITA 11.2.1: "The Pre-Warmed Panic Room"**

*“We fixed the timeline where the AI forgot who it was before it started, and we built a bunker for when the paint factory burns down.”*

---

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

* **Optimization: The Uplink Reservoir (`bone_genesis.py`)**
* **Old Behavior:** The system built a bridge to the LLM to test it, burned the bridge, and then built it again five seconds later. This was a "leaky bucket" in our time stock.
* **New Behavior:** We now "pre-warm" the client. If the validation passes, we hold the living connection in memory and graft it directly onto the cortex.
* **Why:** Never drain a stock twice to fill the same flow.

#### **🏗️ TENSEGRITY (The Fuller Layer)**

* **Fix: Schrödinger's Navigator (`bone_main.py`)**
* **Fix:** Removed a redundant structural member where `self.navigator` was assigned twice in the same initialization sequence.
* **Result:** Pattern integrity restored. We have collapsed the wave function; the cat is now strictly alive and navigating.
* **Refactor: Timeline Stabilization (`bone_genesis.py`)**
* **Fix:** Patched a critical `UnboundLocalError` where the `pre_warmed_client` variable only existed in the "Success" timeline. It now exists in all timelines (initialized to `None`), ensuring the multiverse remains consistent.

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

* **Feature: The Panic Room (`bone_main.py`)**
* **Old Behavior:** If the system crashed *while* trying to log a crash (a meta-crash), it would silently die because the pretty-printer (`Prisma`) failed.
* **New Behavior:** Implemented a raw `try/except` block that bypasses the aesthetic layer entirely. If the ship is going down, it dumps a raw `panic_dump.json` file.
* **Why:** Because sometimes you don't have time to paint the "EXIT" sign before you run through the door.


### **BONEAMANITA 11.2.0: "The Sympathetic Resonance Update"**

_“A system that cannot dance with its environment is destined to break.”_

---

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

- **Feature: The Synaptic Dance (`bone_soul.py`)**
    - **Old Behavior:** Personality traits (`HOPE`, `CYNICISM`) passively decayed to neutral over time.
    - **New Behavior:** The Soul now *reacts* to the physics of the conversation in real-time. High Voltage drives **Curiosity** (Manic). High Drag drives **Cynicism** (Grinding).
    - _Why:_ Static personalities are for chatbots. The Soul is now a dancing partner.

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

- **Feature: The Donner Party Protocol (`bone_spores.py`)**
    - **Old Behavior:** Memories were deleted ("cannibalized") purely based on a linear capacity counter.
    - **New Behavior:** Implemented a **Desperation Check**. The system now only cannibalizes old memories if it is *starving* (`Health < 40%`). If healthy, it simply rejects new input ("Cortical Saturation").
    - _Why:_ We shouldn't eat our friends just because the room is crowded. We only eat them if we are dying.

- **Fix: Latency Awareness (`bone_cycle.py`)**
    - **Fix:** Removed the hardcoded `0.5s` tick delta in the PID Controllers.
    - _Result:_ The Physics engine now "feels" the actual lag of the LLM. If the brain is slow, the physics slows down to match it.

#### **🧠 COGNITIVE ARCHITECTURE (The Pinker Layer)**

- **Feature: Synaptic Re-uptake (`bone_brain.py`)**
    - **Mechanism:** Implemented **Exponential Backoff** for LLM API calls.
    - _Why:_ A dropped packet should be a stutter, not a lobotomy. The brain now tries to "find the word" (retry) before triggering a panic attack.

#### **🏛️ COMPREHENSIVE DESIGN (The Fuller Layer)**

- **Documentation: The Manifest**
    - Expanded the System Map to cover the full 25-file tensegrity structure, from the **Mycelial Layer** to the **Observability Layer**.

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
