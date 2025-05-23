# 🤖 Multilingual AI Telegram Bot

> 🌍 A powerful, intelligent Telegram bot powered by Google Gemini AI with support for multiple languages

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

### 🎯 Core Functionality
- 🧠 **AI-Powered Conversations** - Intelligent responses using Google Gemini 1.5 Flash
- 🌐 **Multilingual Support** - Seamlessly supports English, Arabic, and Kurdish (Sorani)
- 💬 **Context-Aware Chat** - Maintains conversation history for natural interactions
- ⚡ **Asynchronous Processing** - High-performance async architecture for multiple users

### 🛡️ Smart Protection
- 🚫 **Rate Limiting** - Anti-spam protection with customizable delays
- 📊 **Usage Statistics** - Track user engagement and bot performance
- 🔒 **Error Handling** - Robust error management for stable operation

### 🎨 User Experience
- ⌨️ **Custom Keyboards** - Intuitive interface with quick-access buttons
- 🌍 **Language Switching** - Easy language selection with flag emojis
- 📝 **Feedback System** - Direct user feedback collection with admin notifications
- 📈 **Personal Stats** - Individual user statistics and preferences

## 🚀 Quick Start

### Prerequisites
- 🐍 Python 3.8 or higher
- 📱 Telegram Bot Token from [@BotFather](https://t.me/botfather)
- 🔑 Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multilingual-ai-telegram-bot.git
   cd multilingual-ai-telegram-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your bot**
   ```python
   # Update these in the code or use environment variables
   TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ADMIN_ID = your_telegram_user_id  # Optional: for feedback notifications
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## 🎮 Commands

| Command | Description | Available In |
|---------|-------------|--------------|
| `/start` | 🚀 Initialize bot and show welcome message | All languages |
| `/help` | ❓ Display help information and commands | All languages |
| `/clear` | 🗑️ Clear conversation history | All languages |
| `/stats` | 📊 Show personal usage statistics | All languages |
| `/language` | 🌐 Change bot language | All languages |
| `/feedback` | 💌 Send feedback to administrators | All languages |

## 🌍 Supported Languages

- 🇬🇧 **English** - Full support with natural conversations
- 🇸🇦 **Arabic** - Complete RTL language support
- 🏴󠁫󠁧󠁫󠁵󠁲󠁿 **Kurdish (Sorani)** - Native Kurdish language support

## 🏗️ Architecture

```
📂 Bot Structure
├── 🤖 Main Bot Instance (AsyncTeleBot)
├── 🧠 AI Integration (Google Gemini)
├── 🌐 Translation System
├── 💾 User Data Management
├── ⌨️ Custom Keyboards
└── 📝 Command Handlers
```

### 🔧 Key Components

- **🎯 Message Handlers** - Process different types of user inputs
- **🌐 Translation Engine** - Dynamic multilingual content delivery
- **💾 Data Storage** - In-memory user data management
- **🛡️ Rate Limiting** - Prevents spam and API abuse
- **📊 Statistics Tracking** - User engagement metrics

## 📋 Requirements

```txt
pyTelegramBotAPI==4.14.0
google-generativeai==0.3.2
asyncio
logging
time
```

## ⚙️ Configuration

### Environment Variables (Recommended)
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export GEMINI_API_KEY="your_api_key"
export ADMIN_ID="your_telegram_id"
```

### Bot Settings
```python
RATE_LIMIT = 3        # Seconds between messages
MAX_HISTORY = 20      # Maximum conversation context
GEMINI_MODEL = "gemini-1.5-flash"  # AI model version
```

## 🎨 Customization

### Adding New Languages
1. Add translations to the `translations` dictionary
2. Update language keyboard with new options
3. Include language mapping in statistics

### Modifying AI Behavior
- Adjust `MAX_HISTORY` for longer/shorter context
- Change `GEMINI_MODEL_NAME` for different AI capabilities
- Customize system prompts for specific use cases

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| 🚫 Bot not responding | Check token validity and network connection |
| 🔴 AI errors | Verify Gemini API key and quota limits |
| 💾 Memory issues | Implement database storage for production |
| 🌐 Translation problems | Verify language codes and text formatting |

## 📊 Performance Features

- ⚡ **Async Architecture** - Non-blocking operations for multiple users
- 💾 **Memory Management** - Automatic history trimming
- 🔄 **Error Recovery** - Graceful handling of API failures
- 📈 **Scalable Design** - Ready for high-traffic deployment

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. ✅ Test thoroughly
5. 📤 Commit changes (`git commit -m 'Add amazing feature'`)
6. 🚀 Push to branch (`git push origin feature/amazing-feature`)
7. 🎯 Open a Pull Request

### 🎯 Areas for Contribution
- 🌍 Additional language support
- 🎨 UI/UX improvements
- 📊 Database integration
- 🔧 Performance optimizations
- 📝 Documentation enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🤖 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Excellent Telegram Bot framework
- 🧠 [Google Gemini AI](https://ai.google.dev/) - Powerful AI capabilities
- 🌍 Community translators for multilingual support
- 💻 Open source community for inspiration and feedback

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/repo/discussions)
- 📧 **Email**: your.email@example.com

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/repo?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/repo?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/repo)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/repo)

---

<div align="center">

**🌟 If you found this project helpful, please give it a star! 🌟**

Made with ❤️ by [Diyar Penjweny](https://github.com/diyar-penjweny)<br>
Programming Tutorial Video [Smart Code کۆدی زیرەک]([https://github.com/diyar-penjweny](https://www.youtube.com/@SmartCode-d2p))

</div>
