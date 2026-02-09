"""
TTS Providers Package
Factory for creating TTS provider instances
"""

from typing import Dict, Any, Optional
from .base_provider import BaseTTSProvider
from .minimax_provider import MiniMaxProvider


# Registry of available providers
PROVIDERS = {
    'minimax': MiniMaxProvider,
    # Add more providers here as they are implemented
    # 'openai': OpenAIProvider,
    # 'elevenlabs': ElevenLabsProvider,
    # 'azure': AzureTTSProvider,
    # 'google': GoogleTTSProvider,
}


def create_provider(provider_name: str, api_key: str, config: Optional[Dict[str, Any]] = None) -> BaseTTSProvider:
    """
    Factory function to create TTS provider instances

    Args:
        provider_name: Name of the provider (e.g., 'minimax', 'openai')
        api_key: API key for the provider
        config: Additional configuration options

    Returns:
        Instance of the specified TTS provider

    Raises:
        ValueError: If provider_name is not supported
    """
    provider_name = provider_name.lower()

    if provider_name not in PROVIDERS:
        available = ', '.join(PROVIDERS.keys())
        raise ValueError(f"Provider '{provider_name}' not supported. Available providers: {available}")

    provider_class = PROVIDERS[provider_name]
    return provider_class(api_key, config)


def get_available_providers() -> list:
    """
    Get list of available provider names

    Returns:
        List of provider names
    """
    return list(PROVIDERS.keys())


__all__ = ['BaseTTSProvider', 'MiniMaxProvider', 'create_provider', 'get_available_providers', 'PROVIDERS']
