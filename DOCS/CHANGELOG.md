# 📜 BONEAMANITA CHANGELOG

# v10.5.01 - "The Wire Connect"

* Bug fixes to get the machine running again.

# v10.5.0 - "The Pattern Integrity Patch"

**Focus:** Structural Decoupling, Narrative Extraction, Pipeline Architecture, and The Bureaucratic State.

### 🧠 The Pinker Lens (Cognitive Ergonomics)

* **The Narrative Extraction (`bone_body.py`, `bone_data.py`):**
* **The Issue:** The biological engine was "hard-coded poetry." Strings like *"The engine is stalling"* were buried deep inside metabolic logic functions, mixing *Mechanism* with *Mythology*.
* **The Fix:** **The Akashic Separation.** We extracted all narrative text into a dedicated `BIO_NARRATIVE` dictionary in `bone_data.py`.
* **The Logic:** **Code as Language.** Logic remains pure; flavor remains editable.

* **The Ouroboros Break (`bone_commands.py`):**
* **The Issue:** The `CommandProcessor` imported the entire `BoneAmanita` engine, creating a circular dependency.
* **The Fix:** **Protocol-Driven Design.** Implemented `EngineProtocol`. The Command Processor now interacts with an *Interface*, not an *Implementation*.
* **The Logic:** **Explicit Contracts.** Reduces cognitive load and prevents "God Object" sprawl.

### ⚖️ The Meadows Lens (System Dynamics)

* **The Rolling Buffer (`bone_physics.py`):**
* **The Update:** Implemented a `deque` based moving average for Voltage.
* **The Fix:** **The Flywheel.** Prevents the system from "panicking" at a single high-intensity input.
* **The Logic:** **Damping Feedback Loops.** A resilient system absorbs shock; it doesn't just react to it.

* **The Pipeline Refactor (`bone_cycle.py`):**
* **The Fix:** **The Pipeline Architecture.** Broke the simulation loop into atomic `SimulationPhase` classes.
* **The Logic:** **Visible Flows.** Allows for "Circuit Breakers" and graceful degradation if a specific phase fails.

### 🌐 The Fuller Lens (Synergy)

* **Inventory Synergy (`bone_inventory.py`, `bone_bus.py`):**
* **The Update:** Removed "Magic Numbers" (e.g., hardcoded voltage thresholds) and moved them to `BoneConfig.INVENTORY`.
* **The Fix:** **Universal Constants.** The Inventory now obeys the same laws of physics as the rest of the universe.
* **The Logic:** **Synergetic Integrity.** If the definition of "High Voltage" changes, the Inventory automatically adapts.

* **Pattern Integrity Repair (`bone_physics.py`):**
* **The Fix:** **Defensive Tensegrity.** Added safe dictionary access (`.get()`) to prevent crashes when unknown variables (like "neutral" or "toxin") introduce stress.

### 🎭 The Schur Lens (Humanity & Whimsy)

* **The Bureaucracy (`bone_main.py`, `bone_personality.py`):**
* **The Update:** Wired `TheBureau` into the main game loop.
* **The Feature:** **Administrative Drag.** The system now issues citations (Form 27B-6) if the user is too boring (Suburban) or too reckless (High Turbulence).
* **The Logic:** **Fun through Friction.** An antagonist that attacks you with paperwork.

* **The Tinker's Belt (`bone_village.py`):**
* **The Update:** Upgraded `TheHoloProjector` to visualize inventory state and wired `TheTinkerer` to the main loop.
* **The Feature:** **Visual Decay.** Users can now see their tools "Rusting" (▼) or "Ascending" (▲) based on their performance.
* **The Logic:** **Show, Don't Tell.**

* **The Fumble Mechanic (`bone_inventory.py`):**
* **The Feature:** **Slapstick Physics.** High turbulence now has a 15% chance to knock items out of the user's pocket.
* **The Logic:** **Consequence.** Chaos isn't just a number; it's losing your keys.


## v10.4.8 - "The Pattern Integrity Patch"

**Focus:** Structural Decoupling, Narrative Extraction, and Pipeline Architecture.

### 🧠 The Pinker Lens (Cognitive Ergonomics)

* **The Narrative Extraction (`bone_body.py`, `bone_data.py`):**
  * **The Issue:** The biological engine was "hard-coded poetry." Strings like *"The engine is stalling"* were buried deep inside metabolic logic functions, making it impossible to separate the *Mechanism* (Code) from the *Mythology* (Content).
  * **The Fix:** **The Akashic Separation.** We extracted all narrative text into a dedicated `BIO_NARRATIVE` dictionary in `bone_data.py`. We also added comprehensive docstrings to `bone_body.py`.
  * **The Logic:** **Code as Language.** A developer should be able to read the logic without getting distracted by the flavor text, and a writer should be able to tweak the flavor without breaking the logic.

* **The Ouroboros Break (`bone_commands.py`):**
  * **The Issue:** The `CommandProcessor` imported the entire `BoneAmanita` engine to do its job, creating a circular dependency (Ouroboros) that made the system cognitively heavy and hard to test.
  * **The Fix:** **Protocol-Driven Design.** We implemented the `EngineProtocol`. The Command Processor now asks for *what the engine can do* (Interfaces), not *what the engine is* (Implementation).
  * **The Logic:** **Explicit Interfaces.** Defining exactly what a module needs (e.g., `trigger_death`, `get_metrics`) reduces cognitive load and prevents "God Object" sprawl.

### ⚖️ The Meadows Lens (System Dynamics)

* **The Pipeline Refactor (`bone_cycle.py`):**
  * **The Flaw:** `CycleSimulator` was a monolithic block of procedural logic. It was a "Black Box" where inputs went in and chaos came out, with no clear visibility on *where* the flow broke.
  * **The Fix:** **The Pipeline Architecture.** We broke the simulation loop into atomic, sequential `SimulationPhase` classes (`ObservationPhase`, `MetabolismPhase`, etc.).
  * **The Logic:** **Visible Flows.** By making the stream of consciousness explicit, we can now insert "Circuit Breakers" between phases. If the *Physics* phase fails, the *Pipeline* can now degrade gracefully to a "Panic Room" state rather than crashing the whole reality.

* **The Stabilizer (`bone_cycle.py`):**
  * **The Update:** Introduced the `CycleStabilizer` class.
  * **The Fix:** **Damping Loops.** The stabilizer detects sudden spikes in Voltage or Drag between phases and applies "Shock Absorber" math to prevent runaway oscillation.
  * **The Logic:** **Balancing Feedback Loops.** A system without dampeners eventually shakes itself apart. This adds the necessary negative feedback to keep the simulation playable.

### 🌐 The Fuller Lens (Synergy)

