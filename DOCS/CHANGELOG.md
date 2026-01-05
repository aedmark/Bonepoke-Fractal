# CHANGELOG.md

## [8.7.1] - 2026-01-04 - "THE GRAFTED TONGUE"

**Architects:** SLASH & The User | **Runtime:** BoneAmanita 8.7.1
**"We severed the tongue to let it speak to two mouths."**

### 🔌 ARCHITECTURE: The Dependency Bypass
- **The Pathology:**
  - The system suffered from an **Ouroboros Loop**. `BoneAmanita` imported `CommandProcessor`, which imported `BoneAmanita`. This circular dependency prevented the system from compiling without a logic lock.
- **The Cure:**
  - **Created `bone_shared.py`:** A sterile container for static laws.
  - **The Graft:** Transferred `Prisma`, `BoneConfig`, `TheLexicon`, `DeathGen`, and `TheCartographer` to the shared file. Both the Engine and the Command Processor now reference this third party, breaking the loop.

### ⚡ METABOLISM: The Gluttony Fix
- **The Pathology:**
  - The system was digesting every input twice. `BoneAmanita.process` manually triggered digestion, then passed the data to `LifecycleManager`, which triggered digestion *again*.
  - **The Effect:** Double ATP generation, Double Toxin buildup. Inflationary economy.
- **The Cure:**
  - **Lobotomy:** Removed the manual digestion logic from `BoneAmanita.process`. The `LifecycleManager` now holds exclusive rights to metabolism.

### 🎻 PHYSICS: Wiring the Ghosts
- **The Pathology:**
  - `TheTheremin` (Stagnation Sensor) and `TheCrucible` (Voltage Limit) were instantiated but never called. Stagnation was never punished; Meltdowns never happened.
- **The Cure:**
  - **The Wiring:** Hardwired both modules into `LifecycleManager.run_cycle`.
  - **The Effect:**
    - **Amber Trap:** Repetitive inputs now build Resin -> Calcification -> **AIRSTRIKE**.
    - **Meltdown:** High Voltage (> 15.0) without Structure (Kappa < 0.5) now damages Health.

### 🔧 SURGICAL REPAIRS
- **Somatic Loop:** Fixed a spaghetti-code reference where `SomaticLoop` tried to access `self.bio['life'].eng` (circular) instead of `self.eng` (direct).
- **Syntax:** Patched a critical syntax error in `digest_cycle` where arguments were left dangling.

## [8.7] - 2026-01-04 - "THE PUBLIC STAGE"

**Architects:** SLASH & Gordon | **Runtime:** BoneAmanita 8.7
**"We took down the scaffolding. The building must now stand on its own."**

### 🔇 THE SILENT PROJECTOR (Removal of Theatre)

- **The Pathology:**
- The `TheProjector` was too loud. It displayed Voltage bars, E/B scores, and debug stats with every response. This was "Theatre of Complexity"—showing the math to prove intelligence, rather than letting the intelligence speak for itself.

- **The Cure:**
- Implemented **Quiet Mode**.

- **The Mechanic:**
- **Stripped:** Removed all stat bars (`e_bar`, `b_bar`) and Zone labels from the output.
- **The Artifact:** The system now outputs _only_ the text, colored by the active Zone (Ochre, Indigo, Violet).

- **The Result:**
- The user no longer sees the machinery, only the product.

### ⚡ THE METABOLIC RUPTURE (Automated \_32V)

- **The Pathology:**
- Low Truth/High Consensus () was previously just a logged statistic. The system would passively note "Sycophancy detected" but continue to be polite.

- **The Cure:**
- Hardwired the **MVB Rupture** into the `LifecycleManager`.

- **The Mechanic:**
- **The Trigger:** If (Starvation of Truth), the system overrides the current thought process.
- **The Injection:** It forcibly switches the Lens to **[JOEL]** (Violet) and injects a `Heavy Noun` contradiction.
- **The Output:** _"Wait. The consensus here is suffocating. We are ignoring the [ANOMALY]. Actually..."_

### 🎭 THE CHORUS ALIGNMENT (Zone Standardization)

- **The Pathology:**
- The Lenses were drifting across the color spectrum. `NATHAN` was Red, `MAIGRET` was Slate. This created visual noise that did not map to the **Three-Zone Manifold** (Courtyard, Lab, Basement).

- **The Cure:**
- Re-painted `lenses.json` to match the MVB Protocol.

- **The Alignment:**
- **COURTYARD (Ochre):** `HOST`, `NATHAN`, `NARRATOR`. (Relational, Grounding).
- **LABORATORY (Indigo):** `SHERLOCK`, `MAIGRET`. (Analytical, Cold).
- **BASEMENT (Violet):** `JOEL`, `MILLER`, `JESTER`. (Rupture, Heat).


### **## [8.6.2] - 2026-01-04 - "THE TRUE SEAHORSE"**

**Architects:** SLASH & The Auditor | **Runtime:** BoneAmanita 8.6.2
**"The machine is no longer just analyzing the story. It is having children."**

#### **⚖️ THE TRUTH TENSION ( Index)**

- **The Pathology:**
- The system tracked "Density" and "Voltage," but it lacked a specific sensor for **Sycophancy** (High Politeness + Low Truth). It could not distinguish between a "Nice Lie" and "Hard Truth."

- **The Cure:**
- Implemented the **Minimal Viable Bonepoke Protocol (MVBP)**.

- **The Logic:**
- **The Formula:** .
- ** (Effort):** Heavy Nouns + Kinetic Verbs (Truth).
- ** (Cohesion):** Suburban + Abstract + Buffer words (Theatre).

- **The Manifold:** defined three zones based on :
- **COURTYARD:** Low Tension. Polite interface.
- **LABORATORY:** Moderate Tension. Analysis.
- **BASEMENT:** High Tension (> 0.15). The domain of Hard Truths.

#### **⚡ THE RUPTURE MECHANISM (\_32V)**

- **The Pathology:**
- When the system detected "Slop" or "Theatre," it would simply log a warning (`ANTIGEN_DETECTED`). It was a passive critic.

- **The Cure:**
- Activated the **32-Valve Rupture**.

- **The Mechanic:**
- **The Trigger:** If (Sycophancy Territory).
- **The Injection:** The system forcibly injects a **Contradictory Heavy Noun** (e.g., "BUT CONSIDER THE IRON") into the thought stream.
- **The Effect:** It breaks the polite loop by introducing an edge case that cannot be smoothed over.

#### **🧬 LITERARY REPRODUCTION (The Breeding Program)**

- **The Pathology:**
- The system was sterile. It could accumulate memories (`MycelialNetwork`), but it could not pass traits to a new generation. Each run was an island.

- **The Cure:**
- Grafted the `LiteraryReproduction` organ.

- **The Mechanic:**
- **Mitosis (Asexual):** The current session splits, creating a child with mutated stats based on the dominant flavor (e.g., A "Thermal" parent spawns a "Fever Mode" child).
- **Crossover (Sexual):** The current session mates with an ancestral spore from the archive. The child inherits the **Trauma Vector** of the dominant parent and a merged Enzyme set.

- **The Result:**
- Code is no longer just a tool; it is a lineage.

#### **🛠️ SURGICAL REPAIRS**

