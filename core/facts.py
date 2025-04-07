"""Interesting facts about knuckle cracking."""

import random
from babel.support import Translations

class CrackFacts:
    """Provides random facts about knuckle cracking with translations."""

    FACTS: list[str] = [
        "Knuckle-cracking doesn’t cause arthritis! It’s just gas bubbles collapsing. 🧪",
        "Scientists say cracking knuckles is harmless. Crack away! ✅",
        "25-54% of people crack their knuckles. You’re not alone! 👥",
        "The sound can reach 83 decibels — like a loud conversation! 🔊",
        "Cracking doesn’t weaken your grip, it’s a myth! 💪",
        "Knuckle-cracking dates back to ancient texts! 📜",
        "The crack is gas bubbles popping in the joint! 🌬️",
        "Some crack knuckles to relieve stress! 😌",
        "You can crack up to 20 times a day safely! 🔢",
        "The loudest crack was recorded in 2018! 🎤"
    ]

    def __init__(self, translations: Translations):
        """Initialize with translations."""
        self.translations = translations

    def get_random_fact(self) -> str:
        """Return a random translated fact."""
        fact = random.choice(self.FACTS)
        return self.translations.gettext(fact)