# Messages Configuration - ENGLISH ONLY (Hardcoded)
import sys
import os

class Messages(object):
    def __init__(self, user_id=None, language_code=None):
        """Initialize Messages with English language only"""
        self.user_id = user_id
        self.language_code = 'en'
    
    def __getattr__(self, name):
        """Return hardcoded English messages"""
        
        # Basic Messages
        if name == "MAGIC_ALL_MODULES_LOADED_MSG":
            return "✅ All modules loaded successfully!"
        if name == "MAGIC_ALLOWED_GROUP_CHECK_LOG_MSG":
            return "Group {chat_id} allowed: {allowed} | List: {list}"
        if name == "MAGIC_VID_HELP_TITLE_MSG":
            return "<b>📹 /vid Command Help</b>\n\n"
        if name == "MAGIC_VID_HELP_USAGE_MSG":
            return "<b>Usage:</b>\n<code>/vid &lt;url&gt;</code> or just send the URL directly\n\n"
        if name == "MAGIC_VID_HELP_EXAMPLES_MSG":
            return "<b>Examples:</b>\n"
        if name == "MAGIC_VID_HELP_EXAMPLE_1_MSG":
            return "• <code>/vid https://youtube.com/watch?v=... </code>\n"
        if name == "MAGIC_VID_HELP_EXAMPLE_2_MSG":
            return "• <code>/vid 1-7 https://youtube.com/playlist?list=... </code> (download items 1-7 from playlist)\n"
        if name == "MAGIC_VID_HELP_EXAMPLE_3_MSG":
            return "• <code>/vid -1-7 https://youtube.com/playlist?list=... </code> (download last 7 items)\n"
        if name == "MAGIC_VID_HELP_ALSO_SEE_MSG":
            return "\n<b>Also see:</b> /help for more commands"
        if name == "MAGIC_HELP_CLOSED_MSG":
            return "Help menu closed"
        if name == "MAGIC_CLEANUP_COMPLETED_MSG":
            return "🧹 Cleanup completed"
        if name == "MAGIC_ERROR_DURING_CLEANUP_MSG":
            return "⚠️ Error during cleanup: {error}"
        if name == "MAGIC_ERROR_CLOSING_LOGGER_MSG":
            return "⚠️ Error closing logger: {error}"
        if name == "MAGIC_SIGNAL_RECEIVED_MSG":
            return "📡 Signal {signal} received, shutting down gracefully..."
        
        # NSFW Messages
        if name == "NSFW_ON_MSG":
            return "✅ NSFW blur is now <b>DISABLED</b> (content will be shown without blur)"
        if name == "NSFW_OFF_MSG":
            return "🔞 NSFW blur is now <b>ENABLED</b> (content will be hidden with spoiler)"
        if name == "NSFW_INVALID_MSG":
            return "❌ Invalid option! Use <code>/nsfw on</code> or <code>/nsfw off</code>"
        if name == "NSFW_ON_NO_BLUR_MSG":
            return "✅ Disable Blur (Show Content)"
        if name == "NSFW_ON_NO_BLUR_INACTIVE_MSG":
            return "✅ Disable Blur (Currently Active)"
        if name == "NSFW_OFF_BLUR_MSG":
            return "🔞 Enable Blur (Hide Content)"
        if name == "NSFW_OFF_BLUR_INACTIVE_MSG":
            return "🔞 Enable Blur (Currently Active)"
        if name == "NSFW_BLUR_SETTINGS_TITLE_MSG":
            return "<b>🔞 NSFW Blur Settings</b>\n\nCurrent status: <code>{status}</code>\n\nChoose your preference:"
        if name == "NSFW_MENU_OPENED_LOG_MSG":
            return "NSFW settings menu opened"
        if name == "NSFW_MENU_CLOSED_MSG":
            return "NSFW settings closed"
        if name == "NSFW_MENU_CLOSED_LOG_MSG":
            return "NSFW settings menu closed"
        if name == "NSFW_BLUR_DISABLED_MSG":
            return "NSFW blur disabled"
        if name == "NSFW_BLUR_DISABLED_CALLBACK_MSG":
            return "✅ Blur disabled - NSFW content will be visible"
        if name == "NSFW_BLUR_ENABLED_MSG":
            return "NSFW blur enabled"
        if name == "NSFW_BLUR_ENABLED_CALLBACK_MSG":
            return "🔞 Blur enabled - NSFW content will be hidden"
        if name == "NSFW_BLUR_SET_COMMAND_LOG_MSG":
            return "NSFW blur set to {arg} via command"
        if name == "NSFW_USER_REQUESTED_COMMAND_LOG_MSG":
            return "User {user_id} requested NSFW command"
        if name == "NSFW_USER_IS_ADMIN_LOG_MSG":
            return "User {user_id} is admin: {is_admin}"
        if name == "NSFW_USER_IS_IN_CHANNEL_LOG_MSG":
            return "User {user_id} is in channel: {is_in_channel}"
        
        # TO_USE_MSG and CREDITS_MSG - THESE ARE THE IMPORTANT ONES
        if name == "TO_USE_MSG":
            return "🔞 <b>NSFW Content Detected</b>\n\nThis content requires a one-time payment of {cost} Telegram Stars to access."
        if name == "CREDITS_MSG":
            return "\n\n<i>Powered by @Master_x_Bots</i>"
        if name == "CHANNEL_JOIN_BUTTON_MSG":
            return "📢 Join Channel"
        
        # HELP Message
        if name == "HELP_MSG":
            return """
<b>🤖 Bot Commands</b>

<b>📹 Download Commands:</b>
• Send any video URL directly
• /vid &lt;url&gt; - Download video
• /audio &lt;url&gt; - Download audio only
• /link &lt;quality&gt; &lt;url&gt; - Get direct stream link

<b>⚙️ Settings:</b>
• /settings - Open settings menu
• /format &lt;quality&gt; - Set video quality
• /split &lt;size&gt; - Set split size (e.g., 500mb)
• /nsfw - NSFW blur settings

<b>🍪 Cookies:</b>
• /cookie - Download cookies for restricted content
• /check_cookie - Validate cookies

<b>ℹ️ Info:</b>
• /usage - Your download statistics
• /help - Show this message
"""
        
        # Settings Messages
        if name == "SETTINGS_TITLE_MSG":
            return "<b>⚙️ Settings Menu</b>\n\nChoose an option below:"
        if name == "SETTINGS_CLEAN_BUTTON_MSG":
            return "🧹 Clean"
        if name == "SETTINGS_COOKIES_BUTTON_MSG":
            return "🍪 Cookies"
        if name == "SETTINGS_MEDIA_BUTTON_MSG":
            return "🎬 Media"
        if name == "SETTINGS_INFO_BUTTON_MSG":
            return "📊 Info"
        if name == "SETTINGS_MORE_BUTTON_MSG":
            return "🔧 More"
        if name == "SETTINGS_LANGUAGE_BUTTON_MSG":
            return "🌐 Language"
        if name == "SETTINGS_DEV_GITHUB_BUTTON_MSG":
            return "⭐ Star"
        if name == "SETTINGS_CONTR_GITHUB_BUTTON_MSG":
            return "👤 Dev"
        if name == "SETTINGS_MENU_OPENED_MSG":
            return "Settings menu opened"
        if name == "SETTINGS_MENU_CLOSED_MSG":
            return "Settings menu closed"
        if name == "SETTINGS_COMMAND_EXECUTED_MSG":
            return "✅ Command executed"
        if name == "SETTINGS_FLOOD_LIMIT_MSG":
            return "⏳ Too many requests! Please wait a moment."
        if name == "SETTINGS_FLOOD_WAIT_ACTIVE_MSG":
            return "⏳ Flood wait active. Please wait."
        if name == "SETTINGS_HINT_SENT_MSG":
            return "ℹ️ Help message sent"
        if name == "SETTINGS_HINT_CLOSED_MSG":
            return "Closed"
        if name == "SETTINGS_UNKNOWN_COMMAND_MSG":
            return "Unknown command"
        if name == "SETTINGS_CLEAN_TITLE_MSG":
            return "<b>🧹 Clean Settings</b>\n\nChoose what to clean:"
        if name == "SETTINGS_COOKIES_TITLE_MSG":
            return "<b>🍪 Cookie Settings</b>\n\nManage your cookies:"
        if name == "SETTINGS_MEDIA_TITLE_MSG":
            return "<b>🎬 Media Settings</b>\n\nConfigure media options:"
        if name == "SETTINGS_LOGS_TITLE_MSG":
            return "<b>📊 Information</b>\n\nView your stats and info:"
        if name == "SETTINGS_MORE_TITLE_MSG":
            return "<b>🔧 More Options</b>\n\nAdvanced settings:"
        if name == "SETTINGS_CLEAN_OPTIONS_MSG":
            return "<b>🧹 Clean Options</b>\n\nSelect what to clean:"
        
        # Clean options
        if name == "SETTINGS_COOKIES_ONLY_BUTTON_MSG":
            return "🍪 Cookies"
        if name == "SETTINGS_LOGS_BUTTON_MSG":
            return "📊 Logs"
        if name == "SETTINGS_TAGS_BUTTON_MSG":
            return "🏷️ Tags"
        if name == "SETTINGS_FORMAT_BUTTON_MSG":
            return "🎬 Format"
        if name == "SETTINGS_SPLIT_BUTTON_MSG":
            return "✂️ Split"
        if name == "SETTINGS_MEDIAINFO_BUTTON_MSG":
            return "ℹ️ MediaInfo"
        if name == "SETTINGS_SUBTITLES_BUTTON_MSG":
            return "💬 Subtitles"
        if name == "SETTINGS_KEYBOARD_BUTTON_MSG":
            return "⌨️ Keyboard"
        if name == "SETTINGS_ARGS_BUTTON_MSG":
            return "🔧 Args"
        if name == "SETTINGS_NSFW_BUTTON_MSG":
            return "🔞 NSFW"
        if name == "SETTINGS_PROXY_BUTTON_MSG":
            return "🌐 Proxy"
        if name == "SETTINGS_FLOOD_WAIT_BUTTON_MSG":
            return "⏳ Flood Wait"
        if name == "SETTINGS_ALL_FILES_BUTTON_MSG":
            return "🗑️ All Files"
        
        # Command buttons
        if name == "SETTINGS_FORMAT_CMD_BUTTON_MSG":
            return "🎬 /format"
        if name == "SETTINGS_MEDIAINFO_CMD_BUTTON_MSG":
            return "ℹ️ /mediainfo"
        if name == "SETTINGS_SPLIT_CMD_BUTTON_MSG":
            return "✂️ /split"
        if name == "SETTINGS_AUDIO_CMD_BUTTON_MSG":
            return "🎵 /audio"
        if name == "SETTINGS_SUBS_CMD_BUTTON_MSG":
            return "💬 /subs"
        if name == "SETTINGS_PLAYLIST_CMD_BUTTON_MSG":
            return "📋 /playlist"
        if name == "SETTINGS_IMG_CMD_BUTTON_MSG":
            return "🖼️ /img"
        if name == "SETTINGS_TAGS_CMD_BUTTON_MSG":
            return "🏷️ /tags"
        if name == "SETTINGS_HELP_CMD_BUTTON_MSG":
            return "❓ /help"
        if name == "SETTINGS_USAGE_CMD_BUTTON_MSG":
            return "📊 /usage"
        if name == "SETTINGS_PLAYLIST_HELP_CMD_BUTTON_MSG":
            return "📋 Playlist Help"
        if name == "SETTINGS_ADD_BOT_CMD_BUTTON_MSG":
            return "➕ Add to Group"
        if name == "SETTINGS_LINK_CMD_BUTTON_MSG":
            return "🔗 /link"
        if name == "SETTINGS_PROXY_CMD_BUTTON_MSG":
            return "🌐 /proxy"
        if name == "SETTINGS_KEYBOARD_CMD_BUTTON_MSG":
            return "⌨️ /keyboard"
        if name == "SETTINGS_SEARCH_CMD_BUTTON_MSG":
            return "🔍 Search"
        if name == "SETTINGS_ARGS_CMD_BUTTON_MSG":
            return "🔧 /args"
        if name == "SETTINGS_NSFW_CMD_BUTTON_MSG":
            return "🔞 /nsfw"
        if name == "SETTINGS_DOWNLOAD_COOKIE_BUTTON_MSG":
            return "📥 /cookie"
        if name == "SETTINGS_COOKIES_FROM_BROWSER_BUTTON_MSG":
            return "🌐 /cookies_from_browser"
        if name == "SETTINGS_CHECK_COOKIE_BUTTON_MSG":
            return "✅ /check_cookie"
        if name == "SETTINGS_SAVE_AS_COOKIE_BUTTON_MSG":
            return "💾 /save_as_cookie"
        
        # Other messages
        if name == "SUBS_BACK_BUTTON_MSG":
            return "◀️ Back"
        if name == "URL_EXTRACTOR_HELP_CLOSE_BUTTON_MSG":
            return "❌ Close"
        if name == "URL_EXTRACTOR_VID_HELP_CLOSE_BUTTON_MSG":
            return "❌ Close"
        if name == "COMMAND_IMAGE_HELP_CLOSE_BUTTON_MSG":
            return "❌ Close"
        if name == "OTHER_AUDIO_HINT_CLOSE_BUTTON_MSG":
            return "❌ Close"
        if name == "URL_EXTRACTOR_SAVE_AS_COOKIE_HINT_CLOSE_BUTTON_MSG":
            return "❌ Close"
        if name == "SETTINGS_MOBILE_ACTIVATE_SEARCH_MSG":
            return "📱 Activate Search"
        
        # Search message
        if name == "SEARCH_MSG":
            return "<b>🔍 Inline Search</b>\n\nTo search YouTube, type <code>@bot_name query</code> in any chat.\n\nExample: <code>@Master_dl_Bot never gonna give you up</code>"
        
        # Audio help
        if name == "AUDIO_HELP_MSG":
            return "<b>🎵 Audio Download</b>\n\nSend a video URL or use <code>/audio &lt;url&gt;</code>\n\nExample: <code>/audio https://youtube.com/watch?v=...</code>"
        
        # Link hint
        if name == "LINK_HINT_MSG":
            return "<b>🔗 Direct Link</b>\n\nUse <code>/link &lt;quality&gt; &lt;url&gt;</code>\n\nExample: <code>/link 720 https://youtube.com/watch?v=...</code>"
        
        # IMG help
        if name == "IMG_HELP_MSG":
            return "<b>🖼️ Image Download</b>\n\nSend an image URL or use <code>/img &lt;url&gt;</code>\n\nSupports Instagram, Twitter, Reddit, and more."
        
        # Save as cookie hint
        if name == "SAVE_AS_COOKIE_HINT":
            return "<b>🍪 Save Cookie File</b>\n\nSend a .txt file in Netscape cookie format.\n\nExport cookies using Cookie-Editor extension."
        
        # Porn messages
        if name == "PORN_DOMAIN_WHITELIST_MSG":
            return "Domain in whitelist: {domain}"
        if name == "PORN_DOMAIN_BLACKLIST_MSG":
            return "Domain in blacklist: {domain_parts}"
        if name == "PORN_ALL_TEXT_FIELDS_EMPTY_MSG":
            return "All text fields empty"
        if name == "PORN_WHITELIST_KEYWORDS_MSG":
            return "Whitelist keywords found: {keywords}"
        if name == "PORN_KEYWORDS_FOUND_MSG":
            return "NSFW keywords found: {keywords}"
        if name == "PORN_NO_KEYWORDS_FOUND_MSG":
            return "No NSFW keywords found"
        
        # Helper messages
        if name == "HELPER_APP_INSTANCE_NONE_MSG":
            return "❌ App instance not available"
        if name == "HELPER_APP_INSTANCE_NOT_AVAILABLE_MSG":
            return "App instance not available"
        if name == "HELPER_USER_NAME_MSG":
            return "User"
        if name == "HELPER_CHECK_FILE_SIZE_LIMIT_INFO_DICT_NONE_MSG":
            return "Warning: info_dict is None in file size check"
        if name == "HELPER_CHECK_SUBS_LIMITS_INFO_DICT_NONE_MSG":
            return "Warning: info_dict is None in subs limits check"
        if name == "HELPER_CHECK_SUBS_LIMITS_CHECKING_LIMITS_MSG":
            return "Checking subtitle limits: max_quality={max_quality}, max_duration={max_duration}, max_size={max_size}"
        if name == "HELPER_CHECK_SUBS_LIMITS_INFO_DICT_KEYS_MSG":
            return "Info dict keys: {keys}"
        if name == "HELPER_SUBTITLE_EMBEDDING_SKIPPED_DURATION_MSG":
            return "Subtitle embedding skipped: duration {duration}s > {max_duration}s"
        if name == "HELPER_SUBTITLE_EMBEDDING_SKIPPED_SIZE_MSG":
            return "Subtitle embedding skipped: size {size_mb:.1f}MB > {max_size}MB"
        if name == "HELPER_SUBTITLE_EMBEDDING_SKIPPED_QUALITY_MSG":
            return "Subtitle embedding skipped: resolution {width}x{height}, min_side {min_side} > {max_quality}"
        if name == "HELPER_MESSAGE_ID_INVALID_MSG":
            return "message_id"
        if name == "HELPER_MESSAGE_DELETE_FORBIDDEN_MSG":
            return "can't delete"
        if name == "HELPER_ADMIN_RIGHTS_REQUIRED_MSG":
            return "⚠️ <b>Admin Rights Required</b>\n\nPlease make me an admin in this group to function properly."
        if name == "HELPER_RANGE_LIMIT_EXCEEDED_MSG":
            return "⚠️ <b>Range limit exceeded</b>\n\nYou requested {count} items from {service}, but the maximum is {max_count}.\n\nTry this range instead:\n<code>{suggested_command_url_format}</code>\n\nOr use the command format:\n"
        if name == "HELPER_RANGE_LIMIT_EXCEEDED_LOG_MSG":
            return "Range limit exceeded: {service} user {user_id} requested {count} items (max {max_count})"
        if name == "HELPER_COMMAND_TYPE_TIKTOK_MSG":
            return "TikTok"
        if name == "HELPER_COMMAND_TYPE_INSTAGRAM_MSG":
            return "Instagram"
        if name == "HELPER_COMMAND_TYPE_PLAYLIST_MSG":
            return "playlist"
        if name == "HELPER_FLOOD_LIMIT_TRY_LATER_MSG":
            return "⏳ Too many requests! Please try again later."
        if name == "HELPER_FLOOD_WAIT_DETECTED_SLEEPING_MSG":
            return "Flood wait detected, sleeping {wait_seconds} seconds..."
        if name == "HELPER_FLOOD_WAIT_DETECTED_COULDNT_EXTRACT_MSG":
            return "Flood wait detected, sleeping {retry_delay} seconds..."
        if name == "HELPER_MSG_SEQNO_ERROR_DETECTED_MSG":
            return "msg_seqno error detected, sleeping {retry_delay} seconds..."
        
        # Settings messages continued
        if name == "SETTINGS_HELP_SENT_MSG":
            return "Help message sent"
        if name == "SETTINGS_SEARCH_HELPER_OPENED_MSG":
            return "Search helper opened"
        
        # Logger messages
        if name == "LIMITTER_CHANNEL_CHECK_MEMBERSHIP_LOG_MSG":
            return "Checking channel membership for user {user_id} in channel {channel}"
        if name == "LIMITTER_CHANNEL_CHECK_STATUS_LOG_MSG":
            return "User {user_id} channel status: {status}"
        if name == "LIMITTER_CHANNEL_CHECK_IS_MEMBER_LOG_MSG":
            return "User {user_id} is a member of the channel"
        if name == "LIMITTER_CHANNEL_CHECK_NOT_MEMBER_LOG_MSG":
            return "User {user_id} is NOT a member of the channel"
        if name == "LIMITTER_CHANNEL_CHECK_ERROR_LOG_MSG":
            return "Error checking channel membership for user {user_id}: {error}"
        if name == "LIMITTER_SUBTITLE_LIMITS_CHECK_PASSED_LOG_MSG":
            return "Subtitle limits check passed: duration={duration}, size={size}, resolution={width}x{height}"
        if name == "LIMITTER_SUBTITLE_LIMITS_CHECK_ERROR_LOG_MSG":
            return "Error in subtitle limits check: {error}"
        
        # Default fallback
        return f"[{name}]"


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
