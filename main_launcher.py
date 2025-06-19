import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow
from main import HSNApp
import keyring

def is_logged_in():
    email = keyring.get_password("HSNApp", "current_user")
    pin = keyring.get_password("HSNApp", email) if email else None
    return bool(email and pin)

def launch_app():
    app = QApplication(sys.argv)
    
    if is_logged_in():
        window = HSNApp()
        window.show()
    else:
        login_window = LoginWindow()
        login_window.login_successful.connect(lambda email, name: show_main_app())
        login_window.show()
        
    def show_main_app():
        login_window.close()
        main_window = HSNApp()
        main_window.show()
        
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_app()