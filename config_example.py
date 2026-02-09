"""
Configuration Example
Copy this file to config.py and fill in your settings
"""

# ============================================================
# TTS Provider Selection
# ============================================================
# Choose which TTS provider to use
# Options: 'minimax', 'novita', 'elevenlabs', 'azure', 'google'
TTS_PROVIDER = "minimax"  # Default provider


# ============================================================
# API Keys Configuration
# ============================================================
# Add your API keys for different providers
API_KEYS = {
    "minimax": "your_minimax_api_key_here",
    "novita": "your_novita_api_key_here",
    "elevenlabs": "your_elevenlabs_api_key_here",
    "azure": "your_azure_subscription_key_here",
    "google": "your_google_cloud_api_key_here",
}


# ============================================================
# Provider-Specific Configurations
# ============================================================

# MiniMax Configuration
MINIMAX_CONFIG = {
    # API URL Options:
    # - PPIO Provider (recommended): "https://api.ppio.com/v3/minimax-speech-2.8-hd"
    # - MiniMax Official: "https://api.minimax.chat/v1/text_to_speech" (if you have direct access)
    # You can use any MiniMax-compatible API endpoint here
    "api_url": "https://api.ppio.com/v3/minimax-speech-2.8-hd",
    "timeout": 60,
    "default_voice_settings": {
        "vol": 1.0,          # Volume (0.1-10)
        "speed": 1.0,        # Speech rate (0.5-2.0)
        "pitch": 0,          # Pitch (-12 to 12)
        "voice_id": "male-qn-qingse",
        "emotion": "calm"    # Must be one of: happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper
    }
}

# Novita Configuration
NOVITA_CONFIG = {
    "api_url": "https://api.novita.ai/v3/minimax-speech-2.8-turbo",
    "timeout": 60,
    "default_voice_settings": {
        "vol": 1.0,          # Volume (0.1-10)
        "speed": 1.0,        # Speech rate (0.5-2.0)
        "pitch": 0,          # Pitch (-12 to 12)
        "voice_id": "male-qn-qingse",
        "emotion": "calm"    # Must be one of: happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper
    }
}

# ElevenLabs Configuration
ELEVENLABS_CONFIG = {
    "api_url": "https://api.elevenlabs.io/v1/text-to-speech",
    "timeout": 60,
    "default_voice_settings": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "model_id": "eleven_multilingual_v2",
        "stability": 0.5,              # 0-1
        "similarity_boost": 0.75,      # 0-1
        "style": 0.0,                  # 0-1
        "use_speaker_boost": True
    }
}

# Azure Cognitive Services TTS Configuration
AZURE_CONFIG = {
    "region": "eastus",  # Change to your Azure region
    "timeout": 60,
    "default_voice_settings": {
        "voice_name": "en-US-AriaNeural",
        "rate": "1.0",      # 0.5-2.0
        "pitch": "+0Hz"     # e.g., "+10Hz", "-5Hz"
    }
}

# Google Cloud TTS Configuration
GOOGLE_CONFIG = {
    "api_url": "https://texttospeech.googleapis.com/v1/text:synthesize",
    "timeout": 60,
    "default_voice_settings": {
        "language_code": "en-US",
        "voice_name": "en-US-Neural2-F",
        "ssml_gender": "FEMALE",
        "speaking_rate": 1.0,          # 0.25-4.0
        "pitch": 0.0,                  # -20.0 to 20.0
        "volume_gain_db": 0.0          # -96.0 to 16.0
    }
}


# ============================================================
# General Settings
# ============================================================

# Text Processing Settings
TEXT_SETTINGS = {
    "max_chunk_length": 5000,  # Max characters per audio chunk
    "remove_page_numbers": True,
    "remove_extra_spaces": True,
}

# Batch Processing Settings
BATCH_SETTINGS = {
    "output_dir": "audio_output",
    "delay_between_requests": 1,  # Delay in seconds
    "retry_times": 3,
    "retry_delay": 5,
}

# Audio Output Settings (applies to all providers when applicable)
AUDIO_SETTINGS = {
    "format": "mp3",
    "bitrate": 128000,   # Must be one of [32000, 64000, 128000, 256000]
    "sample_rate": 24000,  # Hz
    "channel": 1         # 1=mono, 2=stereo
}


# ============================================================
# Available Voices Reference (Provider-specific)
# ============================================================

MINIMAX_VOICES = {
    "male": [
        "male-qn-qingse",      # Young Male
        "male-qn-jingying",    # Professional Male
        "male-qn-badao",       # Commanding Male
        "male-qn-daxuesheng",  # College Student Male
    ],
    "female": [
        "female-shaonv",       # Young Female
        "female-yujie",        # Mature Female
        "female-chengshu",     # Sophisticated Female
        "female-tianmei",      # Sweet Female
    ]
}

OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
