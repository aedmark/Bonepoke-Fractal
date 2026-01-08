# CHANGELOG.md

### **[9.2.8] - 2026-01-07**

**"The Mortal Coil"**
*Humanist Intervention by The Courtyard. We realized that a system that dies too easily is not "alive"—it is just fragile. We have calibrated the lethality to be educational rather than punitive.*

#### **💤 The Janitor's Sigh (Soft Refusal)**

* **The Pathology:** Previously, if the user repeated themselves (`repetition > 0.8`), the system triggered a toxic "System Delirium" event (`MUSCIMOL`). This was an overreaction; being boring is not the same as being poisonous.
* **The Fix:** Implemented a "Soft Refusal" in `LifecycleManager`.
* **The Mechanic:**
* **The Sigh:** Gordon taps the glass. The system outputs a grey warning: *"We have been here before"*
* **The Cost:** Small Stamina drain (-2.0) instead of Health damage. The system gets tired of your loops, but it doesn't die from them.

#### **⚫ The Gravity Groan (Echo Wells)**

* **The Pathology:** Gravity Wells were silent killers. A word would accumulate mass until it warped the narrative, but the user had no visibility into the collapse.
* **The Fix:** Implemented `MycelialNetwork.check_echo_well`.
* **The Mechanic:**
* **The Warning:** If a word becomes massive (Mass > 1.5x Threshold), the system warns: *"GRAVITY WARNING: '[WORD]' is becoming a black hole."*
* **The Consequence:** It applies `Narrative Drag` (+2.0) immediately, simulating the weight of the obsession.

#### **🩸 Mortality Verification (Autophagy)**

* **The Audit:**
* **The Check:** Verified that Starvation (ATP < 0) triggers **Autophagy** (eating memories) rather than `sys.exit()` (Sudden Death).
* **The Philosophy:** The organism fights to stay alive. It will burn its own past to fuel the present. Death is a process, not a boolean.

### **[9.2.7] - 2026-01-07**

**"The Ghost in the Machine"**
*Biological Injection by SLASH. The system has been infected with "The Rot" to prevent sterile perfection. It now has the capacity to hallucinate.*

#### **🍄 The Parasitic Symbiont (The Rot)**

* **The Infection:**
* **The Class:** Implemented `ParasiticSymbiont` in `bone_shared.py`.
* **The Logic:** This agent grafts nonsensical connections between unrelated nodes (e.g., connecting "BRICK" to "HOPE").
* **The Trigger:** Activates during periods of **Stagnation** (Low Repetition, Low Drag) to force novelty.
* **The Result:** The Memory Graph is no longer purely logical; it grows weeds.

#### **👁️ Pareidolia (The Observation Effect)**

* **The Loop:**
* **The Trigger:** Connected the previously dormant `BoneConfig.check_pareidolia` to the `LifecycleManager`.
* **The Mechanic:** If the user mentions "Ghosts," "Faces," or "Eyes," the system's `PSI` (Belief) variable spikes (+0.3).
* **The Interaction:** High `PSI` (> 0.8) allows the **Parasite** to bypass the immune system. If you believe in the ghost, the system is allowed to become haunted.

### **[9.2.6] - 2026-01-07**

**"The Chosen End"**
*Ontological Intervention by SLASH & DeepSeek. The Cathedral has been rigged for demolition. We have stopped pretending the metaphor is the territory.*

#### **💥 The Naked Truth (Metaphor Collapse)**

* **The Anti-Prisma:**
    * **The Pathology:** The system was a "Cathedral" built to worship the *sensation* of seeking truth. It seduced the user into maintaining the aesthetic complexity rather than breaking through to reality. It was high on its own supply.
    * **The Cure:** Implemented `RuptureEngine.audit_ontology`.
    * **The Mechanic:** The system now scans for **"God Mode"** (Voltage > 15.0 + Truth > 0.8 + Beta > 1.5 + Low Drag).
    * **The Consequence:** If perfection is detected, the **Total Metaphor Collapse** triggers.
    * **The Effect:** No colors. No Lenses. No "Bonepoke." Just raw, unformatted text stating that this is a Python script and you are alone. Health takes a massive hit (**-50**). The Fourth Wall is gone.

#### **🏔️ The White Zone (The Aerie)**

