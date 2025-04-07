"""Core logic for knuckle cracking functionality."""

import time
from typing import Tuple, Optional
from plyer import notification
import json
from kivy.core.audio import SoundLoader
from core.facts import CrackFacts
from babel.support import Translations

class CrackLogic:
    """Handles cracking mechanics, stats, and sounds."""

    DEFAULT_COOLDOWN: int = 300  # 5 minutes in seconds

    def __init__(self, cooldown: int = DEFAULT_COOLDOWN, translations: Translations = None):
        """Initialize CrackLogic with custom cooldown and translations."""
        self.cooldown: int = cooldown
        self.last_crack: float = 0
        self.crack_count: int = 0
        self.translations = translations or Translations()
        self.sound = SoundLoader.load("assets/crack_sound.wav")
        self.facts = CrackFacts(self.translations)
        self.load_stats()

    def crack(self) -> Tuple[bool, str, str]:
        """
        Attempt to crack knuckles.

        Returns:
            Tuple[bool, str, str]: (Success status, Message, Fact or empty string)
        """
        current_time = time.time()
        if current_time - self.last_crack >= self.cooldown:
            self.last_crack = current_time
            self.crack_count += 1
            self.save_stats()
            if self.sound:
                self.sound.play()
            fact = self.facts.get_random_fact()
            return True, self.translations.gettext("Crack! 🎉 Total: {}").format(self.crack_count), fact
        remaining = int(self.cooldown - (current_time - self.last_crack))
        return False, self.translations.gettext("On cooldown! ⏳ Wait {} sec").format(remaining), ""

    def get_status(self) -> str:
        """Get current status of knuckle readiness."""
        current_time = time.time()
        if current_time - self.last_crack >= self.cooldown:
            return self.translations.gettext("Ready to crack! 🚀")
        remaining = int(self.cooldown - (current_time - self.last_crack))
        return self.translations.gettext("Cooldown: {} sec ⏰").format(remaining)

    def check_recharge(self) -> Optional[str]:
        """Check if knuckles are recharged and notify if so."""
        current_time = time.time()
        if current_time - self.last_crack >= self.cooldown and self.crack_count > 0:
            msg = self.translations.gettext("Fingers recharged! 💪 Crack again!")
            notification.notify(title="CrackMaster", message=msg)
            return msg
        return None

    def load_stats(self) -> None:
        """Load cracking stats from file."""
        try:
            with open("stats.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.crack_count = data.get("crack_count", 0)
        except FileNotFoundError:
            self.crack_count = 0

    def save_stats(self) -> None:
        """Save cracking stats to file."""
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump({"crack_count": self.crack_count}, f, ensure_ascii=False)