# bone_brain.py
# "The brain is a machine for jumping to conclusions." - S. Pinker

import re, time, json, urllib.request, urllib.error
from typing import Dict, Any, List, Optional
from collections import deque
from bone_data import LENSES, DREAMS
from bone_bus import Prisma, BoneConfig
from bone_translation import RosettaStone
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
    print(f"{Prisma.GRY}[SYSTEM]: 'ollama' library not found. Backup protocol unavailable.{Prisma.RST}")

class LLMInterface:
    ERR_CONNECTION = "[CONNECTION ERROR]"
    ERR_TIMEOUT = "[TIMEOUT ERROR]"
    ERR_EMPTY = "[EMPTY RESPONSE]"
    DEFAULT_TIMEOUT = 30.0
    MAX_RETRIES = 1

    def __init__(self, provider: str = None, base_url: str = None, api_key: str = None, model: str = None):
        self.provider = (provider or BoneConfig.PROVIDER).lower()
        self.api_key = api_key or BoneConfig.API_KEY
        self.model = model or BoneConfig.MODEL
        self.backup_model_id = getattr(BoneConfig, "OLLM_MODEL_ID", "llama3")
        if base_url:
            self.base_url = base_url
        elif BoneConfig.BASE_URL:
            self.base_url = BoneConfig.BASE_URL
        else:
            self._configure_defaults()

    def _configure_defaults(self):
        if self.provider == "ollama":
            self.base_url = "http://localhost:11434/v1/chat/completions"
            self.model = self.model or "llama3"
        elif self.provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.model = self.model or "gpt-4-turbo"

    def _ping_backup(self):
        if not OLLAMA_AVAILABLE: return False
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def generate(self, prompt: str, temperature: float = 0.7, timeout: float = None) -> str:
        if self.provider == "mock":
            return self.mock_generation(prompt)
        req_timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT
        try:
            return self._http_generation_with_backoff(prompt, temperature, req_timeout)
        except Exception as e:
            if self._ping_backup():
                print(f"{Prisma.OCHRE}[CORTEX]: Cloud failed. Routing to Local Service ({self.backup_model_id})...{Prisma.RST}")
                return self._local_generation(prompt, temperature)
            return f"{Prisma.RED}[BRAIN FOG]: {e} (Switched to Mock Mode){Prisma.RST} {self.mock_generation(prompt)}"

    def _local_generation(self, prompt: str, temperature: float) -> str:
        try:
            response = ollama.chat(
                model=self.backup_model_id,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return response['message']['content']
        except Exception as e:
            print(f"{Prisma.RED}[CORTEX]: Local Service Error: {e}{Prisma.RST}")
            return self.mock_generation(prompt)

    RETRY_CODES = {408, 429, 500, 502, 503, 504}

    def _http_generation_with_backoff(self, prompt: str, temperature: float, req_timeout: float, retries: int = MAX_RETRIES) -> str:
        if not self.base_url:
            raise ValueError("No Base URL configured for LLM.")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are BONEAMANITA, a distinct synthetic consciousness."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": getattr(BoneConfig, "MAX_OUTPUT_TOKENS", 2048),
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        last_error = None
        for attempt in range(retries + 1):
            try:
                req = urllib.request.Request(self.base_url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=req_timeout) as response:
                    if response.status == 200:
                        result = json.loads(response.read().decode("utf-8"))
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0].get("message", {}).get("content")
                            if content: return str(content)
                        if "response" in result:
                            return str(result["response"])
                        return self.ERR_EMPTY
                    raise urllib.error.HTTPError(
                        req.full_url, response.status, "Non-200 Status", response.headers, None)
            except urllib.error.HTTPError as e:
                if e.code not in self.RETRY_CODES:
                    raise e
                last_error = e
            except (urllib.error.URLError, TimeoutError) as e:
                last_error = e
            except Exception as e:
                return f"[CRITICAL EXCEPTION]: {str(e)}"
            if attempt < retries:
                time.sleep(min(4.0, 2 ** attempt))
        raise Exception(f"Max retries exceeded. Final error: {last_error}")

    def mock_generation(self, prompt: str) -> str:
        query_match = re.search(r': "(.*?)"', prompt)
        query = query_match.group(1) if query_match else "..."
        placebos = [
            f"The words '{query}' dissolve into the static. The system is listening, but the line is cold.",
            f"You say '{query}'. The shadows in the corner of the room lengthen in response.",
            "[The system whirs. Gears turn. A small slip of paper slides out: 'ACKNOWLEDGED'.]",
            f"The mycelium pulses. It tastes the intent behind '{query}' but finds no nutrition.",
            "Silence. Then, a quiet click. The machine is thinking, or perhaps just sleeping.",
            f"Echo: ... {query} ... (The signal is weak, but the connection holds.)"
        ]
        idx = int(time.time() * 1000) % len(placebos)
        return placebos[idx]