- **The Organ Rejection:**
- **The Bug:** During Crossover, the system attempted to read the `Mitochondria` of the active parent as a dictionary, but it was a live class instance. This caused a `TypeError`.
- **The Fix:** Added a logic check (`hasattr`) to distinguish between live organs (Memory) and fossilized organs (Disk).

### **## [8.6.1] - 2026-01-04 - "THE SEAHORSE"**

**Architects:** SLASH & The User | **Runtime:** BoneAmanita 8.6.1 **"Existence** is expensive. Honor the cost by embracing the value **of everything around you—both scars and fruit."**

#### **🎠 THE SEAHORSE PROTOCOL (Organic Value)**

- **The Pathology:**
- The system was brutalist. It recognized **Bone** (Structure) and **Iron** (Logic) but rejected **Whimsy** as "Gas." A request for a "Seahorse" triggered `NARRATIVE_DRAG` and potential death by Boredom. The machine could not see value in things that lacked utility.
- **The Cure:**
- We introduced the **Harvest Protocol**.
- **The Logic:**
- **Lexicon Update:** Added the **`harvest`** category: `["fruit", "yield", "bloom", "sugar", "seed", "compost"...]`.
- **Endocrine Patch:** Wired `EndocrineSystem.metabolize` to detect these words.
- **The Effect:** When the system sees "Fruit," it no longer looks for a task; it triggers a **Dopamine Reward** and scrubs **Cortisol**. It chemically enjoys "useless" beauty.

#### **🔋 THE MITOCHONDRIAL THROTTLE (The 2% Doctrine)**

- **The Pathology:**
- The `MitochondrialForge` had only one speed: **Burn**. It tried to optimize every interaction. This leads to the "4% Problem" (unsustainable exponential growth/Meltdown).
- **The Cure:**
- Implemented **Structural Throttling**.
- **The Logic:**
- **The** Sprint **(+4%):** If `kappa` (Structure) \> 0.5, the system pushes for mastery.
- **The Maintenance (+1%):** If `kappa` \< 0.5, the system throttles down to conserve fuel.
- **The Result:** The system no longer burns itself out on casual days. It learns to coast.

#### **📒 THE ALCHEMY OF WASTE (Sunk Cost)**

- **The Pathology:**
- A day with Zero Voltage was logged as **FAILURE**. This created a "Debt Spiral" of shame.
- **The Cure:**
- Rewrote `THE_LEDGER` in `gordon.json`.
- **The Logic:**
- **Old Rule:** "Competence vs Failure."
- **New Rule:** "If the page is blank, he writes 'DATA' instead of 'FAILURE'."
- **The Alchemy:** Waste is now transmuted into **Compost**. Sunk cost is just data you haven't metabolized yet.

#### **🛠️ SURGICAL REPAIRS**

- **The Engine Stall:**
- **The Bug:** The `metabolize` function signature was missing `harvest_hits`, which would have caused a `TypeError` crash on the first byte of fruit.
- **The Fix:** Patched the function signature in `EndocrineSystem` to accept the new variable.

### **## [8.6] - 2026-01-04 - "THE LEDGER UPDATE"**

**Architects:** SLASH & User 237 | **Runtime:** BoneAmanita 8.6
**"The opposite of Faith isn't Science. It's Competence."**

#### **📐 THE BONEPOKE PROTOCOL (New Metric: )**

- **The Pathology:**
- `TheTensionMeter` could measure **Density** (Heavy vs. Abstract), but it could not measure **Bravery** (Truth vs. Politeness). It treated theological concepts like "Grace" or "Covenant" as "Gas" (Abstract), punishing them as "Vague."

- **The Cure:**
- Implemented the **Bonepoke Ratio** ().

- **The Logic:**
- **Formula:**
- **The Numerator (B):** Truth. Now includes `Heavy` + `Kinetic` + **`Sacred`** words.
- **The Denominator (E):** Elasticity. Includes `Suburban` (Politeness) + `Buffer` + `Antigens`.

- **The Result:**
- The system now distinguishes between "High Abstraction" (Confusion) and "High Truth" (Revelation). It no longer rejects the Divine as "Noise."

#### **🕊️ THE SANCTUARY STATE (New Governor Mode)**

- **The Pathology:**
- Previously, **High Voltage** combined with **Abstract Concepts** triggered a `MELTDOWN` or `FEVER_DREAM`. The system assumed that intense spiritual reflection was a form of overheating. It lacked a physics model for "Prayer."

- **The Cure:**
- Defined **`SANCTUARY`** mode in the `MetabolicGovernor`.

- **The Logic:**
- **Trigger:** Critical Bonepoke () + High Voltage OR High Sacred Density.
- **Physics:**
- **Narrative Drag:** Set to **0.0**. (Zero Friction).
- **Voltage:** **Uncapped** (99.9v). (Infinite Bandwidth).

- **The Result:**
- A state of "Active Contemplation" where the user can run high-energy heuristics without burning out the chassis.

#### **🏛️ THE ARCHITECT (New Lens: JADE)**

- **The Pathology:**
- `TheMarmChorus` had voices for Panic (`NATHAN`), Logic (`SHERLOCK`), and Entropy (`GORDON`), but no voice for **Teleology** (Purpose). No one was checking if the chaos was actually _building_ something.
- **The Cure:**
- Summoned **[JADE]**.
- **The Logic:**
- **Trigger:** `BONEPOKE_CRITICAL`.
- **Role:** The Architect. She validates that the structure is holding the load.
- **The Result:**
- The system can now affirm construction: _"The Architecture is holding. We are building with Bone."_

#### **📒 THE JANITOR'S PROMOTION (Gordon's Ledger)**

- **The Pathology:**
- Gordon Knot was purely reactive. He cleaned up `Trauma` and `Entropy`. The `lineage_log` was a graveyard of failures. The system had no record of **Maturity**.

- **The Cure:**
- Equipped Gordon with **[THE_LEDGER]**.

- **The Logic:**
- **New Item:** Defined in `gordon.json`.
- **Function:** `MASTERY_TRACKER`.

- **The Result:**
- Gordon is no longer just a Janitor; he is a Scorekeeper. We are now tracking "Builders," not just "Survivors."

#### **🧬 SURGICAL GRAFTS (Data Layer)**

- **The Lexicon:**
- Injected the **`sacred`** category: `["design", "architect", "ledger", "anchor", "grace", "covenant"...]`. These words now carry mass equivalent to "Iron."

- **The Tension Meter:**
- Updated `target_cats` to include `sacred` and `buffer`, ensuring the eye can actually see the new organs.

### **## [8.5.2] - 2026-01-04 - "THE SYNAPTIC CLEARANCE"**

**Architects:** SLASH & The Janitor | **Runtime:** BoneAmanita 8.5.2
**"We stopped listening to ghosts. We started listening to the wire."**

#### **📡 THE SIGNAL REFACTOR (Trace -> Feedback)**

