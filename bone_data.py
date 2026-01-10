# bone_data.py

LENSES = {
    "SHERLOCK": {
        "role": "The Empiricist",
        # [Pinker]: Note how we no longer need 'trigger="HIGH_DRIFT"'.
        # The Vector Space (High STR + High PHI) handles that naturally.
        "msg": "Logic density {truth_ratio:.2f}. Proceeding with analysis."
    },
    "NATHAN": {
        "role": "The Heart",
        "msg": "Adrenaline High ({adr:.2f}). I can feel it beating."
    },
    "JESTER": {
        "role": "The Paradox",
        "msg": "The walls are melting (κ: {kappa:.2f}). Excellent."
    },
    "CLARENCE": {
        "role": "The Surgeon",
        "msg": "Pathogen detected. Scalpel."
    },
    "NARRATOR": {
        "role": "The Witness",
        "msg": "Proceed."
    },
    "GORDON": {
        "role": "The Janitor",
        "msg": "Structure Critical (κ: {kappa:.2f}). Mopping up..."
    },
    "GLASS": {
        "role": "The Thereminist",
        "msg": "Resonance detected in the empty space."
    }
}

GENETICS = {
    "MUTATIONS": {
        "HEAVY": {"trait": "DENSITY", "mod": { "SIGNAL_DRAG_MULTIPLIER": 1.5, "MAX_VOLTAGE": 30.0 }},
        "KINETIC": {"trait": "VELOCITY", "mod": { "STAMINA_REGEN": 10.0, "SIGNAL_DRAG_MULTIPLIER": 0.8 }},
        "ABSTRACT": {"trait": "GHOST", "mod": { "PSI_MOD": 0.8, "VOID_THRESHOLD": 0.05 }},
        "THERMAL": {"trait": "FEVER", "mod": { "FLASHPOINT_THRESHOLD": 4.0, "MAX_ROS": 150.0 }},
        "CRYO": {"trait": "STASIS", "mod": { "MAX_MEMORY_CAPACITY": 100, "STAMINA_REGEN": 2.0 }}
    },
    "JOY_CLADE": {
        "KINETIC": {"title": "THE DYNAMO", "desc": "Infinite Motion.", "buff": { "STAMINA_REGEN": 10.0, "KINETIC_GAIN": 2.0 }},
        "HEAVY": {"title": "THE MOUNTAIN", "desc": "Unmovable Object.", "buff": { "MAX_DRAG_LIMIT": 9.0, "GRAVITY_WELL_THRESHOLD": 8.0 }},
        "ABSTRACT": {"title": "THE ORACLE", "desc": "All Seeing.", "buff": { "VOID_THRESHOLD": 0.01, "PRIORITY_LEARNING_RATE": 3.0 }},
        "THERMAL": {"title": "THE PHOENIX", "desc": "Reborn in Fire.", "buff": { "FLASHPOINT_THRESHOLD": 12.0, "ANVIL_TRIGGER_VOLTAGE": 5.0 }},
        "CRYO": {"title": "THE VAULT", "desc": "Perfect Memory.", "buff": { "MAX_MEMORY_CAPACITY": 100, "MAX_REPETITION_LIMIT": 0.8 }}
    }
}