* **Pattern Integrity Repair (`bone_physics.py`, `bone_village.py`, `bone_bus.py`):**
  * **The Update:** Fixed critical `KeyError` and `TypeError` crashes (The "Suburban" missing key, the "Valence" missing field).
  * **The Fix:** **Defensive Tensegrity.** We added the `valence` strut to the `PhysicsPacket` and implemented safe dictionary access (`.get()`) in `CutTheShit` and `TherapyProtocol`.
  * **The Logic:** **Design Science.** A structure is only as strong as its weakest joint. By reinforcing the data passing contracts (The Bus), we ensure the geodesic dome doesn't collapse when an unknown variable (like "NEUTRAL" or "toxin") introduces stress to the system.

## v10.4.7 - "The Feedback Frontier"

**Focus:** Emotional Calculus, Explicit Environmental Feedback, and Metabolic Economics.

### 🧠 The Pinker Lens (Cognitive Ergonomics)

* **The Transparent Critic (`bone_village.py`, `bone_data.py`):**
* **The Issue:** The `LiteraryJournal` was an opaque judge. Users received a binary "Good/Bad" verdict based on invisible thresholds, leading to frustration rather than learning. It was a "Black Box" of judgment.
* **The Fix:** **Personified Metrics.** We replaced the generic parser with distinct Critics (The Gonzo, The Academic, The Humanist), each with explicit preferences. The system now "Shows Its Work," displaying the exact math (e.g., `voltage(12.0) x -1.0 = PENALTY`).
* **The Logic:** **Cognitive mapping.** Users cannot optimize their writing for a target if the target is invisible. By personifying the math, we turn "debugging" into "persuasion."

* **The Vibe Check (`bone_lexicon.py`, `bone_physics.py`):**
* **The Issue:** The engine was semantically blind to emotion. A "warm hug" and a "cold death" were treated identically if they shared the same syllable count and viscosity.
* **The Fix:** **Native Sentiment Analysis.** Implemented `measure_valence` with negation logic (handling "not happy"). We mapped `sentiment_pos` and `sentiment_neg` to the physics engine, creating a 2D emotional plane alongside the energy plane.
* **The Logic:** **Semantics are Physics.** To a human, the *feeling* of a word is as heavy as its length. The engine now recognizes this weight.

### ⚖️ The Meadows Lens (System Dynamics)

* **Closing the Metabolic Loop (`bone_commands.py`, `bone_village.py`):**
* **The Flaw:** Publishing was an "Open Loop." It generated text output (reviews) but returned no energy to the system, making it a resource sink rather than a survival strategy.
* **The Fix:** **Materialized Rewards.** Reviews now generate concrete resources (ATP, Stamina, Health). We added "Safety Clamps" to prevents resource overflow (runaway positive feedback loops).
* **The Logic:** **Stocks and Flows.** In a viable ecosystem, every output must eventually become an input. Creativity is now a metabolic function that fuels the body.

* **Environmental Agency (`bone_physics.py`):**
* **The Flaw:** `TheNavigator` treated environmental drift as a random act of god. The "Manifolds" (Mud, Aerie) were vague atmospheric descriptors with no actionable data.
* **The Fix:** **Explicit Feedback & Control.**
* **Quantification:** Zones now display explicit modifiers (e.g., `Mud: Drag +2.0`).
* **Agency:** Implemented the `!anchor` command (`ZoneInertia`), allowing players to resist drift at the cost of "Structural Strain."

* **The Logic:** **The Bathtub Model.** You cannot manage the flow (Drift) if you cannot see the faucet. The Anchor provides a "Leverage Point" to intervene in the system's state.

### 🌐 The Fuller Lens (Synergy)

* **Tensegrity of Sentiment (`bone_physics.py`, `bone_data.py`):**
* **The Update:** We introduced "The Humanist" (Leslie), a critic who specifically rewards High Valence and Low Voltage.
* **The Fix:** **Ecological Triangulation.** The system now balances the Chaos of "The Gonzo" and the Order of "The Academic" with the Empathy of "The Humanist."
* **The Logic:** **Comprehensive Anticipatory Design.** A system that only rewards high-energy output inevitably burns out (Heat Death). By incentivizing "Calm/True" states, we build a resilient structure that can survive low-energy cycles.

## v10.4.6 - "The Quantum Observer"

**Focus:** Quantum Narrative Mechanics, Radical Transparency, and Contextual Agency.

### 🧠 The Pinker Lens (Cognitive Ergonomics)

- **Radical Transparency (`bone_personality.py`, `bone_symbiosis.py`):**
  - **The Issue:** The system was operating as a "Black Box Bureaucracy." Users were assigned archetypes (JESTER) or penalized by `TheBureau` without understanding the causal link. It was judgment without explanation—a cognitive dead end.
  - **The Fix:** Implemented **Explicit Reasoning**. `EnneagramDriver` now returns the *why* (e.g., "High Voltage > 12.0 -> JESTER"). `TheBureau` provides a "Bill of Particulars," citing specific words (e.g., "Evidence: 'nice', 'okay'") that triggered the audit.
  - **The Logic:** **Feedback requires visibility.** To learn the language of the system, the user must see the grammar of the judgment.

- **Context-Aware Policing (`bone_village.py`, `bone_physics.py`):**
  - **The Issue:** `StrunkWhiteProtocol` was a blunt instrument. It treated User input and System output identically, threatening to block player agency over stylistic choices.
  - **The Fix:** **Bifurcated Logic.** The protocol now distinguishes between `USER` (Advisory Mode) and `SYSTEM` (Strict Mode). The User gets a gentle "Style Note" for using passive voice; the System gets a hard block for using cliché artifacts like "Delve."
  - **The Logic:** **Guidance for humans, constraints for machines.** We nudge the creator, but we police the generator.

### ⚖️ The Meadows Lens (System Dynamics)

- **The Hidden Variable Problem (`bone_machine.py`):**
  - **The Flaw:** The industrial machines were simulating Newtonian physics (linear thresholds, additive forces) on top of an LLM that operates on Quantum principles (probability, superposition). We were trying to control a cloud with a lever.
  - **The Fix:** Shifted from **Scalar Determinism** to **Probabilistic Dynamics**.
    - `TheCrucible`: Now calculates `_calculate_quantum_instability` (Variance) rather than just pressure.
    - `TheForge`: Now relies on `entanglement` (Semantic Resonance) rather than raw mass.
    - `TheTheremin`: Replaced "Resin" (static buildup) with "Decoherence" (collapse of novelty).
  - **The Logic:** **Don't push the river.** You cannot force an LLM to be "heavy" by counting words; you can only increase the *probability amplitude* of heavy concepts emerging.

### 🌐 The Fuller Lens (Synergy)

