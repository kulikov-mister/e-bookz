from translations import LANGUAGES, DEFAULT_LANGUAGE
import database

def get_preferred_language(user_id, language_code_from_telegram):
    lang_from_telegram = language_code_from_telegram
    lang_from_db = database.get_user_language(user_id)

    if lang_from_telegram in LANGUAGES:
        return lang_from_telegram
    elif lang_from_db in LANGUAGES:
        return lang_from_db
    else:
        return DEFAULT_LANGUAGE

