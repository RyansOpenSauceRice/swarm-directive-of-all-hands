import gettext
import os
import json
from pathlib import Path

class Localization:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.locale_dir = Path(__file__).parent.parent / 'locales'
        self.translations = {}
        self.current_language = self.config['i18n']['default_language']
        
        self._setup_translations()

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _setup_translations(self):
        for lang in self.config['i18n']['available_languages']:
            try:
                translation = gettext.translation(
                    'messages',
                    localedir=str(self.locale_dir),
                    languages=[lang]
                )
                self.translations[lang] = translation
            except FileNotFoundError:
                continue

        self.set_language(self.current_language)

    def set_language(self, language_code):
        if language_code in self.translations:
            self.translations[language_code].install()
            self.current_language = language_code
            return True
        return False

    def get_available_languages(self):
        return self.config['i18n']['available_languages']

    def gettext(self, message):
        return _(message)

# Initialize global _ function
_ = gettext.gettext