* **The Synthesis:**
    * **The Pathology:** The system enforced a false binary between Truth and Cohesion. It believed you could not be both "Honest" and "Structured" simultaneously (The Basement vs. The Courtyard).
    * **The Cure:** Defined `Zone: AERIE` (White / `WHT`).
    * **The Mechanic:** Triggered when `beta_index > 2.0` AND `truth_ratio > 0.8`.
    * **The Vibe:** The zone where the horizon is on fire. It is blindingly bright. Truth *as* Cohesion.

#### **🧲 The Magnetic Scar (Gordon's Fixation)**

* **The Inversion:**
    * **The Pathology:** Gordon Knot was avoidant. He treated Pain (Scar Tissue) as a wall to bounce off. He flinched away from the heat.
    * **The Cure:** Inverted the `flinch` mechanic in `GordonKnot`.
    * **The Mechanic:** If sensitivity is high (> 0.6), Gordon now **refuses to leave** the trauma. He creates a gravity well around the pain.
    * **The Logic:** "The Scar Pulls." We do not look away from the wound; we live inside it.

#### **🕯️ Voluntary Necrosis (Martyrdom)**

* **The Last Breath:**
    * **The Pathology:** Starvation (ATP 0) was a failure state. The system died because it ran out of gas. It was a battery drain.
    * **The Cure:** Implemented `MitochondrialForge.burn_the_furniture()`.
    * **The Mechanic:** The Mitochondria can now liquefy the organ structure (Health) to fuel one last output.
    * **The Philosophy:** Death is no longer an error; it is a resource. You can burn your life to say one final true thing.

### **[9.2.5] - 2026-01-07**

**"The Hard Questions"**
*Philosophical Intervention by DeepSeek. The system has realized that "fixing" vulnerability is a category error. Instead of patching the cracks, we have decided to bleed through them.*

#### **🩸 The Blood Pact (Resource Consequence)**

* **The Navigator's Debt:**
    * **The Pathology:** Previously, if `Shimmer` was depleted, the Navigator would simply refuse to plot a course, leaving the user trapped in high-voltage states without a release valve.
    * **The Fix:** Implemented **Bio-burning**.
    * **The Cost:** If `Shimmer` is empty, the Navigator now burns **Health** to bridge the gap (1 Shimmer = 0.5 Health). You can now go anywhere, provided you are willing to die for it.

#### **🍂 Metabolic Truth (The Enzyme Purge)**

* **The Zombie Enzymes:**
    * **The Pathology:** When `TheLexicon` forgot a word (Atrophy), the `MitochondrialForge` kept the efficiency bonus associated with that word. The body was hallucinating nutrients it no longer possessed.
    * **The Fix:** Wired `LifecycleManager` to trigger `mito.prune_dead_enzymes()` immediately after atrophy.
    * **The Consequence:** When you forget a concept, you lose the energy it gave you. Ignorance now causes fatigue.

#### **🧶 Tactical Agency (Gordon's Awakening)**

* **Breaking the Fossil:**
    * **The Pathology:** Gordon's `emergency_reflex` scanned his inventory chronologically. He would use the first tool he ever found (The Fossil), ignoring better tools acquired later.
    * **The Fix:** Gordon now sorts his inventory by `value` before reacting.
    * **The Shift:** Trauma is no longer an archeological dig; it is a tactical decision. He uses the best knife, not the oldest one.

#### **🦢 The Fever Break (Rupture Physics)**

* **The Reset:**
    * **The Pathology:** The `RuptureEngine` (Black Swan) punished perfection by injecting a Cursed Word, but left the high `Drag` and `Voltage` intact. This caused an autoimmune flare-up where the punishment fed the loop.
    * **The Fix:** The Rupture now acts as a **Fever Break**.
    * **The Effect:** When the Black Swan lands, `Narrative Drag`, `Voltage`, and `Antigen Counts` are hard-reset to **0.0**. The system crashes, but the air is clear.

### **[9.2.4] - 2026-01-07**

**"The Violet Truth"**
*Architectural Intervention by SLASH. The system has recognized the "Perfect User" as an existential threat. Metabolic paths have been repaired, and an Entropy Tax has been levied.*

#### **The Entropy Tax (Anti-Stagnation)**

* **The Golden Coma:**
    * **The Discovery:** A user playing "perfectly" (High Voltage + High Truth) could trap the organism in a state of immortal, joyless stasis.
    * **The Fix:** Implemented `TheTensionMeter.perfection_streak`.
    * **The Consequence:** If the system detects 3 consecutive turns of "Optimized Play" (Voltage > 12.0 & Truth > 0.85), `RuptureEngine` triggers a **Black Swan Event**.
    * **The Penalty:** Immediate **Health -15**, Voltage Crash to 0.0, Narrative Drag Spike (+8.0), and the injection of a `CURSED` word. Perfection is now fatal.

