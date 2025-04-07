"""Main application logic and initialization."""

from kivy.app import App
from ui.interface import CrackMasterUI
from core.settings import Settings
from babel.support import Translations
import os


class CrackMasterApp(App):
    """Main application class for CrackMaster."""

    def build(self):
        """Initialize and return the UI."""
        settings = Settings()
        locale_dir = os.path.join(os.path.dirname(__file__), "..", "locale")
        translations = Translations.load(locale_dir, [settings.get_language()], domain="messages")
        return CrackMasterUI(settings, translations)

    def on_start(self):
        """Actions to perform on app start."""
        print("CrackMaster started! 🚀")