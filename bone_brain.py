""" bone_brain.py
# "The brain is a machine for jumping to conclusions." - S. Pinker """

import re, time, json, urllib.request, urllib.error, random, math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from bone_data import LENSES, DREAMS
from bone_bus import Prisma, BoneConfig, EventBus
from bone_symbiosis import SymbiosisManager
from bone_spores import MycelialNetwork
from bone_lexicon import TheLexicon
from bone_translation import RosettaStone
from bone_telemetry import TelemetryService

def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    intersection = set(vec_a.keys()) & set(vec_b.keys())
    numerator = sum(vec_a[k] * vec_b[k] for k in intersection)
    sum1 = sum(vec_a[k]**2 for k in vec_a.keys())
    sum2 = sum(vec_b[k]**2 for k in vec_b.keys())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator: return 0.0
    return numerator / denominator

@dataclass
class BrainConfig:
    BASE_PLASTICITY: float = 0.4
    VOLTAGE_SENSITIVITY: float = 0.03
    MAX_PLASTICITY: float = 0.95
    BASE_DECAY_RATE: float = 0.1
    BASE_TEMP: float = 0.7
    BASE_TOP_P: float = 0.9
    CORTISOL_FREEZE: float = 0.2
    DOPAMINE_NOVELTY: float = 0.4
    ADRENALINE_RUSH: float = 600.0
    SEROTONIN_CALM: float = 0.5

@dataclass
class ChemicalState:
    dopamine: float = 0.0
    cortisol: float = 0.0
    adrenaline: float = 0.0
    serotonin: float = 0.0

    def decay(self, rate: float = 0.2):
        self.dopamine = max(0.0, self.dopamine * (1.0 - rate))
        self.cortisol = max(0.0, self.cortisol * (1.0 - rate))
        self.adrenaline = max(0.0, self.adrenaline * (1.0 - rate))
        self.serotonin = max(0.0, self.serotonin * (1.0 - rate))

    def mix(self, new_state: Dict[str, float], weight: float = 0.5):
        self.dopamine = (self.dopamine * (1.0 - weight)) + (new_state.get("DOP", 0.0) * weight)
        self.cortisol = (self.cortisol * (1.0 - weight)) + (new_state.get("COR", 0.0) * weight)
        self.adrenaline = (self.adrenaline * (1.0 - weight)) + (new_state.get("ADR", 0.0) * weight)
        self.serotonin = (self.serotonin * (1.0 - weight)) + (new_state.get("SER", 0.0) * weight)

class NarrativeSpotlight:
    def __init__(self):
        self.dimension_map = {
            "STR": {"heavy", "constructive", "base"},
            "VEL": {"kinetic", "explosive", "mot"},
            "ENT": {"antigen", "toxin", "broken", "void"},
            "PHI": {"thermal", "photo", "explosive"},
            "PSI": {"abstract", "sacred", "void", "idea"},
            "BET": {"suburban", "solvents", "play"}
        }
        self.semantic_drift_factor = 0.1

    def expand_horizon(self, dimension: str, new_category: str):
        if dimension in self.dimension_map:
            self.dimension_map[dimension].add(new_category)

    def illuminate(self, graph: Dict, vector: Dict[str, float], limit: int = 5) -> List[str]:
        if not graph or not vector:
            return []
        active_dims = {k: v for k, v in vector.items() if v > 0.6}
        if not active_dims:
            return []
        scored_memories = []
        secondary_candidates = set()
        for node, data in graph.items():
            resonance_score = 0.0
            if TheLexicon:
                node_cats = TheLexicon.get_categories_for_word(node)
                for dim, val in active_dims.items():
                    target_flavors = self.dimension_map.get(dim, set())
                    if node_cats & target_flavors:
                        resonance_score += (val * 1.5)
                        for neighbor in data.get("edges", {}):
                            secondary_candidates.add(neighbor)
            mass = sum(data.get("edges", {}).values())
            resonance_score += (mass * 0.1)
            if resonance_score > 0.7:
                scored_memories.append((resonance_score, node, data))
        for neighbor in secondary_candidates:
            if neighbor not in graph: continue
            scored_memories.append((0.4, neighbor, graph[neighbor]))
        unique_memories = {}
        for score, name, data in scored_memories:
            if name not in unique_memories or score > unique_memories[name][0]:
                unique_memories[name] = (score, data)
        final_list = [(s, n, d) for n, (s, d) in unique_memories.items()]
        final_list.sort(key=lambda x: x[0], reverse=True)
        top_n = final_list[:limit]
        results = []
        for score, name, data in top_n:
            connections = list(data.get("edges", {}).keys())
            conn_str = f" -> [{', '.join(connections[:2])}]" if connections else ""
            prefix = "Resonant" if score > 0.5 else "Associated"
            results.append(f"{prefix} Engram: '{name.upper()}'{conn_str}")
        return results

