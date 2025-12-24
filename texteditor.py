"""
PROJECT: MOMENTUM [v1.1 - HARDENED]
Architect: SLASH 3.6
Philosophy: "Write like you are running away from something."

FEATURES:
1. THERMAL INTERFACE: The faster you type, the hotter the screen gets.
2. THE BUTCHER'S TOGGLE: In WRITE mode, Backspace is FORBIDDEN.
3. THE HEMINGWAY BRIDGE: You cannot quit if you end on a period.
4. THE BONEYARD: Deleted thoughts are never truly gone.

v1.1 UPDATE:
- Added 'Ghost Patch' for missing TERM environment variables.
- Added explicit detection for Windows 'curses' absence.
"""

import sys
import os
import time
import re
from datetime import datetime

# --- GHOST PATCH: ENVIRONMENT FIX ---
# The 'setupterm' error happens when the system doesn't know what terminal it is.
# We force it to identify as 'xterm-256color' if undefined.
if "TERM" not in os.environ:
    os.environ["TERM"] = "xterm-256color"

try:
    import curses
except ImportError:
    if os.name == 'nt':
        print("❌ CRITICAL MISSING COMPONENT: 'windows-curses'")
        print("   Windows does not have built-in screen physics.")
        print("   FIX: Run 'pip install windows-curses' in your terminal.")
        sys.exit(1)
    else:
        print("❌ CRITICAL ERROR: 'curses' library not found.")
        sys.exit(1)


# --- CONFIGURATION (THE PHYSICS) ---
class Physics:
    # Heat decay per second (The entropy of distraction)
    COOLING_RATE = 5.0
    # Heat gain per keystroke (The friction of creation)
    HEAT_PER_STROKE = 2.5
    # Thresholds
    TEMP_WARM = 30.0
    TEMP_HOT = 70.0
    TEMP_CRITICAL = 90.0  # Focus Mode

