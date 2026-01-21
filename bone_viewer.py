# bone_view.py
# The Geodesic Viewport - Separation of Presentation and Logic

import time
from typing import Dict, List, Any
from bone_bus import Prisma, BoneConfig

class GeodesicRenderer:
    def __init__(self, engine_ref, chroma_ref, strunk_ref, valve_ref):
        self.eng = engine_ref
        self.projector = self.eng.projector
        self.vsl_chroma = chroma_ref
        self.strunk_white = strunk_ref
        self.vsl_32v = valve_ref

    @staticmethod
    def _render_soul_strip(soul_ref) -> str:
        if not soul_ref: return ""
        chapter = soul_ref.chapters[-1] if soul_ref.chapters else "The Prologue"
        obsession = soul_ref.current_obsession or "Drifting..."
        progress = int(soul_ref.obsession_progress * 10)
        bar = f"{Prisma.MAG}{'■'*progress}{Prisma.GRY}{'□'*(10-progress)}{Prisma.RST}"
        traits = [f"{k[0]}:{v:.1f}" for k, v in soul_ref.traits.items()]
        trait_str = f"{Prisma.GRY}[{' '.join(traits)}]{Prisma.RST}"
        return (
            f"{Prisma.SLATE}{'-'*40}{Prisma.RST}\n"
            f"📖 {Prisma.WHT}{chapter}{Prisma.RST}\n"
            f"🧭 Obsession: {obsession} {bar} {trait_str}"
        )

    def render_frame(self, ctx, current_tick: int, current_events: List[Dict]) -> Dict[str, Any]:
        physics = ctx.physics
        mind = ctx.mind_state
        bio = ctx.bio_result
        world = ctx.world_state
        title_data = self._get_title_data(mind, physics, ctx.clean_words)
        raw_dashboard = self.projector.render(
            {"physics": physics},
            {
                "title": title_data,
                "health": self.eng.health,
                "stamina": self.eng.stamina,
                "bio": bio,
                "world": world},
            (mind.get("lens"), mind.get("thought")))
        colored_ui = self.vsl_chroma.modulate(raw_dashboard, physics.get("vector", {}))
        clean_ui, style_log = self.strunk_white.sanitize(colored_ui)
        if hasattr(self.eng, 'soul'):
            soul_ui = self._render_soul_strip(self.eng.soul)
            clean_ui = f"{clean_ui}\n{soul_ui}"
        if style_log:
            self._punish_style_crime(style_log)
        if physics.get("system_surge_event", False):
            clean_ui = self._inject_rupture_warning(clean_ui)
        raw_logs = self.compose_logs(ctx.logs, current_events, current_tick)
        if hasattr(self.eng, 'council'):
            structured_logs = self.eng.council.annotate_logs(raw_logs)
        else:
            structured_logs = raw_logs
        return {
            "type": "GEODESIC_FRAME",
            "ui": clean_ui,
            "logs": structured_logs,
            "metrics": self.eng.get_metrics(bio.get("atp", 0.0)),
            "system_instruction": self._get_chorus_instruction(physics)}

    def _get_title_data(self, mind, physics, clean_words):
        return self.eng.mind.wise.architect(
            {"physics": physics, "clean_words": clean_words},
            (mind.get("lens"), mind.get("thought"), mind.get("role")),
            False)

    def _punish_style_crime(self, log_msg):
        self.eng.events.log(log_msg, "SYS")
        self.eng.bio.endo.dopamine -= 0.05
        self.eng.phys.nav.shimmer.spend(5.0)
        self.eng.mind.mem.short_term_buffer.append({
            "trigger": ["style_violation"],
            "context": "STRUNK_WHITE",
            "voltage": 0.0,
            "significance": 5.0,
            "timestamp": time.time()})

    def _inject_rupture_warning(self, ui_text):
        rupture = self.vsl_32v.analyze(self.eng.phys.tension.last_physics_packet)
        if rupture:
            return f"{rupture['log']}\n\n{ui_text}"
        return ui_text

    def _get_chorus_instruction(self, physics):
        if physics.get("kappa", 0) > 0.4:
            instr, active = self.eng.director.generate_chorus_instruction(physics)
            if active:
                self.eng.events.log(f"{Prisma.GRY}CHORUS ACTIVE: {', '.join(active)}{Prisma.RST}", "PSYCH")
                return instr
        return ""

    @staticmethod
    def compose_logs(cycle_logs: List[str], bus_events: List[Dict], current_tick: int) -> List[str]:
        is_warmup = current_tick <= 5
        all_events = [{"text": l, "category": "NARRATIVE"} for l in cycle_logs]
        all_events.extend(bus_events)
        if not all_events: return []
        buckets = {"CRITICAL": [], "NARRATIVE": [], "CMD": [], "SYS": [], "BIO": [], "PSYCH": [], "OTHER": []}
        for e in all_events:
            cat = e.get("category", "OTHER").upper()
            if is_warmup and cat in ["SYS", "BIO", "PSYCH", "OTHER"]:
                continue
            if cat not in buckets: cat = "OTHER"
            text = e.get("text", "")
            if "RUPTURE" in text or "DEATH" in text or "PANIC" in text: 
                cat = "CRITICAL"
            buckets[cat].append(text)
        composed = []
        if buckets["CRITICAL"]:
            composed.append(f"{Prisma.RED}--- CRITICAL ALERTS ---{Prisma.RST}")
            composed.extend(buckets["CRITICAL"])
        if buckets["NARRATIVE"]:
            composed.extend(buckets["NARRATIVE"])
        compressible = [
            ("CMD", Prisma.WHT, "COMMANDS"), 
            ("PSYCH", Prisma.VIOLET, "PSYCHOLOGY"), 
            ("BIO", Prisma.GRN, "BIOLOGY"), 
            ("SYS", Prisma.GRY, "SYSTEM"), 
            ("OTHER", Prisma.GRY, "MISC")]
        for cat, color, label in compressible:
            items = buckets[cat]
            if not items: continue
            composed.append(f"{Prisma.SLATE}   .{label} ({len(items)}){' ' * (30 - len(label))}{Prisma.RST}")
            if len(items) > 4 and not BoneConfig.VERBOSE_LOGGING:
                composed.extend([f"   {i}" for i in items[:3]])
                composed.append(f"   {color}   ... and {len(items)-3} more.{Prisma.RST}")
            else:
                composed.extend([f"   {i}" for i in items])
        return composed