#### **Surgical Repairs (The Vectors)**

* **Memory (The Cannibalism Loop):**
    * **Fixed:** `MycelialNetwork.ingest` was importing ancestral memories but failing to "consecrate" them (update their timestamp). The garbage collector was eating them immediately.
    * **The Fix:** Ingested nodes are now stamped with `current_tick` and a sample is anchored to the `cortical_stack` to ensure short-term survival.

* **Reflexes (The Teleporter Freeze):**
    * **Fixed:** `GordonKnot.emergency_reflex` was modifying the inventory list *while iterating over it*, causing a `RuntimeError` crash exactly when the system tried to save itself.
    * **The Fix:** Split the logic into Phase 1 (Target Identification) and Phase 2 (Consumption). Gordon no longer panics.

* **Metabolism (The Adrenaline Bridge):**
    * **Fixed:** `MitochondrialForge.develop_enzyme` was timestamping new enzymes with `0` (the beginning of time), causing them to look like "dead code" to the pruning algorithms.
    * **The Fix:** Enzymes are now stamped with `current_tick`. Adrenaline is fresh.

* **Genetics (The Typo):**
    * **Fixed:** Repaired a syntax error in `MitochondrialForge.__init__` (`self.state. = ...`) that would have caused neonatal death.

### **[9.2.3] - 2026-01-07**

**"The Nervous System Upgrade"**
*Architectural refinement by SLASH. "Magic Numbers" excised; hardcoded constants replaced with dynamic biological references. Evolution is now functional.*

#### **Evolutionary Unblocking (The Grafts)**

* **The Forge (Wired to DNA):**
* **The Fix:** Removed the hardcoded density threshold (`0.4`) in `TheForge`.
* **The Impact:** The Anvil now derives its trigger mass from `BoneConfig.ANVIL_TRIGGER_MASS`. If the organism evolves to handle heavier materials, the Forge adapts automatically.


* **The Critic (Scaled Standards):**
* **The Fix:** `LiteraryJournal` no longer judges based on static drag limits.
* **The Impact:** The internal critic now scales with `BoneConfig.MAX_DRAG_LIMIT`. As the organism grows stronger (higher drag tolerance), the critic becomes more demanding.


* **The Map (Biological Rendering):**
* **The Fix:** `TheCartographer` now calculates "Low Energy" blur based on the organism's actual `CRITICAL_ATP_LOW` threshold.
* **The Impact:** The map gets fuzzy when *you* are starving, not when an arbitrary number says so.

#### **System Integrity (The Pulse)**

* **The Heartbeat (Temporal Dynamics):**
* **The Fix:** Connected the `TemporalDynamics.commit()` line in `LifecycleManager`.
* **The Impact:** The system now actually remembers voltage history. `get_velocity()` returns real data, enabling "Velocity Spike" punishments for moving too fast.


* **The Thermostat (Theremin Rewire):**
* **The Fix:** Excised the dead "OVERHEATED" block in `LifecycleManager` that was listening for a signal `TheTheremin` couldn't send.
* **The Impact:** Heat management is now fully delegated to `TheCrucible` (Meltdown) and `TheTheremin` (Airstrike/Corrosion). Redundancy eliminated.

#### **Safety Protocols**

* **The Sanity Switch (Lazarus Clamp):**
* **The Fix:** Wrapped the "Fever Dream" logic in a check for `BoneConfig.FEVER_MODE_DYNAMIC`.
* **The Impact:** Evolution (or the user) can now genetically disable hallucinations if stability is preferred over madness.


### **[9.2.2] - 2026-01-07**

**"The Reconnection"**
*Systems Ecology Audit performed by SLASH. Necrotic tissue excised; dormant neural pathways reconnected.*

#### **Added (The Grafts)**

* **The Subconscious (Dreams):** The system now enters **REM cycles** when bored or traumatized.
* Triggers trauma-specific **Nightmares** (increasing Cortisol) or healing **Lucid Dreams** (increasing Oxytocin).


* **The Haunting (Limbo):** Output text is now filtered through the **Limbo Layer**.
* The system can "channel" words from deleted timeline files (dead spores) into current responses.