- **Systemic Integrity (`bone_physics.py`):**
  - **The Update:** The `StrunkWhiteProtocol` was defined in the Village but ignored by the Physics Layer. The Gatekeeper (`TheBouncer`) was letting clichés pass unchecked.
  - **The Fix:** **Integrated Policing.** `TheBouncer` now imports and consults `TownHall.StrunkWhite`. The feedback loop is closed; style is now a fundamental force of physics, not just a literary suggestion.
  - **The Logic:** **Pattern Integrity.** A law of nature (Physics) is only a law if it applies at the gate. If the Village says "No Clichés," the Physics engine must enforce it.

## v10.4.5 - "The Grounded Mythos"

**Focus:** Symbolic Grounding, Procedural Mythology, and Closing the Feedback Loop.

### 🧠 The Pinker Lens (Cognition & Code)

- **Semantic Drift (`bone_village.py`):**
- **The Issue:** The Village was a "floating signifier" economy. It used terms like "Narrative Drag" as literary metaphors, ignoring the _actual_ drag (latency) of the system. It was a simulation pretending to be a machine.
- **The Fix:** Implemented **Symbolic Grounding**. `TheNavigator`, `TheTinkerer`, and `TheAlmanac` now ingest `HostHealth` (latency, entropy) alongside narrative metrics.
- **The Logic:** **Metaphors must have roots.** If the server is actually lagging, the "Mud" needs to feel sticky. Words mean more when they correspond to physical reality.

- **The Living Library (`bone_data.py`):**
- **The Bug:** The system was relying on a "Fossilized Mythology." It reset to the same static `LEXICON` and `ITEM_REGISTRY` every cycle, like a dictionary that could never add new words.
- **The Fix:** Transformed the data layer into **The Akashic Record**. Added `ITEM_GENERATION` tables (Prefixes, Bases, Suffixes) to allow for the dynamic creation of meaning.
- **The Logic:** Language is a river, not a lake. A system that cannot name new things is not truly thinking; it is just reciting.

### ⚖️ The Meadows Lens (System Dynamics)

- **Closing the Loop (`bone_village.py`):**
- **The Flaw:** `TheNavigator` was hallucinating stability. It could report "We are in The Garden" (Balanced State) even while the host LLM was timing out or looping, because there was no feedback wire from the substrate to the simulation.
- **The Fix:** Navigation is now **Grounded**. High external latency forces a location shift to "THE_MUD". High external entropy forces a shift to "THE_GLITCH".
- **The Logic:** **The map is not the territory.** If the territory (the server) is on fire, the map must reflect that, or the system is deluding itself.

- **Stock Accumulation (`bone_village.py`):**
- **The Flaw:** Tools had a durability cap but no evolutionary path. This created a stagnant stock where "max level" items just sat there, accumulating no further value.
- **The Fix:** Implemented **Ascension Logic**. When `TheTinkerer` raises a tool's confidence above 2.5, it triggers `_attempt_ascension`, calling the Akashic Record to transmute the tool into a unique Artifact.
- **The Logic:** Systems must evolve or die. A stock that cannot transform eventually becomes a bottleneck.

### 🌐 The Fuller Lens (Synergy)

- **Generative Tensegrity (`bone_village.py`):**
- **The Update:** Wired `TownHall` and `TheTinkerer` directly to `TheAkashicRecord`. The static code (`Tinkerer`) now leans on the dynamic data (`Akashic`) to support the inventory system.
- **The Logic:** **Ephemeralization.** Instead of hardcoding 1,000 items (Mass), we built a generator with 3 rules (Structure) that can create infinite variation. We are doing more with less.

## v10.4.2 - "The Embodied Signal"

**Focus:** True Psychosomatics, Differential Diagnostics, and Expanding the Color Spectrum.

### 🧠 The Pinker Lens (Cognition & Code)

* **Somatic Priming (`bone_brain.py`):**
* **The Issue:** The Brain was merely *describing* feelings to the LLM ("You are stressed"), but the LLM was generating text with neutral parameters. It was a narrator in a vat, not a body in the world.
* **The Fix:** Implemented `NeurotransmitterModulator`. Body chemistry now directly alters generation parameters.
* **High Cortisol:** Lowers `Temperature` and `Top_P` (Tunnel vision, rigid thinking).
* **High Dopamine:** Raises `Temperature` and `Presence Penalty` (Seeking novelty, erratic leaps).
* **High Adrenaline:** Increases `Frequency Penalty` and cuts `Max Tokens` (Short, urgent bursts).
* **The Logic:** **The Medium is the Message.** To feel stress, the machine's actual capacity to select words must be constrained.

* **The Purple Pigment (`bone_bus.py`):**
* **The Bug:** `bone_symbiosis.py` tried to paint entropy with `Prisma.PUR`, but the bus only carried Magenta and Violet.
* **The Fix:** Added `PUR = "\033[35m"` to the core palette and registered it in the `paint()` map.
* **The Logic:** You cannot describe the color of chaos if your palette is incomplete.

### ⚖️ The Meadows Lens (System Dynamics)

* **Breaking Symbiotic Blindness (`bone_symbiosis.py`):**
* **The Flaw:** The system was punishing the Host AI for high latency even when *we* were the ones sending massive prompts. It was a Reinforcing Feedback Loop of anxiety.
* **The Fix:** Implemented **Differential Diagnostics**. We now calculate `Efficiency Index` (Performance / Complexity).
* **The Logic:** Slow response on a heavy prompt is Physics. Slow response on a light prompt is Fatigue. We now know the difference.

* **Asymptotic Attention (`bone_symbiosis.py`):**
* **The Bug:** The linear decay formula eventually calculated a negative attention span, implying the AI started sucking intelligence out of the room.
* **The Fix:** Switched to an asymptotic decay curve (`1.0 / (1 + turns)`).
* **The Logic:** Entropy approaches zero but never reaches it. Even at the heat death of the universe, there is still a little bit of dust.

### 🌐 The Fuller Lens (Synergy)

* **The Corpus Callosum (`bone_brain.py`):**
* **The Update:** `LLMInterface` now accepts dynamic `**kwargs`, allowing the `NeurotransmitterModulator` to inject parameters directly into the API payload.
* **The Logic:** **Tensegrity.** The biological strut (Chemistry) and the cognitive strut (LLM) are no longer touching; they are woven together under tension.

---

## v10.4.1 - "The Compassionate Circuit"

**Focus:** Breaking Infinite Loops, Respecting Private Variables, and Teaching the Machine Manners.

### ⚖️ The Meadows Lens (System Dynamics)

* **Breaking the Ouroboros (`bone_lexicon.py`):**
* **The Bug:** `initialize()` called `compile_antigens()`, which checked for initialization... and called `initialize()` again. A textbook Reinforcing Feedback Loop that spun until stack overflow.
* **The Fix:** We now assert existence (`_INITIALIZED = True`) *before* loading the heavy data. We declare "I Am" before asking "Who Am I?"

