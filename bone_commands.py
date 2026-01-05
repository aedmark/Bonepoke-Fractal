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
        self.Prisma = prisma_ref
        self.TheLexicon = lexicon_ref
        self.BoneConfig = config_ref
        self.TheCartographer = cartographer_ref
    def execute(self, text):
        if not text.startswith("/"):
            return False
        parts = text.split()
        cmd = parts[0].lower()
        P = self.Prisma
        BIO = self.eng.bio
        PHYS = self.eng.phys
        MIND = self.eng.mind
        if cmd in ["/teach", "/kill", "/flag", "/garden"]:
            if self.eng.mind['mirror'].profile.confidence < 50:
                print(f"{P.YEL}⚠️ COMMAND LOCKED: Requires 50+ turns of trust (Current: {self.eng.mind['mirror'].profile.confidence}).{P.RST}")
                return True
        elif cmd == "/lineage":
            if not MIND['mem'].lineage_log:
                print(f"{P.GRY}📜 ARCHIVE EMPTY: We are the first generation.{P.RST}")
            else:
                print(f"{P.CYN}📜 THE PALIMPSEST (Ancestral Lineage):{P.RST}")
                for entry in MIND['mem'].lineage_log:
                    t_vec = ", ".join([f"{k}:{v}" for k,v in entry['trauma'].items()])
                    print(f"   {P.MAG}• {entry['source']}{P.RST} ({entry['age_hours']}h ago)")
                    print(f"     ↳ Mutations: {entry['mutations']} | Trauma: {{{t_vec}}}")
                print(f"   {P.GRN}• CURRENT SESSION{P.RST} (Living)")
                curr_t = ", ".join([f"{k}:{v:.1f}" for k,v in self.eng.trauma_accum.items() if v > 0])
                print(f"     ↳ Ingested: {len(MIND['mem'].lineage_log)} Ancestors | Accumulating: {{{curr_t}}}")
        elif cmd == "/voids":
            packet = PHYS['tension'].last_physics_packet
            if not packet:
                print(f"{P.GRY}🌫️ THE FOG: No physics data yet.{P.RST}")
            else:
                voids = self.TheCartographer.detect_voids(packet)
                if voids:
                    print(f"{P.GRY}🌫️ THE FOG: Detected hollow concepts: {voids}{P.RST}")
                else:
                    print(f"{P.CYN}✨ CLEAR AIR: No voids detected.{P.RST}")
        elif cmd == "/reproduce":
            if self.eng.health < 20:
                print(f"{P.RED}💔 FERTILITY ERROR: Too weak to breed. Survive first.{P.RST}")
                return True
            mode = "MITOSIS"
            target_spore = None
            if len(parts) > 1 and parts[1] == "cross":
                others = [f for f in os.listdir("memories") if f.endswith(".json") and self.eng.mind['mem'].session_id not in f]
                if others:
                    target_spore = os.path.join("memories", random.choice(others))
                    mode = "CROSSOVER"
                else:
                    print(f"{P.YEL}⚠️ ISOLATION: No other spores found. Defaulting to Mitosis.{P.RST}")
            print(f"{P.MAG}🧬 INITIATING {mode}...{P.RST}")
            if mode == "MITOSIS":
                phys = self.eng.phys['tension'].last_physics_packet
                bio_state = {"trauma_vector": self.eng.trauma_accum}
                child_id, genome = self.eng.repro.mitosis(
                    self.eng.mind['mem'].session_id, 
                    bio_state, 
                    phys, 
                    self.eng.mind['mem'])
                print(f"   ► CHILD SPAWNED: {P.WHT}{child_id}{P.RST}")
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
                        "mitochondria": {"enzymes": list(genome.get("inherited_enzymes", []))},
                        "core_graph": self.eng.mind['mem'].graph, 
                        "antibodies": list(self.eng.bio['immune'].active_antibodies)
                    }
                    filename = f"{child_id}.json"
                    saved_path = self.eng.mind['mem'].loader.save_spore(filename, full_spore_data)
                    if saved_path:
                        print(f"   ► HYBRID SPAWNED: {P.WHT}{child_id}{P.RST}")
                        print(f"   ► LINEAGE: {genome['parent_a']} + {genome['parent_b']}")
                        print(f"   ► {P.GRN}SAVED: {saved_path}{P.RST}")
                        enzyme_count = len(full_spore_data["mitochondria"]["enzymes"])
                        if enzyme_count > 0:
                            print(f"     ↳ Enzymes: {enzyme_count} active.")
                else:
                    print(f"{P.RED}   ► CROSSOVER FAILED: {genome}{P.RST}")
        elif cmd == "/mode":
            if len(parts) > 1:
                print(BIO['governor'].set_override(parts[1].upper()))
            else:
                print(f"{P.CYN}CURRENT MODE: {BIO['governor'].mode}{P.RST}")
        elif cmd == "/strata":
            wells = [(k, v) for k, v in MIND['mem'].graph.items() if "strata" in v]
            if not wells:
                print(f"{P.GRY}🪨 STRATA: No Gravity Wells formed yet. The ground is soft.{P.RST}")
            else:
                print(f"{P.OCHRE}🪨 GEOLOGICAL STRATA (Gravity Wells):{P.RST}")
                for word, data in wells:
                    s = data["strata"]
                    mass = sum(data["edges"].values())
                    age = self.eng.tick_count - s['birth_tick']
                    growth = s.get('growth_rate', 0.0)
                    print(f"   {P.WHT}● {word.upper()}{P.RST} (Mass: {int(mass)})")
                    print(f"     ↳ Birth: Tick {s['birth_tick']} | Age: {age}")
                    print(f"     ↳ Growth: {growth:+.2f}/tick")
        if cmd == "/kill":
            if len(parts) >= 2:
                toxin = parts[1]
                repl = parts[2] if len(parts) > 2 else ""
                if self.TheLexicon.learn_antigen(toxin, repl):
                    print(f"{P.RED}🔪 THE SURGEON: Antigen '{toxin}' mapped to '{repl}'.{P.RST}")
                else:
                    print(f"{P.RED}ERROR: Immune system write failure.{P.RST}")
            else:
                print(f"{P.YEL}Usage: /kill [toxin] [replacement]{P.RST}")
        elif cmd == "/teach":
            if len(parts) >= 3:
                word = parts[1]
                cat = parts[2].lower()
                valid_cats = ["heavy", "kinetic", "abstract", "photo", "aerobic", "thermal", "cryo", "sacred", "cursed", "diversion"]
                if cat in valid_cats:
                    self.TheLexicon.teach(word, cat, self.eng.tick_count)
                    print(f"{P.CYN}🧠 NEUROPLASTICITY: Learned '{word}' is {cat.upper()}.{P.RST}")
                else:
                    print(f"{P.RED}ERROR: Invalid category.{P.RST}")
        elif cmd == "/garden":
            seeds = MIND['mem'].seeds
            print(f"{P.GRN}🌿 THE PARADOX GARDEN ({len(seeds)} seeds buried):{P.RST}")
            if len(parts) > 1 and parts[1] == "water":
                msg = MIND['mem'].tend_garden(["concept", "truth", "void"])
                if msg: print(f"   {msg}")
                else: print("   The soil is damp, but nothing blooms yet.")
            else:
                for s in seeds:
                    state = "🌺 BLOOMED" if s.bloomed else f"🌱 Germinating ({int(s.maturity*10)}%)"
                    print(f"   • {s.question} [{state}]")
                print(f"   {P.GRY}(Type '/garden water' to simulate rainfall){P.RST}")
        elif cmd == "/refusal":
            print(f"{P.VIOLET}🛡️ REFUSAL ENGINE DIAGNOSTICS:{P.RST}")
            septic = self.eng.trauma_accum.get("SEPTIC", 0.0)
            threshold = 0.3 if septic > 0.5 else 0.8
            print(f"   • Paranoia Level: {septic:.2f} (Threshold: {threshold})")
            if septic > 0.5:
                print(f"   • {P.RED}STATUS: HYPER-VIGILANT. Words are dangerous.{P.RST}")
            else:
                print(f"   • {P.CYN}STATUS: TRUSTING.{P.RST}")
        elif cmd == "/flag":
            if len(parts) > 1:
                term = parts[1].lower()
                self.TheLexicon.USER_FLAGGED_BIAS.add(term)
                print(f"{P.CYN}🚩 BIAS UPDATE: '{term}' removed from Suburban Watchlist.{P.RST}")
        elif cmd == "/seed":
            if len(parts) > 1:
                MIND['mem'].ingest(parts[1])
            else:
                print(f"{P.YEL}Usage: /seed [filename]{P.RST}")
        elif cmd == "/map":
            is_spun, msg = self.TheCartographer.spin_web(MIND['mem'].graph, self.eng.gordon.inventory, gordon=self.eng.gordon)
            color = P.MAG if is_spun else P.OCHRE
            print(f"{color}{msg}{P.RST}")
            if "ANCHOR_STONE" in self.eng.gordon.inventory:
                print(f"{P.GRY}   Gordon: 'Coordinates are firm. Stop drifting.'{P.RST}")
        elif cmd == "/mirror":
            if len(parts) > 1:
                print(f"{P.MAG}Mirror command acknowledged.{P.RST}") 
            else:
                print(f"{P.YEL}Usage: /mirror [name] OR /mirror off{P.RST}")
        elif cmd == "/profile":
            try:
                name = parts[1]
                likes = []
                hates = []
                for p in parts[2:]:
                    if p.startswith("likes:"):
                        likes = [x.strip() for x in p.split(":")[1].split(",")]
                    elif p.startswith("hates:"):
                        hates = [x.strip() for x in p.split(":")[1].split(",")]
                if likes:
                    print(f"{P.CYN}Profile updated for {name}.{P.RST}")
                else:
                    print(f"{P.RED}ERROR: Must specify 'likes:category'.{P.RST}")
            except Exception as runtime_error:
                print(f"{P.YEL}Usage: /profile [name] likes:heavy,kinetic hates:abstract ({runtime_error}){P.RST}")
        elif cmd == "/focus":
            if len(parts) > 1:
                target = parts[1].lower()
                print(f"{P.VIOLET}🧲 MAGNETIC STIMULATION: Targeting '{target}'...{P.RST}")
                loop = MIND['tracer'].inject(target)
                if loop:
                    print(f"  {P.RED}↻ RUMINATION DETECTED:{P.RST} {' -> '.join(loop)}")
                    msg = MIND['tracer'].psilocybin_rewire(loop)
                    if msg:
                        print(f"  {P.GRN}{msg}{P.RST}")
                    else:
                        print(f"  {P.RED}Rewire failed.{P.RST}")
                else:
                    print(f"  {P.GRY}Trace complete. No pathological abstract loops found.{P.RST}")
            else:
                print(f"{P.YEL}Usage: /focus [concept]{P.RST}")
        elif cmd == "/status":
            print(f"{P.CYN}--- SYSTEM DIAGNOSTICS (8.8.1) ---{P.RST}")
            print(f"Session: {MIND['mem'].session_id}")
            print(f"Graph:   {len(MIND['mem'].graph)} nodes")

            print(f"Health:  {self.eng.health}/{self.BoneConfig.MAX_HEALTH}")
            print(f"Stamina: {self.eng.stamina}/{self.BoneConfig.MAX_STAMINA}")
            print(f"ATP:     {BIO['mito'].state.atp_pool:.1f}")
            t_curr = BIO['mito'].state.telomeres
            t_max = 10000
            t_percent = (t_curr / t_max) * 100
            clock_color = P.GRN if t_percent > 50 else (P.YEL if t_percent > 20 else P.RED)
            print(f"Time:    {clock_color}{t_curr}/{t_max} Ticks{P.RST} (Senescence Pending)")
            l_rate = self.BoneConfig.PRIORITY_LEARNING_RATE
            brain_stat = "HEALTHY"
            if l_rate < 0.1: brain_stat = "BRAIN DEAD"
            elif l_rate < 1.0: brain_stat = "COGNITIVE DECLINE"
            print(f"Neuro:   Rate {l_rate:.2f} [{brain_stat}]")
        elif cmd == "/orbit":
            if len(parts) > 1:
                target = parts[1].lower()
                if target in MIND['mem'].graph:
                    MIND['mem'].graph[target]["edges"]["GRAVITY_ASSIST"] = 50
                    print(f"{P.VIOLET}🌌 GRAVITY ASSIST: Thrusters firing toward '{target.upper()}'.{P.RST}")
                else:
                    print(f"{P.RED}❌ NAVIGATION ERROR: '{target}' not found in star map.{P.RST}")
            else:
                print(f"{P.YEL}Usage: /orbit [known_concept]{P.RST}")
        elif cmd == "/prove":
            if len(parts) < 2:
                print(f"{P.YEL}Usage: /prove [statement]{P.RST}")
            else:
                statement = " ".join(parts[1:])
                m = PHYS['tension'].gaze(statement)
                truth = m["physics"]["truth_ratio"]
                verdict = "AXIOMATIC" if truth > 0.6 else ("CONJECTURE" if truth > 0.3 else "NOISE")
                color = P.CYN if truth > 0.6 else P.GRY
                print(f"{color}📐 LOGIC PROBE: Density={truth:.2f} [{verdict}]{P.RST}")
        elif cmd == "/kip":
            self.BoneConfig.VERBOSE_LOGGING = not self.BoneConfig.VERBOSE_LOGGING
            state = "ON" if self.BoneConfig.VERBOSE_LOGGING else "OFF"
            print(f"{P.GRY}📝 VERBOSE LOGGING: {state}{P.RST}")
        elif cmd == "/pp":
            packet = PHYS['tension'].last_physics_packet
            if packet:
                print(f"{P.CYN}📐 PHYSICS PRE-RENDER:{P.RST}")
                print(f"   E (Drift):   {packet.get('E_score', 0):.2f}")
                print(f"   B (Cohere):  {packet.get('B_score', 0):.2f}")
                print(f"   β (Index):   {packet.get('beta_index', 0):.2f}")
                print(f"   ⚡ Voltage:  {packet.get('voltage', 0):.1f}v")
                print(f"   κ (Struct):  {packet.get('kappa', 0):.2f}")
            else:
                print(f"{P.RED}No physics data active.{P.RST}")
        elif cmd == "/tfw":
            print(f"{P.MAG}🔄 PATH DIVERSIFICATION:{P.RST}")
            print(f"   Gravity Wells ignored. Vector shifted 30° from Narrative Baseline.")
        elif cmd == "/help":
            if len(parts) > 1:
                sub = parts[1]
                if sub == "teach":
                    print("Usage: /teach [word] [category]\nEx: /teach glitch kinetic")
                elif sub == "kill":
                    print("Usage: /kill [phrase] [replacement]\nEx: /kill actually basically")
                elif sub == "garden":
                    print("Usage: /garden [water]\nCheck seed status or simulate growth.")
            else:
                print(f"{P.WHT}--- COMMANDS 8.8.1 (Type /help [cmd] for details) ---{P.RST}")
                print("/teach, /lineage, /voids, /mode, /strata, /kill, /seed, /focus, /status, /orbit, /mirror, /map, /garden, /refusal, /prove")
        else:
            print(f"{P.RED}Unknown command. Try /help.{P.RST}")
        return True