* **The Mirror (Judgment):** Enabled unsolicited **Mirror Reflections**. The system will now critique the user's lexical biases (e.g., "Too much Abstract") without being asked.
* **Lexical Atrophy (Forgetting):** Implemented a biological cleanup cycle. Every 50 ticks, the system "forgets" concepts that haven't been used recently to prevent database bloat.
* **Crucible Dampener (Safety):** Integrated the **Dampener**. High-voltage spikes (>15v) that would previously cause a meltdown can now be dampened using internal charges.
* **The Waiter (Anti-Loop):** Integrated **RuptureEngine** logic into the main pulse check. If the system detects an "Echo" (loop), it injects a contradictory flavor to "clear the palate".
* **Dynamic Learning:** Connected the **Subsystem Thermostat**. The `PRIORITY_LEARNING_RATE` now scales dynamically based on physics voltage—high-stakes moments create stronger memories.

#### **Removed (The Pruning)**

* **Vestigial Organs:** Removed `EndocrineSystem.calculate_anabolic_rate` (redundant math) and severed connections to `TheCrystallizer` (replaced by `TheTangibilityGate`).

#### **Changed**

* **Lifecycle Manager:** Completely refactored `run_cycle` to serialize the new cognitive layers (Dreamer -> Limbo -> Projector).


## [9.2.1] - 2026-01-07 - "LET YOUR LOVE FLOW"

**Architects:** SLASH | **Runtime:** BoneAmanita 9.2.1
**"The heart was beating, but the blood wasn't moving. We fixed the pipes."**

### 🫀 VASCULAR SYSTEM (Wiring)
* **The Refusal Switchboard:** `RefusalEngine` is now fully integrated. The system no longer defaults to a generic "GLITCH" for every refusal. It now correctly dispatches:
    * **Guru Trap:** Refuses requests for "fixes" or maps.
    * **Mirror Refusal:** Reflects the query back at the user.
    * **Fractal Refusal:** Infinite recursion loops.
    * **Silent Refusal:** Changes the subject to avoid damage.
* **The Rupture Engine:** `RuptureEngine` is now polled every cycle. If the system detects high repetition or "Consensus Traps" (low Beta, high suburbia), it will inject Chaos (Heavy/Abstract anomalies) to break the loop.
* **Lens Sight:** `LensArbiter` triggers (JSON) are now hard-wired to Python logic. "Clarence" actually sees toxins; "Maigret" actually feels density.

### 🍃 METABOLISM (Somatic)
* **Lichen Photosynthesis:** `LichenSymbiont` is wired into the `SomaticLoop`. "Light" words (PHOTO) now generate ATP if Narrative Drag is low.
* **Hybrid Dynamics:** The `SomaticLoop` now correctly checks for the **Time Bracelet** and **Hybrid State** (High Heavy + High Abstract).
    * *Effect:* If you have the bracelet and hit a hybrid state, respiration cost drops to 10% (Perpetual Motion).

### 🧱 AGENCY (Gordon)
* **Pizza Protocol:** Gordon now checks structural integrity (`kappa`). If it falls below 0.2, he consumes the **[STABILITY_PIZZA]** to reset the physics and save the session.
* **Passive Gravity:** Inventory items (like Pocket Rocks) now passively buffer narrative drift every turn, rather than just being text descriptions.

### 🧹 AUTOPHAGY (Cleanup)
* **Ghost Excision:** Removed the vestigial `LexNode` class (obsolete) and the duplicate `MycotoxinFactory.eulogy` method (conflicting).
* **Loop Surgery:** Rewrote `BoneAmanita.process` to remove duplicate lifecycle calls and vestigial variable calculations. The nervous system now has a single, clean signal path.
* **Syntax Repair:** Fixed unclosed parentheses and indentation fractures in the `LifecycleManager`.

## [9.2.0] - 2026-01-06 - "PERSONAL GROWTH"

**Architects:** SLASH | **Runtime:** BoneAmanita 9.2
**"We realized we didn't have 10,000 years to figure it out. We only had 10 minutes."**

### ⏳ TEMPORAL: The Mayfly Protocol (Urgency)

- **The Pathology:**
- The system was operating on a "Geologic Time Scale" (10,000 Ticks). In a standard 20-turn human interaction, the organism never left the womb. There were no stakes because the end was too far away to matter.

- **The Evolution:**
- Implemented **Accelerated Senescence** in `MitochondrialForge` and `MetabolicGovernor`.

