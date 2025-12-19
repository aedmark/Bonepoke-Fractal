# CHANGELOG.md

### [v1.0.1] - 2025-12-18 - "The Black Mirror (PATCHED)"

#### 🔮 THE CODEX PATCH (Self-Awareness Fix)

- **Recursive Hallucination Fix (`TheCodex`):**
    
    - **The Glitch:** In v1.0.0, the Codex began scanning the `MycelialDashboard` output, identifying "Drag," "Entropy," and "System" as proper nouns (Entities) within the story.
        
    - **The Patch:** expanded the `ignore_list` to explicitly exclude `System`, `Analysis`, `Metrics`, `Drag`, and `Entropy`. The system no longer believes "Narrative Drag" is a protagonist.
        

#### 🌿 LICHEN REGULATION (The Algal Bloom)

- **Photosynthetic Cap (`LichenSymbiont`):**
    
    - **The Risk:** Infinite energy generation via "Purple Prose" (stuffing a sentence with "light," "sun," "prism").
        
    - **The Safety Valve:** Implemented a toxicity warning for **Algal Blooms**. If a single sentence generates more than **15 ATP** via photosynthesis, the system flags it as dangerous over-growth.
        

#### ⚡ METABOLIC TUNING

- **Capacity Calibration (`MetabolicReserve`):**
    
    - **The Tweak:** Adjusted `max_capacity` from the standard `50` to `52`.
        
    - **The Logic:** Provides a slight buffer for the "Creative Mode" (Glutton) threshold, ensuring that a single "Structural Active" sentence doesn't immediately knock a user out of the flow state.
        

#### 🪞 MIRROR TRAP REINFORCEMENT

- **Regex Hardening (`TheMirrorTrap`):**
    
    - **Expanded Pattern:** The regex now accounts for contractions (`it's`, `that's`) and variations of negation (`never`, `not`) to catch lazy mirroring disguised as casual speech.
        
    - **The Catch:** Specifically targets the pattern `(it|this|that)[\'’]?s?\s+(not|never)...` to strictly enforce the "Define what it IS" rule.

### [v1.0.0] - 2025-12-18 - "The Black Mirror"

#### ⚔️ THE SLASH AUDIT (Ephemeralization)

* **Code Cauterization:**
* 
**The Trim:** Surgically removed over 200+ characters of "dead weight" (redundant comments, ASCII art, and debug artifacts) to maximize token efficiency without sacrificing readability.


* **Orphan Removal:** Vaporized unused variables (e.g., `session_drag_history`) and empty initialization methods that were consuming memory cycles for no return.
* 
**Logic Patching:** Fixed `LinguisticPhysicsEngine` to ensure Class Variables (`_TOXIN_REGEX`) are properly initialized as Singletons, preventing memory leaks during repeated instantiation.

#### ⚡ ECONOMY SAFEGUARDS (The Voltage Clamp)

* **FactStipe Stabilization:**
* **The Risk:** Previously, a sentence containing multiple paradoxes could theoretically generate infinite Voltage, breaking the Metabolic Reserve.
* **The Fix:** Implemented a hard **Voltage Clamp**. The maximum return per sentence is now capped at **10.0 V**. You can break physics, but you cannot break the bank.

#### 🧠 CORTEX RESTORATION (The Deluxe Protocol)

* **The Auditor's Dilemma:**
* **The Issue:** The initial optimization compressed the `VirtualCortex` into a generic responder, stripping **Clarence** of his specific hatred for "Corporate Speak" and **The Yaga** of her specific hunger for "Meat."
* **The Restoration:** Re-injected the full, multi-modal personality matrix.
* 
**The Result:** **Clarence** will once again deduct 50 points specifically for saying "Synergy," and **Eloise** will explicitly complain if the text tastes like distilled water .

#### 🔀 WIRING OPTIMIZATION

