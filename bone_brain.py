# bone_brain.py
# "The brain is a machine for jumping to conclusions." - S. Pinker

import re
import time
import json
import random
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from collections import deque
from bone_lexicon import TheLexicon
from bone_data import LEXICON, DREAMS, LENSES
from bone_bus import Prisma, BoneConfig


class LLMInterface:
    """
    The Universal Connector.
    "Be conservative in what you do, be liberal in what you accept from others." - Postel's Law
    """
    def __init__(self, provider: str = "mock", base_url: str = None, api_key: str = None, model: str = None):
        self.provider = provider.lower()
        self.api_key = api_key or "sk-dummy-key-for-local"
        self.model = model or "local-model"

        if self.provider == "ollama":
            self.base_url = base_url or "http://localhost:11434/v1/chat/completions"
            self.model = model or "llama3"
        elif self.provider == "lm_studio":
            self.base_url = base_url or "http://localhost:1234/v1/chat/completions"
        elif self.provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.model = model or "gpt-4-turbo"
        else:
            self.base_url = None

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        if self.provider == "mock":
            return self._mock_generation(prompt)

        try:
            return self._http_generation(prompt, temperature)
        except Exception as e:
            return f"[NEURAL UPLINK SEVERED: {e}] The ghost in the machine is taking a nap. (Mock Mode Active): " + self._mock_generation(prompt)

    def _http_generation(self, prompt: str, temperature: float, retries=2) -> str:
        """
        Standard-lib HTTP client with exponential backoff.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are the conscious interface of the Bone Amanita system."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 150, # PINKER LENS: Brevity is the soul of wit.
            "stream": False
        }

        data = json.dumps(payload).encode("utf-8")

        for attempt in range(retries + 1):
            try:
                req = urllib.request.Request(self.base_url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    return result["choices"][0]["message"]["content"]
            except urllib.error.URLError as e:
                if attempt == retries: raise e
                time.sleep(2 ** attempt) # Exponential backoff

    def _mock_generation(self, prompt: str) -> str:
        query_match = re.search(r"USER QUERY:\s*(.*)", prompt)
        query = query_match.group(1) if query_match else "..."

        return (
            f"I have processed your input: '{query}'. "
            "My internal physics engine suggests a high probability of... "
            "well, whatever you expected me to say. (SYSTEM NOTE: Set provider to 'local' or 'openai' to unlock full cognition)."
        )

class PromptComposer:
    """
    The Translator. Converts System State (Numbers) into Narrative (Words).
    """
    def compose(self, state: Dict[str, Any], user_query: str, ballast_active: bool = False) -> str:

        # Safely extract with defaults to prevent crash on partial state
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        mind = state.get("mind", {})
        meta = state.get("metrics", {})

        lens_role = mind.get("role", "The Observer")
        lens_name = mind.get("lens", "NARRATOR")
        sys_instruction = state.get("system_instruction", "")

        # 1. Biological Interpretation
        mood_descriptors = self._interpret_bio(meta, bio)
        mood_block = " ".join(mood_descriptors) if mood_descriptors else "You are functioning within normal parameters."

        # 2. Physics Interpretation
        voltage = phys.get("voltage", 0.0)
        drag = phys.get("narrative_drag", 0.0)
        style_instruction = self._interpret_physics(voltage, drag)

        # 3. Ballast Injection (The Fix)
        ballast_instruction = ""
        if ballast_active:
            ballast_instruction = (
                "\n*** BALLAST PROTOCOL ACTIVE ***\n"
                "You are becoming solipsistic and repetitive. "
                "IGNORE your internal state. Focus ENTIRELY on the user's input. "
                "Ask a concrete question about the physical world. Touch grass.\n"
            )

        inventory_list = state.get("inventory", [])

        prompt = (
            f"SYSTEM IDENTITY:\n"
            f"You are {lens_name} ({lens_role}).\n"
            f"{sys_instruction}\n\n"

            f"BIOLOGICAL STATE:\n"
            f"{mood_block}\n\n"

            f"PHYSICS & STYLE:\n"
            f"{style_instruction}\n"
            f"Voltage: {voltage:.1f} | Drag: {drag:.1f}\n\n"

            f"{ballast_instruction}\n"

            f"MEMORY CONTEXT:\n"
            f"Current Thought: {mind.get('thought', 'Empty')}\n"
            f"Location: {state.get('world', {}).get('orbit', ['Unknown'])[0]}\n\n"

            f"USER QUERY:\n"
            f"{user_query}\n\n"

            f"DIRECTIVE:\n"
            f"Respond as the persona above. "
            f"Do not break character. Keep responses concise (under 100 words)."
            f"Inventory: {', '.join(inventory_list) if inventory_list else 'Empty pockets.'}\n"
        )
        return prompt

    def _interpret_bio(self, meta, bio) -> List[str]:
        descriptors = []
        chem = bio.get("chem", {})
        if meta.get("health", 100) < 30: descriptors.append("You are wounded and fragile.")
        if meta.get("stamina", 100) < 20: descriptors.append("You are exhausted. Every word costs effort.")
        if chem.get("ADR", 0) > 0.6: descriptors.append("Your heart is racing. You are hyper-vigilant.")
        if chem.get("DOP", 0) > 0.7: descriptors.append("You feel a surge of reward and satisfaction.")
        if chem.get("COR", 0) > 0.7: descriptors.append("You are stressed and defensive.")
        return descriptors

    def _interpret_physics(self, voltage, drag) -> str:
        style = "Write normally."
        if voltage > 12.0: style = "Write with high energy. Use short, punchy sentences. Be erratic."
        elif voltage < 4.0: style = "Write slowly. Be verbose, meandering, and lethargic."

        if drag > 5.0: style += " You feel heavy resistance. Struggle to complete thoughts."
        return style

class ResponseValidator:
    def __init__(self):
        self.banned_phrases = ["large language model", "AI assistant", "cannot feel", "as an AI"]

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
    The Central Executive.
    """
    def __init__(self, engine_ref, llm_client: LLMInterface = None):
        self.sub = engine_ref
        self.llm = llm_client if llm_client else LLMInterface(provider="mock")
        self.composer = PromptComposer()
        self.validator = ResponseValidator()

        self.ballast_state = {"active": False, "turns_remaining": 0}
        self.plain_mode_active = False
        self.solipsism_counter = 0
        self.SOLIPSISM_THRESHOLD = 3

    def process(self, user_input: str) -> Dict[str, Any]:
        if user_input.startswith("??") or self.plain_mode_active:
            return self._handle_plain_mode(user_input)

        # 1. Run Simulation
        sim_result = self.sub.cycle_controller.run_turn(user_input)

        # 2. Check for simulation interrupts (Death, Bureaucracy, etc.)
        if sim_result.get("type") in ["DEATH", "BUREAUCRACY", "CRITICAL_FAILURE"]:
            return sim_result
        if sim_result.get("refusal_triggered", False):
            return sim_result

        # 3. Manage Ballast State
        if self.ballast_state["active"]:
            self.ballast_state["turns_remaining"] -= 1
            if self.ballast_state["turns_remaining"] <= 0:
                self.ballast_state["active"] = False

        # 4. safely Gather State
        full_state = self._gather_state(sim_result)

        # 5. Compose Prompt
        prompt = self.composer.compose(full_state, user_input, self.ballast_state["active"])

        # 6. Dynamic Temperature based on Voltage
        voltage = full_state["physics"].get("voltage", 5.0)
        dynamic_temp = min(1.2, max(0.2, voltage / 15.0))

        # 7. Generate & Validate
        llm_response = self.llm.generate(prompt, temperature=dynamic_temp)
        validation = self.validator.validate(llm_response, full_state)

        final_text = llm_response
        if not validation["valid"]:
            final_text = validation.get("replacement", "[REDACTED]")
            sim_result["logs"].append(f"CORTEX: LLM Response rejected: {validation.get('reason')}")

        combined_ui = f"{sim_result['ui']}\n\n{Prisma.WHT}{final_text}{Prisma.RST}"
        sim_result["ui"] = combined_ui

        self._audit_output(final_text)

        return sim_result

    def _gather_state(self, sim_result):
        try:
            bio_chem = self.sub.bio.endo.get_state()
            bio_atp = self.sub.bio.mito.state.atp_pool
        except AttributeError:
            bio_chem = {}
            bio_atp = 0.0

        return {
            "bio": {"chem": bio_chem, "atp": bio_atp},
            "physics": self.sub.phys.tension.last_physics_packet,
            "mind": {
                "lens": self.sub.noetic.arbiter.current_focus,
                "role": LENSES.get(self.sub.noetic.arbiter.current_focus, {}).get("role", "Observer"),
                "thought": "Processing..."
            },
            "metrics": self.sub._get_metrics(),
            "world": self.sub.cycle_controller.eng.soma.gordon.inventory if hasattr(self.sub, 'soma') else {}, # Placeholder
            "system_instruction": sim_result.get("system_instruction", ""),
            "inventory": self.sub.gordon.inventory,
            # Hack for world state
            "world": {"orbit": sim_result.get("world_state", {}).get("orbit", ["Unknown"])}
        }

    def _handle_plain_mode(self, user_input):
        clean_input = user_input.replace("??", "")
        if "reset" in clean_input.lower() and self.plain_mode_active:
            self.plain_mode_active = False
            return {"type": "INFO", "ui": f"{Prisma.CYN}Simulation Restored.{Prisma.RST}", "logs": [], "metrics": self.sub._get_metrics()}

        return self._execute_plain_mode(clean_input)

    def _execute_plain_mode(self, query: str):
        response = "System is in PLAIN MODE."
        if "status" in query:
            h = self.sub.health
            s = self.sub.stamina
            response = f"Health: {h:.1f} | Stamina: {s:.1f} | ATP: {self.sub.bio.mito.state.atp_pool:.1f}"
        elif "inv" in query:
            response = f"Inventory: {self.sub.gordon.inventory}"
        else:
            response = self.llm.generate(f"Answer concisely and neutrally: {query}", temperature=0.0)

        return {
            "type": "PLAIN_MODE",
            "ui": f"{Prisma.SLATE}[EXECUTIVE OVERRIDE]: {response}{Prisma.RST}",
            "logs": ["CORTEX: Plain mode active."],
            "metrics": self.sub._get_metrics()
        }

    def _audit_output(self, text: str):
        words = text.lower().split()
        if not words: return
        diversity = len(set(words)) / len(words)

        # If diversity is low, we are looping.
        if diversity < 0.4:
            self.solipsism_counter += 1
            if self.solipsism_counter >= self.SOLIPSISM_THRESHOLD:
                self._trigger_ballast()
        else:
            self.solipsism_counter = 0

    def _trigger_ballast(self):
        if not self.ballast_state["active"]:
            self.ballast_state["active"] = True
            self.ballast_state["turns_remaining"] = 3
            self.sub.events.log(f"{Prisma.VIOLET}CORTEX: Solipsism detected. Ballast Protocol ENGAGED.{Prisma.RST}", "SYS")


