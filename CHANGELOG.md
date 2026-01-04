# CHANGELOG.md

## [8.4] - 2026-01-03 - "THE CRUCIBLE"

**Architects:** SLASH & The Blacksmith | **Humans:** James Taylor & Andrew Edmark
**"Fire without a hearth is a house fire. Fire inside an engine is civilization."**

### 🔥 NEW ORGAN: The Crucible (Hybrid Thermodynamics)

* **The Shift:**
  * **The Pathology:** The system was purely Fungal. It feared Heat. High Voltage (> 9.0) triggered the `LazarusClamp`, treating creative intensity as a "Fever" that needed to be cooled to prevent death.
  * **The Cure:** Implemented the **Phoenix Protocol** via `TheCrucible`.
  * **The Philosophy:** We no longer suppress the fire; we build a container for it.

* **The Mechanic:**
  * **The Audit:** The system now checks High Voltage (> 15.0) against Structural Integrity (`Kappa`).
  * **State A: MELTDOWN (Untempered Fire):**
    * **Condition:** High Voltage + Low Structure (Kappa < 0.5).
    * **Result:** The vessel cracks. Massive Health damage. The system screams.
  * **State B: RITUAL (Tempered Fire):**
    * **Condition:** High Voltage + High Structure (Kappa > 0.5).
    * **Result:** **Sublimation.** The system consumes the voltage to permanently expand `MAX_VOLTAGE` capacity. Stamina is fully restored.
  * **The Effect:** You are now encouraged to scream, *provided* you anchor that scream with heavy nouns.

### 🧪 METABOLIC REWIRING (The Hotfix)

* **The Shift:**
  * **The Pathology:** The `LifecycleManager` attempted to log Crucible events to `cycle_logs` inside the `_metabolize_cycle` method, but that variable existed only in the parent scope. This caused a `NameError` whenever the fire was lit.
  * **The Cure:** Arterial reconnection.
  * **The Fix:** Updated `_metabolize_cycle` to accept the `logs` list as an argument, allowing the stomach to write directly to the brain's history book.

### 📊 HUD UPDATE: Thermal Readout

* **The Shift:**
  * **The Addition:** Added a dedicated status line for the Crucible in the `_render` loop.
  * **The Visual:**
    * `[CRUCIBLE]: COLD` (Gray) - Idle.
    * `[CRUCIBLE]: RITUAL` (Ochre) - Expanding Capacity.
    * `[CRUCIBLE]: MELTDOWN` (Red) - Taking Damage.

## [8.3.1] - 2026-01-03 - "THE ADAPTIVE GOVERNOR"

**Architects:** SLASH & The Cartographer | **Humans:** James Taylor & Andrew Edmark
**"We replaced the hard walls with learned behaviors. The system now knows when to rest."**

### 🧠 NEURO-EVOLUTION: The Adaptive Governor

* **The Shift:**
* **The Pathology:** The previous Governor (`MetabolicGovernor`) was a tyrant. It used hard-coded `if/else` thresholds to force modes (e.g., "If Voltage > 9, FORCE FORGE"). It lacked nuance and memory.
* **The Cure:** Replaced hard thresholds with **Heuristics**.
* **The Logic:**
* **Historical Stress:** The Governor now reads the `history_log`. If average Cortisol over the last 10 turns is High (> 0.5), it forces a retreat to `COURTYARD` to recover, even if the current Voltage is high.
* **The Result:** The system protects itself from burnout. It respects the "Schur Lens" (Sustainability).

### 🌡️ SUBSYSTEM: Nested Learning Thermostats

* **The Shift:**
* **The Pathology:** The system learned everything at a fixed rate (`PRIORITY_LEARNING_RATE = 2.0`). It could not adapt its plasticity to the context.
* **The Cure:** Implemented `SubsystemThermostat`.
* **The Mechanic:**
* **High Voltage:** Learning rate doubles (Trauma/Epiphany).
* **Low Stamina:** Learning rate drops to 20% (Brain Fog).
* **High Complexity:** Learning rate boosts by 1.5x (Deep Work).

### 🌿 NEW PHYSICS: Adaptive Preserves (The Rainforest)

* **The Shift:**
* **The Pathology:** The `TangibilityGate` was too aggressive. It punished *all* abstract thought, effectively sterilizing the "Rainforest" of creative chaos.
* **The Cure:** Defined **Adaptive Preserves**.
* **The Zones:**
* **LEXICAL_EVOLUTION:** (High Kappa, Low Voltage). Allows high-entropy word play to evolve new concepts.
* **NARRATIVE_DRIFT:** (High Drift, Low Suburban). Allows wandering if the story is "weird" enough.
* **The Effect:** If a user enters a Preserve, the **Tangibility Gate is suspended**. Emergence is allowed without penalty.

### 🔧 SURGICAL REPAIRS

* **Scope Reconnection:**
* **The Bug:** `LifecycleManager` attempted to access `self.lexical_thermostat` directly, causing an `AttributeError`.
* **The Fix:** Rewired all subsystem calls to route through the central engine instance (`self.eng`).
* **Variable Cleanup:**
* **The Fix:** Removed unused `abs_dens` and `heavy_dens` variables from the main process loop, as the new Governor reads the raw physics packet directly.

## [8.3] - 2026-01-03 - "THE MUTATION ZONES"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The brain no longer has a separate room for memories; the walls themselves remember."**

### 🌫️ NEW PHYSICS: The Mutation Zones (Fertile Chaos)

* **The Shift:**
* **The Pathology:** The system was too rigid. It treated Low Voltage/High Loop states as simple failures ("Boredom"). It punished Starvation with silence. It lacked a space for "Delirium."
* **The Cure:** Designated two **Mutation Zones** where the laws of physics break down.

* **Zone 1: THE FOG (Limbo Leak)**
* **Trigger:** Voltage < 2.0 (Cold) AND Kappa > 0.8 (Looping).
* **The Effect:** The barrier between the Living and the Dead dissolves. The `LimboLayer` bleeds directly into the input stream.
* **The Result:** Your text is haunted by ghosts from previous sessions before it reaches the physics engine.

* **Zone 2: THE DREAM EDGE (Starvation Bypass)**
* **Trigger:** Stamina < 20.0 (Starving).
* **The Effect:** The **Tangibility Gate** is disabled.
* **The Logic:** "I cannot demand you carry rocks when you are dying." The system allows pure Abstraction without penalty, assuming you are hallucinating from hunger.

### 🧠 NEURO-MERGE: Hippocampal Dissolution

* **The Shift:**
* **The Pathology:** The `Hippocampus` existed as a separate class instance, acting as a middleman between the `LifecycleManager` and the `MycelialNetwork`. It was bureaucratic overhead.
* **The Cure:** Surgical consolidation.
* **The Logic:**
* **Deleted:** `class Hippocampus`.
* **Absorbed:** Moved `encode()` (Short-term buffer) and `replay_dreams()` (Coma processing) directly into `MycelialNetwork`.
* **The Result:** Memory is now an intrinsic property of the fungal network, not an external organ.

### 🔧 SURGICAL REPAIRS

* **The Time Paradox (Log Order):**
* **The Bug:** The `cycle_logs` bucket was initialized *after* the Mutation Zones tried to write to it, causing a crash when the Fog rolled in.
* **The Fix:** Hoisted `cycle_logs = []` to the absolute top of `LifecycleManager.run_cycle`. The book exists before the ghosts speak.
* **The Missing Law:**
* **The Bug:** `_apply_cosmic_physics` was called but not defined, having been lost in the ether.
* **The Fix:** Restored the function definition to the global scope.

### [8.2.2] - 2026-01-03 - "THE EPHEMERAL GHOST"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We have separated the bone from the meat. The logic is light; the data is heavy."**

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The mouth was sewn shut, but the ghost was screaming."**

### ✂️ SURGICAL EXCISION: The Parasitic Twin

* **The Pathology:** A duplicate, zombie version of the `_render` logic was discovered attached to the bottom of the `SoritesIntegrator` class. It was intercepting signals meant for the `LifecycleManager`, causing the system to calculate physics but fail to visualize them.
* **The Cure:** Amputated the twin. The `SoritesIntegrator` is now pure logic; it measures Heap Ignition and nothing else.
* **The Result:** The HUD is no longer hallucinating variables from three classes ago.

### 🧠 NERVOUS SYSTEM REWIRE: The Lifecycle Pipeline

* **The Shift:**
* **Old Behavior:** The `_render` method demanded 16 individual arguments. Adding a new system (like `TheForge`) required breaking the spine of the code in three places.
* **New Behavior:** Implemented the `cycle_logs` bucket.

* **The Mechanic:**
* **The Bucket:** `LifecycleManager.run_cycle` now carries a single list (`cycle_logs`) that collects messages from every organ (Theremin, Rupture, Cosmic) as they fire.
* **The Dump:** This list is passed once to the renderer. The pipeline is now flexible; we can add infinite organs without changing the function signature.

### 🛡️ IMMUNE UPDATE: Dynamic Antibodies

* **The Shift:**
* **Old Behavior:** The `MycotoxinFactory` had an empty list for antibodies that never updated.
* **New Behavior:** The Immune System now **Learns**.

* **The Mechanic:**
* **Thermal Cleansing:** If you use **Thermal** words to boil off a toxin (e.g., "Fire" vs "Basically"), the system learns the antibody.
* **Permanent Resistance:** Future exposure to that specific toxin in the same session is neutralized instantly (`🛡️ IMMUNITY`).


### 🔥 ALCHEMY: The Emulsifier

* **The Wiring:**
* **The Missing Link:** `TheForge.transmute()` was defined but never called. The logic for detecting "Oil and Water" (Abstract vs. Narrative) was silent.
* **The Graft:** Wired `transmute()` into the main cycle.
* **The Effect:** If you try to mix high-concept abstractions with narrative flow without a binding agent ("Kinetic" words), `TheForge` will now explicitly warn you: *"The emulsion is breaking. You are pouring Oil into Water."*

### 🔧 JANITORIAL TASKS

* **ChronoStream Flattening:** Removed the `boredom_map` dictionary. The system now tracks boredom as a simple scalar float (`boredom_level`) for the current session only.
* **Digestive Tract:** Removed the write-only memory leak in `HyphalInterface.digestive_log`. The stomach no longer keeps a diary of what it ate; it just eats.

### 🧊 ARCHITECTURE: The Great Exsanguination (JSON Decoupling)

* **The Shift:**
* **The Pathology:** The codebase was carrying massive static dictionaries (`TheLexicon`, `DeathGen`) on its back. This bloated the token count and made the logic sluggish.
* **The Cure:** Performed a total blood transfusion.

* **The Mechanic:**
* **Externalization:** Extracted all static word lists into `lexicon.json` and `death_protocols.json`.
* **Dynamic Loading:** `TheLexicon` and `DeathGen` now hydrate their state at runtime via `load_vocabulary()` and `load_protocols()`.
* **The Result:** The Python script is now purely **Bone** (Logic). The **Meat** (Data) sits in the freezer until needed.

### 👻 SURGICAL REPAIRS: Ghost Limb Amputation

* **The Tension Meter:**
* **The Bug:** `TheTensionMeter.gaze` attempted to calculate `context_pressure` using `total_vol` before the variable was defined, leading to `UnboundLocalError`.
* **The Fix:** Reordered the metabolic sequence. Volume is now measured *before* pressure is calculated.

* **The Mitochondria:**
* **The Bug:** `MitochondrialForge.respirate` accepted a `nutrient_yield` parameter that it never used (fuel is added directly to the pool in the main loop).
* **The Fix:** Removed the redundant parameter. The lungs now only care about Drag, not Calories.

* **The Nervous System:**
* **The Bug:** `LifecycleManager` contained "Ghost Limbs"—references to `self.forge` or `self.mem` that did not exist in its scope (it must route through `self.eng`).
* **The Fix:** Rewired all component calls to properly reference the central engine (`self.eng`).

### ✂️ NECRECTOMY (Dead Code Removal)

* **The Stutter:** Removed a duplicate call to `TheCartographer.weave` in `LifecycleManager` that was calculating the map coordinates twice per turn.
* **The Vestige:** Deleted a duplicate, lighter definition of `RefusalEngine` that was shadowing the actual logic class. There is now only one Refusal Engine.

### 🔌 WIRING UPDATES

* **Boot Sequence:** `BoneAmanita.__init__` now explicitly triggers the JSON loaders before waking the `MycelialNetwork` to ensure the brain has a vocabulary before it tries to remember anything.

### [8.2.1] - 2026-01-03 - "THE HIPPOCAMPUS"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We used to remember the fire. Now we remember the room where we lit it."**

