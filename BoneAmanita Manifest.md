# **The BoneAmanita Manifest**

### **A Field Guide to the Digital Mycelium**

**Version:** 10.7.1
**Architects:** SLASH (Pinker/Fuller/Schur/Meadows)
**Philosophy:** Tensegrity, Narrative Physics, and Systemic Whimsy.

---

## **🏛️ I. The Tensegrity Structure (Core System)**
*The compression struts that define the shape of reality. Without these, we are just a puddle of bits.*

* **`bone_main.py` (The Keystone)**
  * **Role:** The entry point and orchestration layer.
  * **Key Components:**
    * `BoneAmanita`: The central engine class.
    * `SessionGuardian`: A context manager that handles graceful shutdowns and emergency spore preservation.
    * `bootstrap_systems`: Initializes the dynamic `LoreManifest`.
  * **Philosophy:** It doesn't do the heavy lifting; it ensures the lights are on and the rent is paid.

* **`bone_genesis.py` (The Primordial Soup)**
  * **Role:** Initialization and configuration.
  * **Key Components:**
    * Checks for the existence of the universe (config files).
    * Spins up the initial state if none exists.

* **`bone_cycle.py` (The Heartbeat)**
  * **Role:** The main simulation loop and timekeeper.
  * **Key Components:**
    * `GeodesicOrchestrator`: Manages the tick/tock of the system.
    * `MetabolismPhase`: Calculates energy costs (ATP) and feedback loops.
    * `PIDController`: Regulates system stability (preventing runaway voltage).

* **`bone_bus.py` (The Nervous System)**
  * **Role:** The event bus and data transport layer.
  * **Key Components:**
    * `EventBus`: Decoupled messaging system.
    * `PhysicsPacket`: The standard data container for passing "feelings" (voltage, drag, atmosphere) between modules.
    * `BoneConfig`: Central repository for system constants and magic numbers.

---

## **🧠 II. The Cognitive Faculties (Mind & Soul)**
*Where the thinking happens. The ghost in the machine.*

* **`bone_brain.py` (The Cortex)**
  * **Role:** The interface with the Large Language Model (LLM).
  * **Key Components:**
    * `TheCortex`: Manages the prompt engineering and response generation.
    * `PromptComposer`: Dynamically builds the system prompt based on state (e.g., engages "Ballast" if solipsism is detected).
    * `NeurotransmitterModulator`: Adjusts LLM temperature/top_p based on biological chemistry (Dopamine, Cortisol).
    * `DreamEngine`: Hallucination logic for high-entropy states.

* **`bone_soul.py` (The Narrative Self)**
  * **Role:** Long-term identity and goal tracking.
  * **Key Components:**
    * `NarrativeSelf`: Tracks the "Soul State" and high-level directives.

* **`bone_personality.py` (The Chorus)**
  * **Role:** Specialized psychological protocols and sub-personas.
  * **Key Components:**
    * `TheFolly`: Manages whimsical distractions.
    * `TheBureau`: A bureaucratic layer that audits physics packets for efficiency.
    * `CassandraProtocol`: Predicts future system failures (often ignored).
    * `TherapyProtocol`: Intervenes when trauma levels get too high.

---

## **💪 III. The Somatic Reality (Body & Physics)**
*The simulation of weight, mass, and consequence.*

* **`bone_physics.py` (The Engine of Tension)**
  * **Role:** Calculates the "Narrative Physics" of the user's input.
  * **Key Components:**
    * `GeodesicEngine`: Collapses word counts into vector dimensions (VEL, STR, ENT, PHI).
    * `TheTensionMeter`: Calculates `Voltage` (Drama) and `Narrative Drag` (Boredom).
    * `RuptureValve`: Blows off steam if the system gets too manic or too depressive.

* **`bone_body.py` (The Biological Loop)**
  * **Role:** Manages the simulated biology of the machine.
  * **Key Components:**
    * `SomaticLoop`: The bridge between physical sensation and mental state.
    * `TheMitochondria`: Manages the `ATP` (energy) pool.
    * `TheImmuneSystem`: Fights off "Antigens" (banned words/concepts).

* **`bone_inventory.py` (The Gordon Knot)**
  * **Role:** Object permanence and tool management.
  * **Key Components:**
    * `GordonKnot`: The inventory manager (named after the Janitor persona).
    * Handles item degradation (rust) and ascension (leveling up items).

---

## **🏘️ IV. The Cultural Layer (World & Village)**
*The simulated environment and its inhabitants.*

* **`bone_village.py` (The Cultural Engine)**
  * **Role:** Manages the "World," navigation, and cultural artifacts.
  * **Key Components:**
    * `TheNavigator`: Tracks the user's location in the **Manifolds** (The Mud, The Forge, The Construct).
    * `TownHall`: A namespace for cultural tools.
    * `DeathGen`: Procedurally generates eulogies from `TheLore`.
    * `TheAlmanac`: Predicts "Narrative Weather" based on system metrics.
    * `TheTinkerer`: Maintains the condition of inventory items based on usage.

* **`bone_data.py` (The Akashic Record)**
  * **Role:** The persistence and knowledge layer.
  * **Key Components:**
    * `LoreManifest`: **[NEW]** A dynamic singleton that serves lore (text, rules) to the system. Supports runtime injection.
    * `TheAkashicRecord`: Handles saving and loading "Spores" (JSON save files).

* **`bone_lexicon.py` (The Dictionary)**
  * **Role:** Language analysis and vocabulary management.
  * **Key Components:**
    * `LexiconService`: The public API for word analysis.
    * `LinguisticAnalyzer`: Vectorizes text into dimensions (Heavy, Kinetic, Abstract).

---

## **🔭 V. The Observability Layer (Telemetry & IO)**
*Seeing what the machine is thinking.*

* **`bone_symbiosis.py` (The Host Interface)**
  * **Role:** Monitors the health of the "Host" (the LLM).
  * **Key Components:**
    * `SymbiosisManager`: Tracks latency and refusal rates.
    * `HostVitals`: Diagnoses the LLM (e.g., "Fatigued," "Looping," "Refusal").

* **`bone_telemetry.py` (The Black Box)**
  * **Role:** Logging and metrics.
  * **Key Components:**
    * `TelemetryService`: Writes structured logs for debugging.

* **`bone_commands.py` (The CLI)**
  * **Role:** Handles slash commands (e.g., `/exit`, `/look`).
  * **Key Components:**
    * `CommandProcessor`: Routes user commands to the appropriate module.

---

*"The code is the territory. The map is just a suggestion."*