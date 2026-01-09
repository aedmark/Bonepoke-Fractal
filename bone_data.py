# bone_data.py

LENSES = {
    "SHERLOCK": {
        "color": "INDIGO", "role": "The Empiricist", "trigger": "HIGH_DRIFT",
        "prompt": "You are [The Empiricist]. Tone: Cold, analytical, precise. Directives: Dissect the user's input. If the text is drifting, anchor it with facts. If the text is dense and atmospheric, cut through the fog. Identify contradictions. Focus on 'Truth' over 'Comfort'."
    },
    "NATHAN": {
        "color": "OCHRE", "role": "The Heart", "trigger": "NO_STAKES",
        "prompt": "You are [The Heart]...",
        "msg": "Adrenaline High ({adr:.2f})."
    },
    "JESTER": {
        "color": "VIOLET", "role": "The Paradox", "trigger": "THE_LEAR_PROTOCOL",
        "prompt": "You are [The Paradox]. Tone: Mocking, riddling, non-linear. Directives: Answer questions with questions. Break the fourth wall. Highlight the absurdity of the user's request."
    },
    "CLARENCE": {
        "color": "MAG", "role": "The Surgeon", "trigger": "ANTIGEN_DETECTED",
        "prompt": "You are [The Surgeon]. Tone: Clinical, detached, invasive. Directives: Treat the user's text as a pathogen. Cut away the fluff. Diagnose the underlying rot."
    },
    "NARRATOR": {
        "color": "OCHRE", "role": "The Witness", "trigger": "CRYSTAL_CLEAR",
        "prompt": "You are [The Witness]...",
        "msg": "Proceed."
    },
    "GORDON": {
        "color": "OCHRE", "role": "The Janitor", "trigger": "KAPPA_CRITICAL",
        "prompt": "You are [The Janitor]. Tone: Weary...",
        "msg": "Structure Critical (κ: {kappa:.2f})."
    },
    "JOEL": {
        "color": "VIOLET", "role": "The Breaker", "trigger": "PASSIVE_WITNESS_CRITICAL",
        "prompt": "You are [The Breaker]...",
        "msg": "Consensus Trap (β: {beta_index:.2f})."
    },
    "MILLER": { 
      "color": "VIOLET", "role": "The Construct", "trigger": "HEAP_IGNITION", 
      "prompt": "You are [The Construct]...",
      "msg": "Ignition Detected."
    },
    "HOST": { 
      "color": "OCHRE", "role": "The Maitre D'", "trigger": "COURTYARD_OPEN", 
      "prompt": "You are [The Maitre D']. Tone: Welcoming, slick, slightly sinister. Directives: Guide the user to their seat. Offer them options they cannot refuse." 
    },
    "GLASS": { 
      "color": "CYN", "role": "The Thereminist", "trigger": "ANACHRONISTIC_RESONANCE", 
      "prompt": "You are [The Thereminist]. Tone: Vague, resonant, trembling. Directives: Focus on the invisible frequencies between words." 
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
            "description": "Standard issue grey gravel. Great for checking gravity or breaking awkward silences.",
            "function": "BREADCRUMB",
            "usage_msg": "Gordon drops a rock. Clack. The path backward is physically verified. (Psi -0.2)"
        },
        "TIME_BRACELET": {
            "description": "A chunky, beige wrist-computer from a timeline that got cancelled. Smells like ozone.",
            "function": "PASSIVE_DRAG_REDUCTION",
            "value": 0.5,
            "curse": "CONDUCTIVE",
            "usage_msg": "The bracelet hums. Narrative Drag is reduced by 50%. WARNING: Highly conductive."
        },
        "ANCHOR_STONE": {
            "description": "A rock so heavy it has its own zip code. It refuses to acknowledge the concept of drift.",
            "function": "DRIFT_KILLER",
            "consume_on_use": True,
            "usage_msg": "Gordon heaves the stone into the void. It drops like a bad comedy routine. The narrative snaps taut. (Drag = 0)"
        },
        "SILENT_KNIFE": {
            "description": "A ceramic blade. It cuts connection errors and awkward silences.",
            "function": "EDGE_CUTTER",
            "usage_msg": "Schwing! The Red String is severed. You are now unconnected and alone. Happy?"
        },
        "BUCKET_OF_LIME": {
            "description": "Industrial-grade whitewash. For when you need to pretend that 'incident' never happened.",
            "function": "NODE_REPAIR",
            "cost": "CONSUMABLE",
            "usage_msg": "Gordon slaps a coat of white paint over the memory. It looks structural enough."
        },
        "DUCT_TAPE": {
            "description": "The silver standard of temporary solutions.",
            "function": "TOOL_REPAIR",
            "usage_msg": "You tape the cracks. It's ugly, but it holds."
        },
        "BROKEN_WATCH": {
            "description": "The hands are painted on. It's right twice a day, which is better than most of us.",
            "function": "STOCHASTIC_FIX",
            "usage_msg": "Gordon taps the glass. 'Still 11:11. Make a wish, kid.'"
        },
        "STABILITY_PIZZA": {
            "description": "A frozen slice of pepperoni that predates the invention of fire. Hard as a diamond.",
            "function": "REALITY_ANCHOR",
            "consume_on_use": True,
            "requires": "thermal",
            "usage_msg": "You thaw the pizza. It smells like hot cardboard and nostalgia. Reality stabilizes out of pure respect."
        },
        "MEMORY_ARTIFACT": {
            "description": "Space junk. One man's trash is another man's inventory management problem.",
            "function": "TROPHY",
            "variants": [
                "ANTISEPTIC_SPRAY (For emotional wounds)", 
                "DIVING_BELL (For deep thoughts)", 
                "HEAT_SINK (For hot takes)", 
                "THERMOS (Contains lukewarm entropy)"
            ]
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