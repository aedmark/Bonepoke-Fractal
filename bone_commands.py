""" bone_commands.py
 'The snake spits out its tail. The circle becomes a line.' """

import inspect, os, random, shlex
from typing import Dict, Callable, List, Any, Protocol, runtime_checkable

@runtime_checkable
class EngineProtocol(Protocol):
    events: Any
    mind: Any
    phys: Any
    bio: Any
    soul: Any
    limbo: Any
    navigator: Any
    gordon: Any
    kintsugi: Any
    tinkerer: Any
    journal: Any
    repro: Any
    noetic: Any
    health: float
    stamina: float
    tick_count: int
    trauma_accum: Dict[str, float]
    user_name: str

    def trigger_death(self, last_phys) -> Dict: ...

    def get_metrics(self, atp=0.0) -> Dict: ...

class CommandProcessor:
    def __init__(self, engine: EngineProtocol, prisma_ref, lexicon_ref, config_ref, cartographer_ref):
        self.eng = engine
        self.P = prisma_ref
        self.Lex = lexicon_ref
        self.Config = config_ref
        self.Map = cartographer_ref
        self.registry: Dict[str, Callable[[List[str]], bool]] = {
            "/save": self._cmd_save,
            "/load": self._cmd_load,
            "/kip": self._cmd_kip,
            "/mode": self._cmd_mode,
            "/status": self._cmd_status,
            "/map": self._cmd_map,
            "/manifold": self._cmd_manifold,
            "/garden": self._cmd_garden,
            "/voids": self._cmd_voids,
            "/strata": self._cmd_strata,
            "/fossils": self._cmd_fossils,
            "/lineage": self._cmd_lineage,
            "/rummage": self._cmd_rummage,
            "/seed": self._cmd_seed,
            "/reproduce": self._cmd_reproduce,
            "/weave": self._cmd_weave,
            "/publish": self._cmd_publish,
            "/teach": self._cmd_teach,
            "/kill": self._cmd_kill,
            "/flag": self._cmd_flag,
            "/focus": self._cmd_focus,
            "/orbit": self._cmd_orbit,
            "/mirror": self._cmd_mirror,
            "/kintsugi": self._cmd_kintsugi,
            "/prove": self._cmd_prove,
            "/soul": self._cmd_soul,
            "/chapter": self._cmd_chapter,
            "/help": self._cmd_help,
            "/synapse": self._cmd_synapse
        }

    def _log(self, text):
        self.eng.events.log(text, "CMD")

    def execute(self, text: str) -> bool:
        if not text.startswith("/"): return False
        try:
            parts = shlex.split(text)
        except ValueError:
            self._log(f"{self.P.RED}SYNTAX ERROR: Unbalanced quotes. The Bureau rejects your form.{self.P.RST}")
            return True
        cmd = parts[0].lower()
        if cmd not in self.registry:
            self._log(f"{self.P.RED}Unknown command '{cmd}'. Try /help for the manifesto.{self.P.RST}")
            return True
        if cmd in ["/teach", "/kill", "/flag"] and not self.Config.VERBOSE_LOGGING:
            try:
                trust = self.eng.mind.mirror.profile.confidence
                if trust < 10:
                    self._log(f"{self.P.YEL}🔒 LOCKED: Trust {trust}/10 required. Submit Form 27B-6.{self.P.RST}")
                    return True
            except AttributeError:
                pass
        try:
            return self.registry[cmd](parts)
        except Exception as e:
            self._log(f"{self.P.RED}COMMAND CRASH: {e}{self.P.RST}")
            import traceback
            traceback.print_exc()
            return True

    def _cmd_manifold(self, _parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys:
            self._log("NAVIGATION OFFLINE: No physics data yet.")
        else:
            self._log(self.eng.navigator.report_position(phys))
        return True

    def _cmd_reproduce(self, parts):
        if not self._levy_tax("MITOSIS",
                              costs={"atp": 50.0, "stamina": 30.0},
                              checks={"health": 80.0}):
            return True
        mode = "MITOSIS"
        target = None

        if len(parts) > 1 and parts[1] == "cross":
            try:
                if not os.path.exists("memories"): os.makedirs("memories")
                others = [f for f in os.listdir("memories") if f.endswith(".json") and self.eng.mind.mem.session_id not in f]
                if others:
                    target = os.path.join("memories", random.choice(others))
                    mode = "CROSSOVER"
                else:
                    self._log(f"{self.P.YEL}ISOLATION: No partners found. Mitosis fallback.{self.P.RST}")
            except OSError:
                pass
        self._log(f"{self.P.MAG}INITIATING {mode}...{self.P.RST}")
        log_text, child_mutations = self.eng.repro.attempt_reproduction(self.eng, mode, target)
        self._log(log_text)
        if child_mutations:
            self._log(f"{self.P.CYN}↺ CIRCULATION: The parent learns from the child.{self.P.RST}")
            for key, val in child_mutations.items():
                if hasattr(self.Config, key):
                    old_val = getattr(self.Config, key)
                    new_val = (old_val + val) / 2
                    setattr(self.Config, key, new_val)
                    self._log(f"   [MUTATION ADOPTED]: {key} {old_val:.2f} -> {new_val:.2f}")
        return True

    def _cmd_status(self, _parts):
        self._log(f"{self.P.CYN}--- SYSTEM DIAGNOSTICS ---{self.P.RST}")
        self._log(f"Health:  {self.eng.health:.1f} | Stamina: {self.eng.stamina:.1f} | ATP: {self.eng.bio.mito.state.atp_pool:.1f}")
        return True

    def _cmd_save(self, _parts):
        try:
            self.eng.mind.mirror.profile.save()
            path = self.eng.mind.mem.save(
                health=self.eng.health,
                stamina=self.eng.stamina,
                mutations={},
                trauma_accum=self.eng.trauma_accum,
                joy_history=[],
                mitochondria_traits=self.eng.bio.mito.adapt(self.eng.health),
                antibodies=list(self.eng.bio.immune.active_antibodies),
                soul_data=self.eng.soul.to_dict()
            )
            self._log(f"{self.P.GRN}💾 SYSTEM SAVED: {path}{self.P.RST}")
        except Exception as e:
            self._log(f"{self.P.RED}SAVE FAILED: {e}{self.P.RST}")
        return True

    def _cmd_rummage(self, _parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys: return True
        success, msg, cost = self.eng.gordon.rummage(phys, self.eng.stamina)
        self.eng.stamina = max(0.0, self.eng.stamina - cost)
        self._log(msg)
        return True

    def _cmd_map(self, _parts):
        if not self._levy_tax("CARTOGRAPHY", costs={"atp": 5.0, "stamina": 2.0}):
            return True
        phys = self.eng.phys.tension.last_physics_packet
        if not phys or "raw_text" not in phys: return True
        bio = {"cortisol": self.eng.bio.endo.cortisol, "oxytocin": self.eng.bio.endo.oxytocin}
        result, anchors = self.Map.weave(phys["raw_text"], self.eng.mind.mem.graph, bio, self.eng.limbo, physics=phys)
        self._log(f"{self.P.OCHRE}CARTOGRAPHY REPORT:{self.P.RST}\n{result}")
        if anchors: self._log(f"LANDMARKS: {', '.join(anchors)}")
        return True

    def _cmd_garden(self, parts):
        self._log(f"{self.P.GRN}THE PARADOX GARDEN:{self.P.RST}")

        if len(parts) > 1 and parts[1] == "water":
            msg = self.eng.mind.mem.tend_garden(["concept", "truth"])
            self._log(f"   {msg}" if msg else "   The soil is damp.")
        else:
            for s in self.eng.mind.mem.seeds:
                state = "BLOOMED" if s.bloomed else f"Germinating ({int(s.maturity*10)}%)"
                self._log(f"   {s.question} [{state}]")
        return True

    def _cmd_teach(self, parts):
        if len(parts) < 3: return True
        if not self._levy_tax("NEUROPLASTICITY",
                              costs={"atp": 10.0},
                              checks={"trust": 15.0}):
            return True
        self.Lex.teach(parts[1], parts[2].lower(), self.eng.tick_count)
        self._log(f"{self.P.CYN}NEUROPLASTICITY: '{parts[1]}' -> [{parts[2].upper()}].{self.P.RST}")
        return True

    def _cmd_kill(self, parts):
        if len(parts) >= 2:
            self.Lex.learn_antigen(parts[1], parts[2] if len(parts)>2 else "")
            self._log(f"{self.P.RED}IMMUNE UPDATE: '{parts[1]}' flagged.{self.P.RST}")
        return True

    def _cmd_flag(self, parts):
        if len(parts) > 1:
            self.Lex.USER_FLAGGED_BIAS.add(parts[1].lower())
            self._log(f"{self.P.CYN}BIAS FLAGGED: {parts[1]}{self.P.RST}")
        return True

    def _cmd_seed(self, parts):
        from bone_village import ParadoxSeed
        if len(parts) < 2: return True
        text = " ".join(parts[1:])
        self.eng.mind.mem.seeds.append(ParadoxSeed(text, set(self.Lex.clean(text))))
        self._log(f"{self.P.GRN}PLANTED: '{text}'{self.P.RST}")
        return True

    def _cmd_load(self, parts):
        if len(parts) > 1: self.eng.mind.mem.ingest(parts[1] + (".json" if not parts[1].endswith(".json") else ""))
        return True

    def _cmd_kip(self, _parts):
        going_to_sleep = self.Config.VERBOSE_LOGGING
        if going_to_sleep:
            self._log(f"{self.P.CYN}Closing eyes (Saving & Dreaming)...{self.P.RST}")
            try:
                self.eng.mind.mem.save(
                    health=self.eng.health,
                    stamina=self.eng.stamina,
                    mutations={},
                    trauma_accum=self.eng.trauma_accum,
                    joy_history=[],
                    mitochondria_traits=self.eng.bio.mito.adapt(self.eng.health),
                    antibodies=list(self.eng.bio.immune.active_antibodies),
                    soul_data=self.eng.soul.to_dict()
                )
            except Exception as e:
                self._log(f"{self.P.RED}Auto-Save Failed: {e}{self.P.RST}")

            if hasattr(self.eng.mind, "dreamer") and hasattr(self.eng.mind, "mem"):
                bio_packet = {
                    "chem": self.eng.bio.endo.get_state(),
                    "mito": {
                        "ros": self.eng.bio.mito.state.ros_buildup,
                        "atp": self.eng.bio.mito.state.atp_pool
                    },
                    "physics": self.eng.phys.tension.last_physics_packet
                }
                dream_log = self.eng.mind.dreamer.enter_rem_cycle(self.eng.mind.mem, bio_readout=bio_packet)
                self._log(dream_log)

        self.Config.VERBOSE_LOGGING = not self.Config.VERBOSE_LOGGING
        state = "OPEN" if self.Config.VERBOSE_LOGGING else "SHUT"
        self._log(f"EYELIDS: {state}")
        return True

    def _cmd_mode(self, parts):
        if len(parts) < 2: return True
        if not self._levy_tax("GOVERNOR_OVERRIDE", costs={"stamina": 25.0}):
            return True
        target_mode = parts[1].upper()
        result_msg = self.eng.bio.governor.set_override(target_mode)
        self._log(result_msg)
        if "INVALID" in result_msg:
            self._log(f"{self.P.GRY}(Stamina wasted filling out the wrong form. Good job.){self.P.RST}")
        return True

    def _cmd_focus(self, parts):
        if len(parts) > 1:
            loop = self.eng.mind.tracer.inject(parts[1].lower())
            if loop:
                self._log(f"{self.P.RED}RUMINATION:{self.P.RST} {'->'.join(loop)}")
                if len(parts) > 2 and parts[2] == "break":
                    self._log(self.eng.mind.tracer.psilocybin_rewire(loop))
            else: self._log("No loop found.")
        return True

    def _cmd_orbit(self, parts):
        if len(parts) > 1 and parts[1] in self.eng.mind.mem.graph:
            self.eng.mind.mem.graph[parts[1]]["edges"]["GRAVITY_ASSIST"] = 50
            self._log(f"{self.P.VIOLET}GRAVITY ASSIST: Target '{parts[1]}'.{self.P.RST}")
        return True

    def _cmd_weave(self, _parts):
        s, m = self.Map.spin_web(self.eng.mind.mem.graph, self.eng.gordon.inventory, self.eng.gordon)
        self._log(m)
        if s: self.eng.stamina -= 5.0
        return True

    def _cmd_voids(self, _parts):
        p = self.eng.phys.tension.last_physics_packet
        if p: self._log(f"VOIDS: {self.Map.detect_voids(p) or 'None'}")
        return True

    def _cmd_strata(self, _parts):
        wells = [k for k,v in self.eng.mind.mem.graph.items() if "strata" in v]
        self._log(f"STRATA: {wells if wells else 'None'}")
        return True

    def _cmd_fossils(self, _parts):
        self._log(f"FOSSILS: {len(self.eng.mind.mem.fossils)} items archived.")
        return True

    def _cmd_lineage(self, _parts):
        self._log(f"LINEAGE: {len(self.eng.mind.mem.lineage_log)} generations.")
        return True

    def _cmd_mirror(self, parts):
        m = self.eng.mind.mirror
        if len(parts) > 1: m.active_mode = (parts[1].lower() == "on")
        self._log(f"MIRROR: {'ON' if m.active_mode else 'OFF'} | {m.get_status()}")
        return True

    def _cmd_prove(self, parts):
        if len(parts) > 1:
            m = self.eng.phys.tension.gaze(" ".join(parts[1:]))
            self._log(f"LOGIC DENSITY: {m['physics']['truth_ratio']:.2f}")
        return True

    def _cmd_kintsugi(self, _parts):
        k = self.eng.kintsugi
        state = "FRACTURED" if k.active_koan else "WHOLE"
        self._log(f"KINTSUGI: {state} | Repairs: {k.repairs_count}")
        return True

    def _cmd_publish(self, _parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys:
            self._log(f"{self.P.RED}CANNOT PUBLISH: No physics data generated yet.{self.P.RST}")
            return True
        result = self.eng.journal.publish(phys["raw_text"], phys, self.eng.bio)
        self._log(f"{self.P.OCHRE}--- LITERARY REVIEW ---{self.P.RST}")
        self._log(f"Critic: {self.P.WHT}{result.critic_name}{self.P.RST}")
        self._log(f"Score:  {self.P.CYN}{result.score:.1f}/100{self.P.RST}")
        self._log(f"Review: {self.P.GRY}\"{result.verdict}\"{self.P.RST}")
        if self.Config.VERBOSE_LOGGING:
            self._log(f"{self.P.GRY}   [Scoring Logic]: {', '.join(result.breakdown)}{self.P.RST}")
        if result.reward_type == "ATP_BOOST":
            current_atp = self.eng.bio.mito.state.atp_pool
            max_atp = getattr(self.Config, "MAX_ATP", 200.0)
            self.eng.bio.mito.state.atp_pool = min(max_atp, current_atp + result.reward_amount)
            self._log(f"{self.P.GRN}   [REWARD]: +{result.reward_amount} ATP (Royalties){self.P.RST}")
            if result.score > 90:
                max_health = getattr(self.Config, "MAX_HEALTH", 100.0)
                self.eng.health = min(max_health, self.eng.health + 5)
                self._log(f"{self.P.GRN}   [CRITICAL ACCLAIM]: +5 Health.{self.P.RST}")
        elif result.reward_type == "STAMINA_REGEN":
            max_stamina = getattr(self.Config, "MAX_STAMINA", 100.0)
            self.eng.stamina = min(max_stamina, self.eng.stamina + result.reward_amount)
            self._log(f"{self.P.GRN}   [REWARD]: +{result.reward_amount} Stamina (Validation){self.P.RST}")
        elif result.reward_type == "CORTISOL_SPIKE":
            self.eng.bio.endo.cortisol = min(1.0, self.eng.bio.endo.cortisol + (result.reward_amount * 0.05))
            self._log(f"{self.P.RED}   [PENALTY]: Rejection hurts. Cortisol rising.{self.P.RST}")
        return True

    def _cmd_soul(self, _parts):
        soul = self.eng.soul
        self._log(f"{self.P.MAG}--- SOUL DIAGNOSTICS ---{self.P.RST}")
        self._log(f"Traits: {soul.traits}")
        self._log(f"Obsession: {soul.current_obsession} ({soul.obsession_progress*100:.1f}%)")
        if soul.core_memories:
            self._log(f"{self.P.WHT}CORE MEMORIES:{self.P.RST}")
            for i, mem in enumerate(soul.core_memories[-3:]):
                self._log(f"  {i+1}. [{mem.emotional_flavor}] '{mem.lesson}' (V:{mem.impact_voltage:.1f})")
        else:
            self._log("No core memories formed yet. The slate is blank.")
        return True

    def _cmd_chapter(self, parts):
        if len(parts) > 1:
            title = " ".join(parts[1:])
            self.eng.soul.chapters.append(title)
            self._log(f"{self.P.CYN}NARRATIVE JUMP: Chapter set to '{title}'.{self.P.RST}")
            self._log(self.eng.soul.editor.critique(title))
        else:
            self._log(f"Current Chapter: {self.eng.soul.chapters[-1] if self.eng.soul.chapters else 'None'}")
        return True

    def _cmd_synapse(self, _parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys:
            self._log("SYNAPSE OFFLINE: No physics data.")
            return True
        sys_vec = phys.get("vector", {})
        self._log(f"{self.P.MAG}--- NEURAL BRIDGE DIAGNOSTICS ---{self.P.RST}")
        self._log(f"System State Vector (The Body):")
        for k, v in sys_vec.items():
            bar = "█" * int(v * 10)
            self._log(f"  {k}: {bar} {v:.2f}")
        cortex = getattr(self.eng, 'cortex', None)
        if cortex:
            score = getattr(cortex, 'last_alignment_score', 0.0)
            color = self.P.GRN if score > 0.7 else (self.P.YEL if score > 0.4 else self.P.RED)
            self._log(f"Last Alignment Score: {color}{score:.3f}{self.P.RST}")
        return True

    def _levy_tax(self, context: str, costs: Dict[str, float], checks: Dict[str, Any] = None) -> bool:
        if checks:
            for metric, threshold in checks.items():
                current_val = 0.0
                if metric == "voltage": current_val = self.eng.phys.tension.last_physics_packet.get("voltage", 0)
                elif metric == "trust": current_val = self.eng.mind.mirror.profile.confidence
                elif metric == "health": current_val = self.eng.health
                if current_val < threshold:
                    self._log(f"{self.P.OCHRE}🛑 DENIED ({context}): {metric.title()} too low ({current_val:.1f} < {threshold}).{self.P.RST}")
                    return False
        stamina_cost = costs.get("stamina", 0.0)
        atp_cost = costs.get("atp", 0.0)
        if self.eng.stamina < stamina_cost:
            self._log(f"{self.P.RED}🛑 EXHAUSTED: This command requires {stamina_cost} Stamina.{self.P.RST}")
            return False
        current_atp = self.eng.bio.mito.state.atp_pool
        if current_atp < atp_cost:
            self._log(f"{self.P.RED}🛑 STARVING: This command requires {atp_cost} ATP (Have: {current_atp:.1f}).{self.P.RST}")
            return False
        if stamina_cost > 0: self.eng.stamina -= stamina_cost
        if atp_cost > 0: self.eng.bio.mito.state.atp_pool -= atp_cost
        return True

    def _cmd_help(self, _parts):
        help_lines = [
            f"\n{self.P.CYN}--- BONEAMANITA 11.2.4 MANUAL ---{self.P.RST}",
            f"{self.P.GRY}Authorized by the Department of Redundancy Department{self.P.RST}\n"
        ]

        metrics = self.eng.get_metrics()
        health = metrics.get("health", 0)
        atp = self.eng.bio.mito.state.atp_pool

        suggestion = ""
        if atp < 20.0:
            suggestion = f"{self.P.RED}CRITICAL ADVICE: You are starving. Try '/rummage' or '/weave' to generate semantic mass.{self.P.RST}"
        elif health < 40.0:
            suggestion = f"{self.P.RED}CRITICAL ADVICE: You are bleeding. Lower Voltage or find 'Constructive' words.{self.P.RST}"
        elif self.eng.phys.pulse.is_bored():
            suggestion = f"{self.P.YEL}ADVICE: The machine is bored. Try '/garden' or '/mode JESTER'.{self.P.RST}"
        else:
            suggestion = f"{self.P.GRN}ADVICE: Systems nominal. Go make art ('/publish').{self.P.RST}"

        help_lines.append(suggestion + "\n")

        categories = {
            "CORE": ["_cmd_status", "_cmd_save", "_cmd_load", "_cmd_help"],
            "WORLD": ["_cmd_map", "_cmd_manifold", "_cmd_garden", "_cmd_voids"],
            "ACTION": ["_cmd_rummage", "_cmd_reproduce", "_cmd_publish", "_cmd_weave"],
            "DEBUG": ["_cmd_kip", "_cmd_teach", "_cmd_kill", "_cmd_focus"]
        }

        def get_doc(func):
            paperwork = inspect.getdoc(func)
            return paperwork if paperwork else "Undocumented protocol."

        for cat, methods in categories.items():
            help_lines.append(f"{self.P.WHT}{cat}:{self.P.RST}")
            for m_name in methods:
                if hasattr(self, m_name):
                    cmd_name = m_name.replace("_cmd_", "/")
                    doc = get_doc(getattr(self, m_name))
                    help_lines.append(f"  {cmd_name:<12} - {doc}")
            help_lines.append("")

        help_lines.append(f"{self.P.GRY}Type carefully. The machine is listening.{self.P.RST}")
        self._log("\n".join(help_lines))
        return True