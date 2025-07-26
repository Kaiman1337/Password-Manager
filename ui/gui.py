import tkinter as tk
from tkinter import messagebox
from core import (
    get_fernet,
    verify_master_password,
    store_master_hash,
    load_data,
    save_data,
    gen_pass
)

# Theme constants
BG_COLOR = "#141517"
LABEL_FG_COLOR = "#EEE"
FONT = ("Consolas", 12)
PASS_GEN_FONT = ("Consolas", 10)
TITLE_FONT = ("Consolas", 16, "bold")
BTN_COLOR = "#2a2a2a"
BTN_ACTIVE = "#333"
ENTRY_BG = "#1e1e1e"


class PasswordManagerUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        self.geometry("1280x720")
        self.minsize(800, 400)
        self.configure(bg=BG_COLOR)

        self.fernet = None
        self.data = None

        self.sidebar = None
        self.main_content = None

        # Center the window on the screen
        self.update_idletasks()  # Ensure size is calculated
        width = 1280
        height = 720
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.show_unlock_panel()

    def show_unlock_panel(self):
        self.clear_window()

        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(pady=(160, 0))

        title = tk.Label(
            frame,
            text="Enter Master Password",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=TITLE_FONT
        )
        title.pack(pady=20)

        self.master_entry = tk.Entry(
            frame,
            show='*',
            font=FONT,
            width=30,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            insertbackground=LABEL_FG_COLOR,
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.master_entry.bind("<Return>", lambda event: self.try_unlock())
        self.master_entry.pack(pady=10)
        self.master_entry.focus()

        unlock_btn = tk.Button(
            frame,
            text="Unlock",
            command=self.try_unlock,
            bg=BTN_COLOR,
            activebackground=BTN_ACTIVE,
            fg=LABEL_FG_COLOR,
            font=FONT,
            border=0,
            padx=10,
            pady=5
        )
        unlock_btn.pack(pady=20)

    def try_unlock(self):
        password = self.master_entry.get()

        if not password:
            messagebox.showwarning(
                "Input Error", "Please enter the master password.")
            return

        if not verify_master_password(password):
            if messagebox.askyesno("Setup", "No master password found. Create a new vault with this password?"):
                store_master_hash(password)
                self.fernet = get_fernet(password)
                self.data = {}
                save_data(self.fernet, self.data)
                messagebox.showinfo(
                    "Vault Created", "Master password set and vault initialized.")
                self.show_main_app()
            else:
                return
        else:
            if verify_master_password(password):
                self.fernet = get_fernet(password)
                self.data = load_data(self.fernet)
                if isinstance(self.data, dict):
                    self.show_main_app()
                else:
                    messagebox.showerror("Error", "Vault data is corrupted.")
            else:
                messagebox.showerror("Error", "Incorrect master password.")

    def show_main_app(self):
        self.clear_window()

        # Sidebar
        self.sidebar = tk.Frame(self, width=200, bg=BTN_COLOR)
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.main_content = tk.Frame(self, bg=BG_COLOR)
        self.main_content.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        options = [
            ("➕ Add Account", self.show_add_account),
            ("✏️ Manage Account", self.show_manage_account),
            ("🔍 Search Account", self.show_search_account),
            ("🔐 Generate Password", self.show_generate_password)
        ]

        for text, command in options:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=BTN_COLOR,
                activebackground=BTN_ACTIVE,
                fg=LABEL_FG_COLOR,
                font=FONT,
                anchor="w",
                padx=20,
                pady=10,
                relief=tk.FLAT
            )
            btn.pack(fill="x")

        self.show_generate_password()  # default view

    def show_add_account(self):
        self.clear_main_content()

        tk.Label(self.main_content, text="Add Account",
                 fg=LABEL_FG_COLOR, bg=BG_COLOR, font=TITLE_FONT).pack(pady=10)

        # Account Name
        tk.Label(self.main_content, text="Account Name:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        self.add_account_name_var = tk.StringVar()
        tk.Entry(self.main_content, textvariable=self.add_account_name_var,
                 bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT).pack(fill="x", padx=20, pady=5)

        # Email
        tk.Label(self.main_content, text="Email:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        self.add_email_var = tk.StringVar()
        tk.Entry(self.main_content, textvariable=self.add_email_var, bg=ENTRY_BG,
                 fg=LABEL_FG_COLOR, font=FONT).pack(fill="x", padx=20, pady=5)

        # Site URL
        tk.Label(self.main_content, text="Site URL:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        self.add_site_url_var = tk.StringVar()
        tk.Entry(self.main_content, textvariable=self.add_site_url_var, bg=ENTRY_BG,
                 fg=LABEL_FG_COLOR, font=FONT).pack(fill="x", padx=20, pady=5)

        # Description
        tk.Label(self.main_content, text="Description:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        self.add_description_var = tk.StringVar()
        tk.Entry(self.main_content, textvariable=self.add_description_var,
                 bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT).pack(fill="x", padx=20, pady=5)

        # Password Field
        tk.Label(self.main_content, text="Password:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        self.add_password_var = tk.StringVar()
        self.add_password_entry = tk.Entry(
            self.main_content, textvariable=self.add_password_var, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT)
        self.add_password_entry.pack(fill="x", padx=20, pady=5)

        # Password Generator Quick Options
        length_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        length_frame.pack(pady=2)

        tk.Label(length_frame, text="Length (8 - 256):", bg=BG_COLOR,
                 fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")

        self.length_var = tk.StringVar(value="25")
        tk.Spinbox(
            length_frame,
            from_=8,
            to=256,
            textvariable=self.length_var,
            width=6,
            font=PASS_GEN_FONT,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            insertbackground=LABEL_FG_COLOR,
            relief=tk.FLAT,
            justify="center"
        ).pack(side="left", padx=10)

        tk.Label(length_frame, text="recommended 25+", bg=BG_COLOR,
                 fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")

        self.include_small_letters = tk.BooleanVar(value=True)
        self.include_big_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        check_box_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        check_box_frame.pack(pady=2)

        tk.Checkbutton(check_box_frame,
                       text="Include small letters",
                       variable=self.include_small_letters,
                       bg=BG_COLOR,
                       font=PASS_GEN_FONT,
                       fg=LABEL_FG_COLOR,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        tk.Checkbutton(check_box_frame,
                       text="Include BIG LETTERS",
                       variable=self.include_big_letters,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        tk.Checkbutton(check_box_frame,
                       text="Include Numbers",
                       variable=self.include_numbers,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        symbols_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        symbols_frame.pack(pady=2)

        tk.Checkbutton(symbols_frame,
                       text="Include Symbols",
                       variable=self.include_symbols,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        self.custom_symbols_var = tk.StringVar()
        tk.Entry(symbols_frame,
                 textvariable=self.custom_symbols_var,
                 bg=ENTRY_BG,
                 fg=LABEL_FG_COLOR,
                 font=PASS_GEN_FONT,
                 width=36,
                 border=0,
                 justify="center"
                 ).pack(pady=2)
        self.custom_symbols_var.set('~`!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/')

        def generate_and_set_password():
            try:
                length = int(self.length_var.get())
                if length < 8 or length > 256:
                    raise ValueError("Length must be between 8 and 256")
            except ValueError:
                messagebox.showwarning(
                    "Invalid Input", "Please enter a number between 8 and 256.")
                return

            use_symbols = self.include_symbols.get()
            use_numbers = self.include_numbers.get()
            use_big_letters = self.include_big_letters.get()
            use_small_letters = self.include_small_letters.get()
            custom_symbols = self.custom_symbols_var.get().strip() or None

            password = gen_pass(length, use_symbols, use_numbers,
                                custom_symbols, use_big_letters, use_small_letters)
            self.add_password_var.set(password)

        def save_account():
            name = self.add_account_name_var.get().strip()
            email = self.add_email_var.get().strip()
            site_url = self.add_site_url_var.get().strip()
            description = self.add_description_var.get().strip()
            password = self.add_password_var.get().strip()

            if not name or not email or not password:
                messagebox.showwarning(
                    "Input Error", "Account Name, Email, and Password are required.")
                return

            if name in self.data:
                if not messagebox.askyesno("Overwrite?", f"Account '{name}' exists. Overwrite?"):
                    return

            self.data[name] = {
                "email": email,
                "site_url": site_url,
                "description": description,
                "password": password
            }
            save_data(self.fernet, self.data)
            messagebox.showinfo("Success", f"Account '{name}' saved.")
            self.show_main_app()

        btn_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Generate Password", command=generate_and_set_password, bg=BTN_COLOR, fg=LABEL_FG_COLOR,
                  activebackground=BTN_ACTIVE, font=FONT, border=0, padx=10, pady=5).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Save Account", command=save_account, bg=BTN_COLOR, fg=LABEL_FG_COLOR,
                  activebackground=BTN_ACTIVE, font=FONT, border=0, padx=10, pady=5).pack(side="left")

    def show_manage_account(self):
        self.clear_main_content()

        tk.Label(self.main_content, text="Manage Account",
                 fg=LABEL_FG_COLOR, bg=BG_COLOR, font=TITLE_FONT).pack(pady=10)

        tk.Label(self.main_content, text="Search Account:", fg=LABEL_FG_COLOR,
                 bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
        search_var = tk.StringVar()
        search_entry = tk.Entry(
            self.main_content, textvariable=search_var, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT)
        search_entry.pack(padx=20, pady=(0, 10), fill="x")

        # Listbox for search results
        listbox = tk.Listbox(self.main_content, bg=ENTRY_BG,
                             fg=LABEL_FG_COLOR, font=FONT, height=6)
        listbox.pack(padx=20, pady=(0, 10), fill="x")

        # Editable fields
        entry_widgets = {}
        fields = ["Account Name", "Email",
                  "Site URL", "Description", "Password"]
        for field in fields:
            tk.Label(self.main_content, text=field + ":", fg=LABEL_FG_COLOR,
                     bg=BG_COLOR, font=FONT).pack(anchor="w", padx=20)
            entry = tk.Entry(self.main_content, bg=ENTRY_BG,
                             fg=LABEL_FG_COLOR, font=FONT)
            entry.pack(padx=20, pady=2, fill="x")
            entry_widgets[field] = entry

        def update_fields(name):
            account = self.data.get(name)
            if not account:
                return
            entry_widgets["Account Name"].delete(0, tk.END)
            entry_widgets["Account Name"].insert(0, name)
            entry_widgets["Email"].delete(0, tk.END)
            entry_widgets["Email"].insert(0, account.get("email", ""))
            entry_widgets["Site URL"].delete(0, tk.END)
            entry_widgets["Site URL"].insert(0, account.get("site_url", ""))
            entry_widgets["Description"].delete(0, tk.END)
            entry_widgets["Description"].insert(
                0, account.get("description", ""))
            entry_widgets["Password"].delete(0, tk.END)
            entry_widgets["Password"].insert(0, account.get("password", ""))

        def filter_accounts(*args):
            query = search_var.get().lower()
            listbox.delete(0, tk.END)
            for name, info in self.data.items():
                if (query in name.lower() or
                    query in info.get("email", "").lower() or
                    query in info.get("site_url", "").lower() or
                    query in info.get("description", "").lower() or
                        query in info.get("password", "").lower()):
                    listbox.insert(tk.END, name)

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                name = listbox.get(selection[0])
                update_fields(name)

        def save_changes():
            original_name = listbox.get(
                listbox.curselection()) if listbox.curselection() else None
            if not original_name:
                messagebox.showwarning(
                    "No selection", "Please select an account to edit.")
                return

            new_name = entry_widgets["Account Name"].get().strip()
            if not new_name:
                messagebox.showwarning(
                    "Missing Info", "Account name is required.")
                return

            new_data = {
                "email": entry_widgets["Email"].get().strip(),
                "site_url": entry_widgets["Site URL"].get().strip(),
                "description": entry_widgets["Description"].get().strip(),
                "password": entry_widgets["Password"].get().strip()
            }

            # Rename key if name changed
            if new_name != original_name:
                self.data.pop(original_name)
            self.data[new_name] = new_data

            save_data(self.fernet, self.data)
            messagebox.showinfo("Saved", f"Account '{new_name}' updated.")
            self.show_manage_account()

        def delete_selected():
            name = listbox.get(listbox.curselection()
                               ) if listbox.curselection() else None
            if not name:
                messagebox.showwarning(
                    "No selection", "Please select an account to delete.")
                return
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
                self.data.pop(name, None)
                save_data(self.fernet, self.data)
                messagebox.showinfo("Deleted", f"Account '{name}' deleted.")
                self.show_manage_account()

        # Buttons
        btn_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save Changes", command=save_changes, bg=BTN_COLOR,
                  fg=LABEL_FG_COLOR, font=FONT, border=0).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Account", command=delete_selected,
                  bg="red", fg="white", font=FONT, border=0).pack(side="left", padx=10)

        # Bind events
        search_var.trace_add("write", filter_accounts)
        listbox.bind("<<ListboxSelect>>", on_select)

        # Initial search
        filter_accounts()

    def show_search_account(self):
        self.clear_main_content()

        tk.Label(self.main_content, text="Search account",
                 fg=LABEL_FG_COLOR, bg=BG_COLOR, font=TITLE_FONT).pack(pady=10)

        # Layout: split into left and right frames inside main_content
        left_frame = tk.Frame(self.main_content, bg=BTN_COLOR, width=260)
        left_frame.pack(side="left", fill="y", padx=(20, 10), pady=20)
        left_frame.pack_propagate(False)  # prevent shrinking

        right_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both",
                         expand=True, padx=(10, 20), pady=20)

        # Search input on top of left frame
        tk.Label(left_frame, text="Search Accounts:", fg=LABEL_FG_COLOR,
                 bg=BTN_COLOR, font=FONT).pack(anchor="w", pady=(0, 5), padx=5)
        self.search_account_var = tk.StringVar()
        search_entry = tk.Entry(
            left_frame, textvariable=self.search_account_var, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT)
        search_entry.pack(fill="x", padx=5, pady=(0, 10))
        search_entry.focus()

        # Listbox to show filtered account names
        self.search_results_listbox = tk.Listbox(
            left_frame, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT, activestyle='none', selectbackground=BTN_ACTIVE, highlightthickness=0)
        self.search_results_listbox.pack(
            fill="both", expand=True, padx=5, pady=5)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(
            self.search_results_listbox, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.search_results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_results_listbox.yview)

        # Helper function to make Text widget readonly but selectable and copyable
        def make_text_readonly(text_widget):
            # Allow navigation keys but block editing keys
            def block_edit(event):
                if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Next', 'Prior', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
                    return
                # Allow Ctrl+C for copy
                if (event.state & 0x4) and event.keysym.lower() == 'c':
                    return
                return "break"
            text_widget.bind("<Key>", block_edit)
            # Allow Ctrl+C and Ctrl+Insert for copying
            text_widget.bind("<Control-c>", lambda e: None)
            text_widget.bind("<Control-C>", lambda e: None)
            text_widget.bind("<Control-Insert>", lambda e: None)

        # Account details labels on right frame
        self.detail_widgets = {}
        fields = ["Account Name", "Email",
                  "Site URL", "Description", "Password"]
        for field in fields:
            label = tk.Label(right_frame, text=field + ":",
                             fg=LABEL_FG_COLOR, bg=BG_COLOR, font=FONT)
            label.pack(anchor="nw", pady=(
                10 if field == "Account Name" else 2, 2))
            text = tk.Text(right_frame, height=1 if field != "Description" else 4,
                           bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT, relief=tk.FLAT, wrap="word")
            text.pack(fill="x" if field != "Description" else "both", pady=2)
            # Don't disable the widget, keep it normal but block edits
            make_text_readonly(text)
            self.detail_widgets[field] = text

        def update_detail_widgets(account_name):
            if not account_name or account_name not in self.data:
                # Instead of clearing and disabling, just keep current content
                # Or you can just do nothing to keep previous content visible
                return

            account = self.data[account_name]

            for field in self.detail_widgets.values():
                field.config(state="normal")

            # Update fields
            self.detail_widgets["Account Name"].delete("1.0", tk.END)
            self.detail_widgets["Account Name"].insert(tk.END, account_name)

            for key, field in [("email", "Email"), ("site_url", "Site URL"), ("description", "Description"), ("password", "Password")]:
                self.detail_widgets[field].delete("1.0", tk.END)
                self.detail_widgets[field].insert(tk.END, account.get(key, ""))

            for field in self.detail_widgets.values():
                # Keep normal so user can copy text
                field.config(state="normal")

        def filter_accounts(*args):
            query = self.search_account_var.get().lower()
            self.search_results_listbox.delete(0, tk.END)

            # No early return here — we want to show all accounts if query is empty
            filtered = []
            for name, info in self.data.items():
                if (not query or
                    query in name.lower() or
                    query in info.get("email", "").lower() or
                    query in info.get("description", "").lower() or
                    query in info.get("site_url", "").lower() or
                        query in info.get("password", "").lower()):
                    filtered.append(name)

            for account_name in filtered:
                self.search_results_listbox.insert(tk.END, account_name)

            # Optionally clear detail widgets if nothing is selected
            if not filtered:
                update_detail_widgets(None)

        def on_select(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                account_name = event.widget.get(index)
                update_detail_widgets(account_name)
            else:
                update_detail_widgets(None)

        # Bind events
        self.search_account_var.trace_add("write", filter_accounts)
        self.search_results_listbox.bind("<<ListboxSelect>>", on_select)

        # Initially clear detail pane
        update_detail_widgets(None)
        filter_accounts()

    def show_generate_password(self):
        self.clear_main_content()

        title = tk.Label(
            self.main_content,
            text="🔐 Generate Password",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=TITLE_FONT
        )
        title.pack(pady=20)

        length_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        length_frame.pack(pady=2)

        tk.Label(length_frame, text="Length (8 - 256):", bg=BG_COLOR,
                 fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")

        self.length_var = tk.StringVar(value="25")
        tk.Spinbox(
            length_frame,
            from_=8,
            to=256,
            textvariable=self.length_var,
            width=6,
            font=PASS_GEN_FONT,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            insertbackground=LABEL_FG_COLOR,
            relief=tk.FLAT,
            justify="center"
        ).pack(side="left", padx=10)

        tk.Label(length_frame, text="recommended 25+", bg=BG_COLOR,
                 fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")

        self.include_small_letters = tk.BooleanVar(value=True)
        self.include_big_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        check_box_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        check_box_frame.pack(pady=2)

        tk.Checkbutton(check_box_frame,
                       text="Include small letters",
                       variable=self.include_small_letters,
                       bg=BG_COLOR,
                       font=PASS_GEN_FONT,
                       fg=LABEL_FG_COLOR,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        tk.Checkbutton(check_box_frame,
                       text="Include BIG LETTERS",
                       variable=self.include_big_letters,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        tk.Checkbutton(check_box_frame,
                       text="Include Numbers",
                       variable=self.include_numbers,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        symbols_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        symbols_frame.pack(pady=2)

        tk.Checkbutton(symbols_frame,
                       text="Include Symbols",
                       variable=self.include_symbols,
                       bg=BG_COLOR,
                       fg=LABEL_FG_COLOR,
                       font=PASS_GEN_FONT,
                       selectcolor=BG_COLOR,
                       activebackground=BG_COLOR
                       ).pack(side="left")

        self.custom_symbols_var = tk.StringVar()
        tk.Entry(symbols_frame,
                 textvariable=self.custom_symbols_var,
                 bg=ENTRY_BG,
                 fg=LABEL_FG_COLOR,
                 font=PASS_GEN_FONT,
                 width=36,
                 border=0,
                 justify="center"
                 ).pack(pady=2)
        self.custom_symbols_var.set('~`!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/')

        tk.Label(
            self.main_content,
            text="Generated password:",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=FONT
        ).pack(pady=10)

        self.result_var = tk.StringVar()
        self.result_label = tk.Label(
            self.main_content,
            textvariable=self.result_var,
            font=FONT,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            wraplength=500,
            justify="left",
            height=7,
            width=64,
        ).pack(pady=2)

        btn_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,
                  text="Generate Password",
                  command=self.generate_password_button,
                  bg=BTN_COLOR,
                  fg=LABEL_FG_COLOR,
                  activebackground=BTN_ACTIVE,
                  font=FONT,
                  border=0,
                  padx=10,
                  pady=5).pack(side="left", padx=(0, 10))

        tk.Button(btn_frame,
                  text="Copy Password",
                  command=self.copy_password_to_clipboard,
                  bg=BTN_COLOR,
                  fg=LABEL_FG_COLOR,
                  activebackground=BTN_ACTIVE,
                  font=FONT,
                  border=0,
                  padx=10,
                  pady=5).pack(side="left")

    def generate_password_button(self):
        try:
            length = int(self.length_var.get())
            if length < 8 or length > 256:
                raise ValueError("Length must be between 8 and 256")
        except ValueError:
            messagebox.showwarning(
                "Invalid Input", "Please enter a number between 8 and 256.")
            return

        use_symbols = self.include_symbols.get()
        use_numbers = self.include_numbers.get()
        use_big_letters = self.include_big_letters.get()
        use_small_letters = self.include_small_letters.get()
        custom_symbols = self.custom_symbols_var.get().strip() or None

        password = gen_pass(length, use_symbols, use_numbers,
                            custom_symbols, use_big_letters, use_small_letters)

        self.result_var.set(password)

    def copy_password_to_clipboard(self):
        password = self.result_var.get().strip()
        if not password:
            messagebox.showwarning(
                "No Password", "Please generate a password first.")
            return
        self.clipboard_clear()
        self.clipboard_append(password)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
