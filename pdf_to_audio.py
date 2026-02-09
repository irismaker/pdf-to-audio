#!/usr/bin/env python3
"""
PDF to Audio Converter
Convert PDF documents to audio using various TTS providers
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import PyPDF2

from providers import create_provider, get_available_providers


class PDFToAudioConverter:
    """Main converter class for PDF to audio conversion"""

    def __init__(self, provider_name: str, api_key: str, provider_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the converter with a TTS provider

        Args:
            provider_name: Name of the TTS provider (e.g., 'minimax', 'openai')
            api_key: API key for the provider
            provider_config: Additional provider-specific configuration
        """
        self.provider = create_provider(provider_name, api_key, provider_config)
        print(f"✓ Initialized {self.provider.get_provider_name()} TTS provider\n")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        print(f"📖 Reading PDF: {pdf_path}")

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(text)
                        print(f"  ✓ Read page {page_num + 1}")

                full_text = '\n'.join(text_content)
                print(f"✓ Complete! Extracted {len(full_text)} characters\n")
                return full_text

        except Exception as e:
            print(f"❌ Failed to read PDF: {e}")
            return ""

    def split_text(self, text: str, max_length: int = 5000) -> List[str]:
        """
        Split long text into multiple chunks

        Args:
            text: Original text
            max_length: Maximum length per chunk

        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        # Split by periods for better sentence boundaries
        sentences = text.replace('\n', ' ').split('. ')
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:
                current_chunk += sentence + '. '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def convert_pdf_to_audio(self, pdf_path: str, output_dir: Optional[str] = None,
                            voice_settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert PDF document to audio file

        Args:
            pdf_path: PDF file path
            output_dir: Output directory (optional)
            voice_settings: Voice settings (optional)

        Returns:
            Whether successful
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return False

        # Prepare output path
        pdf_name = Path(pdf_path).stem
        if output_dir is None:
            output_dir = str(Path(pdf_path).parent / "audio_output")

        os.makedirs(output_dir, exist_ok=True)

        # Split long text
        chunks = self.split_text(text)
        print(f"📝 Text split into {len(chunks)} chunk(s)\n")

        # Convert each chunk
        success_count = 0
        for i, chunk in enumerate(chunks, 1):
            if len(chunks) > 1:
                output_path = os.path.join(output_dir, f"{pdf_name}_part{i}.mp3")
            else:
                output_path = os.path.join(output_dir, f"{pdf_name}.mp3")

            print(f"[{i}/{len(chunks)}] Processing chunk {i}")
            if self.provider.text_to_speech(chunk, output_path, voice_settings):
                success_count += 1

        print(f"\n{'='*50}")
        print(f"✓ Complete! Successfully generated {success_count}/{len(chunks)} audio file(s)")
        print(f"📁 Output directory: {output_dir}")
        print(f"{'='*50}\n")

        return success_count == len(chunks)

    def batch_convert(self, pdf_dir: str, output_dir: Optional[str] = None,
                     voice_settings: Optional[Dict[str, Any]] = None):
        """
        Batch convert all PDF files in directory

        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Output directory (optional)
            voice_settings: Voice settings (optional)
        """
        pdf_files = list(Path(pdf_dir).glob("*.pdf"))

        if not pdf_files:
            print(f"❌ No PDF files found in {pdf_dir}")
            return

        print(f"🔍 Found {len(pdf_files)} PDF file(s)\n")
        print("="*50)

        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
            print("-"*50)
            self.convert_pdf_to_audio(str(pdf_file), output_dir, voice_settings)

        print("\n" + "="*50)
        print("🎉 Batch conversion complete!")
        print("="*50)


def main():
    """Main function"""
    print("="*50)
    print("📚 PDF to Audio Converter")
    print("="*50)
    print()

    # Display available providers
    providers = get_available_providers()
    print(f"Available TTS providers: {', '.join(providers)}")
    print()

    # Get provider selection
    provider_name = os.environ.get('TTS_PROVIDER', 'minimax').lower()
    print(f"Using provider: {provider_name}")

    # Get API Key from environment variable or user input
    api_key = os.environ.get('MINIMAX_API_KEY')  # For backward compatibility
    if not api_key:
        api_key = os.environ.get('TTS_API_KEY')

    if not api_key:
        api_key = input(f"Enter your {provider_name.title()} API Key: ").strip()

    if not api_key:
        print("❌ Error: API Key is required")
        sys.exit(1)

    # Create converter
    try:
        converter = PDFToAudioConverter(provider_name, api_key)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # Get input path
    input_path = input("Enter PDF file path or directory path: ").strip()

    if not os.path.exists(input_path):
        print(f"❌ Error: Path does not exist: {input_path}")
        sys.exit(1)

    # Optional: Custom voice settings
    print("\nVoice settings (press Enter to use defaults):")
    voice_settings = {}

    speed = input("  Speech rate (e.g., 0.5-2.0, default 1.0): ").strip()
    if speed:
        try:
            voice_settings['speed'] = float(speed)
        except ValueError:
            print("⚠️  Invalid speed value, using default")

    pitch = input("  Pitch (e.g., -12 to 12, default 0): ").strip()
    if pitch:
        try:
            voice_settings['pitch'] = int(pitch)
        except ValueError:
            print("⚠️  Invalid pitch value, using default")

    print("\nStarting conversion...\n")

    # Check if input is file or directory
    if os.path.isfile(input_path):
        converter.convert_pdf_to_audio(input_path, voice_settings=voice_settings if voice_settings else None)
    else:
        converter.batch_convert(input_path, voice_settings=voice_settings if voice_settings else None)


if __name__ == "__main__":
    main()