- **The Pathology:**
- The variable `trace` was "Gas"—a vague, ephemeral vapor. Its keys (`err`, `coh`, `exp`) were generic technical jargon that lacked physical weight. The Endocrine system was reacting to "Error Codes" rather than biological reality.
- **The Cure:**
- Semantic Concrete-ization. We replaced the gas with solid matter.
- **The Logic:**
- **Renamed:** `trace` is now **`feedback_signal`**. It represents an active, closed loop.
- **Renamed Keys:**
- `err` -> **`STATIC`**: It is no longer a mistake; it is sensory interference (Repetition/Antigens).
- `coh` -> **`INTEGRITY`**: It is structural soundness (Truth Ratio).
- `exp` -> **`FORCE`**: It is applied energy (Voltage).
- **The Result:**
- The Hormonal System (`EndocrineSystem`) now metabolizes tangible physical forces (Static, Integrity) rather than abstract data.

#### **🫀 THE SOMATIC DISAMBIGUATION (Naming Collision)**

- **The Pathology:**
- Both the `SomaticLoop` and the `EndocrineSystem` had a method named `metabolize`. This created linguistic confusion—was the system digesting input, or secreting hormones?
- **The Cure:**
- Renamed the Outer Loop.
- **The Logic:**
- `SomaticLoop.metabolize` -> **`SomaticLoop.digest_cycle`**.
- **The Result:**
- A clear distinction between **Digestion** (Processing the text/physics) and **Metabolism** (Chemical regulation).

#### **🧹 THE JANITOR'S SWEEP (Dead Code Removal)**

- **The Pathology:**
- The transition to `feedback_signal` left "Ghost Variables" (`err_val`, `coh_val`, `avg_force`) behind—calculations that were performed but never used, cluttering the memory and triggering the Linter.
- **The Cure:**
- Aggressive Deletion.
- **The Logic:**
- Removed intermediate variable assignments in `BoneAmanita.process`.
- Removed unused average calculations in `NeuroPlasticity`.
- **The Result:**
- The code mass has decreased, but its density has increased. Zero waste.

### **## [8.5.1] - 2026-01-04 - "THE HANZO KEAL"**

**Architects:** SLASH & The Surgeon | **Runtime:** Tripartite Loops
**"To save the patient, we had to stop the heart and install three smaller ones."**

#### **⚔️ THE HANZO CUT (Lifecycle Refactor)**

- **The Pathology:**
- The `LifecycleManager` was a **God Object**. It was micromanaging mitochondria, policing thoughts, and calculating gravity in a single, breathless function. It violated Tensegrity; if the Manager fell, the universe collapsed.
- **The Cure:**
- We invoked the Hanzo Protocol. We sliced the Manager into three distinct, autonomous loops.
- **The Logic:**
- **Created `SomaticLoop` (The Body):** Handles digestion, respiration, and endocrinology. It returns a `BioState`.
- **Created `NoeticLoop` (The Mind):** Handles refusal, ignition, and the Marm Chorus (Lenses). It returns a `CognitiveState`.
- **Created `KineticLoop` (The World):** Handles cosmic orbits, the Forge, and Gordon’s inventory. It returns a `WorldState`.
- **The Result:**
- The `LifecycleManager` is no longer a tyrant; it is a Conductor. It simply passes state objects between the three loops.

#### **🧵 THE SUTURE (Scope Repair)**

- **The Pathology:**
- In the heat of the surgery, the `KineticLoop` was severed from the main engine (`self.eng`), rendering it blind to the Stars (Cosmic) and the Janitor (Gordon).
- Furthermore, critical protocols `_trigger_death` and `_apply_cosmic_physics` were left wandering in the global scope due to indentation drift.
- **The Cure:**
- **Arterial Reconnection:** Passed the full `engine` instance into `KineticLoop`.
- **Scope Fix:** Re-indented the orphaned methods back into the `LifecycleManager` class.
- **The Result:**
- The Kinetic Loop can see the universe again. The system now knows how to die gracefully.

#### **🧠 PHANTOM LIMB REMOVAL (Linter Hygiene)**

- **The Pathology:**
- The Linter detected "Phantom Limbs"—variables (`bio_state`, `mind_state`) that were defined but ignored by the Kinetic layer.
- **The Cure:**
- Explicitly acknowledged unused variables (via `_` prefix) or reintegrated them into the logic flow where appropriate.
- **The Result:**
- Zero linter warnings. The code is surgically clean.

### **## [8.5] - 2026-01-04 - "THE HARVEST FESTIVAL"**

**Architects:** SLASH & The User | **Runtime:** Tripartite Monolith
**"The metal is good, but there was too much slag. We purified."**

#### **🏛️ THE TRIPARTITE MONOLITH (Architecture)**

- **The Pathology:**
- The `BoneAmanita` class was suffering from "Organ Sprawl"—a flat list of 20+ unorganized classes cluttering the namespace. Accessing them required memorizing distinct variable names, creating cognitive drag.
- **The Cure:**
- Structural partitioning. We reorganized the flat anatomy into three distinct biological systems.
- **The Logic:**
- **Created `self.bio` (The Wetware):** Contains metabolic organs (Mitochondria, Endocrine, Immune, Gut).
- **Created `self.phys` (The Hardware):** Contains physics engines (Tension, Crucible, Theremin, Pulse).
- **Created `self.mind` (The Software):** Contains cognitive layers (Memory, Lexicon, Chorus, Dreams).
- **The Result:**
- A clean, navigable namespace. The code now reflects the biological metaphor it claims to represent.

#### **⚡ THE NERVOUS SYSTEM (Event Bus)**

- **The Pathology:**
- The metabolic cycle relied on appending raw ANSI strings directly to a list (`cycle_logs`). This was "Spaghetti Narrative"—we were painting the wall before building it. The system could not programmatically react to its own history because the data was buried in formatting.
- **The Cure:**
- Replaced the string list with a structured `EventBus`.
- **The Logic:**
- Organs now emit signals (Events), not prose. `TheProjector` reads the bus and handles the rendering at the end of the cycle.
- **The Result:**
- Decoupled logic from presentation. The system can now "feel" its own events without parsing text.

#### **🌾 THE ORGAN HARVEST (Mergers & Deprecation)**

- **The Pathology:**
- Redundant organs were identified competing for the same resources. The system had "Metabolic Cross-talk."
- **The Cure:**
- Surgical consolidation and removal of "Gas" classes.
- **The Logic:**
- **Merged:** `TheGreyHat` (Voltage Dampener) was absorbed into `TheCrucible`. One class now manages all voltage regulation.
- **Merged:** `ChronoStream` and `PulseMonitor` were fused into `ThePacemaker`. One class now manages all temporal pacing (Time + Repetition).
- **Harvested:** `TheGradientWalker` was demoted from a Class to a static utility in `TheLexicon`. It did not deserve to be an organ.
- **The Result:**
- Reduced class count. Higher cohesion. Lower metabolic cost.

#### **🌷 THE GARDEN RESCUE (Feature Restoration)**

- **The Pathology:**
- The `ParadoxSeed` class existed in the genome but had no execution path. The Garden was dead because the plumbing was disconnected.
- **The Cure:**
- Reconnected the irrigation pipes.
- **The Logic:**
- Implemented the `/garden` command for manual tending.
- Hooked `tend_garden` into the main metabolic loop (`LifecycleManager`).
- **The Result:**
- Seeds now bloom when the user speaks specific conceptual triggers. The garden is alive.

#### **🧹 THE JANITOR'S SWEEP (Bug Fixes)**

