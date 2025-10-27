#!/bin/bash

echo "🚀 Setting up Viral Shorts Bot..."

# Create directories
mkdir -p ~/youtube-bot/credentials
mkdir -p /sdcard/background_music
mkdir -p /sdcard/YouTube_Videos

# Install system dependencies (Termux)
if command -v pkg &> /dev/null; then
    echo "📦 Installing Termux packages..."
    pkg update
    pkg install -y python ffmpeg
fi

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your ElevenLabs API key in animation_bot.py"
echo "2. Setup YouTube credentials in ~/youtube-bot/credentials/"
echo "3. Run: python animation_bot.py"
Save and exit: Press CTRL+X, then Y, then ENTER
# Make it executable
chmod +x setup.sh
