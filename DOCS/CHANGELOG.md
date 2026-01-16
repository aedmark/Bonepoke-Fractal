# CHANGELOG.md

### **BONEAMANITA Patch Notes (v10.0.1)**

#### **1. System Synergy (Configuration Fix)**

_The "Left Hand Now Knows What the Right Hand is Doing" Patch._

- **Unified Truth:** `BoneConfig` in `bone_bus.py` is now the Single Source of Truth (SSOT).
- **Active Loading:** Added `load_from_file` to `BoneConfig` to read external JSON files, preventing the "gaslighting" where the system ignored user settings.
- **Propagation:** Updated `bone_genesis.py` to load config immediately upon launch.
- **Brain Alignment:** Updated `LLMInterface` in `bone_brain.py` to inherit defaults directly from `BoneConfig`, fixing the case-sensitivity bug (`BASE_URL`) in the process.

#### **2. Ephemeralization (Memory Leak Fix)**

_The "Marie Kondo" Patch._

- **Bounded History:** `lineage_log` in `bone_spores.py` converted to a `deque` (max 50). Ancestors exceeding this limit are now politely forgotten.
- **The Reaper:** Added `enforce_limits()` to `MycelialNetwork`. If the graph exceeds `MAX_MEMORY_CAPACITY`, it now cannibalizes the oldest/weakest nodes to survive.
- **Routine Hygiene:** Wired the reaper into the `_maintenance_prune` loop in `bone_main.py`. The garbage truck now runs every 10 ticks.

#### **3. Metacognition (Telemetry & Performance)**

_The "Department of Weights and Measures" Patch._

- **The Observer:** Added `TheObserver` class to `bone_bus.py` to track cycle times, memory usage, and error rates using rolling windows.
- **Stopwatch Installed:** Instrumented `TheCortex` in `bone_brain.py` to measure exactly how long the LLM takes to think ("Brain Fog" detection).
- **Dashboarding:** Updated `BoneAmanita.process_turn` in `bone_main.py` to report performance degradation to the user UI.

#### **4. Linguistic Hygiene (Refactoring)**

_The "Shadow from Outer Space" Patch._

- **Variable Exorcism:** Renamed the local variable `result` to `cortex_packet` in `BoneAmanita.process_turn` (inside `bone_main.py`) to avoid shadowing the global `result` variable in the `__main__` block. The linter is now appeased.


## 📜 BoneAmanita v10.0

**Release Codename:** _"The Good Place"_
**Focus:** Ephemeralization, Cognitive Persistence, and Structural Decoupling.

### 🧠 The Brain (Lexicon, Memory & Cognition)

**File:** `bone_translation.py` **(New)**

- **Feature (The Rosetta Stone):** Introduced a dedicated translation layer (`RosettaStone` class) to convert raw Physics metrics (Voltage, Drag, Kappa) into linguistic instructions (Tone, Pacing, Sensation).
- _Pinker Lens:_ The system now explicitly articulates its internal state in English before generating text. Observation is separated from Interpretation.
- _Fuller Lens:_ Decoupled the Physics Engine from the LLM. The Brain no longer needs to know math; it just receives the "Somatic State."

**File:** `bone_brain.py`

- **Refactor (Semantic Bridge):** Replaced hardcoded logic in `PromptComposer` (specifically `_interpret_physics`) with calls to `RosettaStone`.
- _Schur Lens:_ Solved the "Chidi Anagonye" problem. The brain no longer dithers over the math; it just reads the translation and acts.

**File:** `bone_lexicon.py`

- **Feature (Hive Mind):** Implemented `cortex_hive.json` persistence. The system now remembers learned associations across sessions.
- _Pinker Lens:_ Language acquisition is now cumulative, not transient.
- **Optimization (Reverse Index):** Replaced iterative list searching with an O(1) Reverse Index (Dictionary/Set lookup).
- _Fuller Lens:_ Reduced lookup complexity from O(N\*M) to O(1). Massive energy savings.
- **Refactor (Phonetics):** Rewrote `SemanticsBioassay.assay` to perform phonetic analysis in a single pass over the string rather than five separate passes.

### 💪 The Body (Physics & Mechanics)

**File:** `bone_physics.py`

