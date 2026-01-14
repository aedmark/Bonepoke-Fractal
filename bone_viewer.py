# bone_view.py
# The Geodesic Viewport - Separation of Presentation and Logic

import time
from typing import Dict, List, Any
from dataclasses import dataclass

# Import Prisma from village for color support
from bone_village import Prisma, BoneConfig

class GeodesicRenderer:
    """
    The Viewport.
    Responsible for taking the raw 'CycleContext' and rendering
    it into a format the human eye can ingest without bleeding.
    """

    def __init__(self, engine_ref):
        self.eng = engine_ref
        self.projector = self.eng.projector
        self.vsl_chroma = self.eng.vsl_chroma
        self.strunk_white = self.eng.strunk_white

    def render_frame(self, ctx) -> Dict[str, Any]:
        """
        Compiles the final UI frame.
        """
        physics = ctx.physics
        mind = ctx.mind_state
        bio = ctx.bio_result
        world = ctx.world_state

        # 1. Generate the Dashboard (The HoloProjector)
        # We fetch the visual title from the Apeirogon resonance
        title_data = self._get_title_data(mind, physics, ctx.clean_words)
        
        raw_dashboard = self.projector.render(
            {"physics": physics},
            {
                "title": title_data,
                "health": self.eng.health,
                "stamina": self.eng.stamina,
                "bio": bio,
                "world": world
            },
            (mind.get("lens"), mind.get("thought"))
        )

        # 2. Apply Chromatic Aberration (VSL Color Theory)
        # Vectors change the color of the text to match the metaphysical "flavor"
        colored_ui = self.vsl_chroma.modulate(raw_dashboard, physics.get("vector", {}))

        # 3. Apply Strunk & White Style Policing
        # If the text is sloppy, the system sanitizes it.
        clean_ui, style_log = self.strunk_white.sanitize(colored_ui)
        
        # If style crimes were committed, we tax the user's dopamine
        if style_log:
            self._punish_style_crime(style_log)

        # 4. Handle VSL Ruptures (System Crashes rendered as UI)
        if physics.get("system_surge_event", False):
            clean_ui = self._inject_rupture_warning(clean_ui)

        # 5. Compose the Log Stream
        # Merging the internal event bus with the cycle logs
        structured_logs = self._compose_logs(ctx.logs, self.eng.events.flush())

        return {
            "type": "GEODESIC_FRAME",
            "ui": clean_ui,
            "logs": structured_logs,
            "metrics": self.eng._get_metrics(bio.get("atp", 0.0)),
            "system_instruction": self._get_chorus_instruction(physics)
        }

    def _get_title_data(self, mind, physics, clean_words):
        """Delegates to the Wise Mind for a title."""
        return self.eng.mind.wise.architect(
            {"physics": physics, "clean_words": clean_words},
            (mind.get("lens"), mind.get("thought"), mind.get("role")),
            False
        )

    def _punish_style_crime(self, log_msg):
        """Enforces the Strunk & White Protocol via punishment."""
        self.eng.events.log(log_msg, "SYS")
        self.eng.bio.endo.dopamine -= 0.05
        # Tax the Shimmer (The navigational fuel)
        self.eng.phys.nav.shimmer.spend(5.0) 
        
        # Record a friction event in short-term memory
        self.eng.mind.mem.short_term_buffer.append({
            "trigger": ["style_violation"],
            "context": "STRUNK_WHITE",
            "voltage": 0.0,
            "significance": 5.0,
            "timestamp": time.time()
        })

    def _inject_rupture_warning(self, ui_text):
        """Prepends a rupture warning if physics broke."""
        # Check if the VSL 32-Valve system detected a rupture
        rupture = self.eng.vsl_32v.analyze(self.eng.phys.tension.last_physics_packet)
        if rupture:
             return f"{rupture['log']}\n\n{ui_text}"
        return ui_text

    def _get_chorus_instruction(self, physics):
        """Checks if the Chorus Driver wants to speak."""
        if physics.get("kappa", 0) > 0.4:
            instr, active = self.eng.director.generate_chorus_instruction(physics)
            if active:
                self.eng.events.log(f"{Prisma.GRY}CHORUS ACTIVE: {', '.join(active)}{Prisma.RST}", "PSYCH")
                return instr
        return ""

    def _compose_logs(self, cycle_logs: List[str], bus_events: List[Dict]) -> List[str]:
        """
        Organizes the chaotic stream of consciousness into a tidy list.
        Schur Lens: "Like filing reports in the Parks Dept."
        """
        # 1. Convert simple strings to dicts
        all_events = [{"text": l, "category": "NARRATIVE"} for l in cycle_logs]
        all_events.extend(bus_events)

        if not all_events: return []

        # 2. Bucket Sort
        buckets = {"CRITICAL": [], "NARRATIVE": [], "CMD": [], "SYS": [], "BIO": [], "PSYCH": [], "OTHER": []}
        
        for e in all_events:
            cat = e.get("category", "OTHER").upper()
            if cat not in buckets: cat = "OTHER"
            
            # High priority overrides
            text = e.get("text", "")
            if "RUPTURE" in text or "DEATH" in text or "PANIC" in text: 
                cat = "CRITICAL"
                
            buckets[cat].append(text)
        
        # 3. Construct the Output
        composed = []
        
        # Critical stuff always comes first and loud
        if buckets["CRITICAL"]:
            composed.append(f"{Prisma.RED}--- CRITICAL ALERTS ---{Prisma.RST}")
            composed.extend(buckets["CRITICAL"])
            
        # Narrative is the "meat"
        if buckets["NARRATIVE"]:
            composed.extend(buckets["NARRATIVE"])
            
        # The "Noise" is compressed if verbose logging is off
        compressible = [
            ("CMD", Prisma.WHT, "COMMANDS"), 
            ("PSYCH", Prisma.VIOLET, "PSYCHOLOGY"), 
            ("BIO", Prisma.GRN, "BIOLOGY"), 
            ("SYS", Prisma.GRY, "SYSTEM"), 
            ("OTHER", Prisma.GRY, "MISC")
        ]
        
        for cat, color, label in compressible:
            items = buckets[cat]
            if not items: continue
            
            # Header
            composed.append(f"{Prisma.SLATE}   .{label} ({len(items)}){' ' * (30 - len(label))}{Prisma.RST}")
            
            # If verbose logging is OFF, we truncate heavy logs
            if len(items) > 4 and not BoneConfig.VERBOSE_LOGGING:
                composed.extend([f"   {i}" for i in items[:3]])
                composed.append(f"   {color}   ... and {len(items)-3} more.{Prisma.RST}")
            else:
                composed.extend([f"   {i}" for i in items])
                
        return composed