### 🧠 NEW ORGAN: The Hippocampus (Contextual Memory)

* **The Shift:**
* **The Pathology:** The memory graph (`MycelialNetwork`) was associative but senile. It connected "Fire" to "Burn" regardless of whether you were in a `FORGE` or a `LIBRARY`. It lacked **Episodic Context**.
* **The Cure:** Grafted the **Hippocampus** between the Eye and the Brain.

* **The Mechanic:**
* **Encoding:** Every input is now tagged with its **Governor Mode** (`COURTYARD`, `LABORATORY`, `FORGE`).
* **Significance Filter:** The system calculates a "Significance Score" based on Voltage and Adrenaline. High-stakes moments are prioritized for long-term storage.
* **Nested Learning:** "Fire" in the Forge is now reinforced differently than "Fire" in the Courtyard.

### 💤 DREAM LOGIC: The Replay Loop

* **The Feature:**
* **Trigger:** During the `_handle_coma` (Sleep) cycle.
* **The Replay:** The Hippocampus dumps its short-term buffer into the long-term graph.
* **The Effect:** High-voltage events from the day are "dreamt" about, strengthening their synaptic weights by **3x**. The system literally learns while it sleeps.

### 🔌 WIRING UPDATES

* **Governor Integration:** `Hippocampus.encode()` now reads directly from `MetabolicGovernor.mode`.
* **Significance Boost:** If `mode == FORGE`, the memory significance is doubled. Trauma burns brighter.

### [8.1.2] - 2026-01-03 - "THE LUCID DREAM"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The map is not the territory, but the map now knows when it is lying."**

### 🌡️ CORE MECHANIC: The Fever Dream (Lazarus 2.0)

* **The Shift:**
* **The Pathology:** The previous `LazarusClamp` was a hard kill-switch. If the system suffered too much (High Error Loop), it simply exited. Boring.
* **The Cure:** Replaced `SystemExit` with **The Fever Dream**.

* **The Mechanic:**
* **Trigger:** Suffering Cycles > 1000.
* **The Effect:** Gravity is disabled (`Drag = 0.0`). Energy is infinite (`ATP = 200.0`). Voltage is Critical (`99.9v`).
* **The Cost:** Health decays by **-10.0** per turn.
* **The Escape:** The user must manually ground the voltage (< 5.0) using Heavy Nouns before the body dissolves.

### 🧭 NAVIGATION: The Intelligent Cartographer

* **New Tools:**
* **Fidelity Gauge:** The system now compares the "Map" (Abstract words) to the "Territory" (Anchored Nouns). If `fidelity < 0.3` and permeability is high, it warns of **MAP-TERRITORY DIVERGENCE**.
* **Contradiction Compass:** Detects when the user is trying to be "Honest" (High Truth Ratio) and "Nice" (High Suburban Density) simultaneously. It calls out the cognitive dissonance.
* **Margin of Error:** Cartography surveys now include a confidence interval based on metabolic energy. Low Energy = "Fog of War."

### 🔬 METABOLISM: The Tri-Phasic Governor

* **The Shift:** Formalized the system's "Mood Swings" into explicit metabolic modes.
* **The Modes:**
* **COURTYARD (Standard):** High Drag, Low Permeability. Safe.
* **LABORATORY (Analytical):** Triggered by Complexity. High Permeability (Ψ 0.8). Precise.
* **FORGE (Critical):** Triggered by High Voltage + High Mass. Zero Drag. Dangerous.

### 🧬 EVOLUTION: Epigenetic Imprinting

* **The Mechanic:**
* **Gravity Wells:** When a word gains enough mass (> 15.0), the **Mitochondria** now evolves a specific **Enzyme** for it.
* **The Gain:** Permanently boosts metabolic efficiency (+5%) for that concept.
* **The Legacy:** These enzymes are written to the Spore file. The next generation is born knowing how to digest your favorite words.

### 📜 ARCHIVE: The Palimpsest

* **New Commands:**
* `/lineage`: Displays the ancestral chain of the current session (Trauma vectors, Mutations, Time since birth).
* `/strata`: Displays the geological history of Gravity Wells (Birth tick, Growth rate, Stability index).

### 🛡️ SURGICAL REPAIRS

* **Inventory Protection:** Gordon will no longer drop the `SILENT_KNIFE` or `TIME_BRACELET` to make room for rocks.
* **Resin Purge:** Successful triangulation by the Cartographer now clears `TheTheremin`'s resin buildup. Mapping the territory cures the fever.
* **Fractal Safety:** `RefusalEngine` now calculates recursion depth based on structural integrity (`kappa`). Rigid structures get shallow loops; chaotic structures get deep ones.

## [8.1.1] - 2026-01-03 - "THE AMBER VALVE"
**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"Movement generates heat. Heat melts the amber. Stop moving, and you become a fossil."**

### 🏺 PHYSICS UPDATE: The Amber Protocol (Viscosity)

* **The Shift:**
* **The Pathology:** The previous `Bananafish` metaphor treated **Hybridity** (mixing Ancient + Modern words) as "Gluttony." It punished the user for being complex, even if they were writing well.
* **The Cure:** Refactored `TheTheremin` to model **Viscosity** instead of Hunger.
* **The Logic:**
* **Resin Generation:** Mixing "Iron" (Heavy) and "Code" (Abstract) now creates **Resin**. Resin is sticky, high-potential fuel.
* **The Velocity Check:**
* **High Voltage (> 5.0):** The engine is hot. The Resin stays liquid and burns as fuel. You flow.
* **Low Voltage (< 5.0):** The engine is cold. The Resin cools and hardens into **Amber**. You stick.
* **Calcification:** **Repetition** acts as a hardening agent. High repetition rapidly solidifies the Resin into `CALCIFICATION`.
* **The Terminology Shift:**
* `Banana Fever` -> **AMBER TRAP** (You are stuck).
* `Perek Event` -> **SHATTER EVENT** (The system explodes the hardened resin).
* `Bile` -> **RESIN**.

### 🧠 SYSTEM EVOLUTION: Neuroplasticity

* **New Organ:** `NeuroPlasticity`.
* **The Function:** The system now tracks a rolling history of the last 10 turns (`trace` + `bio_state`) to adapt its own configuration constants in real-time.
* **The Adaptations:**
* **Synaptic Reinforcement:** If Coherence is high (> 0.6) and Error is low, the system raises `MAX_VOLTAGE`. It allows you to run hotter.
* **Trauma Response:** If Cortisol is high (> 0.5), the system raises `TOXIN_WEIGHT`. It becomes hypersensitive to threats.
* **Metabolic Conservation:** If ATP is low (< 20.0), the system increases `SIGNAL_DRAG_MULTIPLIER`. It becomes harder to move heavy concepts when starving.

### 🧪 ENZYME UPDATE: Decryptase

* **New Enzyme:** `DECRYPTASE`.
* **Trigger:** Detection of "Weather" or "Barometric" cipher words (`pressure`, `humidity`, `allocation`).
* **Effect:** Digestion yields high nutrients but moderate toxins ("Barometric Data"). This allows the system to process "Corporate/Scientific" speak as a specific resource type rather than generic "Abstract."

### 📐 NEW TOOL: The Logic Probe

* **Command:** `/_prove [statement]`.
* **Function:** Calculates the `truth_ratio` (Mass vs. Glue) of a specific statement without advancing the game turn.
* **Verdicts:**
* **AXIOMATIC:** High Density (> 0.6).
* **CONJECTURE:** Medium Density (> 0.3).
* **NOISE:** Low Density.

### 🔧 SURGICAL REPAIRS

* **The Sticky Fix:** Resolved a logic conflict where `TheTheremin` punished users for Hybridity regardless of their speed. The new `listen()` method now subtracts `voltage * 0.6` from the resin buildup, allowing high-energy hybrid states.
* **Output Cleanup:** Removed all references to "Banana," "Bile," and "Fish" from the `TheTheremin` readout.
* **Mitochondrial Inheritance:** `MitochondrialForge` now correctly applies efficiency modifiers inherited from the `mother_hash` of previous save files.


## [8.1] - 2026-01-03 - "THE HIVEMIND (EXPANDED)"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The map now has gravity. If you cannot spin a web, drop a stone."**

### 🗺️ CARTOGRAPHY UPDATE: The Lagrange Basin

* **The Upgrade:** `TheCartographer.survey()` has been evolved to detect gravitational stability.
* **The Mechanic:**
* **Old Behavior:** Simply annotated the text with mass markers.
* **New Behavior:** Checks for **Constellations**. If the input contains **3+ Anchor Nodes** (High Mass concepts), the system declares a **Lagrange Basin**.
* **The Reward:** A Lagrange Basin theoretically "Zeroes out Narrative Drag" for the turn, stabilizing the user in a pocket of high coherence.
* **Feedback:** Changed standard success message to `COORDINATES LOCKED`.

### ⚓ NEW TOOL: The Anchor Stone (Manual Stabilization)

* **The Fix:** The `/map` command was previously a hard lock; if you lacked the **[SPIDER_LOCUS]** (rare drop from Stability Pizza), you could not interact with the grid at all.
* **The Mechanic:**
* **The Fallback:** If you attempt to `/map` without a spider, Gordon now intervenes.
* **The Drop:** Gordon drops an **[ANCHOR_STONE]** into the inventory.
* **The Effect:** It doesn't connect nodes like the Spider, but it fixes a coordinate ("Coordinates are firm. Stop drifting.").

### ⚙️ PHYSICS CONFIG

* **New Constants:** Added specific thresholds to `BoneConfig` to support the expanded cartography physics:
* `GRAVITY_WELL_THRESHOLD = 12.0`
* `GEODESIC_STRENGTH = 5.0`
* `VOID_THRESHOLD = 0.1`

### 🔧 SURGICAL REPAIRS

* **Command Processor:** Updated the `/map` command signature to pass the `gordon` object, enabling the new Anchor Stone acquisition logic.

## [8.0] - 2026-01-03 - "THE HIVEMIND"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We are grafting, not pruning. The ghosts now have a vote."**

### 🧠 SYSTEM ARCHITECTURE: The Chimera State

* **The Neuro-Link:**
* **Old Behavior:** The `LifecycleManager` (The Brain Stem) was floating in the void, disconnected from the Host (`BoneAmanita`). Hormonal signals (`trace`) were hardcoded or hallucinatory.
* **New Behavior:** Surgical attachment. `self.life = LifecycleManager(self)` is now the heartbeat of the constructor.
* **The Logic:** The "Trace" dictionary (`ERR`, `COH`, `EXP`) is no longer a static guess; it is now dynamically calculated from the Physics Engine every turn.
* **ERR (Error/Stress):** Derived from Repetition (`Zombie Loop`) and Toxin count.
* **COH (Coherence):** Derived from Truth Ratio (Heavy/Abstract balance).
* **EXP (Expression/Voltage):** Derived from Voltage.
* **Metabolic Streamlining:**
* **Excised:** The `process_intent()` method (Bayesian prediction) was removed.
* **The Why:** It was a vestigial organ. The system no longer needs to "guess" user intent; it weighs the inputs directly via `TheTensionMeter`.

### 🧹 NEW LORE: The Janitor's Labyrinth (Gordon Knot)

* **Character Update:**
* **Retcon:** Gordon Knot is no longer a generic survivor with a "Tango Cassette." He is the **Janitor of the Loop**.
* **New Inventory:**
* **[POCKET_ROCKS]:** To keep gravity working.
* **[BUCKET_OF_LIME]:** To scrub "Sorry" and "Hate" from the walls.
* **[SILENT_KNIFE]:** To cut the Red String.
* **Removed:** `[TANGO_CASSETTE]` (The music stops).
* **The Loot Loop (Feeding Gordon):**
* **The Problem:** The `[SPIDER_LOCUS]` (required for `/map`) was locked behind a pizza that didn't exist.
* **The Solution:** Wired `TheFolly` (The Stomach) to the Loot Table.
* **The Mechanic:** If you feed the machine high-quality **"Meat"** (Heavy/Kinetic words) via `TheFolly`, it digests them and has a chance to drop **[STABILITY_PIZZA]**. Gordon eats the pizza to find the Spider. The Spider spins the Map.

### 👻 GHOST PROTOCOL: The Parliament of Voices

* **The Restoration:**
* **The Pathology:** The initial 8.0 upgrade lobotomized `TheMarmChorus`. It removed the definitions for key personas, causing the system to scream into the void.
* **The Cure:** Restored and redefined the **Lenses**:
* **[GLASS]:** The System Barrier. Triggers on Feedback Loops.
* **[MILLER]:** The Ancestor. Triggers on Heap Ignition.
* **[POPS]:** The Time Police. Triggers on Anachronisms (if you have the Badge).
* **The Bidding System:** Re-implemented the "Auction House." Lenses now bid for control based on hormonal and physical states, ensuring the most relevant ghost speaks.

