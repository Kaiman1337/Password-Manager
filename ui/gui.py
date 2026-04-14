import tkinter as tk
from tkinter import messagebox
from core import (
    get_fernet,
    verify_master_password,
    store_master_hash,
    load_data,
    save_data,
    gen_pass,
)
from PIL import Image, ImageTk
import uuid

# Theme constants
LABEL_FG_COLOR = "#EEE"
ENTRY_BG = "#1e1e1e"
BG_COLOR = "#141517"
BG_SIDEBAR_COLOR = "#161616"
BTN_COLOR = "#202020"
BTN_ACTIVE = "#333"
FONT = ("Consolas", 12)
PASS_GEN_FONT = ("Consolas", 10)
TITLE_FONT = ("Consolas", 16, "bold")
ACCOUNT_FIELDS = ["Account Name", "Login", "Email", "Site URL", "Description", "Password"]

def add_labeled_entry(parent, label_text, var, **entry_kwargs):
    tk.Label(
        parent,
        text=label_text,
        fg=LABEL_FG_COLOR,
        bg=BG_COLOR,
        font=FONT,
    ).pack(anchor="w", padx=20)
    tk.Entry(
        parent,
        textvariable=var,
        bg=ENTRY_BG,
        fg=LABEL_FG_COLOR,
        font=FONT,
        **entry_kwargs
    ).pack(fill="x", padx=20, pady=5)
    
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

    def create_label(self, parent, text, font=FONT, **kwargs):
        return tk.Label(parent, text=text, fg=LABEL_FG_COLOR, bg=BG_COLOR, font=font, **kwargs)

    def create_entry(self, parent, **kwargs):
        return tk.Entry(parent, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=FONT, insertbackground=LABEL_FG_COLOR, **kwargs)

    def create_button(self, parent, text, command, **kwargs):
        return tk.Button(parent, text=text, command=command, bg=BTN_COLOR, fg=LABEL_FG_COLOR, 
                        activebackground=BTN_ACTIVE, font=FONT, border=0, **kwargs)

    def show_unlock_panel(self):
        self.clear_window()

        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(pady=(160, 0))

        title = tk.Label(
            frame,
            text="Enter Master Password",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=TITLE_FONT,
        )
        title.pack(pady=20)

        self.master_entry = tk.Entry(
            frame,
            show="*",
            font=FONT,
            width=30,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            insertbackground=LABEL_FG_COLOR,
            highlightthickness=0,
            relief=tk.FLAT,
        )
        self.master_entry.bind("<Return>", lambda event: self.try_unlock())
        self.master_entry.pack(pady=10)
        self.master_entry.focus()

        unlock_img = ImageTk.PhotoImage(Image.open("./ui/images/unlock.png").resize((120, 40)))
        unlock_btn = tk.Button(
            frame,
            image=unlock_img,
            command=self.try_unlock,
            bg=BG_COLOR,
            border=0,
        )
        unlock_btn.image = unlock_img
        unlock_btn.pack(pady=30)

    def try_unlock(self):
        password = self.master_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Please enter the master password.")
            return
        
        if verify_master_password(password):
            self.fernet = get_fernet(password)
            self.data = load_data(self.fernet)
            if isinstance(self.data, dict):
                # Add id to existing accounts if missing
                for name, acc in self.data.items():
                    if "id" not in acc:
                        acc["id"] = str(uuid.uuid4())
                self.show_main_app()
            else:
                messagebox.showerror("Error", "Vault data is corrupted.")
        else:
            if messagebox.askyesno("Setup", "No master password found.\n\nCreate a new database using this password?"):
                store_master_hash(password)
                self.fernet = get_fernet(password)
                self.data = {}
                save_data(self.fernet, self.data)
                messagebox.showinfo("Vault Created", "Master password set!")
                self.show_main_app()

    def show_main_app(self):
        self.clear_window()

        # Sidebar
        self.sidebar = tk.Frame(self, width=200, bg=BG_SIDEBAR_COLOR)
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.main_content = tk.Frame(self, bg=BG_COLOR)
        self.main_content.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        options = [
            ("➕ Add Account", self.show_add_account),
            ("📋 Accounts", self.show_accounts),
            ("🔐 Generate Password", self.show_generated_password),
            ("🚪 Logout", self.show_logout),
        ]

        for text, command in options:
            self.create_button(self.sidebar, text, command, anchor="w", padx=20, pady=10, relief=tk.FLAT).pack(fill="x")

        self.show_add_account()

    def _save_account(self):
        account_name = self.add_account_name_var.get().strip()
        login = self.add_login_var.get().strip()
        email = self.add_email_var.get().strip()
        site_url = self.add_site_url_var.get().strip()
        description = self.add_description_text.get("1.0", tk.END).strip()
        password = self.add_password_var.get().strip()
        
        if not account_name or not password:
            messagebox.showwarning("Missing Fields", "Account Name and Password required!")
            return
        
        self.data[account_name] = {
            "login": login,
            "email": email,
            "site_url": site_url,
            "description": description,
            "password": password,
            "id": str(uuid.uuid4())
        }
        
        save_data(self.fernet, self.data)
        messagebox.showinfo("Success", f"Account '{account_name}' saved!")
        
        for var_name in ["add_account_name_var", "add_login_var", "add_email_var", 
                        "add_site_url_var", "add_password_var"]:
            if hasattr(self, var_name):
                getattr(self, var_name).set("")
        self.add_description_text.delete("1.0", tk.END)

    def create_password_gen_panel(self, parent, target_var):
        frame = tk.Frame(parent, bg=BG_COLOR)
        
        # Length frame (your exact code)
        length_frame = tk.Frame(frame, bg=BG_COLOR)
        length_frame.pack(pady=2)
        tk.Label(length_frame, text="Length (8 - 256):", bg=BG_COLOR, fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")
        self.length_var = tk.StringVar(value="25")
        tk.Spinbox(length_frame, from_=8, to=256, textvariable=self.length_var, width=6, font=PASS_GEN_FONT, bg=ENTRY_BG, fg=LABEL_FG_COLOR, insertbackground=LABEL_FG_COLOR, relief=tk.FLAT, justify="center").pack(side="left", padx=10)
        tk.Label(length_frame, text="recommended 25+", bg=BG_COLOR, fg=LABEL_FG_COLOR, font=PASS_GEN_FONT).pack(side="left")
        
        # Checkboxes (your exact code)
        self.include_small_letters = tk.BooleanVar(value=True)
        self.include_big_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        check_box_frame = tk.Frame(frame, bg=BG_COLOR)
        check_box_frame.pack(pady=2)
        for text, var in [("Include small letters", self.include_small_letters), ("Include BIG LETTERS", self.include_big_letters), ("Include Numbers", self.include_numbers)]:
            tk.Checkbutton(check_box_frame, text=text, variable=var, bg=BG_COLOR, font=PASS_GEN_FONT, fg=LABEL_FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack(side="left")
        
        # Symbols (your exact code)
        symbols_frame = tk.Frame(frame, bg=BG_COLOR)
        symbols_frame.pack(pady=2)
        tk.Checkbutton(symbols_frame, text="Include Symbols", variable=self.include_symbols, bg=BG_COLOR, fg=LABEL_FG_COLOR, font=PASS_GEN_FONT, selectcolor=BG_COLOR, activebackground=BG_COLOR).pack(side="left")
        self.custom_symbols_var = tk.StringVar()
        tk.Entry(symbols_frame, textvariable=self.custom_symbols_var, bg=ENTRY_BG, fg=LABEL_FG_COLOR, font=PASS_GEN_FONT, width=36, border=0, justify="center").pack(side="left", padx=5)
        tk.Button(symbols_frame, text="Reset symbols", command=lambda: self.custom_symbols_var.set("~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"), bg=BTN_COLOR, fg=LABEL_FG_COLOR, activebackground=BTN_ACTIVE, font=PASS_GEN_FONT, border=0, padx=5, pady=2).pack(side="left", padx=2)
        
        # Generate button
        self.create_button(frame, "Generate Password", lambda: self._gen_password(target_var)).pack(pady=10)
        self.custom_symbols_var.set("~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/")
        return frame

    def _gen_password(self, target_var):
        try:
            length = int(self.length_var.get())
            if length < 8 or length > 256: raise ValueError()
        except ValueError:
            messagebox.showwarning("Invalid", "Length 8-256.")
            return
        pw = gen_pass(length, self.include_symbols.get(), self.include_numbers.get(),
                      self.custom_symbols_var.get().strip() or None,
                      self.include_big_letters.get(), self.include_small_letters.get())
        target_var.set(pw)

    def show_add_account(self):
        self.clear_main_content()
        tk.Label(
            self.main_content,
            text="Add Account",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=TITLE_FONT,
        ).pack(pady=10)

        fields = [
            ("Account Name:", "add_account_name_var"),
            ("Login:", "add_login_var"),
            ("Email:", "add_email_var"),
            ("Site URL:", "add_site_url_var"),
        ]
        
        for label, var_name in fields:
            setattr(self, var_name, tk.StringVar())
            add_labeled_entry(self.main_content, label, getattr(self, var_name))

        # DESCRIPTION - EXACTLY 4 LINES
        tk.Label(
            self.main_content,
            text="Description:",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=FONT,
        ).pack(anchor="w", padx=20, pady=(0, 2))
        
        self.add_description_text = tk.Text(
            self.main_content,
            height=4,  # Exactly 4 lines
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            font=FONT,
            relief=tk.FLAT,
            bd=1,
            wrap="word",
            padx=5,
            pady=5,
            highlightthickness=0,
        )
        self.add_description_text.pack(fill="x", padx=20, pady=(0, 10))  # fill="x" ONLY

        self.create_label(self.main_content, "Password:").pack(anchor="w", padx=20)
        self.add_password_var = tk.StringVar()
        self.add_password_entry = self.create_entry(self.main_content, textvariable=self.add_password_var)
        self.add_password_entry.pack(fill="x", padx=20, pady=5)
        
        self.create_password_gen_panel(self.main_content, self.add_password_var).pack(pady=10)
        self.create_button(self.main_content, "Save Account", self._save_account).pack(pady=10)

    def show_accounts(self):
        self.clear_main_content()

        tk.Label(
            self.main_content,
            text="Accounts",
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR,
            font=TITLE_FONT,
        ).pack(pady=10)

        # Layout: split into left and right frames inside main_content
        left_frame = tk.Frame(self.main_content, bg=BTN_COLOR, width=260)
        left_frame.pack(side="left", fill="y", padx=(20, 10), pady=20)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

        # Search input
        tk.Label(
            left_frame,
            text="Search Accounts:",
            fg=LABEL_FG_COLOR,
            bg=BTN_COLOR,
            font=FONT,
        ).pack(anchor="w", pady=(0, 5), padx=5)
        
        self.search_account_var = tk.StringVar()
        search_entry = tk.Entry(
            left_frame,
            textvariable=self.search_account_var,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            font=FONT,
        )
        search_entry.pack(fill="x", padx=5, pady=(0, 10))
        search_entry.focus()

        # Listbox
        self.search_results_listbox = tk.Listbox(
            left_frame,
            bg=ENTRY_BG,
            fg=LABEL_FG_COLOR,
            font=FONT,
            activestyle="none",
            selectbackground=BTN_ACTIVE,
            highlightthickness=0,
        )
        self.search_results_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.search_results_listbox, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.search_results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_results_listbox.yview)

        # State variables
        self.edit_mode = False
        self.selected_account_name = None
        self.editing_account = None
        self.detail_widgets = {}

        fields = ["Account Name", "Login", "Email", "Site URL", "Description", "Password"]

        for field in fields:
            field_frame = tk.Frame(right_frame, bg=BG_COLOR)
            field_frame.pack(anchor="nw", pady=(2))
            
            tk.Label(
                field_frame, text=field + ":", fg=LABEL_FG_COLOR, bg=BG_COLOR, font=FONT
            ).pack(side="left")

            def make_copy_handler(field_name):
                def copy_handler():
                    text_widget = self.detail_widgets[field_name]
                    content = text_widget.get("1.0", tk.END).replace('\n', ' ')
                    content = ' '.join(content.split())
                    if content:
                        self.main_content.clipboard_clear()
                        self.main_content.clipboard_append(content)
                return copy_handler
            
            # COPY BUTTON - TIGHT + ICON + SMALLER FONT
            copy_btn = tk.Button(
                field_frame,
                text="copy 📋",
                bg=BTN_COLOR,
                fg=LABEL_FG_COLOR,
                font=("Arial", 10),
                border=0,
                relief="flat",
                padx=0,
                pady=0,
                height=1,
                anchor="center",
                command=make_copy_handler(field),
                activebackground=BTN_ACTIVE,
                cursor="hand2"
            )
            copy_btn.pack(side="right", padx=(5, 0))
            
            text = tk.Text(
                right_frame,
                height=1,
                bg=ENTRY_BG,
                fg=LABEL_FG_COLOR,
                font=FONT,
                relief=tk.FLAT,
                wrap="word",
                padx=8,
                pady=4,
                bd=0,
                highlightthickness=0,
            )
            text.pack(fill="x", pady=2)
            self.detail_widgets[field] = text

        def update_password_height(password_text):
            password_widget = self.detail_widgets["Password"]
            if not password_text:
                password_widget.config(height=1)
                return
            
            lines_needed = (len(password_text) + 63) // 64
            lines_needed = min(max(lines_needed, 1), 4)
            password_widget.config(height=lines_needed)
            
            formatted_lines = [password_text[i:i+64] for i in range(0, len(password_text), 64)]
            password_widget.delete("1.0", tk.END)
            password_widget.insert(tk.END, '\n'.join(formatted_lines))
            password_widget.config(wrap="none")

        def update_description_height(description_text):
            desc_widget = self.detail_widgets["Description"]
            if not description_text:
                desc_widget.config(height=1)
                return
            
            lines = description_text.split('\n')
            total_chars = len(description_text.replace('\n', ' '))
            estimated_lines = len(lines) + (total_chars // 80)
            lines_needed = min(max(estimated_lines, 1), 6)
            
            desc_widget.config(height=lines_needed)
            desc_widget.delete("1.0", tk.END)
            desc_widget.insert(tk.END, description_text)

        # Make text readonly
        def make_text_readonly(text_widget):
            def block_edit(event):
                if self.edit_mode: return
                allowed_keys = {"Left", "Right", "Up", "Down", "Home", "End", 
                            "Next", "Prior", "Shift_L", "Shift_R", 
                            "Control_L", "Control_R"}
                if event.keysym in allowed_keys:
                    return
                if event.state & 0x4 and event.keysym.lower() == 'c':
                    return
                return "break"
            
            text_widget.bind("<Key>", block_edit)

        for widget in self.detail_widgets.values():
            make_text_readonly(widget)

        # Update details
        def update_detail_widgets(account_name):
            if not account_name or account_name not in self.data:
                for field in self.detail_widgets.values():
                    field.delete("1.0", tk.END)
                    if field in [self.detail_widgets["Description"], self.detail_widgets["Password"]]:
                        field.config(height=1)
                    else:
                        field.config(height=1)
                self.selected_account_name = None
                return

            account = self.data[account_name]
            self.selected_account_name = account_name

            for widget in self.detail_widgets.values():
                widget.config(state="normal")

            # FIXED HEIGHT FIELDS - always 1 line
            single_line_fields = ["Account Name", "Login", "Email", "Site URL"]
            for field_name in single_line_fields:
                widget = self.detail_widgets[field_name]
                widget.delete("1.0", tk.END)
                if field_name == "Account Name":
                    widget.insert(tk.END, account_name)
                elif field_name == "Login":
                    widget.insert(tk.END, account.get("login", ""))
                elif field_name == "Email":
                    widget.insert(tk.END, account.get("email", ""))
                elif field_name == "Site URL":
                    widget.insert(tk.END, account.get("site_url", ""))
                widget.config(height=1)

            # DYNAMIC FIELDS - only if NOT in edit mode
            if not self.edit_mode:
                description_text = account.get("description", "")
                update_description_height(description_text)
                
                password_text = account.get("password", "")
                update_password_height(password_text)
            else:
                # In edit mode - preserve current content with fixed height
                self.detail_widgets["Description"].delete("1.0", tk.END)
                self.detail_widgets["Description"].insert(tk.END, account.get("description", ""))
                self.detail_widgets["Description"].config(height=4)
                
                self.detail_widgets["Password"].delete("1.0", tk.END)
                self.detail_widgets["Password"].insert(tk.END, account.get("password", ""))
                self.detail_widgets["Password"].config(height=4, wrap="word")

            if not self.edit_mode:
                for widget in self.detail_widgets.values():
                    make_text_readonly(widget)

        def toggle_edit():
            # Check if an account is selected
            current_selection = self.search_results_listbox.curselection()
            if not current_selection:
                return
            
            self.edit_mode = not self.edit_mode
            
            # Get CURRENT selected account name from listbox
            current_account_name = self.search_results_listbox.get(current_selection[0])
            
            if self.edit_mode:
                self.editing_account = current_account_name
                self.editing_id = self.data[current_account_name].get("id")
            else:
                self.editing_account = None
                self.editing_id = None
            
            # Only change editability
            for widget in self.detail_widgets.values():
                if self.edit_mode:
                    widget.config(state="normal", wrap="word")
                else:
                    make_text_readonly(widget)
                    # Restore dynamic sizing ONLY if account exists
                    if current_account_name and current_account_name in self.data:
                        account = self.data[current_account_name]
                        update_description_height(account.get("description", ""))
                        update_password_height(account.get("password", ""))
            
            if self.edit_mode:
                self.edit_button.config(text="Cancel", bg="orange")
                self.save_button.config(state="normal", bg="green")
                self.delete_button.config(state="normal")
            else:
                self.edit_button.config(text="Edit", bg=BTN_COLOR)
                self.save_button.config(state="disabled", bg=BTN_COLOR)
                self.delete_button.config(state="disabled")
                
                # Update selected name after cancel
                self.selected_account_name = current_account_name

        # Filter accounts
        def filter_accounts(*args):
            if self.edit_mode:
                return  # Don't filter during edit mode to avoid losing changes
            query = self.search_account_var.get().lower()
            self.search_results_listbox.delete(0, tk.END)
            for name, info in self.data.items():
                if (not query or 
                    query in name.lower() or 
                    query in info.get("email", "").lower() or
                    query in info.get("site_url", "").lower() or
                    query in info.get("description", "").lower() or
                    query in info.get("password", "").lower()):
                    self.search_results_listbox.insert(tk.END, name)

        def on_select(event):
            selection = self.search_results_listbox.curselection()
            if selection:
                update_detail_widgets(self.search_results_listbox.get(selection[0]))
                self.edit_button.config(state="normal")
            else:
                self.edit_button.config(state="disabled")

        def on_tab(event):
            lb = self.search_results_listbox
            size = lb.size()
            sel = lb.curselection()
            if size == 0: return "break"
            idx = sel[0] if sel else -1
            next_idx = (idx + 1) % size if idx >= 0 else 0
            lb.selection_clear(0, tk.END)
            lb.selection_set(next_idx)
            lb.see(next_idx)
            update_detail_widgets(lb.get(next_idx))
            return "break"

        def save_changes():
            if not self.edit_mode or not self.editing_id:
                return
            
            # Find the account by id
            old_name = None
            for name, acc in self.data.items():
                if acc.get("id") == self.editing_id:
                    old_name = name
                    break
            if not old_name:
                return
            
            new_name = self.detail_widgets["Account Name"].get("1.0", tk.END).strip()
            
            if not new_name:
                return

            new_data = {
                "login": self.detail_widgets["Login"].get("1.0", tk.END).strip(),
                "email": self.detail_widgets["Email"].get("1.0", tk.END).strip(),
                "site_url": self.detail_widgets["Site URL"].get("1.0", tk.END).strip(),
                "description": self.detail_widgets["Description"].get("1.0", tk.END).strip(),
                "password": self.detail_widgets["Password"].get("1.0", tk.END).replace('\n', ''),
            }

            # Update data
            self.data.pop(old_name, None)
            self.data[new_name] = new_data
            
            save_data(self.fernet, self.data)
            toggle_edit()
            filter_accounts()
            
            # Find the saved account name by id and select it
            saved_name = None
            for name, acc in self.data.items():
                if acc.get("id") == self.editing_id:
                    saved_name = name
                    break
            if saved_name:
                for i in range(self.search_results_listbox.size()):
                    if self.search_results_listbox.get(i) == saved_name:
                        self.search_results_listbox.selection_set(i)
                        self.search_results_listbox.see(i)
                        update_detail_widgets(saved_name)
                        break

        def delete_account():
            if self.selected_account_name:
                self.data.pop(self.selected_account_name)
                save_data(self.fernet, self.data)
                update_detail_widgets(None)
                filter_accounts()
                toggle_edit()

        # Buttons
        btn_frame = tk.Frame(right_frame, bg=BG_COLOR)
        btn_frame.pack(pady=20)
        
        self.edit_button = tk.Button(btn_frame, text="Edit", command=toggle_edit,
                                bg=BTN_COLOR, fg=LABEL_FG_COLOR, font=FONT, border=0, state="disabled")
        self.edit_button.pack(side="left", padx=10)
        
        self.save_button = tk.Button(btn_frame, text="Save", command=save_changes,
                                bg=BTN_COLOR, fg=LABEL_FG_COLOR, font=FONT, border=0, state="disabled")
        self.save_button.pack(side="left", padx=10)
        
        self.delete_button = tk.Button(btn_frame, text="Delete", command=delete_account,
                                    bg="red", fg="white", font=FONT, border=0, state="disabled")
        self.delete_button.pack(side="left", padx=10)

        # Events
        self.search_account_var.trace_add("write", filter_accounts)
        self.search_results_listbox.bind("<<ListboxSelect>>", on_select)
        self.search_results_listbox.bind("<Tab>", on_tab)

        filter_accounts()

    def show_generated_password(self):
        self.clear_main_content()
        self.create_label(self.main_content, "🔐 Generate Password", TITLE_FONT).pack(pady=20)
        
        self.result_var = tk.StringVar()
        self.create_label(self.main_content, "Generated password:").pack(pady=10)
        
        tk.Label(self.main_content, textvariable=self.result_var, font=FONT, bg=ENTRY_BG, fg=LABEL_FG_COLOR,
                wraplength=500, justify="left", height=7, width=64).pack(pady=2)
        
        self.create_password_gen_panel(self.main_content, self.result_var).pack(pady=10)
        
        btn_frame = tk.Frame(self.main_content, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        self.create_button(btn_frame, "Copy Password", self.copy_password_to_clipboard).pack(side="left")

    def generate_unique_password_button(self):
        """Generate UNIQUE password that doesn't exist in any account"""
        try:
            length = int(self.length_var.get())
            if length < 8 or length > 256:
                raise ValueError("Length must be between 8 and 256")
        except ValueError:
            messagebox.showwarning(
                "Invalid Input", "Please enter a number between 8 and 256."
            )
            return

        use_symbols = self.include_symbols.get()
        use_numbers = self.include_numbers.get()
        use_big_letters = self.include_big_letters.get()
        use_small_letters = self.include_small_letters.get()
        custom_symbols = self.custom_symbols_var.get().strip() or None

        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            password = gen_pass(
                length,
                use_symbols,
                use_numbers,
                custom_symbols,
                use_big_letters,
                use_small_letters,
            )
            
            # CHECK UNIQUENESS
            if self.is_password_unique(password):
                self.result_var.set(password)
                return  # SUCCESS!
            
            attempts += 1
        
        # Fallback
        messagebox.showinfo("Unique Password", f"Generated unique {length+8} char password:")
        fallback_pw = gen_pass(length+8, use_symbols, use_numbers, custom_symbols, use_big_letters, use_small_letters)
        self.result_var.set(fallback_pw)

    def is_password_unique(self, password):
        """Check if password already exists in self.data"""
        for account_data in self.data.values():
            if account_data.get("password") == password:
                return False
        return True

    def copy_password_to_clipboard(self):
        password = self.result_var.get().strip()
        if not password:
            messagebox.showwarning(
                "No Password", "Please generate a password first.")
            return
        self.clipboard_clear()
        self.clipboard_append(password)

    def show_logout(self):
        self.fernet = None 
        self.data = None
        self.clear_window()
        self.show_unlock_panel()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
