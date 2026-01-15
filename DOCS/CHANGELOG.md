# CHANGELOG.md

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
