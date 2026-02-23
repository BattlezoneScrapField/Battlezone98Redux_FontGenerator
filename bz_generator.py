import os
import sys
import struct
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import ctypes
from PIL import Image, ImageDraw, ImageFont, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ToolTip:
    def __init__(self, widget, text, bg="#1a1a1a", fg="#00ffff"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                       background=self.bg, foreground=self.fg, 
                       relief='solid', borderwidth=1, font=("Consolas", "9"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def draw_custom_caret(draw, x, y, w, h, color=(255, 255, 255, 255)):
    padding_x = w * 0.25
    top_y = y + (h * 0.3)
    bottom_y = y + (h * 0.6)
    left_x = x + padding_x
    right_x = x + w - padding_x
    mid_x = x + (w / 2)
    draw.line([(left_x, bottom_y), (mid_x, top_y)], fill=color, width=4)
    draw.line([(mid_x, top_y), (right_x, bottom_y)], fill=color, width=4)

def generate_sheet_image(let_f, sym_f, u_v, l_v, n_v, s_v, h_nudge, f_size, center_lower, show_grid):
    width, height = 1024, 1024
    work_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(work_layer)
    
    row1_y, row2_y = 13, 93
    row3_upper_y, row3_lower_y = 173, 187
    row4_alpha_y, row4_symbol_y = 266, 254 

    manual_data = {
        "!": (28, 16, 62), "\"": (43, 35, 62), "#": (80, 41, 62), "$": (128, 41, 62),
        "%": (176, 41, 62), "&": (225, 41, 62), "'": (270, 23, 62), "(": (295, 32, 62),
        ")": (322, 32, 62), "*": (358, 45, 62), "+": (405, 45, 62), ",": (452, 25, 62),
        "-": (482, 34, 62), ".": (525, 13, 62), "/": (543, 42, 62), "0": (591, 42, 62),
        "1": (638, 42, 62), "2": (685, 42, 62), "3": (734, 42, 62), "4": (783, 42, 62),
        "5": (832, 42, 62), "6": (877, 42, 62), "7": (931, 42, 62), "8": (975, 42, 62),
        "9": (0, 42, 62), ":": (43, 17, 62), ";": (60, 17, 62), "<": (79, 27, 62),
        "=": (108, 48, 62), ">": (157, 32, 62), "?": (188, 48, 61), "@": (239, 48, 61),
        "A": (284, 48, 61), "B": (332, 48, 61), "C": (380, 48, 61), "D": (427, 48, 61),
        "E": (477, 48, 61), "F": (523, 48, 61), "G": (572, 48, 61), "H": (620, 48, 61),
        "I": (665, 23, 61), "J": (686, 47, 61), "K": (734, 47, 61), "L": (779, 47, 61),
        "M": (829, 47, 61), "N": (878, 47, 61), "O": (926, 47, 61), "P": (972, 47, 61),
        "Q": (0, 47, 61), "R": (44, 47, 61), "S": (93, 47, 61), "T": (141, 47, 61),
        "U": (187, 47, 61), "V": (236, 47, 61), "W": (285, 47, 61), "X": (333, 47, 61),
        "Y": (381, 47, 61), "Z": (428, 47, 61), "[": (477, 31, 61), "\\": (511, 42, 61),
        "]": (558, 28, 61), "^": (592, 41, 61), "_": (639, 48, 61), "`": (688, 21, 61),
        "a": (709, 46, 49), "b": (756, 46, 49), "c": (807, 46, 49), "d": (854, 46, 49),
        "e": (902, 46, 49), "f": (949, 46, 49),
        "g": (0, 46, 49), "h": (46, 46, 49), "i": (92, 17, 49), "j": (110, 44, 49),
        "k": (160, 44, 49), "l": (207, 44, 49), "m": (254, 44, 49), "n": (300, 44, 49),
        "o": (350, 44, 49), "p": (397, 44, 49), "q": (446, 44, 49), "r": (493, 44, 49),
        "s": (542, 44, 49), "t": (590, 44, 49), "u": (640, 44, 49), "v": (685, 44, 49),
        "w": (734, 44, 49), "x": (781, 44, 49), "y": (831, 44, 49), "z": (878, 44, 49),
        "{": (927, 29, 60), "|": (955, 20, 60), "}": (974, 29, 60)
    }
    
    rows_data = ["!\"#$%&'()*+,-./012345678", "9:;<=>?@ABCDEFGHIJKLMNOP", "QRSTUVWXYZ[\\\\]^_abcdef`", "ghijklmnopqrstuvwxyz{|}~"]

    for r_idx, row_text in enumerate(rows_data):
        for char in row_text:
            if char not in manual_data: continue
            x_base, target_w, target_h = manual_data[char]
            
            y_base = row1_y if r_idx == 0 else row2_y if r_idx == 1 else \
                     (row3_lower_y if char in "abcdef" else row3_upper_y) if r_idx == 2 else \
                     (row4_symbol_y if char in "{|}" else row4_alpha_y)

            v_val = u_v if char.isupper() else l_v if char.islower() else n_v if char.isdigit() else s_v

            if show_grid:
                draw.rectangle([x_base, y_base, x_base + target_w, y_base + target_h], outline=(0, 255, 255, 120))

            if char == "^":
                draw_custom_caret(draw, x_base + h_nudge, y_base - v_val, target_w, target_h)
                continue

            font_path = let_f if char.isalpha() else sym_f
            try: font = ImageFont.truetype(font_path, f_size)
            except: font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), char, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            # Center horizontally within the slot
            draw_x = (x_base + (target_w - text_w) // 2 - bbox[0]) + h_nudge
            
            # Handle descenders for lowercase 'j', 'g', 'p', 'q', 'y'
            if char.islower() and not center_lower and char not in "{|}~":
                draw_y = (y_base + target_h - text_h - bbox[1]) - v_val
            else:
                draw_y = (y_base + (target_h - text_h) // 2 - bbox[1]) - v_val

            draw.text((draw_x, draw_y), char, fill=(255, 255, 255, 255), font=font)

    preview_bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    preview_bg.paste(work_layer, (0, 0), work_layer)
    return preview_bg, work_layer

def save_as_dds_native(image, filename):
    width, height = image.size
    with open(filename, 'wb') as f:
        f.write(b'DDS ')
        f.write(struct.pack('<IIIIIII', 124, 0x1 + 0x2 + 0x4 + 0x8 + 0x1000, height, width, width * 4, 0, 0))
        f.write(b'\x00' * 44) 
        f.write(struct.pack('<IIIIIIII', 32, 0x41, 0, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000))
        f.write(struct.pack('<IIIII', 0x1000, 0, 0, 0, 0))
        f.write(image.tobytes())

class BzoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BZ98 Redux Font Generator")
        self.root.geometry("1100x950")
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', False) else sys._MEIPASS
        self.profiles_dir = os.path.join(os.path.abspath("."), "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Colors
        self.colors = {
            "bg": "#0a0a0a", "fg": "#d4d4d4",
            "highlight": "#00ff00", "dark_highlight": "#004400", "accent": "#00ffff"
        }
        
        self.load_custom_fonts()
        
        # Settings Variables
        self.let_f = resource_path("Orbitron-Bold.ttf")
        self.sym_f = resource_path("Orbitron-Bold.ttf")
        self.u_v, self.l_v, self.n_v, self.s_v = tk.IntVar(value=0), tk.IntVar(value=5), tk.IntVar(value=0), tk.IntVar(value=0)
        self.h_n = tk.IntVar(value=0)
        self.f_size = tk.IntVar(value=55)
        self.center_lower = tk.BooleanVar(value=False)
        self.show_grid = tk.BooleanVar(value=False)

        self.setup_styles()
        self.setup_ui()
        
        self.root.configure(bg=self.colors["bg"])
        self.log("Application Initialized.")

    def load_custom_fonts(self):
        self.current_font = "Segoe UI"
        font_path = os.path.join(os.path.abspath("."), "BZONE.ttf")
        if os.path.exists(font_path):
            try:
                if ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0) > 0:
                    self.current_font = "BZONE"
                    self.log("Loaded BZONE.ttf for UI.")
            except: pass

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        c = self.colors
        main_font = (self.current_font, 10)
        bold_font = (self.current_font, 11, "bold")
        
        style.configure(".", background=c["bg"], foreground=c["fg"], font=main_font)
        style.configure("TFrame", background=c["bg"])
        style.configure("TLabelframe", background=c["bg"], bordercolor=c["highlight"])
        style.configure("TLabelframe.Label", background=c["bg"], foreground=c["highlight"], font=bold_font)
        style.configure("TLabel", background=c["bg"], foreground=c["fg"])
        style.configure("TButton", background="#1a1a1a", foreground=c["fg"])
        style.map("TButton", background=[("active", c["dark_highlight"])], foreground=[("active", c["highlight"])])
        style.configure("Success.TButton", foreground=c["highlight"], font=bold_font)
        style.configure("TCheckbutton", background=c["bg"], foreground=c["fg"])
        style.map("TCheckbutton", background=[("active", c["bg"])])

    def setup_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)
        
        # --- HEADER ---
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 20))
        h_label = tk.Label(header, text="FONT GENERATOR", font=(self.current_font, 24, "bold"), 
                         background=self.colors["bg"], foreground=self.colors["highlight"])
        h_label.pack(side="left")
        
        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)
        
        # LEFT PANEL
        left = ttk.Frame(content, width=350)
        left.pack(side="left", fill="y", padx=(0, 10))
        
        # Profiles Section
        prof_frame = ttk.LabelFrame(left, text=" PROFILE ", padding=10)
        prof_frame.pack(fill="x", pady=(0, 10))
        ttk.Button(prof_frame, text="LOAD PROFILE", command=self.load_profile).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(prof_frame, text="SAVE PROFILE", command=self.save_profile).pack(side="left", fill="x", expand=True, padx=2)

        # Font Selection
        sel_frame = ttk.LabelFrame(left, text=" FONT SELECTION ", padding=10)
        sel_frame.pack(fill="x", pady=(0, 10))
        b1 = ttk.Button(sel_frame, text="CHOOSE LETTER FONT", command=self.set_let)
        b1.pack(fill="x")
        ToolTip(b1, "Select the TTF/OTF font for Alpha characters.")
        
        b2 = ttk.Button(sel_frame, text="CHOOSE SYMBOL FONT", command=self.set_sym)
        b2.pack(fill="x", pady=5)
        ToolTip(b2, "Select the TTF/OTF font for Symbols and Numbers.")

        # Font Settings
        set_frame = ttk.LabelFrame(left, text=" FONT SETTINGS ", padding=10)
        set_frame.pack(fill="x")
        ttk.Label(set_frame, text="Global Font Size").pack()
        s_size = tk.Scale(set_frame, from_=30, to=70, orient="horizontal", variable=self.f_size, 
                         bg=self.colors["bg"], fg=self.colors["fg"], highlightthickness=0,
                         command=lambda x: self.update_preview())
        s_size.pack(fill="x")

        # Vertical Nudges
        nudge_frame = ttk.LabelFrame(left, text=" VERTICAL NUDGES ", padding=10)
        nudge_frame.pack(fill="x", pady=10)
        for lbl, var in [("Uppercase", self.u_v), ("Lowercase", self.l_v), ("Numbers", self.n_v), ("Symbols", self.s_v)]:
            ttk.Label(nudge_frame, text=lbl).pack()
            tk.Scale(nudge_frame, from_=-30, to=30, orient="horizontal", variable=var, 
                    bg=self.colors["bg"], fg=self.colors["fg"], highlightthickness=0,
                    command=lambda x: self.update_preview()).pack(fill="x")
        
        # Presets (New Feature)
        preset_frame = ttk.Frame(nudge_frame)
        preset_frame.pack(fill="x", pady=5)
        ttk.Label(preset_frame, text="Presets:").pack(side="left")
        p1 = ttk.Button(preset_frame, text="Reset", width=6, command=lambda: self.apply_preset(0, 0, 0, 0))
        p1.pack(side="left", padx=2)
        p2 = ttk.Button(preset_frame, text="Abt-Up", width=6, command=lambda: self.apply_preset(-5, -5, -5, -5))
        p2.pack(side="left", padx=2)
        p3 = ttk.Button(preset_frame, text="Abt-Dn", width=6, command=lambda: self.apply_preset(5, 5, 5, 5))
        p3.pack(side="left", padx=2)

        # Alignment
        align_frame = ttk.LabelFrame(left, text=" ALIGNMENT & VIEW ", padding=10)
        align_frame.pack(fill="x")
        ttk.Label(align_frame, text="Horizontal Shift").pack()
        tk.Scale(align_frame, from_=-20, to=20, orient="horizontal", variable=self.h_n, 
                bg=self.colors["bg"], fg=self.colors["fg"], highlightthickness=0,
                command=lambda x: self.update_preview()).pack(fill="x")
        ttk.Checkbutton(align_frame, text="Force Center Lowercase", variable=self.center_lower, command=self.update_preview).pack(anchor="w")
        ttk.Checkbutton(align_frame, text="Show Layout Grid", variable=self.show_grid, command=self.update_preview).pack(anchor="w")

        exp_btn = ttk.Button(left, text="EXPORT DDS", style="Success.TButton", command=self.export_dds)
        exp_btn.pack(fill="x", pady=20, ipady=10)
        
        ttk.Button(left, text="About", command=self.show_about).pack(side="bottom", fill="x")

        # RIGHT PANEL (Preview & Logs)
        right = ttk.Frame(content)
        right.pack(side="right", fill="both", expand=True)
        
        # Canvas Container for centering
        canvas_container = tk.Frame(right, bg="#000")
        canvas_container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_container, bg="black", width=512, height=512, highlightthickness=1, highlightbackground=self.colors["dark_highlight"])
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        
        # Log Box
        self.log_box = tk.Text(right, height=10, state="disabled", bg="#050505", fg=self.colors["fg"], font=("Consolas", 9))
        self.log_box.pack(fill="x", side="bottom", pady=(10, 0))
        
        self.update_preview()

    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def apply_preset(self, u, l, n, s):
        self.u_v.set(u)
        self.l_v.set(l)
        self.n_v.set(n)
        self.s_v.set(s)
        self.update_preview()
        self.log(f"Applied preset: {u}, {l}, {n}, {s}")

    def save_profile(self):
        f = filedialog.asksaveasfilename(initialdir=self.profiles_dir, defaultextension=".json", filetypes=[("Profile", "*.json")])
        if not f: return
        data = {
            "u_v": self.u_v.get(), "l_v": self.l_v.get(), "n_v": self.n_v.get(), "s_v": self.s_v.get(),
            "h_n": self.h_n.get(), "f_size": self.f_size.get(),
            "center_lower": self.center_lower.get(),
            "let_f": self.let_f, "sym_f": self.sym_f
        }
        try:
            with open(f, 'w') as outfile: json.dump(data, outfile, indent=4)
            self.log(f"Profile saved: {os.path.basename(f)}")
        except Exception as e: messagebox.showerror("Error", f"Failed to save profile: {e}")

    def load_profile(self):
        f = filedialog.askopenfilename(initialdir=self.profiles_dir, filetypes=[("Profile", "*.json")])
        if not f: return
        try:
            with open(f, 'r') as infile:
                data = json.load(infile)
                self.u_v.set(data.get("u_v", 0))
                self.l_v.set(data.get("l_v", 5))
                self.n_v.set(data.get("n_v", 0))
                self.s_v.set(data.get("s_v", 0))
                self.h_n.set(data.get("h_n", 0))
                self.f_size.set(data.get("f_size", 55))
                self.center_lower.set(data.get("center_lower", False))
                self.let_f = data.get("let_f", self.let_f)
                self.sym_f = data.get("sym_f", self.sym_f)
            self.update_preview()
            self.log(f"Profile loaded: {os.path.basename(f)}")
        except Exception as e: messagebox.showerror("Error", f"Failed to load profile: {e}")

    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title("About BZFont Generator")
        about.geometry("450x450")
        about.configure(bg=self.colors["bg"])
        container = tk.Frame(about, padx=20, pady=20, bg=self.colors["bg"])
        container.pack()
        tk.Label(container, text="Battlezone 98 Redux Font Generator", font=(self.current_font, 12, "bold"), bg=self.colors["bg"], fg=self.colors["highlight"]).pack()
        tk.Label(container, text="Credits: GrizzlyOne95", font=(self.current_font, 10, "italic"), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=(0, 10))
        tk.Label(container, text="Exports native 32-bit uncompressed DDS files.", wraplength=400, justify="left", bg=self.colors["bg"], fg=self.colors["fg"]).pack()
        link = tk.Label(container, text="\nGitHub Repository", fg=self.colors["accent"], cursor="hand2", font=(self.current_font, 10, "underline"), bg=self.colors["bg"])
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/GrizzlyOne95/Battlezone98ReduxFontGenerator"))
        ttk.Button(container, text="Close", command=about.destroy).pack(pady=20)

    def update_preview(self):
        final_img, _ = generate_sheet_image(self.let_f, self.sym_f, self.u_v.get(), self.l_v.get(), 
                                            self.n_v.get(), self.s_v.get(), self.h_n.get(), 
                                            self.f_size.get(),
                                            self.center_lower.get(), self.show_grid.get())
        prev = final_img.resize((512, 512), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(prev)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def export_dds(self):
        _, export_img = generate_sheet_image(self.let_f, self.sym_f, self.u_v.get(), self.l_v.get(), 
                                             self.n_v.get(), self.s_v.get(), self.h_n.get(), 
                                             self.f_size.get(),
                                             self.center_lower.get(), False)
        f_path = filedialog.asksaveasfilename(defaultextension=".dds", initialfile="bzfont.dds", filetypes=[("DDS", "*.dds")])
        if f_path:
            try:
                save_as_dds_native(export_img, f_path)
                self.log(f"Exported DDS: {os.path.basename(f_path)}")
                messagebox.showinfo("Success", "DDS exported successfully!")
            except Exception as e:
                self.log(f"Export Error: {e}")
                messagebox.showerror("Export Error", f"Failed: {e}")

    def set_let(self):
        f = filedialog.askopenfilename(filetypes=[("Fonts", "*.ttf *.otf")])
        if f: 
            self.let_f = f
            self.update_preview()
            self.log(f"Letter Font updated: {os.path.basename(f)}")

    def set_sym(self):
        f = filedialog.askopenfilename(filetypes=[("Fonts", "*.ttf *.otf")])
        if f: 
            self.sym_f = f
            self.update_preview()
            self.log(f"Symbol Font updated: {os.path.basename(f)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BzoneApp(root)
    root.mainloop()
