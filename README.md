# Sudaverse Normalizer 🇸🇩

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust, production-ready text normalizer specifically designed for **Sudanese Arabic dialect**. This tool handles the unique characteristics of Sudanese Arabic, including dialect-specific spelling variations, colloquialisms, and mixed Arabic-Latin text.

## ✨ Features

- **🎯 Sudanese Dialect-Specific**: Tailored for Sudanese Arabic text patterns and common expressions
- **🔤 Unicode Normalization**: Proper handling of Arabic text encoding (NFKC, NFC, NFD, NFKD)
- **📝 Diacritic Handling**: Remove or preserve Arabic diacritics (tashkeel) with flexible options
- **🔢 Number Normalization**: Convert Arabic-Indic numerals to Western numerals
- **✂️ Character Normalization**: 
  - Normalize all Alef variants (أ، إ، آ، ٱ) to ا
  - Normalize Yeh variants (ى، ئ) to ي
  - Normalize Teh Marbuta (ة) to Heh (ه)
- **🧹 Cleaning Features**:
  - Remove URLs, emails, mentions, and hashtags
  - Remove repeated characters (e.g., "كتييييير" → "كتيير")
  - Normalize punctuation and whitespace
- **⚙️ Highly Configurable**: 20+ configuration options for custom normalization pipelines
- **📊 Batch Processing**: Efficient folder-based processing with real-time progress tracking
- **📈 Statistics**: Get detailed statistics about text transformation

## 📦 Installation

### Requirements
- Python 3.7 or higher

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start Guide

### For First-Time Users

#### Step 1: Prepare Your Text Files

1. Open the `raw-text` folder in your project directory
2. Place your Sudanese Arabic text files (`.txt` format) in this folder
3. You can have as many files as you want!

#### Step 2: Run the Batch Processor

Open your terminal in the project directory and run:

```bash
python batch_processor.py
```

#### Step 3: Get Your Results

- ✅ Normalized files will be saved in the `normalized-text` folder
- 📊 You'll see progress, ETA, and statistics during processing
- 🎉 Done! Your texts are normalized and ready to use

### What You'll See

During processing, you'll see real-time updates:

```
================================================================================
🇸🇩 SUDAVERSE NORMALIZER - BATCH PROCESSOR 🇸🇩
================================================================================

📂 Scanning directory: C:\dev\sudaverse-normalizer\raw-text
✅ Found 3 text file(s)
📁 Output directory: C:\dev\sudaverse-normalizer\normalized-text

🚀 Starting normalization...

[████████████████████████████████████████] 100.0% (3/3)
📄 Processing: sample3.txt
⏱️  Elapsed: 0.2s | ETA: 0.0s
📊 Speed: 40.9 KB/s | Compression: 24.8%
📈 Total: Input 1.3 KB → Output 963 chars

================================================================================
📊 PROCESSING SUMMARY
================================================================================

⏱️  Total Time: 0.2s
⚡ Average Speed: 39.6 KB/s
📄 Files Processed: 3/3
📥 Input Size: 1.3 KB
📤 Output Size: 963 chars
📉 Size Reduction: 376 chars (28.1%)
✅ Normalized files saved to: normalized-text
================================================================================
```

## 📋 Batch Processing Options

### Basic Usage

```bash
# Process all files in raw-text folder with default settings
python batch_processor.py
```

### Advanced Options

```bash
# Custom input/output directories
python batch_processor.py -i my_input -o my_output

# Remove English words, convert Arabic numbers to Western, remove timestamps
python batch_processor.py --remove-latin

# Keep hashtags for social media analysis
python batch_processor.py --keep-hashtags

# Convert Arabic-Indic numbers to Western (١٢٣ → 123)
python batch_processor.py --normalize-numbers

# Remove diacritics
python batch_processor.py --no-diacritics

# Custom character repetition limit
python batch_processor.py --max-repeat 3

# Combine multiple options (pure Arabic with no diacritics)
python batch_processor.py --remove-latin --no-diacritics
```

### Get Help

```bash
python batch_processor.py --help
```

## 💻 Python API Usage

### Basic Normalization

```python
from normalizer_code import SudaneseNormalizer

# Initialize with default configuration
normalizer = SudaneseNormalizer()

# Normalize text
text = "السَّلامُ عليكم!! أنا بحب السودان شديييييييد"
normalized = normalizer.normalize(text)
print(normalized)
# Output: "السلام عليكم! انا بحب السودان شديد"
```

### Custom Configuration