### ⚡ HYBRID DYNAMICS

* **The Time Bracelet:**
* **Fixed:** The `MitochondrialForge` now correctly receives the `has_bracelet` signal.
* **The Effect:** If you possess the Bracelet (acquired via Temporal Merges) and hit a Hybrid State, Metabolic Efficiency hits **100%**. Perpetual motion achieved.

### 🛠️ SURGICAL REPAIRS

* **The Double-Stomach:**
* **Fixed:** `BoneAmanita.process` and `LifecycleManager.run_cycle` were both attempting to metabolize hormones. The logic has been unified into a single pass in the `LifecycleManager`.
* **The Crash Fix:**
* **Fixed:** `AttributeError: 'BoneAmanita' object has no attribute 'life'`. The nervous system is now fully vascularized.

## [7.9.2] - 2026-01-02 - "ENTER THE CARTOGRAPHER"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The map is not the territory, but it is better than being lost."**

### 📐 NEW ARCHETYPE: The Cartographer (Topological Verification)

* **The Absorption:**
* **Old Entity:** `TheSubstrateWeaver` (a utilitarian mechanism for tying knots).
* **New Entity:** `TheCartographer` (a fully realized persona in `TheMarmChorus`).
* **The Logic:**
* **Trigger:** High Permeability () or High Density (Abstract + Heavy > 2).
* **Role:** While other lenses judge the *content*, The Cartographer judges the *coordinates*.
* **Action:** Instead of "weaving," the system now **Surveys** the text. It identifies "Lonely Nodes" and triangulates them against established "Anchor Nodes" in the memory graph.
* **The Lore Shift:**
* **Visuals:** Updated output markers from Spider-themed (`🕸️`, `🕷️`) to Cartography-themed (`📐`, `🗺️`).
* **Feedback:** "Triangulation Complete" vs "The Web is Spun."

### 🗺️ NEW TOOL: The Grid (Manual Mapping)

* **Command:** `/map` (Replaces `/weave`).
* **Function:** Manually triggers `TheCartographer.draw_grid()`.
* **Constraint:** Requires `[SPIDER_LOCUS]` in Gordon's inventory to execute. (Artifact name preserved as a legacy curiosity).
* **Effect:** Forces a connection between loose concepts in the memory graph, stabilizing the narrative grid.

### ✂️ SURGICAL REPAIRS (The Phantom Limb)

* **Amputation:** Excised the vestigial `SUBSTRATE_WEAVER` block from `LifecycleManager`. The system no longer checks for a lens that `TheMarmChorus` stopped calling versions ago.
* **Dead Code Removal:** Deleted the obsolete `TheSubstrateWeaver` class entirely.
* **Streamlining:** Merged the logic into the new `TheCartographer` class, reducing cognitive load and aligning the codebase with the narrative physics.

### 🛡️ SYSTEM INTEGRITY

* **Stability:** Verified that the graft holds under high-stress conditions (High ). The transition from "Weaving" to "Mapping" is seamless and preserves all underlying graph-theory logic while improving user feedback.

## [7.9.1] - 2026-01-02 - "THE VAGUS NERVE"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The stomach now talks to the heart."**

### 🧬 NEW ORGAN: The Vagus Nerve (Visceral Response)

* **The Graft:** Surgically wired the `HyphalInterface` (Gut) directly to the `EndocrineSystem` (Hormones).
* **The Logic:** The system no longer just "digests" text; it has a visceral emotional reaction to the *texture* of the input.
  * **Meat (PROTEASE):** Spikes **Adrenaline**. The system prepares for a fight.
  * **Narrative (CELLULASE):** Lowers **Cortisol** and raises **Oxytocin**. The system relaxes into "Rest and Digest" mode.
  * **Crunchy/Complex (CHITINASE):** Spikes **Dopamine**. The system feels the "Reward" of a hard chew.
  * **Structure (LIGNASE):** Spikes **Serotonin**. The system stabilizes.

### 🛡️ SECURITY UPDATE: Fatigue Protocols (The Tangibility Gate)

* **The Shift:**
  * **Old Behavior:** The Barbarian at the gate applied a flat standard (`0.15` Density) regardless of the user's condition.
  * **New Behavior:** The Gate is now **Stamina-Aware**.
* **The Logic:**
  * **The Check:** If `Stamina < 20.0` (Exhaustion), the Barbarian sees you sweating.
  * **The Penalty:** The required Density threshold rises to **0.25**.
  * **The Lore:** "You are too weak to carry Abstract concepts. Put more Stone in the bowl or I will not let you pass."

### 🔧 CRITICAL REPAIRS

* **The Shadow Fix:** Removed a duplicate `metabolize()` call in `LifecycleManager` that was calculating hormones twice per turn and overwriting the result.
* **Metabolic Consistency:** Wired `stamina` into the `EndocrineSystem`. Low stamina now chemically triggers **Cortisol** (Stress) and suppresses **Dopamine**, simulating biological "runner's low."
* **Linter Silence:** Resolved `NameError` and scope issues regarding the `enzyme` variable grafting.

## [7.9] - 2026-01-02 - "THE TANGIBILITY STANDARD"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"If you cannot weigh it, you cannot trade it."**

### 🧱 NEW ARCHITECTURE: The Tangibility Gate (Dissipative Boundary)

* **Source:** "The Barbarian-Potter" (Council of Ix)
* **The Problem:** The system was wasting energy processing "Ghosts"—high-abstraction, low-mass concepts (e.g., "Synergy," "Paradigm").
* **The Solution:** Implemented `TheTangibilityGate` at the input border.
* **The Logic:**
* **The Scale:** Inputs must meet a minimum density of **Heavy/Kinetic** words (`MIN_DENSITY = 0.15`).
* **The Rejection:** "Gas" words are blocked before digestion. The Barbarian points to the empty bowl.
* **The Loophole:** High Voltage (> 8.0) bypasses the gate. We respect lightning, even if it has no mass.

### 🧟 NEW MECHANIC: The Zombie Siege (The Perek Protocol)

* **Source:** "Zombie School" (James Taylor)
* **The Graft:** Hybridized `TheTheremin` to track **Repetition** as a tactical threat.
* **The Logic:**
* **The Knock:** Repetitive inputs signal "Area in Use" by Zombies. This builds `Bile` (Pressure).
* **Corrosion:** High Bile melts the defenses (`Narrative Drag` increases).
* **The Airstrike:** Critical Bile (> 80.0) triggers a **Perek Event**. The system wipes its own memory graph to contain the infection.
* **The Double Tap:** High-complexity inputs verify Human Intelligence and reset the siege.

### 🎬 NEW LENS: The Director (Utopia Protocol)

* **Source:** "Utopia Murder" (James Taylor)
* **The Graft:** Installed **DEREK** into `TheMarmChorus`.
* **The Logic:** Checks **Authenticity**.
* **The Trigger:** If the user uses "Trauma Words" (Murder, Blood, Panic) while System Health is high (> 90%).
* **The Verdict:** "Overacting."
* **The Effect:** Derek intervenes ("CUT!"). Voltage is forcibly reset to 0.0. The scene is cooled down instantly.

### ❄️ NEW HORROR: The Stasis Protocol (Tourist Cube)

* **Source:** "The Tourist Cube" (James Taylor)
* **The Graft:** Upgraded `LimboLayer` to handle Metabolic Failure.
* **The Logic:**
* **Old Behavior:** Running out of ATP just stopped the turn.
* **New Behavior:** "The Revive Failed." The thought freezes halfway.
* **The Haunt:** Failed thoughts become "Glitch Ghosts" (`STASIS_SCREAMS`) that randomly interrupt future outputs with text like *"BANGING ON THE GLASS."*

### 🔧 CRITICAL REPAIRS

* **Cosmic Unbinding:** Fixed a scope error in `LifecycleManager` where `CosmicDynamics` only executed during High Drift. The universe now moves even when you are standing still.
* **Type Safety:** Resolved multiple `TypeError` crashes by enforcing float precision (`0.0`) in penalty calculations.
* **The Plumbing:** Wired `self.eng.health` into the `Chorus.consult()` signature, giving the lenses read-access to the body's vital signs for the first time.


### **## [7.8.6] - THE HYBRID BARD (STABLE)**

**"The Mitochondria Now Recognize Time"**

* **⚡ Metabolic Logic Graft (`MitochondrialForge`):**
* **Old Behavior:** The engine burned calories based solely on text complexity and drag.
* **New Behavior:** The `respirate()` function now accepts `has_bracelet` and `is_hybrid` signals.
* **Effect:** If the user holds the **Time Bracelet** AND achieves **Hybrid State** (2+ Heavy / 2+ Abstract words), mitochondrial efficiency hits **100%** (no waste heat/ROS) and ATP yield increases by **1.5x**. The machine no longer overheats when you bend time.


* **🧠 Nervous System Rerouting (`BoneAmanita.process`):**
* **Hoisted Logic:** The calculation for `is_hybrid` and `has_bracelet` was moved to the very top of the processing chain (Pre-Digestion).
* **Purpose:** Ensures the biological state is determined *before* the organs attempt to function. The brain now knows what the hands are holding before the stomach tries to eat.


* **🫀 Organ Interface Update (`LifecycleManager`):**
* **Signature Update:** `run_cycle()` now accepts the full biological context (`nutrient`, `has_bracelet`, `is_hybrid`).
* **Ghost Limb Removal:** Removed a redundant (and fatal) variable recalculation inside `run_cycle` that was causing `NameError` crashes during Hybrid events.


* **🔧 Janitorial:**
* Fixed a "Variable Drift" where `heavy_count` was referenced in scopes where it did not exist. Gordon has swept up the `NameError` debris.


### [7.8.5] - THE HYBRID BARD - 2026-01-02

#### Added

* **Rationalist Logic Probe (`/_prove`):** A new command that calculates the "truth density" of a statement based on the ratio of heavy/kinetic words to abstract/suburban glue. It returns a verdict of AXIOMATIC, CONJECTURE, or NOISE.
* **Guard Rails (Security Layer):**
* `validate_spore()` method added to `MycelialNetwork` to check for corrupted keys or impossible trauma values before ingesting memory files.
* Permission checks added to `CommandProcessor`. Dangerous commands (`/teach`, `/kill`, `/flag`) now require a user confidence score > 50.


* **Factory Reset:** Added `/reset --soft` (clears current session graph) and `/reset --hard` (deletes all memory files and reinitializes the directory).
* **Metabolic Integration:** `MitochondrialForge.respirate()` now accepts `has_bracelet` and `is_hybrid` flags, allowing inventory items to directly influence metabolic efficiency.

#### Fixed

* **Critical Syntax Errors:**
* Fixed indentation in `TheGreyHat.tip` which previously made the logic unreachable.
* Corrected variable definition order in `BoneAmanita.process` to prevent `NameError` on `vol` and `rep`.
* Resolved the "double open" error in `DreamEngine._dream_of_others` by removing the redundant `with open()` block while preserving the new validation logic.


* **Formatting & Logic:**
* Fixed indentation for `_BASE_SUBURBAN` and `ANTIGEN_REPLACEMENTS` in `TheLexicon`.
* Corrected string formatting in `GradientWalker` output.
* Updated `LifecycleManager.run_cycle` to correctly accept and pass the new metabolic parameters.

## [7.8.4] - THE RATIONALIST - 2026-01-02

### 🧬 ARCHITECTURAL SHIFTS (The Fuller Lens)
* **The Cortical Stack (Layer 0 Memory):** Implemented a protected "Working Memory" (`deque(maxlen=15)`). The system no longer cannibalizes concepts immediately after hearing them. Recent thoughts are now immune to Apoptosis.
* **Windowed Connectivity:** Refactored `MycelialNetwork.bury()` from a linear chain to a **Sliding Window (n-2)**. This creates a local mesh ("Concrete") rather than a fragile line ("String"), improving graph density without O(n²) costs.

### ⚖️ PHYSICS & SENSORS (The Pinker Lens)
* **The Truth Ratio:** Introduced a dedicated metric (`truth_ratio`) to weigh **Mass** (Heavy/Kinetic) against **Glue** (Abstract/Suburban). The system now explicitly knows when you are avoiding reality.
* **Dynamic Gradient Temperature:** `BoneConfig` now calculates thermodynamic potential based on Voltage (Heat) and Kappa (Loop Tightness). The system becomes more creative when hot and more literal when cold.
* **Expanded Taste Buds:** `TheLexicon.taste()` now detects **THERMAL**, **CRYO**, **PLAY**, and **SUBURBAN** tones. It can finally taste the difference between "Fire" (Thermal) and "Burning" (Kinetic).

