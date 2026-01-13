import os
import sys
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
from PIL import Image, ImageDraw, ImageFont, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
        self.root.geometry("1100x900")
        
        self.let_f = resource_path("Orbitron-Bold.ttf")
        self.sym_f = resource_path("Orbitron-Bold.ttf")
        
        self.u_v, self.l_v, self.n_v, self.s_v = tk.IntVar(value=0), tk.IntVar(value=5), tk.IntVar(value=0), tk.IntVar(value=0)
        self.h_n = tk.IntVar(value=0)
        self.f_size = tk.IntVar(value=55) # New Font Size variable
        self.center_lower = tk.BooleanVar(value=False)
        self.show_grid = tk.BooleanVar(value=False)

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        left = tk.Frame(main, width=300)
        left.pack(side="left", fill="y", padx=10)
        
        tk.Label(left, text="Font Selection", font=("Arial", 10, "bold")).pack()
        tk.Button(left, text="Choose Letter Font", command=self.set_let).pack(fill="x")
        tk.Button(left, text="Choose Symbol Font", command=self.set_sym).pack(fill="x", pady=5)
        
        tk.Label(left, text="Font Settings", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(left, text="Global Font Size").pack()
        tk.Scale(left, from_=30, to=70, orient="horizontal", variable=self.f_size, command=lambda x: self.update_preview()).pack(fill="x")

        tk.Label(left, text="Vertical Nudges", font=("Arial", 10, "bold")).pack(pady=5)
        for lbl, var in [("Uppercase", self.u_v), ("Lowercase", self.l_v), ("Numbers", self.n_v), ("Symbols", self.s_v)]:
            tk.Label(left, text=lbl).pack()
            tk.Scale(left, from_=-30, to=30, orient="horizontal", variable=var, command=lambda x: self.update_preview()).pack(fill="x")

        tk.Label(left, text="Alignment", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Scale(left, from_=-20, to=20, orient="horizontal", variable=self.h_n, command=lambda x: self.update_preview()).pack(fill="x")
        tk.Checkbutton(left, text="Force Center Lowercase", variable=self.center_lower, command=self.update_preview).pack(anchor="w")
        tk.Checkbutton(left, text="Show Layout Grid", variable=self.show_grid, command=self.update_preview).pack(anchor="w")

        tk.Button(left, text="EXPORT DDS", bg="#34a853", fg="white", font=("Arial", 12, "bold"), height=2, command=self.export_dds).pack(fill="x", pady=20)
        
        tk.Frame(left).pack(expand=True, fill="both")
        tk.Button(left, text="About", command=self.show_about).pack(fill="x")

        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(right, bg="black", width=512, height=512)
        self.canvas.pack(pady=20)
        self.update_preview()

    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title("About BZFont Generator")
        about.geometry("450x450")
        container = tk.Frame(about, padx=20, pady=20)
        container.pack()
        tk.Label(container, text="Battlezone 98 Redux Font Generator", font=("Arial", 12, "bold")).pack()
        tk.Label(container, text="Credits: GrizzlyOne95", font=("Arial", 10, "italic")).pack(pady=(0, 10))
        tk.Label(container, text="Exports native 32-bit uncompressed DDS files.", wraplength=400, justify="left").pack()
        link = tk.Label(container, text="\nGitHub Repository", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/GrizzlyOne95/Battlezone98ReduxFontGenerator"))
        tk.Button(container, text="Close", command=about.destroy).pack(pady=20)

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
                messagebox.showinfo("Success", "DDS exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed: {e}")

    def set_let(self):
        f = filedialog.askopenfilename(filetypes=[("Fonts", "*.ttf *.otf")])
        if f: self.let_f = f; self.update_preview()

    def set_sym(self):
        f = filedialog.askopenfilename(filetypes=[("Fonts", "*.ttf *.otf")])
        if f: self.sym_f = f; self.update_preview()

if __name__ == "__main__":
    root = tk.Tk()
    app = BzoneApp(root)
    root.mainloop()