```python
from normalizer_code import SudaneseNormalizer, NormalizationConfig

# Create custom configuration
config = NormalizationConfig(
    remove_diacritics=True,
    keep_shadda=True,           # Keep shadda (ّ) even when removing diacritics
    normalize_alef=True,
    normalize_yeh=True,
    remove_urls=True,
    remove_hashtags=False,      # Keep hashtags
    normalize_numbers=True,     # Convert ١٢٣ to 123
    max_char_repeat=2           # Allow max 2 repeated chars
)

# Initialize normalizer with custom config
normalizer = SudaneseNormalizer(config=config)

# Normalize text
text = "يااااا أخوي الموقع: https://example.com #السودان ١٢٣"
normalized = normalizer.normalize(text)
print(normalized)
# Output: "يا اخوي الموقع: #السودان 123"
```

## 📖 Configuration Options

All configuration options with their default values:

```python
@dataclass
class NormalizationConfig:
    # Unicode normalization
    unicode_form: str = "NFKC"  # Options: NFC, NFD, NFKC, NFKD
    
    # Diacritics
    remove_diacritics: bool = True
    keep_shadda: bool = False
    
    # Character normalization
    normalize_alef: bool = True
    normalize_yeh: bool = True
    normalize_teh: bool = True
    
    # Punctuation
    normalize_punctuation: bool = True
    remove_repeated_punctuation: bool = True
    
    # Whitespace
    normalize_whitespace: bool = True
    remove_extra_spaces: bool = True
    
    # Numbers
    normalize_numbers: bool = False
    remove_numbers: bool = False
    
    # Special cleaning
    remove_urls: bool = True
    remove_emails: bool = True
    remove_mentions: bool = True
    remove_hashtags: bool = False
    remove_latin_chars: bool = False  # Remove English/Latin words (keeps numbers)
    remove_timestamps: bool = True  # Remove timestamps in all formats
    
    # Text length
    min_length: int = 0
    max_length: Optional[int] = None
    
    # Repetition
    remove_repeated_chars: bool = True
    max_char_repeat: int = 2
```

## 💡 Common Use Cases

### 1. Social Media Text Cleaning

```python
from normalizer_code import SudaneseNormalizer, NormalizationConfig

config = NormalizationConfig(
    remove_urls=True,
    remove_mentions=True,
    remove_hashtags=False,  # Keep hashtags for analysis
    remove_repeated_chars=True,
    normalize_alef=True,
    normalize_yeh=True
)

normalizer = SudaneseNormalizer(config=config)
tweet = "@user1 شوف https://example.com #السودان_الحبيب واااااو"
clean_tweet = normalizer.normalize(tweet)
```

### 2. NLP Model Preprocessing

```python
config = NormalizationConfig(
    remove_diacritics=True,
    normalize_alef=True,
    normalize_yeh=True,
    normalize_teh=True,
    normalize_numbers=True,
    remove_urls=True,
    remove_emails=True,
    remove_mentions=True,
    remove_repeated_chars=True,
    remove_latin_chars=True  # Pure Arabic for NLP models
)

normalizer = SudaneseNormalizer(config=config)
```

### 3. Batch Processing via API

```python
from batch_processor import BatchProcessor
from normalizer_code import NormalizationConfig

# Create custom configuration
config = NormalizationConfig(
    remove_diacritics=True,
    normalize_numbers=True,
    remove_hashtags=False
)

# Initialize processor
processor = BatchProcessor(
    input_dir="raw-text",
    output_dir="normalized-text",
    config=config
)

# Process all files with progress tracking
processor.process_all()
```

### 4. In-Memory Batch Processing

```python
normalizer = SudaneseNormalizer()

texts = [
    "النص الأول",
    "النص الثاني", 
    "النص الثالث"
]

# Process with progress bar (requires tqdm)
normalized_texts = normalizer.normalize_batch(texts, show_progress=True)
```

### 5. Text Statistics

```python
normalizer = SudaneseNormalizer()

text = "السَّلامُ عليكم!!! كيييييف الحال"
stats = normalizer.get_stats(text)

print(stats)
# Output:
# {
#     'original_length': 36,
#     'normalized_length': 24,
#     'compression_ratio': 0.33,
#     'original_words': 4,
#     'normalized_words': 4,
#     'removed_chars': 12
# }
```

## 📊 What Gets Normalized?