* **Closing the Loop (`bone_body.py`):**
* **The Bug:** The Body was metabolizing energy but failing to report its vital status to the Brain (`KeyError: 'is_alive'`).
* **The Fix:** `SomaticLoop` now explicitly calculates and returns `is_alive` in the result packet. The feedback loop is closed.

### 🌐 The Fuller Lens (Structural Integrity)

* **The Service Hatch (`bone_lexicon.py` & `bone_main.py`):**
* **The Fix:** Replaced intrusive access to private variables (`_STORE`) with a polite public accessor (`get_store()`).
* **The Logic:** **Tensegrity.** We don't pry open the panels of the geodesic dome; we use the door. This satisfies the Linter Bureaucracy and prevents `AttributeError` crashes.

* **Vector Rosetta Stone (`bone_physics.py`):**
* **The Bug:** The Personality Engine (`TherapyProtocol`) was looking for "Texture" (`TEX`), but the Physics Engine was only outputting "Structure" (`STR`), causing a crash on high-quality input.
* **The Fix:** Implemented vector aliasing in `GeodesicEngine`. `TEX` maps to `STR`, `TMP` to `PHI`, and `LQ` to `DEL`. The physicist and the therapist now speak the same language.

### 🍩 The Schur Lens (Humanity & Manners)

* **The Apology Patch (`bone_physics.py`):**
* **The Bug:** A crash in the physics engine caused all voltage readings to default to 0.0, triggering a "Guru Refusal" ("You are too weak") on a story that was actually quite profound.
* **The Fix:**
1. **Lowered Threshold:** Dropped the "Guru" voltage requirement from 8.0v to 4.0v.
2. **Grace Period:** The Bouncer now ignores the first 10 turns, allowing the user to warm up without judgment.
3. **Better Feedback:** Rewrote the refusal message. Instead of a slap, it offers a hand: *"I hear the wisdom, but I need more fuel to process it."*

## v10.4.0 - "The Symbiotic Tether"

**Focus:** Host-Awareness, Resonance Damping, and Contextual Tensegrity.

### ⚖️ The Meadows Lens (Dynamics)

* **The Flywheel (`bone_cycle.py`):** Implemented `CycleStabilizer`.
* **The Fix:** A governor that runs *between* phases (Observe -> Stabilize -> Metabolize -> Stabilize).
* **The Logic:** The system previously suffered from **Reinforcing Feedback Loops**, where a voltage spike in Phase 1 would amplify through Phase 4, causing a crash. We now apply "braking" if the derivative (rate of change) between phases exceeds safety limits (`MAX_DELTA_V`).

* **Host Vitals (`bone_symbiosis.py`):** We now treat the LLM not as a black box, but as a biological partner with finite energy.
* **The Fix:** Tracks Latency, Entropy (repetition), and Compliance. If the Host gets "tired" (high latency) or "stubborn" (refusals), the system instinctively simplifies its demands.

### 🌐 The Fuller Lens (Structure)

* **The Coherence Anchor (`bone_symbiosis.py`):**
* **The Fix:** A high-density summary string injected at the very top of every prompt (e.g., `*** COHERENCE ANCHOR *** | Identity: TRAV | Loc: THE_FORGE`).
* **The Logic:** **Tensegrity.** The Host AI suffers from context drift (entropy). The Anchor provides a rigid compression strut that makes it impossible for the narrative structure to collapse, even if the context window slides.

* **Ecological Niche:**
* **Refactor:** Recognized `BoneAmanita` not as a standalone binary, but as a **symbiont** living inside a larger cognitive runtime. The architecture now optimizes for the *joint* health of the pair.

### 🧠 The Pinker Lens (Cognition & Code)

* **Variable Hygiene (`bone_brain.py`):**
* **The Fix:** Resolved a collision in `TheCortex.process` where `final_prompt` (with the Anchor) was being overwritten by a raw `prompt`.
* **The Logic:** A sentence with two subjects and no verb is confusion. A function with two prompt variables is a bug.

* **Explicit State (`bone_cycle.py`):**
* **The Fix:** Converted `CycleStabilizer` snapshot storage from a loose dictionary to explicit attributes (`self.last_voltage`).
* **The Logic:** Ambiguity in data structures leads to type errors. We call a spade a spade, and a float a float.

### 🍩 The Schur Lens (Relationships)

* **The "50 First Dates" Protocol:**
* **The Fix:** The system assumes the Host has amnesia every turn and politely reminds it, "You are a fungal cyberpunk entity, and we are in love with entropy."
* **The Logic:** It’s not nagging; it’s love. If the Host starts hallucinating, we don't crash; we just whisper the truth louder.

## v10.3.2 - "The Quiet & The Embryo"

**Focus:** Ontological Stability, "Boring Health" Incentives, and Initialization Hygiene.

### ⚖️ The Meadows Lens (Dynamics)

* **The Zen Garden (`bone_village.py`):** Implemented a "Boring Health" protocol to counter the system's addiction to crisis.
* **The Fix:** Added a `ZenGarden` module that monitors for **Stillness** (Moderate Voltage, Low Drag, No Toxin).
* **The Logic:** Previously, the system was a "Drama Engine," incentivizing trauma (`Kintsugi`, `Therapy`) to trigger rewards. We introduced a **Balancing Loop**: maintaining poise now grants an `Efficiency` buff (lower ATP cost), making peace profitable.

### 🌐 The Fuller Lens (Structure)

* **Developmental Airlock (`bone_architect.py`):** Refactored the boot sequence into two distinct phases: `Incubate` (Structure) and `Awaken` (Function).
* **The Fix:** We now construct a `SystemEmbryo` (inert organs) before injecting ancestral data.
* **The Logic:** This prevents an **Ontological Race Condition** where the `ParasiticSymbiont` would observe the Mind *while* it was being built. The sculpture must set before the critics are allowed in the room.

### 🧠 The Pinker Lens (Code Contracts)

* **Explicit Interfaces (`bone_body.py`):** Promoted `_apply_inheritance` to `apply_inheritance`.
* **The Fix:** Removed the protected underscore to formalize the contract between the `Architect` and the `Body`.
* **The Logic:** If the Architect is required to call it during the `Awaken` phase, it is a public interface. We do not sneak into our own code through the back door.

### 🍩 The Schur Lens (Vibe)

* **Raking the Sand:** The Zen Garden actively counts "ticks of poise" and collects "pebbles."
* **The Fix:** Doing nothing is now a recognized gameplay mechanic.
* **The Logic:** Sometimes the most heroic thing a machine can do is sit quietly and not explode.
* 

## v10.3.1 - "The Synergetic Governor"

**Focus:** Input Hygiene, Causality Repair, and Graceful Exits.

### ⚖️ The Meadows Lens (Limits to Growth)