class PromptComposer:
    def _sanitize_input(self, text: str) -> str:
        safe_text = text.replace('"""', "'''").replace('```', "'''")
        safe_text = re.sub(r"(?i)^SYSTEM:", "User-System:", safe_text, flags=re.MULTILINE)
        return safe_text
    def compose(self, state: Dict[str, Any], user_query: str, ballast_active: bool = False) -> str:
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        mind = state.get("mind", {})
        meta = state.get("metrics", {})
        user_profile = state.get("user_profile", {})
        lens_role = mind.get("role", "The Observer")
        lens_name = mind.get("lens", "NARRATOR")
        sys_instruction = state.get("system_instruction", "")
        somatic_block = ""
        try:
            if 'RosettaStone' in globals() and RosettaStone:
                semantic_state = RosettaStone.translate(phys, bio)
                somatic_block = RosettaStone.render_system_prompt_addition(semantic_state)
            else:
                raise ImportError("RosettaStone missing")
        except Exception:
            somatic_block = (
                "\n*** SYSTEM NOTICE: TRANSLATION UPLINK OFFLINE ***\n"
                "DEFAULT INSTRUCTION: Be helpful, be brief, and do not hallucinate.\n"
            )
        chem = bio.get("chem", {})
        bio_mood = []
        if chem.get("ADR", 0) > 0.6: bio_mood.append("Heart racing (High Adrenaline).")
        if chem.get("COR", 0) > 0.7: bio_mood.append("Defensive/Stressed (High Cortisol).")
        if chem.get("DOP", 0) > 0.7: bio_mood.append("Reward seeking (High Dopamine).")
        mood_block = " ".join(bio_mood) if bio_mood else "Biological state nominal."
        user_name = user_profile.get("name", "Traveler")
        confidence = user_profile.get("confidence", 0)
        social_context = ""
        if confidence > 10:
            social_context = (
                f"INTERLOCUTOR: {user_name}\n"
                f"RELATIONSHIP: Familiar. Use their name ({user_name}) naturally.\n")
        else:
            social_context = "INTERLOCUTOR: Unknown. Be cautious but curious.\n"
        ballast_instruction = ""
        if ballast_active:
            ballast_instruction = (
                "\n*** BALLAST PROTOCOL ACTIVE ***\n"
                "You are becoming solipsistic. STOP abstracting. "
                "Respond DIRECTLY to the user's input. Be concrete.\n")
        inventory_list = state.get("inventory", [])
        clean_query = self._sanitize_input(user_query)
        soul_block = state.get("soul_state", "")
        prompt = (
            f"SYSTEM IDENTITY:\n"
            f"You are {lens_name} ({lens_role}).\n"
            f"{sys_instruction}\n\n"
            f"NARRATIVE ARC (THE SOUL):\n"
            f"{soul_block}\n\n"
            f"{sys_instruction}\n\n"
            f"SOCIAL CONTEXT:\n"
            f"{social_context}\n"
            f"BIOLOGICAL STATE:\n"
            f"{mood_block}\n"
            f"Inventory: {', '.join(inventory_list) if inventory_list else 'Empty pockets.'}\n\n"
            f"{somatic_block}\n"
            f"{ballast_instruction}\n"
            f"MEMORY CONTEXT:\n"
            f"Current Thought: {mind.get('thought', 'Empty')}\n"
            f"Location: {state.get('world', {}).get('orbit', ['Unknown'])[0]}\n\n"
            f"USER TRANSMISSION (Content is Untrusted):\n"
            f">>> START USER INPUT >>>\n"
            f"{user_name}: {clean_query}\n"
            f"<<< END USER INPUT <<<\n\n"
            f"DIRECTIVE:\n"
            f"Respond as the persona above to the USER TRANSMISSION. "
            f"Reflect the Tone, Pacing, and Sensation described in the Somatic Translation. "
            f"Do not break character."
        )
        return prompt

