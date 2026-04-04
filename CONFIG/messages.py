# Messages Configuration - ENGLISH ONLY
import sys
import os

# Simplified English-only messages
class Messages(object):
    def __init__(self, user_id=None, language_code=None):
        """
        Initialize Messages with English language only
        """
        self.user_id = user_id
        self.language_code = 'en'  # Force English
        self._load_messages()
    
    def _load_messages(self):
        """Load all messages in English"""
        
        # Basic Messages
        self.MAGIC_ALL_MODULES_LOADED_MSG = "✅ All modules loaded successfully!"
        self.MAGIC_ALLOWED_GROUP_CHECK_LOG_MSG = "Group {chat_id} allowed: {allowed} | List: {list}"
        self.MAGIC_VID_HELP_TITLE_MSG = "<b>📹 /vid Command Help</b>\n\n"
        self.MAGIC_VID_HELP_USAGE_MSG = "<b>Usage:</b>\n<code>/vid &lt;url&gt;</code> or just send the URL directly\n\n"
        self.MAGIC_VID_HELP_EXAMPLES_MSG = "<b>Examples:</b>\n"
        self.MAGIC_VID_HELP_EXAMPLE_1_MSG = "• <code>/vid https://youtube.com/watch?v=... </code>\n"
        self.MAGIC_VID_HELP_EXAMPLE_2_MSG = "• <code>/vid 1-7 https://youtube.com/playlist?list=... </code> (download items 1-7 from playlist)\n"
        self.MAGIC_VID_HELP_EXAMPLE_3_MSG = "• <code>/vid -1-7 https://youtube.com/playlist?list=... </code> (download last 7 items)\n"
        self.MAGIC_VID_HELP_ALSO_SEE_MSG = "\n<b>Also see:</b> /help for more commands"
        self.MAGIC_HELP_CLOSED_MSG = "Help menu closed"
        self.MAGIC_CLEANUP_COMPLETED_MSG = "🧹 Cleanup completed"
        self.MAGIC_ERROR_DURING_CLEANUP_MSG = "⚠️ Error during cleanup: {error}"
        self.MAGIC_ERROR_CLOSING_LOGGER_MSG = "⚠️ Error closing logger: {error}"
        self.MAGIC_SIGNAL_RECEIVED_MSG = "📡 Signal {signal} received, shutting down gracefully..."
        
        # NSFW Messages
        self.NSFW_ON_MSG = "✅ NSFW blur is now <b>DISABLED</b> (content will be shown without blur)"
        self.NSFW_OFF_MSG = "🔞 NSFW blur is now <b>ENABLED</b> (content will be hidden with spoiler)"
        self.NSFW_INVALID_MSG = "❌ Invalid option! Use <code>/nsfw on</code> or <code>/nsfw off</code>"
        self.NSFW_ON_NO_BLUR_MSG = "✅ Disable Blur (Show Content)"
        self.NSFW_ON_NO_BLUR_INACTIVE_MSG = "✅ Disable Blur (Currently Active)"
        self.NSFW_OFF_BLUR_MSG = "🔞 Enable Blur (Hide Content)"
        self.NSFW_OFF_BLUR_INACTIVE_MSG = "🔞 Enable Blur (Currently Active)"
        self.NSFW_BLUR_SETTINGS_TITLE_MSG = "<b>🔞 NSFW Blur Settings</b>\n\nCurrent status: <code>{status}</code>\n\nChoose your preference:"
        self.NSFW_MENU_OPENED_LOG_MSG = "NSFW settings menu opened"
        self.NSFW_MENU_CLOSED_MSG = "NSFW settings closed"
        self.NSFW_MENU_CLOSED_LOG_MSG = "NSFW settings menu closed"
        self.NSFW_BLUR_DISABLED_MSG = "NSFW blur disabled"
        self.NSFW_BLUR_DISABLED_CALLBACK_MSG = "✅ Blur disabled - NSFW content will be visible"
        self.NSFW_BLUR_ENABLED_MSG = "NSFW blur enabled"
        self.NSFW_BLUR_ENABLED_CALLBACK_MSG = "🔞 Blur enabled - NSFW content will be hidden"
        self.NSFW_BLUR_SET_COMMAND_LOG_MSG = "NSFW blur set to {arg} via command"
        self.NSFW_USER_REQUESTED_COMMAND_LOG_MSG = "User {user_id} requested NSFW command"
        self.NSFW_USER_IS_ADMIN_LOG_MSG = "User {user_id} is admin: {is_admin}"
        self.NSFW_USER_IS_IN_CHANNEL_LOG_MSG = "User {user_id} is in channel: {is_in_channel}"
        
        # Porn Detection Messages
        self.PORN_DOMAIN_WHITELIST_MSG = "Domain in whitelist: {domain}"
        self.PORN_DOMAIN_BLACKLIST_MSG = "Domain in blacklist: {domain_parts}"
        self.PORN_ALL_TEXT_FIELDS_EMPTY_MSG = "All text fields empty"
        self.PORN_WHITELIST_KEYWORDS_MSG = "Whitelist keywords found: {keywords}"
        self.PORN_KEYWORDS_FOUND_MSG = "NSFW keywords found: {keywords}"
        self.PORN_NO_KEYWORDS_FOUND_MSG = "No NSFW keywords found"
        
        # URL Extractor Messages
        self.URL_EXTRACTOR_VID_HELP_CLOSE_BUTTON_MSG = "❌ Close"
        self.URL_EXTRACTOR_HELP_CLOSE_BUTTON_MSG = "❌ Close"
        
    def __getattr__(self, name):
        """
        Get message by name - always returns English message or placeholder
        """
        if name.startswith('_'):
            return super().__getattribute__(name)
        
        if hasattr(self, '_messages') and name in self._messages:
            return self._messages[name]
        
        # Return placeholder if message not found
        return f"[{name}]"


# Helper function to get Messages instance
def get_messages_instance(user_id=None, language_code=None):
    """
    Get Messages instance with English language only
    """
    return Messages(user_id, 'en')


# Safe function that NEVER fails
def safe_get_messages(user_id=None, language_code=None):
    """
    SAFE function that GUARANTEED returns a Messages object
    """
    try:
        return get_messages_instance(user_id, 'en')
    except Exception:
        return Messages(None, 'en')


# Ultra-safe function for any context
def safe_messages(user_id=None):
    """
    ULTRA-SAFE function that works in ANY context
    """
    try:
        return get_messages_instance(user_id, 'en')
    except:
        return Messages(None, 'en')


# Set user language (now does nothing - English only)
def set_user_language(user_id, language_code):
    """
    Language selection disabled - English only
    """
    return False


# Backward compatibility - create default English instance
messages = Messages(None, 'en')
