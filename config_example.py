"""
Configuration Example
Copy this file to config.py and fill in your settings
"""

# ============================================================
# TTS Provider Selection
# ============================================================
# Choose which TTS provider to use
# Options: 'minimax', 'openai', 'elevenlabs', 'azure', 'google'
# (Note: Only 'minimax' is currently implemented)
TTS_PROVIDER = "minimax"


# ============================================================
# API Keys Configuration
# ============================================================
# Add your API keys for different providers
API_KEYS = {
    "minimax": "your_minimax_api_key_here",
    # "openai": "your_openai_api_key_here",
    # "elevenlabs": "your_elevenlabs_api_key_here",
    # "azure": "your_azure_api_key_here",
    # "google": "your_google_api_key_here",
}


# ============================================================
# Provider-Specific Configurations
# ============================================================

# MiniMax Configuration
MINIMAX_CONFIG = {
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

# OpenAI Configuration (Example - not yet implemented)
OPENAI_CONFIG = {
    "model": "tts-1-hd",
    "default_voice_settings": {
        "voice": "alloy",  # alloy, echo, fable, onyx, nova, shimmer
        "speed": 1.0
    }
}

# ElevenLabs Configuration (Example - not yet implemented)
ELEVENLABS_CONFIG = {
    "model_id": "eleven_multilingual_v2",
    "default_voice_settings": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "stability": 0.5,
        "similarity_boost": 0.75
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
