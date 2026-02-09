"""
Google Cloud TTS Provider
Implementation for Google Cloud Text-to-Speech API
"""

import requests
import base64
from typing import Dict, Any, Optional
from .base_provider import BaseTTSProvider


class GoogleTTSProvider(BaseTTSProvider):
    """Google Cloud Text-to-Speech provider implementation"""

    DEFAULT_API_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Google TTS provider

        Args:
            api_key: Google Cloud API key
            config: Additional configuration (e.g., api_url, timeout)
        """
        super().__init__(api_key, config)
        self.api_url = config.get('api_url', self.DEFAULT_API_URL) if config else self.DEFAULT_API_URL
        self.timeout = config.get('timeout', 60) if config else 60
        # Google Cloud uses API key as query parameter
        self.api_key = api_key

    def text_to_speech(self, text: str, output_path: str, voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert text to speech using Google Cloud API

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

        # Build request URL with API key
        url = f"{self.api_url}?key={self.api_key}"

        # Build request payload
        payload = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": settings.get('language_code', 'en-US'),
                "name": settings.get('voice_name', 'en-US-Neural2-F'),
                "ssmlGender": settings.get('ssml_gender', 'FEMALE')
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": settings.get('speaking_rate', 1.0),
                "pitch": settings.get('pitch', 0.0),
                "volumeGainDb": settings.get('volume_gain_db', 0.0),
                "sampleRateHertz": 24000
            }
        }

        try:
            print(f"🔊 Generating audio ({len(text)} characters) with Google Cloud TTS...")
            response = requests.post(
                url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()

                # Google returns base64 encoded audio
                if 'audioContent' in result:
                    audio_data = base64.b64decode(result['audioContent'])
                    with open(output_path, 'wb') as f:
                        f.write(audio_data)
                    print(f"✓ Audio saved: {output_path}\n")
                    return True
                else:
                    print(f"❌ No audio content in response: {result}")
                    return False
            else:
                print(f"❌ API request failed ({response.status_code}): {response.text}")
                return False

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get available Google Cloud voices

        Returns:
            Dictionary of available voices (sample list)
        """
        return {
            "en-US": [
                {"id": "en-US-Neural2-F", "name": "Neural2 Female"},
                {"id": "en-US-Neural2-M", "name": "Neural2 Male"},
                {"id": "en-US-Wavenet-F", "name": "Wavenet Female"},
                {"id": "en-US-Wavenet-M", "name": "Wavenet Male"},
                {"id": "en-US-Studio-O", "name": "Studio O"},
            ],
            "zh-CN": [
                {"id": "cmn-CN-Wavenet-A", "name": "Wavenet Female"},
                {"id": "cmn-CN-Wavenet-B", "name": "Wavenet Male"},
            ],
            "ja-JP": [
                {"id": "ja-JP-Neural2-B", "name": "Neural2 Female"},
                {"id": "ja-JP-Neural2-C", "name": "Neural2 Male"},
            ]
        }

    def get_default_voice_settings(self) -> Dict[str, Any]:
        """
        Get default Google Cloud voice settings

        Returns:
            Dictionary of default settings
        """
        return {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-F",
            "ssml_gender": "FEMALE",
            "speaking_rate": 1.0,  # 0.25 to 4.0
            "pitch": 0.0,  # -20.0 to 20.0
            "volume_gain_db": 0.0  # -96.0 to 16.0
        }

    def validate_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Validate Google Cloud voice settings

        Args:
            voice_settings: Settings to validate

        Returns:
            True if valid, False otherwise
        """
        if 'speaking_rate' in voice_settings:
            if not 0.25 <= voice_settings['speaking_rate'] <= 4.0:
                print("⚠️  Warning: speaking_rate should be between 0.25 and 4.0")
                return False

        if 'pitch' in voice_settings:
            if not -20.0 <= voice_settings['pitch'] <= 20.0:
                print("⚠️  Warning: pitch should be between -20.0 and 20.0")
                return False

        if 'volume_gain_db' in voice_settings:
            if not -96.0 <= voice_settings['volume_gain_db'] <= 16.0:
                print("⚠️  Warning: volume_gain_db should be between -96.0 and 16.0")
                return False

        return True