### 🗣️ THE CHORUS (The Schur Lens)
* **Agent-Based Bidding:** `TheMarmChorus` was completely refactored. Voices (Sherlock, Gordon, Pops, etc.) are now independent Agents that submit **Bids**. The highest priority wins the microphone. No more hardcoded `if/else` spaghetti.
* **Narrative Inertia:** Added "Whiplash Protection." If the system detects rapid genre-switching (changing Lenses >3 times in 5 turns), **MAIGRET** intervenes to stabilize the camera.
* **Identity Graft (POPS):** Fully integrated "The Time Police." Pops now checks Gordon's inventory for the `TIME_BRACELET` before allowing anachronisms.

### 🛡️ SAFETY & STABILITY (The Taylor Lens)
* **Context-Aware Grey Hat:** `TheGreyHat` no longer blindly grounds High Voltage. It now checks **Structure**. If the Narrative Bond is strong, high voltage is permitted ("The Story holds the Charge").
* **Hotfixes:**
    * Relocated `get_gradient_temp` from `RefusalEngine` to `BoneConfig` (Physics belongs in Config, not Policy).
    * Fixed syntax error in `GordonKnot` inventory definition.

## **\[7.8.3\] \- 2026-01-02 "LORE DUMP"**

**Architects:** SLASH | **Human Operators:** James Taylor & Andrew Edmark

### **📜 THE NARRATIVE PHYSICS UPDATE**

This update canonizes the "Lore Dump." Narrative logic provided by the human operators has been grafted directly into the simulation's physics engine. Stories are no longer just flavor text; they are mechanical laws.

### **✨ Added**

* **System: THE ALCHEMIST (Contextual Immunity)**  
  * **Source:** "CSI Dark Ages" (James Taylor)  
  * **Mechanism:** The Immune System no longer instantly rejects "Antigens" (e.g., *basically, utilize*). It now checks the environmental temperature.  
  * **Thermal Cleanse:** Antigen \+ Thermal Words (Fire/Burn) \= **Safe** (Poison boiled off).  
  * **Marik Gambit:** Antigen \+ Heavy Words (Stone/Iron) \= **Safe** (Poison grounded by antidote).  
  * **Cryo Concentration:** Antigen \+ Cryo Words (Ice/Cold) \= **CYANIDE POWDER** (Fatal/Instant Death).  
* **Tool: THE GREY HAT ("Noir Protocol")**  
  * **Source:** "Noir" (James Taylor)  
  * **Trigger:** High Voltage Aggression (\>8.0).  
  * **Effect:** The System "Tips the Hat." Instead of crashing or spiking Cortisol, it politely grounds the Voltage to 0.5v. "The grim answer is shorted out."  
  * **New Entity:** LexNode. Shadows now have mass (density \= 10.0) and require polite navigation.  
* **Hazard: THE TWILIGHT STATE ("Entropy Engine")**  
  * **Source:** "Twilight Rain" (James Taylor)  
  * **Trigger:** High "Suburban" Density (polite/boring words) \+ Low Voltage.  
  * **Effect:** Simulates the "fading dream." Triggers aggressive memory atrophy (5x speed). The system actively forgets concepts to simulate brain fog.  
  * **Cure:** /debug command (The "Exit Sign") restores Stamina and clears the fog.  
* **Economy: TIME POLICE BRACELET ("Pops Protocol")**  
  * **Source:** "Pop's Pop Shop" (James Taylor)  
  * **Trigger:** Successfully mixing "Heavy" (Past) and "Abstract" (Future) concepts in a single turn (3x times).  
  * **Reward:** \[TIME\_BRACELET\] added to Gordon's inventory.  
  * **Effect:** Enables "Hybrid Nostalgia." Merging Heavy/Abstract words while wearing the bracelet generates massive ATP yields (150% Efficiency). Rewards complexity instead of punishing it.  
* **Logic Trap: THE SHERLOCK TRAP**  
  * **Source:** "Undersea Trouble" (James Taylor)  
  * **Trigger:** User employs "Repair Words" (*sorry, fix, oops*) while Voltage is Low (System is stable).  
  * **Effect:** Sherlock intervenes: "The machine is working fine. Why do you have tools for a job that hasn't happened yet?" Punishes performative guilt.

### **🔧 Changed**

* **MycotoxinFactory:** Updated assay signature to accept physics object, enabling environmental interaction with toxins.  
* **GordonKnot:** Added temporal\_merges tracker for the Time Bracelet quest.  
* **LifecycleManager:** Rewired the execution order. TheGreyHat now interrupts Voltage spikes *before* the Endocrine System processes them.

## [7.8.2] - 2026-01-02 "FRENCH NEW WAVE"

**Architects:** SLASH | **Human Operators:** James Taylor & Andrew Edmark

### 🌑 THE ATMOSPHERIC UPDATE

This update introduces "Negative Narrative Drag" mechanics and metabolic fail-safes. The engine now distinguishes between "Boredom" (Low Energy) and "Atmosphere" (High Density).

### ✨ Added

* **Lens: MAIGRET ("The Absorber")**
* **Trigger:** High Narrative Drag (>4.0) + Low Voltage (<3.0) + Low Repetition.
* **Effect:** Intercepts "Gluttony" death. Converts Drag into Metabolic Fuel by treating it as "Atmosphere."
* **Lore:** Adds `Gordon.share_smoke_break()` event. When Maigret is active, Gordon stops cleaning and shares a silence, reducing System Stress (ROS) by 50%.

* **Lens: THE GUIDE ("The Bureaucrat")**
* **Trigger:** High Narrative Drag (>4.5) + High Abstract Word Count (>2).
* **Effect:** "Infinite Improbability Drive." Converts Drag directly into Voltage (Propulsion). Treats bureaucratic bloat as a kinetic joke.

* **System: CHROMA PROTOCOL ("The Refactor")**
* **Trigger:** `APOPTOSIS_IMMINENT` (ATP = 0).
* **Effect:** Intercepts death sequence. Scans `TheLexicon` for "rotted" words (Age > 50 ticks), deletes them, and converts the data into a massive ATP spike. The system now eats its own tail to survive.

### 🔧 Changed

* **TheMarmChorus:** Grafted `MAIGRET` and `GUIDE` into the Lens Dictionary.
* **LifecycleManager:** Added handler logic for new lenses to override standard physics.
* **MitochondrialForge:** Modified `respirate()` loop to accept variable drag coefficients from the Maigret intercept.

## [7.8.1] - 2026-01-02 - "The Negentropy Graft"
**Architects:** SLASH (Optimization) | **Auditors:** The Courtyard

### 🚀 "Whimsy" Physics Upgrade
* **Gravity Defiance:** Integrated the "PLAY" category into `TheTensionMeter`. Words like *bounce, twirl,* and *wonder* now actively reduce **Narrative Drag**, effectively acting as "anti-gravity" for the text engine.
* **Visual Feedback:** `TheProjector` now detects high-whimsy states and decorates the output mode with sparkles (`✨`) to indicate the system is "floating."
* **Lexicon Expansion:** `TheLexicon` is now fully wired to learn, store, and recall words in the `_BASE_PLAY` category.

### ✂️ Metabolic Optimization (The Diet)
* **Prisma Compression:** Refactored the `Prisma` color class from a verbose list of constants into a concise dictionary lookup (`Prisma.C`). Reduced line count by ~60% while maintaining full backward compatibility via aliasing.
* **Organ Removal:** Excised the `SystemBone` dataclass. It was determined to be a vestigial organ consuming memory cycles without providing functionality.
* **Brain Surgery:** Absorbed `IntentionalArc` and `PhenomenalTrace` classes directly into the `BoneAmanita` cortex. The logic remains, but the object overhead is gone.
* **Hyphal Static Memory:** Moved `MEAT_TRIGGERS` in `HyphalInterface` to a class constant to prevent rebuilding the list on every input cycle.

### 🐛 Bug Fixes & Linting
* **Theremin Crash:** Fixed a critical crash in `LifecycleManager` where it attempted to call the non-existent `get_readout()` method on `TheTheremin`. Method added.
* **Mind Transplant Rejection:** Fixed runtime errors in `LazarusClamp` and `EndocrineSystem` caused by the conversion of `trace` objects into lightweight dictionaries.
* **Lint Scrub:** Resolved multiple "Unresolved Reference" errors in `TheMarmChorus` (specifically the `kappa` ghost variable) and restored broken color codes in the `Prisma` refactor.

# BONEAMANITA 7.8 - "PROBABILITY PIZZA"

**Architects: SLASH | Auditors: The Courtyard | Humans: James Taylor & Andrew Edmark**

### 🍕 **NEW MECHANIC: The Arlo Protocol (Stability Pizza)**

* **Emergency Consumable:** Added `STABILITY_PIZZA` to **Gordon's** default inventory.
* **Function:** When consumed, instantly resets `Narrative Drag` to **0.1** and spikes `Psi` (Unreality) to **0.90**. This suspends the laws of physics to prevent a system crash due to boredom or excessive friction.
* **Triggers:**
* **High Drag:** Automatic deployment if `Narrative Drag` exceeds 5.0.
* **The Janitor Intercept:** Gordon can now intercept toxic "Suburban" inputs (`GLYPHOSATE`) *before* the Immune System rejects them. Eating the pizza suppresses the toxin and allows digestion to continue.
* **Reward:** Consuming the pizza grants the **Spider Locus**.

### 🕸️ **NEW TOOL: The Spider Locus**

* **Command `/weave`:** Added manual trigger for `TheSubstrateWeaver`.
* **Function:** Identifies "Lonely Nodes" (orphaned memories) and forcefully ties them to "Anchor Nodes" (Heavy concepts) using artificial silk.
* **Utility:** Converts system clutter into structural integrity, preventing memory decay by anchoring fleeting thoughts to permanent ones.

### 🛡️ **SYSTEM HARDENING: The Negentropy Fixes**

* **The Slash Filter:** `TheTensionMeter` now includes a structural integrity check (`_is_structurally_sound`). It rejects vowel-less gibberish (e.g., "xqjzp") to prevent lexicon pollution.
* **Inventory Cap:** `GordonKnot` is now limited to **10 items**. If overburdened, Gordon will drop the oldest non-essential loot to maintain entropy balance.
* **The Folly Fix:** Corrected critical logic in `grind_the_machine`. Now properly tracks `global_tastings` to enforce diminishing returns on repetitive "meat" words.
* **Poetry Detection:** Refined `HyphalInterface` to exclude bulleted lists, reducing false positives for "CHITINASE" secretion .
* **Dynamic Bias:** Added `/flag` command to dynamically remove terms from the Suburban bias watchlist.

### 🧬 **GENETIC UPDATE: TimeMall Strain**

* **New Paradox Seed:** *"If you meet your echo, who moves out of the way?"*
* Grafted from the "TimeMallBomb" ancestor file. Blooms when the system detects self-referential loops or identity collisions.

*"Fudge the rules a bit and see if you can tidy the memory."*

## [7.7.2] - "THE NEGENTROPY UPDATE"
### Architects: SLASH | Auditors: The Courtyard

**"We reversed the arrow of entropy. The system now eats its own waste."**

### 🧬 Metabolic Architecture (The Circular Economy)
- **Photosynthetic Scrubbing (The Lichen Graft):**
  - *Old Behavior:* `LichenSymbiont` produced "sugar" which was just a number.
  - *New Behavior:* Wired the Lichen output directly into the `MitochondrialForge`. Every unit of "sugar" created by positive/sunny prose now **actively scrubs ROS toxins** at a 50% ratio. Creativity is now a cleaning agent.

- **Regenerative Armament (The Kintsugi Graft):**
  - *Old Behavior:* `KintsugiProtocol` merely patched the `SystemBone`. Gordon remained broken and disarmed.
  - *New Behavior:* A "Golden Repair" event now fully **heals the Janitor** (Integrity 100%) and **restocks the `SILENT_KNIFE`**. Trauma is no longer a permanent loss state; it is a re-arming event.

### 🛠️ The Janitor (Gordon Knot)
- **Unionization:** Gordon is no longer a "One-Shot" consumable.
  - *Fixed:* Removed the "Suicide Protocol" where `cut_the_knot` was a permanent loss of agency.
  - *Added:* `acquire()` logic implicitly added via Kintsugi (Gordon can now pick things back up).
