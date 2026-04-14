# Main entry point for the Password Manager application
from ui.gui import PasswordManagerUI

if __name__ == "__main__":
    app = PasswordManagerUI()
    app.mainloop()