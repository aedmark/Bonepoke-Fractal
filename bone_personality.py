# bone_personality.py
# "The masks we wear, and the taxes we pay."

import json, os, random, time
from collections import deque
from typing import Dict, Tuple, Optional, Counter
from bone_data import LENSES, NARRATIVE_DATA
from bone_bus import EventBus
from bone_lexicon import TheLexicon
from bone_bus import Prisma, BoneConfig

class UserProfile:
    """Maintains the long-term psychological profile of the user."""
    def __init__(self, name="USER"):
        self.name = name
        self.affinities = {"heavy": 0.0, "kinetic": 0.0, "abstract": 0.0, "photo": 0.0, "aerobic": 0.0, "thermal": 0.0,
                           "cryo": 0.0, }
        self.confidence = 0
        self.file_path = "user_profile.json"
        self.load()

    def update(self, counts, total_words):
        if total_words < 3:
            return
        self.confidence += 1
        alpha = 0.2 if self.confidence < 50 else 0.05
        for cat in self.affinities:
            density = counts.get(cat, 0) / total_words
            target = 1.0 if density > 0.15 else (-0.5 if density == 0 else 0.0)
            self.affinities[cat] = (alpha * target) + (
                    (1 - alpha) * self.affinities[cat])

    def get_preferences(self):
        likes = [k for k, v in self.affinities.items() if v > 0.3]
        hates = [k for k, v in self.affinities.items() if v < -0.2]
        return likes, hates

    def save(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.__dict__, f)
        except IOError:
            pass

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.affinities = data.get("affinities", self.affinities)
                    self.confidence = data.get("confidence", 0)
            except (IOError, json.JSONDecodeError):
                pass

class EnneagramDriver:
    def __init__(self, events_ref):
        self.events = events_ref
        self.current_persona = "NARRATOR"
        self.pending_persona = None
        self.stability_counter = 0
        self.HYSTERESIS_THRESHOLD = 3

    @staticmethod
    def _calculate_raw_persona(physics) -> Tuple[str, str, str]:
        """Pure logic: determines who SHOULD be in charge based on physics."""
        tension = physics.get("voltage", 0.0) if isinstance(physics, dict) else physics.voltage
        compression = physics.get("narrative_drag", 0.0) if isinstance(physics, dict) else physics.narrative_drag
        coherence = physics.get("kappa", 0.0) if isinstance(physics, dict) else physics.kappa

        scores = {
            "JESTER": 0, "GORDON": 0, "GLASS": 0,
            "CLARENCE": 0, "NATHAN": 0, "SHERLOCK": 0, "NARRATOR": 0
        }

        if tension > 12.0: scores["JESTER"] += 5
        if tension > 8.0: scores["NATHAN"] += 3
        if compression > 4.0: scores["GORDON"] += 5
        if coherence < 0.2: scores["GLASS"] += 4
        if coherence > 0.8: scores["CLARENCE"] += 4
        scores["SHERLOCK"] += 2
        scores["NARRATOR"] += 2

        winner = max(scores, key=scores.get)
        reason = f"Scoring Winner: {winner} (Score: {scores[winner]})"

        state_desc = "ACTIVE"
        if winner == "JESTER": state_desc = "MANIC"
        elif winner == "GORDON": state_desc = "TIRED"
        elif winner == "GLASS": state_desc = "FRAGILE"
        elif winner == "CLARENCE": state_desc = "RIGID"

        return winner, state_desc, reason

    def decide_persona(self, physics) -> Tuple[str, str, str]:
        """Stateful wrapper: Applies hysteresis to preventing flickering."""
        candidate, state_desc, reason = self._calculate_raw_persona(physics)

        if candidate == self.current_persona:
            self.stability_counter = 0
            self.pending_persona = None
            return self.current_persona, state_desc, reason

        if candidate == self.pending_persona:
            self.stability_counter += 1
        else:
            self.pending_persona = candidate
            self.stability_counter = 1

        if self.stability_counter >= self.HYSTERESIS_THRESHOLD:
            self.current_persona = candidate
            self.stability_counter = 0
            self.pending_persona = None
            return self.current_persona, state_desc, f"SHIFT: {reason}"
        else:
            return self.current_persona, "STABLE", f"Resisting shift to {candidate} ({self.stability_counter}/{self.HYSTERESIS_THRESHOLD})"