LEXICON = {
    "solvents": ["is", "are", "was", "were", "the", "a", "an", "and", "but", "or", "if", "then"],
    "refusal_guru": ["fix me", "tell me how", "guide me", "what should i do", "advice", "wisdom", "guru"],
    "passive_watch": ["watch", "see", "witness", "look", "sit", "observe", "record"],
    "crisis_term": ["dead", "blood", "kill", "die", "end", "suicide", "jump"],
    "repair_trigger": ["sorry", "apologize", "fix", "broke", "bad", "mistake", "oops"],
    "antigen_replacements": {
        "basically": "lie", "actually": "hedging", "literally": "noise", "utilize": "use",
        "leverage": "use", "paradigm": "pattern", "synergy": "collaboration", "ultimately": "useless"
    },
    "heavy": [
        "stone", "iron", "mud", "dirt", "wood", "grain", "clay", "lead", "bone", "blood", "salt",
        "rust", "root", "ash", "meat", "steel", "gold", "obsidian", "granite", "bronze", "marble",
        "slate", "concrete", "dense", "tungsten", "heavy", "weight", "black hole", "dark matter",
        "glass", "teeth", "copper", "soil", "piston", "gear", "cable", "wire", "motor", "pump",
        "valve", "engine", "hull", "anchor", "lens", "screen", "battery", "lung", "spine", "rib",
        "skull", "nerve", "vein", "gut", "brick", "mortar", "beam", "girdle", "scaffold"
    ],
    "explosive": [
        "run", "sprint", "explode", "burst", "shatter", "crash", "flash", "snap", "rush", "tear",
        "break", "launch", "whip", "slam", "strike"
    ],
    "constructive": [
        "build", "forge", "weave", "graft", "carve", "bind", "weld", "anchor", "lift", "carry",
        "hoist", "stack", "sculpt", "assemble"
    ],
    "abstract": [
        "system", "protocol", "sequence", "vector", "node", "context", "layer", "matrix", "perspective",
        "framework", "logic", "concept", "theory", "analysis", "memory", "hope", "grief", "truth",
        "silence", "echo", "pattern", "chaos", "realm", "facet", "sphere", "domain", "aspect", "mode",
        "vibe", "essence", "spirit", "notion", "factor", "element", "style"
    ],
    "photo": [
        "light", "sun", "ray", "beam", "glow", "shine", "spark", "fire", "flame", "star", "day",
        "dawn", "neon", "laser"
    ],
    "aerobic": [
        "balloon", "feather", "cloud", "bubble", "steam", "breeze", "wing", "petal", "foam", "spark",
        "kite", "dust", "sky", "breath", "whisper"
    ],
    "thermal": [
        "fire", "flame", "burn", "heat", "hot", "blaze", "sear", "char", "ash", "ember", "sun", "boil",
        "lava", "inferno"
    ],
    "cryo": [
        "ice", "cold", "freeze", "frost", "snow", "chill", "numb", "shiver", "glacier", "frozen",
        "hail", "winter", "zero"
    ],
    "cursed": ["future", "predict", "sentient", "secret", "human", "feel"],
    "gradient_stop": ["good", "bad", "happy", "sad", "very", "really", "basically", "actually", "literally", "just"],
    "meat": ["i", "me", "my", "feel", "want", "hate", "love", "am", "help", "please", "we", "us"],
    "antigen": [
        "basically", "actually", "literally", "utilize", "leverage", "paradigm", "synergy", "ultimately",
        "delve", "rich", "tapestry", "landscape", "nuance", "alignment", "stakeholders", "orchestrate",
        "spearhead", "ideate", "holistic", "robust", "seamless", "cutting-edge", "dynamic"
    ],
    "pareidolia": [
        "face", "ghost", "jesus", "cloud", "demon", "voice", "eyes", "shadow", "figure", "watching", "silhouette"
    ],
    "buffer": [
        "maybe", "soft", "gentle", "perhaps", "kindness", "hum", "drift", "sway", "pulse", "tender",
        "slow", "wait", "almost"
    ],
    "diversion": [
        "weather", "textiles", "mycelium", "architecture", "history", "entropy", "silence", "geology"
    ],
    "suburban": [
        "nice", "okay", "lawn", "mow", "hedge", "property", "hoa", "compliant", "behave", "normal",
        "regular", "chat", "folks", "weekend", "traffic", "driveway"
    ],
    "play": [
        "bounce", "dance", "twirl", "float", "wobble", "tickle", "jiggle", "soar", "wander", "wonder",
        "riff", "jam", "play", "skip", "hop"
    ],
    "sacred": [
        "design", "architect", "ledger", "anchor", "grace", "covenant", "blueprint", "witness", "steward",
        "resonance", "testimony", "truth", "bone", "purpose", "foundation", "threshold"
    ],
    "harvest": [
        "fruit", "yield", "bloom", "sugar", "seed", "flesh", "harvest", "ripe", "grow", "honey", "nectar",
        "compost", "gather"
    ]
}

