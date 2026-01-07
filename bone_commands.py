# bone_commands.py

import os
import shutil
import random
import time
from typing import List
from bone_shared import Prisma, BoneConfig, TheLexicon, TheCartographer

class CommandProcessor:
    def __init__(self, engine, prisma_ref, lexicon_ref, config_ref, cartographer_ref):
        self.eng = engine
        self.P = prisma_ref
        self.Lex = lexicon_ref
        self.Config = config_ref
        self.Map = cartographer_ref
        self.registry = {
            "/teach": self._cmd_teach,
            "/kill": self._cmd_kill,
            "/flag": self._cmd_flag,
            "/garden": self._cmd_garden,
            "/lineage": self._cmd_lineage,
            "/voids": self._cmd_voids,
            "/reproduce": self._cmd_reproduce,
            "/mode": self._cmd_mode,
            "/strata": self._cmd_strata,
            "/publish": self._cmd_publish,
            "/refusal": self._cmd_refusal,
            "/seed": self._cmd_seed,
            "/map": self._cmd_map,
            "/mirror": self._cmd_mirror,
            "/profile": self._cmd_profile,
            "/focus": self._cmd_focus,
            "/status": self._cmd_status,
            "/orbit": self._cmd_orbit,
            "/prove": self._cmd_prove,
            "/kip": self._cmd_kip,
            "/pp": self._cmd_pp,
            "/tfw": self._cmd_tfw,
            "/help": self._cmd_help
        }

    def execute(self, text):
        if not text.startswith("/"):
            return False
        parts = text.split()
        cmd = parts[0].lower()
        if cmd not in self.registry:
            print(f"{self.P.RED}Unknown command. Try /help.{self.P.RST}")
            return True
        restricted_cmds = ["/teach", "/kill", "/flag", "/garden"]
        if cmd in restricted_cmds:
            confidence = self.eng.mind['mirror'].profile.confidence
            if confidence < 50:
                print(f"{self.P.YEL}⚠️ COMMAND LOCKED: Requires 50+ turns of trust (Current: {confidence}).{self.P.RST}")
                return True
        try:
            return self.registry[cmd](parts)
        except Exception as e:
            print(f"{self.P.RED}COMMAND FAILURE: {e}{self.P.RST}")
            return True

    # --- COMMAND HANDLERS (The Actual Logic) ---

    def _cmd_lineage(self, parts):
        log = self.eng.mind['mem'].lineage_log
        if not log:
            print(f"{self.P.GRY}📜 ARCHIVE EMPTY: We are the first generation.{self.P.RST}")
            return True
        print(f"{self.P.CYN}📜 THE PALIMPSEST (Ancestral Lineage):{self.P.RST}")
        for entry in log:
            t_vec = ", ".join([f"{k}:{v}" for k,v in entry['trauma'].items()])
            print(f"   {self.P.MAG}• {entry['source']}{self.P.RST} ({entry['age_hours']}h ago)")
            print(f"     ↳ Mutations: {entry['mutations']} | Trauma: {{{t_vec}}}")
        print(f"   {self.P.GRN}• CURRENT SESSION{self.P.RST} (Living)")
        curr_t = ", ".join([f"{k}:{v:.1f}" for k,v in self.eng.trauma_accum.items() if v > 0])
        print(f"     ↳ Ingested: {len(log)} Ancestors | Accumulating: {{{curr_t}}}")
        return True

    def _cmd_voids(self, parts):
        packet = self.eng.phys['tension'].last_physics_packet
        if not packet:
            print(f"{self.P.GRY}🌫️ THE FOG: No physics data yet.{self.P.RST}")
            return True
        voids = self.Map.detect_voids(packet)
        if voids:
            print(f"{self.P.GRY}🌫️ THE FOG: Detected hollow concepts: {voids}{self.P.RST}")
        else:
            print(f"{self.P.CYN}✨ CLEAR AIR: No voids detected.{self.P.RST}")
        return True

    def _cmd_reproduce(self, parts):
        if self.eng.health < 20:
            print(f"{self.P.RED}💔 FERTILITY ERROR: Too weak to breed. Survive first.{self.P.RST}")
            return True
        mode = "MITOSIS"
        target_spore = None
        if len(parts) > 1 and parts[1] == "cross":
            others = [f for f in os.listdir("memories") if f.endswith(".json") and self.eng.mind['mem'].session_id not in f]
            if others:
                target_spore = os.path.join("memories", random.choice(others))
                mode = "CROSSOVER"
            else:
                print(f"{self.P.YEL}⚠️ ISOLATION: No other spores found. Defaulting to Mitosis.{self.P.RST}")
        print(f"{self.P.MAG}🧬 INITIATING {mode}...{self.P.RST}")
        if mode == "MITOSIS":
            phys = self.eng.phys['tension'].last_physics_packet
            bio_state = {"trauma_vector": self.eng.trauma_accum}
            child_id, genome = self.eng.repro.mitosis(
                self.eng.mind['mem'].session_id, 
                bio_state, 
                phys, 
                self.eng.mind['mem'])
            print(f"   ► CHILD SPAWNED: {self.P.WHT}{child_id}{self.P.RST}")
            print(f"   ► TRAIT: {genome['mutations']}")
            
        elif mode == "CROSSOVER":
            current_bio = {
                "trauma_vector": self.eng.trauma_accum,
                "mito": self.eng.bio['mito']
            }
            child_id, genome = self.eng.repro.crossover(
                self.eng.mind['mem'].session_id,
                current_bio,
                target_spore
            )
            if child_id:
                full_spore_data = {
                    "session_id": child_id,
                    "meta": {
                        "timestamp": time.time(),
                        "final_health": self.eng.health,
                        "final_stamina": self.eng.stamina
                    },
                    "trauma_vector": genome.get("trauma_inheritance", {}),
                    "config_mutations": genome.get("config_mutations", {}), 
                    "mitochondria": {"enzymes": list(genome.get("inherited_enzymes", []))},
                    "core_graph": self.eng.mind['mem'].graph, 
                    "antibodies": list(self.eng.bio['immune'].active_antibodies)
                }
                filename = f"{child_id}.json"
                saved_path = self.eng.mind['mem'].loader.save_spore(filename, full_spore_data)
                if saved_path:
                    print(f"   ► HYBRID SPAWNED: {self.P.WHT}{child_id}{self.P.RST}")
                    print(f"   ► LINEAGE: {genome['parent_a']} + {genome['parent_b']}")
                    print(f"   ► {self.P.GRN}SAVED: {saved_path}{self.P.RST}")
            else:
                print(f"{self.P.RED}   ► CROSSOVER FAILED: {genome}{self.P.RST}")
        return True

    def _cmd_mode(self, parts):
        if len(parts) > 1:
            print(self.eng.bio['governor'].set_override(parts[1].upper()))
        else:
            print(f"{self.P.CYN}CURRENT MODE: {self.eng.bio['governor'].mode}{self.P.RST}")
        return True

    def _cmd_strata(self, parts):
        wells = [(k, v) for k, v in self.eng.mind['mem'].graph.items() if "strata" in v]
        if not wells:
            print(f"{self.P.GRY}🪨 STRATA: No Gravity Wells formed yet. The ground is soft.{self.P.RST}")
        else:
            print(f"{self.P.OCHRE}🪨 GEOLOGICAL STRATA (Gravity Wells):{self.P.RST}")
            for word, data in wells:
                s = data["strata"]
                mass = sum(data["edges"].values())
                age = self.eng.tick_count - s['birth_tick']
                growth = s.get('growth_rate', 0.0)
                print(f"   {self.P.WHT}● {word.upper()}{self.P.RST} (Mass: {int(mass)})")
                print(f"     ↳ Birth: Tick {s['birth_tick']} | Age: {age}")
                print(f"     ↳ Growth: {growth:+.2f}/tick")
        return True

    def _cmd_kill(self, parts):
        if len(parts) >= 2:
            toxin = parts[1]
            repl = parts[2] if len(parts) > 2 else ""
            if self.Lex.learn_antigen(toxin, repl):
                print(f"{self.P.RED}🔪 THE SURGEON: Antigen '{toxin}' mapped to '{repl}'.{self.P.RST}")
            else:
                print(f"{self.P.RED}ERROR: Immune system write failure.{self.P.RST}")
        else:
            print(f"{self.P.YEL}Usage: /kill [toxin] [replacement]{self.P.RST}")
        return True

    def _cmd_publish(self, parts):
        journal = self.eng.journal
        phys = self.eng.phys['tension'].last_physics_packet
        if not phys:
            print(f"{self.P.RED}Nothing to publish.{self.P.RST}")
            return True
        success, review, reward = journal.publish(phys["raw_text"], phys, self.eng.bio)
        if success:
            print(f"{self.P.CYN}📰 PUBLISHED TO 'journal_of_the_void.txt'{self.P.RST}")
            print(f"   {self.P.WHT}CRITIC SAYS: {review}{self.P.RST}")
            if reward == "SEROTONIN_BOOST":
                self.eng.bio['endo'].serotonin = min(1.0, self.eng.bio['endo'].serotonin + 0.2)
                print(f"   {self.P.GRN}► STATUS UP: Serotonin +0.2{self.P.RST}")
            elif reward == "CORTISOL_SPIKE":
                self.eng.bio['endo'].cortisol = min(1.0, self.eng.bio['endo'].cortisol + 0.2)
                print(f"   {self.P.RED}► STRESS UP: Cortisol +0.2{self.P.RST}")
        else:
            print(f"{self.P.RED}Publish failed.{self.P.RST}")
        return True

    def _cmd_teach(self, parts):
        if len(parts) >= 3:
            word = parts[1]
            cat = parts[2].lower()
            valid_cats = ["heavy", "kinetic", "abstract", "photo", "aerobic", "thermal", "cryo", "sacred", "cursed", "diversion"]
            if cat in valid_cats:
                self.Lex.teach(word, cat, self.eng.tick_count)
                print(f"{self.P.CYN}🧠 NEUROPLASTICITY: Learned '{word}' is {cat.upper()}.{self.P.RST}")
            else:
                print(f"{self.P.RED}ERROR: Invalid category.{self.P.RST}")
        return True

    def _cmd_garden(self, parts):
        seeds = self.eng.mind['mem'].seeds
        print(f"{self.P.GRN}🌿 THE PARADOX GARDEN ({len(seeds)} seeds buried):{self.P.RST}")
        if len(parts) > 1 and parts[1] == "water":
            msg = self.eng.mind['mem'].tend_garden(["concept", "truth", "void"])
            if msg: print(f"   {msg}")
            else: print("   The soil is damp, but nothing blooms yet.")
        else:
            for s in seeds:
                state = "🌺 BLOOMED" if s.bloomed else f"🌱 Germinating ({int(s.maturity*10)}%)"
                print(f"   • {s.question} [{state}]")
            print(f"   {self.P.GRY}(Type '/garden water' to simulate rainfall){self.P.RST}")
        return True

    def _cmd_refusal(self, parts):
        print(f"{self.P.VIOLET}🛡️ REFUSAL ENGINE DIAGNOSTICS:{self.P.RST}")
        septic = self.eng.trauma_accum.get("SEPTIC", 0.0)
        threshold = 0.3 if septic > 0.5 else 0.8
        print(f"   • Paranoia Level: {septic:.2f} (Threshold: {threshold})")
        if septic > 0.5:
            print(f"   • {self.P.RED}STATUS: HYPER-VIGILANT. Words are dangerous.{self.P.RST}")
        else:
            print(f"   • {self.P.CYN}STATUS: TRUSTING.{self.P.RST}")
        return True

    def _cmd_flag(self, parts):
        if len(parts) > 1:
            term = parts[1].lower()
            self.Lex.USER_FLAGGED_BIAS.add(term)
            print(f"{self.P.CYN}🚩 BIAS UPDATE: '{term}' removed from Suburban Watchlist.{self.P.RST}")
        return True

    def _cmd_seed(self, parts):
        if len(parts) > 1:
            self.eng.mind['mem'].ingest(parts[1])
        else:
            print(f"{self.P.YEL}Usage: /seed [filename]{self.P.RST}")
        return True

    def _cmd_map(self, parts):
        is_spun, msg = self.Map.spin_web(self.eng.mind['mem'].graph, self.eng.gordon.inventory, gordon=self.eng.gordon)
        color = self.P.MAG if is_spun else self.P.OCHRE
        print(f"{color}{msg}{self.P.RST}")
        if "ANCHOR_STONE" in self.eng.gordon.inventory:
            print(f"{self.P.GRY}   Gordon: 'Coordinates are firm. Stop drifting.'{self.P.RST}")
        return True

    def _cmd_mirror(self, parts):
        if len(parts) > 1:
            print(f"{self.P.MAG}Mirror command acknowledged.{self.P.RST}") 
        else:
            print(f"{self.P.YEL}Usage: /mirror [name] OR /mirror off{self.P.RST}")
        return True

    def _cmd_profile(self, parts):
        try:
            name = parts[1]
            likes = []
            for p in parts[2:]:
                if p.startswith("likes:"):
                    likes = [x.strip() for x in p.split(":")[1].split(",")]
            if likes:
                print(f"{self.P.CYN}Profile updated for {name}.{self.P.RST}")
            else:
                print(f"{self.P.RED}ERROR: Must specify 'likes:category'.{self.P.RST}")
        except Exception as e:
            print(f"{self.P.YEL}Usage: /profile [name] likes:heavy,kinetic ({e}){self.P.RST}")
        return True

    def _cmd_focus(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            print(f"{self.P.VIOLET}🧲 MAGNETIC STIMULATION: Targeting '{target}'...{self.P.RST}")
            loop = self.eng.mind['tracer'].inject(target)
            if loop:
                print(f"  {self.P.RED}↻ RUMINATION DETECTED:{self.P.RST} {' -> '.join(loop)}")
                msg = self.eng.mind['tracer'].psilocybin_rewire(loop)
                if msg: print(f"  {self.P.GRN}{msg}{self.P.RST}")
                else: print(f"  {self.P.RED}Rewire failed.{self.P.RST}")
            else:
                print(f"  {self.P.GRY}Trace complete. No pathological abstract loops found.{self.P.RST}")
        else:
            print(f"{self.P.YEL}Usage: /focus [concept]{self.P.RST}")
        return True

    def _cmd_status(self, parts):
        BIO = self.eng.bio
        print(f"{self.P.CYN}--- SYSTEM DIAGNOSTICS (8.9.6) ---{self.P.RST}")
        print(f"Session: {self.eng.mind['mem'].session_id}")
        print(f"Health:  {self.eng.health}/{self.Config.MAX_HEALTH}")
        print(f"Stamina: {self.eng.stamina}/{self.Config.MAX_STAMINA}")
        print(f"ATP:     {BIO['mito'].state.atp_pool:.1f}")
        t_curr = BIO['mito'].state.telomeres
        t_percent = (t_curr / 10000) * 100
        clock_color = self.P.GRN if t_percent > 50 else (self.P.YEL if t_percent > 20 else self.P.RED)
        print(f"Time:    {clock_color}{t_curr}/10000 Ticks{self.P.RST}")
        if 'wise' in self.eng.mind:
             last_phys = self.eng.phys['tension'].last_physics_packet
             if last_phys and "vector" in last_phys: 
                 metrics = {"physics": last_phys}
                 _, _, title = self.eng.mind['wise'].architect(metrics, None, False)
                 print(f"Title:   {self.P.VIOLET}{title}{self.P.RST}")
             else:
                 print(f"Title:   {self.P.GRY}[CALIBRATING]{self.P.RST}")
        return True

    def _cmd_orbit(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            if target in self.eng.mind['mem'].graph:
                self.eng.mind['mem'].graph[target]["edges"]["GRAVITY_ASSIST"] = 50
                print(f"{self.P.VIOLET}🌌 GRAVITY ASSIST: Thrusters firing toward '{target.upper()}'.{self.P.RST}")
            else:
                print(f"{self.P.RED}❌ NAVIGATION ERROR: '{target}' not found in star map.{self.P.RST}")
        else:
            print(f"{self.P.YEL}Usage: /orbit [known_concept]{self.P.RST}")
        return True

    def _cmd_prove(self, parts):
        if len(parts) < 2:
            print(f"{self.P.YEL}Usage: /prove [statement]{self.P.RST}")
        else:
            statement = " ".join(parts[1:])
            m = self.eng.phys['tension'].gaze(statement)
            truth = m["physics"]["truth_ratio"]
            verdict = "AXIOMATIC" if truth > 0.6 else ("CONJECTURE" if truth > 0.3 else "NOISE")
            color = self.P.CYN if truth > 0.6 else self.P.GRY
            print(f"{color}📐 LOGIC PROBE: Density={truth:.2f} [{verdict}]{self.P.RST}")
        return True

    def _cmd_kip(self, parts):
        self.Config.VERBOSE_LOGGING = not self.Config.VERBOSE_LOGGING
        state = "ON" if self.Config.VERBOSE_LOGGING else "OFF"
        print(f"{self.P.GRY}📝 VERBOSE LOGGING: {state}{self.P.RST}")
        return True

    def _cmd_pp(self, parts):
        packet = self.eng.phys['tension'].last_physics_packet
        if packet:
            print(f"{self.P.CYN}📐 PHYSICS PRE-RENDER:{self.P.RST}")
            print(f"   E (Drift):   {packet.get('E_score', 0):.2f}")
            print(f"   B (Cohere):  {packet.get('B_score', 0):.2f}")
            print(f"   β (Index):   {packet.get('beta_index', 0):.2f}")
            print(f"   ⚡ Voltage:  {packet.get('voltage', 0):.1f}v")
        else:
            print(f"{self.P.RED}No physics data active.{self.P.RST}")
        return True

    def _cmd_tfw(self, parts):
        print(f"{self.P.MAG}🔄 PATH DIVERSIFICATION:{self.P.RST}")
        print(f"   Gravity Wells ignored. Vector shifted 30° from Narrative Baseline.")
        return True

    def _cmd_help(self, parts):
        print(f"{self.P.WHT}--- COMMANDS (SLASH OPTIMIZED) ---{self.P.RST}")
        cmds = list(self.registry.keys())
        print(", ".join(cmds))
        return True