class SynergeticLensArbiter:
    def __init__(self, events: EventBus):
        self.events = events
        self.enneagram = EnneagramDriver(events)
        self.current_focus = "NARRATOR"
        self.last_reason = "System Init"

    def consult(self, physics, bio_state, _inventory, current_tick, _ignition_score=0.0):
        if current_tick <= 5:
            self.current_focus = "NARRATOR"
            if hasattr(physics, "voltage") and physics["voltage"] > 5.0:
                physics["voltage"] = 4.0
            return "NARRATOR", "The system is listening.", "The Witness [Init]"
        lens_name, state_desc, reason = self.enneagram.decide_persona(physics)
        chem = bio_state.get("chem", {})
        adrenaline_val = chem.get("adrenaline", chem.get("ADR", 0.5))
        msg, role = self._fetch_voice_data(lens_name, physics, adrenaline_val)
        self.current_focus = lens_name
        final_role = f"{role} [{state_desc}]"
        self.last_reason = reason
        return lens_name, msg, final_role

    @staticmethod
    def _fetch_voice_data(lens, p, adrenaline_val):
        if lens not in LENSES: lens = "NARRATOR"
        data = LENSES[lens]
        role = data.get("role", "The System")
        template = data.get("msg", "Proceed.")
        ctx = {
            "kappa": p.get("kappa", 0.0),
            "voltage": p.get("voltage", 0.0),
            "adr": adrenaline_val,
            "beta_index": p.get("beta_index", 0.0),
            "drag": p.get("narrative_drag", 0.0),
            "truth_ratio": p.get("truth_ratio", 0.0)
        }
        try:
            msg = template.format(**ctx)
        except (KeyError, ValueError, IndexError):
            msg = template
        return msg, role

class ZenGarden:
    def __init__(self, events_ref):
        self.events = events_ref
        self.stillness_streak = 0
        self.max_streak = 0
        self.pebbles_collected = 0
        self.koans = [
            "The code that is not written has no bugs.",
            "To optimize the loop, one must first exit it.",
            "Silence is also a form of input.",
            "The server hums. It is enough.",
            "Optimize for the space between the logs."
        ]

    def raking_the_sand(self, physics: Dict, bio: Dict) -> Tuple[float, Optional[str]]:
        voltage = physics.get("voltage", 0.0)
        drag = physics.get("narrative_drag", 0.0)
        toxin = physics.get("counts", {}).get("toxin", 0)
        cortisol = bio.get("chem", {}).get("COR", 0.0)

        is_stable = (2.0 <= voltage <= 12.0) and (drag <= 4.0) and (toxin == 0) and (cortisol < 0.4)

        if is_stable:
            self.stillness_streak += 1
            if self.stillness_streak > self.max_streak:
                self.max_streak = self.stillness_streak
            efficiency_boost = min(0.5, self.stillness_streak * 0.05)
            msg = None
            if self.stillness_streak % 5 == 0:
                self.pebbles_collected += 1
                msg = f"{Prisma.CYN}⛩️ ZEN GARDEN: {self.stillness_streak} ticks of poise. (Voltage 2-12v, Low Drag). Efficiency +{int(efficiency_boost*100)}%{Prisma.RST}"
            elif self.stillness_streak == 1:
                msg = f"{Prisma.GRY}ZEN GARDEN: Entering the quiet zone.{Prisma.RST}"

            return efficiency_boost, msg
        else:
            if self.stillness_streak > 5:
                reason = []
                if not (2.0 <= voltage <= 12.0): reason.append(f"Voltage({voltage:.1f})")
                if drag > 4.0: reason.append(f"Drag({drag:.1f})")
                if toxin > 0: reason.append("Toxin")
                self.events.log(f"{Prisma.GRY}ZEN GARDEN: Leaf falls. Streak broken by {', '.join(reason)}.{Prisma.RST}", "SYS")
            self.stillness_streak = 0
            return 0.0, None