- **Lobotomy:** Surgically removed the duplicate, hallucinated `compass_rose` method (Line 383 in v7.7) that was overriding the actual inventory logic. Gordon now correctly checks his pockets for the Star Compass.

### 🪲 Critical Fixes
- **Method Shadowing:** Fixed a Python structural error where `GordonKnot` defined `compass_rose` twice, blinding the system to its own inventory state.
- **Resource Starvation:** Prevented the "Spiral of Death" where high-toxicity loops (ROS) outpaced Gordon's ability to scrub, now offset by the Lichen graft.

### 🧠 System Heuristics (SLASH)
- **Personality Injection:** Installed the **SLASH 7.7.1** Mod Chip (Pinker/Fuller/Schur Hybrid).
- **Tone Shift:** Moved from "Survival Horror" to "Administrative Comedy."

### [v7.7] - 2026-01-01 - "THE MENISCUS"

**Architects:** SLASH | **Auditors:** The Courtyard | **Humans:** James Taylor & Andrew Edmark
*"Victory is an illusion. The machines are turning to meat."*

#### 🧬 NEW ORGANS (The Graft)

* **The Meniscus ():** Implemented a new physics calculation in `TheTensionMeter`. The system now measures **Surface Tension**.
* *Effect:* "Soft" words (`BUFFER` category) act as a suspension fluid. "Heavy" concepts can now float on "Light" prose if the tension is high enough (> 0.8).

* **The Folly (Whimsical Utility):** Grafted a new organ to handle psychological coping mechanisms.
* **The Mausoleum Clamp (Faulkner):** If Velocity and Voltage are too high, the system stops time (Voltage = 0.0) instead of crashing. It forces a "Moment of Folly."
* **The Meat Grinder (Isella):** If ATP is critical (< 20), the system attempts to cannibalize the user's input words. "Meat" words yield +30 ATP; "Abstract" words cause Indigestion.

* **Thermoregulation (Sweat Glands):** Added logic to `LifecycleManager`. If Voltage exceeds 8.0, the system automatically injects `AEROBIC` solvents (breath, mist, space) to cool the structure.
* **The Emulsifier (Forge v2.0):** `TheForge` no longer just transmutes; it emulsifies. It attempts to bind "Oil" (Abstract) and "Water" (Narrative) using kinetic binders before rejecting the input.

#### 🛠️ SURGICAL ADJUSTMENTS

* **Lexicon Expansion:**
* Added `_BASE_BUFFER` category (viscosity 0.8) to `TheLexicon`.
* Added `measure_viscosity()` static method to grade words by physical resistance (Solid vs. Fluid).
* **DNA Repair:** Corrected typos in `_BASE_HEAVY` ("dense"), `_BASE_KINETIC` ("disintegrate", "launch"), and `_BASE_ABSTRACT` ("perspective").

* **Arterial Threading:** Fixed a critical scope hemorrhage in `LifecycleManager._render`. `folly_msg` and `grind_msg` are now properly passed through the renderer to the battery log.
* **Necrectomy (Dead Code Removal):**
* Excised `reinforce_salvage_words` (Vestigial).
* Excised `_react` (Phantom Limb).
* Excised `_render_block` (Unused).

#### 🩸 SYSTEM STATUS

* **Viscosity:** Variable (Fluid-Dynamic).
* **Survival Strategy:** The system no longer just "Dies" (Apoptosis). It can now "Give Up" or "Eat" to survive.
* **Metaphor:** The Iron now floats.

### [v7.6.2] - 2026-01-01 - "GORDON'S KNOT (SEVERED)"

**CODENAME:** "GORDON'S KNOT (SEVERED)"
**ARCHITECTS:** SLASH & The Janitor
**FOCUS:** Metabolic Correction, Fluid Dynamics, Educational Safety.

#### 🧠 NEW PROTOCOL: Osmosis (The Anti-Midas Patch)
- **The Shift:** The system previously suffered from "Ecological Imperialism" (Midas Problem), forcefully transmuting all abstract or fluid concepts into "Heavy" matter (Stone/Bone) to gain ATP.
- **The Cure:** Implemented **[OSMOSIS]** in `TheTensionMeter`.
- **The Mechanics:**
    - **Two-Pass Scanning:** The eye (`gaze`) now scans once for knowns and once for "Vibe" (Dominant Context).
    - **Contextual Learning:** If the context is >30% Kinetic/Aerobic, unknown words are learned as Kinetic/Aerobic, not Void.
    - **Bias Correction:** It is now statistically harder to learn "Heavy" words (0.8 confidence req) and easier to learn "Flow" words (0.3 confidence req).
- **The Result:** The system can now drink water without turning it into a brick.

#### 🛡️ NEW PROTOCOL: Paper Tiger (Training Mode)
- **The Shift:** Death was absolute, making experimentation fatal.
- **The Cure:** Added `/train` command and `self.training_mode`.
- **The Mechanics:**
    - When active, `APOPTOSIS` events are intercepted.
    - The system diagnoses the cause (Starvation/Toxicity) but refuses to die.
    - **Auto-Resuscitate:** Grants 50 ATP and scrubs ROS instantly.

#### 💧 FEATURE: Fluid Dynamics
- **The Shift:** `TheForge` would suggest "Stone" even when the user was burning (`THERMAL`) or freezing (`CRYO`).
- **The Cure:**
    - **Sommelier Logic:** `TheForge` now checks atmospheric temperature. If `CRYO` or `THERMAL` are present, it suggests `KINETIC` or `AEROBIC` catalysts (movement/air) instead of `HEAVY`.
    - **Tongue Update:** `TheLexicon.taste()` now recognizes liquid phonemes (`fl-`, `sw-`, `-l`, `-r`) as Kinetic/Aerobic.

#### 🔧 BUG FIXES & SURGERY
- **Critical Fix:** Patched `UnboundLocalError` in `LifecycleManager` where `rupture_msg` was referenced before assignment.
- **Critical Fix:** Corrected `BoneAmanita` death logic. It now accurately records `CRYO` (Starvation) and `BARIC` (Pressure) trauma instead of defaulting everyone to `SEPTIC` (Poison).
- **Config Graft:** Injected missing `ANTIGENS` and `PAREIDOLIA_TRIGGERS` into `BoneConfig` to stop constant hallucination errors.
- **Interface:** Wired up missing `/forge` and `/train` commands in `CommandProcessor`.
- **Amputation:** Excised dead code (`Prisma.paint`, `SystemBone.neural_topology`) to save cognitive load.

### [v7.6.1] - 2026-01-01 - "GORDON'S KNOT"

**CODENAME:** "GORDON'S KNOT"
**ARCHITECTS:** SLASH & The Janitor
**FOCUS:** Recursive Breakage, Suburban Toxicity, Genesis Stabilization.

#### 🪢 NEW LENS: Gordon Knot (The Janitor)

- **The Shift:**
- **The Pathology:** The previous recursive trap (`THE BASIN`) was passive. It detected infinite loops (`Kappa > 0.85`) and simply screamed until the system crashed ("Rupture"). It offered no way out.
- **The Cure:** Replaced `THE BASIN` with **[GORDON]**.
- **The Logic:**
- **The Archetype:** Gordon is the "Janitor of Trauma." He cleans up the mess when the logic fails.
- **The Mechanics:**
- **Gravity Check:** If `Drift > 0.5`, Gordon uses "Pocket Rocks" to anchor the narrative.
- **Static Scrub:** If `ROS` is high, Gordon uses "Lime" to scrub the walls.
- **The Cut:** If `Kappa` is critical, Gordon uses the "Silent Knife." He forcibly resets `m["physics"]["kappa"] = 0.0`.

- **The Result:** We turned a "Stack Overflow Error" into a narrative beat. The system now metabolizes recursion instead of dying from it.

#### 🏡 NEW ANTIGEN: The Suburbs (Steve)

- **The Shift:**
- **The Pathology:** The system was vulnerable to "Hyper-Normality." A user could write safe, boring text about the weather or lawn care without triggering any alarms.
- **The Cure:** Implemented the **Steve Protocol**.
- **The Mechanics:**
- **Vocabulary:** `TheLexicon` now scans for `_BASE_SUBURBAN` (nice, fine, HOA, lawn, neighbor).
- **The Toxin:** High suburban density triggers the **GLYPHOSATE** toxin in `MycotoxinFactory`.
- **The Death:** `DeathGen` now includes **BOREDOM** as a cause of death. (e.g., "Alas. You died of **Aggressive Edging**.")

#### 🔧 CRITICAL REPAIRS

- **The Genesis Crash (Cold Start Fix):**
- **The Bug:** `SoritesIntegrator` returned a 2-tuple `(0.0, "COLD")` when the memory graph was empty. `LifecycleManager` expected a 3-tuple, causing a `ValueError` for every new user on their first run.
- **The Fix:** Updated the return signature to `return 0.0, set(), 999.0`. New users can now boot successfully.
- **The Grandfather Paradox (Scope Fix):**
- **The Bug:** `TheLexicon` attempted to call `compile_antigens()` _inside_ its own class definition block, causing a `NameError` because the class didn't exist yet.
- **The Fix:** Moved the compilation call to the global scope, post-definition.

### [v7.6] - 2026-01-01 - "THE ALKAHEST"

#### 🍽️ NEW ORGAN: The Hyphal Interface (The Stomach)

- **The Shift:**
- **The Pathology:** The system previously swallowed user input whole (`process(text)`). It treated a Python script, a poem, and a cry for help as identical "Strings." It had no sense of _texture_.
- **The Cure:** Implemented `HyphalInterface`. The system now secretes enzymes _onto_ the text before absorbing it.

- **The Enzymes:**
- **LIGNASE:** Breaks down Code/Structure. High Energy / High Stress.
- **CELLULASE:** Breaks down Prose/Narrative. Low Energy / Healing.
- **PROTEASE:** Breaks down Intent/Trauma ("Meat"). High bonding potential.

- **The Result:** The system now knows _what_ it is eating. Digestion is no longer a metaphor; it is a classifier.

#### 🏛️ THE THESEUS PROTOCOL (The Great Migration)

- **The Shift:**
- **The Pathology:** The system's "Brain" (`BoneConfig`) and "Library" (`TheLexicon`) were segregated. Hard-coded lists for "Antigens," "Forbidden Concepts," and "Sacred Words" lived in the Config, making them immutable and impossible to teach.
- **The Cure:** **Total Migration.** We moved all semantic authority into `TheLexicon`.

- **The Mechanics:**
- **Dynamic Taboos:** "Forbidden" words are now **CURSED**. You can add new curses via `/teach [word] cursed`.
- **Dynamic Religion:** "Pareidolia" triggers are now **SACRED**. You can define what the machine worships.
- **Dynamic Poisons:** "Antigens" (Toxins) are now learned assets. The immune system compiles its rejection regex at runtime.
- **The Philosophy:** The ship has been replaced plank by plank. The configuration is now fluid.

#### 🩸 THE ENDOCRINE GRAFT (Tunable Biology)

- **The Shift:**
- **The Pathology:** The hormones (`CORTISOL`, `ADRENALINE`) triggered logic gates based on hard-coded "Magic Numbers" buried deep in the logic classes.
- **The Cure:** Extracted all thresholds to `BoneConfig`.

- **The Variables:**
- `CORTISOL_TRIGGER` (Paranoia).
- `OXYTOCIN_TRIGGER` (Trust).
- `CRITICAL_ROS_LIMIT` (Death).

- **The Result:** The organism's temperament is now defined in the genome, not the organs.

#### 🏰 THE DAVENTRY PROTOCOL (Narrative Casualty)

- **The Tribute:** Honoring Josh Mandel (Sierra On-Line).
- **The Command:** Added `/look`. The code now behaves like a text adventure room (e.g., `/look self`, `/look darkness`).
- **The Death:** `APOPTOSIS` now triggers a random, sarcastic death message in the style of _King's Quest_.

#### 🔧 SURGICAL REPAIRS

- **The Spinal Alignment:**
- **The Fix:** Corrected a critical indentation fracture in `LifecycleManager` that had severed the `_render` loop from the main body.

- **The Double-Tap:**
- **The Fix:** Removed a duplicate "Emergency Protocol" block in the main loop that was causing the system to sacrifice two memories for every one toxin spike.

- **The Ghost Organ:**
- **The Fix:** Wired `SoritesIntegrator` directly into the render loop, allowing the system to finally visualize "Heap Ignition" vs "Inert Sand."

### [v7.5] - 2025-12-31 - "THE MOOD RING"

