# Web Interface Quick Start Guide

## 🎉 Welcome to the PDF to Audio Web Interface!

The easiest way to convert your PDFs to audio - no command line knowledge required!

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

This will install:
- Flask (web framework)
- PyPDF2 (PDF processing)
- requests (API calls)

### Step 2: Start the Web Server

```bash
python3 app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

### Step 3: Open in Browser

Open your web browser and visit:
```
http://localhost:5000
```

## 📝 Using the Interface

### 1. Configure API
- **API Key**: Enter your MiniMax API key (required)
- **API URL**: Use the default PPIO endpoint or enter your custom MiniMax-compatible API URL
  - Default: `https://api.ppio.com/v3/minimax-speech-2.8-hd` (recommended)
  - You can change this to use MiniMax official API or other compatible endpoints
- Your API key is never stored and only used for this session

### 2. Upload PDF
- Click the upload area or drag & drop your PDF file
- Maximum file size: 50MB
- Only PDF files are supported

### 3. Customize Voice (Optional)
- **Voice**: Choose from 8 different voices (4 male, 4 female)
- **Speed**: Adjust from 0.5x (slower) to 2.0x (faster)
- **Pitch**: Adjust from -12 (lower) to +12 (higher)
- **Emotion**: Choose from: calm, happy, sad, angry, fearful, disgusted, surprised, fluent, whisper

### 4. Convert
- Click the "Convert to Audio" button
- Watch the real-time progress bar
- Status messages will keep you informed

### 5. Download Your Audio
- **Play**: Listen to the audio directly in your browser
- **Download**: Download individual MP3 files
- **Download All**: Get all files as a ZIP archive

## ✨ Features

### User-Friendly
- No need to find folders or manage files manually
- Everything happens in your browser
- Drag and drop file upload

### Real-Time Feedback
- Visual progress bar
- Status messages during conversion
- Error messages with helpful guidance

### Convenient
- Play audio before downloading
- Download all files at once as ZIP
- Automatic cleanup (files deleted after 1 hour)

### Modern Design
- Modern, clean interface design
- Smooth animations and transitions
- Works on both desktop and mobile

## 🔧 Troubleshooting

### "Connection Refused" Error
Make sure the Flask server is running:
```bash
python3 app.py
```

### "API Key Invalid" Error
- Check that you entered the correct API key
- Ensure you have API credits/quota remaining
- Try copying the key again (no extra spaces)

### PDF Upload Fails
- Check file size (must be under 50MB)
- Ensure the file is a valid PDF
- Try a different PDF file

### Can't Extract Text from PDF
- The PDF might be image-based (scanned document)
- Try using a PDF with selectable text
- Consider using OCR tools first

### Slow Conversion
- Large PDFs take longer to process
- Network speed affects API calls
- Be patient - progress bar shows status

## 💡 Tips

1. **Test with Small PDFs First**: Try a 1-2 page PDF before converting large documents

2. **Keep the Tab Open**: Don't close the browser tab during conversion

3. **Save Your Settings**: Note your preferred voice settings for future use

4. **Download Promptly**: Files are deleted after 1 hour for security

5. **Multiple Conversions**: You can convert multiple PDFs one after another

## 🎨 Voice Recommendations

### For Books & Articles
- **Voice**: Female - Sophisticated or Male - Professional
- **Speed**: 1.0x - 1.2x
- **Emotion**: Calm or Fluent

### For Stories & Fiction
- **Voice**: Female - Sweet or Male - Young
- **Speed**: 1.0x
- **Emotion**: Happy or Calm

### For Technical Content
- **Voice**: Male - Professional or Female - Mature
- **Speed**: 0.9x - 1.0x
- **Emotion**: Calm

### For Quick Review
- **Voice**: Any
- **Speed**: 1.5x - 2.0x
- **Emotion**: Fluent

## 🌐 Accessing from Other Devices

To access the web interface from other devices on your network:

1. Find your computer's IP address:
   ```bash
   # On Mac/Linux
   ifconfig | grep inet

   # On Windows
   ipconfig
   ```

2. On the other device, visit:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

   Example: `http://192.168.1.100:5000`

## 🛑 Stopping the Server

To stop the web server, press:
```
Ctrl + C
```

in the terminal where it's running.

## 📚 Next Steps

- Check out the [main README](README.md) for advanced usage
- Learn about [provider configuration](config_example.py)
- Explore the [command-line interface](quick_start.py)

---

Enjoy converting your PDFs to audio! 🎙️
