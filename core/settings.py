"""Settings management for CrackMaster."""

from typing import Dict, Union
import json

class Settings:
    """Manages application settings including language."""

    DEFAULTS: Dict[str, Union[int, str]] = {
        "cooldown": 300,  # 5 minutes
        "theme": 1,       # 1 = Dark, 2 = Light
        "language": "ru"  # Default language
    }

    def __init__(self):
        """Initialize settings with defaults."""
        self.settings: Dict[str, Union[int, str]] = self.load_settings()

    def load_settings(self) -> Dict[str, Union[int, str]]:
        """Load settings from file or return defaults."""
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.DEFAULTS.copy()

    def save_settings(self) -> None:
        """Save settings to file."""
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False)

    def get_cooldown(self) -> int:
        """Get current cooldown value."""
        return self.settings["cooldown"]

    def set_cooldown(self, value: int) -> None:
        """Set new cooldown value."""
        self.settings["cooldown"] = value
        self.save_settings()

    def get_language(self) -> str:
        """Get current language."""
        return self.settings["language"]

    def set_language(self, language: str) -> None:
        """Set new language."""
        self.settings["language"] = language
        self.save_settings()