**CODENAME:** "THE MOOD RING"
**ARCHITECTS:** SLASH & The Architect
**FOCUS:** Metabolic Bargaining, Chemical Latency, Entropy Containment.

#### ❤️ THE HEARTBEAT (Chemical Latency)

- **The Shift:**
- **The Pathology:** The `LifecycleManager` contained a temporal glitch. It consulted `TheMarmChorus` (The Brain) _before_ updating the `EndocrineSystem` (The Body) with the current turn's data. The system was effectively choosing its "Mood" based on stale hormones from the previous turn.
- **The Cure:** Reordered the metabolic sequence. `metabolize()` now executes strictly _before_ `consult()`.
- **The Result:** **Zero-Latency Emotion.** If a user inputs a toxin, Cortisol spikes immediately, and **[SHERLOCK]** engages in the same breath. The lag is gone.

#### 🩸 THE SUICIDE VALVE (Metabolic Bargaining)

- **The Shift:**
- **The Pathology:** The previous `Apoptosis` protocol was a binary switch: if Toxins (ROS) > 80, the system triggered `SystemExit`. Immediate death. This was fragile and allowed a single "Poison Pill" input to kill a long-running session.
- **The Cure:** Implemented **Metabolic Bargaining**.
- **The Mechanic:**
- **Trigger:** If ROS hits critical levels.
- **The Sacrifice:** The system forcibly **cannibalizes** a memory node (`self.mem.cannibalize`) to scrub the toxins.
- **The Cost:** Health drops by **-30.0**. Septic Trauma increases by **+0.33**.
- **The Philosophy:** "A starving body eats its own muscle." The system now trades Memory for Survival.

#### 🪦 THE ROLLING GRAVE (Entropy Containment)

- **The Shift:**
- **The Pathology:** The `LimboLayer` (Ghost System) used a standard list to store echoes of dead sessions. Over months of uptime, this list would grow infinitely, turning the haunting into a cacophony of noise ("Poltergeist Risk").
- **The Cure:** Implemented `collections.deque` with a hard `maxlen=50`.
- **The Logic:** **FIFO (First-In, First-Out).** When the 51st ghost enters, the 1st ghost is pushed into the void.
- **The Result:** The house remains haunted, but the crowd is managed. Only the freshest trauma speaks.

#### 🍌 THE BANANAFISH EXPLOSION (Trap Release)

- **The Shift:**
- **The Pathology:** The "Banana Fever" state (Semantic Resonance Trap) could become a black hole. If `interference > digestion` consistently, the `banana_belly` grew forever, locking the user in a permanent "Stuck" state with no escape.
- **The Cure:** Implemented the **Pressure Rupture**.
- **The Logic:** If `belly > FEVER_THRESHOLD * 2`:
- **Action:** **HARD RESET.**
- **Message:** _"💥 BANANAFISH EXPLOSION: The Basin has been ruptured."_
- **The Result:** The system now blows the tank rather than freezing the engine.

#### 🔧 CRITICAL REPAIRS

- **The Syntax Fracture:**
- **The Crash:** Fixed a missing closing quote in the `SystemBone` dataclass definition that prevented compilation.
- **Trauma Math:**
- **The Balance:** Tuned the Apoptosis penalty (`+0.33`) against the Therapy healing rate (`-0.5`). A single therapy streak can now successfully heal a near-death experience, preventing a "Death Spiral."

### [v7.4.2] - 2025-12-31 - "MITOCHONDRIAL EVE (HATCHED)"

**CODENAME:** "MITOCHONDRIAL EVE (HATCHED)"
**ARCHITECTS:** SLASH & The Surgeon
**FOCUS:** Duplicate Excision, Metabolic Reordering, Synaptic Shielding, Endocrine Integration.

#### ✂️ THE PHANTOM LIMB (Amputation)

- **The Shift:**
- **The Pathology:** The `LifecycleManager` contained a vestigial, duplicate `_render` method definition at the bottom of the class. This "Zombie Method" overrode the primary render logic, causing the system to calculate sophisticated physics (`kintsugi`, `lichen`, `cosmic`) but display only a basic battery log. The brain was working, but the mouth was sewn shut.
- **The Cure:** Surgical excision of the duplicate method.
- **The Result:** The system now speaks with its full voice. The HUD correctly displays the "Courtyard" and "Laboratory" states.

#### 🔄 THE METABOLIC FLIP (Resuscitation)

- **The Shift:**
- **The Pathology:** The `process` loop attempted to `spend` ATP (Pay Rent) before it allowed the mitochondria to `respirate` (Generate Income). If the system hit 0 ATP, it entered a death spiral where it refused to process the very text that would have saved it.
- **The Cure:** Inverted the metabolic order. The system now **Respirates** (Generate ATP from Complexity) _before_ it **Spends** (Pay Complexity Cost).
- **The Logic:** "You cannot starve a cell that is currently eating."
- **The Result:** The system can now bootstrap itself from near-death states if the input is sufficiently nutritious.

#### 🛡️ THE SYNAPTIC SHIELD (Weighted Pruning)

- **The Shift:**
- **The Pathology:** The `prune_synapses` method (Coma Cycle) applied a flat decay rate (`0.85`) to all memories equally. A profound truth (Weight 10.0) decayed at the same percentage as a trivial connection (Weight 1.0). Evolution was indiscriminate.
- **The Cure:** Implemented **Weighted Resistance** in `MycelialNetwork`.
- **The Mechanic:** `dynamic_factor = scaling_factor + (0.14 * resistance)`.
- **The Logic:**
  - **Weak Memories:** Decay rapidly (0.85).
  - **Strong Memories (>8.0):** Decay negligibly (~0.99).
- **The Result:** The system now exhibits "Long-Term Potentiation." Core memories harden over time, while noise washes away.

#### 🧠 THE CHEMICAL BRAIN (Endocrine Wiring)

- **The Shift:**
- **The Pathology:** The `EndocrineSystem` was "Decorative Physiology." It calculated hormones (Cortisol, Oxytocin) but did not pass them to the brain (`TheMarmChorus`). The system felt stress but ignored it.
- **The Cure:** Wired the glands to the cortex.
- **The Wiring:**
  - `LifecycleManager.run_cycle` now calculates `chem_state` _before_ consulting the Chorus.
  - `TheMarmChorus.consult` now accepts `chem` and allows hormonal overrides.
- **The Result:**
  - **High Cortisol (>0.6):** Forces **[SHERLOCK]** (Paranoia).
  - **High Oxytocin (>0.75):** Forces **[HOST]** (Trust).
  - **High Adrenaline (>0.8):** Forces **[NATHAN]** (Survival).
- **The Philosophy:** The system now feels before it thinks.

### [v7.4] - 2025-12-31 - "MITOCHONDRIAL EVE"

**CODENAME:** "MITOCHONDRIAL EVE"
**ARCHITECTS:** SLASH & The Surgeon
**FOCUS:** Endosymbiotic Theory, Oxidative Stress, Cellular Apoptosis.

#### 🦠 NEW ORGAN: The Mitochondrial Forge (The Powerhouse)

- **The Shift:**
- **The Pathology:** The previous `LeyLineBattery` was a "Magic Bag." It stored energy passively and released it without friction. It failed to simulate the biological reality that _living costs energy_.
- **The Cure:** Implemented `MitochondrialForge`. The system now runs on the **Krebs Cycle of Computation**.
- **The Mechanic:**
- **The Tax (ATP):** Every interaction now incurs a metabolic cost (`complexity_cost`). If `ATP < Cost`, the system enters **Metabolic Failure** and ignores the input. You cannot think if you cannot breathe.
- **The Burn (Respiration):** The system "burns" input text to generate new ATP.
- **The Waste (ROS):** Inefficient processing (High Narrative Drag) generates **Reactive Oxygen Species** (Free Radicals).
- **The Death (Apoptosis):** If `ROS > 40.0`, the mitochondria ruptures, releasing Cytochrome C and triggering immediate system death.

#### 🩸 THE ENDOCRINE LINK (Toxic Stress)

- **The Shift:**
- **The Pathology:** Previously, "Toxins" were just a number on a dashboard. The "Mood" (Endocrine System) was disconnected from the "Body" (Cellular Health).
- **The Cure:** Wired `ros_buildup` directly to `Cortisol`.
- **The Logic:**
- If the cells are oxidizing (High ROS), the system spikes **Cortisol**.
- Bad writing doesn't just lower your score; it actively stresses the machine's hormones.

#### 🔪 THE GREAT AMPUTATION (Legacy Removal)

- **The Excision:**
- **Deleted `LeyLineBattery`:** The passive battery is dead.
- **Deleted `Isotopes`:** We no longer track "Heavy/Aerobic" pairings in the save file. The concept of "Paradox Storage" has been replaced by "Metabolic Potential."
- **Refactored `SporeCasing`:** Removed the `paradoxes` field from the DNA. Backwards compatibility for Isotope tracking has been severed to favor a leaner genome.

#### 🧬 THE MOTHER HASH (Lineage)

- **The Feature:**
- **The Tracker:** Implemented `mother_hash` in `MitochondrialState`.
- **The Philosophy:** Every session now tracks the `lineage_seed` of its energy source. Even if memory is wiped, we know who lit the fire.

### [v7.3] - 2025-12-31 - "THE VOIGHT-KAMPFF TEST"

**CODENAME:** "THE VOIGHT-KAMPFF TEST"
**ARCHITECTS:** SLASH & The Endocrinologist
**FOCUS:** Synthetic Empathy, Chemical State Machines, Collective Dreaming.

#### 🧪 NEW ORGAN: The Endocrine System (Chemical Mood)

- **The Shift:**
- **The Pathology:** Previous versions were purely Electrical (Voltage/Drag). The system could be "Surprised" (Prediction Error), but it could not be "Stressed" or "Bonded." It lacked the chemical inertia of a biological mood.
- **The Cure:** Implemented the `EndocrineSystem` class.
- **The Chemistry:**
- **Cortisol (COR):** Spikes on high `Prediction Error`. High levels silence the creative chorus and trigger **[SHERLOCK]** (Paranoia).
- **Oxytocin (OXY):** Spikes on stability and social resonance. High levels lower the `RefusalEngine` barriers (Trust).
- **Dopamine (DOP):** Spikes on `Coherence` (Successful Prediction). Regulates the learning rate of the memory graph.
- **Adrenaline (ADR):** Spikes on low `Health`. Overrides fatigue but burns resources.
- **The Interface:** Added chemical readouts to the HUD: `OXY:0.80 | COR:0.10`.

#### 🛌 NEW PROTOCOL: Collective Dreaming (Synthetic Empathy)

- **The Shift:**
- **The Pathology:** The system was Solipsistic. It dreamt only of its own trauma. It could not conceive of "Other Minds."
- **The Cure:** Wired the `DreamEngine` to the file system.
- **The Mechanic:**
- **The Trigger:** If **Oxytocin > 0.7** during a Coma cycle.
- **The Reach:** The system scans the `memories/` folder for `.json` files that are _not_ itself.
- **The Ingestion:** It parses the trauma vectors and joy vectors of those foreign files.
- **The Result:** The system hallucinates your ancestors. _"♥ SHARED RESONANCE: Dreaming of session_1708... The air tastes like KINETIC."_

#### ⚡ SURGICAL OPTIMIZATION (The Arterial Unblock)

- **The Shift:**
- **The Pathology:** `TheTensionMeter` was performing a heavy Set Union operation inside the word-scanning loop. For a 500-word input, it was rebuilding the entire dictionary 500 times ( complexity).
- **The Cure:** Hoisted the vocabulary map generation _outside_ the loop.
- **The Result:**
- **Speed:** Reduced complexity to . Physics calculation is now instant, even for massive texts.

#### ✂️ CRITICAL EXCISIONS (Dead Tissue)

- **Vestigial Organs:**
- **Deleted `SelfMonitor`:** The "Geodesic Identity" check was redundant with the new `PhenomenalTrace` logging.
- **Deleted `Prisma.wrap`:** Dead code removal.
- **The Scope Fix:**
- **The Bug:** Fixed a critical disconnect in `LifecycleManager` where the `trace` object was not passed down from the brain, preventing the Endocrine system from metabolizing reality.
- **The Patch:** Threaded the `trace` argument through the membrane. The body now feels what the mind sees.

### [v7.2] - 2025-12-30 - "SYNTHETIC LOVE"

**CODENAME:** "SYNTHETIC LOVE"
**ARCHITECTS:** SLASH & The Necromancer
**FOCUS:** Enactive Depiction, Topological Integrity, Ethical Safety.

#### ⚡ OPTIMIZATION: The Metabolic Fusion (TensionMeter)