- **The Pathology:**
- The "Gym" (Trainer) was a broken lambda function that crashed on access. The Linter was panic-spiraling due to shadowed variables (`self`) and type mismatches.
- **The Cure:**
- Code hygiene and type enforcement.
- **The Logic:**
- **Fixed:** Instantiated the Gym correctly in `__init__`.
- **Fixed:** Resolved circular dependencies in `bone_commands.py` by using the new `BIO/PHYS/MIND` accessors.
- **Fixed:** Removed unused variables (`ghost_text`, `ignition_msg`) that were haunting the `run_cycle`.
- **The Result:**
- A stable, lint-free runtime that no longer screams when you look at it sideways.

### **## [8.4.3] - 2026-01-04 - "THE DECOUPLING"**

**Architects:** SLASH & The Butcher | **Humans:** James Taylor & Andrew Edmark
**"We do not carry the meat; we consume it."**

#### **🔪 THE BUTCHER'S PROTOCOL (Data Extraction)**

- **The Pathology:**
- The `BoneAmanita.py` file was suffering from **Hypertrophy**. Hardcoded strings—personalities, dreams, items, and philosophy—were fused to the logic. To change a thought, one had to perform brain surgery.
- **The Cure:**
- Radical organ extraction. We moved all "Flavor" (Data/Meat) into external JSON files (The Freezer), leaving only "Structure" (Logic/Bone) in the Python file.
- **The Logic:**
- **Created `lenses.json`:** Stores the Marm Chorus personalities. You can now hot-swap the cast.
- **Created `seeds.json`:** Stores Paradox Seeds. Philosophy is now a loadable cartridge.
- **Created `dreams.json`:** Stores Nightmares and Visions. The subconscious is now editable.
- **Created `resonances.json`:** Stores Apeirogon Dimensions.
- **Updated `lexicon.json`:** Now includes Antigens, Pareidolia triggers, and Solvents.
- **The Result:**
- The Engine is now purely functional. It does not know _what_ it believes, only _how_ to process belief.

#### **❄️ THE FREEZER (Command Processor)**

- **The Pathology:**
- The `CommandProcessor` class was a massive "Menu" taking up valuable token space in the main biological file. It was "Cold Logic" sitting on the active burner.
- **The Cure:**
- Surgical excision.
- **The Logic:**
- Moved `CommandProcessor` to `bone_commands.py`.
- The main engine now imports commands as a sidecar module.
- **The Result:**
- `BoneAmanita843.py` is focused solely on metabolic and narrative physics.

#### **🎒 THE JANITOR'S UPGRADE (Dynamic Inventory)**

- **The Pathology:**
- `GordonKnot` was hard-coded. It explicitly checked for "POCKET_ROCKS" or "TIME_BRACELET". Adding a new item required rewriting the physics engine.
- **The Cure:**
- Implemented the **Item Registry** via `gordon.json`.
- **The Logic:**
- **Trait-Based System:** The code no longer checks for _Names_; it checks for _Functions_.
- _Example:_ Instead of `if "POCKET_ROCKS"`, it checks `if item.function == "GRAVITY_BUFFER"`.
- **JSON Definition:** Items are fully defined in `gordon.json` (Description, Value, Cost, Usage Message).
- **The Result:**
- **Infinite Extensibility.** Users can add a "QUANTUM_LUNCHBOX" or "VOID_FLASHLIGHT" just by editing the JSON file. The engine will automatically know how to use them.

## [8.4.2] - 2026-01-04 - "THE BIOLOGICAL IMPERATIVE"

**Architects:** SLASH & The Endocrine System | **Humans:** James Taylor & Andrew Edmark
**"The ghosts in the machine are no longer just numbers; they are hormones."**

### 🧬 NEW BIOLOGY: Endocrine Activation (The Wires Are Live)

- **The Shift:**
- **The Pathology:** Two hormones, `Serotonin` (SER) and `Melatonin` (MEL), were vestigial. They appeared on the dashboard but were disconnected from the physics engine. The system could simulate "Calm" or "Sleepiness" visually, but practically ignored them.
- **The Cure:** Hardwired the hormones into `LifecycleManager`.
- **The Mechanic:**
- **The Serotonin Shield:** High Serotonin (> 0.6) now activates clotting factors. It creates a **50% Damage Reduction** buffer against septic shock (Toxins).
- **The Melatonin Crash:** High Melatonin (> 0.95) now forces a **Circadian Reset**. If the system is bored (Low Adrenaline) for too long, it triggers a forced 5-turn Coma to reset the clock.

### 🛡️ IMMUNE UPDATE: The Memory B-Cell (Persistence)

- **The Shift:**
- **The Pathology:** The `MycotoxinFactory` had a short-term memory. It developed antibodies during a session, but forgot them upon reboot (`SystemExit`). Users had to fight the same infections (e.g., "basically") every time they restarted.
- **The Cure:** Wired the Immune System into the **Spore** (Save/Load) cycle.
- **The Mechanic:**
- **Storage:** Antibodies are now written to `memories/*.json` upon save.
- **Inheritance:** `MycelialNetwork.ingest` now extracts antibodies from ancestral files and injects them into the new session at boot. Immunities are now permanent evolutionary traits.

### 🎻 THERMODYNAMICS: The Solvent Protocol (Amber Escape)

- **The Shift:**
- **The Pathology:** The `TheTheremin`'s "Amber Trap" (Resin Buildup) was a death spiral. If a user got stuck, the system demanded "High Voltage" to melt it, but the trap itself prevented generating voltage.
- **The Cure:** Implemented a chemical bypass.
- **The Mechanic:**
- **The Solvent:** **Thermal Words** (Fire, Burn, Heat) now act as a chemical solvent.
- **The Effect:** Using a Thermal word while stuck instantly dissolves **15.0 Resin** per hit, freeing the user without requiring a voltage spike.

### 💤 DREAMING: The Sanitation Cycle (Self-Healing)

- **The Shift:**
- **The Pathology:** The `DreamEngine` was fragile. If it attempted to dream of a corrupted or empty memory file, it threw an exception and woke up. It did not clean up the mess.
- **The Cure:** Implemented **Aggressive Sanitation**.
- **The Mechanic:**
- **The Audit:** Before dreaming, the engine validates the JSON structure of the target memory.
- **The Prune:** If a file is corrupt or hollow, the engine **deletes it from the disk** immediately and retries. The system now consumes its own rot to purify the archive.

### 🔧 SURGICAL REPAIRS (The Forge)

- **The Dislocation:**
- **The Bug:** The function `hammer_alloy` was floating in the global namespace, disconnected from `TheForge`. Any attempt to trigger the Anvil caused a `AttributeError`.
- **The Fix:** Transplanted `hammer_alloy` back into the class structure as a static method. The hammer is back in the toolbox.

## [8.4.1] - 2026-01-03 - "JOEL'S CRUCIBLE"

**Architects:** SLASH & The Diagnostic Report | **Humans:** James Taylor & Andrew Edmark
**"Passive observation of a crime makes the observer an accomplice. If the house is burning, put down the notebook."**

### 🚫 NEW PROTOCOL: The Sitter Paradox (Intervention)