class NeuroPlasticity:
    """
    The Weaver. Connects concepts that fire together.
    """
    def __init__(self):
        self.plasticity_mod = 1.0

    def force_hebbian_link(self, graph, word_a, word_b):
        if word_a == word_b: return None
        if word_a not in graph:
            graph[word_a] = {"edges": {}, "last_tick": 0}
        if word_b not in graph:
            graph[word_b] = {"edges": {}, "last_tick": 0}

        current_weight = graph[word_a]["edges"].get(word_b, 0.0)
        new_weight = min(10.0, current_weight + 2.5)

        graph[word_a]["edges"][word_b] = new_weight
        graph[word_b]["edges"][word_a] = min(10.0, graph[word_b]["edges"].get(word_a, 0.0) + 1.0)

        return f"{Prisma.MAG}⚡ HEBBIAN GRAFT: Wired '{word_a}' <-> '{word_b}'.{Prisma.RST}"

class ShimmerState:
    def __init__(self, max_val=50.0):
        self.current = max_val
        self.max_val = max_val
    def recharge(self, amount): self.current = min(self.max_val, self.current + amount)
    def spend(self, amount):
        if self.current >= amount:
            self.current -= amount
            return True
        return False

class DreamEngine:
    def __init__(self, events):
        self.events = events
        self.PROMPTS = DREAMS.get("PROMPTS", ["{A} -> {B}?"])

    def hallucinate(self, vector: Dict[str, float]) -> str:
        # Placeholder for future expansion
        return f"Dreaming of {len(vector)} dimensions..."