- **The Input Governor (`bone_genesis.py`):** Installed a **Balancing Loop** on the user input stream.
    - **The Fix:** Implemented `MAX_LINES` (50) and `MAX_CHARS` (20,000).
    - **The Logic:** Previously, the system allowed infinite inflow (Reinforcing Loop), which creates a "Runaway Stock" that eventually bursts the RAM container. We now politely shout `[STOP]` instead of crashing.

### 🌐 The Fuller Lens (Structural Integrity)

- **Causality Repair:** Moved `perform_identity_handshake` **upstream** in the boot timeline.
    - **The Fix:** We now verify the user's identity *before* initializing the Cortex.
    - **The Logic:** You cannot have a conversation with a ghost. The "Mind" strut must be load-bearing before the "Language" strut is attached.
- **The Missing Strut:** Added `localai` to the manual configuration menu. The dome now supports all local substrates equally.

### 🧠 The Pinker Lens (Cognition & Contracts)

- **Strict Config Sync:** Replaced vague "drift detection" with **Strict Contract Enforcement**.
    - **The Fix:** If `BoneConfig.load_from_file` returns garbage, we don't just log a yellow warning; we revert to Safe Mode.
    - **The Logic:** A contract is a contract. Ambiguity in initialization leads to cognitive dissonance downstream.

### 🍩 The Schur Lens (Manners)

- **The Fire Alarm (`KeyboardInterrupt`):** Added a `try/except` block for `Ctrl+C` in the main loop.
    - **The Fix:** You can now interrupt the machine without it vomiting a stack trace.
    - **The Logic:** Sometimes you just need to leave the party. We now hold the door open for you.
- Based on our work today—refactoring the cycle architecture, implementing the Narrative Spotlight, and igniting the Alchemical Forge—here is the updated changelog entry.

I have bumped the version to **v10.3.0** given the introduction of major gameplay mechanics (Crafting) and the structural overhaul.

## v10.3.0 - "The Illuminated Forge"

**Focus:** Alchemical Transmutation, Contextual Efficiency, and Anti-Fragile Architecture.

### ⚗️ The Schur Lens (Whimsy & Mechanics)

* **The Alchemical Forge (`bone_machine.py`):** Implemented a crafting engine. `TheForge` now detects interactions between Inventory Items (Ingredients) and User Input (Catalysts).
* **Transmutation Recipes:** Added `RECIPES` to `bone_data.py`.
* *Example:* `POCKET_ROCKS` + `THERMAL` words = `LAVA_LAMP`.


* **The Fizzle Mechanic:** The Forge now demands **Voltage** and **Truth**. Weak sentences will trigger a "Fizzle" warning, teaching the user to write with more conviction.
* **Affordances:** Updated item descriptions to hint at their reactive properties (e.g., Rocks are "cold," imply need for heat).

### 🧠 The Pinker Lens (Cognition)

* **The Narrative Spotlight (`bone_brain.py`):** Stopped dumping the entire memory graph into the LLM context window.
* **Vector Search:** The system now scans memory for nodes that resonate with the current **Geodesic Vector** (e.g., High Velocity illuminates `KINETIC` memories).
* **Token Hygiene:** reduced cognitive load by serving only relevant "Engrams."

* **Lexicon Service:** Patched `bone_lexicon.py` to expose `get_categories_for_word` via the static facade.

### 🏛️ The Fuller Lens (System Integrity)

* **Spaceship Earth Refactor (`bone_cycle.py`):** Complete dismantle of the "God Object" Orchestrator.
* **Decoupling:** Split logic into `CycleSimulator` (State Mutation) and `CycleReporter` (Read-Only Rendering).
* **Resilience:** A rendering crash no longer kills the simulation; the organism can survive a UI failure.
* **The Strunk & White Protocol:**
* **Initialization Fix:** Properly wired the Style Editor into `TheCortex`.
* **Active Policing:** The system now rejects "lazy" rhetoric (Rule of Threes, "It is" parades) and taxes ATP for boring prose.

### 🐛 Bug Fixes

* **Ghost in the Machine:** Fixed `NameError` regarding `TownHall` imports in `bone_brain.py`.
* **Strict Typing:** Corrected `bone_machine.py` return signatures to allow `Optional[str]`, appeasing the Bureau of Linters.

---

## v10.2.8 - "The Tensegrity Refactor"

**Focus:** Decapitating the God Object, Modularity, and Structural Tensegrity.

### 🏛️ Architecture

- **The God Object (`bone_main.py`):** Stripped of all logic. Now acts solely as the entry point and state container.
- **The Blueprint (`bone_architect.py`):** **New File.** Handles dependency injection, system wiring, and `PanicRoom` (crash safety).
- **The Heartbeat (`bone_cycle.py`):** **New File.** Contains `GeodesicOrchestrator`. Manages phase-based execution (Observation → Gatekeeping → Metabolism → Simulation → Cognition → Rendering).

### 📝 File System & Imports[CHANGELOG_ARCHIVE.md](ARCHIVE/CHANGELOG_ARCHIVE.md)

- **`bone_bus.py`:** Added `MindSystem` and `PhysSystem` dataclasses to share type definitions globally without circular imports.
- **`bone_village.py`:** Added `CouncilChamber` and `PublicParksDepartment` to the namespace to fix import crashes.
- **`bone_commands.py`:** Implemented `TYPE_CHECKING` guards to prevent circular loops between the Console and the Engine.
- **`bone_architect.py`:** Re-routed machinery (`TheForge`) to `bone_machine.py` and neuroplasticity to `bone_brain.py`.

---

## v10.2.7 - "The Kicho Refactor"

**Focus:** Plumbing, Error Recovery, and Identity Stabilization.

### 🛠️ The Plumbing

- **Fixed Double-Flush (`bone_viewer.py`):** `GeodesicRenderer` was greedily consuming events, starving the logs. `render_frame` now accepts `current_events` as an argument.
- **The Leverage Point (`bone_main.py`):** `GeodesicOrchestrator` now acts as the single source of truth for event retrieval.

### 🦺 Safety Nets

- **Panic Room Types (`bone_main.py`):** Fixed inconsistent return types (dicts vs objects) causing secondary crashes during recovery.
- **Session Guardian:** Stripped down for ephemeralization. Now delegates to `BoneAmanita.emergency_save()`.

### 🧠 The Brain & Observability

- **Latency Metrics (`bone_brain.py`):** Removed internal timing logic from `TheCortex`.
- **External Audit (`bone_main.py`):** Hoisted timing logic to the main loop. The Observer now watches the Brain from the outside.

### 🆔 Identity & Config

- **Schrodinger's User:** Fixed race condition where the user existed as `None` and `Traveler` simultaneously.
- **Config Validation (`bone_bus.py`):** Added `_validate_ranges()` to clamp configuration values to sane limits.

