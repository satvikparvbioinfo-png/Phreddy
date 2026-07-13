"""
Phreddy Quality Calculator
-----------------------------
This file's ONLY job is maths: counting GC content, N content,
and working out averages per position. It uses fastq_parser.py
to get the reads and phred_decoder.py to turn quality into numbers.
"""
from fastq_parser import read_records
from phred_decoder import decode_quality
"""
I imported read_records to read equencing records and decodw_quality to convert quality
charaters into phred scores. this modular design avoid code duplication.
"""


def analyze_fastq(filename):
    """
    Goes through every read in the file and works out:
      - total_reads : how many reads there are
      - max_len     : the longest read length
      - min_len     : the shortest read length
      - gc_percent  : % of bases that are G or C
      - n_percent   : % of bases that are N (unknown base)
      - per_base    : average/min/max quality at each position
      - all_scores  : every single quality score (used for overall average)
    """
    total_reads = 0
    max_len = 0
    min_len = None   # we don't know the minimum yet, so start empty
    gc_count = 0
    n_count = 0
    total_bases = 0

    position_scores = {} #empty dictionary to store quality scores for each position
      # position number -> list of scores seen at that position
    all_scores = [] #Empty list to store all quality scores across all reads
    #[40,39,38,40,37...]

    for seq, qual in read_records(filename):
        total_reads += 1 #Count Reads 
        read_len = len(seq) #Read Lengths 

        if read_len > max_len: #Longest Read 
            max_len = read_len

        if min_len is None or read_len < min_len: #Shortest read
            min_len = read_len

        scores = decode_quality(qual)
        """
        EXAMPLE:
        Quality
        III!!
        becomes
        [40,40,40,0,0]
        """

        for position, score in enumerate(scores):
        #without enumerate(), you'd only get the score not its position

            if position not in position_scores: #Check Dictionry 
                position_scores[position] = []
            position_scores[position].append(score) #Append Score
            all_scores.append(score) #Save Overall scores

        gc_count += seq.count('G') + seq.count('C') #Count GC bases
        n_count  += seq.count('N') #Count N bases
        total_bases += read_len #count total bases 

    gc_percent = (gc_count / total_bases * 100) if total_bases > 0 else 0.0 #GC percentage 
    n_percent  = (n_count  / total_bases * 100) if total_bases > 0 else 0.0 #N percentage

    per_base = {}
    
    """
Create New Dictionary 
This dictionary will store
Average quality
Minimum quality
Maximum quality
for every base position.
    """
    for position, score_list in position_scores.items():
        avg = sum(score_list) / len(score_list)
        per_base[position + 1] = (avg, min(score_list), max(score_list))  # +1 so positions start at 1

    if min_len is None:
        min_len = 0  # no reads were found at all

    return total_reads, max_len, min_len, gc_percent, n_percent, per_base, all_scores
#This sends all calculated results back to the main program.