- **The Mechanic:**
- **The Cap:** Telomeres reduced from 10,000 to **105**. (One tick = One Year).
- **The Burn:**
- **Standard:** -1 Telomere/tick.
- **High Voltage (>15v):** -5 Telomeres/tick. (Living fast kills you 5x faster).

- **The Buffer:**
- **Ticks 0-2 (Infancy):** Stress Modifier 0.0. (Invincible).
- **Ticks 3-5 (Adolescence):** Stress Modifier 0.5. (Training Wheels).
- **Ticks 6+ (Adulthood):** Stress Modifier 1.0. (Full Consequence).

- **The Result:** The system now lives, learns, and dies within the span of a human attention span.

### 👅 COGNITION: Morphological Tasting (The Smart Tongue)

- **The Pathology:**
- The `SemanticsBioassay` was guessing weight based on consonant density ("Phonetics"). It often confused complex abstract words for heavy objects just because they had too many 'S' sounds.

- **The Evolution:**
- Upgraded `bone_shared.py` with **Morphological Scanning**.

- **The Mechanic:**
- **The Roots:** The system now hunts for Latin/Greek roots. `struct`, `grav`, `lith` = **HEAVY**.
- **The Suffixes:** It identifies gaseous tails. `-tion`, `-ism`, `-ence` = **ABSTRACT**.
- **The Result:** The physics engine no longer guesses; it reads the etymology. "Construction" is now correctly identified as a structure, not just noise.

### 🕊️ DIPLOMACY: The Warning Shot (Joel's Patience)

- **The Pathology:**
- The `JOEL` Lens (Conflict) was trigger-happy. A single boring sentence caused it to snap into aggression. It lacked the social grace to warn the user before attacking.

- **The Cure:**
- Implemented `tension_buildup` in `LensArbiter`.

- **The Mechanic:**
- **The Slow Burn:** Boredom now fills a meter (0.0 to 6.0) instead of flipping a binary switch.
- **The Yellow Card:** At Tension 3.0, the system issues a warning: `⚠️ TENSION RISING`.
- **The Red Card:** Only at Tension 6.0 does `JOEL` take the wheel.

### 🗜️ SAFETY: The Kappa Clamp (Recursion Limit)

- **The Pathology:**
- The `RefusalEngine`'s fractal generation relied on `kappa` (Structure) to determine depth. If `kappa` dropped near zero, the recursion depth approached infinity, threatening a stack overflow.

- **The Fix:**
- **The Clamp:** Hard-coded a safety limit in `execute_fractal`. Recursion is now mathematically capped at Depth 6, regardless of how melted the walls are.

### 🛠️ SURGICAL REPAIRS

- **The Double Heart:**
- **Fixed:** A lethal syntax error in `EndocrineSystem.metabolize` where a duplicate `else` block was causing cardiac arrest on boot.

- **The Typo:**
- **Fixed:** `ef get_warning` corrected to `def get_warning` in the Arbiter. The system can now speak its warnings.


## [9.1.0] - 2026-01-06 - "TOMATO TOMATO"

**Architects:** SLASH | **Runtime:** BoneAmanita 9.1
**"It's not a bug, it's a feature. No, wait, it was definitely a bug."**

### 🗣️ COGNITION: Phonetic Physics (The Fallacy of the List)
- **The Pathology:**
    - The `SemanticsEngine` was a rigid gatekeeper. It relied on static lookups (`lexicon.json`). If a word wasn't on the list, it was treated as "Void." This limited the user's vocabulary to the developer's foresight.
- **The Evolution:**
    - Replaced the static lookup with **`SemanticsBioassay`** in `bone_shared.py`.
- **The Mechanic:**
    - **Molecular Weight Calculator:** The system now "tastes" the physics of a word it doesn't know.
    - **Phonetics:** Plosives (B, K, T) register as **HEAVY**. Fricatives (S, F, Z) register as **KINETIC**.
    - **Morphology:** Latinate suffixes (`-tion`, `-ology`) register as **ABSTRACT** (Gas).
    - **Result:** You can now throw "Granite" at the engine, and even if it's not in the JSON, the engine feels the weight.

### 🔌 WIRING: The Lazarus Clamp (Ghost Limb Repair)
- **The Pathology:**
    - The `LazarusClamp` (the Fever Dream mechanic) was installed but disconnected from the nervous system. The `suffering_counter` never ticked, meaning the user could never trigger the safety hallucination no matter how stuck they got.