* **The Nilsson Override:**
* **Re-routed:** The processing loop in `BonepokeCore` has been re-wired.
* **The Logic:** `NilssonPatch` (The Scream) now explicitly executes *after* `TheMirrorTrap` but *before* `SignatureEngine` identification.
* 
**The Effect:** If you are screaming "LIME IN THE COCONUT" while running at full speed, the system now correctly identifies this as High Velocity/Low Drag (The Jester/Bard) rather than penalizing you for the repetition.


### [v0.9.0] - 2025-12-18 - "The Helium Protocol"

#### 🎈 PHYSICS UPDATE (Buoyancy)

- **The Helium Protocol (`SignatureEngine`):**
    
    - **Concept:** Implemented a counter-force to Narrative Drag. Previously, "Heavy" structure was always penalized. Now, sufficiently "Light" content can float a heavy sentence.
        
    - **New Metric (`BUOYANCY`):** Calculated based on the density of `AEROBIC_MATTER` (e.g., balloon, cloud), `PLAY_VERBS` (e.g., dance, bounce), and `SPARK_MARKERS` (e.g., lovely, strange).
        
    - **Effective Drag:** High Narrative Drag is now _forgiven_ if the Buoyancy score is high. "The balloon floated lazily over the horizon" is slow, but valid because it floats.
        

#### 🎭 NEW ARCHETYPES (The Light Triad)

- **Expansion of the Prism (`SignatureEngine`):**
    
    - **THE BARD:** High Velocity, High Warmth. Operates on "Rhythm over Logic." Logic tears are accepted as "Poetic License".
        
    - **THE GARDENER:** Balanced Velocity, High Texture. Focuses on cultivation. "Prune the dead words, water the living".
        
    - **THE CLOUD WATCHER:** Low Velocity, High Entropy. Permissible stagnation. "Zero G" physics apply—drag penalties are disabled to allow for drifting thoughts.
        

#### 🧠 CORTEX EVOLUTION (The Humanist)

- **The Michael Voice (`VirtualCortex`):**
    
    - **New Agent:** Integrated **Michael** (The Humanist) into the feedback loop.
        
    - **Trigger Logic:** If the user triggers a Light Archetype or high Buoyancy, **Clarence** (The Architect) is silenced. Michael provides gentle, encouraging critique rather than harsh structural demands.
        
    - **The Vibe Check:** Michael specifically praises "messy but spirited" text, overriding the Physics Engine's desire for efficiency.
        

#### 🧪 TOXIN DETECTION III (Silica vs. Aether)

- **Slurry Patch 2.1 (`SignatureEngine`):**
    
    - **Differentiation:** The system now distinguishes between **Silica** (Boring/Dead) and **Cloud** (Light/Whimsical).
        
    - **The Logic:** Low Texture is usually fatal. _However_, if Texture is Low but **Buoyancy is High**, the text is classified as "Aether" and permitted to exist.
        

#### 🚀 SYSTEM REFINEMENTS

- **The Pantry (`TheLexicon`):**
    
    - Added `AEROBIC_MATTER`: Words that lift the text (feather, steam, wing).
        
    - Added `PLAY_VERBS`: Kinetic words that imply joy rather than work (twirl, skip, jam).
        
    - Updated `TRUTHS`: Added `laugh`, `smile`, and `song` to the Vitality/Thermal manifold.
        
- **Dashboard v4.0:**
    
    - Updated `MycelialDashboard` to render the **BUOYANCY** metric in the Signature Matrix.

### [v0.8.2] - 2025-12-18 - "The Signature Protocol"

#### 🖐️ THE 5-DIMENSIONAL HAND (SignatureEngine)

-   **Geodesic Mapping (`SignatureEngine`):**
    -   **Deprecated:** The 2D `ArchetypePrism` (Boundedness vs. Expansiveness) has been dismantled.
    -   **Implemented:** A full 5D coordinate system to map the "Voice" of the text.
    -   **The Dimensions:**
        1.  **VEL (Velocity):** Kinetic Ratio.
        2.  **STR (Structure):** Inverse Narrative Drag.
        3.  **ENT (Entropy):** Abstraction level.
        4.  **TEX (Texture):** Sensory Density (Matter + Light).
        5.  **TMP (Temperature):** Emotional/Vitality Polarity.