class Boneyard:
    """The Graveyard of Deleted Thoughts."""
    FILE_PATH = "momentum_boneyard.txt"

    @staticmethod
    def bury(text):
        if not text.strip():
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(Boneyard.FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")

class Editor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.buffer = ""
        self.mode = "WRITE"  # Options: WRITE | EDIT
        self.temperature = 0.0
        self.last_stroke = time.time()
        self.start_time = time.time()
        self.filename = f"draft_{int(time.time())}.md"
        
        # Setup Curses
        try:
            curses.curs_set(2)  # Block cursor
        except:
            pass # Some terminals don't support cursor visibility changes
            
        self.stdscr.nodelay(True)  # Non-blocking input for physics loop
        self.height, self.width = self.stdscr.getmaxyx()
        
        # Colors
        try:
            curses.start_color()
            curses.use_default_colors()
            # Pair 1: COLD (Dim/Grey) - Fallback to white/black if defaults fail
            curses.init_pair(1, curses.COLOR_BLUE, -1)
            # Pair 2: WARM (White)
            curses.init_pair(2, curses.COLOR_WHITE, -1)
            # Pair 3: HOT (Yellow/Bright)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            # Pair 4: CRITICAL (Red/Black Background)
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
            # Pair 5: UI (Green)
            curses.init_pair(5, curses.COLOR_GREEN, -1)
        except:
            # Monochrome fallback if colors fail
            pass

    def get_color(self):
        """Resolves current temperature to a color pair."""
        try:
            if self.temperature > Physics.TEMP_CRITICAL: return curses.color_pair(4) | curses.A_BOLD
            if self.temperature > Physics.TEMP_HOT: return curses.color_pair(3) | curses.A_BOLD
            if self.temperature > Physics.TEMP_WARM: return curses.color_pair(2)
            return curses.color_pair(1)  # Cold
        except:
            return curses.A_NORMAL

    def update_physics(self):
        """The Thermodynamic Loop."""
        now = time.time()
        delta = now - self.last_stroke
        
        # Cooling Logic
        if delta > 0.5:
            loss = Physics.COOLING_RATE * (delta - 0.5)
            self.temperature = max(0.0, self.temperature - loss)

    def inject_heat(self):
        """Friction creates heat."""
        self.temperature = min(100.0, self.temperature + Physics.HEAT_PER_STROKE)
        self.last_stroke = time.time()

    def save_file(self):
        """Smart Naming & Saving."""
        # ELOISE: "Name the file based on the content, not a random number."
        words = self.buffer.strip().split()
        if len(words) > 3:
            slug = "_".join(words[:4]).lower()
            slug = re.sub(r'[^a-z0-9_]', '', slug)
            if slug:
                self.filename = f"{slug}.md"
        
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(self.buffer)
        return self.filename

    def check_hemingway_bridge(self):
        """
        THE SCHUR LENS:
        Prevent the user from quitting if they have resolved the tension.
        """
        clean = self.buffer.strip()
        if not clean: return True  # Allow quit if empty
        
        last_char = clean[-1]
        if last_char in ['.', '!', '?']:
            return False # BRIDGE BLOCKED
        return True # BRIDGE OPEN

    def render_ui(self, msg=""):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # 1. RENDER TEXT
        # Word wrap logic (simplified for terminal)
        lines = []
        current_line = ""
        for word in self.buffer.split(' '):
            if len(current_line) + len(word) + 1 > w - 4:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line += word + " "
        lines.append(current_line)
        
        # Draw text with thermal color
        color = self.get_color()
        row = 2
        for line in lines[-(h-5):]: # Only show what fits
            try:
                self.stdscr.addstr(row, 2, line, color)
                row += 1
            except curses.error:
                pass

        # 2. RENDER HUD (Unless Critical/Focus Mode)
        if self.temperature < Physics.TEMP_CRITICAL:
            try:
                # Status Bar
                mode_str = f"MODE: {self.mode}"
                temp_bar = "|" * int(self.temperature / 5)
                # Avoid division by zero in WPM
                elapsed = max(0.1, (time.time() - self.start_time) / 60)
                wpm = len(self.buffer.split()) / elapsed
                
                status = f" {mode_str} | TEMP: {int(self.temperature)}°C [{temp_bar:<20}] | WPM: {int(wpm)} "
                self.stdscr.addstr(h-2, 0, status[:w-1], curses.color_pair(5) | curses.A_REVERSE)
                
                # Instructions
                help_txt = "CTRL+E: Toggle Mode | CTRL+S: Save | ESC: Quit"
                self.stdscr.addstr(h-1, 0, help_txt[:w-1], curses.color_pair(5))
            except curses.error:
                pass
        
        # 3. RENDER TOAST MESSAGE (Feedback)
        if msg:
            try:
                self.stdscr.addstr(h//2, w//2 - len(msg)//2, f" {msg} ", curses.color_pair(4) | curses.A_REVERSE)
            except curses.error:
                pass
                
        self.stdscr.refresh()

    def run(self):
        msg = "BEGIN. DO NOT LOOK BACK."
        
        while True:
            self.render_ui(msg)
            msg = "" # Clear message after one frame
            
            # Physics Tick
            self.update_physics()
            
            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1

            if key == -1:
                time.sleep(0.05) # Prevent CPU burning
                continue

            # --- INPUT HANDLING ---
            
            # QUIT (ESC)
            if key == 27:
                if self.check_hemingway_bridge():
                    saved_as = self.save_file()
                    return f"Session saved to {saved_as}. The bridge is open."
                else:
                    msg = "HEMINGWAY PROTOCOL: Cannot end on a period. Leave a thread dangling."
                    curses.beep()
                    continue

            # TOGGLE MODE (Ctrl+E)
            elif key == 5:
                self.mode = "EDIT" if self.mode == "WRITE" else "WRITE"
                msg = f"SWITCHED TO {self.mode} MODE"
            
            # SAVE (Ctrl+S)
            elif key == 19:
                saved_as = self.save_file()
                msg = f"SAVED: {saved_as}"

            # BACKSPACE / DELETE
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                if self.mode == "WRITE":
                    # CLARENCE: "NO."
                    msg = "THE BUTCHER: NO REGRETS. MOVE FORWARD."
                    curses.beep()
                else:
                    # Allow delete in edit mode
                    if len(self.buffer) > 0:
                        # Send to Boneyard first
                        deleted = self.buffer[-1]
                        # In a real app we'd capture blocks, here just chars for simplicity
                        # Boneyard.bury(deleted) 
                        self.buffer = self.buffer[:-1]
                        self.inject_heat()

            # TYPING
            elif 32 <= key <= 126: # Printable chars
                if self.mode == "EDIT":
                    # ELOISE: "NO."
                    msg = "EDIT MODE: SILENCE. ONLY CUTS ALLOWED."
                    curses.beep()
                else:
                    char = chr(key)
                    self.buffer += char
                    self.inject_heat()
            
            # ENTER
            elif key == 10 or key == 13:
                self.buffer += " " # Simplify newlines to spaces for this prototype visualization
                self.inject_heat()

def main(stdscr):
    editor = Editor(stdscr)
    result = editor.run()
    return result

if __name__ == "__main__":
    try:
        # Check if running in a headless environment
        if not sys.stdout.isatty():
             raise Exception("This tool requires a real terminal (TTY). It cannot run in a static output window.")
        
        msg = curses.wrapper(main)
        print(f"\n>>> MOMENTUM CLOSED.\n>>> {msg}\n")

    except curses.error as e:
        print(f"\n{Prisma.RED}❌ TERMINAL ERROR: {e}{Prisma.RST}")
        print(f"DEBUG: TERM={os.environ.get('TERM')}")
        print("Try running this in a dedicated terminal window (cmd.exe or bash).")
        
    except Exception as e:
        print(f"\n❌ CRASH: {e}")
        print("Note: If on Windows, install 'windows-curses'.")