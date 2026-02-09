# PDF to Audio Converter 🎙️

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/irismaker/pdf-to-audio.svg?style=social&label=Star)](https://github.com/irismaker/pdf-to-audio)

A flexible and extensible Python tool for batch converting PDF documents to high-quality audio using various Text-to-Speech providers. Features a modern web interface for easy file uploads without any command line knowledge required.

## ✨ Features

- 🌐 **Modern Web Interface** - User-friendly web UI with drag & drop upload (NEW!)
- 📚 **Batch Processing** - Convert multiple PDF documents at once
- 🔌 **Multiple TTS Providers** - Extensible architecture to support different TTS services
- ✂️ **Smart Text Splitting** - Automatically splits long texts to avoid API limits
- 🎵 **Customizable Voice** - Adjust speed, pitch, timbre, emotion and more
- 📊 **Progress Tracking** - Real-time progress display and status updates
- 🔄 **Error Handling** - Robust error handling with retry mechanisms
- 🎧 **High Quality Output** - MP3 format at 128kbps bitrate

### Currently Supported Providers

- ✅ **MiniMax** - High-quality Chinese TTS with multiple voice options
- 🔜 **ElevenLabs** - Coming soon
- 🔜 **Azure TTS** - Coming soon
- 🔜 **Google Cloud TTS** - Coming soon
- 🔜 **More providers** - Coming soon

## 🎨 Web Interface

The easiest way to use this tool is through the modern web interface:

- **No Command Line Required** - Everything in your browser
- **Flexible API Configuration** - Use PPIO or custom API endpoints
- **Drag & Drop Upload** - Simply drag your PDF files
- **Real-time Progress** - Visual progress bar with status updates
- **Audio Preview** - Play audio before downloading
- **Batch Download** - Download all files as ZIP
- **Modern Design** - Clean, elegant, and intuitive interface

### Quick Start with Web Interface

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open in browser
# Visit: http://localhost:5000
```

That's it! Upload your PDF, enter your API key, and convert!

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/irismaker/pdf-to-audio.git
cd pdf-to-audio
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API

**Method A: Using Config File (Recommended)**

```bash
cp config_example.py config.py
# Edit config.py and add your API keys and settings
```

**Method B: Using Environment Variables**

```bash
export TTS_PROVIDER="minimax"
export TTS_API_KEY="your_api_key_here"
```

### 4. Run the Program

**Web Interface (Easiest - Recommended)**

```bash
python app.py
```

Then open your browser and visit: `http://localhost:5000`

Features:
- Upload PDFs directly in your browser
- No need to manage file folders
- Visual progress tracking
- Play audio before downloading
- Download all files as ZIP

**Command Line - Quick Start**

```bash
python quick_start.py
```

**Command Line - Interactive Mode**

```bash
python pdf_to_audio.py
```

## 📖 Usage

### Basic Usage

#### Interactive Mode

```bash
python pdf_to_audio.py
```

Follow the prompts to:
1. Select TTS provider
2. Enter API key (if not in config)
3. Specify PDF file or directory
4. Customize voice settings (optional)

#### Quick Start with Config

```bash
python quick_start.py
```

Automatically uses settings from `config.py` and scans current directory for PDFs.

### Web Interface Usage

The web interface provides the easiest way to convert PDFs to audio without any command line knowledge.

#### Starting the Web Server

```bash
python app.py
```

The server will start on `http://localhost:5000`. Open this URL in your web browser.

#### Using the Web Interface

1. **Configure API**
   - Enter your MiniMax API key
   - Configure API URL (default: PPIO provider, or enter your custom endpoint)
   - Select provider (currently only MiniMax is available)

2. **Upload PDF**
   - Click the upload area or drag and drop your PDF file
   - Maximum file size: 50MB
   - Only PDF files are accepted

3. **Customize Voice (Optional)**
   - Select voice type (male or female voices available)
   - Adjust speed (0.5x to 2.0x)
   - Adjust pitch (-12 to +12)
   - Choose emotion (calm, happy, sad, angry, etc.)

4. **Convert**
   - Click "Convert to Audio" button
   - Watch real-time progress
   - View status messages during conversion

5. **Download Results**
   - Play audio files directly in browser
   - Download individual files
   - Download all files as a ZIP archive

#### Web Interface Features

- **No File Management**: Upload files directly through browser
- **Flexible API Configuration**: Use PPIO provider or custom API endpoints
- **Real-time Progress**: Visual progress bar with status messages
- **Audio Preview**: Play audio before downloading
- **Batch Download**: Download all generated files as ZIP
- **Error Handling**: Clear error messages with helpful guidance
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-cleanup**: Temporary files automatically deleted after 1 hour

### Advanced Usage

#### Use as Python Module

```python
from pdf_to_audio import PDFToAudioConverter

# Create converter with MiniMax
converter = PDFToAudioConverter(
    provider_name="minimax",
    api_key="your_api_key",
    provider_config={"timeout": 60}
)

# Convert single file
converter.convert_pdf_to_audio(
    pdf_path="document.pdf",
    output_dir="audio_output"
)

# Batch convert directory
converter.batch_convert(
    pdf_dir="./pdfs",
    output_dir="./audio_output"
)
```

#### Custom Voice Settings

```python
# MiniMax voice settings
voice_settings = {
    "speed": 1.2,           # Speech rate: 0.5-2.0
    "pitch": 2,             # Pitch: -12 to 12
    "vol": 1.5,             # Volume: 0.1-10
    "emotion": "happy",     # Emotion: neutral, happy, sad, angry
    "voice_id": "female-tianmei"  # Voice ID
}

converter.convert_pdf_to_audio(
    pdf_path="document.pdf",
    voice_settings=voice_settings
)
```

## 🎨 Available Voices (MiniMax)

### Male Voices
- `male-qn-qingse` - Young Male
- `male-qn-jingying` - Professional Male
- `male-qn-badao` - Commanding Male
- `male-qn-daxuesheng` - College Student Male

### Female Voices
- `female-shaonv` - Young Female
- `female-yujie` - Mature Female
- `female-chengshu` - Sophisticated Female
- `female-tianmei` - Sweet Female

## ⚙️ Configuration

### Provider Settings

Edit `config.py` to configure providers:

```python
# Select provider
TTS_PROVIDER = "minimax"  # or "elevenlabs", "azure", etc.

# API Keys
API_KEYS = {
    "minimax": "your_minimax_api_key",
    # "elevenlabs": "your_elevenlabs_api_key",
}

# Provider-specific config
MINIMAX_CONFIG = {
    "api_url": "https://api.ppio.com/v3/minimax-speech-2.8-hd",  # Customize your API endpoint
    "timeout": 60,
    "default_voice_settings": {
        "speed": 1.0,
        "pitch": 0,
        "voice_id": "male-qn-qingse"
    }
}
```

### Custom API Endpoints

The project supports custom API endpoints. You can use:

- **PPIO Provider** (default): `https://api.ppio.com/v3/minimax-speech-2.8-hd`
- **MiniMax Official API**: `https://api.minimax.chat/v1/text_to_speech` (if you have direct access)
- **Any MiniMax-compatible API**: Configure your own endpoint in `config.py`

Simply change the `api_url` in your provider configuration:

```python
MINIMAX_CONFIG = {
    "api_url": "YOUR_CUSTOM_API_ENDPOINT",
    "timeout": 60,
    # ... other settings
}
```

### Voice Parameters (MiniMax)

| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| speed | Speech rate | 0.5-2.0 | 1.0 |
| pitch | Voice pitch | -12 to 12 | 0 |
| vol | Volume | 0.1-10 | 1.0 |
| emotion | Emotion | neutral, happy, sad, angry | neutral |
| voice_id | Voice ID | See available voices | male-qn-qingse |

## 📁 Project Structure

```
pdf-to-audio/
├── providers/                 # TTS provider implementations
│   ├── __init__.py           # Provider factory
│   ├── base_provider.py      # Abstract base class
│   └── minimax_provider.py   # MiniMax implementation
├── pdf_to_audio.py           # Main converter class
├── quick_start.py            # Quick start script
├── config_example.py         # Configuration template
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## 🔧 Requirements

- Python 3.7+
- requests >= 2.31.0
- PyPDF2 >= 3.0.0

## 🔌 Adding New TTS Providers

The architecture is designed for easy extensibility. To add a new provider:

1. **Create a new provider class** in `providers/` directory:

```python
# providers/custom_provider.py
from .base_provider import BaseTTSProvider

class CustomProvider(BaseTTSProvider):
    def text_to_speech(self, text, output_path, voice_settings=None):
        # Implement your TTS API call
        pass

    def get_available_voices(self):
        return ["voice1", "voice2", "voice3"]

    def get_default_voice_settings(self):
        return {"voice": "voice1", "speed": 1.0}
```

2. **Register the provider** in `providers/__init__.py`:

```python
from .custom_provider import CustomProvider

PROVIDERS = {
    'minimax': MiniMaxProvider,
    'custom': CustomProvider,  # Add your provider here
}
```

3. **Update config_example.py** with provider-specific settings

4. **Test your implementation** and submit a pull request!

## 📝 Notes

1. **API Keys**: Requires valid API keys for the chosen provider
2. **PDF Format**: Only supports PDFs with extractable text (not scanned images)
3. **Network**: Requires stable internet connection for API calls
4. **API Limits**: Be aware of provider-specific rate limits and quotas
5. **Text Length**: Long texts are automatically split (default max 5000 characters per chunk)

## 🐛 Troubleshooting

### Empty Text Extraction from PDF
- **Cause**: PDF may be a scanned image
- **Solution**: Use OCR tools to convert PDF to searchable text first

### API Returns 401 Error
- **Cause**: Invalid or expired API key
- **Solution**: Check and update your API key in config.py

### API Returns 429 Error
- **Cause**: Rate limit exceeded
- **Solution**: Add delays between requests or wait before retrying

### Provider Not Found Error
- **Cause**: Unsupported provider name
- **Solution**: Check available providers with `get_available_providers()`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add new TTS providers** - Implement support for ElevenLabs, Azure, Google Cloud, etc.
2. **Improve text extraction** - Better handling of PDF formats
3. **Add features** - OCR support, subtitle generation, audio merging
4. **Fix bugs** - Report issues or submit fixes
5. **Improve documentation** - Better examples and tutorials

### Development Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MiniMax](https://www.minimaxi.com/) - For providing the Text-to-Speech API
- [PyPDF2](https://github.com/py-pdf/pypdf2) - For PDF text extraction
- All contributors and users of this project

## 📮 Contact

For questions, suggestions, or issues:
- Open an [Issue](https://github.com/irismaker/pdf-to-audio/issues)
- Submit a [Pull Request](https://github.com/irismaker/pdf-to-audio/pulls)

## 🗺️ Roadmap

- [ ] Add ElevenLabs provider
- [ ] Add Azure TTS provider
- [ ] Add Google Cloud TTS provider
- [ ] Implement OCR for scanned PDFs
- [ ] Add subtitle/caption generation
- [ ] Add audio file merging for multi-part outputs
- [ ] Create GUI interface
- [ ] Add Docker support
- [ ] Add more languages support

---

⭐ If this project helps you, please give it a star!

Made with ❤️ by the open source community