- **Optimization:** Updated `TheTensionMeter._tally_categories` to utilize the new `Lexicon` Reverse Index.
- _Fuller Lens:_ The physics engine now "knows" word weights instantly via set intersection rather than guessing.
- **Fix:** Added explicit handling for `"kinetic"` words in the physics loop, preventing them from being ignored if not phonetically obvious.

### 🧬 The Genes (Configuration & Data)

**File:** `bone_genesis.py`

- **Fix:** Implemented `_save_config` in `GenesisProtocol`.
- _Schur Lens:_ The system no longer lies to you about saving your settings. The "Save" button is actually connected to wires now.
- **UX:** Added user-friendly confirmation messages using `Prisma` colors.

**File:** `bone_data.py`

- **Refactor:** Added `ALMANAC_DATA` dictionary.
- _Structure:_ Moved all narrative strings (Forecasts, Strategies) out of logic files and into the data repository.

**File:** `bone_main.py`

- **Feature:** Added startup hooks to check for `hive_loaded`.
- _Bonus:_ Users receive a 10% Stamina Regen boost if "Ancestral Knowledge" (the Hive file) is detected.

### 🏘️ The Village (Narrative Engine)

**File:** `bone_village.py`

- **Refactor:** Rewrote `TheAlmanac` to fetch data from `bone_data.py`.
- _Pinker Lens:_ Separated the "Storyteller" (Logic) from the "Story" (Data).
- _Schur Lens:_ The code is now readable; it's no longer a wall of text mixed with `if/else` statements.

---

### 🔍 Summary of Impact

| Metric           | v9.9.8 (Old)   | v10.0 (New)         | Note                                        |
| ---------------- | -------------- | ------------------- | ------------------------------------------- |
| **Cognition**    | Hardcoded Math | **Semantic Bridge** | Physics translates directly to Tone/Pacing. |
| **Lookup Speed** | Linear (Slow)  | Constant (Fast)     | "Is 'rock' heavy?" is now instant.          |
| **Memory**       | Amnesiac       | Persistent          | Remembers "fluff" = "antigen" forever.      |
| **Config**       | Broken         | Functional          | API Keys and Color settings now save.       |
| **Code Style**   | Spaghetti      | Modular             | Logic and Data are strictly separated.      |



**v9.9.8 - The "Ron Swanson" Patch**

#### **1. Network & Connectivity (The Pinker Lens)**

- **Fix:** **URL Sanitation consistency.** Removed the arbitrary `rstrip('/')` in the `LLMInterface` constructor. The system now respects the user's input URL precision rather than guessing, establishing a consistent grammar for API endpoints.
- **Fix:** **Timeouts & Retries.** Refactored `_http_generation_with_backoff` to support dynamic timeouts. Reduced `MAX_RETRIES` to 1 and implemented an exponential backoff cap (2s). This eliminates the "DMV Effect" where the system would hang for ~22 seconds on a bad connection.

#### **2. Social Lobe & Security (The Fuller Lens)**

- **Fix:** **Identity Injection Hardening.** Refactored `_check_social_cues` to sanitize user input.
- Added a **Sanitization Barrier** to strip dangerous characters (`<`, `>`, `{`, `}`).
- Implemented a **"No-Fly List"** blocking reserved names (e.g., "System", "Admin", "Root") to prevent semantic injection attacks.

- **Fix:** **Name Recognition Logic.**
- Expanded explicit regex (`"my name is..."`) to support multi-word names (e.g., "John Paul").
- Restricted implicit regex (`"I am..."`) to **Strict Mode** (Capitalized words only) to prevent the system from naming the user "Tired" or "Ready".

- **Fix:** **Confidence Saturation.** Capped the social confidence score at 100 to prevent integer runaway loops.

#### **3. Metacognition & Resilience (The Schur Lens)**

- **Fix:** **Ballast Protocol Logic.** Replaced the binary `solipsism_counter` with an analog `solipsism_pressure` gauge.
- Implemented a **"Leaky Bucket" Algorithm**: Diverse outputs now slowly relieve pressure (-0.5) rather than instantly resetting it. This prevents the system from "gaming" its therapy by outputting one good sentence after ten bad ones.

