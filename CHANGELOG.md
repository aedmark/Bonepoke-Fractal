# Changelog

All notable changes to the **BoneAmanita** project will be documented in this file.

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

## [v0.3.5] - 2023-10-27 - "The Fragility Check"

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

## [v0.3] - 2023-10-25 - "The Virtual Cortex"

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