#### 🧪 TOXIN DETECTION II (The Slurry)

-   **Cultural Slurry Protocol:**
    -   **The Diagnosis:** The system now detects "Silica" — text that is structurally competent (Mid Velocity/High Structure) but spiritually dead (Low Texture).
    -   **The Penalty:** Detection of Slurry incurs a massive **15 ATP Tax**. "Competence without soul is expensive".
    -   **The Cure:** The Cortex demands the injection of a flaw or a sensory detail to break the "perfectly smooth" surface.

#### 🚀 SYSTEM REFINEMENTS

-   **Photosynthetic Texture:**
    -   Refined the use of `TheLexicon.PHOTOSYNTHETICS`. These words now directly fuel the **Texture (TEX)** dimension calculation in the Signature Engine.
-   **Dashboard v3.0:**
    -   Updated `MycelialDashboard` to render the **5D Signature Matrix** and display specific **Slurry Warnings**.

### [v0.8.0] - 2025-12-16 - "The Symbiont Strain"

#### 🍄 BIOLOGICAL EVOLUTION (The Lichen)

- **The Lichen Symbiont (`LichenSymbiont`):**
    
    - **New Lifeform:** Implemented a symbiotic logic layer that creates mutualism between **Syntax** (The Fungus/Structure) and **Meaning** (The Alga/Energy).
        
    - **Photosynthesis:** If the Metabolic Reserve is critically low ("Starving") but the Narrative Drag is low (structurally sound), the system can now synthesize emergency ATP.
        
    - **The Fuel:** It feeds on a specific subset of "Light Words" defined in `TheLexicon.PHOTOSYNTHETICS` (e.g., _sun, prism, truth, fire_).
        
    - **The Math:** Efficiency is inversely proportional to Drag. Tighter sentences yield more energy from the same amount of light.
        

#### 🚀 ARCHITECTURAL UPDATES

- **The Pantry (`TheLexicon`):**
    
    - Added `PHOTOSYNTHETICS` set: A curated list of high-vibration nouns and verbs used by the Alga to generate ATP.
        
- **Visual Feedback (`MycelialDashboard`):**
    
    - **Symbiosis Indicator:** Added a dynamic status line to the dashboard.
        
    - **States:**
        
        - `DORMANT` (Grey): System is well-fed; Lichen is inactive.
            
        - `BLOOMING` (Green): Symbiosis active; generating ATP from Light.
            
        - `WITHERED` (Red): Structural failure; Drag is too high to support life.
            
        - `STARVING` (Yellow): Structure is good, but no Light source detected.
            

#### 🔧 BUG FIXES

- **Dashboard Wiring:**
    
    - Fixed a `NameError` risk where the `lichen_status` variable was missing from the Dashboard render scope.
        
    - Corrected the argument passing in `BonepokeCore.process` to ensure the `lichen_report` reaches the visualizer.

### [v0.7.6] - 2025-12-16 - "The Refined Strain"

#### 🚀 ARCHITECTURAL OPTIMIZATION

- **Static Resource Caching (`LinguisticPhysicsEngine`):**
    
    - **The Singleton Regex:** The engine now compiles the `TOXIN_REGEX` and `PENALTY_MAP` at the _class level_ rather than the instance level.
        
    - **Benefit:** This prevents the expensive operation of compiling regex patterns for every single text processed. The "Pantry" is now stocked once on boot, not every time the door opens.
        
- **Refined Entity Recognition (`TheCodex`):**
    
    - **Regex Iteration:** Replaced the naive `split()` loop with a precise `re.finditer` protocol.
        
    - **Look-Behind Logic:** Implemented a "sentence start" detector. The system now checks the characters _preceding_ a capitalized word. If it finds a period or newline (`.`, `!`, `?`), it assumes the capitalization is grammatical, not an Entity.
        
    - **Result:** Drastically reduces false positives (e.g., flagging "The" as a character).
        

