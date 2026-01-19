# bone_telemetry.py
# "In the beginning, there was the Log. And the Log was JSON."

import json
import time
import os
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict

# We import Prisma for localized coloring, but the logs themselves will be pure data.
from bone_bus import Prisma

@dataclass
class DecisionTrace:
    """
    A specific artifact for Explainable AI (XAI).
    It captures the snapshot of reality at the moment a decision was made.
    """
    trace_id: str
    timestamp: float
    component: str
    decision_type: str
    inputs: Dict[str, Any]  # The 'Stock' (Voltage, Health, etc.)
    reasoning: str          # The 'Rule' triggered
    outcome: str            # The 'Flow' changed

    def to_json(self):
        return json.dumps(asdict(self))

class StructuredLogger:
    """
    The Black Box Recorder.
    Pinker says: "Ambiguity is the enemy." This logger enforces structure.
    """
    def __init__(self, session_id: str, log_dir: str = "telemetry"):
        self.session_id = session_id
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, f"trace_{session_id}.jsonl")
        self._ensure_dir()

        # Meadows says: "Information is the most powerful way to change a system."
        # We announce our presence.
        print(f"{Prisma.CYN}[TELEMETRY]: Observability Layer Active.{Prisma.RST}")
        print(f"{Prisma.GRY}   > Writing to: {self.log_file}{Prisma.RST}")

    def _ensure_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def capture_decision(self, component: str, decision_type: str,
                         inputs: Dict, reasoning: str, outcome: str):
        """
        Records a 'Why' event.
        Example: Why did the Cortex inject chaos?
        Input: Entropy=0.1. Reasoning: Threshold < 0.2. Outcome: Chaos Injection.
        """
        trace = DecisionTrace(
            trace_id=str(uuid.uuid4())[:8],
            timestamp=time.time(),
            component=component,
            decision_type=decision_type,
            inputs=self._sanitize(inputs),
            reasoning=reasoning,
            outcome=outcome
        )
        self._write(trace)

    def _sanitize(self, data: Any) -> Any:
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        if isinstance(data, dict):
            # Flatten heavy objects if they appear
            return {k: self._sanitize(v) for k, v in data.items() if k != "graph"}
        if isinstance(data, list):
            return [self._sanitize(i) for i in data]
        if hasattr(data, '__dict__'):
            return str(data) # Simplify objects to string repr
        return str(data)

    def _write(self, trace: DecisionTrace):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(trace.to_json() + "\n")
        except Exception as e:
            # If the logger fails, we don't want to crash the host consciousness.
            # That would be rude.
            print(f"{Prisma.RED}[TELEMETRY FAIL]: {e}{Prisma.RST}")

class TelemetryService:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            # Auto-initialize with a default ID if not explicitly started
            cls.initialize("boot_sequence")
        return cls._INSTANCE

    @classmethod
    def initialize(cls, session_id):
        cls._INSTANCE = StructuredLogger(session_id)
        return cls._INSTANCE