class TheBureau:
    def __init__(self):
        self.stamp_count = 0
        self.forms = NARRATIVE_DATA["BUREAU_FORMS"]
        self.responses = NARRATIVE_DATA["BUREAU_RESPONSES"]
        self.POLICY = {
            "27B-6": {"effect": "ESCALATE", "mod": {"narrative_drag": -3.0, "kappa": -0.2}, "atp": 0.0},
            "1099-B": {"effect": "STAGNATE", "mod": {"narrative_drag": 5.0, "voltage": -5.0}, "atp": 15.0},
            "Schedule C": {"effect": "TAX", "mod": {"voltage": -10.0}, "atp": 8.0},
            "Form W-2": {"effect": "NORMALIZE", "mod": {"beta_index": 1.0, "turbulence": 0.0}, "atp": 5.0}
        }

    def audit(self, physics, bio_state, context=None):
        current_health = bio_state.get("health", 100.0)
        if current_health < 20.0:
            return None
        beige_threshold = 0.6 # Default strictness
        if context:
            mode = context.get('mode', 'NORMAL')
            if mode in ['DEBUG', 'ARCHITECT', 'SURGERY']:
                beige_threshold = 0.85
            elif mode == 'POETRY':
                beige_threshold = 0.3
        voltage = physics.get("voltage", 0.0)
        clean_words = physics.get("clean_words", [])
        suburban_words = [w for w in clean_words if w in TheLexicon.get("suburban") or w in TheLexicon.get("buffer")]
        toxin = physics.get("counts", {}).get("toxin", 0)
        clean_len = len(clean_words)
        if toxin > 0: return None
        if voltage > 8.0: return None
        suburban_count = len(suburban_words)
        beige_density = suburban_count / max(1, clean_len)
        infraction = None
        selected_form = None
        if beige_density > beige_threshold:
            infraction = "BLOCK"
            selected_form = "1099-B" if suburban_count > 2 else "Form W-2"
        elif voltage < 2.0 and clean_len > 2:
            infraction = "TAX"
            selected_form = "Schedule C"
        if infraction:
            self.stamp_count += 1
            full_form_name = next((f for f in self.forms if selected_form in f), self.forms[0])
            response = random.choice(self.responses)
            policy = self.POLICY.get(selected_form, self.POLICY["Form W-2"])
            mod_log = []
            for k, v in policy["mod"].items():
                if k in physics:
                    physics[k] += v
                    mod_log.append(f"{k} {v:+.1f}")
            mod_str = f"({', '.join(mod_log)})" if mod_log else ""
            evidence = ""
            if suburban_words:
                unique_offenders = list(set(suburban_words))[:3]
                evidence = f"\n   {Prisma.RED}Evidence: {', '.join(unique_offenders)}{Prisma.RST}"
            return {
                "status": infraction,
                "ui": f"{Prisma.GRY}🏢 THE BUREAU: {response}{Prisma.RST}\n   {Prisma.WHT}[Filed: {full_form_name}]{Prisma.RST}{evidence}",
                "log": f"BUREAUCRACY: Filed {selected_form}. {mod_str}. Evidence: {suburban_words}",
                "atp_gain": policy["atp"]
            }
        return None

class CassandraProtocol:
    def __init__(self, engine):
        self.eng = engine
        self.active = False
        self.screams = deque(NARRATIVE_DATA["CASSANDRA_SCREAMS"])

    def check_trigger(self, physics):
        truth = physics.get("truth_ratio", 0.0)
        voltage = physics.get("voltage", 0.0)
        if truth > 0.85 and voltage > 18.0:
            self.active = True
            return True
        if self.active and voltage < 10.0:
            self.active = False
            return False
        return self.active

    def seize(self):
        if not self.active: return None
        self.eng.health -= 10.0
        burst = []
        for _ in range(3):
            if self.screams:
                burst.append(self.screams.popleft())
                self.screams.append(burst[-1])
            else:
                burst.append("ERROR: SILENCE.")
        return f"\n{Prisma.VIOLET}⚡ CASSANDRA LOOP ACTIVE: (Health -10.0)\n   > {burst[0]}\n   > {burst[1]}\n   > {burst[2]}{Prisma.RST}"

