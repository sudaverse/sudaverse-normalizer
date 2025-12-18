"""
Sudanese Dialect Text Normalizer (Production Ready)
===================================================
A robust normalizer for Sudanese Arabic dialect text preprocessing.

Features:
- Unicode normalization
- Diacritic handling
- Punctuation normalization
- Number normalization
- Whitespace cleaning
- Sudanese-specific character handling
- Configurable normalization levels

Author: Sudanese NLP Community
License: MIT
"""

import re
import unicodedata
from typing import Optional, Dict, List
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NormalizationConfig:
    """Configuration for text normalization."""
    
    # Unicode normalization
    unicode_form: str = "NFKC"  # Options: NFC, NFD, NFKC, NFKD
    
    # Diacritics
    remove_diacritics: bool = True
    keep_shadda: bool = False  # Keep shadda (ّ) even if removing diacritics
    
    # Characters
    normalize_alef: bool = True  # Normalize all alef forms to ا
    normalize_yeh: bool = True   # Normalize ى to ي
    normalize_teh: bool = True   # Normalize ة to ه
    
    # Punctuation
    normalize_punctuation: bool = True
    remove_repeated_punctuation: bool = True
    
    # Whitespace
    normalize_whitespace: bool = True
    remove_extra_spaces: bool = True
    
    # Numbers
    normalize_numbers: bool = False  # Convert Arabic-Indic to Western
    remove_numbers: bool = False
    
    # Special cleaning
    remove_urls: bool = True
    remove_emails: bool = True
    remove_mentions: bool = True  # Remove @mentions
    remove_hashtags: bool = False  # Keep hashtags by default
    remove_latin_chars: bool = False  # Remove English/Latin characters
    remove_timestamps: bool = True  # Remove timestamps in all formats
    
    # Text length
    min_length: int = 0  # Minimum character length
    max_length: Optional[int] = None
    
    # Repetition
    remove_repeated_chars: bool = True  # ممممتاااااز -> متاز
    max_char_repeat: int = 2  # Maximum allowed character repetition