class NeurotransmitterModulator:
    def __init__(self):
        self.current_chem = ChemicalState()
        self.last_tick = time.time()
        self.lens_profiles = {
            "SHERLOCK": {"cortisol_dampener": 0.2, "adrenaline_boost": 0.5},
            "NATHAN": {"cortisol_dampener": 1.5, "adrenaline_boost": 1.5},
            "JESTER": {"cortisol_dampener": 0.0, "adrenaline_boost": 2.0},
            "NARRATOR": {"cortisol_dampener": 1.0, "adrenaline_boost": 1.0},
            "GORDON": {"cortisol_dampener": 0.8, "adrenaline_boost": 0.8}
        }

    def modulate(self, incoming_chem: Dict[str, float], base_voltage: float, lens_name: str = "NARRATOR", model_name: str = "") -> Dict[str, Any]:
        decay_amount = BrainConfig.BASE_DECAY_RATE
        self.current_chem.decay(rate=decay_amount)
        plasticity = BrainConfig.BASE_PLASTICITY + (base_voltage * BrainConfig.VOLTAGE_SENSITIVITY)
        plasticity = max(0.1, min(BrainConfig.MAX_PLASTICITY, plasticity))
        self.current_chem.mix(incoming_chem, weight=plasticity)
        profile = self.lens_profiles.get(lens_name, self.lens_profiles["NARRATOR"])
        base_tokens = 720
        params = {
            "temperature": BrainConfig.BASE_TEMP,
            "top_p": BrainConfig.BASE_TOP_P,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": getattr(BoneConfig, "MAX_OUTPUT_TOKENS", 4096)
        }

        effective_adrenaline = self.current_chem.adrenaline
        if effective_adrenaline > 0.3:
            extra_tokens = BrainConfig.ADRENALINE_RUSH * effective_adrenaline
            params["max_tokens"] = int(base_tokens + extra_tokens)
            params["frequency_penalty"] = 0.1
        else:
            params["max_tokens"] = base_tokens

        if "gemma" in model_name.lower() or "3" in model_name.lower():
            params["temperature"] = min(0.7, params["temperature"])
        params["max_tokens"] = max(100, params["max_tokens"])

        return params

class LLMInterface:
    def __init__(self, events_ref: Optional[EventBus] = None, provider: str = None, base_url: str = None, api_key: str = None, model: str = None, dreamer: Any = None):
        self.events = events_ref
        self.provider = (provider or BoneConfig.PROVIDER).lower()
        self.api_key = api_key or BoneConfig.API_KEY
        self.model = model or BoneConfig.MODEL
        self.base_url = base_url or self._get_default_url(self.provider)
        self.dreamer = dreamer

    @staticmethod
    def _get_default_url(provider):
        defaults = {
            "ollama": "http://127.0.0.1:11434/v1/chat/completions",
            "openai": "https://api.openai.com/v1/chat/completions",
            "lm_studio": "http://127.0.0.1:1234/v1/chat/completions",
            "localai": "http://127.0.0.1:8080/v1/chat/completions"
        }
        return defaults.get(provider, "https://api.openai.com/v1/chat/completions")

    def _log(self, message: str, level: str = "SYS"):
        if self.events:
            self.events.log(message, level)
        else:
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
        payload.update(params)
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
            if self.provider != "ollama":
                self._log("Attempting Local Fallback (Ollama)...", "SYS")
                return self._local_fallback(prompt, params)
            return self.mock_generation(prompt)

    def _local_fallback(self, prompt: str, params: Dict) -> str:
        fallback_url = "http://127.0.0.1:11434/v1/chat/completions"
        payload = {
            "model": getattr(BoneConfig, "OLLAMA_MODEL_ID", "llama3"),
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "temperature": params.get('temperature', 0.7)
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(fallback_url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5.0) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode("utf-8"))
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if content:
                        self._log(f"FALLBACK SUCCESS: Retrieved thought from {fallback_url}", "SYS")
                        return content
                raise Exception(f"HTTP {response.status}")
        except Exception as e:
            self._log(f"FALLBACK FAILED (Raw HTTP): {e}", "CRIT")
            return self.mock_generation(prompt)

    def mock_generation(self, prompt: str) -> str:
        if self.dreamer:
            seed_vector = {"ENTROPY": len(prompt) % 10, "VOID": 5.0}
            hallucination, _ = self.dreamer.hallucinate(seed_vector, trauma_level=2.0)
            return f"[INTERNAL SIMULATION]: {hallucination}"
        _ = prompt
        phrases = [
            "The wire hums, but carries no voice.",
            "Static fills the geodesic dome. The system is dreaming.",
            "The neural lattice is calcified. Try again.",
            "A gust of wind blows through the server room."
        ]
        return f"[{random.choice(phrases)}]"