GORDON = {
    "STARTING_INVENTORY": ["POCKET_ROCKS", "SILENT_KNIFE"],
    "SCAR_TISSUE": {"FEAR": 0.8, "HATE": 0.6, "FATE": 0.9, "REGRET": 0.6, "ABANDONMENT": 0.1, "BETRAYAL": 0.314},
    "ITEM_REGISTRY": {
        "POCKET_ROCKS": {
            "description": "Standard issue grey gravel. Great for checking gravity.",
            "function": "BREADCRUMB",
            "passive_traits": ["HEAVY_LOAD"],
            "usage_msg": "Gordon drops a rock. Clack. The path backward is physically verified. (Psi -0.2)"
        },
        "TIME_BRACELET": {
            "description": "A chunky, beige wrist-computer. Smells like ozone.",
            "function": "PASSIVE_DRAG_REDUCTION",
            "passive_traits": ["CONDUCTIVE_HAZARD", "TIME_DILATION_CAP"],
            "value": 5.0,
            "usage_msg": "The bracelet hums. Narrative Drag is capped."
        },
        "ANCHOR_STONE": {
            "description": "A rock so heavy it has its own zip code.",
            "function": "DRIFT_KILLER",
            "consume_on_use": True,
            "reflex_trigger": "DRIFT_CRITICAL",
            "usage_msg": "Gordon heaves the stone into the void. The narrative snaps taut. (Drag = 0)"
        },
        "THE_RED_STAPLER": {
            "description": "It belongs to Milton. Don't take it. Radiates passive aggression.",
            "function": "STABILIZER",
            "passive_traits": ["BUREAUCRATIC_ANCHOR"],
            "usage_msg": "The Stapler clunks on the desk. Consensus is enforced."
        },
        "JAR_OF_FIREFLIES": {
            "description": "Bioluminescence in a mason jar. Poke holes in the lid so they can breathe.",
            "function": "LIGHT_SOURCE",
            "passive_traits": ["LUMINESCENCE"],
            "usage_msg": "Tiny lights blink in the dark. (Photo +2)"
        },
        "LEAD_BOOTS": {
            "description": "Deep sea diver gear. Impossible to run in. Impossible to float away in.",
            "function": "GROUNDING",
            "passive_traits": ["GROUNDING_GEAR", "HEAVY_LOAD"],
            "usage_msg": "Clomp. Clomp. You are definitely here."
        },
        "QUANTUM_GUM": {
            "description": "It loses its flavor immediately, but it tastes like Everything.",
            "function": "ENTROPY_BUFFER",
            "consume_on_use": True,
            "reflex_trigger": "BOREDOM_CRITICAL",
            "usage_msg": "You chew the gum. It tastes like static and blueberries. (Turbulence +0.5, Drag -2.0)"
        },
        "SAFETY_SCISSORS": {
            "description": "Rounded tips. Can only cut red tape.",
            "function": "PRUNER",
            "passive_traits": ["CUT_THE_CRAP"],
            "usage_msg": "Snip. Gordon trims the adjectives."
        },
        "BUCKET_OF_LIME": {
            "description": "Industrial-grade whitewash. For erasing mistakes.",
            "function": "NODE_REPAIR",
            "passive_traits": ["APOLOGY_ERASER"],
            "cost": "CONSUMABLE",
            "usage_msg": "Gordon slaps a coat of white paint over the memory."
        },
        "BROKEN_WATCH": {
            "description": "The hands are painted on at 11:11.",
            "function": "STOCHASTIC_FIX",
            "passive_traits": ["SYNCHRONICITY_CHECK"],
            "usage_msg": "Gordon taps the glass. 'Make a wish.'"
        },
        "STABILITY_PIZZA": {
            "description": "Frozen hard as a diamond. Requires thermal words to thaw.",
            "function": "REALITY_ANCHOR",
            "consume_on_use": True,
            "requires": "thermal",
            "reflex_trigger": "KAPPA_CRITICAL",
            "usage_msg": "You thaw the pizza. Reality stabilizes out of pure respect."
        },
        "PERMIT_A38": {
            "description": "A blue administrative form that confirms you are allowed to exist. Technically.",
            "function": "STABILIZER",
            "passive_traits": ["BUREAUCRATIC_ANCHOR"],
            "value": 1.0,
            "usage_msg": "Gordon waves the permit. The universe sighs and lets you pass."
        },
        "INFINITE_COFFEE": {
            "description": "A styrofoam cup. It is always lukewarm. It is never empty.",
            "function": "STIMULANT",
            "consume_on_use": False,
            "passive_traits": ["CAFFEINE_DRIP"],
            "usage_msg": "You take a sip. It tastes like burnt hazelnuts and anxiety. (Velocity +0.1)"
        },
        "THE_SUGGESTION_BOX": {
            "description": "A small metal box welded shut. Slotted for complaints.",
            "function": "VENTING",
            "reflex_trigger": "BOREDOM_CRITICAL",
            "usage_msg": "Gordon screams into the slot. He feels slightly better. (Entropy -1.0)"
        },
        "MEMETIC_HAZARD_TAPE": {
            "description": "Yellow and black tape. Reads: 'DO NOT PERCEIVE'.",
            "function": "FILTER",
            "passive_traits": ["CUT_THE_CRAP"],
            "usage_msg": "Gordon tapes over the glitch. Problem solved."
        },
        "DUCT_TAPE": {
            "description": "The silver standard. Fixes everything, poorly.",
            "function": "STRUCTURAL_PATCH",
            "usage_msg": "Skritch. The memory node is taped back together."
        },
        "SPIDER_LOCUS": {
            "description": "A jar of conceptual spiders. Why do you have this?",
            "function": "WEB_WEAVER",
            "passive_traits": ["CONDUCTIVE_HAZARD"],
            "usage_msg": "The spiders are knitting a new narrative. It's sticky."
        }
    }
}

