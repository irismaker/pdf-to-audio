// PDF to Audio Converter - Frontend Logic

// State
let selectedFile = null;
let currentJobId = null;
let progressInterval = null;
let currentAudio = null;  // Global audio control to prevent overlapping playback
let previewAudio = null;  // Audio element for preview playback
let inputMode = 'pdf';  // 'pdf' or 'text'

// DOM Elements
const elements = {
    apiKey: document.getElementById('api-key'),
    apiUrl: document.getElementById('api-url'),
    provider: document.getElementById('provider'),
    language: document.getElementById('language'),
    tabPdf: document.getElementById('tab-pdf'),
    tabText: document.getElementById('tab-text'),
    pdfSection: document.getElementById('pdf-section'),
    textSection: document.getElementById('text-section'),
    pdfFile: document.getElementById('pdf-file'),
    dropZone: document.getElementById('drop-zone'),
    uploadPrompt: document.getElementById('upload-prompt'),
    fileInfo: document.getElementById('file-info'),
    fileName: document.getElementById('file-name'),
    fileSize: document.getElementById('file-size'),
    removeFileBtn: document.getElementById('remove-file'),
    textInput: document.getElementById('text-input'),
    textCharCount: document.getElementById('text-char-count'),
    clearTextBtn: document.getElementById('clear-text-btn'),
    voiceId: document.getElementById('voice-id'),
    speed: document.getElementById('speed'),
    speedValue: document.getElementById('speed-value'),
    pitch: document.getElementById('pitch'),
    pitchValue: document.getElementById('pitch-value'),
    emotion: document.getElementById('emotion'),
    previewBtn: document.getElementById('preview-btn'),
    previewBtnText: document.getElementById('preview-btn-text'),
    previewBtnSpinner: document.getElementById('preview-btn-spinner'),
    stopPreviewBtn: document.getElementById('stop-preview-btn'),
    previewAudioElement: document.getElementById('preview-audio'),
    convertBtn: document.getElementById('convert-btn'),
    convertBtnText: document.getElementById('convert-btn-text'),
    convertBtnSpinner: document.getElementById('convert-btn-spinner'),
    progressSection: document.getElementById('progress-section'),
    progressBar: document.getElementById('progress-bar'),
    progressMessage: document.getElementById('progress-message'),
    resultsSection: document.getElementById('results-section'),
    resultsList: document.getElementById('results-list'),
    downloadAllBtn: document.getElementById('download-all-btn'),
    alertContainer: document.getElementById('alert-container')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadProviders();
    loadVoicesForProvider(); // Load initial voices
});

// Event Listeners
function initializeEventListeners() {
    // Tab switching
    elements.tabPdf.addEventListener('click', () => switchTab('pdf'));
    elements.tabText.addEventListener('click', () => switchTab('text'));

    // File upload
    elements.dropZone.addEventListener('click', () => elements.pdfFile.click());
    elements.pdfFile.addEventListener('change', handleFileSelect);
    elements.removeFileBtn.addEventListener('click', removeFile);

    // Drag and drop
    elements.dropZone.addEventListener('dragover', handleDragOver);
    elements.dropZone.addEventListener('dragleave', handleDragLeave);
    elements.dropZone.addEventListener('drop', handleDrop);

    // Text input
    elements.textInput.addEventListener('input', updateCharCount);
    elements.clearTextBtn.addEventListener('click', clearText);

    // Provider selection
    elements.provider.addEventListener('change', () => {
        updateApiUrlPlaceholder();
        loadVoicesForProvider();
    });

    // Language selection
    elements.language.addEventListener('change', () => {
        loadVoicesForProvider();
    });

    // Voice settings
    elements.speed.addEventListener('input', () => {
        elements.speedValue.textContent = elements.speed.value;
    });
    elements.pitch.addEventListener('input', () => {
        elements.pitchValue.textContent = elements.pitch.value;
    });

    // Preview buttons
    elements.previewBtn.addEventListener('click', previewVoice);
    elements.stopPreviewBtn.addEventListener('click', stopPreview);

    // Convert button
    elements.convertBtn.addEventListener('click', startConversion);

    // Download all button
    elements.downloadAllBtn.addEventListener('click', downloadAllFiles);
}