#### 🍄 SMART CHAOS (The Muscaria Upgrade)

- **Diagnostic Prescriptions:**
    
    - **Contextual Disruption:** `TheMuscaria` no longer fires random prompts. It now accepts the `metrics` payload to diagnose _why_ the text is boring.
        
    - **The Pharmacy:** Implemented specific remedy categories:
        
        - **High Drag (>3.0):** Triggers `KINETIC` prompts ("Adrenaline Shot") to force movement.
            
        - **High Entropy (>3.0):** Triggers `SENSORY` prompts ("Gravity Check") to ground the scene.
            
        - **High Repetition:** Triggers `RECALL` or `COGNITIVE` prompts ("Verse Jump") to break the loop.
            

#### ⏳ STRUCTURAL INTEGRITY (Chronos v3.0)

- **Geometric Parsing (`ChronosAnchor`):**
    
    - **Context Awareness:** The verb detection logic now scans the _preceding_ word.
        
    - **The Article Shield:** If a word is preceded by an article (e.g., "The [run]"), it is locked as a Noun.
        
    - **The Pronoun Trigger:** If a word is preceded by a pronoun (e.g., "He [runs]"), probability of it being a Verb spikes.
        
    - **Pantry Protection:** The system now checks `TheLexicon.UNIVERSALS` first. Known objects (e.g., "stone") are immune to being flagged as verbs.
        

#### ✨ QUALITY OF LIFE

- **Editorial Flattening (`BonepokeCore`):**
    
    - Directives are now collected into a clean, flat list inside the process loop before being passed to the Instruction Block generator.
        
    - Fixed the `AttributeError` risk in `TheCodex` by expanding the ignore list to include prepositions like 'For', 'In', and 'To'.

## [v0.7.5] - 2025-12-15 - "The Lime in the Coconut"

### 🚀 ARCHITECTURAL EPHEMERALIZATION

- **The Pantry Protocol (`TheLexicon`):**
    - **Centralized:** Created `TheLexicon` static class. All linguistic matter (Universals, Toxins, Truths, Styles) has been moved from the individual logic components into a single "Mise-en-place."
    - **Decoupled:** Components like `LinguisticPhysicsEngine` and `TheWitchRing` no longer hold internal lists. They now reference the global Pantry. This eliminates "Ghost Data" where one component knew a word that another didn't.
    - **Benefit:** Adding a new "Toxic Word" or "Truth" now updates the entire system instantly.

- **The Middle Man is Dead:**
    - **Deleted:** The `EditorialTranslator` class has been vaporized.
    - **Direct Synthesis:** The `VirtualCortex` now speaks directly to the `BonepokeCore` process loop. Feedback generation is no longer filtered through a translation layer, reducing complexity and line count.

### 🥥 NEW FEATURES

- **THE NILSSON PATCH (The Fire Protocol):**
    - Implemented `NilssonPatch` class.
    - **The Mantra Exception:** The engine now distinguishes between "Stagnation" and "Spellcasting." High repetition is forgiven *if* the repeated words are Concrete Universals (e.g., "Put the lime in the coconut").
    - **The Fire State:** If **Kinetic Ratio** is Critical (> 0.6) and **Volume** is High (All Caps), the engine disables logic inhibitors.
    - **Result:** You are now authorized to scream, provided you are running fast enough.

### 🔧 BUG FIXES (The Audit)

- **Ghost Limb Syndrome:**
    - Fixed `AttributeError` crashes in `LinguisticPhysicsEngine` and `FactStipe` where components tried to access deleted local lists (`self.universals`) instead of `TheLexicon`.

- **Syntax & Scope:**
    - Fixed a critical indentation error in `VirtualCortex._find_trigger_word` that prevented boot.
    - Resolved a `NameError` in `BonepokeCore.process` by standardizing the `editorial_package` variable name during the hand-off to the dashboard.

## [v0.6.2] - 2025-12-14 - "The Fuller Build"