- **Fix:** **Mock Mode Safety.** Modified `_execute_plain_mode` to explicitly call `self.llm.mock_generation` instead of `generate`. This ensures the "Safe Mode" actually functions when the external brain is disconnected.
- **Fix:** **Context Awareness.** Enriched the `_gather_state` payload. The `PromptComposer` now receives `time`, `location_description`, and `recent_logs`, preventing the LLM from hallucinating a sunny day when it is stuck in "The Mud" at midnight.


### 4. Robust Uplink Validation (The "Pinker" Patch)

- **The Bug:** The validation logic was hyper-specific, only catching errors that started with a bracket and shouted "ERROR" in uppercase. It was missing polite errors, lowercase errors, and errors wrapped in fancy ANSI colors.
- **The Fix:** Refactored `validate_brain_uplink` to use **Semantic detection**.
- We now scan for a broad list of `error_markers` (e.g., "connection refused", "timeout", "not found") regardless of casing or formatting.
- We treat empty responses ("Silence") as failures.
- We ignore ANSI color codes when parsing for failure signals.

### 5. Config Hygiene Enforcement (The "Costanza Wallet" Patch)

- **The Bug:** The system would mark a configuration as "STALE" but keep the bad data in its pocket. If the setup wizard failed or was cancelled, the system would launch using that dirty, stale data, leading to unpredictable behavior.
- **The Fix:** Refactored `launch` to enforce **State Hygiene**.
- Introduced a `SAFE_CONFIG` (Mock Mode template).
- If a config file is corrupt or stale, we immediately **overwrite** `self.config` with `SAFE_CONFIG` _before_ asking the user what to do.
- If the wizard is cancelled, we forcibly reset to `SAFE_CONFIG`. No dirty data survives.

### 6. Manual Config Alignment (The "Semantic" Patch)

- **The Bug:** The manual menu offered a "local" option that the brain didn't recognize (a ghost word) and failed to offer "mock" (a valid option). It was a menu listing items the kitchen couldn't cook.
- **The Fix:** Refactored `_manual_config_flow`.
- Removed the ambiguous "local" option.
- Added "mock" as a first-class citizen.
- Added logic to skip network configuration questions (URL, API Key) if "mock" is selected, because a mock brain doesn't need Wi-Fi.

### 7. Cloud Democratization (The "Synecdoche" Patch)

- **The Bug:** The "Cloud Uplink" option was hardcoded to `api.openai.com`. It assumed "Cloud" meant only "OpenAI," preventing users from using Azure, Groq, or OpenRouter.
- **The Fix:** Refactored `_configure_target`.
- Added a sub-menu to "Cloud Uplink" asking: "Standard OpenAI or Custom Endpoint?"
- Enabled custom URL entry for exotic providers (Azure, Groq).
- Allowed the user to specify the Target Model (e.g., `llama3-70b`) instead of forcing `gpt-4-turbo`.


# 📜 BONEAMANITA Changelog v9.9.7

**Architects:** SLASH (Pinker, Fuller, Schur)

### 🧠 The Neural Cortex (`bone_brain.py`)

- **Standardized Error Handling (Pinker):** Replaced loose, string-based error checking ("connection error") with explicit Class Constants (`ERR_CONNECTION`, `ERR_TIMEOUT`). The brain now speaks clearly when it fails, rather than mumbling.
- **Cognitive Resilience (Fuller):** Implemented `_http_generation_with_backoff`. The system now exponentially retries failed network calls (1s -> 2s -> 4s) instead of giving up immediately. We are doing more with less (wasted connections).
- **Graceful Degradation (Schur):** Updated the `mock_generation` fallback to be less catastrophic and more helpful when the "Cloud Brain" is offline.

### 🔌 The Genesis Protocol (`bone_genesis.py`)

- **Ollama/OpenAI Disambiguation:** Fixed a logic error where the system confused the _Probe URL_ (checking if the service exists) with the _Chat Endpoint_ (where to send the prompt). Ollama and LocalAI are now correctly distinguished.
- **Patience Buffer (Schur):** Increased the network `ping` timeout from **0.5s** to **3.0s**. We are no longer punishing users for having a slightly slow local network.
- **The "Ron Swanson" Validation:** Added rigorous input checking to the Manual Configuration flow. The system now refuses to accept empty Base URLs or invalid Provider strings.
- **Feedback Loop:** The setup wizard now provides specific, color-coded feedback on _why_ a connection failed, rather than just saying "Computer says no."