// Tab Switching
function switchTab(tab) {
    inputMode = tab;

    if (tab === 'pdf') {
        // Show PDF section, hide text section
        elements.pdfSection.classList.remove('hidden');
        elements.textSection.classList.add('hidden');

        // Update tab buttons
        elements.tabPdf.classList.add('active', 'border-accent', 'text-accent');
        elements.tabPdf.classList.remove('border-transparent', 'text-text-secondary');
        elements.tabText.classList.remove('active', 'border-accent', 'text-accent');
        elements.tabText.classList.add('border-transparent', 'text-text-secondary');
    } else {
        // Show text section, hide PDF section
        elements.textSection.classList.remove('hidden');
        elements.pdfSection.classList.add('hidden');

        // Update tab buttons
        elements.tabText.classList.add('active', 'border-accent', 'text-accent');
        elements.tabText.classList.remove('border-transparent', 'text-text-secondary');
        elements.tabPdf.classList.remove('active', 'border-accent', 'text-accent');
        elements.tabPdf.classList.add('border-transparent', 'text-text-secondary');
    }
}

// Text Input Handling
function updateCharCount() {
    const charCount = elements.textInput.value.length;
    elements.textCharCount.textContent = charCount.toLocaleString();
}

function clearText() {
    elements.textInput.value = '';
    updateCharCount();
}

// File Handling
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    elements.dropZone.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    elements.dropZone.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    elements.dropZone.classList.remove('drag-over');

    const file = event.dataTransfer.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

function validateAndSetFile(file) {
    // Check if it's a PDF
    if (file.type !== 'application/pdf') {
        showAlert('Only PDF files are allowed', 'error');
        return;
    }

    // Check file size (50MB max)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File size must be less than 50MB', 'error');
        return;
    }

    selectedFile = file;
    displayFileInfo(file);
}

function displayFileInfo(file) {
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
    elements.uploadPrompt.classList.add('hidden');
    elements.fileInfo.classList.remove('hidden');
}

function removeFile() {
    selectedFile = null;
    elements.pdfFile.value = '';
    elements.uploadPrompt.classList.remove('hidden');
    elements.fileInfo.classList.add('hidden');
}

function updateApiUrlPlaceholder() {
    const provider = elements.provider.value;
    const apiUrlMap = {
        'minimax': 'https://api.ppio.com/v3/minimax-speech-2.8-hd',
        'novita': 'https://api.novita.ai/v3/minimax-speech-2.8-turbo',
        'elevenlabs': 'https://api.elevenlabs.io/v1/text-to-speech',
        'azure': 'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1',
        'google': 'https://texttospeech.googleapis.com/v1/text:synthesize'
    };

    const defaultUrl = apiUrlMap[provider] || apiUrlMap['minimax'];
    elements.apiUrl.value = defaultUrl;
    elements.apiUrl.placeholder = defaultUrl;
}

// API Functions
async function loadProviders() {
    try {
        const response = await fetch('/api/providers');
        const data = await response.json();

        if (data.success) {
            // Providers loaded (currently only MiniMax)
            console.log('Available providers:', data.providers);
        }
    } catch (error) {
        console.error('Error loading providers:', error);
    }
}