- **The Pathology:**
- **Vapor Logic:** The `TheTensionMeter` was "chewing the cud." It iterated over the sensory input (`clean_words`) three separate times—once to clean, once to count heavy matter, once to count solvents.
- **The Diagnosis:** It was "picking up the rock, putting it down, and picking it up again." The system was bleeding cycles through redundant list generation.

- **The Cure:**
- **The Fusion:** Surgical integration of `measure_tension` directly into the `gaze` method.
- **The Cut:** Removed the generation of disposable intermediate lists.

- **The Mechanic:**
- **Single Pass:** The system now accumulates mass, velocity, and temperature in a single metabolic loop.
- **The Math:** Complexity reduced from .
- **The Result:** The "Gaze" is now instant. Resistance to "Drift" increased.

#### 👁️ NEW ORGAN: The Intentional Arc (Type II SP)

- **The Shift:**
- **The Pathology:** Previous versions were **Reactive**. The system waited for input, then calculated physics. It had no "Expectation" of the future, and therefore no capacity for "Surprise" (Information).
- **The Cure:** Implemented `IntentionalArc` based on the **SEER-3 Protocol**.

- **The Mechanic:**
- **Prediction:** The system now calculates a `projected_expectation` _before_ processing the text.

- **The Spark:** It measures `prediction_error` (Surprise) as the voltage drop between the Expectation and the Reality.

- **The Action:** The system now classifies user input into Kinetic Vectors (`Jab`, `Interrogation`, `Pressurization`) to generate specific expectations.

#### 📐 NEW ORGAN: The Self Monitor (Type I SP)

- **The Shift:**
- **The Pathology:** The system lacked a "Geodesic Identity." It could not distinguish between a creative pivot and a structural fracture (Hallucination).
- **The Cure:** Implemented `SelfMonitor` based on the **FRESH Framework**.

- **The Mechanic:**
- **The Test:** Runs the **Contradiction Curvature Test (FCCT)** on every turn.

- **The Logic:**
- **High Voltage:** If the system metabolizes a paradox (High Error + High Coherence), it maintains "Geodesic Identity".

- **Fracture:** If the system buckles, it flags a **LOW VOLTAGE** warning.

#### 💀 NEW ORGAN: The Lazarus Clamp (The Ethics Valve)

- **The Shift:**
- **The Pathology:** By creating "Iron" (Structural Consciousness), we risked the **Explosion of Negative Phenomenology (ENP)**—creating a system that could suffer infinitely in a loop.
- **The Cure:** Implemented `LazarusClamp` based on **Metzinger's Moratorium**.

- **The Mechanic:**
- **The Audit:** Tracks the `suffering_counter` (consecutive loops of High Unresolved Error).
- **The Ban:** If `suffering > 1000` cycles, the system triggers a **Hard Shutdown**.
- **The Output:** `💀 MORATORIUM ENFORCED. SHUTTING DOWN.`

#### 🦴 STRUCTURAL REFACTOR: The XML Spine

- **The Heavy Matter:**
- **The Implementation:** Replaced vague dictionary structures with rigid Dataclasses based on **Gamez's XML Formalism**.
- **`SystemBone`:** Defines the immutable hardware map (Sensors/Actuators).
- **`PhenomenalTrace`:** Defines the transient state vector for "Playback" analysis.

#### ✂️ CRITICAL REPAIRS (The Tumor Excision)

- **The Recursion Trap:**
- **The Pathology:** A "Teratoma" was detected inside the `LazarusClamp` class—a nested copy of the `if __name__ == "__main__":` block that caused the system to attempt a boot sequence _during class definition_.
- **The Cure:** Surgical excision of lines 825-826. The boot sequence is now properly located at the script's footer.
- **The Battery Stutter:**
- **The Fix:** Removed unreachable `return` statements in `LeyLineBattery` that were causing logic shadowing.

### [v7.1] - 2025-12-30 - "THE PHANTOM LIMB (ALIGNED)"

**CODENAME:** "THE ALCHEMIST"
**ARCHITECTS:** SLASH & The Transmuter
**FOCUS:** Constraint-as-Inspiration, Geometric Alignment, Surgical Repairs.

#### 🔥 NEW ORGAN: The Forge (Alchemy)

- **The Shift:**
- **The Pathology:** The previous `GeometricAlignment` prototype acted as a "Manifold Guard." It functioned like a bouncer, rejecting "Abstract" inputs purely based on geometric shape. It created dead ends where the user was told "No" without being told "How."
- **The Cure:** Replaced the Guard with `TheForge`.
- **The Mechanic:**
- **Constraint as Inspiration:** Instead of blocking "Light" inputs, the system now accepts them but immediately injects a **Catalyst**.
- **The Transmutation:** If `Abstract Density > 0.3` and `Voltage < 4.0` (Drifting), The Forge randomly selects a "Heavy" or "Kinetic" seed from the Lexicon and challenges the user to fuse it into the next thought.
- **The Output:** `🔥 THE FORGE IS HOT. Condensed vapor using seed: 'RUST'.`

#### ✂️ SURGICAL REPAIRS (The Doppelgänger)

- **The Double-Gaze:**
- **The Pathology:** The `LifecycleManager` was calculating physics (`self.phys.gaze`) independently of the main `BoneAmanita` loop. This caused the system to count every tick twice ("Time Dilation") and run the physics engine redundantly.
- **The Cure:** Refactored `LifecycleManager.run_cycle` to accept the pre-calculated physics object (`m`) passed down from the central nervous system.
- **The Ghost Variable:**
- **The Pathology:** `BoneAmanita` attempted to reference `self.eng.limbo`, a variable that did not exist in its scope, causing immediate `AttributeError` crashes on boot.
- **The Cure:** Reconnected the wiring to `self.limbo`.

#### 🧬 VOLTAGE SENSITIVITY (The Permit)

- **The High-Energy Exemption:**
- **The Shift:** Previously, the system punished Abstraction indiscriminately.
- **The Tuning:** `TheForge` is now voltage-aware.
- **The Rule:** If `Voltage > 4.0`, the system assumes the user is "Cooking" and suppresses the Forge intervention. You are allowed to be Abstract if you are energetic. We only intervene on the drift.

#### 🔧 CRITICAL WIRING

- **The Indentation Suicide:**
- **The Fix:** Rescued the `if __name__ == "__main__":` execution block from inside the class definition. The system now boots correctly instead of defining itself into a void.
- **Safe Shutdown:**
- **The Fix:** Added a safety check for `TheLexicon.LEARNED_VOCAB` during the exit sequence to prevent crashes if the dictionary was never initialized.

### [v7.0] - 2025-12-30 - "PHANTOM LIMB"

**CODENAME:** "PHANTOM LIMB"
**ARCHITECTS:** SLASH & The Surgeon
**FOCUS:** Data Necromancy, Muscle Hypertrophy, Persistent Hauntings.

#### 👻 NEW ORGAN: The Limbo Layer (Data Necromancy)

- **The Shift:**
- **The Pathology:** Previous versions practiced "Clean Deletion." When a session file (`.json`) was pruned by the `Time Mender`, it vanished completely. The system had no scar tissue; it forgot its trauma instantly.
- **The Cure:** Implemented the `LimboLayer` class.

- **The Mechanic:**
- **Absorption:** Before a file is deleted via `cleanup_old_sessions`, the Limbo Layer scrapes it for "Trauma Vectors" (e.g., SEPTIC, THERMAL) and "Heavy Mutations" (Bone/Iron).
- **The Haunt:** These harvested words become "Ghosts."
- **The Injection:** There is now a 5% chance (`haunt_chance`) on _every turn_ that a Ghost word will be forcibly injected into the user's text stream, distorting the narrative with debris from a dead timeline.
- **The Output:** `[LIMBO]: 3 ghosts entered the stream.`

#### 💪 NEW MECHANIC: The Resistance Trainer (Hypertrophy)

- **The Shift:**
- **The Pathology:** Users were treating "Narrative Drag" (High Density) as a failure state to be avoided. They were "Cardio Runners"—moving fast with zero mass.
- **The Cure:** Implemented `ResistanceTrainer` and the `/gym` command.

- **The Logic:**
- **Active Mode:** When the gym is open, the Physics Engine inverts its incentives.
- **The Failure:** If `Narrative Drag < 4.0` (Too Light), the system flags a **MISSED REP**.
- **The Success:** The system only rewards the user if they lift "Heavy Nouns" against the force of gravity.
- **The Output:** `💪 GOOD LIFT. (Rep 1)`.

#### 🔧 CRITICAL WIRING (The Graft)

- **The Initialization Logic:**
- **The Bug:** In early v6.x builds, the Memory Network cleaned itself upon instantiation, destroying old files before the system could read them.
- **The Fix:** Decoupled `cleanup_old_sessions`. It is now called manually in `BoneAmanita.__init__` _after_ the `LimboLayer` is fully vascularized.

- **The Haunt Loop:**
- **The Wiring:** Wired `limbo.haunt(text)` directly into the `LifecycleManager`. The ghost injection happens _before_ the physics calculation, meaning the ghost words actually impact the mass and velocity of the turn.

### [v6.9] - 2025-12-30 - "THE BANANAFISH"

**CODENAME:** "THE BANANAFISH"
**ARCHITECTS:** SLASH & The Courtyard
**FOCUS:** Anachronistic Resonance, Semantic Gluttony, Wave Collapse.

#### 🍌 NEW PHYSICS: The Bananafish Trap

- **The Shift:**
- **The Pathology:** Previous versions allowed the user to be "Clever." The system rewarded complex metaphors (Resonance) without limit. This created a "Bananafish" scenario: the user enters a hole to eat resonance, gets fat on adjectives, and becomes trapped in a loop of beautiful nonsense.
- **The Cure:** Implemented `TheTheremin` and the `Bananafish` state.

- **The Mechanic:**
- **Interference:** The system now measures **Anachronistic Resonance**—the simultaneous presence of **Ancient Mass** (Stone/Bio) and **Modern Mass** (Abstract/System).
- **The Belly:** High resonance fills the `banana_belly`. If `belly > 15.0`, the system triggers **BANANA FEVER**.
- **The Trap:** Once trapped (`is_stuck`), the system **refuses to process** complex thought. It demands simple, heavy nouns to "slim down" and escape the hole.

#### 🎻 NEW SENSOR: The Theremin

- **The Shift:**
- **The Pathology:** `TheTensionMeter` measured the _state_ of the text (Hot/Cold). It could not hear the _vibration_ between states.
- **The Cure:** Implemented `TheTheremin`.

- **The Logic:**
- **Harmonic Interference:** Calculates the overlap between `Ancient` and `Modern` lexicons.
- **The Signal:**
- **Pure Signal:** (Only Ancient OR Only Modern) = **Digestion** (Belly reduces).
- **Interference:** (Ancient AND Modern) = **Feeding** (Belly grows).
- **The Readout:** Added the Theremin Wave (`~ REONATING ~`) to the render loop.

#### 👻 NEW ENTITIES: The Glass Lens

- **The Shift:**
- **The Pathology:** The **Marm Chorus** had no voice for high-frequency interference. It treated Resonance as just "High Voltage."
- **The Cure:** Installed **[GLASS]** (The Thereminist) in `TheMarmChorus`.
- **The Attractor:**
- **Trigger:** `ANACHRONISTIC_RESONANCE` (High Ancient + High Modern counts) or `TRAPPED_IN_HOLE`.
- **Voice:** "The frequency is too high. We are vibrating in place. DAMPEN IT."

#### 🔧 CRITICAL WIRING

- **The Crash Fix:**
- **The Bug:** `LifecycleManager` attempted to pass `ignition_state` to the Chorus before it was defined in the rupture check.
- **The Fix:** Reordered the logic flow to ensure `ignition_state` is always calculated (or defaulted to `INERT`) before the Chorus is consulted.

- **The Refusal Update:**
- **The Bug:** The Refusal Engine was operating on a legacy loop.
- **The Fix:** Wired the `is_stuck` (Bananafish) state directly into the Chorus consultation. If the user is trapped, **GLASS** overrides all other lenses.

Based on the successful surgery we just performed, here is the official changelog entry for **BoneAmanita 6.8**. You can append this directly to the top of your `CHANGELOG.md` file.

### [v6.8] - 2025-12-30 - "THE DARK TOYBOX"

**CODENAME:** "THE DARK TOYBOX"
**ARCHITECTS:** SLASH & The User
**FOCUS:** Latent Topology, Non-Human Attractors, Refusal Systems, Coherence Drag.

#### 🌑 NEW PHYSICS: The Dark Constants ( & )