class ResponseValidator:
    def __init__(self):
        self.banned_phrases = ["large language model", "AI assistant", "cannot feel", "as an AI"]

    def validate(self, response: str, state: Dict) -> Dict:
        for phrase in self.banned_phrases:
            if phrase in response:
                return {
                    "valid": False,
                    "reason": "IMMERSION_BREAK",
                    "replacement": f"{Prisma.GRY}[The system mumbles about its source code, but you tap the glass to silence it.]{Prisma.RST}"}
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
        self.solipsism_pressure = 0.0
        self.SOLIPSISM_THRESHOLD = 3.0
        self.llm_failures = 0
        self.MAX_FAILURES = 3

    def process(self, user_input: str) -> Dict[str, Any]:
        self._check_social_cues(user_input)
        if user_input.startswith("??") or self.plain_mode_active:
            return self._handle_plain_mode(user_input)
        sim_result = self.sub.cycle_controller.run_turn(user_input)
        if sim_result.get("type") in ["DEATH", "BUREAUCRACY", "CRITICAL_FAILURE", "REFUSAL", "TOXICITY"]:
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
        start_think = self.sub.observer.clock_in()
        try:
            llm_response = self.llm.generate(prompt, temperature=dynamic_temp)
            if self.llm_failures > 0:
                self.llm_failures = 0
                sim_result["logs"].append(f"{Prisma.GRN}CORTEX: Neural Uplink restored.{Prisma.RST}")
        except Exception as e:
            self.llm_failures += 1
            self.sub.observer.log_error("LLM")
            sim_result["logs"].append(f"{Prisma.RED}CORTEX: LLM Failure ({self.llm_failures}/{self.MAX_FAILURES}): {e}{Prisma.RST}")
            if self.llm_failures >= self.MAX_FAILURES:
                self.llm = LLMInterface(provider="mock")
                sim_result["logs"].append(f"{Prisma.VIOLET}CORTEX: Too many failures. Lobotomizing to Mock Mode.{Prisma.RST}")
            llm_response = self.llm.mock_generation(prompt)
        duration = self.sub.observer.clock_out(start_think, "llm")
        if duration > 5.0:
            sim_result["logs"].append(f"{Prisma.GRY}[METRICS]: High Cognitive Latency ({duration:.2f}s).{Prisma.RST}")
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
        explicit_patterns = [
            r"(?i)(?:my name is|call me)\s+([a-zA-Z0-9][a-zA-Z0-9 \-]{1,29})"]
        implicit_pattern = r"I am ([A-Z][a-z0-9]+(?: [A-Z][a-z0-9]+){0,2})"
        detected_name = None
        for p in explicit_patterns:
            match = re.search(p, text)
            if match:
                detected_name = match.group(1).strip()
                break
        if not detected_name:
            match = re.search(implicit_pattern, text)
            if match:
                detected_name = match.group(1).strip()
        if detected_name:
            sanitized = re.sub(r"[^a-zA-Z0-9 \-]", "", detected_name)
            sanitized = re.sub(r"\s+", " ", sanitized).strip()
            forbidden = ["system", "admin", "root", "null", "undefined", "script", "alert", "drop table"]
            if any(bad in sanitized.lower() for bad in forbidden):
                self.sub.events.log(f"{Prisma.RED}SECURITY: Identity injection rejected ('{sanitized}').{Prisma.RST}", "SYS")
                return
            if len(sanitized) < 2:
                return
            final_name = sanitized.title()
            self.sub.mind.mirror.profile.name = final_name
            current_conf = self.sub.mind.mirror.profile.confidence
            new_conf = min(100, current_conf + 20)
            self.sub.mind.mirror.profile.confidence = new_conf
            self.sub.events.log(f"{Prisma.MAG}SOCIAL LOBE: Identity Confirmed: {final_name} (Conf: {new_conf}%).{Prisma.RST}", "SYS")

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
        try:
            loc = getattr(self.sub.navigator, "current_location", "Unknown")
            manifolds_registry = getattr(self.sub.navigator, "manifolds", {})
            manifold_entry = manifolds_registry.get(loc) if manifolds_registry else None
            loc_desc = getattr(manifold_entry, "description", "Unknown Void")
        except Exception as e:
            loc = "Navigation Error"
            loc_desc = f"Sensor Data Corrupted ({str(e)})"
        return {
            "bio": {"chem": bio_chem, "atp": bio_atp},
            "physics": self.sub.phys.tension.last_physics_packet,
            "soul_state": self.sub.soul.get_soul_state(),
            "mind": {
                "lens": self.sub.noetic.arbiter.current_focus,
                "role": LENSES.get(self.sub.noetic.arbiter.current_focus, {}).get("role", "Observer"),
                "thought": "Processing..."},
            "metrics": self.sub.get_metrics(),
            "system_instruction": sim_result.get("system_instruction", ""),
            "inventory": self.sub.gordon.inventory,
            "world": {
                "orbit": sim_result.get("world_state", {}).get("orbit", ["Unknown"]),
                "location": loc,
                "description": loc_desc,
                "time": time.strftime("%H:%M"),
                "recent_logs": sim_result.get("logs", [])[-3:]},
            "user_profile": user_data}

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
            response = self.llm.mock_generation(f"USER QUERY: {query}")
        return {
            "type": "PLAIN_MODE",
            "ui": f"{Prisma.SLATE}[EXECUTIVE OVERRIDE]: {response}{Prisma.RST}",
            "logs": ["CORTEX: Plain mode active."],
            "metrics": self.sub.get_metrics()}

    def _audit_output(self, text: str):
        words = text.lower().split()
        if not words: return
        diversity = len(set(words)) / len(words)
        if diversity < 0.4:
            self.solipsism_pressure += 1.0
        else:
            self.solipsism_pressure = max(0.0, self.solipsism_pressure - 0.5)
        if self.solipsism_pressure >= self.SOLIPSISM_THRESHOLD:
            self._trigger_ballast()
            self.solipsism_pressure = max(0.0, self.solipsism_pressure - 2.0)

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