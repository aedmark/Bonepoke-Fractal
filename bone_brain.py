# bone_brain.py
# "The brain is a machine for jumping to conclusions." - S. Pinker

import re, time, json, urllib.request, urllib.error, random
from typing import Dict, Any, List, Optional, Tuple
from collections import deque
from dataclasses import dataclass
from bone_data import LENSES, DREAMS
from bone_bus import Prisma, BoneConfig, EventBus
from bone_village import TownHall
from bone_symbiosis import SymbiosisManager

try:
    from bone_lexicon import TheLexicon
except ImportError:
    TheLexicon = None
    print(f"{Prisma.YEL}[WARNING]: TheLexicon missing. Spotlight will be dim.{Prisma.RST}")
try:
    from bone_translation import RosettaStone
except ImportError:
    RosettaStone = None
    print(f"{Prisma.YEL}[WARNING]: RosettaStone missing. Reverting to Pidgin Protocol.{Prisma.RST}")
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
try:
    from bone_telemetry import TelemetryService
except ImportError:
    TelemetryService = None
    print("Telemetry module not found. Flying blind.")

@dataclass
class ChemicalState:
    """Represents the neuro-chemical balance of the mind."""
    dopamine: float = 0.0
    cortisol: float = 0.0
    adrenaline: float = 0.0
    serotonin: float = 0.0

    def decay(self, rate: float = 0.2):
        """Applies a half-life to the chemicals."""
        self.dopamine = max(0.0, self.dopamine * (1.0 - rate))
        self.cortisol = max(0.0, self.cortisol * (1.0 - rate))
        self.adrenaline = max(0.0, self.adrenaline * (1.0 - rate))
        self.serotonin = max(0.0, self.serotonin * (1.0 - rate))

    def mix(self, new_state: Dict[str, float], weight: float = 0.5):
        """Blends new influx with existing state (Meadows: Stocks & Flows)."""
        self.dopamine = (self.dopamine * (1.0 - weight)) + (new_state.get("DOP", 0.0) * weight)
        self.cortisol = (self.cortisol * (1.0 - weight)) + (new_state.get("COR", 0.0) * weight)
        self.adrenaline = (self.adrenaline * (1.0 - weight)) + (new_state.get("ADR", 0.0) * weight)
        self.serotonin = (self.serotonin * (1.0 - weight)) + (new_state.get("SER", 0.0) * weight)

class NarrativeSpotlight:
    """
    Retrieves relevant memories based on the current 'Geodesic Vector'.
    Pinker Lens: Associative memory, not just keyword search.
    """
    def __init__(self):
        self.DIMENSION_MAP = {
            "STR": {"heavy", "constructive", "base"},
            "VEL": {"kinetic", "explosive", "mot"},
            "ENT": {"antigen", "toxin", "broken", "void"},
            "PHI": {"thermal", "photo", "explosive"},
            "PSI": {"abstract", "sacred", "void", "idea"},
            "BET": {"suburban", "solvents", "play"}
        }

    def illuminate(self, graph: Dict, vector: Dict[str, float], limit: int = 5) -> List[str]:
        if not graph or not vector:
            return []

        active_dims = {k: v for k, v in vector.items() if v > 0.3}
        if not active_dims:
            candidates = list(graph.keys())
            if not candidates: return []
            return [f"Drifting thought: '{w}'" for w in random.sample(candidates, min(len(candidates), 3))]

        scored_memories = []
        for node, data in graph.items():
            resonance_score = 0.0

            if TheLexicon:
                node_cats = TheLexicon.get_categories_for_word(node)
                for dim, val in active_dims.items():
                    target_flavors = self.DIMENSION_MAP.get(dim, set())
                    if node_cats & target_flavors:
                        resonance_score += (val * 1.5)

            mass = sum(data.get("edges", {}).values())
            resonance_score += (mass * 0.1)

            if resonance_score > 0.5:
                scored_memories.append((resonance_score, node, data))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        top_n = scored_memories[:limit]

        results = []
        for score, name, data in top_n:
            connections = list(data.get("edges", {}).keys())
            conn_str = f" -> [{', '.join(connections[:2])}]" if connections else ""
            results.append(f"Resonant Engram: '{name.upper()}'{conn_str}")

        return results