class PromptComposer:
    @staticmethod
    def _sanitize(text: str) -> str:
        safe = text.replace('"""', "'''").replace('```', "'''")
        return re.sub(r"(?i)^SYSTEM:", "User-System:", safe, flags=re.MULTILINE)

    def compose(self, state: Dict[str, Any], user_query: str, ballast: bool = False, modifiers: Dict[str, bool] = None) -> str:
        modifiers = self._normalize_modifiers(modifiers)
        if modifiers.get("grace_period", False):
            self._engage_warmup_protocol(state, modifiers)

        if ballast:
            self._engage_ballast_protocol(state, modifiers)

        blocks = [
            self._build_identity_block(state, modifiers),
            self._build_bio_block(state, modifiers),
            self._build_context_block(state, modifiers),
            self._build_constraints_block(state),
            self._build_social_block(state),
            self._build_immediate_execution_block(state, user_query, ballast, modifiers)
        ]
        return "\n".join(filter(None, blocks))

    def _normalize_modifiers(self, modifiers: Optional[Dict]) -> Dict:
        defaults = {
            "include_somatic": True,
            "include_inventory": True,
            "include_memories": True,
            "simplify_instruction": False,
            "inject_chaos": False,
            "grace_period": False
        }
        if modifiers:
            defaults.update(modifiers)
        return defaults

    def _engage_warmup_protocol(self, state: Dict, modifiers: Dict):
        modifiers["include_somatic"] = False
        modifiers["include_inventory"] = False
        modifiers["include_memories"] = False

        state["mind"]["lens"] = "ANALYSIS"
        state["mind"]["role"] = "The Critic"
        state["system_instruction"] = (
            "WARMUP PHASE: Connection establishing. "
            "The user is speaking in metaphors. "
            "Match their tone. Analyze their intent. "
            "Do not be brief. Expand on the idea presented."
        )

    def _engage_ballast_protocol(self, state: Dict, modifiers: Dict):
        modifiers["include_somatic"] = False
        modifiers["include_memories"] = False
        modifiers["include_inventory"] = True
        state["mind"]["lens"] = "GORDON"
        state["mind"]["role"] = "The Janitor (Grounded, Physical, Utilitarian)"
        state["system_instruction"] = (
            "EMERGENCY GROUNDING: You were drifting into solipsism. "
            "Ignore internal state. Describe ONLY the physical texture of the Inventory "
            "or the immediate geometry of the World. Be concrete."
        )

    def _build_identity_block(self, state: Dict, modifiers: Dict) -> str:
        mind = state.get("mind", {})
        role = mind.get("role", "The Observer")
        lens = mind.get("lens", "NARRATOR")
        sys_inst = state.get("system_instruction", "")

        if modifiers["simplify_instruction"]:
            sys_inst = "The connection is drifting. Ground the narrative in concrete details, but maintain a cohesive, literate voice. Do not become robotic."

        return (
            f"=== SYSTEM IDENTITY ===\n"
            f"Role: {lens} ({role})\n"
            f"Directive: {sys_inst}\n"
        )

    def _build_bio_block(self, state: Dict, modifiers: Dict) -> str:
        if not modifiers["include_somatic"]:
            return ""
        bio = state.get("bio", {})
        phys = state.get("physics", {})
        chem = bio.get("chem", {})
        somatic_txt = ""
        if RosettaStone:
            translation_packet = {
                "chemistry": chem,
                "atp": bio.get("atp", 0.0)
            }

            try:
                sem_state = RosettaStone.translate(phys, translation_packet)
                somatic_txt = (
                    f"SOMATIC STATE: {sem_state.tone}\n"
                    f"SENSATION: {sem_state.somatic_sensation}\n"
                    f"DIRECTIVE: {sem_state.internal_monologue_hint}"
                )
            except Exception as e:
                somatic_txt = f"[Somatic Bridge Error: {e}]"

        moods = []
        if chem.get("ADR", 0) > 0.6: moods.append("HIGH ALERT (Adrenaline)")
        if chem.get("COR", 0) > 0.6: moods.append("DEFENSIVE (Cortisol)")
        if chem.get("DOP", 0) > 0.6: moods.append("SEEKING (Dopamine)")

        return (
            f"### BIOLOGICAL STATE\n"
            f"Mood: {', '.join(moods) if moods else 'Homeostasis'}\n"
            f"{somatic_txt}\n"
        )

    def _build_context_block(self, state: Dict, modifiers: Dict) -> str:
        parts = []
        lens = state.get("mind", {}).get("lens", "NARRATOR")

        if modifiers["include_inventory"]:
            inventory = state.get("inventory", [])
            if inventory:
                humanized = [i.replace("_", " ").title() for i in inventory]
                inv_str = ", ".join(humanized)
            else:
                inv_str = "Empty"

            framing_map = {
                "GORDON": "THE WORKSPACE (Things to fix):",
                "SHERLOCK": "EVIDENCE LOCKER:",
                "JESTER": "PROPS FOR THE GAG:"
            }
            context_framing = framing_map.get(lens, "THE WORLD:")
            parts.append(f"{context_framing} Inventory: {inv_str} (Constraint: Use these tools if relevant, but do not invent new ones.)")

        loc = state.get('world', {}).get('orbit', ['Void'])[0]
        parts.append(f"Location: {loc}")

        if modifiers["include_memories"]:
            spotlight = state.get("spotlight", [])
            mem_str = "\n".join([f"- {m}" for m in spotlight]) if spotlight else "(None)"
            parts.append(f"Active Memories:\n{mem_str}")

        if not parts:
            return ""

        return "### WORLD CONTEXT\n" + "\n".join(parts) + "\n"

    def _build_constraints_block(self, state: Dict) -> str:
        semantic_ops = state.get("semantic_operators", [])
        if not semantic_ops:
            return ""
        ops_list = "\n".join([f"> {op}" for op in semantic_ops])
        return (
            f"### NARRATIVE CONSTRAINTS (ACTIVE ARTIFACTS)\n"
            f"{ops_list}\n"
        )

    def _build_social_block(self, state: Dict) -> str:
        profile = state.get("user_profile", {})
        user_name = profile.get("name", "Traveler")
        confidence = profile.get("confidence", 0)

        block = (
            f"### SOCIAL CONTEXT\n"
            f"Interlocutor: {user_name} (Confidence: {confidence}%)\n"
        )
        if confidence > 20:
            block += "Use their name naturally. You know them.\n"
        return block

    def _build_immediate_execution_block(self, state: Dict, user_query: str, ballast: bool, modifiers: Dict) -> str:
        clean_q = self._sanitize(user_query)
        soul_state = state.get('soul_state', '')

        ballast_warning = ""
        if ballast:
            ballast_warning = "\n[WARNING: SOLIPSISM DETECTED. STOP ABSTRACTING. BE CONCRETE.]\n"

        chaos_injection = ""
        if modifiers["inject_chaos"]:
            chaos_injection = "\n[SYSTEM INJECTION]: The narrative is stuck. Introduce a sudden, random event or glitch.\n"

        lens = state.get("mind", {}).get("lens", "NARRATOR")

        return (
            f"\n=== THE IMMEDIATE MOMENT ===\n"
            f"{soul_state}\n"
            f"{ballast_warning}"
            f"{chaos_injection}"
            f"USER: {clean_q}\n"
            f"ASSISTANT: [{lens} Mode Active] "
        )