### ✅ Cleaned/Removed:
- ❌ Diacritics (تَشْكِيل)
- ❌ URLs (https://...)
- ❌ Emails (user@example.com)
- ❌ @mentions (configurable)
- ❌ #hashtags (configurable)
- ❌ English/Latin words (configurable - keeps numbers, converts Arabic numerals to Western)
- ❌ Timestamps in all formats (HH:MM, DD/MM/YYYY, ISO, Unix, etc.)
- ❌ Excessive character repetition (ياااااا → ياا)
- ❌ Extra whitespace

### ✅ Normalized:
- أ إ آ ٱ → ا (all Alef variants)
- ى ئ → ي (all Yeh variants)  
- ة → ه (Teh Marbuta to Heh)
- ؤ → و (Waw with Hamza)
- ؟ → ? (Arabic punctuation)
- ، → , (Arabic comma)
- ؛ → ; (Arabic semicolon)
- ١٢٣٤٥٦٧٨٩ → 123456789 (Arabic-Indic to Western numerals)
- ۰۱۲۳۴۵۶۷۸۹ → 0123456789 (Persian to Western numerals)

## 🔧 Advanced Features

### Sudanese Dialect Patterns

The normalizer includes specific handling for common Sudanese dialect patterns and expressions. This is automatically applied during normalization.

### Multiple Encoding Support

The batch processor automatically tries multiple encodings when reading files:
- UTF-8 (with and without BOM)
- CP1256 (Arabic Windows encoding)
- ISO-8859-6 (Arabic ISO encoding)
- Latin-1 (fallback)

## 🛠️ Project Structure

```
sudaverse-normalizer/
├── normalizer_code.py      # Main normalizer implementation
├── batch_processor.py      # Batch file processing with progress tracking
├── raw-text/              # Input folder for batch processing (with sample files)
├── normalized-text/       # Output folder for normalized files
├── requirements.txt        # Python dependencies (tqdm for progress bars)
├── README.md              # This file - complete documentation
├── LICENSE                # MIT License
├── DEPLOYMENT.md          # GitHub deployment guide
└── .gitignore            # Git ignore file
```

## 🚨 Troubleshooting

### "No text files found"
- Make sure your files have `.txt` extension
- Check that files are in the `raw-text` folder
- Verify the folder path is correct

### "Module not found"
- Run: `pip install -r requirements.txt`
- Make sure you're in the project directory
- Check Python environment is activated

### Encoding Issues
- The processor automatically tries multiple encodings (UTF-8, CP1256, etc.)
- If a file still fails, try re-saving it as UTF-8
- Check for corrupted or binary files

### Import Errors
- Ensure all files are in the same directory
- Verify file names: `normalizer_code.py` (underscore, not hyphen)
- Check Python version is 3.7+

## 🎯 GitHub Deployment

### Quick Deployment Steps

1. **Initialize Git Repository**
```bash
git init
git add .
git commit -m "Initial commit: Sudanese dialect text normalizer with batch processing"
```

2. **Create GitHub Repository**
- Go to https://github.com/new
- Name: `sudaverse-normalizer`
- Description: "Robust text normalizer for Sudanese Arabic dialect with batch processing"
- Don't initialize with README (we have one!)
- Create repository

3. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/sudaverse-normalizer.git
git branch -M main
git push -u origin main
```

4. **Add Topics** (on GitHub)
- python
- nlp
- arabic
- sudanese
- text-normalization
- arabic-nlp
- sudanese-arabic
- text-processing
- batch-processing

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Sudanese NLP Community**

## 🙏 Acknowledgments

- Inspired by the needs of Sudanese Arabic NLP research
- Built for the Sudanese developer and researcher community
- Contributions from Sudanese dialect experts

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

## 🗺️ Roadmap

- [ ] Add support for more Sudanese dialect patterns
- [ ] Implement spell checking for common Sudanese words
- [ ] Add transliteration support
- [ ] Create web API version
- [ ] Add more comprehensive test coverage
- [ ] Performance optimizations for large-scale processing
- [ ] GUI application for non-technical users

## 📊 Performance

- Processes ~40,000 characters per second on average hardware
- Memory efficient - suitable for large-scale batch processing
- Optimized regex patterns for speed
- Real-time progress tracking with ETA
- Handles multiple file encodings automatically

## 🧪 Testing

The project has been tested with:
- ✅ Various Sudanese dialect texts
- ✅ Social media content (Twitter, Facebook)
- ✅ News articles
- ✅ Literary texts
- ✅ Mixed Arabic-English content
- ✅ Multiple file encodings

---

**Made with ❤️ by Sudaverse for the Sudanese NLP Community** 🇸🇩