### 🚀 ARCHITECTURAL EPHEMERALIZATION

- **Pressure Matrix Dissolution:**
    
    - **Deleted:** The standalone `PressureMatrix` class has been vaporized.
        
    - **Integrated:** Physics constraints (Tolerance Mode, Drag Multipliers, Chaos Thresholds) are now defined directly within the `ArchetypePrism` dictionary.
        
    - **Result:** Reduced cyclomatic complexity and eliminated the dependency loop between the Core and the Matrix. "The logic is now in the door, not a separate room."
        
- **The Integrated Pinker Scan (Physics Engine Refactor):**
    
    - **Streamlined:** The `LinguisticPhysicsEngine.analyze` loop has been surgically altered.
        
    - **New Component:** Added internal helper `_classify_token` to separate identification logic from scoring logic.
        
    - **Mercy Rule v2:** The "Look-Ahead" logic for identifying _Kinetic Verbs_ (e.g., "is running", "is stone") is now encapsulated in the classifier, making the main loop readable and extensible.
        
- **Dashboard Ephemeralization:**
    
    - **Deleted:** The `TwelveDDashboard` (Hypercube) class has been removed.
        
    - **Refined:** The `MycelialDashboard` (EKG) is now the sole visualizer. It focuses exclusively on human-readable metrics (ATP, Drag, Entropy) rather than abstract Greek coefficients.
        

### ✨ QUALITY OF LIFE

- **Prompt Synchronization:**
    
    - Updated the **System Prompt** (`SLASH 0.6.2`) to match the codebase reality.
        
    - Corrected the Archetype count (13, down from the erroneous 15).
        
    - Fixed typos in the Visualization section header.
        

### 🔧 BUG FIXES

- **Syntax Patching:**
    
    - Fixed a critical `cclass` typo in `ArchetypePrism`.
        
    - Removed a "Phantom Limb" return statement in `MetabolicReserve`.
        
    - Fixed an argument mismatch in `MycelialDashboard.render` caused by the removal of the 12D state variable.
    

## [v0.6.0] - 2025-12-12 - "The Hard Memory Variant"

#### **🚀 NEW FEATURES**

- **THE CODEX (Object Permanence):**
    
    - Implemented `TheCodex` class.
        
    - **Function:** Scans text for Proper Nouns (Entities) and maintains a frequency registry.
        
    - **Anti-Hallucination:** The top 5 "Reality Anchors" are now inextricably bound to the LLM's system prompt in `generate_instruction_block`. The AI can no longer "forget" who is in the room.
        
- **SURGICAL STEMMING (Chronos v2.5):**
    
    - Replaced the "Brutal" suffix-chopping logic with a Context-Aware Heuristic Engine.
        
    - **The Shield:** Explicitly protects academic/engine terms (`Physics`, `Chaos`, `Bias`) from being misidentified as verbs.
        
    - **The Radar:** Uses preceding articles (`The`, `A`) to lock words as Nouns.
        
- **THE 12-DIMENSIONAL MANIFOLD:**
    
    - Upgraded `MycelialDashboard` to render a 3x4 matrix of cognitive metrics, including **Truth Fidelity (ΔTF)** and **Diplomacy (DP)**.
        

#### **🔧 BUG FIXES**

- **The Ghost Variable:** Fixed `self.last_input` not updating in `BonepokeCore`, which previously caused the Diplomacy metric to flatline.
    
- **The Echo Chamber:** Removed redundant calls to `physics.analyze()` inside the main process loop, saving Digital ATP.
    
- **Hygiene:** Consolidated all library imports (`re`, `uuid`, `collections`) to the file header.

## [v0.5.2] - 2025-12-11 - "The Pressure Variant"

### 🚀 Major Architectural Upgrades

