# bone_commands.py

import os
import random
import time
from typing import List
from bone_shared import ParadoxSeed

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
            "/load": self._cmd_load,
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
            "/weave": self._cmd_weave,
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

        restricted_cmds = ["/teach", "/kill", "/flag"]
        if cmd in restricted_cmds:
            confidence = self.eng.mind['mirror'].profile.confidence
            if confidence < 10:
                print(f"{self.P.YEL}⚠️ COMMAND LOCKED: Requires 10+ turns of trust (Current: {confidence}).{self.P.RST}")
                return True
                
        try:
            return self.registry[cmd](parts)
        except Exception as e:
            print(f"{self.P.RED}COMMAND FAILURE: {e}{self.P.RST}")
            return True

    def _cmd_weave(self, parts):
        inventory = self.eng.gordon.inventory
        success, msg = self.Map.spin_web(
            self.eng.mind['mem'].graph, 
            inventory, 
            self.eng.gordon
        )
        if success:
            print(f"{self.P.CYN}{msg}{self.P.RST}")
            self.eng.stamina = max(0.0, self.eng.stamina - 5.0) 
            print(f"   {self.P.GRY}(Stamina -5.0){self.P.RST}")
        else:
            print(f"{self.P.RED}{msg}{self.P.RST}")
        return True

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
            print(f"{self.P.GRY}🪨 STRATA: No Gravity Wells formed yet.{self.P.RST}")
        else:
            print(f"{self.P.OCHRE}🪨 GEOLOGICAL STRATA:{self.P.RST}")
            for word, data in wells:
                s = data["strata"]
                age = self.eng.tick_count - s['birth_tick']
                print(f"   {self.P.WHT}● {word.upper()}{self.P.RST} (Age: {age} ticks)")
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
            print(f"{self.P.CYN}📰 PUBLISHED.{self.P.RST} Review: {review}")
            if reward == "SEROTONIN_BOOST":
                self.eng.bio['endo'].serotonin = min(1.0, self.eng.bio['endo'].serotonin + 0.2)
                print(f"   {self.P.GRN}► STATUS UP: Serotonin +0.2{self.P.RST}")
        return True

    def _cmd_teach(self, parts):
        if len(parts) >= 3:
            word = parts[1]
            cat = parts[2].lower()
            self.Lex.teach(word, cat, self.eng.tick_count)
            print(f"{self.P.CYN}🧠 NEUROPLASTICITY: Learned '{word}' is {cat.upper()}.{self.P.RST}")
        return True

    def _cmd_garden(self, parts):
        seeds = self.eng.mind['mem'].seeds
        print(f"{self.P.GRN}🌿 THE PARADOX GARDEN:{self.P.RST}")
        if len(parts) > 1 and parts[1] == "water":
            msg = self.eng.mind['mem'].tend_garden(["concept", "truth", "void"])
            if msg: print(f"   {msg}")
            else: print("   The soil is damp, but nothing blooms yet.")
        else:
            for s in seeds:
                state = "🌺 BLOOMED" if s.bloomed else f"🌱 Germinating ({int(s.maturity*10)}%)"
                print(f"   • {s.question} [{state}]")
        return True

    def _cmd_refusal(self, parts):
        septic = self.eng.trauma_accum.get("SEPTIC", 0.0)
        print(f"{self.P.VIOLET}🛡️ REFUSAL ENGINE: Paranoia Level {septic:.2f}{self.P.RST}")
        return True

    def _cmd_flag(self, parts):
        if len(parts) > 1:
            term = parts[1].lower()
            self.Lex.USER_FLAGGED_BIAS.add(term)
            print(f"{self.P.CYN}🚩 BIAS UPDATE: '{term}' flagged.{self.P.RST}")
        return True

    def _cmd_seed(self, parts):
        if len(parts) < 2:
            print(f"{self.P.YEL}Usage: /seed [The question or paradox to plant]{self.P.RST}")
            return True
        
        text = " ".join(parts[1:])
        triggers = set(self.Lex.clean(text))
        
        if not triggers:
            print(f"{self.P.RED}🌱 SEED ERROR: That idea is too hollow. Use heavier words.{self.P.RST}")
            return True

        new_seed = ParadoxSeed(text, triggers)
        self.eng.mind['mem'].seeds.append(new_seed)
        
        print(f"{self.P.GRN}🌱 GARDEN: Planted new seed.{self.P.RST}")
        print(f"   Question: '{text}'")
        print(f"   {self.P.GRY}Triggers: {triggers}{self.P.RST}")
        return True

    def _cmd_load(self, parts):
        if len(parts) > 1:
            target = parts[1]
            if not target.endswith(".json"):
                target += ".json"
            self.eng.mind['mem'].ingest(target)
        else:
             print(f"{self.P.YEL}Usage: /load [filename]{self.P.RST}")
        return True

    def _cmd_map(self, parts):
        phys = self.eng.phys['tension'].last_physics_packet
        if not phys or "raw_text" not in phys:
            print(f"{self.P.GRY}🌫️ FOG OF WAR: No physics data. Speak to the system first to generate terrain.{self.P.RST}")
            return True
        bio_metrics = {
            "cortisol": self.eng.bio['endo'].cortisol,
            "oxytocin": self.eng.bio['endo'].oxytocin,
            "atp": self.eng.bio['mito'].state.atp_pool
        }
        phys = self.eng.phys['tension'].last_physics_packet
        result_msg, anchors = self.Map.weave(
            self.eng.phys['tension'].last_physics_packet["raw_text"],
            self.eng.mind['mem'].graph,
            bio_metrics,
            self.eng.limbo,
            physics=phys
        )
        print(f"{self.P.OCHRE}🗺️ CARTOGRAPHY REPORT:{self.P.RST}")
        print(result_msg)
        if "ANCHOR_STONE" in self.eng.gordon.inventory:
            print(f"{self.P.GRY}   Gordon: 'The anchor holds. We are here.'{self.P.RST}")
        elif len(anchors) < 2:
             print(f"{self.P.GRY}   Gordon: 'This map is useless. I need more rocks.'{self.P.RST}")
        return True

    def _cmd_mirror(self, parts):
        mirror = self.eng.mind['mirror']
        if len(parts) > 1:
            if parts[1].lower() == "off":
                mirror.active_mode = False
                print(f"{self.P.GRY}🪞 MIRROR: Disabled. The system will no longer reflect your biases.{self.P.RST}")
            elif parts[1].lower() == "on":
                mirror.active_mode = True
                print(f"{self.P.MAG}🪞 MIRROR: Enabled. Watching for patterns.{self.P.RST}")
            else:
                 print(f"{self.P.YEL}Usage: /mirror [on/off]{self.P.RST}")
        else:
            state = "ON" if mirror.active_mode else "OFF"
            print(f"{self.P.CYN}🪞 MIRROR STATUS: {state}{self.P.RST}")
            print(mirror.get_status())
        return True

    def _cmd_profile(self, parts):
        print(f"{self.P.GRY}Profile update stub.{self.P.RST}")
        return True

    def _cmd_focus(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            print(f"{self.P.VIOLET}🧲 FOCUSING: '{target}'...{self.P.RST}")
            tracer = self.eng.mind['tracer']
            loop = tracer.inject(target)
            if loop:
                print(f"  {self.P.RED}↻ RUMINATION:{self.P.RST} {' -> '.join(loop)}")
                if len(parts) > 2 and parts[2] == "break":
                    result = tracer.psilocybin_rewire(loop)
                    if result:
                         print(f"  {self.P.GRN}{result}{self.P.RST}")
                else:
                    print(f"  {self.P.GRY}To rewire this loop, use: /focus {target} break{self.P.RST}")
            else:
                print(f"  {self.P.GRY}No pathological loops found.{self.P.RST}")
        return True

    def _cmd_status(self, parts):
        BIO = self.eng.bio
        print(f"{self.P.CYN}--- SYSTEM DIAGNOSTICS (9.2.9-PATCHED) ---{self.P.RST}")
        print(f"Health:  {self.eng.health:.1f}/{self.Config.MAX_HEALTH}")
        print(f"Stamina: {self.eng.stamina:.1f}/{self.Config.MAX_STAMINA}")
        print(f"ATP:     {BIO['mito'].state.atp_pool:.1f}")
        return True

    def _cmd_orbit(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            if target in self.eng.mind['mem'].graph:
                self.eng.mind['mem'].graph[target]["edges"]["GRAVITY_ASSIST"] = 50
                print(f"{self.P.VIOLET}🌌 GRAVITY ASSIST: Thrusters firing toward '{target.upper()}'.{self.P.RST}")
            else:
                print(f"{self.P.RED}❌ ERROR: '{target}' not found.{self.P.RST}")
        return True

    def _cmd_prove(self, parts):
        if len(parts) < 2:
            print(f"{self.P.YEL}Usage: /prove [statement]{self.P.RST}")
        else:
            statement = " ".join(parts[1:])
            m = self.eng.phys['tension'].gaze(statement)
            truth = m["physics"]["truth_ratio"]
            print(f"{self.P.CYN}📐 LOGIC PROBE: Density={truth:.2f}{self.P.RST}")
        return True

    def _cmd_kip(self, parts):
        self.Config.VERBOSE_LOGGING = not self.Config.VERBOSE_LOGGING
        state = "ON" if self.Config.VERBOSE_LOGGING else "OFF"
        print(f"{self.P.GRY}📝 VERBOSE LOGGING: {state}{self.P.RST}")
        return True

    def _cmd_pp(self, parts):
        packet = self.eng.phys['tension'].last_physics_packet
        if packet:
            print(f"{self.P.CYN}📐 PHYSICS DUMP:{self.P.RST} V:{packet.get('voltage',0)} D:{packet.get('narrative_drag',0)}")
        return True

    def _cmd_tfw(self, parts):
        phys = self.eng.phys['tension'].last_physics_packet
        if phys:
            old_drag = phys.get("narrative_drag", 0.0)
            phys["narrative_drag"] = max(0.0, old_drag - 2.0)
            phys["beta_index"] = random.uniform(0.1, 2.0)
            
            print(f"{self.P.MAG}🔄 PATH DIVERSIFICATION EXECUTED:{self.P.RST}")
            print(f"   Gravity Wells ignored. Vector shifted 30°.")
            print(f"   {self.P.GRY}Drag reduced by 2.0. Beta randomized.{self.P.RST}")
        else:
            print(f"{self.P.RED}Cannot shift vector: No physics packet active.{self.P.RST}")
        return True

    def _cmd_help(self, parts):
        print(f"{self.P.WHT}--- COMMANDS (PATCHED) ---{self.P.RST}")
        cmds = list(self.registry.keys())
        print(", ".join(cmds))
        return True