class NeurotransmitterModulator:
    """
    Manages the translation of 'Biology' (Chemicals) into 'Cognition' (LLM Params).
    Now with MEMORY to prevent jittery personality shifts.
    """
    def __init__(self):
        self.current_chem = ChemicalState()

    def modulate(self, incoming_chem: Dict[str, float], base_voltage: float) -> Dict[str, Any]:
        self.current_chem.mix(incoming_chem, weight=0.6)

        params = {
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": getattr(BoneConfig, "MAX_OUTPUT_TOKENS", 2048)
        }

        if self.current_chem.cortisol > 0.3:
            params["temperature"] -= (self.current_chem.cortisol * 0.4)
            params["top_p"] -= (self.current_chem.cortisol * 0.3)
            params["frequency_penalty"] += 0.2

        if self.current_chem.dopamine > 0.3:
            params["temperature"] += (self.current_chem.dopamine * 0.4)
            params["presence_penalty"] += (self.current_chem.dopamine * 0.4)

        if self.current_chem.adrenaline > 0.3:
            base_tokens = 150
            params["max_tokens"] = int(base_tokens + (300 * (1.0 - self.current_chem.adrenaline)))
            params["frequency_penalty"] += (self.current_chem.adrenaline * 0.6)

        if self.current_chem.serotonin > 0.5:
            diff = 0.7 - params["temperature"]
            params["temperature"] += (diff * self.current_chem.serotonin * 0.5)

        if base_voltage > 15.0:
            params["temperature"] += 0.25
        elif base_voltage < 5.0:
            params["temperature"] -= 0.15

        params["temperature"] = max(0.1, min(1.6, params["temperature"]))
        params["top_p"] = max(0.1, min(1.0, params["top_p"]))
        params["max_tokens"] = max(50, params["max_tokens"])

        return params

class LLMInterface:
    """
    The Hardware Interface.
    Fuller Lens: Robust, handles errors, logs to bus (if available).
    """
    def __init__(self, events_ref: Optional[EventBus] = None, provider: str = None, base_url: str = None, api_key: str = None, model: str = None):
        self.events = events_ref
        self.provider = (provider or BoneConfig.PROVIDER).lower()
        self.api_key = api_key or BoneConfig.API_KEY
        self.model = model or BoneConfig.MODEL
        self.base_url = base_url or self._get_default_url(self.provider)

    def _get_default_url(self, provider):
        defaults = {
            "ollama": "http://127.0.0.1:11434/v1/chat/completions",
            "openai": "https://api.openai.com/v1/chat/completions",
            "lm_studio": "http://127.0.0.1:1234/v1/chat/completions",
            "localai": "http://127.0.0.1:8080/v1/chat/completions"
        }
        return defaults.get(provider, "https://api.openai.com/v1/chat/completions")

    def _log(self, message: str, level: str = "SYS"):
        """Safe logging wrapper that handles missing EventBus."""
        if self.events:
            self.events.log(message, level)
        else:
            # Fallback for Genesis/Test mode
            print(f"[{level}] {message}")

    def generate(self, prompt: str, params: Dict[str, Any]) -> str:
        if self.provider == "mock":
            return self.mock_generation(prompt)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        payload.update(params) # Inject temp, top_p, etc.

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.base_url, data=data, headers=headers)

            with urllib.request.urlopen(req, timeout=30.0) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode("utf-8"))
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if content: return content
                raise Exception(f"HTTP {response.status}")

        except Exception as e:
            self._log(f"CORTEX UPLINK FAILED: {e}", "ERR")
            # Fallback to local Ollama if primary fails
            if OLLAMA_AVAILABLE and self.provider != "ollama":
                self._log("Attempting Local Fallback (Ollama)...", "SYS")
                return self._local_fallback(prompt, params)

            return self.mock_generation(prompt)

    def _local_fallback(self, prompt: str, params: Dict) -> str:
        try:
            response = ollama.chat(
                model=getattr(BoneConfig, "OLLAMA_MODEL_ID", "llama3"),
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': params.get('temperature', 0.7)}
            )
            return response['message']['content']
        except Exception as e:
            self._log(f"FALLBACK FAILED: {e}", "CRIT")
            return self.mock_generation(prompt)

    def mock_generation(self, prompt: str) -> str:
        """Schur Lens: When the brain breaks, make it poetic."""
        phrases = [
            "The wire hums, but carries no voice.",
            "Static fills the geodesic dome. The system is dreaming.",
            "The neural lattice is calcified. Try again.",
            "A gust of wind blows through the server room."
        ]
        return f"[{random.choice(phrases)}]"