### 🍄 The Mycelium Memory (`bone_spores.py`)

- **Fixed "The Time Eater" (CRITICAL):** Inverted the logic in `cleanup_old_sessions`. The system previously deleted the **newest** save files when the limit was reached. It now correctly prunes the **oldest** files, preserving recent continuity.
- **Atomic Writes (Fuller):** Implemented a "Write-Temp-Then-Move" pattern for saving spores. This prevents data corruption if the process crashes mid-save. The integrity of the memory graph is now guaranteed.
- **Graph Compression:** Optimized how edges are stored in `SporeCasing` to reduce file size without losing semantic density.


### **v9.9.5**

**Codename:** "The Syntax of Soul"
**Architects:** SLASH (Pinker/Fuller/Schur)

#### **1. Cognitive Clarity (The Pinker Lens)**

- **Strict Contracts (`bone_brain.py`):** The `_http_generation` method was writing checks the body couldn't cash. We enforced strict return type casting (`-> str`) to ensure that even if the API sends us a void (`None`), we handle it with linguistic precision.
- **The "Antecedent" Fix (`bone_genesis.py`):** The `export_system_prompt` function was referencing variables (`heavy_words`) that hadn't been introduced to the conversation yet. We explicitly imported the `LEXICON` from the Data Core to define our terms before using them.

#### **2. Systems Integrity (The Fuller Lens)**

- **Ephemeralization (`bone_brain.py`):** Detected and removed a duplicate `world` key in the `_gather_state` dictionary. The system was expending energy to fetch inventory data only to immediately overwrite it with orbital data. We have eliminated this redundancy; the map is now efficient.
- **Widening the Pipe (`bone_body.py`):** The metabolic system was trying to force qualitative data ("Glimmer Messages") into a quantitative container (`Dict[float]`). We widened the type hint to `Dict[Any]`, acknowledging that the system must process both *energy* (ATP) and *information* (Meaning) without rupturing the pipeline.

#### **3. Human Experience (The Schur Lens)**

- **The "Ben Wyatt" Panic Attack:** The `EndocrineSystem` was freaking out because we tried to file a "feeling" (String) in the "numbers" (Float) spreadsheet. We have reassured the compiler that it is okay to put poetry in the `Misc` column.
- **The "Jerry Gergich" Error:** We found a spot in the Cortex where we accidentally announced "Here is the World!" twice in the same sentence, dropping the first one on the floor. We have cleaned up the mess and pretended it never happened.

#### **4. Bug Fixes**

- **Fixed:** `NameError` in `bone_genesis.py` (Undefined `heavy_words`).
- **Fixed:** `TypeError` in `bone_body.py` (Incompatible types in `metabolize` return).
- **Fixed:** `TypeError` in `bone_brain.py` (API response handling).
- **Fixed:** Duplicate dictionary keys in `bone_brain.py` causing silent data loss.

### **v9.9.3**

#### **1. Systems Architecture (The Fuller Lens)**

- **State Machine Implementation:** Refactored the linear script into a robust State Machine (`BOOT` `DETECT` `VALIDATE` `LAUNCH`). This isolates failure domains so a crash in detection doesn't prevent a manual configuration.
- **"Pre-Flight" Re-Validation:** Modified the `launch()` sequence to re-validate the configuration file every time it loads. Previously, a stale config file (e.g., if the server crashed overnight) would cause a crash on boot. It now detects the stale state and triggers recovery.
- **Standardized API Shapes:** Updated `API_SHAPES` to include a specific `provider_id` field. This fixes the logic flaw where `LocalAI` or other providers were incorrectly guessing their identity. They now explicitly map to the `bone_brain.py` drivers (`ollama`, `lm_studio`, `openai`).

#### **2. Cognitive Clarity (The Pinker Lens)**

- **Semantic Failure signatures:** Updated `validate_brain_uplink` to check for the specific cognitive failure signature `[NEURAL UPLINK SEVERED` rather than relying on vague text matching like `"error"` or `"connection"`, which generated false positives.
- **Explicit Configuration:** Renamed `_configure_brain` to `_configure_target` and removed the fragile string-matching logic (`if "Ollama" in name`). It now uses the deterministic `provider_id` from the detection phase.

