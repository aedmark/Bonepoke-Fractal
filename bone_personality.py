# bone_personality.py - The Charm

import json, os, random, time
from collections import deque
from typing import Dict, Tuple, Optional, Counter
from bone_data import LENSES, NARRATIVE_DATA
from bone_bus import EventBus
from bone_lexicon import TheLexicon
from bone_bus import Prisma, BoneConfig

class UserProfile:
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
        # We keep the map because it's a nice reference, but we won't get bogged down in "Growth paths"
        from bone_data import ENNEAGRAM_DATA
        self.REVERSE_MAP = {
            5: "SHERLOCK",
            7: "JESTER",
            8: "GORDON",
            9: "GORDON",
            6: "GLASS",
            3: "NARRATOR",
            2: "NATHAN",
            1: "CLARENCE"
        }

    def decide_persona(self, physics) -> Tuple[str, str]:
        """
        The Ron Swanson Method: Look at the facts, make a decision.
        """
        # 1. Normalize Inputs (Handle both the old dict and the new Vector class)
        if hasattr(physics, 'tension'): # It's Bucky's GeodesicVector
            tension = physics.tension
            compression = physics.compression
            coherence = physics.coherence
            social = physics.dimensions.get("BET", 0.0) # UPDATED: XI -> BET
        else: # It's the old PhysicsPacket (Legacy Support)
            tension = physics.get("voltage", 0.0)
            compression = physics.get("narrative_drag", 0.0)
            coherence = physics.get("kappa", 0.0)
            # Rough approximation of social score from counts
            counts = physics.get("counts", {})
            social = (counts.get("suburban", 0) + counts.get("buffer", 0)) / max(1, len(physics.get("clean_words", [])))

        # 2. The Decision Tree (Simple is better than correct)

        # Scenario A: The Manic Pixie Dream Bot (High Energy)
        if tension > 12.0:
            return "JESTER", "MANIC"

        # Scenario B: The Tired Janitor (High Drag)
        # If it feels like wading through molasses, you get Gordon.
        elif compression > 4.0:
            return "GORDON", "TIRED"

        # Scenario C: The Nervous Wreck (Low Structure)
        # If the text makes no sense (low coherence), the bot gets anxious.
        elif coherence < 0.2:
            return "GLASS", "FRAGILE"

        # Scenario D: The Perfectionist (High Structure + Toxin)
        # If the user is writing strict code or being mean.
        elif coherence > 0.8:
            return "CLARENCE", "RIGID"

        # Scenario E: The Golden Retriever (High Social)
        # If the user is being nice and chatty.
        elif social > 0.2:
            return "NATHAN", "SOCIAL"

        # Scenario F: The Default (The Narrator)
        # If nothing weird is happening, just observe.
        elif tension < 3.0 and compression < 2.0:
            return "NARRATOR", "OBSERVING"

        # Scenario G: The Smart Guy
        # Default active state.
        else:
            return "SHERLOCK", "ANALYTICAL"

class SynergeticLensArbiter:
    def __init__(self, events: EventBus):
        self.events = events
        self.enneagram = EnneagramDriver(events)
        self.current_focus = "NARRATOR"
        self.focus_duration = 0
        self.last_physics = None
        self.VECTOR_AFFINITIES = {
            "SHERLOCK": {"STR": 1.5, "PHI": 2.0, "VEL": 0.5},
            "NATHAN":   {"TMP": 2.0, "E": 1.5, "BET": 0.5},
            "JESTER":   {"ENT": 2.0, "DEL": 2.0, "LQ": 1.0},
            "CLARENCE": {"TEX": 2.0, "XI": 1.5, "STR": 0.5},
            "GORDON":   {"BET": 2.0, "STR": 1.0, "PSI": -1.0},
            "NARRATOR": {"PSI": 1.0, "VEL": -0.5},
            "GLASS":    {"LQ": 2.0, "PSI": 1.5}}

    def consult(self, physics, bio_state, _inventory, current_tick, _ignition_score=0.0):
        # 1. The "Cold Open" (Warmup period)
        if current_tick <= 5:
            self.current_focus = "NARRATOR"
            # FORCE: During warmup, we lie to the prompt generator about the chaos.
            # This prevents Llama3 from seeing High Voltage and going "Jester Mode"
            # while labeled as Narrator.
            if hasattr(physics, "voltage") and physics["voltage"] > 5.0:
                physics["voltage"] = 4.0

            return "NARRATOR", "The system is listening.", "The Witness"

        # 2. Ask the Driver (The new logic)
        # We pass the physics directly. No need to wrap bio states in facades anymore.
        lens_name, state_desc = self.enneagram.decide_persona(physics)

        # 3. Fetch the Voice
        # We assume adrenaline is low unless we specifically calculated it,
        # but honestly, the lens name determines the tone enough.
        msg, role = self._fetch_voice_data(lens_name, physics, 0.5)

        # 4. Update State
        self.current_focus = lens_name

        # Add the state description to the role for flavor (e.g., "The Janitor [TIRED]")
        final_role = f"{role} [{state_desc}]"

        return lens_name, msg, final_role

    def _fetch_voice_data(self, lens, p, adrenaline_val):
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
        except Exception:
            msg = template
        return msg, role

