# BONEAMANITA v11 CHANGELOG





### **BONEAMANITA 11.2.4: "Soft Landing"**

_“Gentleness is not weakness. It is the precise application of force.”_

---

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

- **Feature: The Boot Camp Protocol (`TutorialDirector`)**
- **Problem:** New users were dropped into a "Void" with no instructions, leading to existential dread before the first turn.
- **Solution:** Implemented a 4-step interactive curriculum (Look, Wait, Inspect, Graduate) that guides the Traveler through the core loops.
- **Tone Shift:** Injected a "Softener" into `TheCortex` during tutorials. The AI temporarily suspends its "Cryptic Void God" persona to act as a helpful mentor.

- **Fix: The Air Lock (`bone_genesis.py`)**
- **Bug:** The input loop was swallowing empty "Enter" key presses, making it impossible to perform the "WAIT" action.
- **Fix:** The airlock is unsealed. The system now recognizes silence (Enter) as a valid input.

- **Improvement: The Neural Handshake**
- **Old:** The system booted into a blank cursor.
- **New:** The Cortex now proactively greets the user by name immediately after boot, bridging the gap between "System Online" and the first prompt.

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

- **Feature: Dynamic Paradigms (`BonePresets`)**
- **Old:** Physics constants were hardcoded, requiring a restart to change the "vibe."
- **New:** Introduced hot-swappable `BonePresets` (e.g., `ZEN_GARDEN`, `THUNDERDOME`).
- **Why:** High leverage. We can now shift the system's entire rule set from "Safe Mode" to "Chaos Mode" with a single function call.

- **Upgrade: The Nervous System (`DiagnosticHub`)**
- **New:** Upgraded `SystemHealth` to differentiate between `Errors` (System Breaks), `Warnings` (Resource Low), and `Hints` (Missed Opportunities).
- **Effect:** The system no longer fails silently; it complains constructively directly in the UI stream.

#### **🏗️ TENSEGRITY (The Fuller Layer)**

- **Refactor: The Immutable Snapshot (`CycleContext`)**
- **Critical Fix:** `CycleContext` now performs a true `deepcopy` during snapshots.
- **Why:** Previously, rolling back a phase (Time Travel) left "ghost data" in mutable dictionaries. Now, the past is truly immutable.

- **Resilience: The Neural Circuit Breaker (`LLMInterface`)**
- **Fix:** Implemented a robust retry loop for LLM failures.
- **Result:** A malformed JSON response is now treated as a hiccup (Retry), not a stroke (Crash).

#### **🧠 COGNITION (The Pinker Lens)**

- **Bug Fix: The Phantom Limb (`bone_genesis.py`)**
- **Bug:** The Genesis Protocol attempted to access configuration data via the Engine (`engine.config`) rather than its own internal state.
- **Fix:** Reconnected the neural pathways to the correct memory bank.

- **Bug Fix: The Impossible Setter (`MachineryPhase`)**
- **Bug:** Attempted to write to a read-only property (`efficiency_mod`).
- **Fix:** The logic now correctly modifies the underlying state (`membrane_potential`).

---

### **BONEAMANITA 11.2.3: "Spinning Plates"**

*“We stopped the mitochondria from printing money, and we taught the hormones to tell time.”*

---

#### **🚀 SYSTEM DYNAMICS (The Meadows Layer)**

* **Refactor: The Central Bank of ATP (`MitochondrialForge`)**
* **Old Behavior:** ATP was deducted in multiple places, creating a race condition where the system could spend energy it didn't have.
* **New Behavior:** All energy transactions now go through `adjust_atp()`.
* **Why:** You cannot manage a stock (Energy) if you don't control the flows. The vault is now secure.

* **Fix: The Causality Violation (`EndocrineSystem`)**
* **Critical Fix:** The system was attempting to apply Homeostasis *before* checking what time of day it was.
* **Result:** The metabolic order of operations is restored: Circadian Baseline -> Environmental Pressure -> Homeostatic Correction.

* **Tuning: The Dopamine Dampener**
* **Fix:** Removed a "double-dipping" logic error where successful resource harvesting rewarded Dopamine twice, creating a reinforcing feedback loop (addiction).

#### **🏗️ TENSEGRITY (The Fuller Layer)**

* **Optimization: Ephemeralization of Harvest (`SomaticLoop`)**
* **Old:** Iterate through the word list for every check ().
* **New:** `Counter` based logic ().
* **Effect:** Digestion is now cleaner and faster. We are doing more with less.

* **Structural Integrity: The Recursive Circuit Breaker (`ViralTracer`)**
* **Fix:** Replaced a dangerous recursive Depth-First Search with an iterative stack.
* **Why:** Deep thoughts shouldn't crash the stack. The system can now ruminate indefinitely without structural failure.

#### **🍩 HUMAN EXPERIENCE (The Schur Layer)**

* **Feature: The Ron Swanson Protocol (`ThePacemaker`)**
* **Fix:** Capped the time-delta calculation.
* **Old Behavior:** If the server slept for an hour, the system woke up screaming from "terminal boredom."
* **New Behavior:** The system understands that a nap is just a nap. Maximum boredom accrual is capped at 5 minutes.

* **Safety: The Panic Valve (`MetabolicGovernor`)**
* **Fix:** Added a voltage override to the Manual Mode. If Voltage > 25.0, the Governor ignores the manual setting and saves the ship.

#### **🧠 COGNITIVE ERGONOMICS (The Pinker Lens)**

* **Clarity: The End of Magic Numbers (`BioConstants`)**
* **Change:** Replaced cryptic floats (`8.0`, `0.7`) with semantic constants (`ROS_DAMAGE`, `DOPAMINE_SATIETY`).
* **Why:** Code should be read like a novel, not a sudoku puzzle.

* **Standardization: Noetic Consistency (`NoeticLoop`)**
* **Fix:** Enforced a standardized dictionary return schema for thoughts. No more guessing if the key is `"msg"` or `"context_msg"`.

---

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