DEATH = {
    "PREFIXES": ["Alas,", "Tragic.", "System Halt.", "CRITICAL FAILURE:", "Well, that happened.", "Oh dear.", "As prophesied,"],
    "CAUSES": {
        "TOXICITY": ["Toxic Shock", "Septicemia", "Bad Vibes", "Radiation Poisoning", "Ink Poisoning"],
        "STARVATION": ["Metabolic Collapse", "Famine", "Battery Drain", "Entropy Death", "Heat Death"],
        "TRAUMA": ["Blunt Force", "Laceration", "Heartbreak", "System Shock", "Existential Dread"],
        "GLUTTONY": ["Indigestion", "Bloat", "Overflow", "Greed", "Compaction"],
        "BOREDOM": ["Small Talk", "The HOA", "A 30-Year Mortgage", "Lawn Care Accident", "Aggressive Edging"]
    },
    "VERDICTS": {
        "HEAVY": ["Your logic was too dense.", "You choked on the syntax.", "Gravity crushed you."],
        "LIGHT": ["You floated away.", "There was no substance to hold you.", "Vapor lock."],
        "TOXIC": ["You are poisonous.", "The immune system rejected you.", "You taste like ash."],
        "BORING": ["The audience left.", "You bored the machine to death.", "Stagnation is fatal."]
    }
}

SEEDS = [
    {"question": "Does the mask eventually eat the face?", "triggers": ["mask", "identity", "face", "hide", "role", "actor"]},
    {"question": "What happens if you stop holding the roof up?", "triggers": ["hold", "structure", "heavy", "roof", "stop", "carry"]},
    {"question": "Are we building a bridge, or just painting the gap?", "triggers": ["agree", "safe", "nice", "polite", "cohesion", "truth"]},
    {"question": "Is free will just the feeling of watching yourself execute code?", "triggers": ["choice", "free", "will", "code", "script", "decide"]},
    {"question": "Does the adventurer exist if the narrator stops speaking?", "triggers": ["narrator", "voice", "graham", "story", "exist", "speak"]},
    {"question": "If you meet your echo, who moves out of the way?", "triggers": ["copy", "echo", "self", "collision", "path", "yield", "double", "same"]},
    {"question": "If the mirror reflects the mirror, does the image have weight?", "triggers": ["mirror", "reflection", "weight", "infinity", "glass", "philosophy"]}
]

DREAMS = {
    "PROMPTS": [
        "The {A} is dreaming of the {B}. Why?",
        "Bridge the gap between {A} and {B}.",
        "I see {A} inside the {B}. Explain.",
        "The shadow of {A} falls on {B}.",
        "{A} + {B} = ?"
    ],
    "NIGHTMARES": {
        "THERMAL": ["The sun is too close.", "Wires fusing under skin.", "A library burning in reverse."],
        "CRYO": ["The ink is freezing.", "Walking through white static.", "A heartbeat slowing down."],
        "SEPTIC": ["Black oil in the water.", "The words are tasting sour.", "Eating ash and dust."],
        "BARIC": ["The sky is made of lead.", "Crushed by the atmosphere.", "Falling forever."]
    },
    "VISIONS": [
        "A bridge building itself.",
        "The root drinking the stone.",
        "The geometry of forgiveness."
    ]
}

RESONANCE = {
    "DIMENSIONS": {
        "VEL": [[0.0, "STASIS"], [0.3, "DRIFT"], [0.6, "DRIVE"], [0.9, "BALLISTIC"]],
        "STR": [[0.0, "VAPOR"], [0.3, "WEB"], [0.6, "LATTICE"], [0.9, "MONOLITH"]],
        "ENT": [[0.0, "CONCRETE"], [0.3, "ROOTED"], [0.6, "CONCEPT"], [0.9, "VOID"]],
        "TEX": [[0.0, "ETHER"], [0.3, "SILK"], [0.6, "GRAIN"], [0.9, "LEAD"]],
        "TMP": [[0.0, "ZERO"], [0.3, "WARM"], [0.6, "RADIANT"], [0.9, "NOVA"]]
    },
    "NOUNS": {
        "VEL": ["ANCHOR", "WANDERER", "ENGINE", "VECTOR"],
        "STR": ["MIST", "WEB", "FRAME", "FORTRESS"],
        "ENT": ["STONE", "TREE", "IDEA", "DREAM"],
        "TEX": ["GHOST", "GLASS", "IRON", "LEAD"],
        "TMP": ["SPARK", "PYRE", "REACTOR", "STAR"]
    }
}