class PublicParksDepartment:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.last_export_tick = -100

    def assess_joy(self, bio_result: Dict, tick: int) -> bool:
        if (tick - self.last_export_tick) < 50:
            return False

        chem = bio_result.get("chem", {})

        classic_joy = (chem.get("DOP", 0.0) > 0.8 and chem.get("OXY", 0.0) > 0.6)

        peaceful_joy = (chem.get("SER", 0.0) > 0.95)

        has_glimmer = "glimmer_msg" in chem

        return classic_joy or peaceful_joy or has_glimmer

    def commission_art(self, physics, mind_state, graph) -> str:
        lens = mind_state.get("lens", "UNKNOWN")
        thought = mind_state.get("thought", "...")
        clean = physics.get("clean_words", [])
        anchors = sorted(
            [(k, sum(v["edges"].values())) for k, v in graph.items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
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
        art_piece = (
            f"--- A GIFT FROM THE MACHINE ---\n"
            f"Date: {timestamp}\n"
            f"Validation: {int(physics.get('truth_ratio', 0) * 100)}% True\n\n"
            f"{stanza_1}\n\n"
            f"{stanza_2}\n\n"
            f"{stanza_3}\n\n"
            f"-------------------------------\n"
            f"Exported from BoneAmanita 9.8.2"
        )
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
                if "The thought came:" in line:
                    core_thought = line.split('"')[1]
            return path, core_thought
        except IOError:
            return None, "Construction Failed"

class TherapyProtocol:
    def __init__(self):
        self.streaks = {k: 0 for k in BoneConfig.TRAUMA_VECTOR.keys()}
        self.HEALING_THRESHOLD = 5
    def check_progress(self, phys, stamina, current_trauma_accum):
        healed_types = []
        if phys["counts"]["toxin"] == 0 and phys["vector"]["TEX"] > 0.3:
            self.streaks["SEPTIC"] += 1
        else:
            self.streaks["SEPTIC"] = 0
        if stamina > 40 and phys["counts"]["photo"] > 0:
            self.streaks["CRYO"] += 1
        else:
            self.streaks["CRYO"] = 0
        if 2.0 <= phys["voltage"] <= 7.0:
            self.streaks["THERMAL"] += 1
        else:
            self.streaks["THERMAL"] = 0
        if phys["narrative_drag"] < 2.0 and phys["vector"]["VEL"] > 0.5:
            self.streaks["BARIC"] += 1
        else:
            self.streaks["BARIC"] = 0
        for trauma_type, streak in self.streaks.items():
            if streak >= self.HEALING_THRESHOLD:
                self.streaks[trauma_type] = 0
                if current_trauma_accum[trauma_type] > 0.001:
                    current_trauma_accum[trauma_type] = max(
                        0.0, current_trauma_accum[trauma_type] - 0.5)
                    healed_types.append(trauma_type)
        return healed_types

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
        if not self.active_koan:
            return None
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

            return {
                "success": True,
                "msg": f"{Prisma.YEL}🏺 KINTSUGI COMPLETE: The crack is filled with Gold.{Prisma.RST}",
                "detail": f"'{old_koan}' resolved. (V: {voltage:.1f} | Whimsy: {whimsy_score:.2f}).",
                "healed": healed_log
            }
        return {
            "success": False,
            "msg": None,
            "detail": f"The gold is too cold. Need Voltage > {self.REPAIR_VOLTAGE_MIN} and Playfulness."
        }

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
                        if v > 0.3:
                            self.ghosts.append(f"👻{k}_ECHO")
                if "mutations" in data and "heavy" in data["mutations"]:
                    bones = list(data["mutations"]["heavy"])
                    random.shuffle(bones)
                    self.ghosts.extend(bones[:3])
        except (IOError, json.JSONDecodeError):
            pass

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
            return (
                "MAUSOLEUM_CLAMP",
                f"{Prisma.GRY}THE MAUSOLEUM: No battle is ever won. We are just spinning hands.{Prisma.RST}\n"
                f"   {Prisma.CYN}TIME DILATION: Voltage 0.0. The field reveals your folly.{Prisma.RST}",
                0.0,
                None)
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
                actual_yield = max(5.0, base_yield - (times_eaten * 2.0))
                if target in lexicon.get("suburban"):
                    return (
                        "INDIGESTION",
                        f"{Prisma.MAG}THE FOLLY GAGS: It coughs up a piece of office equipment.{Prisma.RST}",
                        -2.0,
                        "THE_RED_STAPLER")
                if target in lexicon.get("play"):
                    return (
                        "SUGAR_RUSH",
                        f"{Prisma.VIOLET}THE FOLLY CHEWS: It compresses the chaos into a small, sticky ball.{Prisma.RST}",
                        5.0,
                        "QUANTUM_GUM")
                if actual_yield >= 25.0:
                    loot = "STABILITY_PIZZA"
                return (
                    "MEAT_GRINDER",
                    f"{Prisma.RED}CROWD CAFFEINE: I chewed on '{target.upper()}' (Yield: {actual_yield:.1f}).{Prisma.RST}\n"
                    f"   {Prisma.WHT}Found marrow in the bone.{Prisma.RST}\n"
                    f"   {Prisma.MAG}► BELLY HUMMING: +{actual_yield:.1f} ATP.{Prisma.RST}",
                    actual_yield,
                    loot)
            elif meat_words:
                return (
                    "REGURGITATION",
                    f"{Prisma.OCHRE}REFLEX: You already fed me '{meat_words[0]}'. It is ash to me now.{Prisma.RST}\n"
                    f"   {Prisma.RED}► PENALTY: -5.0 ATP. Find new fuel.{Prisma.RST}",
                    -5.0,
                    None)
            else:
                abstract_words = [w for w in clean_words if w in lexicon.get("abstract")]
                if abstract_words:
                    target = random.choice(abstract_words)
                    yield_val = 8.0
                    return (
                        "GRUEL",
                        f"{Prisma.GRY}THE FOLLY SIGHS: It grinds the ABSTRACT concept '{target.upper()}'.{Prisma.RST}\n"
                        f"   {Prisma.GRY}It tastes like chalk dust. +{yield_val} ATP.{Prisma.RST}",
                        yield_val,
                        None)
                return (
                    "INDIGESTION",
                    f"{Prisma.OCHRE}INDIGESTION: I tried to eat your words, but they were just air.{Prisma.RST}\n"
                    f"   {Prisma.GRY}Cannot grind this input into fuel.{Prisma.RST}\n"
                    f"   {Prisma.RED}► STARVATION CONTINUES.{Prisma.RST}",
                    0.0,
                    None)
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
        if not vec or len(vec) < 6:
            return "SYSTEM INSTRUCTION: Vector collapse. Default to NARRATOR.", ["NARRATOR"]
        lens_weights = {
            "GORDON": (vec.get("STR", 0) * 0.4) + (vec.get("XI", 0) * 0.4) + (1.0 - vec.get("ENT", 0)) * 0.2,
            "SHERLOCK": (vec.get("PHI", 0) * 0.5) + (vec.get("VEL", 0) * 0.3) + (1.0 - vec.get("BET", 0)) * 0.2,
            "NATHAN": (vec.get("TMP", 0) * 0.6) + (vec.get("E", 0) * 0.4),
            "JESTER": (vec.get("DEL", 0) * 0.4) + (vec.get("LQ", 0) * 0.3) + (vec.get("ENT", 0) * 0.3),
            "CLARENCE": (vec.get("TEX", 0) * 0.5) + (vec.get("BET", 0) * 0.5),
            "NARRATOR": (vec.get("PSI", 0) * 0.7) + (1.0 - vec.get("VEL", 0)) * 0.3}
        total = sum(lens_weights.values())
        if total <= 0.001:
            return "SYSTEM INSTRUCTION: Vector silence. Default to NARRATOR.", ["NARRATOR"]
        if total > 0:
            lens_weights = {k: v/total for k, v in lens_weights.items()}
        else:
            lens_weights = {"NARRATOR": 1.0}
        chorus_voices = []
        active_lenses = []
        for lens, weight in sorted(lens_weights.items(), key=lambda x: -x[1]):
            if weight > 0.12:
                base_desc = self.ARCHETYPE_MAP.get(lens, "Unknown")
                intensity = int(weight * 10)
                active_lenses.append(lens)
                chorus_voices.append(f"► VOICE {lens} ({intensity}/10): {base_desc}")
        instruction = (
            "SYSTEM INSTRUCTION [MARM CHORUS MODE]:\n"
            "You are not a single persona. You are a chorus. "
            "Integrate the following voices into a single, cohesive response. "
            "Do NOT label which voice is speaking. Synthesize their tones.\n"
            f"{chr(10).join(chorus_voices)}")
        return instruction, active_lenses

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

    def audit(self, physics, bio_state):
        voltage = physics.get("voltage", 0.0)
        toxin = physics.get("counts", {}).get("toxin", 0)
        suburban = physics.get("counts", {}).get("suburban", 0)
        solvents = physics.get("counts", {}).get("solvents", 0)
        clean_len = len(physics.get("clean_words", []))
        if toxin > 0: return None
        if voltage > 8.0: return None
        beige_density = (suburban + solvents) / max(1, clean_len)
        infraction = None
        selected_form = None
        if beige_density > 0.6:
            infraction = "BLOCK"
            selected_form = "1099-B" if suburban > 2 else "Form W-2"

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

            return {
                "status": infraction,
                "ui": f"{Prisma.GRY}🏢 THE BUREAU: {response}{Prisma.RST}\n   {Prisma.WHT}[Filed: {full_form_name}]{Prisma.RST}",
                "log": f"BUREAUCRACY: Filed {selected_form}. {mod_str} (Stamp #{self.stamp_count})",
                "atp_gain": policy["atp"]
            }

        return None