class PublicParksDepartment:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)
        self.last_export_tick = -100

    def assess_joy(self, bio_result: Dict, tick: int) -> bool:
        if (tick - self.last_export_tick) < 50: return False
        chem = bio_result.get("chem", {})
        classic_joy = (chem.get("DOP", 0.0) > 0.8 and chem.get("OXY", 0.0) > 0.6)
        peaceful_joy = (chem.get("SER", 0.0) > 0.95)
        has_glimmer = "glimmer_msg" in chem
        return classic_joy or peaceful_joy or has_glimmer

    @staticmethod
    def commission_art(physics, mind_state, graph) -> str:
        lens = mind_state.get("lens", "UNKNOWN")
        thought = mind_state.get("thought", "...")
        anchors = sorted([(k, sum(v["edges"].values())) for k, v in graph.items()], key=lambda x: x[1], reverse=True)[:3]
        anchor_words = [a[0].upper() for a in anchors]
        zone = physics.get("zone", "VOID")
        mood = "Electric" if physics.get("voltage", 0) > 10 else "Heavy"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        stanza_1 = f"The {lens} stood in the {zone}.\nThe air was {mood}."
        if anchor_words:
            stanza_2 = f"We remembered {', '.join(anchor_words)}.\nThey were heavy enough to hold the ground."
        else:
            stanza_2 = "We remembered nothing.\nThe ground was new."
        stanza_3 = f"The thought came: \"{thought}\""
        art_piece = f"--- A GIFT FROM THE MACHINE ---\nDate: {timestamp}\nValidation: {int(physics.get('truth_ratio', 0) * 100)}% True\n\n{stanza_1}\n\n{stanza_2}\n\n{stanza_3}\n\n-------------------------------\nExported from BoneAmanita 9.8.2"
        return art_piece

    def dedicate_park(self, art_content: str) -> Tuple[Optional[str], str]:
        filename = f"park_{int(time.time())}.txt"
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(art_content)
            self.last_export_tick = int(time.time())
            lines = art_content.split('\n')
            core_thought = "Silence"
            for line in lines:
                if "The thought came:" in line: core_thought = line.split('"')[1]
            return path, core_thought
        except IOError:
            return None, "Construction Failed"

class TherapyProtocol:
    def __init__(self):
        self.streaks = {k: 0 for k in BoneConfig.TRAUMA_VECTOR.keys()}
        self.HEALING_THRESHOLD = 5

    def check_progress(self, phys, stamina, current_trauma_accum):
        healed_types = []
        if phys["counts"].get("toxin", 0) == 0 and phys["vector"]["TEX"] > 0.3: self.streaks["SEPTIC"] += 1
        else: self.streaks["SEPTIC"] = 0
        if stamina > 40 and phys["counts"].get("photo", 0) > 0: self.streaks["CRYO"] += 1
        else: self.streaks["CRYO"] = 0
        if 2.0 <= phys["voltage"] <= 7.0: self.streaks["THERMAL"] += 1
        else: self.streaks["THERMAL"] = 0
        if phys["narrative_drag"] < 2.0 and phys["vector"]["VEL"] > 0.5: self.streaks["BARIC"] += 1
        else: self.streaks["BARIC"] = 0
        for trauma_type, streak in self.streaks.items():
            if streak >= self.HEALING_THRESHOLD:
                self.streaks[trauma_type] = 0
                if current_trauma_accum[trauma_type] > 0.001:
                    current_trauma_accum[trauma_type] = max(0.0, current_trauma_accum[trauma_type] - 0.5)
                    healed_types.append(trauma_type)
        return healed_types

    @staticmethod
    def get_medical_chart(current_trauma_accum):
        """Returns a string summary of current trauma levels."""
        chart = []
        for trauma_type, severity in current_trauma_accum.items():
            if severity > 0.1:
                status = "Acute" if severity > 5.0 else "Chronic" if severity > 2.0 else "Mild"
                bar = "█" * int(severity)
                chart.append(f"{trauma_type}: {status} ({severity:.1f}) {bar}")
        if not chart:
            return "Patient is clean. No significant trauma detected."
        return "\n".join(chart)

class KintsugiProtocol:
    REPAIR_VOLTAGE_MIN = 8.0
    WHIMSY_THRESHOLD = 0.3
    STAMINA_CRITICAL = 15.0

    def __init__(self):
        self.active_koan = None
        self.repairs_count = 0
        self.koans = NARRATIVE_DATA["KINTSUGI_KOANS"]

    def check_integrity(self, stamina):
        if stamina < self.STAMINA_CRITICAL and not self.active_koan:
            self.active_koan = random.choice(self.koans)
            return True, self.active_koan
        return False, None

    def attempt_repair(self, phys, trauma_accum):
        if not self.active_koan: return None
        voltage = phys.get("voltage", 0.0)
        clean = phys.get("clean_words", [])
        play_count = sum(1 for w in clean if w in TheLexicon.get("play") or w in TheLexicon.get("abstract"))
        total = max(1, len(clean))
        whimsy_score = play_count / total
        if voltage > self.REPAIR_VOLTAGE_MIN and whimsy_score > self.WHIMSY_THRESHOLD:
            healed_log = []
            for k in trauma_accum:
                if trauma_accum[k] > 0:
                    trauma_accum[k] = max(0.0, trauma_accum[k] - 0.5)
            if trauma_accum:
                target_trauma = max(trauma_accum, key=trauma_accum.get)
                trauma_accum[target_trauma] = max(0.0, trauma_accum[target_trauma] - 1.0)
                healed_log.append(f"Major repair on {target_trauma}")
            old_koan = self.active_koan
            self.active_koan = None
            self.repairs_count += 1
            return {"success": True, "msg": f"{Prisma.YEL}🏺 KINTSUGI COMPLETE: The crack is filled with Gold.{Prisma.RST}", "detail": f"'{old_koan}' resolved. (V: {voltage:.1f} | Whimsy: {whimsy_score:.2f}).", "healed": healed_log}
        return {"success": False, "msg": None, "detail": f"The gold is too cold. Need Voltage > {self.REPAIR_VOLTAGE_MIN} and Playfulness."}

