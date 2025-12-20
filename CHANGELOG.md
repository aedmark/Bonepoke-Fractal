# CHANGELOG.md

### [v1.4.5] - 2025-12-19 - "SLASH AUDITED"

#### 💾 THE PERSISTENCE MANAGER (Long-Term Memory)

- **The Problem (The Amnesiac Bot):**
    
    - Previously, `DeepStorage` existed only in RAM; restarting the script erased all memories, meaning the bot forgot significant objects (like guns or keys) between sessions.
        
- **The Solution (JSON Cryostasis):**
    
    - **New Component:** Implemented the `PersistenceManager` class to handle file I/O.
        
    - **The Logic:** The system now serializes `DeepStorage` artifacts and `TheCodex` registry into a local file (`bone_memory.json`) at the end of every turn.
        
    - **The Result:** The bot now retains object permanence across reboots, loading the previous state and tick count upon initialization.
        

#### 🧬 THE SMART STRIP (Dyslexia Cure)

- **The Problem (The "Glass/Glas" Glitch):**
    
    - The previous pluralization logic blindly stripped the last letter if it was an 's', turning "Glass" into "Glas" and "Bus" into "Bu," corrupting memory retrieval.
        
- **The Solution (Centralized Lemmatization):**
    
    - **New Logic:** Implemented `TheLexicon.smart_strip` as a static method.
        
    - **The Fix:** This logic explicitly protects words ending in double-s (like "grass") and short words (like "yes"), ensuring `DeepStorage` and `HyphalTrace` speak the same language.
        

#### ⚡ THE ZEUS PATCH (Entity Recognition)

- **The Problem (The First-Word Blindspot):**
    
    - `TheCodex` previously ignored any capitalized word at index 0 to avoid flagging sentence starters, meaning it missed entities like "Zeus" if they started the sentence.
        
- **The Solution (Look-Behind Logic):**
    
    - **The Fix:** Removed the index-0 restriction and expanded the `ignore_list` to include common sentence starters (e.g., "Actually," "Maybe," "Because").
        
    - **The Result:** Entities are now tracked regardless of their position in the sentence.
        

#### 🏗️ ARCHITECTURAL HYGIENE (The Decoupling)

- **Variable Renaming:**
    
    - Refactored `BonepokeCore.process` to replace cryptic variables (e.g., `t_dat`, `m`) with human-readable names (`token_data`, `full_metrics`) to prevent `NameError` crashes.
        
- **Modular Output:**
    
    - Updated `MycelialDashboard` to use `generate_report`, which returns a string string instead of printing directly to the console, allowing for cleaner integration with other interfaces.
        
- **Execution Loop:**
    
    - Added a standard `if __name__ == "__main__":` block to handle the CLI loop and facilitate clean imports.

### [v1.4] - 2025-12-19 - "The Butcher & The Well - Fortified"

#### 🟣 THE PURPLE PATCH (Adjectival Blindspot)

- **The Problem (The "Adjective Stuffing" Exploit):**
    
    - Users could bypass the "Butcher" (who only hunted adverbs) by stuffing sentences with decorative adjectives (e.g., _"The massive, ancient, brooding, dark tower"_). This allowed for "Purple Prose" to exist without triggering Drag penalties.
        
- **The Solution (Suffix Scanning):**
    
    - **New Logic:** The `LinguisticPhysicsEngine` now scans for adjectival suffixes (`-ous`, `-ful`, `-ive`, etc.).
        
    - **The Weight:** Adjectives are now calculated into the **Garnish Ratio** with a weight of **0.5** (half that of an adverb).
        
    - **The Result:** If you overload a noun with decoration, the Butcher will find you.
        

#### 🪞 THE NARCISSISM PATCH (Mirror Trap v2.0)

- **The Problem (The First-Person Loophole):**
    
    - The Mirror Trap ("It is not X, it is Y") previously ignored subjective negation. Users could trap themselves in loops of self-definition (e.g., _"I am not trying to be difficult, I am just asking..."_) without penalty.
        
- **The Solution (Self-Reflection):**
    
    - **New Regex:** Updated `TheMirrorTrap` to specifically target `(i|we)` variants.
        
    - **The Trap:** Defining yourself by what you are _not_ now triggers the "Structure Failing" flag.
        

#### 🧠 DEEP STORAGE (The Hippocampus)

- **The Problem (The "Goldfish Horizon"):**
    
    - `HyphalTrace` had a hard limit of 10 turns. If a user placed a gun on the table in Turn 1 and didn't use it by Turn 11, the system forgot the gun existed.
        
