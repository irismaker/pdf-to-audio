#!/usr/bin/env python3
"""
Quick Start Script
Easy-to-use script for batch converting PDFs using configuration file
"""

import os
from pathlib import Path
from pdf_to_audio import PDFToAudioConverter

# Try to load configuration
try:
    from config import TTS_PROVIDER, API_KEYS, MINIMAX_CONFIG, BATCH_SETTINGS
    print("✓ Loaded configuration file\n")
    provider_name = TTS_PROVIDER
    api_key = API_KEYS.get(TTS_PROVIDER)
    provider_config = MINIMAX_CONFIG if TTS_PROVIDER == "minimax" else {}
    voice_settings = provider_config.get("default_voice_settings", {})
except ImportError:
    print("⚠️  config.py not found. Please create one from config_example.py")
    print("   Or enter settings manually:\n")
    provider_name = "minimax"
    api_key = input("Enter your MiniMax API Key: ").strip()
    provider_config = {}
    voice_settings = {
        "speed": 1.0,
        "pitch": 0,
        "emotion": "neutral",
        "voice_id": "male-qn-qingse"
    }
    BATCH_SETTINGS = {
        "output_dir": "audio_output"
    }


def main():
    """Main function"""
    print("="*60)
    print("🚀 PDF to Audio - Quick Start")
    print("="*60)
    print()

    if not api_key or api_key == f"your_{provider_name}_api_key_here":
        print(f"❌ Error: Please set your API Key in config.py")
        return

    # Create converter
    try:
        converter = PDFToAudioConverter(provider_name, api_key, provider_config)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}\n")

    # Find PDF files in current directory
    pdf_files = list(current_dir.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDF files found in current directory")
        print("\nPlease choose an option:")
        print("1. Enter PDF file path")
        print("2. Enter PDF directory path")
        choice = input("Choose (1/2): ").strip()

        if choice == "1":
            pdf_path = input("Enter PDF file path: ").strip()
            if os.path.isfile(pdf_path):
                print(f"\nStarting conversion: {pdf_path}\n")
                converter.convert_pdf_to_audio(
                    pdf_path,
                    output_dir=BATCH_SETTINGS.get("output_dir"),
                    voice_settings=voice_settings
                )
            else:
                print(f"❌ File not found: {pdf_path}")

        elif choice == "2":
            pdf_dir = input("Enter PDF directory path: ").strip()
            if os.path.isdir(pdf_dir):
                print(f"\nStarting batch conversion: {pdf_dir}\n")
                converter.batch_convert(
                    pdf_dir,
                    output_dir=BATCH_SETTINGS.get("output_dir"),
                    voice_settings=voice_settings
                )
            else:
                print(f"❌ Directory not found: {pdf_dir}")
        return

    # Display found PDF files
    print(f"🔍 Found {len(pdf_files)} PDF file(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        file_size = pdf_file.stat().st_size / 1024  # KB
        print(f"  {i}. {pdf_file.name} ({file_size:.1f} KB)")
    print()

    # Ask user
    print("Please choose an option:")
    print("1. Convert all PDF files")
    print("2. Select specific files to convert")
    print("3. Cancel")

    choice = input("\nChoose (1/2/3): ").strip()

    if choice == "1":
        # Batch convert all files
        print("\n" + "="*60)
        print("Starting batch conversion...")
        print("="*60 + "\n")

        converter.batch_convert(
            str(current_dir),
            output_dir=BATCH_SETTINGS.get("output_dir"),
            voice_settings=voice_settings
        )

    elif choice == "2":
        # Select specific files
        file_nums = input("Enter file numbers (comma-separated, e.g., 1,3,5): ").strip()
        try:
            selected_indices = [int(n.strip()) - 1 for n in file_nums.split(",")]
            selected_files = [pdf_files[i] for i in selected_indices if 0 <= i < len(pdf_files)]

            if selected_files:
                print("\n" + "="*60)
                print(f"Converting {len(selected_files)} file(s)...")
                print("="*60 + "\n")

                for i, pdf_file in enumerate(selected_files, 1):
                    print(f"\n[{i}/{len(selected_files)}] Processing: {pdf_file.name}")
                    print("-"*60)
                    converter.convert_pdf_to_audio(
                        str(pdf_file),
                        output_dir=BATCH_SETTINGS.get("output_dir"),
                        voice_settings=voice_settings
                    )

                print("\n" + "="*60)
                print("🎉 Conversion complete!")
                print("="*60)
            else:
                print("❌ No valid files selected")

        except (ValueError, IndexError):
            print("❌ Invalid input format")

    elif choice == "3":
        print("Cancelled")
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
