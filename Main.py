import logging
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import google.generativeai as genai
import time


# --- Configuration ---
TELEGRAM_BOT_TOKEN = "Insert Telegram Bot Token"
GEMINI_API_KEY = "Insert Gemini API Token"
GEMINI_MODEL_NAME = "gemini-1.5-flash"

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Gemini API Initialization ---
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)

# --- Bot Initialization ---
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# --- User Data Storage ---
user_data = {}  # user_id: {settings}

# Constants
RATE_LIMIT = 3  # seconds
MAX_HISTORY = 20

# --- Translations ---
translations = {
    'welcome': {
        'en': "Hello {name}! I'm your AI assistant ",
        'ar': "مرحباً {name}! أنا مساعدك الذكي",
        'ku': "سڵاو {name}! من یاریدەدەری AI-م بۆ تۆم"
    },
    'commands': {
        'en': "\n\nCommands:\n/start - Restart\n/clear - Clear history\n/stats - Your stats\n/help - Help\n/language - Change language\n/feedback - Send feedback",
        'ar': "\n\nالأوامر:\n/start - إعادة التشغيل\n/clear - مسح المحادثة\n/stats - إحصائياتك\n/help - مساعدة\n/language - تغيير اللغة\n/feedback - إرسال ملاحظات",
        'ku': "\n\nفەرمانەکان:\n/start - دەستپێکردنەوە\n/clear - پاککردنەوەی مێژوو\n/stats - ئامارەکان\n/help - یارمەتی\n/language - گۆڕینی زمان\n/feedback - ناردنی ڕەخنە"
    },
    'cleared': {
        'en': "History cleared!",
        'ar': "تم مسح المحادثة!",
        'ku': "مێژوو پاککرایەوە!"
    },
    'stats': {
        'en': "📊 Stats:\nMessages: {count}\nLanguage: {lang}",
        'ar': "📊 الإحصائيات:\nالرسائل: {count}\nاللغة: {lang}",
        'ku': "📊 ئامارەکان:\nنامەکان: {count}\nزمان: {lang}"
    },
    'help': {
        'en': "ℹ️ I'm an AI assistant. I support multiple languages.",
        'ar': "ℹ️ أنا مساعد ذكي. أدعم عدة لغات.",
        'ku': "ℹ️ من یاریدەدەری AI-م. پشتیوانی چەند زمانێک دەکەم."
    },
    'rate_limit': {
        'en': "⏳ Please wait {seconds} seconds...",
        'ar': "⏳ انتظر {seconds} ثانية...",
        'ku': "⏳ تکایە {seconds} چرکە چاوەڕێ بکە..."
    },
    'language_set': {
        'en': "✅ Language set to English",
        'ar': "✅ تم تعيين اللغة إلى العربية",
        'ku': "✅ زمان گۆڕدرا بۆ کوردی"
    },
    'language_prompt': {
        'en': "🌍 Please choose your language:",
        'ar': "🌍 الرجاء اختيار لغتك:",
        'ku': "🌍 تکایە زمان هەڵبژێرە:"
    },
    'error': {
        'en': "❌ Error occurred. Please try again.",
        'ar': "❌ حدث خطأ. يرجى المحاولة مرة أخرى.",
        'ku': "❌ هەڵەیەک ڕوویدا. تکایە دووبارە هەوڵبدەرەوە."
    },
    'feedback_prompt': {
        'en': "📝 Please send your feedback or suggestions:",
        'ar': "📝 الرجاء إرسال ملاحظاتك أو اقتراحاتك:",
        'ku': "📝 تکایە ڕەخنە یان پێشنیارەکانت بنێرە:"
    },
    'feedback_thanks': {
        'en': "🙏 Thank you for your feedback!",
        'ar': "🙏 شكراً لك على ملاحظاتك!",
        'ku': "🙏 سوپاس بۆ ڕەخنەکەت!"
    },
    'voice_not_supported': {
        'en': "🔇 Voice messages are not supported yet.",
        'ar': "🔇 الرسائل الصوتية غير مدعومة حالياً.",
        'ku': "🔇 هێشتا پشتگیری نامەی دەنگی ناکرێت."
    },
    'admin_notified': {
        'en': "👤 Admin has been notified about your feedback.",
        'ar': "👤 تم إعلام المسؤول بملاحظاتك.",
        'ku': "👤 ئەدمین ئاگادارکرایەوە لە ڕەخنەکەت."
    }
}

# Admin ID for feedback notifications
ADMIN_ID = None  # Set your Telegram user ID here to receive feedback


# --- Helper Functions ---
def get_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'history': [],
            'message_count': 0,
            'last_message_time': 0,
            'language': 'ku',  # Default to Kurdish
            'waiting_for_feedback': False
        }
    return user_data[user_id]


def get_translation(key, user_id, **kwargs):
    lang = get_user_data(user_id)['language']
    text = translations.get(key, {}).get(lang, key)
    try:
        return text.format(**kwargs)
    except (KeyError, IndexError):
        logger.error(f"Failed to format translation for key '{key}' with args {kwargs}")
        return text


def create_language_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('English 🇬🇧')
    btn2 = types.KeyboardButton('العربية 🇸🇦')
    btn3 = types.KeyboardButton('کوردی (سۆرانی) 🇹🇯')
    markup.add(btn1, btn2, btn3)
    return markup


