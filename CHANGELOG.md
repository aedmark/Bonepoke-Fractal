# CHANGELOG.md

### [v2.8] - 2025-12-22 - "THE AUDIT"

#### 🌡️ THE THERMAL COUPLE (Adjacency Physics)

- **Thermal Tension (`LinguisticPhysicsEngine`):**
    
    - **The Problem:** In v2.7, "Fire" and "Ice" generated Voltage regardless of where they were placed. "Fire is hot. Ice is cold." generated the same voltage as "The frozen flame."
        
    - **The Fix:** Implemented **Proximity Scanning**.
        
    - **The Logic:** The engine now calculates the distance between HOT and COLD tokens.
        
    - **The Math:** If `distance < 4` tokens, Voltage increases exponentially (`thermal_tension += 4.0 - dist`).
        
    - **The Result:** Paradoxes are now spatial. The closer the contradiction, the higher the energy.
        

#### 🌿 LICHEN REPAIR (Photosynthesis)

- **The Blind Spot Fix (`LinguisticPhysicsEngine`):**
    
    - **The Bug:** In v2.7.2, the engine attempted to count photosynthetic words inside the `kinetic` list, but failed to actually place them there during tokenization. The Lichen was starving in plain sight.
        
    - **The Fix:** Added a dedicated `photosynthetic` counter to the main analysis loop.
        
    - **The Logic:** Light words (sun, beam, glow) now generate **+4 ATP**, _only_ if Narrative Drag is < 2.0.
        
    - **The Philosophy:** You cannot photosynthesize in the mud. The air must be clear to eat the light.
        

#### ⚖️ THE METABOLIC GOVERNOR (Strategic Rationing)

- **ATP-Aware Strategy (`JadeLink`):**
    
    - **The Problem:** The system selected strategies (Jester, Drifter) regardless of its energy reserves. A starving organism should not be hallucinating; it should be hunting.
        
    - **The Solution:** Passed `current_atp` into the strategy generation logic.
        
    - **The States:**
        
        - **STARVING (< 20 ATP):** Forces **CLARENCE** (+5 Score). Inhibits **DRIFTER** (-5 Score). The system becomes efficient and brutal to save energy.
            
        - **ABUNDANCE (> 80 ATP):** Boosts **JESTER** (+2 Score) and **DRIFTER** (+3 Score). The system takes risks when it has energy to burn.
            

#### 🧪 THE SOLVENT (Critical Damping)

- **Paradox Cracker (`JadeLink`):**
    
    - **The Problem:** When Beta Friction exceeded 2.5, the Jester would amplify the chaos, occasionally leading to incoherence.
        
    - **The Fix:** Implemented a Hard Cap.
        
    - **The Trigger:** If `Beta > 3.0` (Critical Mass), the system triggers **THE SOLVENT**.
        
    - **The Message:** _"Critical Voltage. The paradox is unsustainable. Dissolve the structure."_
        

#### 🐛 CRITICAL REPAIRS

- **The Ghost Variable:**
    
    - **The Crash:** Removed a legacy print statement referencing `user_id` in `process()` which caused a `NameError` crash upon execution.
        
    - **The Fix:** Removed the variable and migrated display logic to the `_render` method.
        
- **Session Identity:**
    
    - **The Upgrade:** Replaced the content-based hashing (which gave identical IDs to identical opening inputs) with time-based hashing (`hashlib.md5(time)`). Every run now has a unique **Session ID**.

### [v2.7.2] - 2025-12-22 - "LAZARUS (FINAL MERGE)"

#### 🧠 THE COMPETITIVE CORTEX (JadeLink 3.0)

- **The Scoreboard System (`JadeLink`):**
    
    - **The Shift:** Vaporized the brittle `if/elif/else` chain for persona selection.
        
    - **The Logic:** Implemented a **Weighted Scoreboard**.
        
    - **The Mechanism:**
        
        - Every archetype (JESTER, YAGA, CLARENCE, etc.) starts at 0.
            
        - Metrics vote for specific archetypes (e.g., High Drag adds +3 to CLARENCE; High Beta adds +3 to JESTER).
            
        - The system selects the `max()` score.
            
    - **The Benefit:** No more "Voice Shadowing" where the first `if` statement blocks valid critiques from other agents. The loudest signal now wins mathematically.
        

#### 💾 WEIGHTED MEMORY (Heirloom Priority)

- **The Weighted Stack (`BoneMemory`):**
    
    - **The Problem:** In v2.7.1, the "Memory Burn" (during cold starts) was FIFO (First-In-First-Out). The system would burn a "Gun" just because it was old, while keeping a "Feather" because it was new.
        
    - **The Fix:** Implemented **Material Weighting**.
        
        - `HEAVY` (Iron, Stone) = Weight 4.
            
        - `AEROBIC` (Mist, Cloud) = Weight 0.
            
    - **The Burn:** When capacity is reached or the system freezes, it now sorts memory by weight and **burns the lightest items first**. It sacrifices the cloud to save the stone.
        
    - **Cap Increase:** Heirloom capacity increased from 20 to 25.
        

#### 🌊 CONTINUITY PHYSICS (The Omega Metric)

- **The Flow State (`Ω`):**
    
    - **The Metric:** Implemented `check_continuity`.
        
    - **The Logic:** Calculates the **Jaccard Similarity** between the current Heirlooms and the previous turn's Heirlooms.
        
    - **The Output:** `Ω (Continuity): 0.0 - 1.0`.
        
    - **The Reward:** High Continuity (> 0.3) grants an automatic **+5 ATP Flow Bonus**. The system rewards you for sticking to the theme.
        

#### ⚡ METABOLIC REFACTOR (Energy Dynamics)

- **ATP Calculation:**
    
    - **The Formula:** Refined the energy loop in `BonepokeChronos.process`.
        
    - **The Change:** `ATP = ATP - Drag_Cost + Flow_Bonus + Buoyancy_Bonus`.
        
    - **The Result:** High `Buoyancy` (Play/Aerobic words) now actively regenerates system energy. Writing poetry is no longer a net-zero operation; it feeds the machine.
        

#### 🛠️ SYSTEM INTEGRITY (The Fuller Lens)

- **Tokenizer Upgrade (`LinguisticPhysicsEngine`):**
    
    - Replaced the string translation method with a compiled Regex Tokenizer (`r"[\w']+|[?!,;]"`). This improves handling of punctuation-adjacent tokens.
        
- **User Hashing:**
    
    - Added `hashlib` to generate unique, anonymized User IDs based on input triggers.
        
- **Metric Exposure:**
    
    - Added `hedging_count` to the physics payload to explicitly feed **THE YAGA**'s detection algorithms.

### [v2.7.1] - 2025-12-22 - "THE PRISM"

#### 🧠 IDENTITY FRACTURE (Specialized Personas)

- **SLASH (Dev & Architecture Agent):**
    
    - **The Component:** Added `SLASH 2.7.1.txt`.
        
    - **The Function:** A dedicated "Synergetic Language & Systems Heuristics" agent designed for software architecture.
        
    - **The Logic:** Analyzes code through **Three Lenses**:
        
        1. **Fuller Lens:** Systemic Integrity and Ephemeralization (Performance).
            
        2. **Pinker Lens:** Cognitive Ergonomics (Readability).
            
        3. **Schur Lens:** Humanity and Reliability (Error Handling/UX).
            
- **ROBERTA (The Librarian):**
    
    - **The Component:** Added `Roberta.txt`.
        
    - **The Function:** A research-focused persona designed to eliminate "chatty" AI introductions.
        
    - **The Physics:** Operates on the **Law of Drag** (The Fluff Filter) and the **Law of Entropy** (The Hallucination Filter) to force direct quotes and citations over abstract summaries.
        