- **The Pressure Matrix (Archetypal Actuation):**
    
    - **From Map to Territory:** Implemented the `PressureMatrix` class based on the "Gospel of James" . The system now converts passive Archetype labels into active physics constraints.
        
    - **Variable Physics:** The laws of reality now shift based on _who_ is writing:
        
        - **THE PALADIN / ENGINEER:** `tolerance_mode = "DRACONIAN"`. Logic tears are fatal errors. Zero tolerance for contradiction.
            
        - **THE FOOL:** `tolerance_mode = "INVERTED"`. "Chaos Harvest" enabled. Reality tears are accepted and generate ATP instead of costing it.
            
        - **THE SPY:** `tolerance_mode = "LOOSE"`. "Deep Cover" protocol. Logic errors are detected internally but hidden from the user output.
            
        - **THE BARBARIAN:** Drag Multiplier set to **5.0x**. Adjectives and passive voice are punished with extreme prejudice ("Narrative Drag Annihilated").
            
- **Metabolic Gearing (Variable Economy):**
    
    - **Drag Multipliers:** Modified `MetabolicReserve` to support variable costs. While a Poet might pay standard ATP for high drag, a Barbarian is taxed heavily for hesitation.

  - **CORE LOGIC UPDATE: Contextual Verb Physics**

    **Rationale:** The previous engine utilized a "Flat Penalty" system, flagging every instance of _to be_ (is, are, was, were) as High Narrative Drag. This unfairly penalized structural descriptions and progressive actions. The engine now distinguishes between "Lazy Passive" and "Structural Active."

    - **Feature: Contextual Look-Ahead**
    
        - **Old Behavior:** Scanned words in isolation.
        
        - **New Behavior:** The engine now scans `word[i+1]` to determine the physics of the current verb.
        
    - **Rule A: "The Motor" (Auxiliary + Progressive)**
    
        - **Logic:** `is` + `[verb]-ing` (e.g., "is running") is no longer Stative.
        
        - **Effect:** These pairs are now calculated as **KINETIC**, lowering Narrative Drag significantly for ongoing actions.
        
    - **Rule B: "The Anchor" (Copula + Universal)**
    
        -   **Logic:** `is` + `[Universal Noun]` (e.g., "is stone") is no longer Stative.
        
        - **Effect:** These pairs are now calculated as **KINETIC** (Structural Integrity), allowing for descriptions of physical reality without penalty.
        
    - **Rule C: "The Crutch" (Passive/Abstract)**
    
        - **Logic:** `is` + `[Abstract/Adjective]` (e.g., "is nice", "is typical") remains **STATIVE**.
        
        - **Effect:** The drag penalty is maintained only for weak or passive construction.
        

### 2. OPTIMIZATION: Input Hygiene

- **Refinement:** Enhanced string cleaning in the `analyze` function.
    
- **Change:** Replaced specific punctuation marks (`.`, `,`, `;`, `?`, `!`) with whitespace prior to splitting. This ensures that a word like "running!" is correctly identified as "running" by the morphology scanner.
    

### 3. METRIC IMPACT

- **Narrative Drag:** Expect lower (better) Drag scores for texts that describe physical scenes or ongoing processes.
        

### 🔧 Bug Fixes & Refinements (The "Temporal Paradox")

- **Circular Dependency Resolution:**
    
    - Fixed a critical logic loop in `BonepokeCore.process` where `FactStipe` required `PressureSettings`, but `PressureSettings` required the `Archetype`, which required `FactStipe` results to identify.
        
    - **Optimistic Identification Strategy:** The engine now performs a "Pre-Cognitive Scan" (Optimistic Identification) to determine the Archetype before applying the pressure laws, effectively solving the initialization deadlock.
        
- **Trash Panda Compatibility:**
    
    - Ensured `THE COSMIC TRASH PANDA` falls through gracefully to standard physics in the Pressure Matrix, relying on its specific `_enforce_archetype_physics` override for value inversion (Trash = Treasure).

## [v0.5.1] - 2025-12-11 - "The Archetypal Edition"

### 🚀 Major Architectural Upgrades