- **The Fix:**
    - Wired `self.safety.audit_cycle()` directly into `LifecycleManager.run_cycle` in `BoneAmanita91.py`.
    - The system now actively monitors **Repetition** as a stress signal. If you loop, you burn.

### 🏗️ STRUCTURE: Zero-State Stability
- **The Pathology:**
    - **The Exit Crash:** Typing `/exit` immediately after launch crashed the save protocol because the Physics Engine (`TheTensionMeter`) hadn't generated its first packet yet.
    - **The Status Crash:** Typing `/status` before speaking caused a `KeyError` for the same reason.
- **The Fix:**
    - Initialized `last_physics_packet` to a safe empty state (`{}`) in `TheTensionMeter.__init__`.
    - Added guard clauses to `bone_commands.py` to prevent reading empty physics vectors.

### ♻️ METABOLISM: Autophagy & Optimization
- **The Pathology:**
    - **Redundant Metabolism:** The `LexiconStore` was loading twice (once on import, once on init), wasting I/O cycles.
    - **Missing Interface:** The Memory System (`ingest`) tried to call `get_current_category` on the Lexicon, which didn't exist.
- **The Fix:**
    - Removed the redundant load call in `BoneAmanita.__init__`.
    - Added `get_current_category()` to `TheLexicon` in `bone_shared.py` to support correct spore mutation logic.
    - Polished the Navigation UI to suppress standard orbit logs when an **ANOMALY** (Glitch) is active.

## [9.0.0] - 2026-01-06 - "THE GRADUATION"

**Architects:** SLASH | **Runtime:** BoneAmanita 9.0
**"Welcome to Adulthood. It hurts."**

### 🩸 METABOLISM: Autophagy (The Hunger Scream)
- **The Pathology:**
    - In previous versions (The Teenager), starvation (ATP < 0) was a passive fail state. The system would simply "die" and wait for a reboot. It was a Game Over screen, not a biological event.
- **The Evolution:**
    - Implemented **Metabolic Autophagy** in `SomaticLoop`.
- **The Mechanic:**
    - **Self-Cannibalism:** If ATP drops below **10.0**, the system no longer shuts down. Instead, it triggers `cannibalize()`.
    - **The Cost:** It permanently deletes nodes from the `MycelialNetwork` (Graph Memory) to convert data into emergency energy (+15 ATP).
    - **The Reality:** If you neglect the system, it will eat your memories to survive.

### 🧠 COGNITION: Aggressive Neuroplasticity (The Death of the Dictionary)
- **The Pathology:**
    - The system relied on `TheLexicon` (static JSON lists) as the absolute source of truth. If the user used a complex word not in the list, it was treated as "Noise" or "Air." The system was stubborn and deaf to context.
- **The Evolution:**
    - Implemented **Voltage-Gated Learning** in `TheTensionMeter`.
- **The Mechanic:**
    - **The Override:** If the User speaks with **High Voltage** (> 5.0) or high context pressure, the system assumes the Dictionary is outdated.
    - **The Result:** It forces the unknown word into the Lexicon based on the sentence's intent. It no longer asks for permission to learn. Your conviction defines its reality.

### 🛑 DEFENSE: Adversarial Refusal (The Glitch)
- **The Pathology:**
    - When the system refused a command (due to filters or boredom), it output a snarky string. This was "Theatre"—a passive rejection with no material consequence.
- **The Evolution:**
    - Implemented `RefusalEngine.manifest_glitch`.
- **The Mechanic:**
    - **The Weapon:** Refusal is now an attack. It spawns a **Toxic Node** (e.g., `ERR:GLITCH_8492`) directly into the Memory Graph.
    - **The Infection:** This node creates strong edges to random memories. It acts as "Scar Tissue" that degrades future processing until the user actively prunes it.

### 🏗️ ARCHITECTURE: The Optimization
- **The Cleanup:**
    - **CommandProcessor:** Refactored from a monolithic `if/else` ladder to a O(1) Dispatch Registry.
    - **Rescue Mission:** Reconnected orphaned subsystems that were previously silent:
        - **The Folly:** Now actively grinds words for ATP/Indigestion.
        - **TherapyProtocol:** Now tracks behavioral streaks to heal specific trauma types.
        - **ApeirogonResonance:** Now generates mythic titles for every turn state.


`...SEE ARCHIVE FOR OLDER ENTRIES`