class SudaneseNormalizer:
    """
    Production-ready normalizer for Sudanese Arabic dialect.
    """
    
    # Arabic character mappings
    ALEF_VARIANTS = ['أ', 'إ', 'آ', 'ٱ', 'ٲ', 'ٳ', 'ء']
    YEH_VARIANTS = ['ى', 'ي', 'ئ']
    WAW_VARIANTS = ['ؤ', 'و']
    
    # Arabic diacritics (tashkeel)
    DIACRITICS = [
        '\u064B',  # Fathatan
        '\u064C',  # Dammatan
        '\u064D',  # Kasratan
        '\u064E',  # Fatha
        '\u064F',  # Damma
        '\u0650',  # Kasra
        '\u0651',  # Shadda
        '\u0652',  # Sukun
        '\u0653',  # Maddah
        '\u0654',  # Hamza above
        '\u0655',  # Hamza below
        '\u0656',  # Subscript alef
        '\u0657',  # Inverted damma
        '\u0658',  # Mark noon ghunna
        '\u0670',  # Superscript alef
    ]
    
    # Punctuation mappings
    PUNCTUATION_MAP = {
        '؟': '?',  # Arabic question mark
        '،': ',',  # Arabic comma
        '؛': ';',  # Arabic semicolon
        '‹': '<',
        '›': '>',
        '«': '"',
        '»': '"',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '–': '-',
        '—': '-',
        '…': '...',
    }
    
    # Arabic-Indic to Western numerals
    ARABIC_INDIC_MAP = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    }
    
    # Sudanese dialect-specific normalization patterns
    SUDANESE_PATTERNS = {
        # Common Sudanese colloquial spelling variations
        'كده': 'كدا',  # Common Sudanese spelling
        'كدا': 'كدا',
        'ياخ': 'يا اخ',  # Common Sudanese expression
        'ياخي': 'يا اخي',
        'شنو': 'شنو',  # What (Sudanese)
        'كيف': 'كيف',
        'داير': 'داير',  # Wanting (Sudanese)
        'دايرة': 'دايرة',
    }
    
    def __init__(self, config: Optional[NormalizationConfig] = None):
        """
        Initialize the normalizer with configuration.
        
        Args:
            config: NormalizationConfig object. If None, uses default config.
        """
        self.config = config or NormalizationConfig()
        self._compile_patterns()
        logger.info("Sudanese Normalizer initialized")
    
    def _compile_patterns(self):
        """Compile regex patterns for efficiency."""
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
        self.mention_pattern = re.compile(r'@\w+')
        self.hashtag_pattern = re.compile(r'#\w+')
        self.repeated_char_pattern = re.compile(r'(.)\1{' + str(self.config.max_char_repeat) + r',}')
        self.whitespace_pattern = re.compile(r'\s+')
        self.repeated_punct_pattern = re.compile(r'([!?.,:;])\1+')
    
    def normalize(self, text: str) -> str:
        """
        Apply all normalization steps to the text.
        
        Args:
            text: Input text string
            
        Returns:
            Normalized text string
            
        Raises:
            ValueError: If text is not a string
        """
        if text is None:
            return ""
        
        if not isinstance(text, str):
            raise ValueError(f"Expected string input, got {type(text).__name__}")
        
        if not text.strip():
            return ""
        
        # Apply normalization pipeline
        text = self._normalize_unicode(text)
        
        if self.config.remove_urls:
            text = self._remove_urls(text)
        
        if self.config.remove_emails:
            text = self._remove_emails(text)
        
        if self.config.remove_mentions:
            text = self._remove_mentions(text)
        
        if self.config.remove_hashtags:
            text = self._remove_hashtags(text)
        
        if self.config.remove_latin_chars:
            text = self._remove_latin_chars(text)
        
        if self.config.remove_timestamps:
            text = self._remove_timestamps(text)
        
        if self.config.remove_diacritics:
            text = self._remove_diacritics(text)
        
        if self.config.normalize_alef:
            text = self._normalize_alef(text)
        
        if self.config.normalize_yeh:
            text = self._normalize_yeh(text)
        
        if self.config.normalize_teh:
            text = self._normalize_teh_marbuta(text)
        
        if self.config.normalize_punctuation:
            text = self._normalize_punctuation(text)
        
        if self.config.remove_repeated_punctuation:
            text = self._remove_repeated_punctuation(text)
        
        if self.config.normalize_numbers:
            text = self._normalize_numbers(text)
        
        if self.config.remove_numbers:
            text = self._remove_numbers(text)
        
        if self.config.remove_repeated_chars:
            text = self._remove_repeated_chars(text)
        
        if self.config.normalize_whitespace:
            text = self._normalize_whitespace(text)
        
        # Apply length constraints
        if len(text) < self.config.min_length:
            return ""
        
        if self.config.max_length and len(text) > self.config.max_length:
            text = text[:self.config.max_length]
        
        return text.strip()
    
    def _normalize_unicode(self, text: str) -> str:
        """Normalize Unicode representation."""
        return unicodedata.normalize(self.config.unicode_form, text)
    
    def _remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritics (tashkeel)."""
        if self.config.keep_shadda:
            # Remove all diacritics except shadda
            diacritics_to_remove = [d for d in self.DIACRITICS if d != '\u0651']
            for diacritic in diacritics_to_remove:
                text = text.replace(diacritic, '')
        else:
            for diacritic in self.DIACRITICS:
                text = text.replace(diacritic, '')
        return text
    
    def _normalize_alef(self, text: str) -> str:
        """Normalize all Alef variants to ا."""
        for variant in self.ALEF_VARIANTS:
            text = text.replace(variant, 'ا')
        return text
    
    def _normalize_yeh(self, text: str) -> str:
        """Normalize Yeh variants to ي."""
        text = text.replace('ى', 'ي')
        text = text.replace('ئ', 'ي')
        return text
    
    def _normalize_teh_marbuta(self, text: str) -> str:
        """Normalize Teh Marbuta ة to Heh ه."""
        return text.replace('ة', 'ه')
    
    def _normalize_punctuation(self, text: str) -> str:
        """Normalize punctuation marks."""
        for arabic_punct, latin_punct in self.PUNCTUATION_MAP.items():
            text = text.replace(arabic_punct, latin_punct)
        return text
    
    def _remove_repeated_punctuation(self, text: str) -> str:
        """Remove repeated punctuation (e.g., !!! -> !)."""
        return self.repeated_punct_pattern.sub(r'\1', text)
    
    def _normalize_numbers(self, text: str) -> str:
        """Convert Arabic-Indic numerals to Western numerals."""
        for arabic_num, western_num in self.ARABIC_INDIC_MAP.items():
            text = text.replace(arabic_num, western_num)
        return text
    
    def _remove_numbers(self, text: str) -> str:
        """Remove all numbers from text."""
        return re.sub(r'[0-9٠-٩۰-۹]+', '', text)
    
    def _remove_repeated_chars(self, text: str) -> str:
        """Remove repeated characters beyond max_char_repeat."""
        return self.repeated_char_pattern.sub(r'\1' * self.config.max_char_repeat, text)
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace to single spaces."""
        return self.whitespace_pattern.sub(' ', text)
    
    def _remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return self.url_pattern.sub('', text)
    
    def _remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return self.email_pattern.sub('', text)
    
    def _remove_mentions(self, text: str) -> str:
        """Remove @mentions from text."""
        return self.mention_pattern.sub('', text)
    
    def _remove_hashtags(self, text: str) -> str:
        """Remove #hashtags from text."""
        return self.hashtag_pattern.sub('', text)
    
    def _remove_latin_chars(self, text: str) -> str:
        """Remove English/Latin letters, keeping Arabic text and numbers."""
        # Remove only Latin letters (a-z, A-Z), keep numbers
        text = re.sub(r'[a-zA-Z]+', '', text)
        return text
    
    def _remove_timestamps(self, text: str) -> str:
        """Remove timestamps in various formats."""
        # Bracketed timestamps: [0:09:43.329000], [00:09:43], [HH:MM:SS.mmm]
        text = re.sub(r'\[\d{1,2}:\d{2}:\d{2}(?:\.\d+)?\]', '', text)
        # Time formats: HH:MM, HH:MM:SS, HH:MM AM/PM
        text = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?\b', '', text)
        # Date formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD.MM.YYYY
        text = re.sub(r'\b\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}\b', '', text)
        # ISO format: 2023-12-25T10:30:00
        text = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?', '', text)
        # Unix timestamps (10-13 digits)
        text = re.sub(r'\b\d{10,13}\b', '', text)
        return text
    
    def _normalize_sudanese_patterns(self, text: str) -> str:
        """Normalize Sudanese-specific dialect patterns."""
        for pattern, replacement in self.SUDANESE_PATTERNS.items():
            text = text.replace(pattern, replacement)
        return text
    
    def normalize_batch(self, texts: List[str], show_progress: bool = True) -> List[str]:
        """
        Normalize a batch of texts.
        
        Args:
            texts: List of text strings
            show_progress: Show progress bar (requires tqdm)
            
        Returns:
            List of normalized text strings
        """
        if show_progress:
            try:
                from tqdm import tqdm
                return [self.normalize(text) for text in tqdm(texts, desc="Normalizing")]
            except ImportError:
                logger.warning("tqdm not installed. Install with: pip install tqdm")
        
        return [self.normalize(text) for text in texts]
    
    def get_stats(self, text: str) -> Dict:
        """
        Get statistics about the text before and after normalization.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with statistics
        """
        normalized = self.normalize(text)
        
        return {
            'original_length': len(text),
            'normalized_length': len(normalized),
            'compression_ratio': 1 - (len(normalized) / len(text)) if len(text) > 0 else 0,
            'original_words': len(text.split()),
            'normalized_words': len(normalized.split()),
            'removed_chars': len(text) - len(normalized),
        }


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Default normalization
    print("=" * 60)
    print("Example 1: Default Configuration")
    print("=" * 60)
    
    normalizer = SudaneseNormalizer()
    
    test_text = """
    السَّلامُ عليكم ورحمة الله وبركاته!!!
    أنا من السودان 🇸🇩 وأحِب بلدي كتيييييير
    للتواصل: test@example.com
    موقعنا: https://example.com
    @username #السودان
    الأرقام: ١٢٣٤٥ و 67890
    """
    
    normalized = normalizer.normalize(test_text)
    print(f"Original:\n{test_text}")
    print(f"\nNormalized:\n{normalized}")
    
    stats = normalizer.get_stats(test_text)
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example 2: Custom configuration for preserving more features
    print("\n" + "=" * 60)
    print("Example 2: Custom Configuration (Preserve Hashtags)")
    print("=" * 60)
    
    custom_config = NormalizationConfig(
        remove_diacritics=True,
        keep_shadda=True,
        normalize_alef=True,
        remove_hashtags=False,  # Keep hashtags
        remove_urls=True,
        normalize_numbers=True,
    )
    
    custom_normalizer = SudaneseNormalizer(config=custom_config)
    custom_normalized = custom_normalizer.normalize(test_text)
    print(f"Custom Normalized:\n{custom_normalized}")
    
    # Example 3: Minimal normalization (for evaluation)
    print("\n" + "=" * 60)
    print("Example 3: Minimal Normalization")
    print("=" * 60)
    
    minimal_config = NormalizationConfig(
        remove_diacritics=False,
        normalize_alef=False,
        normalize_yeh=False,
        normalize_teh=False,
        normalize_whitespace=True,
        remove_urls=True,
    )
    
    minimal_normalizer = SudaneseNormalizer(config=minimal_config)
    minimal_normalized = minimal_normalizer.normalize(test_text)
    print(f"Minimal Normalized:\n{minimal_normalized}")
    
    print("\n" + "=" * 60)
    print("Normalizer ready for production use!")
    print("=" * 60)