import os, random, time, math
from typing import Dict, List, Callable
from bone_shared import ParadoxSeed

class CommandProcessor:
    def __init__(self, engine, prisma_ref, lexicon_ref, config_ref, cartographer_ref):
        self.eng = engine
        self.P = prisma_ref
        self.Lex = lexicon_ref
        self.Config = config_ref
        self.Map = cartographer_ref
        self.registry: Dict[str, Callable[[List[str]], bool]] = {
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
            "/focus": self._cmd_focus,
            "/status": self._cmd_status,
            "/manifold": self._cmd_manifold,
            "/orbit": self._cmd_orbit,
            "/prove": self._cmd_prove,
            "/kip": self._cmd_kip,
            "/pp": self._cmd_pp,
            "/tfw": self._cmd_tfw,
            "/weave": self._cmd_weave,
            "/kintsugi": self._cmd_kintsugi,
            "/help": self._cmd_help
        }

    def _log(self, text):
        self.eng.events.log(text, "CMD")

    def _cmd_manifold(self, parts):
        nav = self.eng.navigator
        current = nav.current_location
        phys = self.eng.phys.tension.last_physics_packet
        if not phys or "voltage" not in phys:
            self._log(f"{self.P.GRY}NAVIGATION OFFLINE: No physics data yet.{self.P.RST}")
            return True

        drag = min(10.0, max(0.0, phys.get("narrative_drag", 0.0)))
        volt = min(20.0, max(0.0, phys.get("voltage", 0.0)))
        my_vec = (round(drag / 10.0, 2), round(volt / 20.0, 2))

        self._log(f"{self.P.CYN}--- MANIFOLD NAVIGATION ---{self.P.RST}")
        self._log(f"Current Vector: [Drag: {my_vec[0]} | Voltage: {my_vec[1]}]")
        self._log(f"Location: {self.P.WHT}{current}{self.P.RST}")
        self._log(f"Shimmer Reserves: {self.eng.shimmer_state.current:.1f}")

        self._log(f"\n{self.P.GRY}Destinations:{self.P.RST}")
        for name, data in nav.manifolds.items():
            dist = math.dist(my_vec, data.center_vector)
            bar_len = int((1.0 - min(1.0, dist)) * 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)

            highlight = self.P.GRN if name == current else self.P.GRY
            self._log(f"   {highlight}{name:<12}{self.P.RST} {bar} ({dist:.2f} AU) - {data.description}")

        return True

    def execute(self, text):
        if not text.startswith("/"):
            return False
        parts = text.split()
        cmd = parts[0].lower()
        if cmd not in self.registry:
            self._log(f"{self.P.RED}Unknown command. Try /help.{self.P.RST}")
            return True
        restricted_cmds = ["/teach", "/kill", "/flag"]
        if cmd in restricted_cmds:
            confidence = self.eng.mind.mirror.profile.confidence
            if confidence < 10:
                self._log(f"{self.P.YEL}COMMAND LOCKED: Requires 10+ turns of trust (Current: {confidence}).{self.P.RST}")
                return True
        try:
            handler = self.registry[cmd]
            return handler(parts)
        except Exception as e:
            self._log(f"{self.P.RED}COMMAND FAILURE: {e}{self.P.RST}")
            return True

    def _cmd_teach(self, parts):
        if len(parts) >= 3:
            word = parts[1]
            cat = parts[2].lower()
            self.Lex.teach(word, cat, self.eng.tick_count)
            self._log(f"{self.P.CYN}NEUROPLASTICITY: Learned '{word}' is {cat.upper()}.{self.P.RST}")
        return True

    def _cmd_kill(self, parts):
        if len(parts) >= 2:
            toxin = parts[1]
            repl = parts[2] if len(parts) > 2 else ""
            if self.Lex.learn_antigen(toxin, repl):
                self._log(f"{self.P.RED}THE SURGEON: Antigen '{toxin}' mapped to '{repl}'.{self.P.RST}")
            else:
                self._log(f"{self.P.RED}ERROR: Immune system write failure.{self.P.RST}")
        else:
            self._log(f"{self.P.YEL}Usage: /kill [toxin] [replacement]{self.P.RST}")
        return True

    def _cmd_flag(self, parts):
        if len(parts) > 1:
            term = parts[1].lower()
            self.Lex.USER_FLAGGED_BIAS.add(term)
            self._log(f"{self.P.CYN}BIAS UPDATE: '{term}' flagged.{self.P.RST}")
        return True

    def _cmd_garden(self, parts):
        seeds = self.eng.mind.mem.seeds
        self._log(f"{self.P.GRN}THE PARADOX GARDEN:{self.P.RST}")
        if len(parts) > 1 and parts[1] == "water":
            msg = self.eng.mind.mem.tend_garden(["concept", "truth", "void"])
            if msg: self._log(f"   {msg}")
            else: self._log("   The soil is damp, but nothing blooms yet.")
        else:
            for s in seeds:
                state = "BLOOMED" if s.bloomed else f"Germinating ({int(s.maturity*10)}%)"
                self._log(f"   {s.question} [{state}]")
        return True

    def _cmd_reproduce(self, parts):
        if self.eng.health < 20:
            self._log(f"{self.P.RED}FERTILITY ERROR: Too weak to breed. Survive first.{self.P.RST}")
            return True
        mode = "MITOSIS"
        target_spore = None
        if len(parts) > 1 and parts[1] == "cross":
            others = [f for f in os.listdir("memories") if f.endswith(".json") and self.eng.mind.mem.session_id not in f]
            if others:
                target_spore = os.path.join("memories", random.choice(others))
                mode = "CROSSOVER"
            else:
                self._log(f"{self.P.YEL}ISOLATION: No other spores found. Defaulting to Mitosis.{self.P.RST}")
        self._log(f"{self.P.MAG}INITIATING {mode}...{self.P.RST}")
        if mode == "MITOSIS":
            phys = self.eng.phys.tension.last_physics_packet
            bio_state = {"trauma_vector": self.eng.trauma_accum}
            child_id, genome = self.eng.repro.mitosis(
                self.eng.mind.mem.session_id,
                bio_state,
                phys,
                self.eng.mind.mem)
            self._log(f"   ► CHILD SPAWNED: {self.P.WHT}{child_id}{self.P.RST}")
            self._log(f"   ► TRAIT: {genome['mutations']}")
        elif mode == "CROSSOVER":
            current_bio = {
                "trauma_vector": self.eng.trauma_accum,
                "mito": self.eng.bio.mito}
            child_id, genome = self.eng.repro.crossover(
                self.eng.mind.mem.session_id,
                current_bio,
                target_spore)
            if child_id:
                full_spore_data = {
                    "session_id": child_id,
                    "meta": {
                        "timestamp": time.time(),
                        "final_health": self.eng.health,
                        "final_stamina": self.eng.stamina},
                    "trauma_vector": genome.get("trauma_inheritance", {}),
                    "config_mutations": genome.get("config_mutations", {}),
                    "mitochondria": {"enzymes": list(genome.get("inherited_enzymes", []))},
                    "core_graph": self.eng.mind.mem.graph,
                    "antibodies": list(self.eng.bio.immune.active_antibodies)}
                filename = f"{child_id}.json"
                saved_path = self.eng.mind.mem.loader.save_spore(filename, full_spore_data)
                if saved_path:
                    self._log(f"   HYBRID SPAWNED: {self.P.WHT}{child_id}{self.P.RST}")
                    self._log(f"   {self.P.GRN}SAVED: {saved_path}{self.P.RST}")
            else:
                self._log(f"{self.P.RED}   CROSSOVER FAILED: {genome}{self.P.RST}")
        return True

    def _cmd_mode(self, parts):
        if len(parts) > 1:
            self._log(self.eng.bio.governor.set_override(parts[1].upper()))
        else:
            self._log(f"{self.P.CYN}CURRENT MODE: {self.eng.bio.governor.mode}{self.P.RST}")
        return True

    def _cmd_seed(self, parts):
        if len(parts) < 2:
            self._log(f"{self.P.YEL}Usage: /seed [The question or paradox to plant]{self.P.RST}")
            return True
        text = " ".join(parts[1:])
        triggers = set(self.Lex.clean(text))
        if not triggers:
            self._log(f"{self.P.RED}SEED ERROR: That idea is too hollow. Use heavier words.{self.P.RST}")
            return True
        new_seed = ParadoxSeed(text, triggers)
        self.eng.mind.mem.seeds.append(new_seed)

        self._log(f"{self.P.GRN}GARDEN: Planted new seed.{self.P.RST}")
        self._log(f"   Question: '{text}'")
        self._log(f"   {self.P.GRY}Triggers: {triggers}{self.P.RST}")
        return True

    def _cmd_load(self, parts):
        if len(parts) > 1:
            target = parts[1]
            if not target.endswith(".json"):
                target += ".json"
            self.eng.mind.mem.ingest(target)
        else:
            self._log(f"{self.P.YEL}Usage: /load [filename]{self.P.RST}")
        return True

    def _cmd_mirror(self, parts):
        mirror = self.eng.mind.mirror
        if len(parts) > 1:
            if parts[1].lower() == "off":
                mirror.active_mode = False
                self._log(f"{self.P.GRY}MIRROR: Disabled. The system will no longer reflect your biases.{self.P.RST}")
            elif parts[1].lower() == "on":
                mirror.active_mode = True
                self._log(f"{self.P.MAG}MIRROR: Enabled. Watching for patterns.{self.P.RST}")
            else:
                self._log(f"{self.P.YEL}Usage: /mirror [on/off]{self.P.RST}")
        else:
            state = "ON" if mirror.active_mode else "OFF"
            self._log(f"{self.P.CYN}MIRROR STATUS: {state}{self.P.RST}")
            self._log(mirror.get_status())
        return True

    def _cmd_focus(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            self._log(f"{self.P.VIOLET}FOCUSING: '{target}'...{self.P.RST}")
            tracer = self.eng.mind.tracer
            loop = tracer.inject(target)
            if loop:
                self._log(f"  {self.P.RED}RUMINATION:{self.P.RST} {' -> '.join(loop)}")
                if len(parts) > 2 and parts[2] == "break":
                    result = tracer.psilocybin_rewire(loop)
                    if result:
                        self._log(f"  {self.P.GRN}{result}{self.P.RST}")
                else:
                    self._log(f"  {self.P.GRY}To rewire this loop, use: /focus {target} break{self.P.RST}")
            else:
                self._log(f"  {self.P.GRY}No pathological loops found.{self.P.RST}")
        return True

    def _cmd_orbit(self, parts):
        if len(parts) > 1:
            target = parts[1].lower()
            if target in self.eng.mind.mem.graph:
                self.eng.mind.mem.graph[target]["edges"]["GRAVITY_ASSIST"] = 50
                self._log(f"{self.P.VIOLET}GRAVITY ASSIST: Thrusters firing toward '{target.upper()}'.{self.P.RST}")
            else:
                self._log(f"{self.P.RED}ERROR: '{target}' not found.{self.P.RST}")
        return True

    def _cmd_prove(self, parts):
        if len(parts) < 2:
            self._log(f"{self.P.YEL}Usage: /prove [statement]{self.P.RST}")
        else:
            statement = " ".join(parts[1:])
            m = self.eng.phys.tension.gaze(statement)
            truth = m["physics"]["truth_ratio"]
            self._log(f"{self.P.CYN}LOGIC PROBE: Density={truth:.2f}{self.P.RST}")
        return True

    def _cmd_weave(self, parts):
        inventory = self.eng.gordon.inventory
        success, msg = self.Map.spin_web(
            self.eng.mind.mem.graph,
            inventory,
            self.eng.gordon)
        if success:
            self._log(f"{self.P.CYN}{msg}{self.P.RST}")
            self.eng.stamina = max(0.0, self.eng.stamina - 5.0)
            self._log(f"   {self.P.GRY}(Stamina -5.0){self.P.RST}")
        else:
            self._log(f"{self.P.RED}{msg}{self.P.RST}")
        return True

    def _cmd_lineage(self, parts):
        log = self.eng.mind.mem.lineage_log
        if not log:
            self._log(f"{self.P.GRY}ARCHIVE EMPTY: We are the first generation.{self.P.RST}")
            return True
        self._log(f"{self.P.CYN}THE PALIMPSEST (Ancestral Lineage):{self.P.RST}")
        for entry in log:
            t_vec = ", ".join([f"{k}:{v}" for k,v in entry['trauma'].items()])
            self._log(f"   {self.P.MAG}• {entry['source']}{self.P.RST} ({entry['age_hours']}h ago)")
            self._log(f"     ↳ Mutations: {entry['mutations']} | Trauma: {{{t_vec}}}")
        return True

    def _cmd_voids(self, parts):
        packet = self.eng.phys.tension.last_physics_packet
        if not packet:
            self._log(f"{self.P.GRY}THE FOG: No physics data yet.{self.P.RST}")
            return True
        voids = self.Map.detect_voids(packet)
        if voids:
            self._log(f"{self.P.GRY}THE FOG: Detected hollow concepts: {voids}{self.P.RST}")
        else:
            self._log(f"{self.P.CYN}CLEAR AIR: No voids detected.{self.P.RST}")
        return True

    def _cmd_strata(self, parts):
        wells = [(k, v) for k, v in self.eng.mind.mem.graph.items() if "strata" in v]
        if not wells:
            self._log(f"{self.P.GRY}STRATA: No Gravity Wells formed yet.{self.P.RST}")
        else:
            self._log(f"{self.P.OCHRE}GEOLOGICAL STRATA:{self.P.RST}")
            for word, data in wells:
                s = data["strata"]
                age = self.eng.tick_count - s['birth_tick']
                self._log(f"   {self.P.WHT}● {word.upper()}{self.P.RST} (Age: {age} ticks)")
        return True

    def _cmd_kintsugi(self, parts):
        k = self.eng.kintsugi
        self._log(f"{self.P.YEL}--- KINTSUGI STATUS ---{self.P.RST}")
        if k.active_koan:
            self._log(f"STATE: {self.P.RED}FRACTURED{self.P.RST}")
            self._log(f"ACTIVE KOAN: '{k.active_koan}'")
            self._log(f"REQUIREMENT: High Voltage + Playfulness")
        else:
            self._log(f"STATE: {self.P.GRN}WHOLE{self.P.RST}")
        self._log(f"TOTAL REPAIRS: {k.repairs_count}")
        self._log(f"TRAUMA LOAD: {self.eng.trauma_accum}")
        return True

    def _cmd_publish(self, parts):
        journal = self.eng.journal
        phys = self.eng.phys.tension.last_physics_packet
        if not phys:
            self._log(f"{self.P.RED}Nothing to publish.{self.P.RST}")
            return True
        success, review, reward = journal.publish(phys["raw_text"], phys, self.eng.bio)
        if success:
            self._log(f"{self.P.CYN}PUBLISHED.{self.P.RST} Review: {review}")
            if reward == "SEROTONIN_BOOST":
                self.eng.bio.endo.serotonin = min(1.0, self.eng.bio.endo.serotonin + 0.2)
                self._log(f"   {self.P.GRN}► STATUS UP: Serotonin +0.2{self.P.RST}")
        return True

    def _cmd_refusal(self, parts):
        septic = self.eng.trauma_accum.get("SEPTIC", 0.0)
        self._log(f"{self.P.VIOLET}REFUSAL ENGINE: Paranoia Level {septic:.2f}{self.P.RST}")
        return True

    def _cmd_map(self, parts):
        phys = self.eng.phys.tension.last_physics_packet
        if not phys or "raw_text" not in phys:
            self._log(f"{self.P.GRY}FOG OF WAR: No physics data. Speak to the system first to generate terrain.{self.P.RST}")
            return True
        bio_metrics = {
            "cortisol": self.eng.bio.endo.cortisol,
            "oxytocin": self.eng.bio.endo.oxytocin,
            "atp": self.eng.bio.mito.state.atp_pool}
        phys = self.eng.phys.tension.last_physics_packet
        result_msg, anchors = self.Map.weave(
            self.eng.phys.tension.last_physics_packet["raw_text"],
            self.eng.mind.mem.graph,
            bio_metrics,
            self.eng.limbo,
            physics=phys)
        self._log(f"{self.P.OCHRE}CARTOGRAPHY REPORT:{self.P.RST}")
        self._log(result_msg)
        if "ANCHOR_STONE" in self.eng.gordon.inventory:
            self._log(f"{self.P.GRY}   Gordon: 'The anchor holds. We are here.'{self.P.RST}")
        elif len(anchors) < 2:
            self._log(f"{self.P.GRY}   Gordon: 'This map is useless. I need more rocks.'{self.P.RST}")
        return True

    def _cmd_status(self, parts):
        bio = self.eng.bio
        self._log(f"{self.P.CYN}--- SYSTEM DIAGNOSTICS ---{self.P.RST}")
        self._log(f"Health:  {self.eng.health:.1f}/{self.Config.MAX_HEALTH}")
        self._log(f"Stamina: {self.eng.stamina:.1f}/{self.Config.MAX_STAMINA}")
        self._log(f"ATP:     {bio.mito.state.atp_pool:.1f}")
        return True

    def _cmd_kip(self, parts):
        self.Config.VERBOSE_LOGGING = not self.Config.VERBOSE_LOGGING
        state = "ON" if self.Config.VERBOSE_LOGGING else "OFF"
        self._log(f"{self.P.GRY}VERBOSE LOGGING: {state}{self.P.RST}")
        return True

    def _cmd_pp(self, parts):
        packet = self.eng.phys.tension.last_physics_packet
        if packet:
            self._log(f"{self.P.CYN}PHYSICS DUMP:{self.P.RST} V:{packet.get('voltage',0)} D:{packet.get('narrative_drag',0)}")
        return True

    def _cmd_tfw(self, parts):
        phys = self.eng.phys.tension.last_physics_packet
        if phys:
            old_drag = phys.get("narrative_drag", 0.0)
            phys["narrative_drag"] = max(0.0, old_drag - 2.0)
            phys["beta_index"] = random.uniform(0.1, 2.0)

            self._log(f"{self.P.MAG}PATH DIVERSIFICATION EXECUTED:{self.P.RST}")
            self._log(f"   Gravity Wells ignored. Vector shifted 30°.")
            self._log(f"   {self.P.GRY}Drag reduced by 2.0. Beta randomized.{self.P.RST}")
        else:
            self._log(f"{self.P.RED}Cannot shift vector: No physics packet active.{self.P.RST}")
        return True

    def _cmd_help(self, parts):
        self._log(f"{self.P.WHT}--- COMMANDS ---{self.P.RST}")
        cmds = list(self.registry.keys())
        self._log(", ".join(cmds))
        return True