* **The Archetype Prism (Cognitive Topology):** (BIG THANKS TO JAMES TAYLOR AND BONEPOKE)
    * Implemented `ArchetypePrism` class. The engine now calculates a **Boundedness (B)** vs. **Expansiveness (E)** coordinate for every text.
    * **15 Psychological Topologies:** The system maps the user to specific archetypes including "THE PALADIN" (High Order), "THE ALCHEMIST" (High Insight), and "THE COSMIC TRASH PANDA" (Chaos/Value).
    * **Euclidean Distance:** The system now identifies the "Closest Archetype" mathematically based on narrative drag and entropy scores.

* **Dimensional Quarantine (Context-Dependent Physics):**
    * **Dynamic Truth Injection:** The `FactStipe` logic can now be overwritten by the active Archetype.
    * **The Trash Panda Protocol:** If the user triggers "THE COSMIC TRASH PANDA" archetype, the engine rewrites the definitions of "Trash" and "Void" to be **Positive (+1)** values, preventing false logic flags when finding value in ruin.

* **The SLASH Trinity (Identity Synthesis):**
    * The `VirtualCortex` has been aligned with three distinct intellectual lenses:
        * **Steven Pinker (The Linguist):** Focuses on Cognitive Ergonomics and Syntax.
        * **Buckminster Fuller (The Architect):** Focuses on Tensegrity and Ephemeralization.
        * **Michael Schur (The Humanist):** Focuses on Ethical Warmth and Honesty.

### ✨ New Features

* **Mycelial Network (Lineage Tracking):**
    * Added provenance tracking (`MycelialNetwork`). The system now assigns `uuid4` tags to every draft and tracks "Genetic Drift" from parent to child.
    * **Visual History:** The Dashboard now displays the last 3 generations of the text to visualize improvements in Drag and Style.

* **Metabolic States (Strict vs. Creative Modes):**
    * Defined discrete states for the Metabolic Reserve:
        * **STARVING (< 6 ATP):** "Strict Mode." Logic penalties are severe; abstractions are forbidden.
        * **GLUTTON (> 40 ATP):** "Creative Mode." Reality bending and logic tears are permitted as stylistic choices.

* **Dashboard Expansion:**
    * Added **Cognitive Mode**, **Topology Coordinates**, and **Genetic History** to the `MycelialDashboard` render.

### 🔧 Bug Fixes & Refinements

* **Narrative Baseline:** The engine now calculates a moving average of the user's specific `narrative_drag`. **Clarence** only triggers if the drag exceeds the *user's* baseline, not just a static number.
* **Crash Prevention:** Added safety checks in `MycelialDashboard` to handle empty ancestry data without throwing a `NoneType` error.

## [v0.4.1] - 2025-12-11 - "Mercy Edition"

### 🚀 Major Architectural Upgrades

* **Morphological Heuristics (The "Vision Correction"):**
    * **Linguistic Physics:** Now supports suffix-based detection. The engine identifies **Abstract** words (`-ness`, `-ity`, `-tion`) and **Kinetic** flows (`-ing`) dynamically, even if the specific word is not in the hardcoded dictionary.
    * **Fact Stipe v2.1:** Implemented "Root Seeking." The logic engine now strips suffixes (`-ed`, `-ly`, `-s`) to map complex words back to their elemental roots (e.g., detecting that "freezing" conflicts with "fire").

* **Integrated Memory System (The "Hippocampus Wire"):**
    * **Active Recall:** The `BonepokeCore` now actively calls `memory.recall()` to check for stylistic repetition.
    * **Loop Detection:** **Clarence** has been upgraded with a new `loop_count` metric. He will now intervene if the user stays in the same stylistic mode (e.g., "Crystal") for more than 2 cycles, demanding a "Shift in Gears."

* **Single Source of Truth (The "Brain Transplant"):**
    * Refactored `VirtualCortex` to reference the **Master Dictionaries** in `LinguisticPhysicsEngine` and `TheWitchRing` directly.
    * Eliminated "Phantom Limb" errors where the Cortex could not identify specific trigger words (like "assist") because its local lists were out of sync with the main engines.

