"""
Azure Cognitive Services TTS Provider
Implementation for Azure Text-to-Speech API
"""

import requests
from typing import Dict, Any, Optional
from .base_provider import BaseTTSProvider


class AzureTTSProvider(BaseTTSProvider):
    """Azure Cognitive Services Text-to-Speech provider implementation"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Azure TTS provider

        Args:
            api_key: Azure subscription key
            config: Additional configuration (region, api_url, timeout)
        """
        super().__init__(api_key, config)

        # Azure requires region specification
        self.region = config.get('region', 'eastus') if config else 'eastus'

        # Build API URL based on region
        default_url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        self.api_url = config.get('api_url', default_url) if config else default_url

        self.timeout = config.get('timeout', 60) if config else 60
        self.headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3'
        }

    def text_to_speech(self, text: str, output_path: str, voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert text to speech using Azure API

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

        # Get voice name
        voice_name = settings.get('voice_name', 'en-US-AriaNeural')

        # Get speech parameters
        rate = settings.get('rate', '1.0')
        pitch = settings.get('pitch', '+0Hz')

        # Build SSML
        ssml = f"""<speak version='1.0' xml:lang='en-US'>
    <voice name='{voice_name}'>
        <prosody rate='{rate}' pitch='{pitch}'>
            {text}
        </prosody>
    </voice>
</speak>"""

        try:
            print(f"🔊 Generating audio ({len(text)} characters) with Azure TTS...")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=ssml.encode('utf-8'),
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
        Get available Azure voices

        Returns:
            Dictionary of available voices (sample list)
        """
        return {
            "en-US": [
                {"id": "en-US-AriaNeural", "name": "Aria (Female)"},
                {"id": "en-US-JennyNeural", "name": "Jenny (Female)"},
                {"id": "en-US-GuyNeural", "name": "Guy (Male)"},
                {"id": "en-US-DavisNeural", "name": "Davis (Male)"},
            ],
            "zh-CN": [
                {"id": "zh-CN-XiaoxiaoNeural", "name": "Xiaoxiao (Female)"},
                {"id": "zh-CN-YunxiNeural", "name": "Yunxi (Male)"},
                {"id": "zh-CN-YunjianNeural", "name": "Yunjian (Male)"},
            ],
            "ja-JP": [
                {"id": "ja-JP-NanamiNeural", "name": "Nanami (Female)"},
                {"id": "ja-JP-KeitaNeural", "name": "Keita (Male)"},
            ]
        }

    def get_default_voice_settings(self) -> Dict[str, Any]:
        """
        Get default Azure voice settings

        Returns:
            Dictionary of default settings
        """
        return {
            "voice_name": "en-US-AriaNeural",
            "rate": "1.0",  # 0.5 to 2.0, or use percentage like "+20%"
            "pitch": "+0Hz"  # e.g., "+10Hz", "-5Hz", "+20%"
        }

    def validate_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Validate Azure voice settings

        Args:
            voice_settings: Settings to validate

        Returns:
            True if valid, False otherwise
        """
        if 'rate' in voice_settings:
            try:
                rate = float(voice_settings['rate'].rstrip('%'))
                if not 0.5 <= rate <= 2.0:
                    print("⚠️  Warning: rate should be between 0.5 and 2.0")
                    return False
            except:
                pass  # Allow percentage format like "+20%"

        return True