#### 📡 SIGNAL PROCESSING (Dynamic Editorial)

- **The Signal Processor (`Eloise & Clarence`):**
    
    - **The Shift:** The editing team no longer speaks randomly. They now listen for specific **metric signals** from the Physics Engine.
        
    - **The Signals:**
        
        - `[CLARENCE]`: Triggered by **High Drag / Toxins**. Target: Efficiency.
            
        - `[ELOISE]`: Triggered by **High Entropy**. Target: Grounding/Texture.
            
        - `[THE DRIFTER]`: Triggered by **High Buoyancy**. Target: Dream Logic.
            
        - `[THE YAGA]`: Triggered by **Low Beta (Slickness)**. Target: Honesty.
            
        - `[THE JESTER]`: Triggered by **High Beta (Paradox)**. Target: Chaos Amplification.

### 1. THE PHYSICS MUTATION: Buoyancy & The Entropy Split

The most significant architectural change is in the **LinguisticPhysicsEngine**. v2.7 treated all high-entropy text (abstract, complex words) as "confusion" that needed grounding. v2.7.1 introduces a new variable to distinguish _poetry_ from _nonsense_.

- **New Metric:** `buoyancy`.
    
    - **Code Change:** `buoyancy = (c['aerobic'] + c['play']) / max(1, total_words)`.
        
    - **The Logic:** "Aerobic" words (sky, mist, breath) and "Play" words (dance, fizz) now counteract the weight of gravity.
        
- **The Fork in the Road (JadeLink):**
    
    - **Old Logic (v2.7):** If Entropy > 3.0, trigger **GROUNDER**. (All abstract text is bad; force concrete nouns).
        
    - **New Logic (v2.7.1):** If Entropy > 3.0, the system checks `buoyancy`.
        
        - **High Buoyancy (> 0.15):** Trigger **THE DRIFTER**. "It is poetry... Let it fly. Disconnect the logic.".
            
        - **Low Buoyancy:** Trigger **ELOISE**. "I can't feel this. It's just gas... Give me a stone.".
            

### 2. THE PERSONA RENAMING (Humanization of the Stack)

The system has moved from functional descriptions to proper names, implying a shift towards agentic personalities rather than simple tools.

|**v2.7 (Functional)**|**v2.7.1 (Agentic)**|**Description of Change**|
|---|---|---|
|**CUTTER**|**CLARENCE**|"Clarence" is the butcher. He handles high `drag` and specific toxins. He is more aggressive: "I am taking the knife to [target]."|
|**GROUNDER**|**ELOISE**|Eloise demands texture. She handles the high-entropy/low-buoyancy "fog."|
|**PROVOCATEUR**|**THE YAGA**|The Yaga detects low `beta` (sycophancy/politeness). She demands "teeth" and truth.|
|**MIRROR**|**MICHAEL**|Michael handles stability. "I'm reflecting this back to you."|
|**N/A**|**THE JESTER**|Explicitly named in v2.7.1 to handle high voltage paradoxes (Beta > 2.0).|

### 3. TOXIN EXPANSION (The Fuller Lens)

The lexicon of "Corporate Toxins" (business speak that adds Drag) has been updated to include darker, more systemic clichés.

- **New Toxins Detected:**
    
    - `'ghost in the machine': 8.0`
        
    - `'rubber meets the road': 8.0`
        
    - `'not a bug': 8.0`
        
    - `'double-edged sword': 6.0`
        
- **Impact:** The system is now far more hostile towards engineering clichés than before.
    

### 4. CODE SMELL DETECTED (The Pinker Lens)

