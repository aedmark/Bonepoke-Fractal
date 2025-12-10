### **Changelog: BoneAmanita v0.1.2**

**Date:** December 9, 2025 **Codename:** "The Temporal Metabolism"

#### **1. Codebase Updates (`BoneAmanita012.py`)**

- **New Class: `ChronosAnchor`**
    - **Function:** Enforces **Temporal Integrity** by detecting unintentional drifts between Past and Present tense.
    - **Logic:** Uses heuristic maps (`past_map`, `present_map`) and a `slippage_threshold` (0.20) to distinguish between sloppy writing and intentional "Hybrid State" flashbacks.
    - **Integration:** Added to `BonepokeCore` to automatically flag "Drift" errors in the feedback loop.
        
- **New Class: `MetabolicReserve`**
    - **Function:** Introduces a "Creative ATP" economy. Writers must "earn" the right to use abstractions by first using concrete universals.
    - **The Economy:** Concrete/Kinetic words generate energy; Abstract concepts cost energy.
    - **States:** Defined **STARVING** (Strict Mode) and **GLUTTON** (Creative Mode) based on current ATP levels.
        
- **New Class: `MycelialNetwork`**
    - **Function:** Implements **Genetic History** tracking.
    - **Logic:** Treats every text output not as an isolated event but as a descendant of a parent draft, tracking "Genetic Drift" in Drag and Style over generations.
        
- **Updated Class: `MycelialDashboard`**
    - **Visual Update:** Added a new **CREATIVE ATP** bar to the EKG.
    - **Lineage Rendering:** Now displays the **GENETIC HISTORY** tree at the bottom of the dashboard.
        

#### **2. Driver/Prompt Updates (`Roberta` & `Eloise/Clarence`)**

- **Updated Persona: Clarence**
    - **Nxw Role:** Now explicitly identified as a **"Tax Collector"**.
    - **Directive:** Monitors **Metabolic Reserve**. If the user is "STARVING," Clarence enters "Strict Mode" and forbids the use of words like "framework" until the debt is paid in "mud".
    - **New Protocol:** Enforces the **Chronos Protocol** to punish "Tense Drift".
        
- **New Behavior: State Inheritance (The Loop)**
    - **Logic:** The system now scans the input for previous "MYCELIAL EKG" data.
    - **Continuity:** It inherits the previous **ATP Status** (forcing debt repayment across turns) and appends the new text to the existing **Genetic History** tree rather than restarting it.
        
- **Updated Output Protocol**
    - **Structure:** The "System Shimmer" block now includes the updated EKG with ATP bars and Ancestry logs.
    - **Navigation:** Added explicit instructions for the agents to "Commission a specific nutrient" in the next step, rather than asking generic questions.
    
---

### **Changelog: BoneAmanita v0.1.1**
**Date:** December 9, 2025
**Codename:** "The Reality Anchor"

#### **1. Codebase Updates (`BoneAmanita01.py`)**

* **Class Modified: `FactStipe`**
    * **Expanded `conflict_map`:** Added new mutually exclusive sets to track sensory contradictions (e.g., `silence` vs. `whisper`, `indoors` vs. `rain`).
    * **New Logic:** Implemented a "Strict Logic" check in `check_consistency`. It now scans for specific keyword collisions (e.g., "sun" appearing in a "night" context).
    * **New Output:** The function now returns a forceful `intervention` string (e.g., *"STOP. Logic Error."*) rather than just a boolean flag.

* **Class Modified: `BonepokeCore`**
    * **Workflow Update:** Modified the `process()` loop. It now halts the "editorial" phase if a Stipe error is detected.
    * **Penalty Mechanism:** Added a direct penalty to the `MetabolicReserve`. A logic error now deducts **10 ATP**, forcing the system into "Starving" mode (Strict Mode) immediately.
    * **Feedback Integration:** Critical logic errors are now injected directly into the `editorial['feedback']` dictionary under the key `CRITICAL_LOGIC`.

#### **2. Driver/Prompt Updates (`Roberta` & `Eloise`)**

* **Hex-Brain Schematic Updated:**
    * **New Component:** Inserted **Step 2.5: THE STIPE (Reality Anchor)** into the processing order.
    * [cite_start]**Location:** Placed between *The Lattice* (Physics) [cite: 10] [cite_start]and *The Shimmer* (Editorial)[cite: 18].
* **New Directives:**
    * Explicitly commanded the persona to "Scan the `conflict_map`" before finalizing text.
    * Added a strict rule: "If a conflict is found, DELETE the hallucination."

#### **3. Narrative Impact**

* **Reduced Surrealism:** The system will now "catch" itself if it tries to describe sunlight during a midnight scene.
* [cite_start]**Harder Difficulty:** Because logic errors now cost ATP (Energy), the system is more likely to trigger **Clarence's Strict Mode**[cite: 29], forcing simpler, grounded language until the logic is corrected.
