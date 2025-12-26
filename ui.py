import tkinter as tk
from tkinter import messagebox
import auth
import notes
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller onefile."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Notes")
        self.root.geometry("800x500")

        self.username = None
        self.show_password = False
        self.dark_mode = False

        # Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")

        self.build_login()

    # ---------------- LOGIN UI ----------------
    def build_login(self):
        self.clear()
        self.root.configure(bg="white")

        tk.Label(self.root, text="Safe Notes", font=("Arial", 20, "bold"), bg="white").pack(pady=15)

        tk.Label(self.root, text="Username", bg="white").pack()
        self.user_entry = tk.Entry(self.root, width=30)
        self.user_entry.pack()
        self.user_entry.bind("<Return>", self.focus_password)

        tk.Label(self.root, text="Password", bg="white").pack()

        frame = tk.Frame(self.root, bg="white")
        frame.pack()

        self.pass_entry = tk.Entry(frame, show="*", width=25)
        self.pass_entry.pack(side="left")
        self.pass_entry.bind("<Return>", self.login)

        self.toggle_btn = tk.Button(frame, text="👁", command=self.toggle_password)
        self.toggle_btn.pack(side="left", padx=5)

        tk.Button(self.root, text="Login / Register", command=self.login).pack(pady=10)

    def focus_password(self, event):
        self.pass_entry.focus_set()

    def toggle_password(self):
        if self.show_password:
            self.pass_entry.config(show="*")
            self.toggle_btn.config(text="👁")
        else:
            self.pass_entry.config(show="")
            self.toggle_btn.config(text="🙈")
        self.show_password = not self.show_password

    def login(self, event=None):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return
        if auth.user_exists(username):
            if not auth.verify_user(username, password):
                messagebox.showerror("Error", "Wrong password")
                return
        else:
            auth.register_user(username, password)

        self.username = username
        self.build_notes_ui()

    # ---------------- NOTES UI ----------------
    def build_notes_ui(self):
        self.clear()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # LEFT PANEL
        self.left_frame = tk.Frame(self.main_frame, width=200)
        self.left_frame.pack(side="left", fill="y")

        tk.Label(self.left_frame, text="Your Notes", font=("Arial", 12, "bold")).pack(pady=5)
        self.notes_list = tk.Listbox(self.left_frame)
        self.notes_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.notes_list.bind("<<ListboxSelect>>", self.load_note)

        # Dark mode toggle at bottom
        self.theme_btn = tk.Button(self.left_frame, text="🌙 Dark Mode", command=self.toggle_theme)
        self.theme_btn.pack(side="bottom", pady=10)

        # RIGHT PANEL
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Top bar for title and logout
        top_bar = tk.Frame(self.right_frame)
        top_bar.pack(fill="x", pady=5)

        self.title_entry = tk.Entry(top_bar, font=("Arial", 14), fg="gray")
        self.title_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.title_entry.insert(0, "Enter note title...")
        self.title_entry.bind("<FocusIn>", self.clear_title_placeholder)
        self.title_entry.bind("<FocusOut>", self.add_title_placeholder)

        tk.Button(top_bar, text="Logout", command=self.logout).pack(side="right")

        # Text area for note content
        self.text_area = tk.Text(self.right_frame, wrap="word", fg="gray")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=5)
        self.text_area.insert("1.0", "Write your note here...")
        self.text_area.bind("<FocusIn>", self.clear_text_placeholder)
        self.text_area.bind("<FocusOut>", self.add_text_placeholder)

        # Save & Delete buttons
        btn_frame = tk.Frame(self.right_frame)
        btn_frame.pack(fill="x", pady=5, padx=10)
        tk.Button(btn_frame, text="💾 Save", command=self.save_note).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑 Delete", command=self.delete_note).pack(side="left", padx=5)

        self.refresh_notes()
        self.apply_theme()

    # ---------------- THEME ----------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg = "#1e1e1e"
            fg = "white"
            box = "#2b2b2b"
            self.theme_btn.config(text="☀ Light Mode")
        else:
            bg = "white"
            fg = "black"
            box = "white"
            self.theme_btn.config(text="🌙 Dark Mode")

        self.root.configure(bg=bg)
        self.left_frame.configure(bg=bg)
        self.right_frame.configure(bg=bg)

        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

        self.notes_list.configure(bg=box, fg=fg)
        self.text_area.configure(bg=box, fg=fg)
        self.title_entry.configure(bg=box, fg=fg)

    # ---------------- PLACEHOLDERS ----------------
    def clear_title_placeholder(self, event):
        if self.title_entry.get() == "Enter note title...":
            self.title_entry.delete(0, tk.END)
            self.title_entry.config(fg="black")

    def add_title_placeholder(self, event):
        if not self.title_entry.get():
            self.title_entry.insert(0, "Enter note title...")
            self.title_entry.config(fg="gray")

    def clear_text_placeholder(self, event):
        if self.text_area.get("1.0", tk.END).strip() == "Write your note here...":
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg="black")

    def add_text_placeholder(self, event):
        if not self.text_area.get("1.0", tk.END).strip():
            self.text_area.insert("1.0", "Write your note here...")
            self.text_area.config(fg="gray")

    # ---------------- NOTES LOGIC ----------------
    def refresh_notes(self):
        self.notes_list.delete(0, tk.END)
        self.user_notes = notes.get_user_notes(self.username)
        for note in self.user_notes:
            self.notes_list.insert(tk.END, note["title"])

    def save_note(self):
        title = self.title_entry.get()
        content = self.text_area.get("1.0", tk.END)
        if title == "Enter note title..." or not title.strip():
            messagebox.showerror("Error", "Title required")
            return
        notes.add_note(self.username, title, content)
        self.refresh_notes()

    def load_note(self, event):
        if not self.notes_list.curselection():
            return
        note = self.user_notes[self.notes_list.curselection()[0]]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note["title"])
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", note["content"])

    def delete_note(self):
        if not self.notes_list.curselection():
            return
        notes.delete_note(self.username, self.notes_list.curselection()[0])
        self.refresh_notes()

    # ---------------- LOGOUT ----------------
    def logout(self):
        self.username = None
        self.build_login()

    # ---------------- UTILITY ----------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