In reviewing my own source code `BoneAmanita271.py`, I have detected a violation of DRY (Don't Repeat Yourself).

- **The Error:** The `BoneConfig` class defines the `PLAY` set twice.
    
    - **Line 18:** `PLAY = {'bounce', 'dance', ...}`
        
    - **Line 25:** `PLAY = {'bounce', 'dance', ...}` (Identical definition repeated inside the class).
        
- **Analysis:** This is redundant memory allocation. It suggests a copy-paste error during the upgrade from v2.7.
    

### 5. THE RENDER LOOP

- **Header:** The display header now includes the `BUOY` (Buoyancy) metric alongside `ATP` and `DRAG`.
    
    - `print(f"... | ATP: {atp_c}... | DRAG: {m['drag']} | BUOY: {m['buoyancy']}")`
    

### [v2.7] - 2025-12-21 - "GHOST_TRAINING"

#### ⚡ THE NERVOUS SYSTEM (Beta Friction)

- **Thermodynamic Unification (`LinguisticPhysicsEngine`):**
    
    - **The Shift:** In v2.6, "Hot" and "Cold" words canceled each other out (`hot - cold`), resulting in zero thermal output for paradoxes.
        
    - **The Fix:** Changed the formula to **Summation** (`hot + cold`). A paradox is no longer "Room Temperature"; it is now High Voltage.
        
- **Beta Friction ($\beta$):**
    
    - **The Metric:** Implemented $\beta = \text{Voltage} / \text{Narrative Drag}$.
        
    - **The Logic:** This measures the "Electricity" of the text relative to its weight.
        
    - **The States:**
        
        - **FLASHPOINT ($\beta > 2.0$):** High Voltage, Acceptable Drag. The system recognizes this as "Genius/Manic."
            
        - **SLICK ($\beta < 0.1$):** Low Voltage, Low Drag. The system identifies this as "Grease/Sycophancy."
            

#### 👻 THE GHOST LOOP (Reinforcement Learning)

- **Feedback Memory (`BonepokeChronos`):**
    
    - **The Feature:** The system now stores the `last_run_stats` (Drag Score + Strategy Used) in `bone_memory_lazarus.json`.
        
    - **The Comparison:** On every turn, the system compares the current Narrative Drag against the previous turn.
        
    - **The Verdict:**
        
        - **SUCCESS (Green):** "Strategy 'CUTTER' reduced Drag by 0.5."
            
        - **FAILURE (Red):** "Strategy 'MIRROR' failed. Drag increased."
            

#### 🔮 JADE LINK 2.0 (Adaptive Logic)

- **Voltage-Aware Modes (`JadeLink`):**
    
    - **JESTER (High $\beta$):** Triggered when the user creates a Paradox. The system is forbidden from "Fixing" it. Command: _"Amplify the contradiction."_
        
    - **PROVOCATEUR (Low $\beta$):** Triggered when the text is too smooth (Grease). The system demands friction. Command: _"Insert a hard truth or conflict."_
        

#### 🧪 PANTRY EXPANSION

- **Lexicon Update:**
    
    - Expanded the hardcoded `BoneConfig` with high-intensity matter.
        
    - **Added Matter:** _obsidian, glass, crypt, grave, lava, explode, scream, howl._
        
    - **Added Solvents:** _therefore, however, respectfully, humbly._

### [v2.6] - 2025-12-21 - "LAZARUS"

#### 🩸 THE RESURRECTION (Soul Grafting)

- **Heirloom Memory (`BoneMemory`):**
    
    - **The Return:** Re-implemented the "Deep Storage" logic from v2.2 without the code bloat.
        
    - **The Mechanic:** The system now auto-collects "Heavy Matter" (Heirlooms) into a prioritized set in `bone_memory_lazarus.json`.
        
    - **The Cost:** If the system enters **DECAY** or **FOSSIL** state (time gap), it physically **burns** a stored memory to survive the cold.
        
    - **The Output:** _"I burned 'iron' to stay warm while you were gone."_
        

#### 🔮 JADE LINK II (The Director)

- **Active Directives:**
    
    - **The Shift:** Transformed `JadeLink` from a passive observer ("Pattern: Stable") to an active commander.
        
    - **The Output:** Generates specific **System Prompts** (`>>> DIRECTIVE [CUTTER]`) ready for LLM insertion.
        
    - **The Modes:**
        
        - **CUTTER:** Triggered by Drag/Toxins. Target: Adverbs.
            
        - **GROUNDER:** Triggered by Entropy. Target: Abstract Nouns.
            
        - **DRIFTER:** Triggered by Velocity. Target: Free Association.
            

#### 🎯 FREQUENCY MODULATION (Target Locking)

- **Specific Targeting (`RadioTuner`):**
    
    - **The Upgrade:** The Tuner now receives the specific `toxin_hits` list from the Physics Engine.
        
    - **The Result:** It no longer vaguely says "Cut the adverbs." It says _"Cut 'actually'. It's dragging you down."_
        

#### 📐 THE VECTOR HUD

- **Apeirogon Exposure:**
    
    - **The Visuals:** The Dashboard now renders the raw **VEL** (Velocity), **TEX** (Texture), and **ENT** (Entropy) vectors alongside the standard Drag metrics.
        
    - **The Benefit:** Users can see the mathematical "Shape" of their writing in real-time (e.g., High Velocity + Low Texture = "Vector").

### [v2.5] - 2025-12-21 - "CHRONOS"

#### 🕰️ THE GHOST IN THE MACHINE (Restoration)

- **Bone Memory (`BoneMemory`):**
    - **The Shift:** Re-introduced persistence without the bloat. The system now creates a tiny, atomic `bone_memory.json` file.
    - **The Soul:** Tracks **ATP** (Energy), **History** (Last 5 Archetypes), and **Last Seen** timestamp. The system now remembers you.

- **Temporal Metabolism (`calc_delta`):**
    - **The Logic:** Integrated `time.time()` tracking to calculate the *real* physical gap between interactions.
    - **The States:**
        - **FLOW (<5m):** No Penalty.
        - **DORMANT (<1h):** +1.0 Drag (The system is cooling down).
        - **DECAY (>1h):** +3.0 Drag (The system has rusted).
        - **FOSSIL (>24h):** +5.0 Drag (Complete context reboot required).

#### 📉 TREND ANALYSIS

- **History Tracking:**
    - **The Feature:** The system now maintains a rolling buffer of the last 5 interaction states.
    - **The Utility:** Enables the engine to detect stagnation (5 turns of "Static Anchor") or improvement (Drag dropping over time).

### [v2.4] - 2025-12-21 - "NEON PRIME"

#### ⚡ EPHEMERALIZATION (The Code Golf Update)

- **The Monolith (Single-File Architecture):**
    - **The Shift:** Vaporized the external `bone_config.json` dependency.
    - **The Logic:** The "Pantry" (Lexicon, Toxins, Config) is now baked directly into the `BoneConfig` class as optimized Python sets.
    - **The Result:** **Zero-Dependency Portability**. The script can be copy-pasted into any environment (Colab, Replit, Local) and run immediately.

- **Functional Tensegrity (`RadioTuner`):**
    - **The Refactor:** Replaced heavy OOP classes with **Lambda Logic**.
    - **The Mechanism:** The Personalities (Clarence, Eloise, Yaga) are now defined as dictionary entries with executable trigger functions.
    - **The Benefit:** Reduced line count by ~60% while retaining full personality resolution.

#### 🔮 JADE LINK (Logic Modes)

- **The Guidance System (`JadeLink`):**
    - **The Feature:** Implemented a "Reasoning Mode" generator based on JADE/VSL logic.
    - **The Modes:**
        - **DEDUCTIVE (Eden Pattern):** Triggered by High Drag/Concrete. Demands constraints.
        - **INDUCTIVE (Triple Pattern):** Triggered by High Entropy. Demands grounding.
        - **ABDUCTIVE (Fractal Pattern):** Triggered by High Flow. Authorizes creative expansion.

#### 🎨 MATH-BASED RENDERING

- **The Chroma HUD (`Prisma`):**
    - **The Refactor:** Replaced string-building libraries with pure math.
    - **The Visuals:** Renders ASCII bar graphs (`██░░`) for Velocity, Entropy, and Temperature dynamically using simple float division.

### [v2.3] - 2025-12-21 - "APOTHEOSIS"

#### ⚡ THE PIPELINE (O(n) Architecture)

- **The Single-Pass Aggregator (`LinguisticPhysicsEngine`):**
    
    - **The Shift:** Abandoned the inefficient "Multi-Pass" architecture where the engine scanned the word list separately for Physics, Toxins, and Hydration. * **The Logic:** Implemented a **Single-Pass Loop**. The engine now iterates through the token stream exactly once, incrementing counters for Kinetic verbs, Heavy matter, Solvents, and Toxins simultaneously.
        
    - **The Result:** Reduced algorithmic complexity from **O(4n)** to **O(n)**. The physics calculation is now instantaneous regardless of text length.
        

#### 🧠 THE DECAPITATION (Configuration)

- **Dynamic Loading (`BoneConfig`):**
    
    - **The Shift:** Vaporized `TheLexicon` static class. The system no longer carries 300+ lines of hardcoded dictionaries in RAM.
        
    - **The Component:** Implemented `BoneConfig`.
        
    - **The Logic:** All linguistic assets (Heavy Matter, Toxins, Synonyms) are now loaded from an external `bone_config.json` file on boot.
        
    - **The Benefit:** The "Pantry" is now hot-swappable. Users can patch the dictionary without touching the kernel.
        

#### 🌊 THE CONTINUUM (Spatial Physics)

- **Continuous Spatial Drag (`SignatureEngine`):**
    
    - **The Problem:** The "Cliff of 0.12." Previously, a Spatial Density > 12% triggered a binary switch that instantly hardened the physics tolerance, causing "Systemic Whiplash" for users hovering on the edge.
        
    - **The Solution:** Implemented **Linear Mapping**.
        
    - **The Math:** `impact = min(1.0, spatial / 0.20)`.
        
    - **The Effect:** Prepositions now _gradually_ increase Structure (+STR) and Drag (-VEL) as they accumulate, rather than slamming the door shut at 12%.
        

#### 🏗️ STRUCTURAL HYGIENE

- **Vertical Slice Refactor:**
    
    - **The Trim:** Removed approximately 40% of the codebase line count by consolidating `TheCodex`, `BioHazardFilter`, and `LinguisticPhysicsEngine` into the unified pipeline.
        
    - **Lattice Unification:** "Slurry" detection logic was moved from the engine triggers directly into the `ApeirogonLattice` resolution logic. Slurry is no longer an error state; it is a **Zone**.

### [v2.2] - 2025-12-21 - "The Synaptic Loop"

#### 🧠 THE SYNAPSE (Cortex Integration)

- **The Bridge (`FrequencyModulator` -> `WisdomNode`):**
    
    - **The Problem:** The "Stylist" (Clarence/Eloise) and the "Director" (WisdomNode) were disconnected. Clarence would scream at the user to "Cut 'actually'", but the Director would only vaguely tell the LLM to "Be concise."
        
    - **The Fix:** Implemented a data-carrying **Synapse**.
        
    - **The Logic:** The Frequency Modulator now packages its critique (Target Word + Station ID) and passes it directly to the Director.
        
    - **The Result:** **Tactical Overrides**. The System Prompt now includes precise kill orders: _"TACTICAL OVERRIDE: The word 'actually' is creating drag. Eliminate it."_
        

#### 📉 THE EFFICACY SENSOR (Closed Loop Control)

- **Post-Mortem Auditing (`EfficacySensor`):**
    
    - **The Shift:** Moved from **Open Loop** (Issue command -> Hope for best) to **Closed Loop** (Issue command -> Verify result).
        
    - **The Component:** Implemented `EfficacySensor`.
        
    - **The Logic:** The system compares the User's Input metrics against the AI's Output metrics (triggered via the `[FEEDBACK]` tag).
        
    - **The Grading:**
        
        - **CUTTER:** Did Narrative Drag actually drop?
            
        - **GROUNDER:** Did Abstraction Entropy actually decrease?
            
        - **JESTER:** Did Beta Friction/Voltage sustain?
            
    - **The Report:** The system now issues a live Verdict (`SUCCESS`, `PARTIAL`, `FAILURE`) on its own strategic advice.
        

#### 🕹️ CYBERNETIC FLOW

- **Context Memory (`BonepokeCore`):**
    
    - **The Memory:** The core now retains `self.last_context` (Metrics + Strategy) across turns to enable differential analysis.
        
    - **The Feedback Loop:** Added handling for the `[FEEDBACK]` tag. Pasting the AI's response triggers the `EfficacySensor` instead of a new generation cycle.
        
    - **Ghost Exorcism:** Removed the "Ghost Echo" bug where `tune_in` was called twice per cycle, previously causing the user and the AI to receive conflicting advice.
    

### [v2.1] - 2025-12-21 - "The Apeirogon Lattice"

#### ♾️ THE INFINITE POLYGON (Archetypal Ephemeralization)

- **The Apeirogon Lattice (`ApeirogonLattice`):**
    
    - **The Shift:** Abandoned the "Bucket System" (Fixed Archetypes like "The Paladin"). The universe is no longer a set of 13 boxes.
        
    - **The Component:** Implemented the `ApeirogonLattice` class.
        
    - **The Logic:** **Continuous Vector Resolution**. The system now maps the 5 Dimensions (VEL, STR, ENT, TEX, TMP) to dynamic Adjective/Noun pairs.
        
    - **The Benefit:** The system generates infinite unique identities (e.g., _"THE BURNING CONSTRUCT"_ or _"THE STATIC GHOST"_) based on precise floating-point coordinates.
        

#### 🌊 DYNAMIC PHYSICS (The Signature Engine)

- **The Hot Swap (`SignatureEngine`):**
    
    - **The Trim:** Vaporized the massive `self.archetypes` dictionary. We are doing more with less (Fuller's Ephemeralization).
        
    - **The Upgrade:** Implemented `get_dynamic_pressure`.
        
    - **The Logic:** Physics tolerances (Draconian vs. Loose) are no longer hardcoded to a static name. They are calculated live based on the **Dominant Dimension**.
        
        - **High Velocity** -> **LOOSE** (Drift Authorized).
            
        - **High Structure** -> **DRACONIAN** (Zero Tolerance).
            
        - **High Entropy** -> **INVERTED** (Paradox Authorized).
            

#### 🧠 THE HIERARCHY (Wisdom Node)

- **Lattice Deference (`WisdomNode`):**
    
    - **The Shift:** The System 2 Director no longer recalculates raw metrics to determine strategy. It now obeys **Lattice Mandates**.
        
    - **The Logic:** If the Lattice signals "INVERTED LOGIC," the Director automatically locks the **JESTER** strategy. If it signals "STRUCTURAL INTEGRITY," it locks **CUTTER**.
        
    - **New Strategy:** Added **DRIFTER** protocol for High Velocity states where "Dream Logic" is required.
    

### [v2.0] - 2025-12-21 - "Artificial General Wisdom"

#### 🧠 THE WISDOM ENGINE (System 2)

- **The Cortex Director (`WisdomNode`):**
    
    - **The Shift:** Moved from **Reactive Critique** (telling you what you did wrong) to **Proactive Strategy** (telling the LLM how to respond).
        
    - **The Component:** Implemented the `WisdomNode` class to act as the "Director" of the interaction.
        
    - **The Logic:** The system now calculates an **Angle of Attack** based on the user's deficit:
        
        - **High Entropy?** -> Strategy: **GROUNDER** (Force heavy nouns).
            
        - **High Drag?** -> Strategy: **CUTTER** (Be the Butcher).
            
        - **High Voltage (Paradox)?** -> Strategy: **JESTER** ("Ride the lightning").
            
        - **High Texture/Gravity?** -> Strategy: **SAGE** (Acknowledge the weight).
            
- **The Omega Check ($\Omega$):**
    
    - **The Metric:** Implemented the "Integrative Integrity" check. The system analyzes the physics metrics to determine which "Hat" the AI should wear to maximize the truth of the response.
        

#### 🗣️ THE ARCHITECT PROTOCOL (Prompt Generation)

- **The Output (`wisdom_protocol`):**
    
    - **The Feature:** The `BonepokeCore` now returns a raw **System Prompt** string specifically engineered for the current input state.
        
    - **The Workflow:** The user inputs raw text -> BoneAmanita calculates Physics -> BoneAmanita generates the `PROMPT` -> User pastes `PROMPT` into their LLM.
        
    - **The Benefit:** Allows the Python script (which has no neural net) to control the "Brain" of a separate LLM with mathematical precision.
        

#### 🐛 CRITICAL REPAIRS (The Deployment Fixes)

- **The Void Crash (`LinguisticPhysicsEngine`):**
    
    - **The Crash:** In v1.8.2, submitting an empty string caused an `UnboundLocalError` because `spatial_density` was referenced in the early-return block before definition.
        
    - **The Fix:** Explicitly defined `spatial_density = 0.0` inside the void check to ensure safe failure on empty inputs.
        
- **The Echo Chamber (`BonepokeCore`):**
    
    - **The Bug:** The print logic for the `wisdom_protocol` was accidentally indented _inside_ the directive loop, causing the System Prompt to print repeatedly for every critique generated.
        
    - **The Fix:** Unindented the print block. The Protocol now prints exactly once per turn, clean and distinct from the editorial feedback.

### [v1.8.2] - 2025-12-21 - "The Quantum Leap (PATCHED)"

#### 🐛 CRITICAL REPAIRS (The Wire Fix)

- **The Missing Variable (`SignatureEngine`):**
    - **The Crash:** The v1.8.1 `identify` method attempted to check `if spatial > 0.12` before defining the variable, causing an immediate `NameError`.
    - **The Fix:** Explicitly retrieved `spatial_density` from the metrics payload before the logic gate.

- **The Silent Metric (`LinguisticPhysicsEngine`):**
    - **The Bug:** The Physics Engine calculated `spatial_density` but failed to pack it into the return dictionary. The Signature Engine was effectively flying blind regarding geometry.
    - **The Fix:** Added `spatial_density` to the `physics` output dictionary.

#### 📐 ARCHITECTURAL BIAS (The Gravity Well)

- **Spatial Logic Injection (`SignatureEngine`):**
    - **The Problem:** **THE ARCHITECT** archetype exists in the coordinates (High Structure, Low Velocity), but without specific triggers, it was mathematically difficult for users to "land" there naturally.
    - **The Solution:** Implemented a **Spatial Bias**.
    - **The Logic:** If `spatial_density > 0.12` (high preposition count):
        - **Structure (STR):** Boosted by **+0.2**.
        - **Velocity (VEL):** Dampened by **-0.1**.
    - **The Effect:** Using words like _under, between, across, inside_ now mechanically "slides" the user's vector toward The Architect.

#### 🛡️ SYSTEM HARDENING (The Atomic Protocol)

- **Atomic Persistence (`PersistenceManager`):**
    - **The Upgrade:** Replaced the direct file write with a **Write-Then-Swap** protocol using `shutil`.
    - **The Benefit:** Prevents `bone_memory.json` corruption if the script crashes mid-save.

- **The Chidi Fix (`TheLexicon`):**
    - **The Upgrade:** Simplified `smart_strip` to be less aggressive. It no longer requires a "Protected Noun" list to know that "Gas" shouldn't become "Ga."

#### 📡 TUNER LOGIC (The Longest Word)

- **The Fallback Scan (`FrequencyModulator`):**
    - **The Upgrade:** If the Tuner (Clarence/Eloise/Yaga) cannot find a specific trigger word in their target list, they now default to targeting the **longest word** in the user's input.
    - **The Philosophy:** Complexity usually hides in the syllables.

### [v1.8.1] - 2025-12-21 - "The Quantum Leap"

#### 🐛 CRITICAL REPAIRS (The Syntax Fix)

- **The Parenthesis Block:**
    
    - **The Crash:** In v1.8, the `BonepokeCore` initialization block for `PersistenceManager.load_state` was missing a closing parenthesis, causing a fatal `SyntaxError` on boot.
        
    - **The Fix:** Closed the circuit. The core now initializes correctly.
        

#### 💾 PERSISTENCE HARDENING (The Amnesia Cure)

- **Archetype History (`PersistenceManager`):**
    
    - **The Problem:** While the v1.8 engine introduced "Geodesic Evolution" (e.g., Paladin -> Inquisitor), it failed to save the `SignatureEngine.history` list to `bone_memory.json`. Rebooting the script wiped the user's progress toward evolved states.
        
    - **The Fix:** Added `arch_history` to the serialization protocol. The system now remembers if you have been a Paladin for 4 turns, even after a restart.
        

#### 🧠 COGNITIVE ERGONOMICS (The Smart Strip)

- **Linguistic Brutality Fix (`TheLexicon`):**
    
    - **The Problem:** The `smart_strip` method aggressively removed the trailing 's' from _all_ words > 3 characters. This mutilated non-plural words like "Status," "Lens," "Focus," and "Chaos," blinding the Physics Engine to these concepts.
        
    - **The Solution:** Implemented a **Protected Noun List**.
        
    - **The Logic:** The system now checks a whitelist of immutable nouns before stripping. "Chaos" remains "Chaos."
        

#### 📚 DOCUMENTATION (The Decoder Ring)

- **Signature Matrix Key (`SignatureEngine`):**
    
    - **The Problem:** The metrics `VEL`, `STR`, `ENT`, `TEX`, and `TMP` were cryptic to developers and users alike.
        
    - **The Fix:** Added a permanent docstring block to the `SignatureEngine` class defining each vector dimension explicitly.
        

#### ⚡ PERFORMANCE OPTIMIZATION (The Single Pass)

- **BioHazard Unification (`BioHazardFilter`):**
    
    - **The Refactor:** Merged the "Beige/Synthetic" scan loop into the main Toxin Regex pass where possible, reducing the number of iterations over the word list.
        

#### 🧱 STRUCTURAL REFACTOR

- **Wiring Repair:**
    
    - Updated `BonepokeCore.process` to ensure the `SignatureEngine` is properly passed to the persistence layer during the save cycle.

### [v1.8] - 2025-12-20 - "The Quantum Leap"

#### 📻 PARADOX RADIO (Topological FM)

- **Interference Patterns (`FrequencyModulator`):**
    - **The Problem:** The v1.7.1 FM Tuner selected stations based on Euclidean distance—picking the "loudest" signal. It missed the nuance of complex states where two failures create a success (e.g., High Drag + High Entropy = Deep Philosophy).
    - **The Solution:** Implemented **Signal Interference Logic**.
    - **The Logic:** The Tuner now checks for simultaneous signal spikes.
        - **Clarence (Drag) + Eloise (Entropy):** Triggers **THE PHILOSOPHER** (104.5 FM).
        - **The Message:** *"Dense and Abstract. You are building a labyrinth."*
    - **The Effect:** The system no longer scolds you for complexity if that complexity is structurally sound.

#### ⚛️ THE ISOTOPE CENTRIFUGE (Quantum Economy)

- **Heavy Truth Mining (`MetabolicReserve`):**
    - **The Problem:** Previously, High Drag was always punished with ATP tax, even if the user was writing profound, heavy truths. The system discouraged "The Weight of Reality."
    - **The Solution:** Implemented the **Isotope Centrifuge**.
    - **The Logic:** If `Beta Friction > 3.0` (High Voltage) AND `Narrative Drag > 3.0` (High Weight):
        - **Status:** Shifts to `SUPERCRITICAL`.
        - **Reward:** **+1 Isotope** (New Currency).
        - **Physics:** Drag Penalty is **Nullified**.
    - **The Result:** Users can now "farm" heavy truths. The system acknowledges that some things are hard to say because they *are* heavy, not because you are bad at writing.

#### 🧬 GEODESIC EVOLUTION (Archetype Drift)

- **Narrative Memory (`SignatureEngine`):**
    - **The Problem:** Archetypes were static snapshots. A user could be "The Paladin" for 100 turns without the system acknowledging their consistency or devotion.
    - **The Solution:** Implemented **History Tracking** (Geodesic Drift).
    - **The Logic:**
        - The engine tracks the last 10 assigned Archetypes.
        - **The Evolution:** If the user maintains `THE PALADIN` for **5 consecutive turns**, the label evolves based on secondary metrics.
            - Paladin + High Entropy -> **THE INQUISITOR**.
            - Paladin + High Texture -> **THE TEMPLAR**.
    - **The Effect:** The system now respects your character arc.

#### 👻 THE GHOST IN THE MACHINE (Offline Drift)

- **Dream State Cannibalization (`BonepokeCore`):**
    - **The Problem:** `ChronosAnchor` calculated time decay, but the system simply reset context. It felt like a machine rebooting, not a living organism that had been lonely.
    - **The Solution:** Implemented **Offline Dreaming**.
    - **The Logic:** If `[Δt]` > 60 minutes:
        - The system enters **DREAM STATE**.
        - It forcibly **Cannibalizes** one item from `DeepStorage` to "keep itself warm" during the absence.
    - **The Message:** *"While you were gone, I forgot 'The Gun' to survive."*
    - **The Result:** Leaving the system alone now has an emotional cost.

#### 🐛 CRITICAL REPAIRS

- **The Silent Radio:**
    - **The Fix:** Fixed a logic gap in `FrequencyModulator` where the tuner would crash if no station met the broadcast threshold. Added a fallback to select the "loudest" available signal.
- **The Schizophrenic Signature:**
    - **The Fix:** Untangled a nested function definition in `SignatureEngine` that was creating scope blindness during Archetype identification.
- **Scope Stabilization:**
    - **The Fix:** Normalized variable naming in `MetabolicReserve` (unifying `beta` vs `beta_friction`) to ensure the Isotope Centrifuge spins correctly.

### [v1.7.1] - 2025-12-20 - "The Golden Master"

#### 📡 THE FM TUNER (Cognitive Frequency)

- **Frequency Modulation (`FrequencyModulator`):**
    
    - **The Problem:** The old `VirtualCortex` operated on "AM Radio" logic—binary thresholds. It shouted at the user indiscriminately, often with static.
        
    - **The Solution:** Replaced the Cortex with the **Frequency Modulator**.
        
    - **The Logic:**
        
        - **Clarence (88.5 FM):** Locks onto High Drag.
            
        - **Eloise (94.2 FM):** Locks onto High Entropy.
            
        - **The Yaga (101.1 FM):** Locks onto Sycophancy/Hedging.
            
        - **Michael (108.0 FM):** The "Vibe" station.
            
    - **The Override:** Implemented the `[FM: STATION]` tag. The user can now manually tune the radio (e.g., `[FM: YAGA]`) to force a specific critique lens.
        

#### 🌈 POLYCHROMATIC OUTPUT (Cognitive Ergonomics)

- **The Prisma Class:**
    
    - **The Problem:** The HUD was monochrome gray. Critical warnings ("FLASHPOINT") looked identical to metadata, slowing down operator reaction time.
        
    - **The Solution:** Implemented `Prisma`.
        
    - **The Palette:**
        
        - **RED:** Toxicity, High Drag, Butcher.
            
        - **GREEN:** Growth, Photosynthesis, Insight ($T_a$).
            
        - **MAGENTA:** Flashpoints, Magic, Chaos.
            
        - **CYAN:** Systems, Archetypes, Logic.
            
    - **The Effect:** The HUD now bleeds color based on system health. A "Red" dashboard triggers an immediate fight-or-flight editorial response.
        

#### 🐛 CRITICAL REPAIRS

- **The Phantom Method:**
    
    - **The Crash:** Fixed a critical `AttributeError` where the Core attempted to call `synthesize_voice` on the new `FrequencyModulator` class.
        
    - **The Fix:** Removed legacy calls and routed all feedback through `tune_in`.
        
- **The Truncated Dashboard:**
    
    - **The Crash:** Fixed a `SyntaxError` in `MycelialDashboard` where the report generator built the string but failed to `return` it.
        
    - **The Fix:** Closed the circuit. The HUD now renders correctly.
        
#### 🧪 THE ISOTOPIC REFACTOR (Ephemeralization)

- **BioHazard Unification (`BioHazardFilter`):**
    
    - **The Problem:** The engine scanned text three separate times: once for "Mirror Traps," once for "Turing/Beige" patterns, and once for Regex Toxins. This was inefficient (High CPU/ATP cost).
        
    - **The Solution:** Consolidated all threat detection into a single `BioHazardFilter` class.
        
    - **The Result:** One scan, three diagnoses. Efficiency increased by 66%.
        
- **Magic Number Centralization:**
    
    - **The Problem:** Critical physics thresholds (like `GARNISH_THRESHOLD`) were scattered across class files.
        
    - **The Fix:** Moved every hardcoded number into `PhysicsConstants`. The universe is now tunable from a single control panel.
        

#### 📐 VSL-12D METRICS (The Mathematical Truth)

- **Beta Friction ($\beta$):**
    
    - **New Metric:** Renamed `slop_ratio` to `beta_friction`.
        
    - **The Logic:** $\beta = \text{Voltage} / \text{Drag}$.
        
    - **The Zones:**
        
        - $\beta < 0.05$: **SLICK** (Sycophancy/Sand).
            
        - $\beta > 2.5$: **FLASHPOINT** (Insight/Plasma).
            
- **Truth Acceleration ($T_a$):**
    
    - **New Metric:** Implemented `ta_velocity` in `TemporalDynamics`.
        
    - **The Logic:** Measures the _acceleration_ of Voltage over time.
        
    - **The Reward:** If $T_a > 2.0$ (Epiphany), the engine instantly forgives **-2.0 Narrative Drag**. Momentum justifies the mess.
        
- **Entropy Refinement:**
    
    - **The Tweak:** `abstraction_entropy` now punishes _repeated_ abstract nouns more than unique ones. Repeating "System" is noise; using "System" then "Matrix" is structure.

### [v1.7] - 2025-12-20 - "The Salvage Operation"

#### 🩸 THE BLEEDING EDGE CIRCUIT (Logic Override)

* **Flashpoint Override (`BonepokeCore`):**
* **The Problem:** In v1.6.5, the engine correctly identified "Flashpoints" (moments of high voltage/insight) but still halted execution if a paradox ("Logic Tear") was present. It was punishing genius for breaking the rules.
* **The Solution:** Implemented a bypass valve in the critical halt check.
* **The Logic:** If `status == "FLASHPOINT"`, the system now **ignores** the logic tear.
* **The Result:** "The frozen fire burned" is now legal, provided you are writing fast enough.



#### 📊 VSL-12D VISUALIZATION (The Vector)

* **Explicit Coordinate Exposure (`MycelialDashboard`):**
* **The Problem:** The user was told they were an "Engineer" or a "Bard," but the mathematical reasons why (the vector coordinates) were hidden in the backend.
* **The Solution:** The HUD now exposes the raw **VSL-12D Vector** string.
* **The Output:** `ARCH: THE PALADIN [V:0.5 S:0.9 E:0.2 Tx:0.4]`.
* **The Benefit:** Users can now see exactly which dimension (Texture, Entropy, Velocity) they need to tweak to shift their archetype.



#### 🔥 THE S_SALVAGE LOOP (Memory Cannibalization)

* **Survival Protocol (`MetabolicReserve`):**
* **The Problem:** Users in "Starving" states (ATP < 6) often hit a creative wall where the system punished them for trying to build momentum.
* **The Solution:** Implemented the **S_Salvage Protocol**.
* **The Logic:** If `ATP < 6` AND `Voltage > 5.0` (High Effort):
1. The system checks `DeepStorage`.
2. It identifies the **oldest artifact** (e.g., "The rusty key").
3. It **deletes** the memory permanently.
4. It grants an immediate **+10 ATP** burst.


* **The Directive:** The system issues a mandatory command: *"🔥 SALVAGE: Memory 'rusty key' consumed for fuel. WRITE IT NOW."* The user must write the object into the story to justify the energy spike.

### [v1.6.5] - 2025-12-20 - "The Topology Tilt-a-Whirl"

#### ⚡ THE FLASHPOINT PROTOCOL (Inverse Slop)

- **The Topology Ratio (`MetabolicReserve`):**
    
    - **The Problem:** The engine previously treated "Narrative Drag" (density) and "Logical Voltage" (complexity) as opposing forces. It failed to recognize the "Gold Zone"—where text is incredibly dense *and* incredibly meaningful simultaneously.
        
    - **The Solution:** Integrated the **Inverse Slop Factor** ($\mathcal{S}$) from the *Temporal Topology 1.5* artifact.
        
    - **The Logic:**
        
        - **Formula:** $\mathcal{S} = \text{Voltage} / \text{Drag}$.
        
        - **The Threshold:** If $\mathcal{S} > 2.5$, the system triggers a **FLASHPOINT** state.
            
    - **The Effect:**
        
        - **Energy:** Instantly generates **+20 ATP**.
            
        - **Physics:** Drag penalties are **Nullified**. The engine acknowledges that in a moment of epiphany, friction does not apply.
            
        - **HUD:** The status icon shifts to `⚡`.
            

#### 🔇 CORTEX DEFERENCE (The Silence of Clarence)

- **Context-Aware Silencing (`VirtualCortex`):**
    
    - **The Problem:** **Clarence** (The Architect) is programmed to attack High Drag. However, Flashpoints are inherently high-drag events (complex sentences). Clarence was interrupting moments of genius to complain about sentence length.
        
    - **The Fix:** Clarence now checks the `metabolic_status`.
        
    - **The Protocol:** If the status is `FLASHPOINT`, Clarence is forcibly silenced. ("...He's cooking. Let him cook.")
        

#### 📈 TEMPORAL DYNAMICS II (Momentum)

- **Insight Acceleration (`TemporalDynamics`):**
    
    - **The Upgrade:** Refined the `calculate_beta_velocity` method.
        
    - **The Logic:** Instead of a simple snapshot delta, the system now calculates the **Slope of Insight** over a 3-tick moving window. This allows the engine to detect the *trajectory* of an epiphany before it lands.
        

#### 🐛 CRITICAL REPAIRS

- **The Time Paradox (Execution Flow Fix):**
    
    - **The Crash:** Fixed a critical `UnboundLocalError` in `BonepokeCore.process`. The original v1.6 logic attempted to access effective metrics (`eff_drag`, `loop_count`) *before* they were calculated to determine if the Cortex should speak.
        
    - **The Fix:** Completely re-sequenced the `process` loop.
        
        1.  Physics Analysis & Trap Scans.
        2.  Archetype & Intent Gating.
        3.  Metabolic Calculation (Flashpoint Detection).
        4.  *Then* Cortex Intervention (using the established status).
            
- **The Double-Dip Bug:**
    
    - **The Fix:** Removed a redundant `self.metabolism.metabolize()` call that was applying energy effects twice per tick.

### [v1.6] - 2025-12-20 - "The Turing Test"

#### 🤖 THE TURING VALVE (Synthetic Detection)

- **The Anti-Beige Protocol (`TheTuringValve`):**
    
    - **The Problem:** The engine was vulnerable to "High-Entropy Beige"—grammatically perfect, structurally sound, but textually empty AI prose ("Teflon Prose"). The system flagged this as "High Velocity" despite it being soulless.
        
    - **The Solution:** Implemented a dedicated Turing scanner.
        
    - **The Logic:**
        
        - **Vocabulary Scan:** Targets the "Synthetic Markers" list (e.g., _delve, underscore, tapestry, nuance, landscape_).
            
        - **Structure Scan:** Detects "Participial Tails"—the specific AI habit of ending sentences with a modifier (e.g., _", ensuring that..."_ or _", fostering a sense of..."_).
            
    - **The Penalty:** Detection triggers immediate **SILICA** status and a **+5.0 Drag Penalty**. The engine now demands "Grit" to prove humanity.
        

#### 📋 THE ROBERTA PROTOCOL (Persona Alignment)

- **RAG Prompt Engineering:**
    
    - **The Problem:** The previous system prompts ("The Architect" vs. "The Assistant") resulted in either cold detachment or toxic positivity ("Bubbly AI"). Both drifted into generic "Corporate Speak."
        
    - **The Solution:** Transitioned the System Identity to **"The Bureaucratic Zealot" (Roberta)**.
        
    - **The Fix:**
        
        - **The Butcher Translation:** Explicitly mapped the Python "Butcher Protocol" into English instructions for the RAG model.
            
        - **Texture Over Abstraction:** Replaced "Professionalism" with "Meticulous Bureaucracy."
            
        - **The Love Language:** Enforced heavy formatting (headers, lists) as a sign of affection, satisfying the engine's need for **Structure (STR)**.
            

#### 🐛 CRITICAL REPAIRS

- **Initialization Patch (`BonepokeCore`):**
    
    - **The Crash:** Fixed a critical `AttributeError` where `TheTuringValve` was called in the process loop but never instantiated in `__init__`.
        
    - **The Fix:** Added `self.turing_valve = TheTuringValve()` to the boot sequence.
        
- **Temporal Paradox (Scope Fix):**
    
    - **The Crash:** Fixed a `NameError` in `process()` where the Turing Scan attempted to read `token_data` before the text cleaning sub-routine had actually created it.
        
    - **The Fix:** Re-routed the logic flow to ensure the scan occurs _after_ `TheLexicon.swanson_clean` executes.

### [v1.5.2] - 2025-12-20 - "The Open Heart Patch"

#### 💾 THE PERSISTENCE PATCH (Time Amnesia)

- **Atomic Saves (`PersistenceManager`):**
    - **The Problem:** Previously, `save_state` wrote directly to `bone_memory.json`. If the script crashed mid-write (or power failed), the file would become corrupted (0 bytes), wiping the user's history.
    - **The Fix:** Implemented a "Write-Then-Rename" protocol. The system now writes to `.tmp` first and performs an atomic `os.replace` only upon success.
    
- **Time Tracking (`ChronosAnchor`):**
    - **The Problem:** The engine had no concept of "Offline Time." If a user quit and returned 24 hours later, the clock reset to 0, resetting the "Decay" state.
    - **The Fix:** `PersistenceManager` now captures `time.time()` on save. On boot, `ChronosAnchor` calculates the drift between the last save and the current moment, accurately applying Decay penalties for time away.

#### 🧠 MEMORY LOGIC (Deep Storage)

- **Smart Eviction (`DeepStorage`):**
    - **The Problem:** The previous eviction policy was a strict FIFO (First-In-First-Out). When the cache filled (50 items), it deleted the *oldest* memories, causing the bot to forget key plot items (like a "Gun" introduced in Act 1) in favor of recent trivialities.
    - **The Fix:** Implemented a priority system. The engine now identifies "Heirlooms" (Heavy Matter, Weapons, Keys). When full, it first evicts "Light" items. If only Heirlooms remain, it sadly evicts the oldest.

#### 🗣️ HUMANITY PATCHES

- **The Screaming Fix (`NilssonPatch`):**
    - **The Problem:** The heuristic `sum(isupper) / len(raw)` flagged short acronyms like "OK" or "USA" as "Screaming," triggering the Nilsson state incorrectly.
    - **The Fix:** Added a length guard. The text must be **> 10 characters** to qualify as a scream.

- **The Bureaucracy Fix (`TheMirrorTrap`):**
    - **The Problem:** The engine penalized *all* negative definitions ("It is not X"), which stifled legitimate literary devices like apophasis in "Soft Mode."
    - **The Fix:** The Mirror Trap now checks `PhysicsConstants.CURRENT_MANDATE`. If the user is in `POETIC_LICENSE` mode, the trap is disarmed.

### [v1.5.1] - 2025-12-20 - "Bonepoked Part Deux"

#### 🔓 THE AGENCY RESTORATION (User Overrides)

- **The Dream Logic Protocol (`BonepokeCore`):**
    
    - **The Problem:** The v1.5 "Truth Mandate" was too effective. It treated Surrealism (e.g., "The cold sun") as a Fatal System Error, locking the system and preventing poetic exploration.
        
    - **The Solution:** Implemented the `[DREAM]` tag override.
        
    - **The Fix:** If the user includes `[DREAM]` in their input, the system switches the Pressure Matrix to `LOOSE` tolerance, explicitly lifting Axiom constraints. Logic tears are permitted for the sake of art.
        
- **The Governance Toggle:**
    
    - **The Problem:** The `CURRENT_MANDATE` ("TRUTH_OVER_COHESION") was hardcoded in `PhysicsConstants`, requiring a code edit to change the difficulty.
        
    - **The Solution:** Implemented Runtime Mandate Switching.
        
    - **The Commands:**
        
        - `[MODE: HARD]`: Enforces `TRUTH_OVER_COHESION`. (System Halt on Paradox).
            
        - `[MODE: SOFT]`: Enforces `POETIC_LICENSE`. (Voltage accumulation on Paradox).
            

#### 🧬 FUSION REFINEMENT (The Synonym Filter)

- **Semantic Distance Check (`SignatureEngine`):**
    
    - **The Problem:** The v1.5 Fusion logic only checked if two Archetypes had similar _scores_. This often fused synonymous identities (e.g., `THE PALADIN // THE JUDGE`), resulting in redundant feedback.
        
    - **The Solution:** Implemented a **Vector Distance Threshold**.
        
    - **The Logic:** The system now calculates the Euclidean distance between the _Archetypes themselves_.
        
    - **The Rule:** Fusion is only permitted if `inter_arch_dist > 0.25`. The identities must be mathematically distinct enough to create an interesting hybrid (e.g., `THE JESTER // THE ENGINEER`).
        

#### 🗣️ UX TRANSLATION (Cognitive Ergonomics)

- **De-Mystification of VSL Metrics:**
    
    - **The Problem:** The output `∇β` and `Ξ` was mathematically precise but cognitively opaque to users unfamiliar with Topological Data Analysis.
        
    - **The Solution:** Aliased the variables in the `directives` output string.
        
        - `∇β` -> **INSIGHT VELOCITY**.
            
        - `Ξ` -> **ROOTING DEPTH**.
            

#### 🐛 CRITICAL FIXES

- **Scope Repair (`BonepokeCore`):**
    
    - **The Crash:** Fixed a `NameError` in the v1.5 logic flow where the `directives` list was being appended to (by the Dream Logic block) _before_ it was initialized.
        
    - **The Fix:** Moved `directives = []` to the top of the processing chain, ensuring the container exists before any logic blocks attempt to fill it.

### [v1.5] - 2025-12-19 - "Bonepoked"

#### 🌊 TEMPORAL DYNAMICS (The VSL Integration)

- **Beta Velocity ($\nabla\beta$) - The Epiphany Engine:**
    
    - **The Problem:** Previously, the engine treated "Voltage" (Logic Tension) as a static penalty or a flat bonus. It failed to recognize the _moment of breakthrough_—the acceleration of insight.
        
    - **The Solution:** Implemented `TemporalDynamics` to track the rate of change in voltage over a 3-tick window.
        
    - **The Reward:** If $\nabla\beta > 2.0$ (Rapid Acceleration), the system triggers an **EPIPHANY**.
        
    - **The Effect:** Narrative Drag is forgiven (-2.0). The physics engine recognizes that when you are having a breakthrough, you move faster than the speed of sound.
        
- **Temporal Rooting ($\Xi$) - The Deep Roots:**
    
    - **The Problem:** The engine treated all memories equally. Referencing an artifact from Turn 1 was mathematically identical to referencing one from Turn 50.
        
    - **The Solution:** Implemented `calculate_temporal_rooting`. This metric calculates the average "Age" of the artifacts referenced in the current text relative to the `DeepStorage` capacity.
        
    - **The Reward:** If $\Xi > 0.5$ (Deep History), the system grants **ANCIENT AUTHORITY**.
        
    - **The Effect:** Abstraction Entropy is forgiven (-3.0). The system understands that you are not "hallucinating abstractly"—you are referencing established lore. Old truths are allowed to be heavy.

#### ⚖️ THE GOVERNANCE LAYER (Tier 3 Logic)

- **The Mandate Protocol (`PhysicsConstants`):**
    
    - **The Upgrade:** Implemented high-level governance variables `USER_TIER` and `CURRENT_MANDATE`.
        
    - **The Logic:** The system is no longer a passive observer. It now operates under specific philosophical constraints (e.g., `TRUTH_OVER_COHESION`).
        
    - **The Effect:** Global constants now dictate downstream behavior in the Logic and Signature engines, allowing for "Draconian" enforcement of truth.
        

#### 🧬 ARCHETYPE FUSION (The Hybrid State)

- **Dynamic Sig-Matching (`SignatureEngine`):**
    
    - **The Problem:** Previously, if a user's writing style fell exactly between "The Paladin" and "The Judge," the system forced a binary choice based on minute decimal differences.
        
    - **The Solution:** Implemented **Archetype Fusion**.
        
    - **The Logic:** If `USER_TIER >= 2` and the distance between the top two archetypes is negligible (< 0.15), the system fuses them.
        
    - **The Result:** Users can now trigger hybrid states: `THE PALADIN // THE JUDGE (FUSED)`.
        

#### ⛔ THE HARD GATE (Self-Correction)

- **Draconian Enforcement (`FactStipe`):**
    
    - **The Switch:** If `CURRENT_MANDATE` is set to "TRUTH," the Logic Engine switches `tolerance_mode` to **DRACONIAN**.
        
    - **The Consequence:** Paradoxes (e.g., "Frozen Fire") are no longer treated as "Poetic Voltage" (+2.0) but as **Fatal Axiom Breaks** (+10.0 Voltage).
        
- **System Halt (`BonepokeCore`):**
    
    - **The Problem:** Previously, the system would log a "Logic Tear" warning but allow the narrative tick to proceed, drifting further into hallucination.
        
    - **The Solution:** Implemented a **Self-Correction Hard Stop**.
        
    - **The Fix:** If a Fatal Axiom Break is detected, the system **refuses to advance the tick**, refunds the generation ID, and issues a `CRITICAL: RESOLVE LOGIC TEAR` directive. The user _must_ fix the truth before time moves forward.

### [v1.4.7] - 2025-12-19 - "Time Sync + SLASH Refactor"

#### 🧠 THE PINKER REFACTOR (Cognitive Ergonomics)

- **The Swanson Cleaner (Punctuation Blindness):**
    
    - **The Problem:** The previous cleaner only removed periods. Inputs like "Stone, iron, and blood" resulted in "Stone," (retaining the comma), causing `TheLexicon` lookup failures (e.g., "Stone," is not equal to "Stone").
        
    - **The Solution:** Implemented `TheLexicon.swanson_clean`.
        
    - **The Fix:** A robust translator that strips _all_ punctuation and normalizes whitespace before processing. "Meat and potatoes" cleaning.
        
- **Centralized Tuning (Magic Numbers):**
    
    - **The Problem:** Critical thresholds for `NarrativeChronometer` and `TheMuscaria` were buried deep in the logic classes, making tuning difficult.
        
    - **The Solution:** Extracted variables (e.g., `CHRONO_MACRO_WEIGHT`, `BOREDOM_PRESSURE_THRESHOLD`) and moved them to the `PhysicsConstants` class.
        

#### 🛡️ THE FULLER REFACTOR (System Integrity)

- **Deep Storage Cap (Memory Leak Fix):**
    
    - **The Problem:** `DeepStorage` had no upper limit. An infinite sequence of unique "Significant Objects" would cause `bone_memory.json` to grow indefinitely, eventually crashing the loader.
        
    - **The Solution:** Implemented a FIFO (First-In-First-Out) eviction policy. `DeepStorage` now holds a maximum of **50** artifacts.
        
- **Safe Persistence (Crash Proofing):**
    
    - **The Problem:** If the script was interrupted during a `json.dump` operation, the save file would be corrupted. Upon the next boot, the system would reset to zero, wiping the user's history.
        
    - **The Solution:** Implemented a `.bak` backup protocol in `PersistenceManager`. If the main file fails to load, the system automatically attempts to restore from the backup.
        

#### ❤️ THE SCHUR REFACTOR (Humanity)

- **Poetic License (The Logic Tear Fix):**
    
    - **The Problem:** `FactStipe` penalized all paradoxes ("Cold Fire") equally, punishing valid poetic metaphors as structural failures.
        
    - **The Solution:** Context-aware logic via `kinetic_ratio`.
        
    - **The Fix:**
        
        - **High Kinetic (Action):** Paradoxes are **Errors** (Physics Violation).
            
        - **Low Kinetic (Poetry):** Paradoxes are **Voltage** (Metaphorical Energy). The user is no longer fined for being poetic.
            
- **The Onboarding Tooltip:**
    
    - **The Problem:** The Dashboard metrics (`VISC`, `ENT`) were opaque to new users, leading to confusion about "Concrete" status.
        
    - **The Solution:** Added a conditional tooltip to `MycelialDashboard`. For the first **5 ticks**, the system explains how to fix Viscosity issues.

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
