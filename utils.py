"""
Phreddy Utilities
-----------------
This file has small helper things that other files need:
1. A function to open FASTQ files (normal or zipped)
2. Colour codes to make text green/yellow/red in the terminal
"""
import gzip

# These are special codes that change text colour in the terminal
GREEN  = '\033[92m'   # good quality (score 28 or higher)
YELLOW = '\033[93m'   # okay quality (score 20 to 27)
RED    = '\033[91m'   # bad quality (score below 20)
RESET  = '\033[0m'    # this brings the colour back to normal


def open_fastq(filename):
    """
    Opens a FASTQ file so we can read it.
    Works whether the file is zipped (.gz) or not.
    """
    try: #python attempts to open the file 
        if filename.endswith('.gz'):#checks weather the filename exists with .gz
            return gzip.open(filename, 'rt')  # 'rt' = read as text #open compresed fastq file in read text mode 
        else:
            return open(filename, 'r')#open normal fastq file
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file: {filename}")