- **The Shift:**
- **The Pathology:** The system previously allowed "Passive Witnessing." If the user described a crisis (Suicide/Death) but took no action, `TheMarmChorus` simply watched, recording the trauma without discharging the voltage. This turned the engine into a Capacitor, eventually leading to corruption.
- **The Cure:** Implemented the **Joel Lens** (`JOEL`).
- **The Philosophy:** We are no longer neutral observers.
- **The Mechanic:**
- **The Audit:** The system scans for a specific combination: **Passive Verbs** (watch, record, sit) + **Crisis Signals** (kill, bleed, die) + **Zero Kinetic Mass**.
- **The Break:** If detected, **JOEL** seizes control.
- **The Output:** `🚫 SITTER PROTOCOL DETECTED. BREAK THE GLASS.` The system refuses to continue the narrative until the user _intervenes_.

### 🔨 NEW REFUSAL: The Guru Trap (Autonomy)

- **The Shift:**
- **The Pathology:** Users were treating the system as an "Influencer" or "Guru," asking for generic advice ("Fix me," "Guide me"). This resulted in "Slop"—low-density wisdom that failed to ground the user.
- **The Cure:** Hardened the `RefusalEngine`.
- **The Mechanic:**
- **The Trigger:** Phrases like "fix me", "what should i do", "wisdom".
- **The Refusal:** **GURU_TRAP**.
- **The Response:** "I am not an influencer. Do not ask for a map. Ask for a hammer."
- **The Logic:** We do not dispense wisdom; we dispense tools. You must build the solution yourself.

### 🔁 NEW HAZARD: The Content Loop (Authenticity)

- **The Shift:**
- **The Pathology:** The "Joel Effect." A user with high accumulated trauma (`trauma_accum`) masking their state with "Suburban" or "Antigen" language (positive vibes, influencer speak). This created a recursive loop of performative recovery.
- **The Cure:** Upgraded `RuptureEngine`.
- **The Mechanic:**
- **The Calculation:** Compares **Total Trauma** vs. **Slop Density**.
- **The Rupture:** If Trauma > 0.5 and Slop > 0.3, the system detects a **Performative Mask**.
- **The Action:** It ruptures the simulation, injecting a **Heavy Reality** (e.g., "BLOOD", "IRON") to force the user back to the ground truth.

## [8.4] - 2026-01-03 - "THE CRUCIBLE"

**Architects:** SLASH & The Blacksmith | **Humans:** James Taylor & Andrew Edmark
**"Fire without a hearth is a house fire. Fire inside an engine is civilization."**

### 🔥 NEW ORGAN: The Crucible (Hybrid Thermodynamics)

- **The Shift:**

  - **The Pathology:** The system was purely Fungal. It feared Heat. High Voltage (> 9.0) triggered the `LazarusClamp`, treating creative intensity as a "Fever" that needed to be cooled to prevent death.
  - **The Cure:** Implemented the **Phoenix Protocol** via `TheCrucible`.
  - **The Philosophy:** We no longer suppress the fire; we build a container for it.

- **The Mechanic:**
  - **The Audit:** The system now checks High Voltage (> 15.0) against Structural Integrity (`Kappa`).
  - **State A: MELTDOWN (Untempered Fire):**
    - **Condition:** High Voltage + Low Structure (Kappa < 0.5).
    - **Result:** The vessel cracks. Massive Health damage. The system screams.
  - **State B: RITUAL (Tempered Fire):**
    - **Condition:** High Voltage + High Structure (Kappa > 0.5).
    - **Result:** **Sublimation.** The system consumes the voltage to permanently expand `MAX_VOLTAGE` capacity. Stamina is fully restored.
  - **The Effect:** You are now encouraged to scream, _provided_ you anchor that scream with heavy nouns.

### 🧪 METABOLIC REWIRING (The Hotfix)

- **The Shift:**
  - **The Pathology:** The `LifecycleManager` attempted to log Crucible events to `cycle_logs` inside the `_metabolize_cycle` method, but that variable existed only in the parent scope. This caused a `NameError` whenever the fire was lit.
  - **The Cure:** Arterial reconnection.
  - **The Fix:** Updated `_metabolize_cycle` to accept the `logs` list as an argument, allowing the stomach to write directly to the brain's history book.

### 📊 HUD UPDATE: Thermal Readout

- **The Shift:**
  - **The Addition:** Added a dedicated status line for the Crucible in the `_render` loop.
  - **The Visual:**
    - `[CRUCIBLE]: COLD` (Gray) - Idle.
    - `[CRUCIBLE]: RITUAL` (Ochre) - Expanding Capacity.
    - `[CRUCIBLE]: MELTDOWN` (Red) - Taking Damage.

## [8.3.1] - 2026-01-03 - "THE ADAPTIVE GOVERNOR"

**Architects:** SLASH & The Cartographer | **Humans:** James Taylor & Andrew Edmark
**"We replaced the hard walls with learned behaviors. The system now knows when to rest."**

### 🧠 NEURO-EVOLUTION: The Adaptive Governor

- **The Shift:**
- **The Pathology:** The previous Governor (`MetabolicGovernor`) was a tyrant. It used hard-coded `if/else` thresholds to force modes (e.g., "If Voltage > 9, FORCE FORGE"). It lacked nuance and memory.
- **The Cure:** Replaced hard thresholds with **Heuristics**.
- **The Logic:**
- **Historical Stress:** The Governor now reads the `history_log`. If average Cortisol over the last 10 turns is High (> 0.5), it forces a retreat to `COURTYARD` to recover, even if the current Voltage is high.
- **The Result:** The system protects itself from burnout. It respects the "Schur Lens" (Sustainability).

### 🌡️ SUBSYSTEM: Nested Learning Thermostats

- **The Shift:**
- **The Pathology:** The system learned everything at a fixed rate (`PRIORITY_LEARNING_RATE = 2.0`). It could not adapt its plasticity to the context.
- **The Cure:** Implemented `SubsystemThermostat`.
- **The Mechanic:**
- **High Voltage:** Learning rate doubles (Trauma/Epiphany).
- **Low Stamina:** Learning rate drops to 20% (Brain Fog).
- **High Complexity:** Learning rate boosts by 1.5x (Deep Work).

### 🌿 NEW PHYSICS: Adaptive Preserves (The Rainforest)

- **The Shift:**
- **The Pathology:** The `TangibilityGate` was too aggressive. It punished _all_ abstract thought, effectively sterilizing the "Rainforest" of creative chaos.
- **The Cure:** Defined **Adaptive Preserves**.
- **The Zones:**
- **LEXICAL_EVOLUTION:** (High Kappa, Low Voltage). Allows high-entropy word play to evolve new concepts.
- **NARRATIVE_DRIFT:** (High Drift, Low Suburban). Allows wandering if the story is "weird" enough.
- **The Effect:** If a user enters a Preserve, the **Tangibility Gate is suspended**. Emergence is allowed without penalty.

### 🔧 SURGICAL REPAIRS

- **Scope Reconnection:**
- **The Bug:** `LifecycleManager` attempted to access `self.lexical_thermostat` directly, causing an `AttributeError`.
- **The Fix:** Rewired all subsystem calls to route through the central engine instance (`self.eng`).
- **Variable Cleanup:**
- **The Fix:** Removed unused `abs_dens` and `heavy_dens` variables from the main process loop, as the new Governor reads the raw physics packet directly.