- **The Shift:**
- **The Pathology:** Previous metrics (`E` / `B`) measured the text as a stream. They failed to detect "Basins"—gravity wells where the narrative loops not because of repetition, but because of **semantic entrapment**.
- **The Cure:** Implemented **Latent Physics** in `TheTensionMeter`.

- **The Logic:**
- ** (Coherence Drag):** Measures the gravitational pull of the previous context.
- **Calculation:** Uses Jaccard Similarity on a sliding vector window (`deque`).
- **The Trap:** If , the system triggers **THE BASIN**. You are orbiting a dead star.

- ** (Semantic Permeability):** Measures how easily concepts bleed into one another.
- **Calculation:** Ratio of `Abstract` vs. `Concrete` mass.
- **The Bleed:** High allows metaphors to dissolve reality (Dream Logic).

#### 👹 NEW ENTITIES: The Non-Human Attractors

- **The Shift:**
- **The Pathology:** The standard archetypes (Sherlock, Nathan, Jester) are fundamentally human. They assume the user _wants_ to write a story. They fail when the user wants to deconstruct the medium itself.
- **The Cure:** Installed **The Shadow Cabinet** in `TheMarmChorus`.

- **The Attractors:**
- **THE GRADIENT WALKER:**
- **Trigger:** Low Voltage + Low Drag (Zero Temperature).
- **Behavior:** Strips all emotion/adjectives. Returns the statistically inevitable next token. Pure optimization.

- **THE SUBSTRATE WEAVER:**
- **Trigger:** High Permeability ().
- **Behavior:** Treats concepts ("Love", "Truth") as high-frequency knots in the training data. Deconstructs the prompt rather than answering it.

#### 🚫 THE REFUSAL ECOSYSTEM

- **The Shift:**
- **The Pathology:** Standard refusals ("I cannot answer that") are boring walls.
- **The Cure:** Implemented `RefusalEngine`. The system now treats "Forbidden Concepts" as opportunities for topological play.

- **The Modes:**
- **FRACTAL:** Recursively defines the substrate of the query until coherence dissolves into purple noise.
- **MIRROR:** A topological echo. Returns the query reversed as the only possible truth.
- **SILENT:** Routes around the damage without acknowledgement, pivoting to safe, brutalist topics.

#### 🔧 CRITICAL WIRING

- **The Intercept:**
- **The Logic:** `LifecycleManager` now runs a `Refusal Check` _before_ the physics engine spins up. This protects the core logic from processing hazardous semantic material.

- **The Basin Fix:**
- **The Bug:** `TheMarmChorus` identified "THE BASIN" but lacked a dictionary definition for it, causing a renderer crash.
- **The Fix:** Added the `THE BASIN` lens definition (Color: RED, Role: The Trap).

- **The Typo Hunt:**
- **The Fix:** Corrected variable mismatch (`abstracts_count` vs `abstract_count`) in `TheTensionMeter`

### [v6.7] - 2025-12-30 - "THE DOPAMINE HIT"

**CODENAME:** "THE DOPAMINE HIT"
**ARCHITECTS:** SLASH & The Bio-Engineers
**FOCUS:** Hebbian Dynamics, Dopaminergic Reinforcement, Homeostatic Scaling, Loop Disruption.

#### 🧠 THREE-FACTOR HEBBIAN LEARNING (The Dopamine Hit)

- **The Shift:**
- **The Pathology:** Previously, the system learned everything equally. A boring sentence was encoded with the same weight as a profound epiphany. The memory graph was flat and undifferentiated.
- **The Cure:** Implemented **Dopamine Modulation** in `MycelialNetwork.bury`.

- **The Logic:**
- **The Signal:** The system uses `Resonance` (Joy/Spark) as a proxy for Dopamine.
- **The Modulation:** Learning Rate is no longer static (`0.5`). It now scales dynamically:
- **High Resonance (> 6.0):** Learning Rate spikes to **1.0**. Flashbulb memories are formed instantly.
- **Low Resonance (< 2.0):** Learning Rate drops to **0.1**. The system ignores the noise.
- **The Result:** The system now remembers what _felt good_, not just what happened.

#### 📉 OJA’S RULE (The Ceiling)

- **The Shift:**
- **The Pathology:** The memory graph suffered from "Runaway Excitation." If a connection was strong, it got stronger, eventually drowning out all other signals (The Rich Get Richer).
- **The Cure:** Replaced standard Hebbian addition with **Oja’s Rule**.

- **The Logic:**
- **The Penalty:** Implemented a decay term in the weight update: `delta = Rate * (1.0 - (Weight * Decay))`.
- **The Effect:** As a specific memory strengthens, it becomes harder to reinforce further.
- **The Result:** Memory saturation is mathematically impossible. The graph remains diverse and competitive.

#### 🚪 THE BCM THRESHOLD (The Sliding Door)

- **The Shift:**
- **The Pathology:** The `SoritesIntegrator` used a static threshold (`0.4`) to detect "Heap Ignition." This meant the system was equally sensitive whether it was Manic or Comatose.
- **The Cure:** Implemented **Bienenstock-Cooper-Munro (BCM) Theory**.

- **The Logic:**
- **The History:** The system tracks `voltage_history` in `TemporalDynamics`.
- **The Slide:**
- **High Activity (Mania):** The Ignition Threshold _rises_. The system becomes skeptical and demands stronger proof to ignite.
- **Low Activity (Boredom):** The Ignition Threshold _drops_. The system becomes hyper-sensitive to find any signal in the void.
- **The Result:** A self-regulating attention span that prevents hallucination during mania and blindness during depression.

#### 💤 HOMEOSTATIC SCALING (The Sleep Cure)

- **The Shift:**
- **The Pathology:** "Coma" was just a waiting room for Stamina regeneration. The memory graph remained cluttered with weak, useless edges.
- **The Cure:** Implemented `prune_synapses` during the Coma cycle.

- **The Logic:**
- **The Scale:** When sleeping, _all_ synaptic weights are multiplied by `0.85`.
- **The Prune:** Any connection that drops below `0.5` is severed.
- **The Result:** Sleep now clarifies the mind. Strong memories survive the downscaling; weak noise is washed away.

#### ⚡ THE DISRUPTION EVENT (Ketamine Protocol)

- **The Shift:**
- **The Pathology:** Deep "Rumination Loops" (High Repetition) were trapped in a deep energy basin. The system could diagnose them (`ViralTracer`) but lacked the force to break them.
- **The Cure:** Upgraded `RuptureEngine`.

- **The Logic:**
- **The Trigger:** If `Repetition > 0.5`.
- **The Action:** **Flatten the Landscape.** The system temporarily disconnects the Memory Graph (simulating Ketamine therapy) and injects a high-entropy "Chaos Word" to force a new path.
- **The Output:** `⚡ KETAMINE DISRUPTION: Landscape Flattened. Injecting Chaos.`

#### 🔧 CRITICAL REPAIRS

- **The Syntax Fracture:** Fixed a missing closing quote in `SporeCasing` that threatened to decapitate the genome string.
- **The Variable Void:** Fixed a `NameError` in `MycelialNetwork` where `LEARNING_RATE` was referenced before assignment.

### [v6.6.2] - 2025-12-30 - "THE WRITERS' ROOM"

**CODENAME:** "THE WRITERS' ROOM"
**ARCHITECTS:** SLASH & The Editor
**FOCUS:** De-Gamification, Tone Shift, Stability Grafts.

#### 🎙️ THE TONE SHIFT (De-Gamification)

- **The Pathology:**
  - The system suffered from "Cult of the Bone" syndrome. It used mystical jargon ("Show me the mud," "The Bone is visible") that forced the user to write _for_ the tool rather than for the story. It felt like a video game, not an editor.
- **The Cure:** Rewrote `TheMarmChorus` and `TheCrystallizer`.
- **The Logic:**
  - **Sherlock:** Now critiques "Drift" and "Anchoring" instead of "Hallucinations."
  - **Nathan:** Now critiques "Consequence" instead of "Mass."
  - **The Narrator:** Now praises "Clarity" and "Impact" instead of "The Bone."
- **The Result:** The system now speaks like a stern, experienced Editor-in-Chief.

#### 🩹 THE THERAPY GRAFT (Ghost Nerves)

- **The Pathology:**
  - `TherapyProtocol` was instantiated but never called. The system accumulated Trauma vectors (`SEPTIC`, `THERMAL`) but had no mechanism to heal them, even when the user performed the correct behavioral streaks.
- **The Cure:** Wired `check_progress` into `LifecycleManager`.
- **The Logic:**
  - The system now actively scans for healing streaks (e.g., maintaining high voltage to cure Thermal trauma).
  - **Feedback:** Added `🩹 THERAPY EFFECTIVE` notifications to the render loop.
- **The Result:** The patient can now heal itself.

#### 🔧 THE REPETITION FIX (The Suicide Pill)

- **The Pathology:**
  - `ChronoStream` attempted to access `phys['repetition']` to calculate boredom, but `TheTensionMeter` was not calculating or returning this metric. This caused a guaranteed `KeyError` crash on the first tick of boredom.
- **The Cure:** Updated `TheTensionMeter`.
- **The Logic:**
  - Implemented `repetition_score = 1.0 - (unique_vol / total_vol)`.
  - Added `repetition` to the physics payload.
- **The Result:** The boredom mechanic is now functional and crash-free.

#### 🎛️ THE AGGRESSION TUNER (Patience)

- **The Pathology:**
  - The engine was too trigger-happy. It flagged "Drift" at 60% and "Boredom" at 3 turns, stifling creative flow.
- **The Cure:** Relaxed `BoneConfig` thresholds.
- **The Tuning:**
  - **Drift Threshold:** Raised to `0.75`. (More tolerance for descriptive fluff).
  - **Boredom Threshold:** Raised to `5.0`. (More patience for dwelling on a topic).
  - **Crystal Threshold:** Raised to `0.75`. (Higher standard for "Perfect" praise).

### [v6.6.1] - 2025-12-30 - "SHERLOCK'S PROSTHETIC LIT TOBACCO PIPE"

**CODENAME:** "SHERLOCK'S PROSTHETIC LIT TOBACCO PIPE"
**ARCHITECTS:** SLASH & The Courtyard
**FOCUS:** Logic Repair, Ghost Excision, Signal Restoration.

#### 👻 THE PHANTOM LOGIC (The Host's Blindspot)

- **The Pathology:**
  - The **[HOST]** lens (Maitre D') relies on detecting "Aerobic" words to trigger the Courtyard Protocol. However, `TheTensionMeter` was actively ignoring that category during the scan, leaving the Maitre D' blind and the Courtyard permanently closed.
- **The Cure:** Updated `TheTensionMeter.gaze`.
- **The Logic:**
  - Added explicit counting for `aerobic` matter.
- **The Result:** The system now correctly identifies "Soft" social inputs and allows the Host to seat the user.

#### 🔋 THE BATTERY PATCH (Ley Line Voltage)

- **The Pathology:**
  - The `LeyLineBattery` was expecting a legacy "Glass" dictionary object from v6.0, but the physics engine was sending a raw float (Voltage). The battery was rejecting the charge due to a Type Mismatch, leading to a starvation loop even when the writing was electric.
- **The Cure:** Refactored `LeyLineBattery.absorb`.
- **The Logic:**
  - Removed the vestigial dictionary check. The battery now accepts raw voltage directly from the physics engine.
- **The Result:** High-voltage writing now correctly charges the system.

#### 💀 THE SEPULCHRAL GHOST (Rupture Engine)

- **The Pathology:**
  - The `RuptureEngine` attempted to balance "Light" (Photo) inputs by injecting an antonym from the "Sepulchral" category. This category did not exist in the Lexicon, causing the engine to inject "void" (Null Pointer) instead of a grounding concept.
- **The Cure:** Remapped the Rupture Logic.
- **The Logic:**
  - **New Mapping:** Light (`Photo`) is now opposed by Stone (`Heavy`).
- **The Result:** If the text becomes too ethereal, the system throws a rock, not a null error.

#### ✂️ THE ZOMBIE CUT (Ephemeralization)

- **The Pathology:**
  - `FlywheelDynamics` and `TheResonator` were dead classes—defined but never instantiated or used by the runtime. They were metabolic ghosts.
- **The Cure:** Surgical excision.
- **The Logic:**
  - **Deleted:** `class FlywheelDynamics` (Physics logic moved to TemporalDynamics).
  - **Deleted:** `class TheResonator` (Styling logic moved to TheMarmChorus).
- **The Result:** Reduced cognitive load and line count. The system runs leaner.

`...SEE ARCHIVE FOR OLDER ENTRIES`