def create_main_menu_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    commands = [
        types.KeyboardButton('/help'),
        types.KeyboardButton('/clear'),
        types.KeyboardButton('/stats'),
        types.KeyboardButton('/language'),
        types.KeyboardButton('/feedback')
    ]
    markup.add(*commands)
    return markup


# --- Bot Handlers ---
@bot.message_handler(commands=['start'])
async def start_handler(message):
    user = message.from_user
    user_data = get_user_data(user.id)

    welcome = get_translation('welcome', user.id, name=user.first_name)
    commands = get_translation('commands', user.id)

    await bot.send_message(
        message.chat.id,
        welcome + commands,
        reply_markup=create_main_menu_keyboard(user.id)
    )


@bot.message_handler(commands=['help'])
async def help_handler(message):
    help_msg = get_translation('help', message.from_user.id)
    commands = get_translation('commands', message.from_user.id)
    await bot.send_message(
        message.chat.id,
        help_msg + commands,
        reply_markup=create_main_menu_keyboard(message.from_user.id)
    )


@bot.message_handler(commands=['clear'])
async def clear_handler(message):
    user_data = get_user_data(message.from_user.id)
    user_data['history'] = []
    await bot.send_message(
        message.chat.id,
        get_translation('cleared', message.from_user.id),
        reply_markup=create_main_menu_keyboard(message.from_user.id)
    )


@bot.message_handler(commands=['stats'])
async def stats_handler(message):
    user_data = get_user_data(message.from_user.id)
    lang_map = {'en': 'English', 'ar': 'العربية', 'ku': 'کوردی'}
    stats = get_translation('stats', message.from_user.id,
                            count=user_data['message_count'],
                            lang=lang_map[user_data['language']])
    await bot.send_message(
        message.chat.id,
        stats,
        reply_markup=create_main_menu_keyboard(message.from_user.id)
    )


@bot.message_handler(commands=['language'])
async def language_handler(message):
    await bot.send_message(
        message.chat.id,
        get_translation('language_prompt', message.from_user.id),
        reply_markup=create_language_keyboard()
    )


@bot.message_handler(commands=['feedback'])
async def feedback_handler(message):
    user_data = get_user_data(message.from_user.id)
    user_data['waiting_for_feedback'] = True
    await bot.send_message(
        message.chat.id,
        get_translation('feedback_prompt', message.from_user.id),
        reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda m: m.text in ["English 🇬🇧", "العربية 🇸🇦", "کوردی (سۆرانی) 🇹🇯"])
async def set_language_handler(message):
    user_data = get_user_data(message.from_user.id)

    if message.text == "English 🇬🇧":
        user_data['language'] = 'en'
    elif message.text == "العربية 🇸🇦":
        user_data['language'] = 'ar'
    else:
        user_data['language'] = 'ku'

    await bot.send_message(
        message.chat.id,
        get_translation('language_set', message.from_user.id),
        reply_markup=create_main_menu_keyboard(message.from_user.id)
    )


@bot.message_handler(content_types=['voice'])
async def voice_handler(message):
    await bot.send_message(
        message.chat.id,
        get_translation('voice_not_supported', message.from_user.id)
    )


@bot.message_handler(func=lambda m: True)
async def message_handler(message):
    user = message.from_user
    user_data = get_user_data(user.id)

    # Handle feedback
    if user_data.get('waiting_for_feedback'):
        user_data['waiting_for_feedback'] = False

        # Send thanks to user
        await bot.send_message(
            message.chat.id,
            get_translation('feedback_thanks', user.id),
            reply_markup=create_main_menu_keyboard(user.id)
        )

        # Notify admin if set
        if ADMIN_ID:
            feedback_msg = f"📩 New feedback from @{user.username} ({user.id}):\n\n{message.text}"
            await bot.send_message(ADMIN_ID, feedback_msg)
            await bot.send_message(
                message.chat.id,
                get_translation('admin_notified', user.id)
            )
        return

    # Rate limiting
    current_time = time.time()
    if current_time - user_data['last_message_time'] < RATE_LIMIT:
        remaining = RATE_LIMIT - (current_time - user_data['last_message_time'])
        await bot.send_message(
            message.chat.id,
            get_translation('rate_limit', user.id, seconds=round(remaining, 1)))
        return

    user_data['last_message_time'] = current_time
    user_data['message_count'] += 1

    # Add to history
    user_data['history'].append({"role": "user", "parts": [{"text": message.text}]})
    if len(user_data['history']) > MAX_HISTORY:
        user_data['history'] = user_data['history'][-MAX_HISTORY:]

    await bot.send_chat_action(message.chat.id, 'typing')

    try:
        chat = gemini_model.start_chat(history=user_data['history'])
        response = await asyncio.to_thread(chat.send_message, message.text)

        if response and response.text:
            reply = response.text
        else:
            reply = get_translation('error', user.id)

        user_data['history'].append({"role": "model", "parts": [{"text": reply}]})
        await bot.send_message(
            message.chat.id,
            reply,
            reply_markup=create_main_menu_keyboard(user.id)
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await bot.send_message(
            message.chat.id,
            get_translation('error', user.id),
            reply_markup=create_main_menu_keyboard(user.id)
        )


# --- Main ---
async def main():
    logger.info("Starting bot...")
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(main())