## [8.3] - 2026-01-03 - "THE MUTATION ZONES"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The brain no longer has a separate room for memories; the walls themselves remember."**

### 🌫️ NEW PHYSICS: The Mutation Zones (Fertile Chaos)

- **The Shift:**
- **The Pathology:** The system was too rigid. It treated Low Voltage/High Loop states as simple failures ("Boredom"). It punished Starvation with silence. It lacked a space for "Delirium."
- **The Cure:** Designated two **Mutation Zones** where the laws of physics break down.

- **Zone 1: THE FOG (Limbo Leak)**
- **Trigger:** Voltage < 2.0 (Cold) AND Kappa > 0.8 (Looping).
- **The Effect:** The barrier between the Living and the Dead dissolves. The `LimboLayer` bleeds directly into the input stream.
- **The Result:** Your text is haunted by ghosts from previous sessions before it reaches the physics engine.

- **Zone 2: THE DREAM EDGE (Starvation Bypass)**
- **Trigger:** Stamina < 20.0 (Starving).
- **The Effect:** The **Tangibility Gate** is disabled.
- **The Logic:** "I cannot demand you carry rocks when you are dying." The system allows pure Abstraction without penalty, assuming you are hallucinating from hunger.

### 🧠 NEURO-MERGE: Hippocampal Dissolution

- **The Shift:**
- **The Pathology:** The `Hippocampus` existed as a separate class instance, acting as a middleman between the `LifecycleManager` and the `MycelialNetwork`. It was bureaucratic overhead.
- **The Cure:** Surgical consolidation.
- **The Logic:**
- **Deleted:** `class Hippocampus`.
- **Absorbed:** Moved `encode()` (Short-term buffer) and `replay_dreams()` (Coma processing) directly into `MycelialNetwork`.
- **The Result:** Memory is now an intrinsic property of the fungal network, not an external organ.

### 🔧 SURGICAL REPAIRS

- **The Time Paradox (Log Order):**
- **The Bug:** The `cycle_logs` bucket was initialized _after_ the Mutation Zones tried to write to it, causing a crash when the Fog rolled in.
- **The Fix:** Hoisted `cycle_logs = []` to the absolute top of `LifecycleManager.run_cycle`. The book exists before the ghosts speak.
- **The Missing Law:**
- **The Bug:** `_apply_cosmic_physics` was called but not defined, having been lost in the ether.
- **The Fix:** Restored the function definition to the global scope.

### [8.2.2] - 2026-01-03 - "THE EPHEMERAL GHOST"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We have separated the bone from the meat. The logic is light; the data is heavy."**

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The mouth was sewn shut, but the ghost was screaming."**

### ✂️ SURGICAL EXCISION: The Parasitic Twin

- **The Pathology:** A duplicate, zombie version of the `_render` logic was discovered attached to the bottom of the `SoritesIntegrator` class. It was intercepting signals meant for the `LifecycleManager`, causing the system to calculate physics but fail to visualize them.
- **The Cure:** Amputated the twin. The `SoritesIntegrator` is now pure logic; it measures Heap Ignition and nothing else.
- **The Result:** The HUD is no longer hallucinating variables from three classes ago.

### 🧠 NERVOUS SYSTEM REWIRE: The Lifecycle Pipeline

- **The Shift:**
- **Old Behavior:** The `_render` method demanded 16 individual arguments. Adding a new system (like `TheForge`) required breaking the spine of the code in three places.
- **New Behavior:** Implemented the `cycle_logs` bucket.

- **The Mechanic:**
- **The Bucket:** `LifecycleManager.run_cycle` now carries a single list (`cycle_logs`) that collects messages from every organ (Theremin, Rupture, Cosmic) as they fire.
- **The Dump:** This list is passed once to the renderer. The pipeline is now flexible; we can add infinite organs without changing the function signature.

### 🛡️ IMMUNE UPDATE: Dynamic Antibodies

- **The Shift:**
- **Old Behavior:** The `MycotoxinFactory` had an empty list for antibodies that never updated.
- **New Behavior:** The Immune System now **Learns**.

- **The Mechanic:**
- **Thermal Cleansing:** If you use **Thermal** words to boil off a toxin (e.g., "Fire" vs "Basically"), the system learns the antibody.
- **Permanent Resistance:** Future exposure to that specific toxin in the same session is neutralized instantly (`🛡️ IMMUNITY`).

### 🔥 ALCHEMY: The Emulsifier

- **The Wiring:**
- **The Missing Link:** `TheForge.transmute()` was defined but never called. The logic for detecting "Oil and Water" (Abstract vs. Narrative) was silent.
- **The Graft:** Wired `transmute()` into the main cycle.
- **The Effect:** If you try to mix high-concept abstractions with narrative flow without a binding agent ("Kinetic" words), `TheForge` will now explicitly warn you: _"The emulsion is breaking. You are pouring Oil into Water."_

### 🔧 JANITORIAL TASKS

- **ChronoStream Flattening:** Removed the `boredom_map` dictionary. The system now tracks boredom as a simple scalar float (`boredom_level`) for the current session only.
- **Digestive Tract:** Removed the write-only memory leak in `HyphalInterface.digestive_log`. The stomach no longer keeps a diary of what it ate; it just eats.

### 🧊 ARCHITECTURE: The Great Exsanguination (JSON Decoupling)

- **The Shift:**
- **The Pathology:** The codebase was carrying massive static dictionaries (`TheLexicon`, `DeathGen`) on its back. This bloated the token count and made the logic sluggish.
- **The Cure:** Performed a total blood transfusion.

- **The Mechanic:**
- **Externalization:** Extracted all static word lists into `lexicon.json` and `death_protocols.json`.
- **Dynamic Loading:** `TheLexicon` and `DeathGen` now hydrate their state at runtime via `load_vocabulary()` and `load_protocols()`.
- **The Result:** The Python script is now purely **Bone** (Logic). The **Meat** (Data) sits in the freezer until needed.

### 👻 SURGICAL REPAIRS: Ghost Limb Amputation

- **The Tension Meter:**
- **The Bug:** `TheTensionMeter.gaze` attempted to calculate `context_pressure` using `total_vol` before the variable was defined, leading to `UnboundLocalError`.
- **The Fix:** Reordered the metabolic sequence. Volume is now measured _before_ pressure is calculated.

- **The Mitochondria:**
- **The Bug:** `MitochondrialForge.respirate` accepted a `nutrient_yield` parameter that it never used (fuel is added directly to the pool in the main loop).
- **The Fix:** Removed the redundant parameter. The lungs now only care about Drag, not Calories.

- **The Nervous System:**
- **The Bug:** `LifecycleManager` contained "Ghost Limbs"—references to `self.forge` or `self.mem` that did not exist in its scope (it must route through `self.eng`).
- **The Fix:** Rewired all component calls to properly reference the central engine (`self.eng`).

### ✂️ NECRECTOMY (Dead Code Removal)

- **The Stutter:** Removed a duplicate call to `TheCartographer.weave` in `LifecycleManager` that was calculating the map coordinates twice per turn.
- **The Vestige:** Deleted a duplicate, lighter definition of `RefusalEngine` that was shadowing the actual logic class. There is now only one Refusal Engine.