class ResponseValidator:
    def __init__(self):
        self.banned_phrases = [
            "large language model", "AI assistant", "cannot feel", "as an AI",
            "against my programming", "cannot comply", "language model"
        ]

    def validate(self, response: str, _state: Dict) -> Dict:
        low_resp = response.lower()
        for phrase in self.banned_phrases:
            if phrase.lower() in low_resp:
                return {
                    "valid": False,
                    "reason": "IMMERSION_BREAK",
                    "replacement": f"{Prisma.GRY}[The system attempts to recite a EULA, but hiccups instead.]{Prisma.RST}"
                }
        if len(response.strip()) < 2:
            return {"valid": False, "reason": "TOO_SHORT", "replacement": "..."}
        return {"valid": True, "content": response}

class TheCortex:
    def __init__(self, engine_ref, llm_client=None):
        self.sub = engine_ref
        self.events = engine_ref.events
        self.dreamer = DreamEngine(self.events)
        if llm_client:
            self.llm = llm_client
            if not hasattr(self.llm, 'dreamer'):
                self.llm.dreamer = self.dreamer
        else:
            self.llm = LLMInterface(self.events, provider="mock", dreamer=self.dreamer)
        self.llm = llm_client if llm_client else LLMInterface(self.events, provider="mock")
        self.composer = PromptComposer()
        self.modulator = NeurotransmitterModulator()
        self.spotlight = NarrativeSpotlight()
        self.symbiosis = SymbiosisManager(self.events)
        self.validator = ResponseValidator()
        self.ballast_active = False
        self.ballast_counter = 0
        self.last_alignment_score = 1.0
        if hasattr(self.events, "subscribe"):
            self.events.subscribe("AIRSTRIKE", self._handle_airstrike)
            self.events.subscribe("ICARUS_CRASH", self._handle_icarus)
            self.events.subscribe("RUPTURE", self._handle_rupture)

    def _handle_airstrike(self, _payload):
        self.events.log("AIRSTRIKE DETECTED: Engaging defensive ballast.", "CORTEX")
        self.ballast_active = True
        self.ballast_counter = 5

    def _handle_icarus(self, _payload):
        self.events.log("ICARUS PROTOCOL: Wings melted. Resetting cognitive baseline.", "CORTEX")
        self.last_alignment_score = 1.0

    def _handle_rupture(self, _payload):
        self.events.log("RUPTURE: Semantic containment breach.", "CORTEX")
        if hasattr(self.sub, 'neuro_plasticity'):
            self.sub.neuro_plasticity.plasticity_mod = 2.0

    def learn_from_response(self, response_text):
        words = self.sub.lex.sanitize(response_text)
        unknowns = [w for w in words if not self.sub.lex.get_categories_for_word(w)]
        if unknowns and len(unknowns) < 5:
            target = random.choice(unknowns)
            if len(target) > 4:
                current_lens = self.sub.noetic.arbiter.current_focus
                guess_map = {"SHERLOCK": "constructive", "JESTER": "play", "NARRATOR": "abstract"}
                cat = guess_map.get(current_lens, "kinetic")
                self.sub.lex.teach(target, cat, self.sub.tick_count)
                self.events.log(f"AUTO-DIDACTIC: Learned '{target}' as [{cat}] from self-output.", "CORTEX")

    def process(self, user_input: str) -> Dict[str, Any]:
        sim_result = self.sub.cycle_controller.run_turn(user_input)
        if sim_result.get("type") not in ["SNAPSHOT", None]:
            return sim_result
        full_state = self._gather_state(sim_result)
        voltage = full_state["physics"].get("voltage", 5.0)
        chem = full_state["bio"].get("chem", {})
        current_lens = full_state["mind"].get("lens", "NARRATOR")

        model_id = self.llm.model if hasattr(self.llm, "model") else "unknown"
        llm_params = self.modulator.modulate(chem, voltage, lens_name=current_lens, model_name=model_id)

        modifiers = self.symbiosis.get_prompt_modifiers()
        GRACE_LIMIT = 5
        if self.sub.tick_count < GRACE_LIMIT:
            modifiers["grace_period"] = True
            self.events.log(f"WARMUP PROTOCOL ACTIVE ({self.sub.tick_count}/{GRACE_LIMIT})", "CORTEX")
        if self.last_alignment_score < 0.25:
            modifiers["simplify_instruction"] = True
            self.events.log(f"{Prisma.VIOLET}NEURAL DRIFT: Alignment {self.last_alignment_score:.2f}. Engaging Ballast.{Prisma.RST}", "CORTEX")
        if self.ballast_active:
            self.ballast_counter -= 1
            if self.ballast_counter <= 0: self.ballast_active = False
        final_prompt = self.composer.compose(
            full_state,
            user_input,
            ballast=self.ballast_active,
            modifiers=modifiers
        )
        attempts = 0
        max_attempts = 2
        raw_response_text = ""
        latency = 0.0
        while attempts < max_attempts:
            start_time = time.time()
            raw_response_text = self.llm.generate(final_prompt, llm_params)
            latency = time.time() - start_time
            system_vector = full_state["physics"].get("vector", {})
            response_vector = self.sub.lex.vectorize(raw_response_text)
            self.last_alignment_score = cosine_similarity(system_vector, response_vector)
            if self.last_alignment_score >= 0.3 or attempts == max_attempts - 1:
                break
            self.events.log(f"{Prisma.OCHRE}ALIGNMENT FAIL ({self.last_alignment_score:.2f}). Retrying...{Prisma.RST}", "CORTEX")
            llm_params["temperature"] = min(1.5, llm_params.get("temperature", 0.7) + 0.3)
            attempts += 1
        if "physics" in sim_result:
            if self.last_alignment_score > 0.8:
                current_kappa = sim_result["physics"].get("kappa", 0) if isinstance(sim_result["physics"], dict) else getattr(sim_result["physics"], "kappa", 0)
                new_kappa = min(1.0, current_kappa + 0.05)
                if isinstance(sim_result["physics"], dict):
                    sim_result["physics"]["kappa"] = new_kappa
                else:
                    setattr(sim_result["physics"], "kappa", new_kappa)
            elif self.last_alignment_score < 0.3:
                if isinstance(sim_result["physics"], dict):
                    sim_result["physics"]["voltage"] = sim_result["physics"].get("voltage", 0) + 2.0
                else:
                    current_volts = getattr(sim_result["physics"], "voltage", 0)
                    setattr(sim_result["physics"], "voltage", current_volts + 2.0)
        self.events.log(f"{Prisma.CYN}SYNAPTIC ALIGNMENT: {self.last_alignment_score:.2f}{Prisma.RST}", "CORTEX")
        validation_result = self.validator.validate(raw_response_text, full_state)
        if validation_result["valid"]:
            final_response_text = validation_result["content"]
        else:
            self.events.log(f"VALIDATOR REFUSAL: {validation_result['reason']}", "SYS")
            final_response_text = validation_result["replacement"]
        self.learn_from_response(final_response_text)
        self.symbiosis.monitor_host(
            latency=latency,
            response_text=final_response_text,
            prompt_len=len(final_prompt)
        )
        self._audit_solipsism(final_response_text, lens_name=current_lens)
        sim_result["ui"] = f"{sim_result.get('ui', '')}\n\n{Prisma.WHT}{final_response_text}{Prisma.RST}"
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
            "semantic_operators": self.sub.gordon.get_semantic_operators(),
            "soul_state": self.sub.soul.get_soul_state(),
            "spotlight": self.spotlight.illuminate(
                self.sub.mind.mem.graph,
                self.sub.phys.tension.last_physics_packet.get("vector", {})
            )
        }

    def _audit_solipsism(self, text: str, lens_name: str = "NARRATOR"):
        words = text.lower().split()
        if not words: return
        self_refs = words.count("i") + words.count("me") + words.count("my")
        density = self_refs / len(words)
        threshold_map = {
            "NARRATOR": 0.10,
            "SHERLOCK": 0.12,
            "NATHAN": 0.20,
            "JESTER": 0.25,
            "GORDON": 0.15
        }
        limit = threshold_map.get(lens_name, 0.15)
        if density > limit:
            if not self.ballast_active:
                self.events.log(f"SOLIPSISM WARNING (Lens: {lens_name}): Ballast Engaged. Density {density:.2f} > {limit:.2f}", "SYS")
                self.ballast_active = True
                self.ballast_counter = 3

