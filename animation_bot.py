#!/data/data/com.termux/files/usr/bin/python
import os
import json
import requests
import random
import pickle
from datetime import datetime, timedelta
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from gtts import gTTS
import subprocess
import signal
import sys
from threading import Thread

try:
    from PIL import Image
except ImportError:
    os.system("pip install -q Pillow")
    from PIL import Image


class ViralShortsBot:
    def __init__(self):
        self.gemini_key = "AIzaSyC0jcYLHAMr2r9STSHQWXkqCwrKUvbOVSU"
        self.youtube = None
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        # FIXED: Correct credential paths
        self.base_dir = os.path.expanduser('~/uyanimation')
        self.credentials_dir = os.path.join(self.base_dir, 'credentials')
        self.token_file = os.path.join(self.credentials_dir, 'token.pickle')
        self.secrets_file = os.path.join(self.credentials_dir, 'client_secrets.json')
        self.pid_file = os.path.join(self.base_dir, 'background_bot.pid')
        self.log_file = os.path.join(self.base_dir, 'background_bot.log')
        
        self.running = True

        self.viral_titles = [
            "😱 {title}! | #{num}",
            "🔥 {title} | Part {num}",
            "{title} ❤️ | Ep {num}",
            "✨ {title} | #{num}",
            "💯 {title} Part {num}",
            "🎯 {title} | Episode {num}"
        ]

        self.viral_hashtags = [
            "#shorts #viral #trending #motivation #hindi",
            "#shorts #viral #hindi #story #animation",
            "#shorts #trending #motivational #hindistory",
            "#viral #shorts #animation #motivational #hindi",
            "#trending #shorts #viral #inspiration #hindistories",
            "#shorts #viral #motivationalstory #hindi #trending"
        ]

        self.setup_directories()

    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "/sdcard/background_music",
            "/sdcard/YouTube_Videos",
            "/sdcard/temp_scenes",
            self.credentials_dir
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

        self.download_background_music()

    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass

    def download_background_music(self):
        """Create background music"""
        print("📦 Setting up background music...")

        music_dir = "/sdcard/background_music"
        music_files = {
            'upbeat.mp3': (523, 659),
            'emotional.mp3': (440, 330),
            'inspiring.mp3': (392, 494)
        }

        for music, (freq1, freq2) in music_files.items():
            music_path = f"{music_dir}/{music}"
            if not os.path.exists(music_path):
                print(f"  Creating {music}...", end=" ")
                cmd = f'ffmpeg -f lavfi -i "sine=frequency={freq1}:duration=60" -f lavfi -i "sine=frequency={freq2}:duration=60" -filter_complex "[0:a][1:a]amix=inputs=2,volume=0.25" -y "{music_path}" -loglevel error'
                os.system(cmd)
                print("✓")

        print("✓ Background music ready\n")

    def authenticate_youtube(self):
        """Authenticate with YouTube API"""
        creds = None

        if not os.path.exists(self.secrets_file):
            print("\n❌ Error: client_secrets.json not found!")
            print("Please place your OAuth credentials at:")
            print(f"  {self.secrets_file}\n")
            return False

        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                self.log(f"Error loading token: {e}")
                if os.path.exists(self.token_file):
                    os.remove(self.token_file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.log(f"Token refresh failed: {e}")
                    if os.path.exists(self.token_file):
                        os.remove(self.token_file)
                    return self.authenticate_youtube()
            else:
                print("\n⚠️ YouTube authentication required")
                print("⚠️ IMPORTANT: Login with the CORRECT YouTube channel!\n")
                flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file, self.SCOPES)

                try:
                    creds = flow.run_local_server(port=8080, open_browser=False)
                except:
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print(f"\n🔗 Open this URL in browser:\n{auth_url}\n")
                    code = input("Enter the authorization code: ").strip()
                    flow.fetch_token(code=code)
                    creds = flow.credentials

            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.youtube = build('youtube', 'v3', credentials=creds)
        
        # Verify the channel
        try:
            channels = self.youtube.channels().list(part='snippet', mine=True).execute()
            if channels['items']:
                channel_name = channels['items'][0]['snippet']['title']
                print(f"✓ YouTube authenticated")
                print(f"✓ Channel: {channel_name}\n")
                self.log(f"Authenticated to channel: {channel_name}")
        except Exception as e:
            print(f"✓ YouTube authenticated\n")
            
        return True

    def generate_viral_metadata(self, story, video_number):
        """Generate VIRAL metadata"""
        title_template = random.choice(self.viral_titles)
        base_title = story['title'][:40]
        title = title_template.format(title=base_title, num=video_number)

        description_parts = [
            f"🎬 {story['title']}\n",
            f"\n📖 कहानी:\n{story['full_script'][:800]}\n",
            f"\n{'─' * 40}\n",
            "\n💡 इस कहानी से सीख:\n",
            "• हमेशा मेहनत करो\n",
            "• सपने देखो और पूरे करो\n",
            "• कभी हार मत मानो\n",
            f"\n{'─' * 40}\n",
            "\n🔔 Subscribe करें और Bell Icon दबाएं!\n",
            "\n📺 More Motivational Stories Coming Soon!\n",
            "\n" + random.choice(self.viral_hashtags) + "\n",
            "\n#hindikahaniya #moralstories #inspirationalstories",
            "\n#lifelessons #motivationalvideos #hindimotivation",
            "\n#youtubeshorts #viralshorts #trendingshorts",
            f"\n\n⏰ Video #{video_number}",
            f"\n📅 {datetime.now().strftime('%d %B %Y')}",
        ]

        description = ''.join(description_parts)[:5000]

        tags = [
            'hindi shorts', 'hindi kahani', 'hindi story',
            'motivational story hindi', 'shorts', 'viral shorts',
            story['category'], 'animated stories', '3d animation',
            'moral stories', 'life lessons', 'inspiration'
        ]

        return {
            'title': title[:100],
            'description': description,
            'tags': tags,
            'category': '22'
        }

    def upload_to_youtube(self, video_path, metadata, auto_upload=True):
        """Upload video to YouTube"""
        if not auto_upload or not self.youtube:
            return self.save_video_locally(video_path, metadata)

        print("  📤 Uploading to YouTube...", flush=True)
        self.log("Starting YouTube upload...")

        body = {
            'snippet': {
                'title': metadata['title'],
                'description': metadata['description'],
                'tags': metadata['tags'],
                'categoryId': metadata['category'],
                'defaultLanguage': 'hi',
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            }
        }

        try:
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            last_progress = 0

            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    if progress != last_progress:
                        print(f"    Upload progress: {progress}%", flush=True)
                        last_progress = progress

            video_id = response['id']
            url = f"https://youtube.com/shorts/{video_id}"

            print(f"\n  ✅ Successfully uploaded to YouTube!")
            print(f"  🔗 URL: {url}\n")
            self.log(f"Upload successful: {url}")

            # Also save locally as backup
            self.save_video_locally(video_path, metadata)

            return url

        except Exception as e:
            error_msg = f"Upload failed: {str(e)}"
            print(f"\n  ❌ {error_msg}")
            print("  💾 Saving locally instead...\n")
            self.log(error_msg)
            return self.save_video_locally(video_path, metadata)

    def save_video_locally(self, video_path, metadata):
        """Save video locally"""
        save_dir = "/sdcard/YouTube_Videos"

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = ''.join(c for c in metadata['title'][:30] if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')

        final_video = f"{save_dir}/{timestamp}_{safe_title}.mp4"
        metadata_file = f"{save_dir}/{timestamp}_{safe_title}_INFO.txt"

        import shutil
        shutil.copy2(video_path, final_video)

        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {metadata['title']}\n\n")
            f.write(f"DESCRIPTION:\n{metadata['description']}\n\n")
            f.write(f"TAGS: {', '.join(metadata['tags'][:20])}\n")

        print(f"  💾 Saved: {final_video}")
        return final_video

    def generate_long_story_with_scenes(self):
        """Generate story with scenes"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_key}"

        categories = ["motivation", "friendship", "wisdom", "life lesson", "success", "courage", "kindness"]
        category = random.choice(categories)
        num_scenes = random.randint(10, 14)

        data = {
            "contents": [{
                "parts": [{
                    "text": f"""Create COMPLETE LONG Hindi {category} story with {num_scenes} scenes (400-500 words).

Return ONLY valid JSON:
{{
  "title": "Catchy Hindi title (max 40 chars)",
  "category": "{category}",
  "full_script": "Complete Hindi story 400-500 words with ending",
  "character_description": "cute 3D Pixar character description",
  "scenes": [
    {{
      "scene_number": 1,
      "emotion": "happy",
      "action": "character doing something",
      "visual_description": "detailed scene description",
      "hindi_text": "35-50 words Hindi narration"
    }}
  ]
}}

EMOTIONS: happy, sad, excited, surprised, determined, peaceful, worried, thoughtful, joyful
Include complete story with proper ending and moral."""
                }]
            }],
            "generationConfig": {"temperature": 0.9, "topK": 40, "topP": 0.95, "maxOutputTokens": 4000}
        }

        for attempt in range(5):
            try:
                print(f"  Attempt {attempt+1}/5...", end=" ", flush=True)
                response = requests.post(url, json=data, timeout=60)

                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result:
                        text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                        text = text.replace('```json', '').replace('```', '').strip()

                        json_start = text.find('{')
                        json_end = text.rfind('}') + 1

                        if json_start != -1:
                            story = json.loads(text[json_start:json_end])
                            if 'scenes' in story and len(story['scenes']) >= 10:
                                words = len(story['full_script'].split())
                                print(f"✓ ({words} words, {len(story['scenes'])} scenes)")
                                return story

                print("✗")
                time.sleep(5)
            except Exception as e:
                print(f"✗ {str(e)[:30]}")
                time.sleep(5)

        raise Exception("Story generation failed")

    def generate_fast_clear_voice(self, script):
        """Generate voice at high speed"""
        print("  🎙️ Creating voice...", flush=True)

        ts = datetime.now().strftime('%H%M%S%f')
        audio = f"/sdcard/voice_{ts}.mp3"

        tts = gTTS(text=script, lang='hi', slow=False)
        tts.save(audio)

        speed = random.uniform(1.7, 2.0)
        print(f"    Speed: {speed:.2f}x")

        processed = audio.replace('.mp3', '_fast.mp3')

        filter_complex = f"atempo={speed},highpass=f=100,lowpass=f=10000,volume=3.0,alimiter=limit=0.9"

        cmd = [
            'ffmpeg', '-i', audio, '-af', filter_complex,
            '-ar', '44100', '-ab', '192k', '-ac', '1',
            '-y', processed, '-loglevel', 'error'
        ]

        subprocess.run(cmd)
        os.remove(audio)

        dur_cmd = f'ffprobe -i "{processed}" -show_entries format=duration -v quiet -of csv=p=0'
        duration = float(os.popen(dur_cmd).read().strip())

        print(f"  ✓ Voice ready! Duration: {duration:.1f}s")
        return processed, duration

    def generate_image_for_scene(self, scene, character_desc):
        """Generate image using Pollinations AI"""
        emotion = scene['emotion']
        action = scene.get('action', 'standing')
        visual = scene['visual_description']
        scene_num = scene['scene_number']

        prompt = f"3D Pixar Disney style animation, {character_desc}, {action}, {visual}, {emotion} expression, ultra detailed, vibrant colors, 8k, professional animation, cinematic lighting"

        print(f"    Scene {scene_num} [{emotion}]...", end=" ", flush=True)

        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1080&height=1920&model=flux&nologo=true&seed={scene_num*137}&enhance=true"

        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200 and len(response.content) > 5000:
                img_file = f"/sdcard/temp_scenes/scene_{scene_num}.jpg"
                with open(img_file, 'wb') as f:
                    f.write(response.content)

                print("✓")
                return img_file
        except Exception as e:
            print(f"✗ {str(e)[:20]}")

        return None

    def animate_image_with_ffmpeg(self, image_path, scene, duration):
        """Convert image to video with FFmpeg"""
        print(f"      🎬 Animating...", end=" ", flush=True)

        output = image_path.replace('.jpg', '_animated.mp4')
        emotion = scene.get('emotion', 'happy')

        effects = {
            'happy': f"zoompan=z='min(1+0.002*on,1.25)':d=25*{duration}:x='iw/2-(iw/zoom/2)+8*sin(on/20)':y='ih/2-(ih/zoom/2)-2*on':s=1080x1920",
            'sad': f"zoompan=z='max(1.2-0.001*on,1.0)':d=25*{duration}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+2*on':s=1080x1920",
            'excited': f"zoompan=z='1.1+0.1*sin(2*PI*on/40)':d=25*{duration}:x='iw/2-(iw/zoom/2)+12*sin(on/12)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'determined': f"zoompan=z='min(1+0.0025*on,1.4)':d=25*{duration}:x='iw/2-(iw/zoom/2)-4*on':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'peaceful': f"zoompan=z='1+0.0005*on':d=25*{duration}:x='iw/2-(iw/zoom/2)+4*sin(on/30)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'surprised': f"zoompan=z='1.15+0.05*sin(2*PI*on/20)':d=25*{duration}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'worried': f"zoompan=z='1.1':d=25*{duration}:x='iw/2-(iw/zoom/2)+5*sin(on/10)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'thoughtful': f"zoompan=z='min(1+0.001*on,1.15)':d=25*{duration}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            'joyful': f"zoompan=z='1.2':d=25*{duration}:x='iw/2-(iw/zoom/2)+10*sin(on/15)':y='ih/2-(ih/zoom/2)-3*on':s=1080x1920"
        }

        effect = effects.get(emotion, effects['happy'])

        cmd = [
            'ffmpeg', '-loop', '1', '-i', image_path,
            '-vf', effect,
            '-t', str(duration), '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p', '-y', output,
            '-loglevel', 'error'
        ]

        subprocess.run(cmd)
        print("✓")
        return output

    def create_complete_video(self, story, voice_file, duration):
        """Create complete video with all scenes"""
        print(f"  Duration: {duration:.1f}s | Per scene: {duration/len(story['scenes']):.1f}s\n")

        scene_duration = duration / len(story['scenes'])
        animated_videos = []

        print("  🎬 Converting images to videos...")
        for scene in story['scenes']:
            img = self.generate_image_for_scene(scene, story['character_description'])
            if img:
                video = self.animate_image_with_ffmpeg(img, scene, scene_duration)
                animated_videos.append(video)

        print(f"\n  ✓ {len(animated_videos)} scenes animated")

        if not animated_videos:
            raise Exception("No scenes created")

        print("  🔗 Combining scenes...")
        ts = datetime.now().strftime('%H%M%S')
        concat_file = f"/sdcard/concat_{ts}.txt"

        with open(concat_file, 'w') as f:
            for v in animated_videos:
                f.write(f"file '{v}'\n")

        combined = f"/sdcard/combined_{ts}.mp4"
        cmd = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -c copy -y "{combined}" -loglevel error'
        os.system(cmd)

        print("  🎙️ Adding voice...")
        with_voice = f"/sdcard/with_voice_{ts}.mp4"
        cmd = f'ffmpeg -i "{combined}" -i "{voice_file}" -c:v copy -c:a aac -shortest -y "{with_voice}" -loglevel error'
        os.system(cmd)

        music = random.choice(['upbeat.mp3', 'emotional.mp3', 'inspiring.mp3'])
        music_path = f"/sdcard/background_music/{music}"

        print("  🎵 Adding background music...")
        final = f"/sdcard/final_{ts}.mp4"
        cmd = f'ffmpeg -i "{with_voice}" -stream_loop -1 -i "{music_path}" -filter_complex "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=shortest[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -shortest -y "{final}" -loglevel error'
        os.system(cmd)

        print("  🧹 Cleaning up...")
        for v in animated_videos:
            try:
                os.remove(v)
                os.remove(v.replace('_animated.mp4', '.jpg'))
            except:
                pass

        for f in [concat_file, combined, with_voice, voice_file]:
            try:
                os.remove(f)
            except:
                pass

        print(f"\n  ✓ Final video ready: {final}")
        return final

    def create_and_upload_video(self, video_num=1, auto_upload=True):
        """Create and upload a complete video"""
        try:
            print(f"\n{'='*60}")
            print(f"🎬 Creating Video #{video_num}")
            print(f"{'='*60}\n")

            print("1️⃣ Generating story...")
            story = self.generate_long_story_with_scenes()
            print(f"  ✓ Story: {story['title']}")
            print(f"  ✓ Category: {story['category']}\n")

            print("2️⃣ Generating voice...")
            voice, duration = self.generate_fast_clear_voice(story['full_script'])

            print("\n3️⃣ Creating video...")
            video = self.create_complete_video(story, voice, duration)

            print("\n4️⃣ Generating metadata...")
            metadata = self.generate_viral_metadata(story, video_num)
            print(f"  ✓ Title: {metadata['title']}\n")

            print("5️⃣ Publishing...")
            url = self.upload_to_youtube(video, metadata, auto_upload)

            print(f"{'='*60}")
            print(f"✅ Video #{video_num} Complete!")
            print(f"{'='*60}\n")

            return {'status': 'success', 'url': url, 'title': metadata['title']}

        except Exception as e:
            error = f"Video #{video_num} failed: {str(e)}"
            print(f"\n❌ {error}\n")
            self.log(error)
            return {'status': 'failed', 'error': str(e)}

    def run_background_scheduler(self, interval_hours=3):
        """Run bot in background mode with automatic uploads every N hours"""
        
        # Check if already running
        if os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as f:
                old_pid = f.read().strip()
            print(f"⚠️ Background bot may already be running (PID: {old_pid})")
            print(f"If not, delete: {self.pid_file}\n")
            return
        
        # Save PID
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        print(f"\n{'='*60}")
        print(f"🤖 BACKGROUND MODE STARTED")
        print(f"{'='*60}")
        print(f"📅 Upload interval: {interval_hours} hours")
        print(f"📝 Log file: {self.log_file}")
        print(f"🔑 PID file: {self.pid_file}")
        print(f"{'='*60}\n")
        
        self.log(f"Background bot started - Upload every {interval_hours} hours")
        
        # Authenticate YouTube
        if not self.authenticate_youtube():
            print("❌ YouTube authentication failed!")
            os.remove(self.pid_file)
            return
        
        video_count = 1
        
        def signal_handler(sig, frame):
            print("\n\n⚠️ Stopping background bot...")
            self.log("Background bot stopped by user")
            self.running = False
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            while self.running:
                self.log(f"Starting video #{video_count} creation")
                
                result = self.create_and_upload_video(video_count, auto_upload=True)
                
                if result['status'] == 'success':
                    self.log(f"Video #{video_count} uploaded successfully: {result['url']}")
                    video_count += 1
                else:
                    self.log(f"Video #{video_count} failed: {result.get('error', 'Unknown error')}")
                
                # Wait for next interval
                next_time = datetime.now() + timedelta(hours=interval_hours)
                self.log(f"Next upload scheduled at: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                print(f"\n⏳ Waiting {interval_hours} hours until next upload...")
                print(f"⏰ Next upload at: {next_time.strftime('%H:%M:%S')}")
                print("Press Ctrl+C to stop\n")
                
                # Sleep in smaller intervals to allow interruption
                sleep_seconds = interval_hours * 3600
                for i in range(int(sleep_seconds)):
                    if not self.running:
                        break
                    if i % 300 == 0:  # Log every 5 minutes
                        remaining = timedelta(seconds=sleep_seconds - i)
                        print(f"⏱️  {str(remaining).split('.')[0]} remaining...", end='\r', flush=True)
                    time.sleep(1)
                
        except Exception as e:
            self.log(f"Background bot error: {str(e)}")
            print(f"\n❌ Error: {e}")
        finally:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            self.log("Background bot terminated")

    def stop_background_bot(self):
        """Stop the background bot"""
        if not os.path.exists(self.pid_file):
            print("❌ No background bot is running\n")
            return
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            print(f"⚠️ Stopping background bot (PID: {pid})...")
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            
            print("✓ Background bot stopped\n")
        except ProcessLookupError:
            print("❌ Process not found (already stopped)")
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except Exception as e:
            print(f"❌ Error stopping bot: {e}\n")

    def check_background_status(self):
        """Check if background bot is running"""
        if not os.path.exists(self.pid_file):
            print("❌ Background bot is NOT running\n")
            return
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process exists
            os.kill(pid, 0)
            print(f"✅ Background bot is RUNNING")
            print(f"   PID: {pid}")
            print(f"   Log: {self.log_file}\n")
            
            # Show last few log entries
            if os.path.exists(self.log_file):
                print("📝 Recent activity:")
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-5:]:
                        print(f"   {line.strip()}")
                print()
                
        except ProcessLookupError:
            print(f"❌ Background bot not running (stale PID: {pid})")
            os.remove(self.pid_file)
        except Exception as e:
            print(f"❌ Error checking status: {e}\n")

    def batch_upload(self, num_videos, interval_minutes):
        """Interactive batch upload (original functionality)"""
        print(f"\n⚠️ This will upload {num_videos} videos with {interval_minutes} min intervals (~{num_videos * interval_minutes} minutes = {num_videos * interval_minutes / 60:.1f} hours).")
        confirm = input("Continue? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("❌ Cancelled\n")
            return

        print(f"\n{'='*60}")
        print(f"🚀 AUTO YOUTUBE UPLOAD MODE")
        print(f"{'='*60}")
        print(f"Videos to create: {num_videos}")
        print(f"Upload interval: {interval_minutes} minutes")
        print(f"Total time: ~{num_videos * interval_minutes} minutes")
        print(f"{'='*60}\n")

        print("🔑 Authenticating YouTube...")
        if not self.authenticate_youtube():
            return

        results = []
        start_time = datetime.now()

        try:
            for i in range(1, num_videos + 1):
                print(f"\n{'*'*60}")
                print(f"📹 VIDEO {i} of {num_videos}")
                print(f"{'*'*60}\n")

                result = self.create_and_upload_video(i, auto_upload=True)
                results.append({
                    'video_num': i,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'result': result
                })

                if i < num_videos:
                    next_time = datetime.now() + timedelta(minutes=interval_minutes)
                    print(f"\n⏳ Waiting {interval_minutes} minutes...")
                    print(f"⏰ Next upload at: {next_time.strftime('%H:%M:%S')}")

                    for remaining in range(interval_minutes * 60, 0, -60):
                        mins = remaining // 60
                        print(f"⏱️  {mins:02d}:00 remaining...", end='\r', flush=True)
                        time.sleep(60)

        except KeyboardInterrupt:
            print("\n\n⚠️ Batch interrupted by user\n")

        end_time = datetime.now()
        duration = end_time - start_time

        print(f"\n{'='*60}")
        print(f"📊 BATCH SUMMARY")
        print(f"{'='*60}")
        print(f"Total videos attempted: {len(results)}")
        print(f"Successful uploads: {sum(1 for r in results if r['result']['status'] == 'success')}")
        print(f"Failed: {sum(1 for r in results if r['result']['status'] == 'failed')}")
        print(f"Total time: {duration}")
        print(f"{'='*60}\n")

        print("📝 DETAILED RESULTS:\n")
        for r in results:
            status = "✅" if r['result']['status'] == 'success' else "❌"
            print(f"{status} Video #{r['video_num']}")
            print(f"   Time: {r['time']}")
            if r['result']['status'] == 'success':
                print(f"   Result: {r['result']['url']}")
            else:
                print(f"   Error: {r['result'].get('error', 'Unknown')}")
            print()

        log_file = f"/sdcard/YouTube_Videos/batch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Batch Upload Log\n")
            f.write(f"{'='*60}\n")
            f.write(f"Start: {start_time}\n")
            f.write(f"End: {end_time}\n")
            f.write(f"Duration: {duration}\n\n")
            for r in results:
                f.write(f"Video #{r['video_num']}\n")
                f.write(f"Time: {r['time']}\n")
                f.write(f"Status: {r['result']['status']}\n")
                if r['result']['status'] == 'success':
                    f.write(f"URL: {r['result']['url']}\n")
                else:
                    f.write(f"Error: {r['result'].get('error', 'Unknown')}\n")
                f.write(f"\n")

        print(f"✓ Log saved: {log_file}\n")


def main():
    """Main function"""
    os.system('clear')

    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║        🎬 VIRAL YOUTUBE SHORTS BOT v3.2                   ║")
    print("║        Auto Upload + Background Mode + 3 Hour Interval    ║")
    print("║        Optimized for Termux                                ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    if os.path.exists('/data/data/com.termux'):
        print("✓ Running in Termux environment\n")
    else:
        print("⚠️ Not running in Termux - some features may not work\n")

    bot = ViralShortsBot()

    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Create single video (save locally)")
        print("2. Create single video + AUTO UPLOAD to YouTube")
        print("3. AUTO BATCH UPLOAD (custom)")
        print("4. Quick batch: 5 videos, 20 min interval")
        print("5. Daily batch: 10 videos, 30 min interval")
        print("6. Setup YouTube authentication")
        print("7. Check storage space")
        print("8. View created videos")
        print("9. Exit")
        print("-" * 60)
        print("🆕 BACKGROUND MODE (NEW!)")
        print("="*60)
        print("10. Start background bot (upload every 3 hours)")
        print("11. Stop background bot")
        print("12. Check background bot status")
        print("="*60)

        try:
            choice = input("\nSelect option (1-12): ").strip()

            if choice == '1':
                bot.create_and_upload_video(1, auto_upload=False)

            elif choice == '2':
                if bot.authenticate_youtube():
                    bot.create_and_upload_video(1, auto_upload=True)

            elif choice == '3':
                try:
                    num = int(input("Number of videos: "))
                    interval = int(input("Interval (minutes): "))
                    if bot.authenticate_youtube():
                        bot.batch_upload(num, interval)
                except ValueError:
                    print("❌ Invalid input\n")

            elif choice == '4':
                if bot.authenticate_youtube():
                    bot.batch_upload(5, 20)

            elif choice == '5':
                if bot.authenticate_youtube():
                    bot.batch_upload(10, 30)

            elif choice == '6':
                bot.authenticate_youtube()

            elif choice == '7':
                result = os.popen("df -h /sdcard | tail -1").read()
                print(f"\n📊 Storage:\n{result}")

            elif choice == '8':
                videos = os.popen("ls -lh /sdcard/YouTube_Videos/*.mp4 2>/dev/null | tail -10").read()
                if videos:
                    print(f"\n📹 Recent videos:\n{videos}")
                else:
                    print("\n❌ No videos found\n")

            elif choice == '9':
                print("\n👋 Goodbye!\n")
                break

            elif choice == '10':
                print("\n" + "="*60)
                print("🤖 BACKGROUND MODE SETUP")
                print("="*60)
                print("This will start the bot in background mode.")
                print("Videos will be created and uploaded every 3 hours.")
                print("The bot will run continuously until stopped.")
                print("="*60)
                
                confirm = input("\nStart background bot? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    print("\n⚠️ Starting background mode...")
                    print("⚠️ Press Ctrl+C to stop (will save progress)\n")
                    bot.run_background_scheduler(interval_hours=3)
                else:
                    print("❌ Cancelled\n")

            elif choice == '11':
                bot.stop_background_bot()

            elif choice == '12':
                bot.check_background_status()

            else:
                print("❌ Invalid option\n")

        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
