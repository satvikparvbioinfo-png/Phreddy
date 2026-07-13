# analysis.py
"""
This program combines quality decoding and FASTQ analysis into one module. 
It first converts FASTQ quality symbols into numerical Phred scores using the decode_quality() function.
The analyze_fastq() function then reads the FASTQ file record by record, counts the total reads, determines the maximum read length, 
calculates GC and N content, and groups quality scores by base position. After processing the entire file, it computes per-base average, 
minimum, and maximum quality scores and returns all the calculated statistics. The design uses dictionaries and lists to efficiently organize sequencing
quality data while processing the file one read at a time
"""
from utils import open_fastq
#I imported the open_fastq() function from the utilities module so that this program can read both normal and compressed FASTQ files 

def decode_quality(q_line, offset=33):
    """Turn quality symbols like 'E?;@' into numbers."""
    scores = [] #Empty list 
    for char in q_line.strip(): #When reading line from a file, python includes then newline chracter so we use strip()
        score = ord(char) - offset #ord() convert character into number
        scores.append(score) # add decoded score to the list 
    return scores #return the complete list of the quality scores 

def analyze_fastq(filename):

    """Read a FASTQ file and return all quality stats."""
    total_reads = 0
    max_len = 0
    gc_count = 0
    n_count = 0
    total_bases = 0
    position_scores = {}      # key: position (0‑based), value: list of scores
    all_scores = []

    with open_fastq(filename) as f:
        #uses the helper function to open the fastq file 
        while True: #infinite loop 
            header = f.readline().strip() #reads the header line 
            if header == '': #empty string returned 
                break #file has ended the loop stops 
            seq = f.readline().strip() #read  the DNA sequence 
            f.readline()               # skip '+' line
            qual = f.readline().strip() #reads the quality symbol

            total_reads += 1
            read_len = len(seq)
            if read_len > max_len:
                max_len = read_len

            # decode quality and store per position
            scores = decode_quality(qual) #convert the quality character to the numerical phred scores 
            for i, sc in enumerate(scores): #it provides position and quality scores 
                if i not in position_scores:
                    position_scores[i] = [] #if this position has not seen before ccreate an empty list for that position 
                position_scores[i].append(sc)
                all_scores.append(sc) #above line of code add score to the base position and this line stores every quality score 

            # count bases
            gc_count += seq.count('G') + seq.count('C')
            n_count += seq.count('N')
            total_bases += read_len #Count G,C and N bases and adds the current read length to the total

    #CALCULATE GC AND N PERCENTAGE
    gc_content = (gc_count / total_bases * 100) if total_bases > 0 else 0.0
    n_content = (n_count / total_bases * 100) if total_bases > 0 else 0.0

    # per‑base averages
    per_base = {}
    #WILL store the statistics for each base position 
    for pos, scores_list in position_scores.items(): #processes every position stored in the dictionary 
        avg = sum(scores_list) / len(scores_list) 
        min_s = min(scores_list)
        max_s = max(scores_list)
        per_base[pos + 1] = (avg, min_s, max_s)   # 1‑based because python starts counting at zero , adds the statistics to the dictionary 

    return total_reads, max_len, gc_content, n_content, per_base, all_scores
 #return all calculated statistics to the calling program 