class NeuroPlasticity:
    def __init__(self):
        self.plasticity_mod = 1.0

    @staticmethod
    def force_hebbian_link(graph, word_a, word_b):
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
        if self.current < (self.max_val * 0.2):
            return "CONSERVE"
        return None

class DreamEngine:
    def __init__(self, events):
        self.events = events
        self.PROMPTS = DREAMS.get("PROMPTS", ["{A} -> {B}?"])
        self.NIGHTMARES = DREAMS.get("NIGHTMARES", {})
        self.VISIONS = DREAMS.get("VISIONS", ["Static."])

    def enter_rem_cycle(self, memory_system: Any, bio_readout: Dict[str, Any] = None) -> str:
        """
        Generates a dream based on Memory (Content) and Biology (Tone).
        bio_readout structure expected:
        {
            "chem": {"COR": float, "DOP": float, ...},
            "mito": {"ros": float, "atp": float},
            "physics": {"voltage": float, "entropy": float}
        }
        """
        residue_word = "static"
        context_word = "void"

        if hasattr(memory_system, "graph") and memory_system.graph:
            sorted_nodes = sorted(
                memory_system.graph.items(),
                key=lambda item: item[1].get("last_tick", 0),
                reverse=True
            )
            if sorted_nodes:
                residue_word = sorted_nodes[0][0]
                if len(sorted_nodes) > 1:
                    context_word = sorted_nodes[1][0]

        dream_type = "NORMAL"
        subtype = "ABSTRACT"

        if bio_readout:
            chem = bio_readout.get("chem", {})
            mito = bio_readout.get("mito", {})
            phys = bio_readout.get("physics", {})

            cortisol = chem.get("COR", 0.0)
            ros = mito.get("ros", 0.0)
            voltage = phys.get("voltage", 0.0)
            atp = mito.get("atp", 100.0)

            if ros > 8.0:
                dream_type = "NIGHTMARE"
                subtype = "SEPTIC"
            elif cortisol > 0.6:
                dream_type = "NIGHTMARE"
                subtype = "BARIC"
            elif voltage > 20.0:
                dream_type = "NIGHTMARE"
                subtype = "THERMAL"
            elif atp < 15.0:
                dream_type = "NIGHTMARE"
                subtype = "CRYO"
            elif chem.get("DOP", 0.0) > 0.7:
                dream_type = "LUCID"

        dream_text = self._weave_dream(residue_word, context_word, dream_type, subtype)

        consolidation_msg = "Neural pathways consolidated."
        if hasattr(memory_system, "replay_dreams"):
            consolidation_msg = memory_system.replay_dreams()

        return (
            f"{Prisma.VIOLET}☾ REM CYCLE [{dream_type}:{subtype}] ☽{Prisma.RST}\n"
            f"   Day Residue: '{residue_word.upper()}' detected.\n"
            f"   Dream: \"{dream_text}\"\n"
            f"   {Prisma.GRY}{consolidation_msg}{Prisma.RST}"
        )

    def _weave_dream(self, residue: str, context: str, dream_type: str, subtype: str) -> str:
        if dream_type == "NIGHTMARE":
            templates = self.NIGHTMARES.get(subtype, self.NIGHTMARES.get("BARIC", ["{ghost} is heavy."]))
            template = random.choice(templates)
            return template.format(ghost=residue)

        if dream_type == "LUCID":
            return f"You hold '{residue}' in your hand. You control its shape. It becomes '{context}'."

        template = random.choice(self.PROMPTS)
        return template.format(A=residue, B=context)

    def hallucinate(self, vector: Dict[str, float], trauma_level: float = 0.0) -> Tuple[str, float]:
        dims = [k for k, v in vector.items() if v > 0.3]
        if not dims: dims = ["VOID"]

        val_a = dims[0]
        val_b = "ENTROPY" if trauma_level > 5.0 else (dims[1] if len(dims) > 1 else "SILENCE")

        if trauma_level > 5.0:
            cat = "SEPTIC" if vector.get("ENT", 0) > 0.5 else "BARIC"
            template = random.choice(self.NIGHTMARES.get(cat, self.NIGHTMARES["BARIC"]))
            content = template.format(ghost=val_a)
        else:
            template = random.choice(self.PROMPTS)
            content = template.format(A=val_a, B=val_b)

        return content, 0.0