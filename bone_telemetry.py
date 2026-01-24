""" bone_telemetry.py """

import json
import time
import os
import glob
import uuid
from typing import Any, Dict
from dataclasses import dataclass, asdict
from bone_bus import Prisma

@dataclass
class DecisionTrace:
    trace_id: str
    timestamp: float
    component: str
    decision_type: str
    inputs: Dict[str, Any]
    reasoning: str
    outcome: str

    def to_json(self):
        return json.dumps(asdict(self))

class LogManager:
    MAX_BYTES = 5 * 1024 * 1024
    BACKUP_COUNT = 5

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._file = None
        self._open_file()

    def _open_file(self):
        self._ensure_dir()
        self._file = open(self.filepath, "a", encoding="utf-8")

    def _ensure_dir(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, data: str):
        if self._file is None:
            self._open_file()

        try:
            self._file.write(data + "\n")
            self._file.flush()
            if self._file.tell() >= self.MAX_BYTES:
                self._rotate()
        except Exception as e:
            print(f"{Prisma.RED}[LOG MANAGER FAIL]: {e}{Prisma.RST}")

    def _rotate(self):
        print(f"{Prisma.YEL}[LOG MANAGER]: Rotating logs. Flushing the bathtub.{Prisma.RST}")
        self._close()
        for i in range(self.BACKUP_COUNT - 1, 0, -1):
            src = f"{self.filepath}.{i}"
            dst = f"{self.filepath}.{i+1}"
            if os.path.exists(src):
                os.rename(src, dst)
        if os.path.exists(self.filepath):
            os.rename(self.filepath, f"{self.filepath}.1")
        self._open_file()

    def _close(self):
        if self._file:
            self._file.close()
            self._file = None

    def __del__(self):
        self._close()


class StructuredLogger:
    def __init__(self, session_id: str, log_dir: str = "telemetry"):
        self.session_id = session_id
        filepath = os.path.join(log_dir, f"trace_{session_id}.jsonl")
        self.manager = LogManager(filepath)
        print(f"{Prisma.CYN}[TELEMETRY]: Observability Layer Active.{Prisma.RST}")
        print(f"{Prisma.GRY}   > Managed by LogManager at: {filepath}{Prisma.RST}")

    def capture_decision(self, component: str, decision_type: str,
                         inputs: Dict, reasoning: str, outcome: str):
        trace = DecisionTrace(
            trace_id=str(uuid.uuid4())[:8],
            timestamp=time.time(),
            component=component,
            decision_type=decision_type,
            inputs=self._sanitize(inputs),
            reasoning=reasoning,
            outcome=outcome
        )
        self.manager.write(trace.to_json())

    def _sanitize(self, data: Any, depth: int = 0, max_depth: int = 3) -> Any:
        if depth > max_depth:
            return "<Max Depth Exceeded>"

        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        if isinstance(data, dict):
            return {k: self._sanitize(v, depth + 1, max_depth)
                    for k, v in data.items() if k != "graph"}
        if isinstance(data, list):
            return [self._sanitize(i, depth + 1, max_depth) for i in data]
        if hasattr(data, '__dict__'):
            return self._sanitize(vars(data), depth + 1, max_depth)
        return str(data)

class TelemetryService:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls.initialize("boot_sequence")
        return cls._INSTANCE

    @classmethod
    def initialize(cls, session_id):
        cls._INSTANCE = StructuredLogger(session_id)
        return cls._INSTANCE