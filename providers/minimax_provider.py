"""
MiniMax TTS Provider
Implementation for MiniMax Text-to-Speech API
"""

import requests
import base64
from typing import Dict, Any, Optional
from .base_provider import BaseTTSProvider


class MiniMaxProvider(BaseTTSProvider):
    """MiniMax Text-to-Speech provider implementation"""

    DEFAULT_API_URL = "https://api.ppio.com/v3/minimax-speech-2.8-hd"

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize MiniMax provider

        Args:
            api_key: MiniMax API key
            config: Additional configuration (e.g., api_url, timeout)
        """
        super().__init__(api_key, config)
        self.api_url = config.get('api_url', self.DEFAULT_API_URL) if config else self.DEFAULT_API_URL
        self.timeout = config.get('timeout', 60) if config else 60
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def text_to_speech(self, text: str, output_path: str, voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert text to speech using MiniMax API

        Args:
            text: Text to convert
            output_path: Path to save the audio file
            voice_settings: Voice customization settings

        Returns:
            True if successful, False otherwise
        """
        # Merge default settings with user settings
        settings = self.get_default_voice_settings()
        if voice_settings:
            settings.update(voice_settings)

        # Build request payload
        payload = {
            "text": text,
            "stream": False,
            "output_format": "hex",  # Must be "url" or "hex"
            "voice_setting": settings,
            "audio_setting": {
                "format": "mp3",
                "bitrate": 128000,  # Must be one of [32000, 64000, 128000, 256000]
                "sample_rate": 24000,
                "channel": 1
            }
        }

        try:
            print(f"🔊 Generating audio ({len(text)} characters) with MiniMax...")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()

                # Handle base64 encoded audio data
                if 'data' in result and 'audio' in result['data']:
                    audio_data = base64.b64decode(result['data']['audio'])
                    with open(output_path, 'wb') as f:
                        f.write(audio_data)
                    print(f"✓ Audio saved: {output_path}\n")
                    return True

                # Handle direct audio response
                elif response.headers.get('Content-Type', '').startswith('audio'):
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ Audio saved: {output_path}\n")
                    return True

                else:
                    print(f"❌ Unknown response format: {result}")
                    return False
            else:
                print(f"❌ API request failed ({response.status_code}): {response.text}")
                return False

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get available MiniMax voices

        Returns:
            Dictionary of available voices
        """
        return {
            "male": [
                {"id": "male-qn-qingse", "name": "Young Male"},
                {"id": "male-qn-jingying", "name": "Professional Male"},
                {"id": "male-qn-badao", "name": "Commanding Male"},
                {"id": "male-qn-daxuesheng", "name": "College Student Male"},
            ],
            "female": [
                {"id": "female-shaonv", "name": "Young Female"},
                {"id": "female-yujie", "name": "Mature Female"},
                {"id": "female-chengshu", "name": "Sophisticated Female"},
                {"id": "female-tianmei", "name": "Sweet Female"},
            ]
        }

    def get_default_voice_settings(self) -> Dict[str, Any]:
        """
        Get default MiniMax voice settings

        Returns:
            Dictionary of default settings
        """
        return {
            "vol": 1.0,          # Volume (0.1-10)
            "speed": 1.0,        # Speech rate (0.5-2.0)
            "pitch": 0,          # Pitch (-12 to 12)
            "voice_id": "male-qn-qingse",
            "emotion": "calm"    # Must be one of: happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper
        }

    def validate_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Validate MiniMax voice settings

        Args:
            voice_settings: Settings to validate

        Returns:
            True if valid, False otherwise
        """
        if 'speed' in voice_settings:
            if not 0.5 <= voice_settings['speed'] <= 2.0:
                print("⚠️  Warning: speed should be between 0.5 and 2.0")
                return False

        if 'pitch' in voice_settings:
            if not -12 <= voice_settings['pitch'] <= 12:
                print("⚠️  Warning: pitch should be between -12 and 12")
                return False

        if 'vol' in voice_settings:
            if not 0.1 <= voice_settings['vol'] <= 10:
                print("⚠️  Warning: volume should be between 0.1 and 10")
                return False

        return True