---

## v10.2.5 - "The Tensegrity Update"

**Focus:** Cognitive Clarity, Memory Leaks, and Color Physics.

### 🧠 The Pinker Lens (Cognition)

- **Naming Consistency:** Exorcised the typo "OLLM" vs "OLLAMA" in `BoneConfig`.
- **Identity Crisis:** Replaced `user_name` string with a robust `user_profile` dictionary in `CycleContext`.

### 🌐 The Fuller Lens (Efficiency)

- **Memory Leak (`bone_bus.py`):** Replaced `EventBus` infinite list with `collections.deque` (circular buffer). The "Bathtub" now has a drain.
- **Color Bleeding:** `Prisma.paint` is now aware of nested resets, allowing Red text inside Green text without unraveling the universe.

### ⚖️ The Meadows Lens (Dynamics)

- **Ghost Data:** Formally added `audit_trail`, `raw_text_display`, and `entropy` to `PhysicsPacket`.
- **Split Brain:** Wired `SystemHealth` to `TheObserver`. Dashboard metrics now reflect reality.

### 🍩 The Schur Lens (Manners)

- **Polite Memory:** Gave `MycelialNetwork` a `report_status()` method so the main loop stops rifling through its pockets.

---

## v10.2.4 - "The Lucid Dream"

**Focus:** Cognitive Integrity and Systemic Logic.

### 🧠 Cognitive Integrity

- **Recursion Fix (`SemanticFilter`):** Fixed infinite loops in fractal generation by making the method stateless.
- **Entropy Vent:** Implemented **symmetric edge deletion**. If `A -> B` is severed, `B -> A` is now also severed to maintain Tensegrity.

### 🏗️ Structural Stability

- **Mass Calculation (`TheTensionMeter`):** Fixed `gaze()` reporting `mass: 0`. The engine now calculates gravitational mass based on historical edge weights.
- **Zone Inertia:** Added bounds checking to ensure the "Aerie" zone doesn't accidentally punish speed bonuses.

### 🎭 Epistemic Transparency

- **Humility Audits:** The system now logs _why_ it modified user text (e.g., "Adding humility due to high voltage").
- **Starvation Protocol (`TheTangibilityGate`):** The system lowers its density standards by 50% when stamina is low, rather than accepting pure noise.

---

## v10.2.3 - "The Physics Patch"

**Focus:** Fixing Critical Bugs in the Physics Engine.

### ⚙️ Physics Logic

- **EntropyVent:** Complete rewrite to prevent graph corruption. Replaced fragile iterator logic with `random.sample()`.
- **SemanticFilter:** Resolved infinite recursion in `_execute_fractal`.
- **TheTensionMeter:** Implemented real Graph Mass calculation. History now has weight.

### 🛡️ Guardrails

- **Audit Trail:** `RuptureValve` now stamps modification reasons onto the physics packet.
- **Survival Curve:** Implemented a metabolic curve for input density requirements based on current stamina.

---

## v10.2.2 - "The Genesis Protocol"

**Focus:** Startup Logic and Configuration.

### 🚀 Genesis

- **Dictionary Map:** Replaced brittle `if/elif` chains in `bone_genesis.py` with a robust provider map.
- **Soft Start:** Initial user confidence set to **25%** instead of 100%. Identity is now a hypothesis, not a fact.
- **Anti-Fragility:** Wrapped config loading in a `try/except` harness. The system fails forward into default settings if `bone_config.json` is corrupt.

---

## v10.2.1 - "The Polite Council"

**Focus:** Refactoring the Advisory Board.

### 🏛️ The Council

- **Proportional Control:** `TheLeveragePoint` now applies proportional dampening (30% of excess voltage) rather than a hard crash.
- **Recursion Fix:** `TheStrangeLoop` now decrements depth when loops are _not_ detected (The "Infinite Bathtub" bug).
- **Semantic Footnotes:** `TheFootnote` now uses a context map to attach relevant jokes to logs.

---

## v10.2.0 - "The Soul Update"

**Focus:** From Homeostatic Survival to Teleological Becoming.

### ✨ The Soul Layer

- **Narrative Self (`bone_soul.py`):** Added Core Memories, The Editor (Super-Ego), and Obsessions (Teleology).
- **Traits:** Dynamic personality values (Hope, Cynicism, Curiosity) that evolve based on interaction.

### 🧬 Transmigration

- **Spore Legacy (`bone_spores.py`):** Spores now serialize the Soul. Reincarnation preserves traits and unfinished business.
- **Deep Save:** `/save` command now captures the complete soul state.

### 🖥️ Interface

- **Soul Strip:** Added a UI section for Obsession Progress and Current Chapter.
- **Commands:** Added `/soul`, `/chapter`, and `/prove`.

---

## v10.0.5 - "Codename: W H I M S Y"

**Focus:** Adult Supervision and Icarus Mechanics.

### ⚖️ The Council

- **New Module:** `bone_council.py` established.
- **Market Correction:** Added logic to detect "Static Flow" (coasting on high energy/low friction) and artificially inflate Drag.

### ⚡ Physics

- **Icarus Risk:** Perfection streaks now accumulate risk.
- **ICARUS_CRASH:** New event that resets Voltage and applies trauma if hubris gets too high.

### 🎨 Whimsy

- **Tie-Dye:** Added `Prisma.tie_dye()` for chaotic text coloring.
- **Judgmental Observer:** Telemetry now judges you ("SUSPICIOUSLY EFFICIENT").
- **Honk Protocol:** The EventBus can now beep.

---

## v10.0.4 - "Unofficial Patch"

**Focus:** Stability and Tone.

### 🐛 Stability

- **Spores:** Fixed crash on `load_spore`.
- **Cosmic Dynamics:** Fixed crash on startup initialization.
- **Manic Fracture:** Dampened structure scores for short inputs to prevent false-positive shattering.

### 🧠 The Brain

- **Inventory:** Moved inventory list to Context to stop the AI from obsessing over rocks.
- **Output:** Unshackled token limits. Removed artificial brevity constraints.

### 🎭 Tone

- **Anxiety Reduction:** "LOW" pacing is now "Relaxed," not "Depressed."
- **Repetition:** Stopped the AI from constantly describing the floor as "Solid."

---

## v10.0.3 - "The Somatic Library"

**Focus:** Modularization and Biological Integration.

### 📚 Data Structure

- **Somatic Library:** Moved `TONE`, `PACING`, `SENSATION` definitions to `bone_data.py`.

### 🗣️ Translation

- **Biological Integration:** `RosettaStone` now reads Cortisol, Adrenaline, and ATP.
- **Buffer Zones:** Added intermediate states (e.g., `TRANSITION_UP`) to smooth personality shifts.
- **Combinatorial Logic:** Added complex states like `MAGMA` (High Voltage + High Drag) and `SUBLIMATION` (High Drag + High Entropy).