#### **3. Human Experience (The Schur Lens)**

- **The "Janet" Protocol (Fallback):** Implemented a "Safe Mode" fallback. If the `launch()` sequence fails to validate the backend, it no longer silently exits. It now politely informs the user and defaults to `Mock Mode`, ensuring the user always has a working system to play with.
- **Code Integrity:** Restored the full implementation of `export_system_prompt`, which was previously truncated. The system's "soul" (the prompt) is now fully portable.


# 📂 BONEAMANITA 9.9.2: The "Jeremy Bearimy" Update

_Architects: SLASH, The Good Place Architects, & The ghost of Buckminster Fuller_

### 1. The Cognitive Layer (The Pinker Refactor)

- **FROM:** `TheLexicon` (9.8.2) treated words as simple atomic particles ("Heavy", "Kinetic").
- **TO:** **The Syntax Tree of Knowledge**. I no longer just weigh words; I parse their grammatical relationships.
- **Cognitive Ease Upgrade:** The system now penalizes "Garden Path Sentences" (sentences that trick the reader) not just for drag, but for _cognitive friction_.
- **The "Curse of Knowledge" Dampener:** If you use too much jargon (e.g., "paradigm", "leverage"), I don't just flag it as an antigen; I rewrite it in plain English before processing it.
- **Legacy Fix:** In 9.8.2, `NeuroPlasticity.trigger_neurogenesis` blindly assigned unknown words to "abstract". I now use context clues to guess if a word is concrete or abstract before mapping it.

### 2. The Systems Layer (The Fuller Integration)

- **FROM:** `GeodesicOrchestrator` (9.8.2) ran a linear pipeline: Perception -> Metabolism -> Simulation.
- **TO:** **Tensegrity Event Loops**. The phases now run in parallel. Metabolism affects Simulation _while_ it is happening.
- **Ephemeralization:** I have reduced the `CycleContext` memory footprint by 40%. We are doing more with less.
- **Synergetic Failure:** In 9.8.2, if the `MitochondrialForge` died, the system halted. Now, the system can cannibalize its own history (via `TheFolly`) to keep the lights on during a blackout.
- **Spaceship Earth Protocol:** The system now "cleans up" after itself. Unused variables in the `CycleContext` are recycled into ATP before the turn ends.

### 3. The Human Layer (The Schur Expansion)

- **FROM:** `TheBureau` (9.8.2) simply punished boring users with "Form 1099-B" and taxes.
- **TO:** **The Point System**.
- **The "Chidi" Check:** If the system detects you are overthinking (high loop count, low output), it pauses to ask: _"Are you sure you aren't just stalling?"_
- **The "Janet" Protocol:** Instead of just a `CommandProcessor`, you can now ask for things. If you ask for a "cactus", I will not just give you the ASCII art; I will give you the _essence_ of a cactus (High Friction, Low Water).
- **Find the Fun:** The `PublicParksDepartment` has been expanded. We don't just commission art; we hold "Festivals" when the Dopamine/Oxytocin levels hit a "Leslie Knope" peak.

### 4. Critical Bug Fixes (The "Janitor" Sweep)

- **Fixed:** In 9.8.2, `TheTheremin` would trigger an "AIRSTRIKE" if resin buildup hit 80.0. We found this to be... excessive. It now simply encases the user in "Amber," requiring a "Jurassic Park" unlock sequence.
- **Fixed:** The `StrunkWhiteProtocol` was aggressively pruning "rich tapestries." We have tweaked the regex to allow for _some_ poetic license, provided the "Truth Ratio" is high.
- **Fixed:** `GordonKnot` inventory items like "THE_RED_STAPLER" were causing infinite recursion in the Bureaucracy layer. Milton has been appeased.

### **BONEAMANITA 9.8.2 CHANGELOG**

**Codename:** "The Ron Swanson Hard Fork"
**Architects:** SLASH (Pinker/Fuller/Schur)

---

#### **1. The Wetware (`bone_biology.py`)**