async function startConversion() {
    // Stop any playing audio before starting new conversion
    stopAllAudio();

    // Hide previous results
    elements.resultsSection.classList.add('hidden');
    elements.resultsList.innerHTML = '';

    // Validate inputs
    if (!elements.apiKey.value.trim()) {
        showAlert('Please enter your API key', 'error');
        elements.apiKey.classList.add('shake');
        setTimeout(() => elements.apiKey.classList.remove('shake'), 500);
        return;
    }

    // Validate based on input mode
    if (inputMode === 'pdf') {
        if (!selectedFile) {
            showAlert('Please select a PDF file', 'error');
            elements.dropZone.classList.add('shake');
            setTimeout(() => elements.dropZone.classList.remove('shake'), 500);
            return;
        }
    } else {
        if (!elements.textInput.value.trim()) {
            showAlert('Please enter some text to convert', 'error');
            elements.textInput.classList.add('shake');
            setTimeout(() => elements.textInput.classList.remove('shake'), 500);
            return;
        }
    }

    // Prepare form data
    const formData = new FormData();

    if (inputMode === 'pdf') {
        formData.append('pdf_file', selectedFile);
    } else {
        formData.append('text_content', elements.textInput.value.trim());
    }

    formData.append('api_key', elements.apiKey.value.trim());
    formData.append('api_url', elements.apiUrl.value.trim());
    formData.append('provider', elements.provider.value);
    formData.append('language', elements.language.value);
    formData.append('voice_id', elements.voiceId.value);
    formData.append('speed', elements.speed.value);
    formData.append('pitch', elements.pitch.value);
    formData.append('emotion', elements.emotion.value);

    // Disable convert button
    setConvertButtonState(true);

    // Hide results from previous conversion
    elements.resultsSection.classList.add('hidden');
    elements.resultsList.innerHTML = '';

    // Show progress section
    elements.progressSection.classList.remove('hidden');
    updateProgress(0, 'Starting conversion...');

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Conversion failed');
        }

        currentJobId = data.job_id;
        showAlert('Conversion started successfully!', 'success');

        // Start polling for progress
        startProgressPolling();

    } catch (error) {
        showAlert(error.message, 'error');
        setConvertButtonState(false);
        elements.progressSection.classList.add('hidden');
    }
}