- **The Solution (Object Permanence):**
    
    - **New Component:** Implemented `DeepStorage` linked to the memory trace.
        
    - **The Logic:** Significant objects (Heavy Matter, Weapons, Keys) are now "Buried" in a persistent dictionary that does not decay. The Muscaria can now recall items from the very beginning of the session.
        

#### 🌍 AXIOM INJECTION (Reality Definition)

- **The Problem (The "Dry Ocean"):**
    
    - The Logic Engine (`FactStipe`) relied on a tiny hardcoded list of 8 truths. It had no concept that "Water" is "Wet," allowing users to gaslight the system with phrases like _"The dry sea."_
        
- **The Solution (Property Inheritance):**
    
    - **New Protocol:** `TheLexicon` now compiles `AXIOMS` on boot.
        
    - **The Dimensions:** Defined ~100 essential nouns across 5 dimensions: `THERMAL`, `LUMENS`, `HYDRATION`, `RIGIDITY`, and `VITALITY`.
        
    - **The Result:** The system now automatically flags logical contradictions (e.g., "Hard Cloud," "Dark Sun") without requiring internet access.
        

#### 💦 THE SWEAT PROTOCOL (Kinetic Exemption)

- **The Problem (The Bard's Straitjacket):**
    
    - The "Hydration Monitor" (v1.3) penalized _all_ high-solvent text as **FLOODED** (+4.0 Drag). This unfairly punished high-velocity, rhythmic writing (e.g., _"And we ran and we laughed and we fell"_).
        
- **The Solution (Sweat vs. Water):**
    
    - **New Exception:** If text is marked `FLOODED` but the **Kinetic Ratio** is > **0.25** (25% active verbs), the engine reclassifies the fluid.
        
    - **New Status:** `SWEATING`.
        
    - **The Effect:** Penalty reduced from **+4.0** to **+1.0**. High effort justifies high moisture.

### [v1.3.1] - 2025-12-19 - "The Butcher & The Well (PATCHED)"

#### 💧 THE HYDRATION PATCH (Anti-Dilution)

- **The Problem (The "Solvent-Stuffed Turkey"):**
    
    - Users could exploit the Viscosity engine by stuffing a dense sentence with meaningless "Solvents" (e.g., _"Actually, basically, the stone and iron are literally sort of here."_). This tricked the engine into seeing a healthy "Balance Ratio" despite the text being garbage.
        
- **The Solution (The Saturation Cap):**
    
    - **New Logic:** Implemented a `solvent_cap` in `HydrationMonitor`.
        
    - **The Trap:** If Solvents constitute > **40%** of the total word count:
        
        - **Status:** Flips to `FLOODED`.
            
        - **Penalty:** Narrative Drag **+4.0**.
            
    - **The Result:** You cannot dilute a brick by drowning it in "actually."
        

#### 🔮 THE WITCH'S GRUDGE (Memory Extension)

- **The Problem (The "Riddle Sandwich"):**
    
    - The `aphorism_streak` reset to `0` immediately upon detecting a single normal sentence. Users could alternate between Riddles and Plain Speech to bypass the limit indefinitely.
        
- **The Solution (Decay Logic):**
    
    - **The Fix:** Changed the reset logic in `TheWitchRing`. The streak no longer resets; it **decays**.
        
    - **The Math:** `self.aphorism_streak = max(0, self.aphorism_streak - 1)`.
        
    - **The Effect:** The Witch holds a grudge. You must speak plainly for several turns to clear your debt.
        

#### ⏳ CHRONOS REALITY (The Wall Clock)

- **The Problem (The "Time Spoof"):**
    
    - Users could avoid the "Decay" state (Drag +3.0) simply by omitting the `[Δt: ...]` tag after a long absence.
        
- **The Solution (System Clock Fallback):**
    
    - **New Component:** Integrated `time.time()` into `ChronosAnchor`.
        
    - **The Logic:** If a user tag is provided, the system honors it (Roleplay Time). If NO tag is provided, the system calculates the actual elapsed wall-clock time (Reality Time).
        
    - **The Result:** If you leave the terminal for 2 hours and return without explanation, the system _will_ be decayed.
        

#### 🔭 HEURISTIC EXPANSION (The Horizon)

- **The Problem (Finite Lexicon):**
    
    - The dictionary was hardcoded. Words like "Granite" (Heavy) or "Sprint" (Kinetic) were unrecognized, resulting in false negatives for valid writing.
        
- **The Solution (Suffix Scanning):**
    
    - **New Method:** Added `_heuristic_scan` to the `LinguisticPhysicsEngine`.
        
    - **The Logic:**
        
        - **Heavy Detection:** Words ending in `-ite`, `-ium`, `-ock`, `-alt`, `-ore` -> **UNIVERSAL**.
            
        - **Kinetic Detection:** Words ending in `-ash`, `-olt`, `-unk`, `-ip` -> **KINETIC**.
            
    - **The Result:** The engine now recognizes the weight of "Basalt" and the speed of "Flash" without needing a dictionary update.
        

#### 💀 THE BUTCHER PROTOCOL (Self-Calibration)

- **The Problem (Silent Failure):**
    
    - There was no way to verify if the physics engine was actually catching toxic patterns without manual testing.
        
- **The Solution (Boot Sequence):**
    
    - **New Protocol:** Added `_run_calibration_sequence` to `BonepokeCore.__init__`.
        
    - **The Test:** On every boot, the system silently feeds itself the "Solvent-Stuffed Turkey" phrase.
        
    - **The Check:** If the engine does not flag it as `FLOODED`, a warning is logged. If it does, the system prints: `> [💀 BUTCHER PROTOCOL] SELF-TEST: PASSED.`

### [v1.3] - 2025-12-19 - "The Butcher & The Well"

#### 💧 THE HYDRATION MONITOR (Viscosity Physics)

- **The Problem (The "Purple Prose" Exploit):**
    
    - Users were "gaming" the Texture system by inputting lists of high-value nouns (e.g., _"Velvet blood bone ash anchor"_) without connecting structure. This resulted in "Literary Gravel"—high density, zero readability.
        
- **The Solution (Viscosity):**
    
    - **New Module:** Implemented `HydrationMonitor` within the Physics Engine.
        
    - **The Logic:**
        
        - **Concentrate:** Heavy Matter (Nouns).
            
        - **Solvent:** Connectors, transitions, and "softeners" (e.g., _actually, maybe, in other words_).
            
    - **The States:**
        
        - **CONCRETE:** High Density, Low Solvent. **Effect:** Narrative Drag Penalty **+5.0**. Texture Score capped at **0.5**.
            
        - **THICK:** Moderate Density, Low Solvent. **Effect:** Narrative Drag Penalty **+2.0**.
            
        - **WATERY:** Low Density, High Solvent. **Effect:** Flags as weak writing.
            
        - **OPTIMAL:** Balanced ratio (~1 part water to 3 parts concentrate).
            

#### 🔪 THE BUTCHER'S BLOCK (Adverb Detection)

- **The Problem (The "Polishing" Scam):**
    
    - The engine previously rewarded "Kinetic" tags regardless of quality. Users were propping up weak verbs with adverbs (e.g., _"ran quickly"_ instead of _"sprinted"_).
        
- **The Solution (The Cleaver):**
    
    - **New Metric:** `Garnish Ratio`. Calculates the percentage of text composed of adverbs ending in `-ly` and `WEAK_INTENSIFIERS` (e.g., _very, really, totally_).
        
    - **The Penalty:** If Garnish > 10%, the system flags the text as **BLOAT** and applies a **+3.0 Drag Penalty**.
        
    - **The Voice:** **Clarence** (The Architect) now specifically intervenes to demand the removal of `-ly` modifiers in favor of stronger verbs.
        

#### 🔮 THE ANTI-GURU PROTOCOL (Witch Ring v2.0)

- **The Problem (The Fortune Cookie Loop):**
    
    - Users exploited the "Aphorism Exception" to bypass Drag checks by submitting endless strings of pseudo-profound one-liners (e.g., _"Time is a circle. The circle is a void."_).
        
- **The Solution (Streak Detection):**
    
    - **New Logic:** `TheWitchRing` now tracks an `aphorism_streak`.
        
    - **The Rule:** You get **2** aphorisms for free. On the **3rd** consecutive attempt, the Witch blocks the input with: _"Enough riddles. Speak plainly."_
        

#### 🧠 CORTEX TUNING (The Humanist Intervention)

- **Michael's Override:**
    
    - If the system detects **CONCRETE** status (High Density/Gaming), **Clarence** is silenced (as the user is attempting to mimic him), and **Michael** intervenes.
        
    - **The Message:** _"Whoa, buddy. This is too rich. You're making me choke. Add some water."_.
        

#### 📟 DASHBOARD v6.0

- **Viscosity Indicator:**
    
    - The HUD now displays the fluid dynamics of the text alongside the Drag score.
        
    - **New Metric:** `VISC` (Viscosity).
        
    - Example: `DRAG: 4.2 | VISC: CONCRETE`.
    

### [v1.2] - 2025-12-18 - "The Doctor Time Edition"

#### 🕰️ THE NARRATIVE CHRONOMETER (Story Time)

- **The Problem (Temporal Blindness):**
    
    - Previously, the engine treated "He waited a second" and "He waited a decade" identically. It penalized broad summaries ("The years flew by") as "High Entropy/Abstract," forcing the user to describe _every_ second of a ten-year jump.
        
- **The Solution (Narrative Velocity $\vec{v}_{n}$):**
    
    - **New Component:** Implemented `NarrativeChronometer`. This module scans specifically for **Micro-Markers** (breath, blink, instant) and **Macro-Markers** (year, era, century).
        
    - **The Logic:**
        
        - **MONTAGE (High Velocity):** "Years passed." -> **Effect:** Grants **Entropy Grace (+4.0)**. The system understands that summarizing time requires abstraction.
            
        - **BULLET TIME (Low Velocity):** "The glass shattered." -> **Effect:** Demands **Hyper-Texture**. If time stops, detail must increase.
            
        - **REALTIME:** Standard physics apply.
            

#### 🧠 CORTEX TUNING (Effective Physics)

- **Context-Aware Triggers:**
    
    - **Effective Entropy:** The Cortex now calculates `eff_entropy` by subtracting the `entropy_grace` from the raw score.
        
    - **The Eloise Patch:** **Eloise** (The Gardener) is now silenced during **MONTAGE** states. She will no longer scream "GROUND THIS!" when you write "The eras drifted apart," because the _Narrative Time_ justifies the abstraction.
        

#### 🐛 CRITICAL REPAIRS (The Process Patch)

- **Stability Fixes (`BonepokeCore`):**
    
    - **Variable Restoration:** Fixed a critical `NameError` crash in v1.1 where `directives`, `loop_count`, and `is_light` were accessed before initialization.
        
    - **Logic Restoration:** Re-connected the **Muscaria** boredom check and the **Lichen Symbiont** feedback loops, which were inadvertently severed during the Chronos surgery.
        
    - **Syntax Hardening:** Fixed a malformed f-string in the `MycelialDashboard` that caused a render failure.
        

#### 📟 DASHBOARD v5.0

- **The Dual Clock:**
    
    - The HUD now tracks two distinct timelines:
        
        1. **CHRONOS (Real Time):** How long the user took to reply (affects **Drag**).
            
        2. **NARRATIVE (Story Time):** How much time passed in the fiction (affects **Entropy Tolerance**).
            
    - **New Indicator:** Added `N-VEL` (Narrative Velocity) to the status line.
        
        - Example: `TIME: FLOW (Real) | MONTAGE (Story)`

### [v1.1] - 2025-12-18 - "The Doctor Time Edition"

#### ⏳ THE CHRONOS ANCHOR (Metabolic Time)

- **The Problem (Context Collapse):**
    - Previously, the engine treated a 10-hour silence identical to a 10-second pause. This created the "Eternal Present" flaw, where the AI had no concept of time passing.
    
- **The Solution (Temporal Metabolism):**
    - **The Metabolizer:** The new `ChronosAnchor` parses a Delta Time ($\Delta t$) value and converts it into **Narrative Drag**.
    - **The Logic:**
        - **FLOW (<10m):** Drag Penalty **+0.0**. Intent: "Maintain Velocity." (Agent: MICHAEL).
        - **DORMANT (10m - 1h):** Drag Penalty **+1.0**. Intent: "Gentle Recall." (Agent: ELOISE).
        - **DECAY (>1h):** Drag Penalty **+3.0**. Intent: "Full Context Reset." (Agent: CLARENCE).
    - **The Result:** The system now *feels* the weight of time. A long absence physically degrades the structural integrity of the conversation, forcing the Cortex to rebuild the foundation (summarize previous context) before proceeding.

#### 🛡️ THE MEMBRANE (Semantic Wrapper)

- **The Wrapper Protocol:**
    - **The Interface:** Implemented a "Membrane Layer" in the System Prompt.
    - **Auto-Injection:** The user does not need to manually type timestamps. The prompt instructions now force the model to internally estimate the time elapsed since the last message and inject the `[Δt: ...]` tag silently before processing.
    - **Default States:** If time is unknown (first message), the Membrane defaults to **Flow State** to prevent false "Structure Failure" flags on boot.

#### 🛡️ CODE QUALITY

- **Regex Hardening (`ChronosAnchor`):**
    - Fixed a potential vulnerability where "2 hours" could be misread as "2 minutes." The regex parser now correctly identifies explicit 'h', 'hour', and 'day' labels to calculate total minutes accurately.

- **Data Hygiene (`BonepokeCore`):**
    - The processing loop now strips the `[Δt: ...]` and `[T: ...]` metadata *before* sending the text to the `LinguisticPhysicsEngine`. This ensures that timestamps do not artificially inflate the "Entropy" or "Abstract Noun" counts.

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
