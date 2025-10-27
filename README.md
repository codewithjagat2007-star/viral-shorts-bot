# 🎬 Viral Shorts Bot with ElevenLabs Voice

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-orange)

> **Automated YouTube Shorts creation bot with ultra-realistic AI voice powered by ElevenLabs API**

Create professional, engaging YouTube Shorts automatically with 3D Pixar-style animations, ultra-realistic Hindi voiceovers, and viral-optimized metadata.

---

## ✨ Features

### 🎙️ **Ultra-Realistic Voice**
- **ElevenLabs AI Voice** - Human-like male Hindi voice
- 5 professional voice options (randomly selected)
- Natural intonation and emotional expression
- 1.7x-2.0x speed optimization for shorts
- Professional audio enhancement

### 🎨 **Professional Animations**
- 3D Pixar/Disney style characters
- 10-14 animated scenes per video
- Emotion-based animations (happy, sad, excited, etc.)
- Dynamic camera movements (zoom, pan, motion)
- Stability AI image-to-video conversion

### 📊 **Viral Optimization**
- SEO-optimized titles with emojis
- Trending hashtags automatically added
- Engaging descriptions with call-to-actions
- Strategic tags for maximum reach
- 50-60 second perfect length

### 🚀 **Automation**
- Auto story generation using Gemini AI
- Automatic thumbnail creation
- YouTube auto-upload functionality
- Background music mixing
- Batch video creation

---

## 📸 Preview

```
📱 Video Output:
├── Resolution: 1080x1920 (9:16 vertical)
├── Duration: 50-60 seconds
├── Scenes: 10-14 animated scenes
├── Voice: Ultra-realistic male Hindi
├── Music: Soft background music
└── Format: MP4 (optimized for YouTube)
```

---

## 🔧 Requirements

### Software
- **Python**: 3.8 or higher
- **FFmpeg**: For video processing
- **Termux**: For Android (or Linux)
- **Git**: For version control