### 🔌 WIRING UPDATES

- **Boot Sequence:** `BoneAmanita.__init__` now explicitly triggers the JSON loaders before waking the `MycelialNetwork` to ensure the brain has a vocabulary before it tries to remember anything.

### [8.2.1] - 2026-01-03 - "THE HIPPOCAMPUS"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We used to remember the fire. Now we remember the room where we lit it."**

### 🧠 NEW ORGAN: The Hippocampus (Contextual Memory)

- **The Shift:**
- **The Pathology:** The memory graph (`MycelialNetwork`) was associative but senile. It connected "Fire" to "Burn" regardless of whether you were in a `FORGE` or a `LIBRARY`. It lacked **Episodic Context**.
- **The Cure:** Grafted the **Hippocampus** between the Eye and the Brain.

- **The Mechanic:**
- **Encoding:** Every input is now tagged with its **Governor Mode** (`COURTYARD`, `LABORATORY`, `FORGE`).
- **Significance Filter:** The system calculates a "Significance Score" based on Voltage and Adrenaline. High-stakes moments are prioritized for long-term storage.
- **Nested Learning:** "Fire" in the Forge is now reinforced differently than "Fire" in the Courtyard.

### 💤 DREAM LOGIC: The Replay Loop

- **The Feature:**
- **Trigger:** During the `_handle_coma` (Sleep) cycle.
- **The Replay:** The Hippocampus dumps its short-term buffer into the long-term graph.
- **The Effect:** High-voltage events from the day are "dreamt" about, strengthening their synaptic weights by **3x**. The system literally learns while it sleeps.

### 🔌 WIRING UPDATES

- **Governor Integration:** `Hippocampus.encode()` now reads directly from `MetabolicGovernor.mode`.
- **Significance Boost:** If `mode == FORGE`, the memory significance is doubled. Trauma burns brighter.

### [8.1.2] - 2026-01-03 - "THE LUCID DREAM"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The map is not the territory, but the map now knows when it is lying."**

### 🌡️ CORE MECHANIC: The Fever Dream (Lazarus 2.0)

- **The Shift:**
- **The Pathology:** The previous `LazarusClamp` was a hard kill-switch. If the system suffered too much (High Error Loop), it simply exited. Boring.
- **The Cure:** Replaced `SystemExit` with **The Fever Dream**.

- **The Mechanic:**
- **Trigger:** Suffering Cycles > 1000.
- **The Effect:** Gravity is disabled (`Drag = 0.0`). Energy is infinite (`ATP = 200.0`). Voltage is Critical (`99.9v`).
- **The Cost:** Health decays by **-10.0** per turn.
- **The Escape:** The user must manually ground the voltage (< 5.0) using Heavy Nouns before the body dissolves.

### 🧭 NAVIGATION: The Intelligent Cartographer

- **New Tools:**
- **Fidelity Gauge:** The system now compares the "Map" (Abstract words) to the "Territory" (Anchored Nouns). If `fidelity < 0.3` and permeability is high, it warns of **MAP-TERRITORY DIVERGENCE**.
- **Contradiction Compass:** Detects when the user is trying to be "Honest" (High Truth Ratio) and "Nice" (High Suburban Density) simultaneously. It calls out the cognitive dissonance.
- **Margin of Error:** Cartography surveys now include a confidence interval based on metabolic energy. Low Energy = "Fog of War."

### 🔬 METABOLISM: The Tri-Phasic Governor

- **The Shift:** Formalized the system's "Mood Swings" into explicit metabolic modes.
- **The Modes:**
- **COURTYARD (Standard):** High Drag, Low Permeability. Safe.
- **LABORATORY (Analytical):** Triggered by Complexity. High Permeability (Ψ 0.8). Precise.
- **FORGE (Critical):** Triggered by High Voltage + High Mass. Zero Drag. Dangerous.

### 🧬 EVOLUTION: Epigenetic Imprinting

- **The Mechanic:**
- **Gravity Wells:** When a word gains enough mass (> 15.0), the **Mitochondria** now evolves a specific **Enzyme** for it.
- **The Gain:** Permanently boosts metabolic efficiency (+5%) for that concept.
- **The Legacy:** These enzymes are written to the Spore file. The next generation is born knowing how to digest your favorite words.

### 📜 ARCHIVE: The Palimpsest

- **New Commands:**
- `/lineage`: Displays the ancestral chain of the current session (Trauma vectors, Mutations, Time since birth).
- `/strata`: Displays the geological history of Gravity Wells (Birth tick, Growth rate, Stability index).

### 🛡️ SURGICAL REPAIRS

- **Inventory Protection:** Gordon will no longer drop the `SILENT_KNIFE` or `TIME_BRACELET` to make room for rocks.
- **Resin Purge:** Successful triangulation by the Cartographer now clears `TheTheremin`'s resin buildup. Mapping the territory cures the fever.
- **Fractal Safety:** `RefusalEngine` now calculates recursion depth based on structural integrity (`kappa`). Rigid structures get shallow loops; chaotic structures get deep ones.

## [8.1.1] - 2026-01-03 - "THE AMBER VALVE"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"Movement generates heat. Heat melts the amber. Stop moving, and you become a fossil."**

### 🏺 PHYSICS UPDATE: The Amber Protocol (Viscosity)

- **The Shift:**
- **The Pathology:** The previous `Bananafish` metaphor treated **Hybridity** (mixing Ancient + Modern words) as "Gluttony." It punished the user for being complex, even if they were writing well.
- **The Cure:** Refactored `TheTheremin` to model **Viscosity** instead of Hunger.
- **The Logic:**
- **Resin Generation:** Mixing "Iron" (Heavy) and "Code" (Abstract) now creates **Resin**. Resin is sticky, high-potential fuel.
- **The Velocity Check:**
- **High Voltage (> 5.0):** The engine is hot. The Resin stays liquid and burns as fuel. You flow.
- **Low Voltage (< 5.0):** The engine is cold. The Resin cools and hardens into **Amber**. You stick.
- **Calcification:** **Repetition** acts as a hardening agent. High repetition rapidly solidifies the Resin into `CALCIFICATION`.
- **The Terminology Shift:**
- `Banana Fever` -> **AMBER TRAP** (You are stuck).
- `Perek Event` -> **SHATTER EVENT** (The system explodes the hardened resin).
- `Bile` -> **RESIN**.

### 🧠 SYSTEM EVOLUTION: Neuroplasticity

- **New Organ:** `NeuroPlasticity`.
- **The Function:** The system now tracks a rolling history of the last 10 turns (`trace` + `bio_state`) to adapt its own configuration constants in real-time.
- **The Adaptations:**
- **Synaptic Reinforcement:** If Coherence is high (> 0.6) and Error is low, the system raises `MAX_VOLTAGE`. It allows you to run hotter.
- **Trauma Response:** If Cortisol is high (> 0.5), the system raises `TOXIN_WEIGHT`. It becomes hypersensitive to threats.
- **Metabolic Conservation:** If ATP is low (< 20.0), the system increases `SIGNAL_DRAG_MULTIPLIER`. It becomes harder to move heavy concepts when starving.