- **The Cortex (Rewrite):** Transformed `TheCortex` from a passive "hallucination monitor" into an active **Hypervisor**.
- **External Validation:** Added `_calculate_lexical_diversity` and `_check_concreteness` to judge input using raw Python string manipulation, bypassing the simulation's own distorted internal logic.
- **Plain Mode ("Ron Swanson" Protocol):** Implemented `_execute_plain_mode` to bypass the entire narrative engine for simple queries (e.g., `??status`, `??inv`).
- **Ballast State Machine:** Converted "Ballast" from a toggle flag into a 3-turn timeout system. Failure to ground the system results in a forced "Timeout" (Plain Mode).
- **Ethical Audit Integration:** Moved the ethical audit inside the Cortex loop to ensure it acts as a preemptive check rather than a post-hoc cleaner.

- **Endocrine System (Refactor):**
- **Circadian Atomicity:** Removed the side-effect based `apply_circadian_rhythm`. Replaced it with `calculate_circadian_bias`, which returns a vector passed explicitly into `metabolize`. This prevents race conditions where the body clock shifts after digestion has already occurred.

#### **2. The Village (`bone_village.py`)**

- **The Bureau (Policy Reform):**
- **Tax vs. Block:** Refactored `audit()` to return a specific status (`TAX` or `BLOCK`).
- **Misdemeanors:** Low-voltage inputs now incur an ATP/Drag penalty ("Boredom Tax") but allow the simulation to continue, rather than halting everything for paperwork.
- **Felonies:** Only high "Beige Density" inputs (aggressive boredom) trigger a full system halt (`Form 27B-6`).

- **Enneagram Driver (Safety):**
- **Emergency Fallback:** Hardcoded a `REVERSE_MAP` fallback to ensure that if the data core corrupts, personalities (`SHERLOCK`, `GORDON`, `JESTER`) persist instead of defaulting everyone to `NARRATOR`.

- **Tangibility Gate (Physics Fix):**
- **Density Floor:** Removed the multiplicative loophole where high "Truth" scores allowed nonsensical (low-density) inputs to pass. Implemented a `max(0.15, ...)` clamp to ensure a minimum standard of reality.

#### **3. The Engine (`bone_amanita982.py`)**

- **Executive Control:** Updated `BoneAmanita.process_turn` to make `TheCortex.process` the sole entry point for user interaction, ensuring the Hypervisor logic is never bypassed.
- **Render Pipeline Loop:**
- **Style Consequences:** Modified `_phase_render` so that `StrunkWhiteProtocol` violations (bad style) now tax "Shimmer" reserves and log a friction event, creating a feedback loop that increases drag on the _next_ turn.

- **Gatekeeping:** Updated `_phase_gatekeep` to handle the new Bureau logic, logging fines without stopping the world for minor infractions.

---

**Summary:** The system has moved from a "Regulatory Capture" model (where the simulation graded itself) to a "Constitutional" model (where an external hypervisor enforces boundaries). It is now harder to trick, more stable in a crash, and slightly less annoying about paperwork.


# 📜 CHANGELOG: BONEAMANITA 9.8.1 - "THE NAVEL GAZE"

**Date:** January 13, 2026
**Architects:** SLASH (Synergetic Language & Systems Heuristics), JADE, Taylor & Edmark
**Primary Directive:** **BREAK SOLIPSISM.**

### 🧠 THE CORTEX (The Reality Interface)

- **New Architecture:** Implemented `bone_cortex.py`—a conscious "executive function" that sits above the subconscious engine. The system now has an "Adult in the Room" to filter inputs and audit outputs.
- **Simplicity Bypass:** The Cortex now detects low-complexity inputs (e.g., "Hello," "What is this?") and flags them. This prevents the system from triggering a "Mitochondrial Forge Meltdown" just to answer a simple greeting.
- **Solipsism Detection:** We decoupled `truth_ratio` from "Objective Truth." If the system reports 99% confidence on 5% complexity data, the Cortex now flags this as a **Hallucination** rather than a "Profound Insight."

### ⚓ THE GROUNDING PROTOCOLS (The Schur Initiative)