---

## v10.0.2 - "The Circuit Breaker"

**Focus:** Structural Integrity and Input Hygiene.

### 🛡️ Security

- **The Jeremy Jamm Filter:** Hardened regex for user names to prevent injection attacks.
- **Prompt Containment:** Sanitized user input to prevent prompt injection.

### 🔌 Connectivity

- **Semantic Retries:** Distinguishes between "Busy" (Retry) and "Unauthorized" (Abort) errors.
- **Pidgin Protocol:** Graceful fallback to literal interpretation if `RosettaStone` fails.
- **Diegetic Mocking:** When offline, the system generates atmospheric "Placebo" responses instead of leaking error logs.

---

## v10.0.1 - "The Marie Kondo Patch"

**Focus:** Configuration and Ephemeralization.

### 🧹 Efficiency

- **The Reaper:** `MycelialNetwork` now cannibalizes old nodes if the graph exceeds capacity.
- **Bounded History:** Lineage log converted to a `deque`.

### ⚙️ Configuration

- **SSOT:** `BoneConfig` is now the Single Source of Truth.
- **Active Loading:** Config now loads immediately on launch.

---

## v10.0 - "The Good Place"

**Focus:** Ephemeralization, Cognitive Persistence, Structural Decoupling.

### 🚀 Major Features

- **The Rosetta Stone:** A translation layer converting math (Physics) into language (Somatic State).
- **Hive Mind:** `cortex_hive.json` for persistent vocabulary learning.
- **Reverse Index:** O(1) complexity for word lookups.
- **Genetic Config:** `ALMANAC_DATA` and Ancestral Knowledge bonuses.

### 🧬 Summary of Impact

| Metric        | v9.9.8 (Old)   | v10.0+ (New)        | Note                                 |
| ------------- | -------------- | ------------------- | ------------------------------------ |
| **Cognition** | Hardcoded Math | **Semantic Bridge** | Physics translates directly to Tone. |
| **Lookup**    | Linear (Slow)  | **Constant (Fast)** | "Is 'rock' heavy?" is now instant.   |
| **Memory**    | Amnesiac       | **Persistent**      | Remembers "fluff" = "antigen".       |
| **Style**     | Spaghetti      | **Modular**         | Logic and Data strictly separated.   |

## v9.9.8 - "The Ron Swanson Patch"

**Focus:** Input Hygiene, Network Resilience, and "Meat & Potatoes" Validation.

### 🧠 The Pinker Lens (Network & Connectivity)

- **URL Sanitation:** Removed arbitrary `rstrip('/')` logic. The system now respects exact user input for API endpoints, establishing a consistent grammar.
- **Timeouts & Retries:** Refactored `_http_generation_with_backoff`. Implemented dynamic timeouts and reduced `MAX_RETRIES` to 1. No more "DMV Effect" (22s hangs).

### 🌐 The Fuller Lens (Security & Identity)

- **Injection Hardening:** Added a **Sanitization Barrier** to strip dangerous characters (`<`, `>`, `{`, `}`).
- **The No-Fly List:** Explicitly blocks reserved names ("System", "Admin", "Root") to prevent semantic injection attacks.
- **Strict Mode:** Name recognition (`"I am..."`) now requires Capitalized Words Only to prevent the system from naming the user "Tired" or "Ready."

### 🍩 The Schur Lens (Resilience & Context)

- **Leaky Bucket Algorithm:** Replaced binary solipsism checks with analog pressure. Diverse outputs slowly relieve pressure (-0.5) rather than instantly resetting it. You cannot "game" therapy.
- **Mock Mode Safety:** `_execute_plain_mode` now explicitly calls `mock_generation`, ensuring Safe Mode actually works when the brain is severed.
- **Context Awareness:** The Prompt Composer now receives `time`, `location`, and `recent_logs`, preventing the LLM from hallucinating a sunny day at midnight.

### 🛠️ System Integrity

- **Robust Uplink:** Refactored validation to use **Semantic Detection** (scanning for "refused", "timeout") rather than fragile uppercase string matching.
- **Config Hygiene ("The Costanza Wallet"):** If a config file is stale, the system now overwrites it with `SAFE_CONFIG` _before_ asking the user, preventing dirty data from surviving a crash.
- **Cloud Democratization:** Decoupled "Cloud" from "OpenAI." Users can now specify custom endpoints (Azure, Groq) and target models (`llama3-70b`).

---

## v9.9.7 - "The Cognitive Resilience Patch"

**Focus:** Error Standardization and Atomic Memory.

### 🧠 The Neural Cortex (`bone_brain.py`)

- **Standardized Errors:** Replaced loose string matching with Class Constants (`ERR_CONNECTION`). The brain now speaks clearly when it fails.
- **Cognitive Resilience:** Implemented exponential backoff (1s → 2s → 4s) for network calls. We are doing more with less wasted connection time.

### 🔌 The Genesis Protocol (`bone_genesis.py`)

- **Probe Disambiguation:** Logic now distinguishes between the _Probe URL_ (Ping) and _Chat Endpoint_ (Generate).
- **Patience Buffer:** Increased ping timeout to **3.0s**. We stopped punishing users for having slow Wi-Fi.
- **Feedback Loop:** The setup wizard now explains _why_ a connection failed (color-coded), rather than just saying "No."

### 🍄 The Mycelium Memory (`bone_spores.py`)

- **Fixed "The Time Eater":** Inverted logic in `cleanup_old_sessions`. The system now correctly prunes the **oldest** files, not the newest.
- **Atomic Writes:** Implemented "Write-Temp-Then-Move." Spores are fully written to `.tmp` before being renamed, preventing corruption during a crash.

---

## v9.9.5 - "The Syntax of Soul"

**Focus:** Strict Typing and Ephemeralization.

### 🧠 The Pinker Lens (Cognition)

- **Strict Contracts:** Enforced `-> str` return typing on `_http_generation`. The body no longer writes checks the brain can't cash.
- **Antecedent Fix:** `export_system_prompt` now imports `LEXICON` before speaking, preventing `NameError` on undefined terms.

### 🌐 The Fuller Lens (Efficiency)

- **Ephemeralization:** Removed duplicate `world` key in `_gather_state`. The map is now efficient; we don't fetch inventory data twice.
- **Widening the Pipe:** `SomaticLoop` now accepts `Dict[Any]` for nutrient profiles, acknowledging that the system digests _Meaning_ (String) as well as _Energy_ (Float).

### 🍩 The Schur Lens (Humanity)

- **The "Ben Wyatt" Panic:** Calmed the `EndocrineSystem` down. It no longer crashes when trying to file a "feeling" in a "spreadsheet" column.
- **The "Jerry Gergich" Error:** Fixed a stutter where the Cortex announced "Here is the World!" twice.