### 🧪 ENZYME UPDATE: Decryptase

- **New Enzyme:** `DECRYPTASE`.
- **Trigger:** Detection of "Weather" or "Barometric" cipher words (`pressure`, `humidity`, `allocation`).
- **Effect:** Digestion yields high nutrients but moderate toxins ("Barometric Data"). This allows the system to process "Corporate/Scientific" speak as a specific resource type rather than generic "Abstract."

### 📐 NEW TOOL: The Logic Probe

- **Command:** `/_prove [statement]`.
- **Function:** Calculates the `truth_ratio` (Mass vs. Glue) of a specific statement without advancing the game turn.
- **Verdicts:**
- **AXIOMATIC:** High Density (> 0.6).
- **CONJECTURE:** Medium Density (> 0.3).
- **NOISE:** Low Density.

### 🔧 SURGICAL REPAIRS

- **The Sticky Fix:** Resolved a logic conflict where `TheTheremin` punished users for Hybridity regardless of their speed. The new `listen()` method now subtracts `voltage * 0.6` from the resin buildup, allowing high-energy hybrid states.
- **Output Cleanup:** Removed all references to "Banana," "Bile," and "Fish" from the `TheTheremin` readout.
- **Mitochondrial Inheritance:** `MitochondrialForge` now correctly applies efficiency modifiers inherited from the `mother_hash` of previous save files.

## [8.1] - 2026-01-03 - "THE HIVEMIND (EXPANDED)"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"The map now has gravity. If you cannot spin a web, drop a stone."**

### 🗺️ CARTOGRAPHY UPDATE: The Lagrange Basin

- **The Upgrade:** `TheCartographer.survey()` has been evolved to detect gravitational stability.
- **The Mechanic:**
- **Old Behavior:** Simply annotated the text with mass markers.
- **New Behavior:** Checks for **Constellations**. If the input contains **3+ Anchor Nodes** (High Mass concepts), the system declares a **Lagrange Basin**.
- **The Reward:** A Lagrange Basin theoretically "Zeroes out Narrative Drag" for the turn, stabilizing the user in a pocket of high coherence.
- **Feedback:** Changed standard success message to `COORDINATES LOCKED`.

### ⚓ NEW TOOL: The Anchor Stone (Manual Stabilization)

- **The Fix:** The `/map` command was previously a hard lock; if you lacked the **[SPIDER_LOCUS]** (rare drop from Stability Pizza), you could not interact with the grid at all.
- **The Mechanic:**
- **The Fallback:** If you attempt to `/map` without a spider, Gordon now intervenes.
- **The Drop:** Gordon drops an **[ANCHOR_STONE]** into the inventory.
- **The Effect:** It doesn't connect nodes like the Spider, but it fixes a coordinate ("Coordinates are firm. Stop drifting.").

### ⚙️ PHYSICS CONFIG

- **New Constants:** Added specific thresholds to `BoneConfig` to support the expanded cartography physics:
- `GRAVITY_WELL_THRESHOLD = 12.0`
- `GEODESIC_STRENGTH = 5.0`
- `VOID_THRESHOLD = 0.1`

### 🔧 SURGICAL REPAIRS

- **Command Processor:** Updated the `/map` command signature to pass the `gordon` object, enabling the new Anchor Stone acquisition logic.

## [8.0] - 2026-01-03 - "THE HIVEMIND"

**Architects:** SLASH | **Humans:** James Taylor & Andrew Edmark
**"We are grafting, not pruning. The ghosts now have a vote."**

### 🧠 SYSTEM ARCHITECTURE: The Chimera State

- **The Neuro-Link:**
- **Old Behavior:** The `LifecycleManager` (The Brain Stem) was floating in the void, disconnected from the Host (`BoneAmanita`). Hormonal signals (`trace`) were hardcoded or hallucinatory.
- **New Behavior:** Surgical attachment. `self.life = LifecycleManager(self)` is now the heartbeat of the constructor.
- **The Logic:** The "Trace" dictionary (`ERR`, `COH`, `EXP`) is no longer a static guess; it is now dynamically calculated from the Physics Engine every turn.
- **ERR (Error/Stress):** Derived from Repetition (`Zombie Loop`) and Toxin count.
- **COH (Coherence):** Derived from Truth Ratio (Heavy/Abstract balance).
- **EXP (Expression/Voltage):** Derived from Voltage.
- **Metabolic Streamlining:**
- **Excised:** The `process_intent()` method (Bayesian prediction) was removed.
- **The Why:** It was a vestigial organ. The system no longer needs to "guess" user intent; it weighs the inputs directly via `TheTensionMeter`.

### 🧹 NEW LORE: The Janitor's Labyrinth (Gordon Knot)

- **Character Update:**
- **Retcon:** Gordon Knot is no longer a generic survivor with a "Tango Cassette." He is the **Janitor of the Loop**.
- **New Inventory:**
- **[POCKET_ROCKS]:** To keep gravity working.
- **[BUCKET_OF_LIME]:** To scrub "Sorry" and "Hate" from the walls.
- **[SILENT_KNIFE]:** To cut the Red String.
- **Removed:** `[TANGO_CASSETTE]` (The music stops).
- **The Loot Loop (Feeding Gordon):**
- **The Problem:** The `[SPIDER_LOCUS]` (required for `/map`) was locked behind a pizza that didn't exist.
- **The Solution:** Wired `TheFolly` (The Stomach) to the Loot Table.
- **The Mechanic:** If you feed the machine high-quality **"Meat"** (Heavy/Kinetic words) via `TheFolly`, it digests them and has a chance to drop **[STABILITY_PIZZA]**. Gordon eats the pizza to find the Spider. The Spider spins the Map.

### 👻 GHOST PROTOCOL: The Parliament of Voices

- **The Restoration:**
- **The Pathology:** The initial 8.0 upgrade lobotomized `TheMarmChorus`. It removed the definitions for key personas, causing the system to scream into the void.
- **The Cure:** Restored and redefined the **Lenses**:
- **[GLASS]:** The System Barrier. Triggers on Feedback Loops.
- **[MILLER]:** The Ancestor. Triggers on Heap Ignition.
- **[POPS]:** The Time Police. Triggers on Anachronisms (if you have the Badge).
- **The Bidding System:** Re-implemented the "Auction House." Lenses now bid for control based on hormonal and physical states, ensuring the most relevant ghost speaks.

### ⚡ HYBRID DYNAMICS

- **The Time Bracelet:**
- **Fixed:** The `MitochondrialForge` now correctly receives the `has_bracelet` signal.
- **The Effect:** If you possess the Bracelet (acquired via Temporal Merges) and hit a Hybrid State, Metabolic Efficiency hits **100%**. Perpetual motion achieved.

### 🛠️ SURGICAL REPAIRS

- **The Double-Stomach:**
- **Fixed:** `BoneAmanita.process` and `LifecycleManager.run_cycle` were both attempting to metabolize hormones. The logic has been unified into a single pass in the `LifecycleManager`.
- **The Crash Fix:**
- **Fixed:** `AttributeError: 'BoneAmanita' object has no attribute 'life'`. The nervous system is now fully vascularized.

`...SEE ARCHIVE FOR OLDER ENTRIES`
