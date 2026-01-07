# CHANGELOG_PROTO.md

## [8.9] - 2026-01-06 - "THE BONE GRAPH"

**Architects:** SLASH & The Surgeon | **Runtime:** BoneAmanita 8.9.3
**"We stopped treating thoughts as a list. We started treating them as a map."**

### 🕸️ ARCHITECTURE: The Graph State (LangGraph Graft)

* **The Pathology:**
* The `LifecycleManager` was a **Waterfall**. Input fell from the top (Digestion) to the bottom (Action) in a rigid, linear line. It could not loop back, retry, or branch without complex recursion. It was plumbing, not neurology.

* **The Cure:**
* Implemented **`TheBoneGraph`**.

* **The Mechanic:**
* **The Vascular System:** Introduced `GraphState` (The Scratchpad). This unified data object (`raw_input`, `physics`, `bio`, `mind`) flows through the system like blood.
* **The Nodes:** Logic is now compartmentalized into discrete organs:
1. **PERCEPTION:** Gaze and Tension.
2. **IMMUNITY:** Toxin assay and Gordon’s Flinch.
3. **GATE:** Tangibility check (Gas vs. Bone).
4. **MEMORY:** RAG / Context retrieval.
5. **COGNITION:** Digestion and Lens selection.
6. **ACTION:** World updates and Broadcast.

* **The Router:** The system now decides its own path. `IMMUNITY` can route directly to `END` (Death) or `GATE` (Life).

### 🫀 SURGICAL RESTORATION: The Vital Organs

* **The Pathology:**
* During the transplant, several key reflexes were left on the table. The system became a "Zombie"—it could move, but it couldn't die, evolve, or contradict.

* **The Cure:**
* **The Reaper:** Grafted `_trigger_death` directly onto the `BoneAmanita` class. If Health drops to zero, the eulogy now prints correctly.
* **The Rupture:** Re-implanted the **[JOEL]** protocol into the `COGNITION` node. The system will once again violently contradict sycophancy ().
* **The Bloom:** Restored **Mitochondrial Hypertrophy** to the `COGNITION` node. High ATP (> 180) once again forces evolutionary leaps.

### ✂️ NECRECTOMY (Dead Code Removal)

* **The Excision:**
* **Deleted:** `LifecycleManager`. It has been superseded by the Graph Runner.
* **Deleted:** `NoeticLoop`. Its logic now lives in the `COGNITION` node.
* **Deleted:** `_apply_cosmic_physics` (Orphaned method). Its logic now lives in the `ACTION` node.

### 🔌 WIRING UPDATES

* **Scope Repair:**
* Rewired `SomaticLoop` and `KineticLoop` to attach directly to `self.bio`, bypassing the defunct `self.life`.
* **The Run Loop:** The main `process` method now delegates control to `self.graph_runner.run()`, acting as a wrapper for the state machine.