### API Keys (Required)
- **ElevenLabs API Key** - [Get Free API Key](https://elevenlabs.io)
- **Google Gemini API Key** - Story generation
- **Stability AI API Key** - Image-to-video (optional)
- **YouTube API Credentials** - Auto-upload (optional)

---

## 📦 Installation

### Method 1: Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade -y

# Install required packages
pkg install python git ffmpeg -y

# Clone repository
git clone https://github.com/codewithjagat2007-star/viral-shorts-bot.git

# Navigate to directory
cd viral-shorts-bot

# Install Python dependencies
pip install -r requirements.txt

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Method 2: Linux/Ubuntu

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip git ffmpeg -y

# Clone repository
git clone https://github.com/codewithjagat2007-star/viral-shorts-bot.git

# Navigate to directory
cd viral-shorts-bot

# Install Python packages
pip3 install -r requirements.txt

# Run setup
chmod +x setup.sh
./setup.sh
```

---

## 🔑 Configuration

### 1️⃣ Get ElevenLabs API Key

1. Visit [ElevenLabs](https://elevenlabs.io)
2. Sign up for free account (10,000 chars/month)
3. Go to Settings → API Keys
4. Copy your API key

### 2️⃣ Configure Script

Open `animation_bot.py` and add your API keys:

```python
# Line 17-18
self.elevenlabs_key = "sk-your-elevenlabs-api-key-here"
self.gemini_key = "your-gemini-api-key-here"
```

### 3️⃣ Setup YouTube Credentials (Optional)

For automatic YouTube upload:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials
5. Download `client_secrets.json`
6. Place in `~/youtube-bot/credentials/`

**Note:** Without YouTube credentials, videos will be saved locally to `/sdcard/YouTube_Videos/`

---

## 🚀 Usage

### Basic Usage

```bash
# Navigate to project directory
cd ~/viral-shorts-bot

# Run the bot
python animation_bot.py

# Follow prompts
# Enter number of videos to create (e.g., 5)
```

### Advanced Usage

```python
# Custom video creation
from animation_bot import ViralShortsBot

bot = ViralShortsBot()
bot.authenticate_youtube()  # Optional

# Create single video
bot.create_and_upload_video(video_number=1)

# Create multiple videos
for i in range(1, 11):  # Create 10 videos
    bot.create_and_upload_video(video_number=i)
    time.sleep(300)  # Wait 5 minutes between uploads
```

---

## 🎙️ Voice Options

The bot includes 5 professional male voices:

| Voice | Characteristics | Best For |
|-------|----------------|----------|
| **Adam** | Deep, authoritative | Serious stories, wisdom |
| **Josh** | Clear, energetic | Motivational content |
| **Sam** | Warm, friendly | Emotional stories |
| **Arnold** | Strong, confident | Success stories |
| **Roger** | Professional, engaging | Life lessons |

Voice is **randomly selected** for variety. To use specific voice, modify line 151:

```python
# Random selection (default)
voice_id = random.choice(self.male_voices)

# Specific voice
voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam
```

---

## 📊 Voice Settings Explained

```python
voice_settings = {
    "stability": 0.5,           # 0-1: Lower = more variation
    "similarity_boost": 0.85,   # 0-1: Higher = more consistent
    "style": 0.5,               # 0-1: Higher = more expressive
    "use_speaker_boost": True   # Clarity enhancement
}
```

**Customize for your needs:**
- **Stability**: 0.3 (dramatic) → 0.8 (consistent)
- **Similarity**: 0.7 (varied) → 1.0 (exact match)
- **Style**: 0.2 (neutral) → 0.8 (very expressive)

---

## 💰 Pricing

### ElevenLabs Plans

| Plan | Price | Characters/Month | Videos/Month |
|------|-------|------------------|--------------|
| **Free** | $0 | 10,000 | ~20 videos |
| **Starter** | $5 | 30,000 | ~60 videos |
| **Creator** | $22 | 100,000 | ~200 videos |
| **Pro** | $99 | 500,000 | ~1,000 videos |

**Calculation:** Each video ≈ 400-500 characters

### Cost Comparison

- **Google TTS**: Free but robotic voice
- **ElevenLabs**: $5/month for ultra-realistic
- **Professional Voice Actor**: $50-100 per video
- **This Bot**: Automates everything!

---

## 📈 Expected Results

### Video Quality
- ✅ Professional 3D animations
- ✅ Human-like voice quality
- ✅ Perfect 9:16 vertical format
- ✅ Optimized for mobile viewing
- ✅ 50-60 seconds (ideal for shorts)

### Growth Metrics
- 📊 3-5x better viewer retention
- 📊 Higher engagement rates
- 📊 Increased subscriber growth
- 📊 Better YouTube algorithm ranking
- 📊 More shares and comments

### Realistic Expectations
- **Week 1-2**: 100-500 views per video
- **Month 1**: 1,000-5,000 views per video
- **Month 3**: 10,000+ views per video (if consistent)
- **Month 6**: Potential viral videos (100K+ views)

---

## 🎯 Growth Strategy

### Daily Workflow
```
1. Morning (9-10 AM)
   └── Create 2-3 videos

2. Afternoon (2-3 PM)
   └── Upload Video #1

3. Evening (6-7 PM)
   └── Upload Video #2

4. Night (9-10 PM)
   └── Engage with comments
```

### Best Practices
- ✅ Upload 1-2 videos daily
- ✅ Post during peak hours (6-9 PM IST)
- ✅ Respond to all comments (first hour)
- ✅ Use trending hashtags
- ✅ Cross-promote on Instagram/Facebook
- ✅ Create video series (Part 1, 2, 3...)
- ✅ Consistent posting schedule

### Content Strategy
- **Monday**: Motivational stories
- **Tuesday**: Success stories
- **Wednesday**: Life lessons
- **Thursday**: Friendship stories
- **Friday**: Wisdom tales
- **Saturday**: Emotional stories
- **Sunday**: Inspirational content

---

## 🛠️ Troubleshooting

### Voice Generation Issues

**Error: "API key required"**
```bash
# Solution: Add ElevenLabs API key
# Edit line 18 in animation_bot.py
self.elevenlabs_key = "sk-your-key-here"
```

**Error: "Character limit exceeded"**
```bash
# Solution: Upgrade ElevenLabs plan or reduce script length
# Free plan: 10,000 chars/month
```

**Voice sounds robotic**
```bash
# Solution: Verify API key is correct
# Check ElevenLabs dashboard for usage
```

### Upload Issues

**Error: "YouTube authentication failed"**
```bash
# Solution: Re-authenticate
rm ~/youtube-bot/credentials/token.pickle
python animation_bot.py
```

**Videos not uploading**
```bash
# Solution: Videos saved locally
# Check: /sdcard/YouTube_Videos/
# Upload manually or fix credentials
```

### Video Quality Issues

**Images not generating**
```bash
# Solution: Check internet connection
# Pollinations AI might be slow - wait and retry
```

**Animation not smooth**
```bash
# Solution: Use Stability AI (premium)
# Or increase FFmpeg quality settings
```

---

## 📁 Project Structure

```
viral-shorts-bot/
├── animation_bot.py          # Main script
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
├── .gitignore               # Git ignore rules
│
├── ~/youtube-bot/
│   └── credentials/
│       ├── client_secrets.json    # YouTube OAuth
│       └── token.pickle           # Auth token
│
└── /sdcard/
    ├── background_music/     # Background music files
    ├── YouTube_Videos/       # Saved videos
    ├── scene_*.jpg          # Temporary images
    └── voice_*.mp3          # Temporary audio
```

---

## 🔒 Security Best Practices

### ⚠️ Never Commit Sensitive Data

```bash
# Files to NEVER push to GitHub:
- client_secrets.json
- token.pickle
- config.py (if contains keys)
- Any file with API keys
```

### Secure Your API Keys

```python
# ❌ Bad: Hardcoded keys
self.api_key = "sk-1234567890"

# ✅ Good: Environment variables
import os
self.api_key = os.getenv('ELEVENLABS_API_KEY')
```

### Use Environment Variables

```bash
# Add to ~/.bashrc
export ELEVENLABS_API_KEY="your-key-here"
export GEMINI_API_KEY="your-key-here"

# Reload
source ~/.bashrc
```

---

## 📝 Output Files

### Video Files
```
/sdcard/YouTube_Videos/
├── 20250127_143025_Motivational_Story.mp4
├── 20250127_143025_Motivational_Story_INFO.txt
├── 20250127_150132_Success_Story.mp4
└── 20250127_150132_Success_Story_INFO.txt
```

### Metadata File Example
```txt
TITLE: 🔥 Motivational Story | Part 1

DESCRIPTION:
🎬 जीवन बदल देने वाली कहानी
[Full story text...]

TAGS: hindi shorts, motivation, viral, trending...
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### Fork & Clone
```bash
# Fork repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/viral-shorts-bot.git
cd viral-shorts-bot
```

### Create Feature Branch
```bash
git checkout -b feature/amazing-feature
```

### Make Changes & Commit
```bash
git add .
git commit -m "Add amazing feature"
```

### Push & Create PR
```bash
git push origin feature/amazing-feature
# Create Pull Request on GitHub
```

### Contribution Ideas
- [ ] Add more voice options
- [ ] Implement female voices
- [ ] Add thumbnail generation
- [ ] Create GUI interface
- [ ] Add Instagram Reels support
- [ ] Implement video scheduling
- [ ] Add analytics dashboard

---

## 📜 License

MIT License - Free to use and modify

```
Copyright (c) 2025 codewithjagat2007-star

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.
```

---

## 🙏 Acknowledgments

### APIs & Services
- **[ElevenLabs](https://elevenlabs.io)** - Ultra-realistic AI voice
- **[Google Gemini](https://ai.google.dev/)** - Story generation
- **[Stability AI](https://stability.ai)** - Image-to-video conversion
- **[Pollinations AI](https://pollinations.ai)** - Image generation
- **[YouTube API](https://developers.google.com/youtube)** - Video upload

### Technologies
- **Python** - Programming language
- **FFmpeg** - Video processing
- **Google APIs** - Authentication & upload
- **Requests** - HTTP library

---

## 📞 Support & Contact

### Get Help
- 📧 **Email**: Open an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions
- 🐛 **Bug Reports**: Create an issue with details
- 💡 **Feature Requests**: Open feature request issue

### Social Media
- **GitHub**: [@codewithjagat2007-star](https://github.com/codewithjagat2007-star)
- **YouTube**: Share your channel when live!

### Useful Links
- [ElevenLabs Documentation](https://docs.elevenlabs.io)
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Python Requests Docs](https://requests.readthedocs.io)

---

## ⭐ Star History

If you find this project useful, please give it a star! ⭐

```
Star History Chart
(Will be generated as project grows)
```

---

## 🎉 Success Stories

Share your success! Create an issue with:
- Your channel link
- View counts achieved
- Tips for others
- Feature suggestions

---

## 📊 Roadmap

### Version 1.0 (Current)
- [x] ElevenLabs voice integration
- [x] Automated video creation
- [x] YouTube auto-upload
- [x] Viral metadata optimization

### Version 1.1 (Coming Soon)
- [ ] Web dashboard interface
- [ ] Video scheduling system
- [ ] Analytics integration
- [ ] Multiple language support

### Version 2.0 (Future)
- [ ] Instagram Reels support
- [ ] TikTok integration
- [ ] AI thumbnail generation
- [ ] Voice cloning option
- [ ] Mobile app (Android)

---

## 💡 Pro Tips

### Maximize Views
1. **Timing**: Upload at 6-7 PM (peak hours)
2. **Consistency**: Post daily or every 2 days
3. **Engagement**: Reply to all comments in first hour
4. **Hashtags**: Use 3-5 trending hashtags
5. **Series**: Create part 1, 2, 3 for continuation

### Content Ideas
- Life lessons from famous people
- Motivational stories with morals
- Success journey stories
- Friendship and relationship stories
- Problem-solving wisdom tales
- Emotional heart-touching stories

### Optimization
- Keep videos 50-60 seconds (sweet spot)
- Use emojis in titles (attracts attention)
- Add cliffhangers at the end
- Create hook in first 3 seconds
- Use trending background music

---

## 🔥 Final Words

> "Success is the sum of small efforts repeated day in and day out."

This bot is your **automated content creation machine**. Use it wisely:

✅ Create quality content consistently  
✅ Engage with your audience  
✅ Be patient with growth  
✅ Keep learning and improving  
✅ Share your success stories  

**Good luck with your YouTube journey!** 🚀

---

<div align="center">

### Made with ❤️ by [codewithjagat2007-star](https://github.com/codewithjagat2007-star)

**If this helped you, give it a ⭐!**

[![GitHub stars](https://img.shields.io/github/stars/codewithjagat2007-star/viral-shorts-bot.svg?style=social&label=Star)](https://github.com/codewithjagat2007-star/viral-shorts-bot)
[![GitHub forks](https://img.shields.io/github/forks/codewithjagat2007-star/viral-shorts-bot.svg?style=social&label=Fork)](https://github.com/codewithjagat2007-star/viral-shorts-bot/fork)

</div>
