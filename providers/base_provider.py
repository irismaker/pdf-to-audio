"""
Base TTS Provider Interface
Defines the standard interface for all TTS providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TTS provider

        Args:
            api_key: API key for authentication
            config: Additional configuration options
        """
        self.api_key = api_key
        self.config = config or {}

    @abstractmethod
    def text_to_speech(self, text: str, output_path: str, voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert text to speech and save to file

        Args:
            text: Text to convert
            output_path: Path to save the audio file
            voice_settings: Voice customization settings

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get list of available voices for this provider

        Returns:
            Dictionary of available voices
        """
        pass

    @abstractmethod
    def get_default_voice_settings(self) -> Dict[str, Any]:
        """
        Get default voice settings for this provider

        Returns:
            Dictionary of default settings
        """
        pass

    def validate_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Validate voice settings

        Args:
            voice_settings: Settings to validate

        Returns:
            True if valid, False otherwise
        """
        return True

    def get_provider_name(self) -> str:
        """
        Get the name of this provider

        Returns:
            Provider name
        """
        return self.__class__.__name__.replace('Provider', '')