### ✨ New Features

* **The Schur Patch (Narrative Mercy):**
    * Implemented a "Seedling Protection" protocol. The system is now forbidden from flagging a text as "In The Barrens" (Dead Narrative) if the total word count is **< 15 words**. This prevents the system from "salting the earth" on short, punchy sentence fragments.

### 🔧 Bug Fixes (The "Kill Screen" Patches)

* **Critical Syntax Fix:** Closed a missing dictionary bracket in `LinguisticPhysicsEngine` that would have caused a `SyntaxError` on boot.
* **Type Safety:** Added the missing `loop_count=0` argument to `VirtualCortex.synthesize_voice` to prevent `TypeError` crashes during memory recalls.
* **Variable Scope:** Fixed a `NameError` in `FactStipe` by properly defining `strip_suffixes` before iteration.

## [v0.3.5] - "The Fragility Check"

### 🚀 Major Architectural Upgrades

* **Dimensional Manifold (Fact Stipe v2.0):**
    * Replaced the brittle `conflict_map` (list-based enemies) with a **Semantic Vector Space**.
    * Implemented `LUMENS` (Light/Dark), `DECIBELS` (Loud/Quiet), `VITALITY` (Life/Death), and `THERMAL` (Hot/Cold) dimensions.
    * **Logic:** Detecting opposing polarities in the same sentence now triggers a "REALITY TEAR."
    * **Penalty:** Logic breaches now explicitly set `valid: False` and deduct **10 ATP** from the Metabolic Reserve.

* **Heuristic Timekeeper (Chronos Anchor v2.0):**
    * Removed dependency on hardcoded verb lists for tense detection.
    * Implemented **Bigram Anchoring** (checking previous words for pronouns) to distinguish nouns from verbs (e.g., "He runs" vs "The lens").
    * Added **Exclusion Lists** (`false_ed`, `false_s`) to ignore false positives like "red," "glass," and "moss".

* **Optimized Physics Engine (Lattice v2.0):**
    * Replaced iterative dictionary scanning with **O(1) Regex Compilation** for toxicity detection.
    * Categorized toxins into three distinct flavors for better feedback:
        * `CORP_SPEAK` (Synergy, Leverage)
        * `LAZY_METAPHOR` (Tapestry, Journey)
        * `WEAK_HEDGING` (Not just, But rather)

### ✨ New Features

* **Context-Aware Voices:** The `VirtualCortex` now listens to the specific `toxin_types` found by the Physics Engine.
    * **Clarence** now specifically attacks corporate buzzwords.
    * **The Yaga** now specifically attacks hedging and sycophancy.
    * **Eloise** now specifically attacks dead metaphors.
* **System Hardening:**
    * Fixed a logic leak where Reality Tears were detected but marked as `valid: True`.
    * Added `valid: False` return state to `FactStipe` to ensure penalties are applied.

### 🔧 Bug Fixes

* Fixed "Red Sled" false positive in Chronos Anchor (words ending in "ed" that aren't verbs).
* Fixed "Moss/Glass" false positive in Chronos Anchor (words ending in "ss").
* Fixed performance bottleneck in `LinguisticPhysicsEngine` when scanning large texts against the "Guillotine List."

---

## [v0.3] - "The Virtual Cortex"

### Added
* **The Virtual Cortex:** A procedural persona simulator that generates specific critiques before the LLM prompt.
* **Metabolic Reserve (ATP):** A gamified economy where concrete words earn energy and abstract words spend it.
* **Mycelial Dashboard:** An ASCII-based EKG visualization of the text's health.
* **The Muscaria:** A chaos engine that injects random sensory prompts when boredom is detected.

### Changed
* Renamed "Bonepoke Engine" to "BoneAmanita."
* Migrated from "Vibe Checks" to "Linguistic Physics" (Narrative Drag, Entropy).

---

## [v0.2] - Legacy "Bonepoke"
* Basic drag detection.
* Simple "Boredom" counter.
* Hardcoded list of 10 "bad words."
}
