"""
Sudaverse Normalizer - Batch File Processor
==========================================

This script processes all text files in the raw-text folder,
normalizes them, and saves them to the normalized-text folder.

Features:
- Automatic folder scanning
- Progress tracking with ETA
- Real-time statistics and metrics
- Error handling and logging
- Support for multiple file encodings
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from normalizer_code import SudaneseNormalizer, NormalizationConfig


class BatchProcessor:
    """Process multiple text files with progress tracking."""
    
    def __init__(self, 
                 input_dir: str = "raw-text",
                 output_dir: str = "normalized-text",
                 config: NormalizationConfig = None):
        """
        Initialize the batch processor.
        
        Args:
            input_dir: Directory containing raw text files
            output_dir: Directory to save normalized files
            config: Normalization configuration
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.normalizer = SudaneseNormalizer(config or NormalizationConfig())
        
        # Statistics
        self.total_files = 0
        self.processed_files = 0
        self.failed_files = 0
        self.total_chars_input = 0
        self.total_chars_output = 0
        self.total_words_input = 0
        self.total_words_output = 0
        self.start_time = None
        self.errors: List[Tuple[str, str]] = []
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
    
    def find_text_files(self) -> List[Path]:
        """
        Find all text files in the input directory.
        
        Returns:
            List of Path objects for text files
        """
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")
        
        # Common text file extensions
        extensions = ['.txt', '.text', '.md', '.csv']
        files = []
        
        for ext in extensions:
            files.extend(self.input_dir.glob(f"*{ext}"))
        
        return sorted(files)
    
    def read_file(self, file_path: Path) -> str:
        """
        Read a text file with multiple encoding attempts.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File contents as string
        """
        encodings = ['utf-8', 'utf-8-sig', 'cp1256', 'iso-8859-6', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise Exception(f"Error reading file: {e}")
        
        raise UnicodeDecodeError(f"Could not decode file with any encoding: {file_path}")
    
    def write_file(self, file_path: Path, content: str):
        """
        Write content to a file.
        
        Args:
            file_path: Path to write to
            content: Content to write
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def format_size(self, chars: int) -> str:
        """Format character count into human-readable size."""
        if chars < 1024:
            return f"{chars} chars"
        elif chars < 1024 * 1024:
            return f"{chars / 1024:.1f} KB"
        else:
            return f"{chars / (1024 * 1024):.1f} MB"
    
    def print_progress(self, current: int, total: int, file_name: str, 
                      elapsed: float, current_stats: Dict):
        """
        Print progress bar and statistics.
        
        Args:
            current: Current file number
            total: Total number of files
            file_name: Current file name
            elapsed: Elapsed time in seconds
            current_stats: Statistics for current file
        """
        # Calculate progress
        progress = current / total
        bar_length = 40
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        percentage = progress * 100
        
        # Calculate ETA
        if current > 0:
            avg_time_per_file = elapsed / current
            remaining_files = total - current
            eta_seconds = avg_time_per_file * remaining_files
            eta_str = self.format_time(eta_seconds)
        else:
            eta_str = "Calculating..."
        
        # Calculate speeds
        chars_per_second = self.total_chars_input / elapsed if elapsed > 0 else 0
        
        # Clear line and print progress
        sys.stdout.write('\r' + ' ' * 120 + '\r')
        sys.stdout.flush()
        
        # Progress bar
        print(f"\r[{bar}] {percentage:.1f}% ({current}/{total})", end='')
        sys.stdout.flush()
        
        # File info
        print(f"\n📄 Processing: {file_name[:50]}", end='')
        sys.stdout.flush()
        
        # Stats
        print(f"\n⏱️  Elapsed: {self.format_time(elapsed)} | ETA: {eta_str}", end='')
        sys.stdout.flush()
        
        print(f"\n📊 Speed: {self.format_size(int(chars_per_second))}/s | "
              f"Words: {current_stats.get('original_words', 0)} → {current_stats.get('normalized_words', 0)}", end='')
        sys.stdout.flush()

        print(f"\n📈 Total: Input {self.format_size(self.total_chars_input)} → "
              f"Output {self.format_size(self.total_chars_output)} | "
              f"Words: {self.total_words_input} → {self.total_words_output}", end='')
    def process_file(self, file_path: Path) -> Dict:
        """
        Process a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with processing statistics
        """
        try:
            # Read file
            content = self.read_file(file_path)
            original_length = len(content)
            original_words = len(content.split())
            
            # Normalize
            normalized = self.normalizer.normalize(content)
            normalized_length = len(normalized)
            normalized_words = len(normalized.split())
            
            # Save to output
            output_path = self.output_dir / file_path.name
            self.write_file(output_path, normalized)
            
            # Update totals
            self.total_chars_input += original_length
            self.total_chars_output += normalized_length
            self.total_words_input += original_words
            self.total_words_output += normalized_words
            
            # Calculate stats
            compression = 1 - (normalized_length / original_length) if original_length > 0 else 0
            
            return {
                'success': True,
                'original_length': original_length,
                'normalized_length': normalized_length,
                'original_words': original_words,
                'normalized_words': normalized_words,
                'compression_ratio': compression,
                'output_path': output_path
            }
            
        except Exception as e:
            self.errors.append((str(file_path), str(e)))
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_all(self):
        """Process all files in the input directory."""
        print("=" * 80)
        print("🇸🇩 SUDAVERSE NORMALIZER - BATCH PROCESSOR 🇸🇩")
        print("=" * 80)
        print()
        
        # Find files
        print(f"📂 Scanning directory: {self.input_dir.absolute()}")
        files = self.find_text_files()
        self.total_files = len(files)
        
        if self.total_files == 0:
            print(f"⚠️  No text files found in {self.input_dir}")
            print(f"💡 Place your .txt files in the '{self.input_dir}' folder and try again.")
            return
        
        print(f"✅ Found {self.total_files} text file(s)")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print()
        print("🚀 Starting normalization...")
        print()
        
        # Start processing
        self.start_time = time.time()
        
        for idx, file_path in enumerate(files, 1):
            result = self.process_file(file_path)
            
            if result['success']:
                self.processed_files += 1
            else:
                self.failed_files += 1
            
            # Update progress
            elapsed = time.time() - self.start_time
            self.print_progress(idx, self.total_files, file_path.name, elapsed, result)
        
        # Final summary
        self.print_summary()
    
    def print_summary(self):
        """Print final summary of the batch processing."""
        print("\n\n")
        print("=" * 80)
        print("📊 PROCESSING SUMMARY")
        print("=" * 80)
        print()
        
        # Time stats
        total_time = time.time() - self.start_time
        print(f"⏱️  Total Time: {self.format_time(total_time)}")
        print(f"⚡ Average Speed: {self.format_size(int(self.total_chars_input / total_time))}/s")
        print()
        
        # File stats
        print(f"📄 Files Processed: {self.processed_files}/{self.total_files}")
        if self.failed_files > 0:
            print(f"❌ Failed Files: {self.failed_files}")
        print()
        
        # Size stats
        print(f"📥 Input Size: {self.format_size(self.total_chars_input)}")
        print(f"📤 Output Size: {self.format_size(self.total_chars_output)}")
        
        if self.total_chars_input > 0:
            overall_compression = 1 - (self.total_chars_output / self.total_chars_input)
            reduction = self.total_chars_input - self.total_chars_output
            print(f"📉 Size Reduction: {self.format_size(reduction)} ({overall_compression:.1%})")
        print()
        
        # Word stats
        print(f"📝 Word Count:")
        print(f"   Before: {self.total_words_input:,} words")
        print(f"   After: {self.total_words_output:,} words")
        if self.total_words_input > 0:
            word_reduction = self.total_words_input - self.total_words_output
            word_reduction_pct = (word_reduction / self.total_words_input) * 100
            print(f"   Removed: {word_reduction:,} words ({word_reduction_pct:.1f}%)")
        print()
        
        # Errors
        if self.errors:
            print("⚠️  ERRORS:")
            for file_path, error in self.errors:
                print(f"   • {file_path}: {error}")
            print()
        
        # Output location
        print(f"✅ Normalized files saved to: {self.output_dir.absolute()}")
        print()
        print("=" * 80)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch process Sudanese Arabic text files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process files with default settings
  python batch_processor.py
  
  # Specify custom input/output directories
  python batch_processor.py -i my_texts -o my_output
  
  # Remove English words, keep/convert numbers, remove timestamps
  python batch_processor.py --remove-latin
  
  # Use custom configuration
  python batch_processor.py --no-diacritics --keep-hashtags
        """
    )
    
    parser.add_argument('-i', '--input', default='raw-text',
                       help='Input directory containing text files (default: raw-text)')
    parser.add_argument('-o', '--output', default='normalized-text',
                       help='Output directory for normalized files (default: normalized-text)')
    parser.add_argument('--no-diacritics', action='store_true',
                       help='Remove Arabic diacritics')
    parser.add_argument('--keep-hashtags', action='store_true',
                       help='Keep hashtags in text')
    parser.add_argument('--remove-latin', action='store_true',
                       help='Remove English/Latin words (keeps numbers, converts Arabic numerals)')
    parser.add_argument('--normalize-numbers', action='store_true',
                       help='Convert Arabic-Indic numerals to Western')
    parser.add_argument('--max-repeat', type=int, default=2,
                       help='Maximum character repetition (default: 2)')
    parser.add_argument('--keep-html', action='store_true',
                       help='Keep HTML/XML tags (removed by default)')
    parser.add_argument('--keep-special-chars', action='store_true',
                       help='Keep unrecognized/special characters (removed by default)')
    parser.add_argument('--keep-decorative-lines', action='store_true',
                       help='Keep decorative lines made of tatweel/kashida characters (removed by default)')
    parser.add_argument('--preserve-arabic-punct', action='store_true',
                       help='Preserve Arabic punctuation when removing special characters')
    
    args = parser.parse_args()
    
    # Create configuration
    config = NormalizationConfig(
        remove_diacritics=args.no_diacritics,
        remove_hashtags=not args.keep_hashtags,
        remove_latin_chars=args.remove_latin,
        normalize_numbers=args.normalize_numbers or args.remove_latin,  # Auto-enable with --remove-latin
        remove_timestamps=args.remove_latin,  # Auto-enable with --remove-latin
        max_char_repeat=args.max_repeat,
        remove_html_tags=not args.keep_html,
        remove_special_chars=not args.keep_special_chars,
        remove_decorative_lines=not args.keep_decorative_lines,
        preserve_arabic_punctuation=args.preserve_arabic_punct
    )
    
    # Create processor
    processor = BatchProcessor(
        input_dir=args.input,
        output_dir=args.output,
        config=config
    )
    
    try:
        processor.process_all()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
