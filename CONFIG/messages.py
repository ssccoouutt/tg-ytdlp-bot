# Messages Configuration - English Only
import sys
import os

# Direct import of English messages
from CONFIG.LANGUAGES.messages_EN import Messages as EnglishMessages

class Messages(object):
    def __init__(self, user_id=None, language_code=None):
        self.user_id = user_id
        self.language_code = 'en'
        self._en_messages = EnglishMessages()
    
    def __getattr__(self, name):
        if hasattr(self._en_messages, name):
            value = getattr(self._en_messages, name)
            if isinstance(value, str):
                return self._format_message(value)
            return value
        return f"[{name}]"
    
    def _format_message(self, template: str) -> str:
        try:
            from CONFIG.config import Config
            # Get values from config with proper defaults
            required_channel = getattr(Config, "REQUIRED_CHANNEL_MENTION", "@Master_x_Bots")
            if not required_channel:
                required_channel = "@Master_x_Bots"
            
            managed_by = getattr(Config, "CREDITS_MANAGED_BY", "\n@itszeeshan196")
            if not managed_by:
                managed_by = "\n@itszeeshan196"
            
            credits_bots = getattr(Config, "CREDITS_BOTS", "@Master_x_Bots\n@TechZoneX")
            if not credits_bots:
                credits_bots = "@Master_x_Bots\n@TechZoneX"
            
            cost = str(getattr(Config, "NSFW_STAR_COST", 1))
            
            placeholders = {
                "required_channel": required_channel,
                "managed_by": managed_by,
                "credits_bots": credits_bots,
                "cost": cost
            }
            return template.format(**placeholders)
        except Exception as e:
            print(f"Format error: {e}")
            return template


def safe_get_messages(user_id=None, language_code=None):
    try:
        return Messages(user_id, 'en')
    except Exception:
        return Messages(None, 'en')


def set_user_language(user_id, language_code):
    return False


messages = Messages(None, 'en')
