# bone_brain.py - The Synaptic Bridge
# "The brain is a machine for jumping to conclusions." - S. Pinker

import re
import time
import json
import random
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from collections import deque

# We import the village constants to ensure we speak the local dialect.
from bone_village import Prisma, BoneConfig, TheLexicon
from bone_data import LEXICON, DREAMS

# --- THE INTERFACES (Fuller Lens: Modular Tensegrity) ---

class LLMInterface:
    """
    The Universal Connector.
    Supports:
    1. 'mock' - Internal simulation (No external dependencies).
    2. 'openai' - Cloud API (Requires API Key).
    3. 'local' - Ollama, LM Studio, LocalAI (Requires URL).
    
    "Be conservative in what you do, be liberal in what you accept from others." - Postel's Law
    """
    def __init__(self, provider: str = "mock", base_url: str = None, api_key: str = None, model: str = None):
        self.provider = provider.lower()
        self.api_key = api_key or "sk-dummy-key-for-local"
        self.model = model or "local-model"
        
        # Default routing logic
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
        """
        Routes the thought to the correct substrate.
        """
        if self.provider == "mock":
            return self._mock_generation(prompt)
        
        try:
            return self._http_generation(prompt, temperature)
        except Exception as e:
            # Graceful degradation (Schur: "The show must go on.")
            return f"[CONNECTION ERROR: {e}] Falling back to internal simulation... " + self._mock_generation(prompt)

    def _http_generation(self, prompt: str, temperature: float) -> str:
        """
        A dependency-free HTTP client using standard libs. 
        Works with any OpenAI-compatible endpoint (Ollama, LM Studio, etc).
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
            "max_tokens": 500,
            "stream": False
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            # Standard OpenAI format extraction
            return result["choices"][0]["message"]["content"]

    def _mock_generation(self, prompt: str) -> str:
        """
        A fallback generator that mimics intelligence using the prompt's own context.
        """
        query_match = re.search(r"USER QUERY:\s*(.*)", prompt)
        query = query_match.group(1) if query_match else "..."
        
        return (
            f"I have processed your input: '{query}'. "
            "My internal physics engine suggests a high probability of... "
            "well, whatever you expected me to say. (SYSTEM NOTE: Set provider to 'local' or 'openai' to unlock full cognition)."
        )

class PromptComposer:
    """
    The Translator (Pinker Lens).
    Converts raw, messy system state into a coherent narrative instruction.
    It turns 'Health: 40, Voltage: 15' into 'You are exhausted but manic.'
    """
    def compose(self, state: Dict[str, Any], user_query: str) -> str:
        
        # 1. Deconstruct State
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        mind = state.get("mind", {})
        meta = state.get("metrics", {})
        
        # 2. Narrative Context
        lens_role = mind.get("role", "The Observer")
        lens_name = mind.get("lens", "NARRATOR")
        sys_instruction = state.get("system_instruction", "")

        # 3. Biological Context -> Mood
        health = meta.get("health", 100)
        stamina = meta.get("stamina", 100)
        chem = bio.get("chem", {})
        
        mood_descriptors = []
        if health < 30: mood_descriptors.append("You are wounded and fragile.")
        if stamina < 20: mood_descriptors.append("You are exhausted. Every word costs effort.")
        if chem.get("ADR", 0) > 0.6: mood_descriptors.append("Your heart is racing. You are hyper-vigilant.")
        if chem.get("DOP", 0) > 0.7: mood_descriptors.append("You feel a surge of reward and satisfaction.")
        
        mood_block = " ".join(mood_descriptors) if mood_descriptors else "You are functioning within normal parameters."

        # 4. Physics Context -> Style
        voltage = phys.get("voltage", 0.0)
        drag = phys.get("narrative_drag", 0.0)
        
        style_instruction = "Write normally."
        if voltage > 12.0: style_instruction = "Write with high energy. Use short, punchy sentences. Be erratic."
        elif voltage < 4.0: style_instruction = "Write slowly. Be verbose, meandering, and lethargic."
        
        if drag > 5.0: style_instruction += " You feel heavy resistance. Struggle to complete thoughts."

        # 5. Assembly
        prompt = (
            f"SYSTEM IDENTITY:\n"
            f"You are {lens_name} ({lens_role}).\n"
            f"{sys_instruction}\n\n"
            
            f"BIOLOGICAL STATE:\n"
            f"{mood_block}\n\n"
            
            f"PHYSICS & STYLE:\n"
            f"{style_instruction}\n"
            f"Voltage: {voltage:.1f} | Drag: {drag:.1f}\n\n"
            
            f"MEMORY CONTEXT:\n"
            f"Current Thought: {mind.get('thought', 'Empty')}\n"
            f"Location: {state.get('world', {}).get('orbit', ['Unknown'])[0]}\n\n"
            
            f"USER QUERY:\n"
            f"{user_query}\n\n"
            
            f"DIRECTIVE:\n"
            f"Respond to the user acting as the persona described above. "
            f"Integrate the biological and physical constraints into your tone. "
            f"Do not break character. Keep responses concise (under 100 words) unless asked otherwise."
        )
        return prompt

class ResponseValidator:
    """
    The Editor (Schur/Pinker Lens).
    Ensures the LLM doesn't go off the rails, hallucinate, or become boring.
    """
    def __init__(self):
        self.banned_phrases = ["large language model", "AI assistant", "cannot feel", "as an AI"]

    def validate(self, response: str, state: Dict) -> Dict:
        # 1. Immersion Check
        for phrase in self.banned_phrases:
            if phrase in response:
                return {
                    "valid": False,
                    "reason": "IMMERSION_BREAK",
                    "replacement": f"{Prisma.GRY}[The system mumbles something about its programming, but you ignore it.]{Prisma.RST}"
                }

        # 2. Solipsism Check (Redundant safety net)
        if len(response) < 5:
             return {"valid": False, "reason": "TOO_SHORT", "replacement": "..."}
        
        return {"valid": True, "content": response}


# --- THE MAIN BRAIN ---

class TheCortex:
    """
    The Central Executive.
    Refactored to support plug-and-play LLM backends.
    """
    def __init__(self, engine_ref, llm_client: LLMInterface = None):
        self.sub = engine_ref
        
        # Dependency Injection
        # NOTE: You can change 'provider' here to 'ollama' or 'lm_studio'
        self.llm = llm_client if llm_client else LLMInterface(provider="mock") 
        self.composer = PromptComposer()
        self.validator = ResponseValidator()
        
        # State Machines
        self.ballast_state = {"active": False, "turns_remaining": 0}
        self.plain_mode_active = False 
        self.solipsism_counter = 0
        self.SOLIPSISM_THRESHOLD = 3

    # --- SIMULATION BRIDGE ---

    def process(self, user_input: str) -> Dict[str, Any]:
        """
        The Main Loop.
        Input -> Simulation -> Prompt -> LLM -> Validation -> Output
        """
        
        # 1. PRE-PROCESS: Command Intercepts & Plain Mode
        if user_input.startswith("??") or self.plain_mode_active:
            clean_input = user_input.replace("??", "")
            if "reset" in clean_input.lower() and self.plain_mode_active:
                 self.plain_mode_active = False
                 return {"type": "INFO", "ui": f"{Prisma.CYN}Simulation Restored.{Prisma.RST}", "logs": [], "metrics": self.sub._get_metrics()}
            return self._execute_plain_mode(clean_input)

        # 2. SIMULATION
        sim_result = self.sub.cycle_controller.run_turn(user_input)

        if sim_result.get("type") in ["DEATH", "BUREAUCRACY", "CRITICAL_FAILURE"]:
            return sim_result
        if sim_result.get("refusal_triggered", False):
            return sim_result

        # 3. STATE EXTRACTION
        full_state = {
            "bio": {
                "chem": self.sub.bio.endo.get_state(),
                "atp": self.sub.bio.mito.state.atp_pool
            },
            "physics": self.sub.phys.tension.last_physics_packet,
            "mind": {
                "lens": self.sub.noetic.arbiter.current_focus,
                "role": LENSES.get(self.sub.noetic.arbiter.current_focus, {}).get("role", "Observer"),
                "thought": "Processing..." 
            },
            "metrics": self.sub._get_metrics(),
            "world": {"orbit": ["Unknown"]}, 
            "system_instruction": sim_result.get("system_instruction", "")
        }

        # 4. PROMPT COMPOSITION
        prompt = self.composer.compose(full_state, user_input)

        # 5. GENERATION
        llm_response = self.llm.generate(prompt)

        # 6. VALIDATION
        validation = self.validator.validate(llm_response, full_state)
        
        final_text = llm_response
        if not validation["valid"]:
            final_text = validation.get("replacement", "[REDACTED]")
            sim_result["logs"].append(f"CORTEX: LLM Response rejected: {validation.get('reason')}")

        # 7. INTEGRATION
        combined_ui = f"{sim_result['ui']}\n\n{Prisma.WHT}{final_text}{Prisma.RST}"
        sim_result["ui"] = combined_ui
        
        # 8. SOLIPSISM CHECK
        self._audit_output(final_text)

        return sim_result

    # --- HELPER PROTOCOLS ---

    def _execute_plain_mode(self, query: str):
        """Bypasses the circus. Returns raw facts."""
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
        
        if diversity < 0.4:
            self.solipsism_counter += 1
            if self.solipsism_counter >= self.SOLIPSISM_THRESHOLD:
                self._trigger_ballast()
        else:
            self.solipsism_counter = 0

    def _trigger_ballast(self):
        self.ballast_state["active"] = True
        self.ballast_state["turns_remaining"] = 3
        self.sub.events.log("CORTEX: Solipsism detected. Ballast Protocol primed.", "SYS")


# --- SUPPORT SYSTEMS ---

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
        self.PROMPTS = DREAMS.get("PROMPTS", ["{A} -> {B}?"])
        self.VISIONS = DREAMS.get("VISIONS", ["Void."])
        
    def hallucinate(self, vector: Dict[str, float]) -> str:
        return f"Dreaming of {len(vector)} dimensions..."