class PromptComposer:
    """
    Constructs the System Prompt using Geodesic Layering.
    Now responsive to Symbiosis Modifiers (Meadows Lens).
    """
    def _sanitize(self, text: str) -> str:
        safe = text.replace('"""', "'''").replace('```', "'''")
        return re.sub(r"(?i)^SYSTEM:", "User-System:", safe, flags=re.MULTILINE)

    def compose(self, state: Dict[str, Any], user_query: str, ballast: bool = False, modifiers: Dict[str, bool] = None) -> str:
        if modifiers is None:
            modifiers = {
                "include_somatic": True, "include_inventory": True,
                "include_memories": True, "simplify_instruction": False,
                "inject_chaos": False
            }

        mind = state.get("mind", {})
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        profile = state.get("user_profile", {})

        role = mind.get("role", "The Observer")
        lens = mind.get("lens", "NARRATOR")
        sys_inst = state.get("system_instruction", "")

        if modifiers["simplify_instruction"]:
            sys_inst = "Keep responses short. Focus on the immediate physical sensation."

        identity_block = (
            f"### SYSTEM IDENTITY\n"
            f"You are {lens} ({role}).\n"
            f"{sys_inst}\n"
        )

        somatic_block = ""
        if modifiers["include_somatic"]:
            somatic_txt = ""
            if RosettaStone:
                sem_state = RosettaStone.translate(phys, bio)
                somatic_txt = RosettaStone.render_system_prompt_addition(sem_state)

            moods = []
            chem = bio.get("chem", {})
            if chem.get("ADR", 0) > 0.6: moods.append("HIGH ALERT (Adrenaline)")
            if chem.get("COR", 0) > 0.6: moods.append("DEFENSIVE (Cortisol)")
            if chem.get("DOP", 0) > 0.6: moods.append("SEEKING (Dopamine)")

            somatic_block = (
                f"### BIOLOGICAL STATE\n"
                f"Mood: {', '.join(moods) if moods else 'Homeostasis'}\n"
                f"{somatic_txt}\n"
            )

        context_block = ""
        parts = []

        if modifiers["include_inventory"]:
            inventory = state.get("inventory", [])
            inv_str = ", ".join(inventory) if inventory else "Empty"
            parts.append(f"Inventory: {inv_str}")

        parts.append(f"Location: {state.get('world', {}).get('orbit', ['Void'])[0]}")

        if modifiers["include_memories"]:
            spotlight = state.get("spotlight", [])
            mem_str = "\n".join([f"- {m}" for m in spotlight]) if spotlight else "(None)"
            parts.append(f"Active Memories:\n{mem_str}")

        if parts:
            context_block = "### WORLD CONTEXT\n" + "\n".join(parts) + "\n"

        user_name = profile.get("name", "Traveler")
        confidence = profile.get("confidence", 0)
        social_block = (
            f"### SOCIAL CONTEXT\n"
            f"Interlocutor: {user_name} (Confidence: {confidence}%)\n"
        )
        if confidence > 20:
            social_block += f"Use their name naturally. You know them.\n"

        ballast_txt = ""
        if ballast:
            ballast_txt = "\n[WARNING: SOLIPSISM DETECTED. STOP ABSTRACTING. BE CONCRETE.]\n"

        chaos_txt = ""
        if modifiers["inject_chaos"]:
            chaos_txt = "\n[SYSTEM INJECTION]: The narrative is stuck. Introduce a sudden, random event or glitch.\n"

        clean_q = self._sanitize(user_query)

        final_prompt = (
            f"{identity_block}\n"
            f"{somatic_block}\n"
            f"{context_block}\n"
            f"{social_block}\n"
            f"### NARRATIVE ARC\n"
            f"{state.get('soul_state', '')}\n\n"
            f"{ballast_txt}"
            f"{chaos_txt}"
            f"### INPUT TRANSMISSION\n"
            f"{user_name}: {clean_q}\n\n"
            f"### DIRECTIVE\n"
            f"Respond as {lens}. Reflect the biological state in your tone. "
            f"Do not break character. Do not explain the simulation."
        )
        return final_prompt

class ResponseValidator:
    """
    The Immune System for the Mind.
    Filters out 'Silicon Ash' (LLM refusals, repetition, breaking character).
    """
    def __init__(self):
        self.banned_phrases = [
            "large language model", "AI assistant", "cannot feel", "as an AI",
            "against my programming", "cannot comply", "language model"
        ]

    def validate(self, response: str, state: Dict) -> Dict:
        for phrase in self.banned_phrases:
            if phrase in response:
                return {
                    "valid": False,
                    "reason": "IMMERSION_BREAK",
                    "replacement": f"{Prisma.GRY}[The system mumbles about its source code, but you tap the glass to silence it.]{Prisma.RST}"
                }
        if len(response) < 2:
            return {"valid": False, "reason": "TOO_SHORT", "replacement": "..."}
        return {"valid": True, "content": response}

