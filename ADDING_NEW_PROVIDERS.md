# Adding New TTS Providers

This guide explains how to add support for any Text-to-Speech (TTS) provider to the PDF to Audio Converter.

## Overview

The project uses a **provider pattern** architecture that makes it easy to add new TTS services. Each provider is a separate class that implements a common interface.

## Current Supported Providers

- ✅ **MiniMax** (via PPIO)
- ✅ **Novita AI**

## How to Add a New Provider

### Step 1: Create a New Provider Class

Create a new file in the `providers/` directory (e.g., `providers/elevenlabs_provider.py`):

```python
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
            'Content-Type': 'application/json'
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
                # Save audio data
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

        return True
```

### Step 2: Register the Provider

Update `providers/__init__.py` to register your new provider:

```python
from .elevenlabs_provider import ElevenLabsProvider

PROVIDERS = {
    'minimax': MiniMaxProvider,
    'novita': NovitaProvider,
    'elevenlabs': ElevenLabsProvider,  # Add your provider here
}

__all__ = ['BaseTTSProvider', 'MiniMaxProvider', 'NovitaProvider', 'ElevenLabsProvider',
           'create_provider', 'get_available_providers', 'PROVIDERS']
```

### Step 3: Add Configuration

Update `config_example.py` with provider-specific settings:

```python
# ElevenLabs Configuration
ELEVENLABS_CONFIG = {
    "api_url": "https://api.elevenlabs.io/v1/text-to-speech",
    "timeout": 60,
    "default_voice_settings": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "model_id": "eleven_multilingual_v2",
        "stability": 0.5,
        "similarity_boost": 0.75
    }
}
```

### Step 4: Update Web Interface

Add your provider to the dropdown in `templates/index.html`:

```html
<select id="provider">
    <option value="minimax">MiniMax (PPIO)</option>
    <option value="novita">Novita AI</option>
    <option value="elevenlabs">ElevenLabs</option>  <!-- Add here -->
</select>
```

Update the API URL mapping in `static/js/main.js`:

```javascript
function updateApiUrlPlaceholder() {
    const provider = elements.provider.value;
    const apiUrlMap = {
        'minimax': 'https://api.ppio.com/v3/minimax-speech-2.8-hd',
        'novita': 'https://api.novita.ai/v3/minimax-speech-2.8-turbo',
        'elevenlabs': 'https://api.elevenlabs.io/v1/text-to-speech'  // Add here
    };

    const defaultUrl = apiUrlMap[provider] || apiUrlMap['minimax'];
    elements.apiUrl.value = defaultUrl;
    elements.apiUrl.placeholder = defaultUrl;
}
```

### Step 5: Update Documentation

Update `README.md` to list the new provider:

```markdown
### Currently Supported Providers

- ✅ **MiniMax (PPIO)** - High-quality TTS via PPIO provider
- ✅ **Novita AI** - MiniMax Speech 2.8 Turbo via Novita AI platform
- ✅ **ElevenLabs** - Premium quality TTS with realistic voices
```

## Popular TTS Providers You Can Add

### 1. **ElevenLabs**
- **API Docs**: https://docs.elevenlabs.io/api-reference
- **Features**: High-quality, realistic voices, voice cloning
- **Pricing**: Paid tiers with free trial
- **Best For**: Premium quality, audiobooks, content creation

### 2. **OpenAI TTS**
- **API Docs**: https://platform.openai.com/docs/guides/text-to-speech
- **Features**: 6 voices (alloy, echo, fable, onyx, nova, shimmer)
- **Pricing**: $15 per 1M characters
- **Best For**: Fast, good quality, multilingual

### 3. **Azure Cognitive Services TTS**
- **API Docs**: https://learn.microsoft.com/azure/cognitive-services/speech-service/
- **Features**: 400+ voices, 140+ languages, SSML support
- **Pricing**: Free tier available, then pay-as-you-go
- **Best For**: Enterprise, many languages, neural voices