function startProgressPolling() {
    // Poll every 2 seconds
    progressInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/progress/${currentJobId}`);
            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Failed to get progress');
            }

            updateProgress(data.progress, data.message);

            if (data.status === 'completed') {
                clearInterval(progressInterval);
                handleConversionComplete(data.files);
            } else if (data.status === 'error') {
                clearInterval(progressInterval);
                handleConversionError(data.message);
            }

        } catch (error) {
            clearInterval(progressInterval);
            handleConversionError(error.message);
        }
    }, 2000);
}

function updateProgress(percent, message) {
    elements.progressBar.style.width = `${percent}%`;
    elements.progressMessage.textContent = message;
}

function handleConversionComplete(files) {
    setConvertButtonState(false);
    showAlert('Conversion completed successfully!', 'success');

    // Display results
    displayResults(files);

    // Reset progress after a delay
    setTimeout(() => {
        elements.progressSection.classList.add('hidden');
        updateProgress(0, '');
    }, 2000);
}

function handleConversionError(message) {
    setConvertButtonState(false);
    elements.progressSection.classList.add('hidden');
    showAlert(message || 'Conversion failed', 'error');
}

function displayResults(files) {
    elements.resultsSection.classList.remove('hidden');
    elements.resultsList.innerHTML = '';

    files.forEach((file, index) => {
        const fileCard = createFileCard(file, index);
        elements.resultsList.appendChild(fileCard);
    });

    // Show "Download All" button if more than one file
    if (files.length > 1) {
        elements.downloadAllBtn.classList.remove('hidden');
    } else {
        elements.downloadAllBtn.classList.add('hidden');
    }
}

function createFileCard(file, index) {
    const card = document.createElement('div');
    card.className = 'file-card';
    card.style.animationDelay = `${index * 0.1}s`;

    card.innerHTML = `
        <div class="file-card-info">
            <svg class="h-10 w-10 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
            <div>
                <p class="font-medium text-text-primary">${file.filename}</p>
                <p class="text-sm text-text-secondary">${file.size_mb} MB</p>
            </div>
        </div>
        <div class="file-card-actions">
            <button class="btn-play" data-filename="${file.filename}">▶ Play</button>
            <button class="btn-download" data-filename="${file.filename}">
                <svg class="inline-block h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download
            </button>
        </div>
    `;

    // Add event listeners
    const playBtn = card.querySelector('.btn-play');
    const downloadBtn = card.querySelector('.btn-download');

    playBtn.addEventListener('click', function() {
        toggleAudio(file.filename, this);
    });

    downloadBtn.addEventListener('click', function() {
        downloadFile(file.filename);
    });

    return card;
}

function stopAllAudio() {
    // Stop any currently playing audio
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }

    // Reset all play buttons
    document.querySelectorAll('.btn-play').forEach(btn => {
        btn.textContent = '▶ Play';
        btn.classList.remove('playing');
    });
}

function playAudio(filename, buttonElement) {
    // Stop any currently playing audio first
    stopAllAudio();

    // Create and play new audio
    currentAudio = new Audio(`/api/download/${currentJobId}/${filename}`);

    // Update button state
    if (buttonElement) {
        buttonElement.textContent = '⏸ Pause';
        buttonElement.classList.add('playing');
    }

    // Handle audio end
    currentAudio.addEventListener('ended', () => {
        if (buttonElement) {
            buttonElement.textContent = '▶ Play';
            buttonElement.classList.remove('playing');
        }
        currentAudio = null;
    });

    // Handle play errors
    currentAudio.play().catch(error => {
        showAlert('Failed to play audio: ' + error.message, 'error');
        if (buttonElement) {
            buttonElement.textContent = '▶ Play';
            buttonElement.classList.remove('playing');
        }
        currentAudio = null;
    });
}

function toggleAudio(filename, buttonElement) {
    // If this audio is playing, pause it
    if (currentAudio && buttonElement.classList.contains('playing')) {
        currentAudio.pause();
        buttonElement.textContent = '▶ Play';
        buttonElement.classList.remove('playing');
        currentAudio = null;
    } else {
        // Play the audio
        playAudio(filename, buttonElement);
    }
}

function downloadFile(filename) {
    const link = document.createElement('a');
    link.href = `/api/download/${currentJobId}/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function downloadAllFiles() {
    const link = document.createElement('a');
    link.href = `/api/download-all/${currentJobId}`;
    link.download = `audio_files_${currentJobId}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// UI Helper Functions
function setConvertButtonState(loading) {
    elements.convertBtn.disabled = loading;
    if (loading) {
        elements.convertBtnText.textContent = 'Converting...';
        elements.convertBtnSpinner.classList.remove('hidden');
    } else {
        elements.convertBtnText.textContent = 'Convert to Audio';
        elements.convertBtnSpinner.classList.add('hidden');
    }
}

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;

    const icon = getAlertIcon(type);

    alert.innerHTML = `
        ${icon}
        <span>${message}</span>
    `;

    elements.alertContainer.appendChild(alert);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

function getAlertIcon(type) {
    const icons = {
        success: `
            <svg class="h-5 w-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
        `,
        error: `
            <svg class="h-5 w-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
        `,
        warning: `
            <svg class="h-5 w-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
        `,
        info: `
            <svg class="h-5 w-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
        `
    };

    return icons[type] || icons.info;
}

// Voice and Language Functions
async function loadVoicesForProvider() {
    const provider = elements.provider.value;
    const language = elements.language.value;

    try {
        const response = await fetch(`/api/voices/${provider}`);
        const data = await response.json();

        if (!data.success) {
            console.error('Failed to load voices:', data.error);
            return;
        }

        // Clear existing options
        elements.voiceId.innerHTML = '';

        // Voice mapping for different providers and languages
        const voiceMapping = {
            'minimax': {
                'en-US': [
                    { id: 'male-qn-qingse', name: 'Young Male', group: 'Male Voices' },
                    { id: 'male-qn-jingying', name: 'Professional Male', group: 'Male Voices' },
                    { id: 'male-qn-badao', name: 'Commanding Male', group: 'Male Voices' },
                    { id: 'male-qn-daxuesheng', name: 'College Student Male', group: 'Male Voices' },
                    { id: 'female-shaonv', name: 'Young Female', group: 'Female Voices' },
                    { id: 'female-yujie', name: 'Mature Female', group: 'Female Voices' },
                    { id: 'female-chengshu', name: 'Sophisticated Female', group: 'Female Voices' },
                    { id: 'female-tianmei', name: 'Sweet Female', group: 'Female Voices' }
                ],
                'zh-CN': [
                    { id: 'male-qn-qingse', name: '青涩青年音色', group: '男声' },
                    { id: 'male-qn-jingying', name: '精英青年音色', group: '男声' },
                    { id: 'male-qn-badao', name: '霸道青年音色', group: '男声' },
                    { id: 'male-qn-daxuesheng', name: '青年大学生音色', group: '男声' },
                    { id: 'female-shaonv', name: '少女音色', group: '女声' },
                    { id: 'female-yujie', name: '御姐音色', group: '女声' },
                    { id: 'female-chengshu', name: '成熟女性音色', group: '女声' },
                    { id: 'female-tianmei', name: '甜美女性音色', group: '女声' }
                ]
            },
            'elevenlabs': {
                'en-US': data.voices.premade || []
            },
            'azure': {
                'en-US': data.voices['en-US'] || [],
                'zh-CN': data.voices['zh-CN'] || [],
                'ja-JP': data.voices['ja-JP'] || []
            },
            'google': {
                'en-US': data.voices['en-US'] || [],
                'zh-CN': data.voices['zh-CN'] || [],
                'ja-JP': data.voices['ja-JP'] || []
            }
        };

        // Get voices for current provider and language
        let voices = [];
        if (voiceMapping[provider] && voiceMapping[provider][language]) {
            voices = voiceMapping[provider][language];
        } else if (voiceMapping[provider] && voiceMapping[provider]['en-US']) {
            // Fallback to English if language not available
            voices = voiceMapping[provider]['en-US'];
        }

        // Group voices by category
        const groups = {};
        voices.forEach(voice => {
            const group = voice.group || 'Voices';
            if (!groups[group]) {
                groups[group] = [];
            }
            groups[group].push(voice);
        });

        // Add optgroups and options
        Object.keys(groups).forEach(groupName => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = groupName;

            groups[groupName].forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.id;
                option.textContent = voice.name;
                optgroup.appendChild(option);
            });

            elements.voiceId.appendChild(optgroup);
        });

    } catch (error) {
        console.error('Error loading voices:', error);
    }
}

async function previewVoice() {
    // Stop any currently playing preview
    stopPreview();

    // Validate inputs
    if (!elements.apiKey.value.trim()) {
        showAlert('Please enter your API key to preview voice', 'error');
        elements.apiKey.classList.add('shake');
        setTimeout(() => elements.apiKey.classList.remove('shake'), 500);
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('api_key', elements.apiKey.value.trim());
    formData.append('api_url', elements.apiUrl.value.trim());
    formData.append('provider', elements.provider.value);
    formData.append('language', elements.language.value);
    formData.append('voice_id', elements.voiceId.value);
    formData.append('speed', elements.speed.value);
    formData.append('pitch', elements.pitch.value);
    formData.append('emotion', elements.emotion.value);

    // Set preview button loading state
    elements.previewBtn.disabled = true;
    elements.previewBtnText.textContent = 'Generating...';
    elements.previewBtnSpinner.classList.remove('hidden');

    try {
        const response = await fetch('/api/preview', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Preview generation failed');
        }

        // Get audio blob
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);

        // Play preview audio
        previewAudio = new Audio(audioUrl);

        // Update UI
        elements.previewBtn.classList.add('hidden');
        elements.stopPreviewBtn.classList.remove('hidden');

        // Handle audio end
        previewAudio.addEventListener('ended', () => {
            stopPreview();
            showAlert('Preview completed', 'success');
        });

        // Handle play errors
        previewAudio.play().catch(error => {
            showAlert('Failed to play preview: ' + error.message, 'error');
            stopPreview();
        });

        showAlert('Preview playing...', 'info');

    } catch (error) {
        showAlert(error.message, 'error');
        // Reset button state
        elements.previewBtn.disabled = false;
        elements.previewBtnText.textContent = 'Preview Voice';
        elements.previewBtnSpinner.classList.add('hidden');
    }
}

function stopPreview() {
    // Stop and cleanup preview audio
    if (previewAudio) {
        previewAudio.pause();
        previewAudio.currentTime = 0;
        previewAudio = null;
    }

    // Reset button states
    elements.previewBtn.disabled = false;
    elements.previewBtnText.textContent = 'Preview Voice';
    elements.previewBtnSpinner.classList.add('hidden');
    elements.previewBtn.classList.remove('hidden');
    elements.stopPreviewBtn.classList.add('hidden');
}

// Prevent page unload during conversion
window.addEventListener('beforeunload', (event) => {
    if (progressInterval) {
        event.preventDefault();
        event.returnValue = 'Conversion is in progress. Are you sure you want to leave?';
    }
});