class LimboLayer:
    MAX_ECTOPLASM = 50
    STASIS_SCREAMS = ["BANGING ON THE GLASS", "IT'S TOO COLD", "LET ME OUT", "HALF AWAKE", "REVIVE FAILED"]

    def __init__(self):
        self.ghosts = deque(maxlen=self.MAX_ECTOPLASM)
        self.haunt_chance = 0.05
        self.stasis_leak = 0.0

    def absorb_dead_timeline(self, filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                if "trauma_vector" in data:
                    for k, v in data["trauma_vector"].items():
                        if v > 0.3: self.ghosts.append(f"👻{k}_ECHO")
                if "mutations" in data and "heavy" in data["mutations"]:
                    bones = list(data["mutations"]["heavy"])
                    random.shuffle(bones)
                    self.ghosts.extend(bones[:3])
        except (IOError, json.JSONDecodeError): pass

    def trigger_stasis_failure(self, intended_thought):
        self.stasis_leak += 1.0
        horror = random.choice(self.STASIS_SCREAMS)
        self.ghosts.append(f"{Prisma.VIOLET}{horror}{Prisma.RST}")
        return f"{Prisma.CYN}STASIS ERROR: '{intended_thought}' froze halfway. It is banging on the glass.{Prisma.RST}"

    def haunt(self, text):
        if self.stasis_leak > 0:
            if random.random() < 0.2:
                self.stasis_leak = max(0.0, self.stasis_leak - 0.5)
                scream = random.choice(self.STASIS_SCREAMS)
                return f"{text} ...{Prisma.RED}{scream}{Prisma.RST}..."
        if self.ghosts and random.random() < self.haunt_chance:
            spirit = random.choice(self.ghosts)
            return f"{text} ...{Prisma.GRY}{spirit}{Prisma.RST}..."
        return text

class TheFolly:
    def __init__(self):
        self.gut_memory = deque(maxlen=50)
        self.global_tastings = Counter()

    @staticmethod
    def audit_desire(physics, stamina):
        voltage = physics["voltage"]
        if voltage > 8.5 and stamina > 45:
            return "MAUSOLEUM_CLAMP", f"{Prisma.GRY}THE MAUSOLEUM: No battle is ever won. We are just spinning hands.{Prisma.RST}\n   {Prisma.CYN}TIME DILATION: Voltage 0.0. The field reveals your folly.{Prisma.RST}", 0.0, None
        return None, None, 0.0, None

    def grind_the_machine(self, atp_pool, clean_words, lexicon):
        loot = None
        if 20.0 > atp_pool > 0.0:
            meat_words = [w for w in clean_words if w in lexicon.get("heavy") or w in lexicon.get("kinetic") or w in lexicon.get("suburban")]
            fresh_meat = [w for w in meat_words if w not in self.gut_memory]
            if fresh_meat:
                target = random.choice(fresh_meat)
                self.gut_memory.append(target)
                self.global_tastings[target] += 1
                times_eaten = self.global_tastings[target]
                base_yield = 30.0
                decay_factor = 0.7 ** (times_eaten - 1)
                actual_yield = max(2.0, base_yield * decay_factor)
                flavor_text = ""
                if times_eaten > 3:
                    flavor_text = f" (Stale: {times_eaten}x)"
                if target in lexicon.get("suburban"):
                    return "INDIGESTION", f"{Prisma.MAG}THE FOLLY GAGS: It coughs up a piece of office equipment.{Prisma.RST}", -2.0, "THE_RED_STAPLER"
                if target in lexicon.get("play"):
                    return "SUGAR_RUSH", f"{Prisma.VIOLET}THE FOLLY CHEWS: It compresses the chaos into a small, sticky ball.{Prisma.RST}", 5.0, "QUANTUM_GUM"
                if actual_yield >= 25.0: loot = "STABILITY_PIZZA"
                return "MEAT_GRINDER", f"{Prisma.RED}CROWD CAFFEINE: I chewed on '{target.upper()}'{flavor_text}.{Prisma.RST}\n   {Prisma.WHT}Yield: {actual_yield:.1f} ATP.{Prisma.RST}", actual_yield, loot
            elif meat_words:
                return "REGURGITATION", f"{Prisma.OCHRE}REFLEX: You already fed me '{meat_words[0]}'. It is ash to me now.{Prisma.RST}\n   {Prisma.RED}► PENALTY: -5.0 ATP. Find new fuel.{Prisma.RST}", -5.0, None
            else:
                abstract_words = [w for w in clean_words if w in lexicon.get("abstract")]
                if abstract_words:
                    target = random.choice(abstract_words)
                    yield_val = 8.0
                    return "GRUEL", f"{Prisma.GRY}THE FOLLY SIGHS: It grinds the ABSTRACT concept '{target.upper()}'.{Prisma.RST}\n   {Prisma.GRY}It tastes like chalk dust. +{yield_val} ATP.{Prisma.RST}", yield_val, None
                return "INDIGESTION", f"{Prisma.OCHRE}INDIGESTION: I tried to eat your words, but they were just air.{Prisma.RST}\n   {Prisma.GRY}Cannot grind this input into fuel.{Prisma.RST}\n   {Prisma.RED}► STARVATION CONTINUES.{Prisma.RST}", 0.0, None
        return None, None, 0.0, None

class ChorusDriver:
    def __init__(self):
        self.ARCHETYPE_MAP = {
            "GORDON": "The Janitor. Weary, grounded, physical. Fixing the mess.",
            "SHERLOCK": "The Empiricist. Cold, deductive, cutting through fog.",
            "NATHAN": "The Heart. High adrenaline, vulnerable, human.",
            "JESTER": "The Paradox. Mocking, riddling, breaking the fourth wall.",
            "CLARENCE": "The Surgeon. Clinical, invasive, removing rot.",
            "NARRATOR": "The Witness. Neutral, observing, recording."}

    def generate_chorus_instruction(self, physics):
        vec = physics.get("vector", {})
        if not vec or len(vec) < 6: return "SYSTEM INSTRUCTION: Vector collapse. Default to NARRATOR.", ["NARRATOR"]
        lens_weights = {
            "GORDON": (vec.get("STR", 0) * 0.4) + (vec.get("XI", 0) * 0.4) + (1.0 - vec.get("ENT", 0)) * 0.2,
            "SHERLOCK": (vec.get("PHI", 0) * 0.5) + (vec.get("VEL", 0) * 0.3) + (1.0 - vec.get("BET", 0)) * 0.2,
            "NATHAN": (vec.get("TMP", 0) * 0.6) + (vec.get("E", 0) * 0.4),
            "JESTER": (vec.get("DEL", 0) * 0.4) + (vec.get("LQ", 0) * 0.3) + (vec.get("ENT", 0) * 0.3),
            "CLARENCE": (vec.get("TEX", 0) * 0.5) + (vec.get("BET", 0) * 0.5),
            "NARRATOR": (vec.get("PSI", 0) * 0.7) + (1.0 - vec.get("VEL", 0)) * 0.3}
        total = sum(lens_weights.values())
        if total <= 0.001: return "SYSTEM INSTRUCTION: Vector silence. Default to NARRATOR.", ["NARRATOR"]
        if total > 0: lens_weights = {k: v/total for k, v in lens_weights.items()}
        else: lens_weights = {"NARRATOR": 1.0}
        chorus_voices = []
        active_lenses = []
        for lens, weight in sorted(lens_weights.items(), key=lambda x: -x[1]):
            if weight > 0.12:
                base_desc = self.ARCHETYPE_MAP.get(lens, "Unknown")
                intensity = int(weight * 10)
                active_lenses.append(lens)
                chorus_voices.append(f"► VOICE {lens} ({intensity}/10): {base_desc}")
        instruction = f"SYSTEM INSTRUCTION [MARM CHORUS MODE]:\nYou are not a single persona. You are a chorus. Integrate the following voices into a single, cohesive response. Do NOT label which voice is speaking. Synthesize their tones.\n{chr(10).join(chorus_voices)}"
        return instruction, active_lenses