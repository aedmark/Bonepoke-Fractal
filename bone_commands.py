# bone_commands.py - CORRECTION PATCH
# Breaking the Ouroboros

import inspect, os, random, shlex, time
from typing import Dict, Callable, List, TYPE_CHECKING
from bone_village import ParadoxSeed

# [CORRECTION: Prevent circular import]
if TYPE_CHECKING:
    from bone_main import BoneAmanita

class CommandProcessor:
    def __init__(self, engine: 'BoneAmanita', prisma_ref, lexicon_ref, config_ref, cartographer_ref):
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
            "/help": self._cmd_help}

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
            trust = self.eng.mind.mirror.profile.confidence
            if trust < 10:
                self._log(f"{self.P.YEL}🔒 LOCKED: Trust {trust}/10 required. Submit Form 27B-6.{self.P.RST}")
                return True
        try:
            return self.registry[cmd](parts)
        except Exception as e:
            self._log(f"{self.P.RED}COMMAND CRASH: {e}{self.P.RST}")
            return True

    def _cmd_manifold(self, parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys:
            self._log("NAVIGATION OFFLINE: No physics data yet.")
        else:
            self._log(self.eng.navigator.report_position(phys))
        return True

    def _cmd_reproduce(self, parts):
        if self.eng.health < 20:
            self._log(f"{self.P.RED}FERTILITY ERROR: Too weak to breed.{self.P.RST}")
            return True
        mode = "MITOSIS"
        target = None
        if len(parts) > 1 and parts[1] == "cross":
            others = [f for f in os.listdir("memories") if f.endswith(".json") and self.eng.mind.mem.session_id not in f]
            if others:
                target = os.path.join("memories", random.choice(others))
                mode = "CROSSOVER"
            else:
                self._log(f"{self.P.YEL}ISOLATION: No partners found. Mitosis fallback.{self.P.RST}")
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

    def _cmd_status(self, parts):
        self._log(f"{self.P.CYN}--- SYSTEM DIAGNOSTICS ---{self.P.RST}")
        self._log(f"Health:  {self.eng.health:.1f} | Stamina: {self.eng.stamina:.1f} | ATP: {self.eng.bio.mito.state.atp_pool:.1f}")
        try:
            enneagram = self.eng.noetic.arbiter.enneagram
            self._log(enneagram.get_psych_report())
        except AttributeError:
            pass
        return True

    def _cmd_save(self, parts):
        self.eng.mind.mirror.profile.save()
        try:
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

    def _cmd_rummage(self, parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys: return True
        success, msg, cost = self.eng.gordon.rummage(phys, self.eng.stamina)
        self.eng.stamina = max(0.0, self.eng.stamina - cost)
        self._log(msg)
        return True

    def _cmd_map(self, parts):
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
        if len(parts) >= 3:
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
        if len(parts) < 2: return True
        text = " ".join(parts[1:])
        self.eng.mind.mem.seeds.append(ParadoxSeed(text, set(self.Lex.clean(text))))
        self._log(f"{self.P.GRN}PLANTED: '{text}'{self.P.RST}")
        return True

    def _cmd_load(self, parts):
        if len(parts) > 1: self.eng.mind.mem.ingest(parts[1] + (".json" if not parts[1].endswith(".json") else ""))
        return True

    def _cmd_kip(self, parts):
        self.Config.VERBOSE_LOGGING = not self.Config.VERBOSE_LOGGING
        self._log(f"VERBOSE LOGGING: {self.Config.VERBOSE_LOGGING}")
        return True

    def _cmd_mode(self, parts):
        if len(parts) > 1: self._log(self.eng.bio.governor.set_override(parts[1].upper()))
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

    def _cmd_weave(self, parts):
        s, m = self.Map.spin_web(self.eng.mind.mem.graph, self.eng.gordon.inventory, self.eng.gordon)
        self._log(m)
        if s: self.eng.stamina -= 5.0
        return True

    def _cmd_voids(self, parts):
        p = self.eng.phys.tension.last_physics_packet
        if p: self._log(f"VOIDS: {self.Map.detect_voids(p) or 'None'}")
        return True

    def _cmd_strata(self, parts):
        wells = [k for k,v in self.eng.mind.mem.graph.items() if "strata" in v]
        self._log(f"STRATA: {wells if wells else 'None'}")
        return True

    def _cmd_fossils(self, parts):
        self._log(f"FOSSILS: {len(self.eng.mind.mem.fossils)} items archived.")
        return True

    def _cmd_lineage(self, parts):
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

    def _cmd_kintsugi(self, parts):
        k = self.eng.kintsugi
        state = "FRACTURED" if k.active_koan else "WHOLE"
        self._log(f"KINTSUGI: {state} | Repairs: {k.repairs_count}")
        return True

    def _cmd_publish(self, parts):
        phys = self.eng.phys.tension.last_physics_packet
        if phys:
            s, r, _ = self.eng.journal.publish(phys["raw_text"], phys, self.eng.bio)
            if s: self._log(f"PUBLISHED: {r}")
        return True

    def _cmd_soul(self, parts):
        soul = self.eng.soul
        self._log(f"{self.P.MAG}--- SOUL DIAGNOSTICS ---{self.P.RST}")
        self._log(f"Traits: {soul.traits}")
        self._log(f"Obsession: {soul.current_obsession} ({soul.obsession_progress*100:.1f}%)")
        if soul.core_memories:
            self._log(f"{self.P.WHT}CORE MEMORIES:{self.P.RST}")
            for i, mem in enumerate(soul.core_memories[-3:]): # Last 3
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

    def _cmd_help(self, parts):
        help_lines = [
            f"\n{self.P.CYN}--- BONEAMANITA 10.4 MANUAL ---{self.P.RST}",
            f"{self.P.GRY}Authorized by the Department of Redundancy Department{self.P.RST}\n"]
        categories = {
            "CORE": ["_cmd_status", "_cmd_save", "_cmd_load", "_cmd_help"],
            "WORLD": ["_cmd_map", "_cmd_manifold", "_cmd_garden", "_cmd_voids"],
            "ACTION": ["_cmd_rummage", "_cmd_reproduce", "_cmd_publish", "_cmd_weave"],
            "DEBUG": ["_cmd_kip", "_cmd_teach", "_cmd_kill", "_cmd_focus"]}

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