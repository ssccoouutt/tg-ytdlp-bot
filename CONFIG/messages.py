# Messages Configuration - English Only
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Direct import of English messages
from CONFIG.LANGUAGES.messages_EN import Messages as EnglishMessages

class Messages(object):
    def __init__(self, user_id=None, language_code=None):
        """Initialize Messages with English language only"""
        self.user_id = user_id
        self.language_code = 'en'
        self._en_messages = EnglishMessages()
    
    def __getattr__(self, name):
        """Get message from English messages file"""
        if hasattr(self._en_messages, name):
            value = getattr(self._en_messages, name)
            if isinstance(value, str):
                return self._format_message(value)
            return value
        # Fallback for missing messages
        return f"[{name}]"
    
    def _format_message(self, template: str) -> str:
        """Format message with placeholders from config"""
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
            return template


# Helper function to get Messages instance
def get_messages_instance(user_id=None, language_code=None):
    """Get Messages instance with English language only"""
    return Messages(user_id, 'en')


# Safe function that NEVER fails
def safe_get_messages(user_id=None, language_code=None):
    """SAFE function that GUARANTEED returns a Messages object"""
    try:
        return get_messages_instance(user_id, 'en')
    except Exception:
        return Messages(None, 'en')


# Ultra-safe function for any context
def safe_messages(user_id=None):
    """ULTRA-SAFE function that works in ANY context"""
    try:
        return get_messages_instance(user_id, 'en')
    except:
        return Messages(None, 'en')


# Set user language (now does nothing - English only)
def set_user_language(user_id, language_code):
    """Language selection disabled - English only"""
    return False


# Backward compatibility - create default English instance
messages = Messages(None, 'en')
