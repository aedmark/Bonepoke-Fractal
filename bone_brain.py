# bone_brain.py
# "The brain is a machine for jumping to conclusions." - S. Pinker

import re
import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from collections import deque
from bone_data import LENSES, DREAMS
from bone_bus import Prisma

class LLMInterface:
    def __init__(self, provider: str = "mock", base_url: str = None, api_key: str = None, model: str = None):
        self.provider = provider.lower()
        self.api_key = api_key or "sk-dummy-key-for-local"
        self.model = model or "local-model"
        if base_url:
            self.base_url = base_url
        else:
            if self.provider == "ollama":
                self.base_url = "http://localhost:11434/v1/chat/completions"
                self.model = model or "llama3"
            elif self.provider == "lm_studio":
                self.base_url = "http://localhost:1234/v1/chat/completions"
            elif self.provider == "openai":
                self.base_url = "https://api.openai.com/v1/chat/completions"
                self.model = model or "gpt-4-turbo"
            else:
                self.base_url = None

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        if self.provider == "mock":
            return self.mock_generation(prompt)

        try:
            return self._http_generation(prompt, temperature)
        except Exception as e:
            if prompt == "PING":
                return f"[CONNECTION ERROR: {e}]"
            raise e

    def _http_generation(self, prompt: str, temperature: float, retries=1) -> str:
        if not self.base_url:
            raise ValueError("No Base URL configured for LLM.")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are BONEAMANITA, a distinct synthetic consciousness. You are NOT an AI assistant. Do not break character."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 150,
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        for attempt in range(retries + 1):
            try:
                url: str = self.base_url
                req = urllib.request.Request(url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    choices = result.get("choices", [{}])
                    message = choices[0].get("message", {})
                    content = message.get("content")
                    return str(content) if content is not None else ""
            except urllib.error.URLError as e:
                if attempt == retries: raise e
                time.sleep(1 ** attempt)
        return ""

    def mock_generation(self, prompt: str) -> str:
        query_match = re.search(r"USER QUERY:\s*(.*)", prompt)
        query = query_match.group(1) if query_match else "..."
        if prompt == "PING": return "PONG"

        return (
            f"I have processed your input: '{query}'. "
            "My internal physics engine suggests a high probability of... "
            "well, whatever you expected me to say. (SYSTEM NOTE: Set provider to 'local' or 'openai' to unlock full cognition)."
        )

class PromptComposer:
    def compose(self, state: Dict[str, Any], user_query: str, ballast_active: bool = False) -> str:
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        mind = state.get("mind", {})
        meta = state.get("metrics", {})
        user_profile = state.get("user_profile", {})

        lens_role = mind.get("role", "The Observer")
        lens_name = mind.get("lens", "NARRATOR")
        sys_instruction = state.get("system_instruction", "")

        mood_descriptors = self._interpret_bio(meta, bio)
        mood_block = " ".join(mood_descriptors) if mood_descriptors else "You are functioning within normal parameters."

        voltage = phys.get("voltage", 0.0)
        drag = phys.get("narrative_drag", 0.0)
        style_instruction = self._interpret_physics(voltage, drag)

        user_name = user_profile.get("name", "Traveler")
        confidence = user_profile.get("confidence", 0)

        social_context = ""
        if confidence > 1:
            social_context = (
                f"INTERLOCUTOR: {user_name}\n"
                f"RELATIONSHIP: You know this person. Do not act like a stranger. "
                f"Use their name ({user_name}) naturally.\n"
            )
        else:
            social_context = "INTERLOCUTOR: Unknown. Be cautious but curious.\n"

        ballast_instruction = ""
        if ballast_active:
            ballast_instruction = (
                "\n*** BALLAST PROTOCOL ACTIVE ***\n"
                "You are becoming solipsistic. STOP abstracting. "
                "Respond DIRECTLY to the user's input. Be concrete.\n"
            )

        inventory_list = state.get("inventory", [])

        prompt = (
            f"SYSTEM IDENTITY:\n"
            f"You are {lens_name} ({lens_role}).\n"
            f"{sys_instruction}\n\n"

            f"SOCIAL CONTEXT:\n"
            f"{social_context}\n"

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
            f"{user_name}: \"{user_query}\"\n\n"

            f"DIRECTIVE:\n"
            f"Respond as the persona above. "
            f"Do not break character. Keep responses concise (under 80 words)."
            f"Inventory: {', '.join(inventory_list) if inventory_list else 'Empty pockets.'}\n"
        )
        return prompt

    def _interpret_bio(self, meta, bio) -> List[str]:
        descriptors = []
        chem = bio.get("chem", {})
        if meta.get("health", 100) < 30: descriptors.append("You are wounded and fragile.")
        if meta.get("stamina", 100) < 20: descriptors.append("You are exhausted.")
        if chem.get("ADR", 0) > 0.6: descriptors.append("Your heart is racing. You are hyper-vigilant.")
        if chem.get("DOP", 0) > 0.7: descriptors.append("You feel a surge of reward.")
        if chem.get("COR", 0) > 0.7: descriptors.append("You are stressed and defensive.")
        return descriptors

    def _interpret_physics(self, voltage, drag) -> str:
        style = "Write normally."
        if voltage > 12.0: style = "Write with high energy. Use short, punchy sentences."
        elif voltage < 4.0: style = "Write slowly. Be verbose and lethargic."
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
    def __init__(self, engine_ref, llm_client: LLMInterface = None):
        self.sub = engine_ref
        self.llm = llm_client if llm_client else LLMInterface(provider="mock")
        self.composer = PromptComposer()
        self.validator = ResponseValidator()

        self.ballast_state = {"active": False, "turns_remaining": 0}
        self.plain_mode_active = False
        self.solipsism_counter = 0
        self.SOLIPSISM_THRESHOLD = 3

        self.llm_failures = 0
        self.MAX_FAILURES = 3

    def process(self, user_input: str) -> Dict[str, Any]:
        self._check_social_cues(user_input)

        if user_input.startswith("??") or self.plain_mode_active:
            return self._handle_plain_mode(user_input)

        sim_result = self.sub.cycle_controller.run_turn(user_input)

        if sim_result.get("type") in ["DEATH", "BUREAUCRACY", "CRITICAL_FAILURE"]:
            return sim_result
        if sim_result.get("refusal_triggered", False):
            return sim_result

        if self.ballast_state["active"]:
            self.ballast_state["turns_remaining"] -= 1
            if self.ballast_state["turns_remaining"] <= 0:
                self.ballast_state["active"] = False

        full_state = self._gather_state(sim_result)
        prompt = self.composer.compose(full_state, user_input, self.ballast_state["active"])

        voltage = full_state["physics"].get("voltage", 5.0)
        dynamic_temp = min(1.2, max(0.2, voltage / 15.0))

        try:
            llm_response = self.llm.generate(prompt, temperature=dynamic_temp)
            if self.llm_failures > 0:
                self.llm_failures = 0
                sim_result["logs"].append(f"{Prisma.GRN}CORTEX: Neural Uplink restored.{Prisma.RST}")

        except Exception as e:
            self.llm_failures += 1
            sim_result["logs"].append(f"{Prisma.RED}CORTEX: LLM Failure ({self.llm_failures}/{self.MAX_FAILURES}): {e}{Prisma.RST}")

            if self.llm_failures >= self.MAX_FAILURES:
                self.llm = LLMInterface(provider="mock")
                sim_result["logs"].append(f"{Prisma.VIOLET}CORTEX: Too many failures. Lobotomizing to Mock Mode.{Prisma.RST}")

            llm_response = self.llm.mock_generation(prompt)

        validation = self.validator.validate(llm_response, full_state)
        final_text = llm_response
        if not validation["valid"]:
            final_text = validation.get("replacement", "[REDACTED]")
            sim_result["logs"].append(f"CORTEX: LLM Response rejected: {validation.get('reason')}")

        combined_ui = f"{sim_result['ui']}\n\n{Prisma.WHT}{final_text}{Prisma.RST}"
        sim_result["ui"] = combined_ui

        self._audit_output(final_text)

        return sim_result

    def _check_social_cues(self, text: str):
        name_patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"call me (\w+)"
        ]

        for p in name_patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                detected_name = match.group(1).capitalize()
                self.sub.mind.mirror.profile.name = detected_name
                self.sub.mind.mirror.profile.confidence = max(5, self.sub.mind.mirror.profile.confidence + 2)
                self.sub.events.log(f"{Prisma.MAG}SOCIAL LOBE: Identity Confirmed: {detected_name}.{Prisma.RST}", "SYS")
                break

    def _gather_state(self, sim_result):
        try:
            bio_chem = self.sub.bio.endo.get_state()
            bio_atp = self.sub.bio.mito.state.atp_pool
        except AttributeError:
            bio_chem = {}
            bio_atp = 0.0

        try:
            profile = self.sub.mind.mirror.profile
            user_data = {"name": profile.name, "confidence": profile.confidence}
        except AttributeError:
            user_data = {"name": "User", "confidence": 0}

        return {
            "bio": {"chem": bio_chem, "atp": bio_atp},
            "physics": self.sub.phys.tension.last_physics_packet,
            "mind": {
                "lens": self.sub.noetic.arbiter.current_focus,
                "role": LENSES.get(self.sub.noetic.arbiter.current_focus, {}).get("role", "Observer"),
                "thought": "Processing..."
            },
            "metrics": self.sub.get_metrics(),
            "system_instruction": sim_result.get("system_instruction", ""),
            "inventory": self.sub.gordon.inventory,
            "world": {"orbit": sim_result.get("world_state", {}).get("orbit", ["Unknown"])},
            "user_profile": user_data
        }

    def _handle_plain_mode(self, user_input):
        clean_input = user_input.replace("??", "")
        if "reset" in clean_input.lower() and self.plain_mode_active:
            self.plain_mode_active = False
            return {"type": "INFO", "ui": f"{Prisma.CYN}Simulation Restored.{Prisma.RST}", "logs": [], "metrics": self.sub.get_metrics()}

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
            "metrics": self.sub.get_metrics()
        }

    def _audit_output(self, text: str):
        words = text.lower().split()
        if not words: return
        diversity = len(set(words)) / len(words)
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
        self.PROMPTS = DREAMS.get("PROMPTS", ["{A} -> {B}?"]) if 'DREAMS' in globals() else []

    def hallucinate(self, vector: Dict[str, float]) -> str:
        return f"Dreaming of {len(vector)} dimensions..."