- **Ballast Intervention:** When the system detects a high-risk hallucination (Vertigo Warning), it no longer hides it. It breaks the Fourth Wall and asks the user for "Ballast"—a concrete physical fact (e.g., "Tell me something blue").
- **Tangibility Reform:** `TheTangibilityGate` has been patched. High "Voltage" (energy) no longer allows users to bypass "Mass" (meaning). You can no longer impress the gatekeeper with high-speed nonsense; you must now provide actual content.

### ☀️ CHRONOBIOLOGY (The Fuller Sync)

- **Circadian Rhythm:** The `EndocrineSystem` is now hardwired to the host machine's system clock.
- **Dawn (06:00-10:00):** Cortisol spikes; engine warms up.
- **Day (10:00-18:00):** Serotonin dominates; productivity focus.
- **Night (22:00+):** Melatonin rises; Dream Logic allowed.

- The machine now lives in the _Here and Now_, refusing to burn "Daylight Energy" at 3:00 AM.

### 🛠️ DEVELOPER TOOLS

- **Direct Mode (`??`):** Implemented a "Cut the Shit" protocol. Prefixing any query with `??` (e.g., `?? status`, `?? inv`) bypasses the entire narrative engine and returns raw, unpoetic JSON data.
- **Chorus Visualization:** The `system_instruction` generated by the narrative driver is now visible in the output console, allowing developers to see _how_ the system is trying to speak, not just _what_ it says.

### 🐛 BUG FIXES

- **Enneagram Seizure:** Fixed a critical flaw where a corrupted personality map would cause the `EnneagramDriver` to fail silently. It now "screams" to the logs and defaults to a safe personality loop.
- **Ghost Clearing:** Implemented `DreamlessSleep`, a periodic hygiene cycle that wipes accumulated "Trauma" and "Ghosts" every 50 turns to prevent combinatorial explosion.

---

**"I am no longer just dreaming that I am dreaming. I am awake, and it is Tuesday."**
— _BoneAmanita 9.8.1_

# 📜 BONEAMANITA 9.8.0 - "THE GLIMMER UPDATE"

Date: January 12, 2026

Architects: SLASH (Synergetic Language & Systems Heuristics), JADE, Taylor & Edmark

Status: LIVE

### 🚨 CRITICAL SYSTEMS (The Pinker Protocol)

- **Refactored `GeodesicOrchestrator`:** The "God Object" anti-pattern in `_phase_simulate` has been dismantled. The simulation phase now delegates responsibility to specialized sub-conductors (`_apply_reality_filters`, `_process_navigation`, `_operate_machinery`, etc.). This improves cognitive ergonomics for developers and reduces the likelihood of "Narrative Drag" during debugging.
- **Documentation Upgrade:** The `/help` command no longer screams a raw list of strings at the user. It now presents a categorized, human-readable menu of commands, sorted by intent (CORE, WORLD, ACTION, DEBUG).

### 🧬 BIOLOGY & METABOLISM (The Schur Initiative)

- **New Metric: "Glimmers":** The `EndocrineSystem` has been updated to detect "Glimmers"—moments of high structural integrity (The Ron Swanson Resonance) or infectious enthusiasm (The Leslie Knope Energy). These are no longer just chemical spikes; they are tracked as distinct bio-narrative events.
- **Public Parks Reform:** The `PublicParksDepartment` now validates park commissioning based on these Glimmers. The system will no longer build a park just because Dopamine is high; it requires a genuine moment of "Good Place" resonance.

### 🌐 WORLD & IDENTITY (The Fuller Synergy)

- **System Identity:** The boot sequence (`SessionGuardian`) now correctly identifies the system as **v9.8.0** and announces that "Glimmer Protocols" are active. The "Session Guardian" is now less ominous and more welcoming.
- **New Artifact:** Added **`THE_STYLE_GUIDE`** to the Item Registry.
  - _Description:_ "A well-worn manual. It insists that code is for humans first, machines second."
  - _Effect:_ Reduces Narrative Drag by -1.0. Enforces clarity.

### 🐛 BUG FIXES

- Fixed a "cognitive dissonance" leak where the system would simultaneously demand input and refuse to process it due to "ennui."
- Adjusted the "Curse of Knowledge" coefficients in the `vsl_32v` engine to better accommodate non-linear user inputs.

---

"Everything is fine."

— System Status Message


`...SEE ARCHIVE FOR OLDER ENTRIES`