### 4. **Google Cloud TTS**
- **API Docs**: https://cloud.google.com/text-to-speech
- **Features**: WaveNet voices, 220+ voices, 40+ languages
- **Pricing**: Free tier available, then per character
- **Best For**: Google ecosystem, neural voices, SSML

### 5. **AWS Polly**
- **API Docs**: https://docs.aws.amazon.com/polly/
- **Features**: Neural voices, 60+ voices, 30+ languages
- **Pricing**: Free tier, then per character
- **Best For**: AWS ecosystem, neural TTS

### 6. **Coqui TTS** (Open Source)
- **Docs**: https://github.com/coqui-ai/TTS
- **Features**: Open source, voice cloning, multilingual
- **Pricing**: Free (self-hosted)
- **Best For**: Privacy, customization, self-hosting

## Implementation Checklist

When adding a new provider, make sure to:

- [ ] Create provider class in `providers/` directory
- [ ] Implement all required methods from `BaseTTSProvider`
- [ ] Register provider in `providers/__init__.py`
- [ ] Add configuration to `config_example.py`
- [ ] Add provider option to web interface (`templates/index.html`)
- [ ] Update API URL mapping in JavaScript (`static/js/main.js`)
- [ ] Update documentation (`README.md`)
- [ ] Test with a sample PDF
- [ ] Handle provider-specific error messages
- [ ] Document any special requirements or limitations

## Provider Interface Requirements

Every provider must implement these methods from `BaseTTSProvider`:

### Required Methods

1. **`text_to_speech(text, output_path, voice_settings)`**
   - Convert text to audio
   - Save to output_path
   - Return True on success, False on failure

2. **`get_available_voices()`**
   - Return dict of available voices
   - Format: `{"category": [{"id": "...", "name": "..."}]}`

3. **`get_default_voice_settings()`**
   - Return dict of default settings
   - Include all provider-specific parameters

4. **`validate_settings(voice_settings)`**
   - Validate voice settings
   - Return True if valid, False otherwise

## Testing Your Provider

After implementing a new provider, test it:

### Command Line Test

```bash
python quick_start.py
# Select your new provider when prompted
```

### Python Test

```python
from pdf_to_audio import PDFToAudioConverter

converter = PDFToAudioConverter(
    provider_name="elevenlabs",  # Your provider name
    api_key="your_api_key",
    provider_config={"timeout": 60}
)

converter.convert_pdf_to_audio(
    pdf_path="test.pdf",
    output_dir="output"
)
```

### Web Interface Test

```bash
PORT=5001 python app.py
# Open browser, select your provider, upload PDF
```

## Common Implementation Patterns

### Pattern 1: Direct Audio Response

If the API returns audio directly:

```python
response = requests.post(url, json=payload)
if response.status_code == 200:
    with open(output_path, 'wb') as f:
        f.write(response.content)
```

### Pattern 2: Base64 Encoded Audio

If the API returns base64-encoded audio:

```python
import base64

result = response.json()
audio_data = base64.b64decode(result['audio'])
with open(output_path, 'wb') as f:
    f.write(audio_data)
```

### Pattern 3: Hex Encoded Audio (like MiniMax)

If the API returns hex-encoded audio:

```python
result = response.json()
audio_data = bytes.fromhex(result['data']['audio'])
with open(output_path, 'wb') as f:
    f.write(audio_data)
```

### Pattern 4: URL-based Audio

If the API returns a URL to download audio:

```python
result = response.json()
audio_url = result['audio_url']
audio_response = requests.get(audio_url)
with open(output_path, 'wb') as f:
    f.write(audio_response.content)
```

## Need Help?

- Check existing providers (`minimax_provider.py`, `novita_provider.py`) as examples
- Read the API documentation of the TTS service you want to add
- Open an issue on GitHub if you encounter problems
- Submit a Pull Request to share your implementation with others

---

**Contributions Welcome!** If you implement a new provider, please consider contributing it back to the project by submitting a Pull Request.