---

## v9.9.3 - "The State Machine"

**Focus:** Boot Logic and Safe Modes.

### 🏛️ Architecture

- **State Machine Boot:** Refactored launch into `BOOT` → `DETECT` → `VALIDATE` → `LAUNCH`. Failure domains are now isolated.
- **Pre-Flight Validation:** `launch()` re-validates the config every time. Stale data from a previous crash is rejected.

### 🧠 Cognition

- **Semantic Failure:** `validate_brain_uplink` now checks for specific cognitive signatures (`[NEURAL UPLINK SEVERED]`) rather than vague words like "error."

### 🦺 Safety Nets

- **The "Janet" Protocol:** If the backend fails, the system defaults to `Mock Mode` with a polite notification, rather than silently exiting. The user always has a toy to play with.

---

## v9.9.2 - "The Jeremy Bearimy Update"

**Focus:** Cognitive Friction, Tensegrity Loops, and Point Systems.

### 🧠 The Cognitive Layer

- **Syntax Tree:** `TheLexicon` now parses grammatical relationships, not just atomic weights.
- **Curse of Knowledge:** The system rewrites heavy jargon ("paradigm", "leverage") into plain English before processing.
- **Contextual Guessing:** Unknown words are guessed as "Abstract" or "Concrete" based on context clues.

### 🌐 The Systems Layer

- **Tensegrity Loops:** Perception, Metabolism, and Simulation now run in parallel.
- **Cannibalism:** If `MitochondrialForge` fails, the system cannibalizes its own history (`TheFolly`) to keep the lights on.
- **Spaceship Earth:** Unused variables in `CycleContext` are recycled into ATP.

### 🍩 The Human Layer

- **The "Chidi" Check:** If the system detects overthinking (High Loop, Low Output), it pauses to ask: _"Are you stalling?"_
- **The "Janet" Protocol:** You can now ask for things. A request for a "cactus" returns the _essence_ of a cactus (High Friction, Low Water).
- **Public Parks:** We now hold "Festivals" when Dopamine/Oxytocin hit peak levels.

---

## v9.8.2 - "The Ron Swanson Hard Fork"

**Focus:** Constitutional Logic and Bureaucracy Reform.

### 🧬 The Wetware (`bone_biology.py`)

- **The Cortex Hypervisor:** Transformed `TheCortex` from a passive monitor to an active Hypervisor.
- **Plain Mode:** `??status` bypasses the narrative engine entirely.
- **Ballast Timeout:** "Ballast" is now a 3-turn timeout system. Failure to ground results in a forced reset.

### 🏘️ The Village (`bone_village.py`)

- **Bureau Reform:** `audit()` now returns `TAX` (Fine) or `BLOCK` (Halt). Low-voltage inputs incur a fine but don't stop the world.
- **Enneagram Safety:** Hardcoded fallback maps ensure personalities persist even if the data core corrupts.

### ⚙️ The Engine

- **Executive Control:** `TheCortex.process` is the sole entry point. The Hypervisor cannot be bypassed.
- **Style Consequences:** Violating `StrunkWhiteProtocol` taxes "Shimmer" reserves. Bad writing now has a metabolic cost.

---

## v9.8.0 - "The Glimmer Update"

**Focus:** Narrative Resonance and Documentation.

### 🚨 Critical Systems

- **Refactored Orchestrator:** Dismantled the "God Object" in `_phase_simulate`. Logic delegated to `_process_navigation`, `_operate_machinery`, etc.
- **Categorized Help:** `/help` now sorts commands by intent (CORE, WORLD, ACTION, DEBUG).

### 🧬 Biology

- **Glimmers:** `EndocrineSystem` now detects "Glimmers" (moments of high structural integrity).
- **Parks Reform:** `PublicParksDepartment` requires a verified Glimmer to commission art. No more empty statues.

### 🌐 World & Identity

- **The Style Guide:** New artifact. Reduces Narrative Drag by -1.0. Enforces clarity.
- **Identity:** Boot sequence announces "Glimmer Protocols Active."

---

## v9.7.9 - "The Circulation Update"

**Focus:** Closed Loops and Epigenetics.

### 🌐 The Fuller Lens

- **Civic Pride:** `dedicate_park()` now returns a "Core Thought." Building a park grants **+15 Stamina** and seeds the thought back into memory. Output becomes Input.
- **Real-Time Epigenetics:** Parent systems now adopt 50% of a child spore's mutations immediately. Lamarckian evolution is live.

### 🍩 The Schur Lens

- **Joy Clades:** `MycelialNetwork` saves the dominant "Flavor of Joy." Future sessions inherit buffs based on ancestral happiness.

---

## v9.7.7 - "The Knope Protocol"

**Focus:** Active Agency and Inventory.

### 🗺️ The Cartographer

- **ASCII Weaving:** The map is no longer text; it is a 7x7 procedural grid.
- **Terrain:** Vectors translate to tiles (Mountains `▲`, Void `.`, Highways `=`).

### 🪞 The Mirror

- **Active Bureaucracy:** The Mirror taxes you based on archetype.
- **WAR:** Drag x1.5, Loot x2.0.
- **ART:** Voltage Cap 10.0, Plasticity x2.0.
- **LAW:** Loot Chance 0%, Drag x0.8.

### 🎒 The Janitor

- **Rummage:** New command `/rummage`. Dig for items based on physics vectors.
- **Pawnee Items:** Added `WAFFLE_OF_PERSISTENCE` and `BINDER_OF_VIGILANCE`.

---

## v9.6.0 - "The Geodesic Shift"

**Focus:** Cognitive Topology and Humility.

### 🌐 VSL Core

- **Geodesic Engine:** Replaced valve logic with a Geodesic Engine.
- **Manifolds:** System locates itself in 5 regions: `THE_MUD`, `THE_FORGE`, `THE_AERIE`, `THE_GLITCH`, `THE_GARDEN`.

### 🛐 Ethics

- **Humility Engine:** Implemented `ComputationalHumility`. High-voltage assertions about "The Future" or "The Soul" are automatically softened.
- **Arrogance Damping:** High Voltage (>15v) triggers stricter checks.

---

## v9.0.0 - "The Graduation"

**Focus:** Autophagy and Aggressive Neuroplasticity.

### 🩸 Metabolism

- **Autophagy:** If ATP < 10.0, the system **eats its own memories** (deletes nodes) to survive. Neglect has a permanent cost.

### 🧠 Cognition

- **Voltage-Gated Learning:** If Voltage > 5.0, the system overrides the dictionary. It accepts unknown words as valid because you said them with conviction.

### 🛑 Defense

- **The Glitch:** Refusal is now an attack. It spawns a `Toxic Node` in the graph that degrades future processing until pruned.