class TheCortex:
    """
    The Orchestrator of Cognition.
    Connects the Body (Cycle) to the Mind (LLM).
    """
    def __init__(self, engine_ref, llm_client=None):
        self.sub = engine_ref
        self.events = engine_ref.events

        self.llm = llm_client if llm_client else LLMInterface(self.events, provider="mock")
        self.composer = PromptComposer()
        self.modulator = NeurotransmitterModulator()
        self.spotlight = NarrativeSpotlight()
        self.symbiosis = SymbiosisManager(self.events)

        self.ballast_active = False
        self.ballast_counter = 0

    def process(self, user_input: str) -> Dict[str, Any]:
        sim_result = self.sub.cycle_controller.run_turn(user_input)

        if sim_result.get("type") not in ["SNAPSHOT", None]:
            if sim_result.get("ui") and not sim_result.get("logs"):
                return sim_result

        full_state = self._gather_state(sim_result)

        voltage = full_state["physics"].get("voltage", 5.0)
        chem = full_state["bio"].get("chem", {})
        llm_params = self.modulator.modulate(chem, voltage)

        modifiers = self.symbiosis.get_prompt_modifiers()

        if self.ballast_active:
            self.ballast_counter -= 1
            if self.ballast_counter <= 0: self.ballast_active = False

        final_prompt = self.composer.compose(
            full_state,
            user_input,
            ballast=self.ballast_active,
            modifiers=modifiers
        )

        start_time = time.time()
        response_text = self.llm.generate(final_prompt, llm_params)
        latency = time.time() - start_time

        self.symbiosis.monitor_host(latency, response_text)
        self._audit_solipsism(response_text)

        sim_result["ui"] = f"{sim_result.get('ui', '')}\n\n{Prisma.WHT}{response_text}{Prisma.RST}"
        return sim_result

    def _gather_state(self, sim_result):
        return {
            "bio": {
                "chem": self.sub.bio.endo.get_state(),
                "atp": self.sub.bio.mito.state.atp_pool
            },
            "physics": self.sub.phys.tension.last_physics_packet,
            "mind": {
                "role": LENSES.get(self.sub.noetic.arbiter.current_focus, {}).get("role", "Observer"),
                "lens": self.sub.noetic.arbiter.current_focus
            },
            "user_profile": self.sub.mind.mirror.profile.__dict__,
            "world": {"orbit": sim_result.get("world_state", {}).get("orbit", ["Void"])},
            "inventory": self.sub.gordon.inventory,
            "soul_state": self.sub.soul.get_soul_state(),
            "spotlight": self.spotlight.illuminate(
                self.sub.mind.mem.graph,
                self.sub.phys.tension.last_physics_packet.get("vector", {})
            )
        }

    def _audit_solipsism(self, text: str):
        """Checks if the LLM is talking to itself too much."""
        words = text.lower().split()
        if not words: return
        self_refs = words.count("i") + words.count("me") + words.count("my")
        density = self_refs / len(words)

        if density > 0.15:
            if not self.ballast_active:
                self.events.log("SOLIPSISM WARNING: Ballast Engaged.", "SYS")
                self.ballast_active = True
                self.ballast_counter = 3

class NeuroPlasticity:
    """
    Manages Hebbian Learning: "Neurons that fire together, wire together."
    Called by bone_body.py during high-voltage events.
    """
    def __init__(self):
        self.plasticity_mod = 1.0

    def force_hebbian_link(self, graph, word_a, word_b):
        """
        Creates a strong edge between two concepts in the graph.
        """
        if word_a == word_b: return None

        if word_a not in graph:
            graph[word_a] = {"edges": {}, "last_tick": 0}
        if word_b not in graph:
            graph[word_b] = {"edges": {}, "last_tick": 0}

        current_weight = graph[word_a]["edges"].get(word_b, 0.0)
        new_weight = min(10.0, current_weight + 2.5)
        graph[word_a]["edges"][word_b] = new_weight

        back_weight = graph[word_b]["edges"].get(word_a, 0.0)
        graph[word_b]["edges"][word_a] = min(10.0, back_weight + 1.0)

        return f"{Prisma.MAG}⚡ HEBBIAN GRAFT: Wired '{word_a}' <-> '{word_b}'.{Prisma.RST}"

class ShimmerState:
    """
    The Fuel Tank for Navigation.
    'Shimmer' is the resource consumed to move between Manifolds (e.g., Courtyard -> Aerie).
    """
    def __init__(self, max_val=50.0):
        self.current = max_val
        self.max_val = max_val

    def recharge(self, amount):
        self.current = min(self.max_val, self.current + amount)

    def spend(self, amount):
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def get_bias(self):
        return None

class DreamEngine:
    """
    Generates 'hallucinations' when the system is asleep or in high-entropy states.
    """
    def __init__(self, events):
        self.events = events
        self.PROMPTS = DREAMS.get("PROMPTS", ["{A} -> {B}?"]) if 'DREAMS' in globals() else []

    def hallucinate(self, vector: Dict[str, float]) -> str:
        dims = [k for k, v in vector.items() if v > 0.5]
        dim_str = ", ".join(dims) if dims else "VOID"
        return f"Dreaming of {dim_str}..."