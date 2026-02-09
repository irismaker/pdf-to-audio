"""
ElevenLabs TTS Provider
Implementation for ElevenLabs Text-to-Speech API
"""

import requests
from typing import Dict, Any, Optional
from .base_provider import BaseTTSProvider


class ElevenLabsProvider(BaseTTSProvider):
    """ElevenLabs Text-to-Speech provider implementation"""

    DEFAULT_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ElevenLabs provider

        Args:
            api_key: ElevenLabs API key
            config: Additional configuration (e.g., api_url, timeout)
        """
        super().__init__(api_key, config)
        self.api_url = config.get('api_url', self.DEFAULT_API_URL) if config else self.DEFAULT_API_URL
        self.timeout = config.get('timeout', 60) if config else 60
        self.headers = {
            'xi-api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'audio/mpeg'
        }

    def text_to_speech(self, text: str, output_path: str, voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert text to speech using ElevenLabs API

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

        # Get voice ID
        voice_id = settings.get('voice_id', '21m00Tcm4TlvDq8ikWAM')

        # Build request URL
        url = f"{self.api_url}/{voice_id}"

        # Build request payload
        payload = {
            "text": text,
            "model_id": settings.get('model_id', 'eleven_multilingual_v2'),
            "voice_settings": {
                "stability": settings.get('stability', 0.5),
                "similarity_boost": settings.get('similarity_boost', 0.75),
                "style": settings.get('style', 0.0),
                "use_speaker_boost": settings.get('use_speaker_boost', True)
            }
        }

        try:
            print(f"🔊 Generating audio ({len(text)} characters) with ElevenLabs...")
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                # Save audio data directly (response is MP3)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Audio saved: {output_path}\n")
                return True
            else:
                print(f"❌ API request failed ({response.status_code}): {response.text}")
                return False

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get available ElevenLabs voices

        Returns:
            Dictionary of available voices
        """
        return {
            "premade": [
                {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel"},
                {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi"},
                {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella"},
                {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni"},
                {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli"},
                {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh"},
                {"id": "VR6AewLTigWG4xSOukaG", "name": "Arnold"},
                {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam"},
                {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam"},
            ]
        }

    def get_default_voice_settings(self) -> Dict[str, Any]:
        """
        Get default ElevenLabs voice settings

        Returns:
            Dictionary of default settings
        """
        return {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "model_id": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }

    def validate_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Validate ElevenLabs voice settings

        Args:
            voice_settings: Settings to validate

        Returns:
            True if valid, False otherwise
        """
        if 'stability' in voice_settings:
            if not 0 <= voice_settings['stability'] <= 1:
                print("⚠️  Warning: stability should be between 0 and 1")
                return False

        if 'similarity_boost' in voice_settings:
            if not 0 <= voice_settings['similarity_boost'] <= 1:
                print("⚠️  Warning: similarity_boost should be between 0 and 1")
                return False

        if 'style' in voice_settings:
            if not 0 <= voice_settings['style'] <= 1:
                print("⚠️  Warning: style should be between 0 and 1")
                return False

        return True
