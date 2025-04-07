"""User interface for CrackMaster with modern design."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from core.facts import CrackFacts
from core.logic import CrackLogic
from core.settings import Settings
from babel.support import Translations
import os

class CrackMasterUI(BoxLayout):
    """Main UI class for CrackMaster."""

    status_text = StringProperty("Ready to crack! 🚀")
    count_text = StringProperty("Cracks: 0")
    fact_text = StringProperty("")

    def __init__(self, settings: Settings, translations: Translations, **kwargs):
        """Initialize UI with logic, settings, and translations."""
        super().__init__(**kwargs)
        self.settings = settings
        self.translations = translations
        self.logic = CrackLogic(self.settings.get_cooldown(), self.translations)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15
        self.build_ui()
        Clock.schedule_interval(self.update_status, 1)

    def build_ui(self) -> None:
        """Construct the UI elements."""
        self.canvas.before.add(Color(0.1, 0.1, 0.1, 1))  # Dark BG
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        self.status_label = Label(text=self.status_text, font_size=24, color=(1, 0.8, 0, 1), bold=True)
        self.count_label = Label(text=self.count_text, font_size=18, color=(0.9, 0.9, 0.9, 1))
        self.fact_label = Label(text=self.fact_text, font_size=16, color=(0.7, 0.9, 1, 1), halign="center")

        crack_btn = Button(
            text=self.translations.gettext("Crack! 💥"),
            size_hint=(1, 0.3),
            background_color=(1, 0.5, 0, 1),
            font_size=22,
            on_press=self.on_crack
        )
        settings_btn = Button(
            text=self.translations.gettext("⚙️ Settings"),
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.show_settings
        )

        self.add_widget(self.status_label)
        self.add_widget(self.count_label)
        self.add_widget(self.fact_label)
        self.add_widget(crack_btn)
        self.add_widget(settings_btn)

    def on_crack(self, instance) -> None:
        """Handle crack button press."""
        success, message, fact = self.logic.crack()
        self.status_text = message
        self.count_text = self.translations.gettext("Cracks: {}").format(self.logic.crack_count)
        self.fact_text = fact if success else ""

    def update_status(self, dt: float) -> None:
        """Update status label and check recharge."""
        self.status_text = self.logic.get_status()
        self.count_text = self.translations.gettext("Cracks: {}").format(self.logic.crack_count)
        recharge_msg = self.logic.check_recharge()
        if recharge_msg:
            self.status_text = recharge_msg

    def show_settings(self, instance) -> None:
        """Show settings popup."""
        content = BoxLayout(orientation="vertical", padding=10)
        cooldown_label = Label(text=self.translations.gettext("Cooldown: {} sec").format(self.settings.get_cooldown()))
        cooldown_btn = Button(
            text=self.translations.gettext("60 sec ⏱️"),
            on_press=lambda x: self.update_cooldown(60, cooldown_label)
        )
        lang_label = Label(text=self.translations.gettext("Language: {}").format(
            "Русский" if self.settings.get_language() == "ru" else "English"))
        lang_btn = Button(
            text=self.translations.gettext("Change language 🌐"),
            on_press=lambda x: self.toggle_language(lang_label)
        )

        content.add_widget(cooldown_label)
        content.add_widget(cooldown_btn)
        content.add_widget(lang_label)
        content.add_widget(lang_btn)

        popup = Popup(
            title=self.translations.gettext("⚙️ Settings"),
            content=content,
            size_hint=(0.8, 0.6),
            background_color=(0.1, 0.1, 0.1, 1)
        )
        popup.open()

    def update_cooldown(self, value: int, label: Label) -> None:
        """Update cooldown value in settings."""
        self.settings.set_cooldown(value)
        self.logic.cooldown = value
        label.text = self.translations.gettext("Cooldown: {} sec").format(value)

    def toggle_language(self, label: Label) -> None:
        """Toggle between languages and reload UI."""
        new_lang = "en" if self.settings.get_language() == "ru" else "ru"
        self.settings.set_language(new_lang)
        locale_dir = os.path.join(os.path.dirname(__file__), "..", "..", "locale")
        self.translations = Translations.load(locale_dir, [new_lang], domain="messages")
        self.logic.translations = self.translations
        self.logic.facts = CrackFacts(self.translations)
        label.text = self.translations.gettext("Language: {}").format("Русский" if new_lang == "ru" else "English")
        self.clear_widgets()
        self.build_ui()