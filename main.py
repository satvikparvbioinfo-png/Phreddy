import gzip
# ANSI colour codes for terminal output
GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m' #[93,92,91] are the escape codes for yellow, green, and red text colors in the terminal
RESET  = '\033[0m' #escape character to reset the color back to default
from collections import defaultdict
def open_fastq(filename):
    """
    open a FastQ file, gzipped or plain text."""
    if filename.endswith(".gz"):
        return gzip.open(filename, "rt")  # open gzipped file in text mode
    else:
        return open(filename, "r")  # open plain text file

def decode_quality(q_line, offset=33):
    """
    Convert a FASTQ quality ASCII line into a list of phred quality scores.
    standard Sanger/ILLUMINA encoding uses an offset of 33.
    """
    scores =[]#empty list to hold the quality numbers 
    for char in q_line.strip():#strip()removes trailing newline 
        score=ord(char)-offset#convert character to number 
        scores.append(score)#add to the list 
    return scores
def analyze_fastq(filename):
    """
    analyse a Fastq file and returns the read count and maximum read length
    """
    total_reads=0
    max_read_length=0
    gc_count=0#total number of G and C bases         
    n_count=0#TOTAL NUMBER OF N BASES
    total_bases=0#total bases procesed 
    position_counts=defaultdict(list)#key = position(index), value =list of quality scores
    all_scores = []#store every quality score
    #open the fastq file 
    with open_fastq(filename)as file:
        while True:
            #read the four lines of one fastq record
            header=file.readline().strip()

            sequence=file.readline().strip()
            plus=file.readline().strip()
            quality=file.readline().strip()

            #if there is no header we reached the end of the file 
            if header=="":
                break
            #count this read 
            total_reads+=1
            #find the length of the sequence 
            read_length =len(sequence)

            #update the maximum read elngth if needed 
            if read_length > max_read_length:
                max_read_length=read_length
            
                #deocde the wuality line 
            scores = decode_quality(quality)
                #stores scores per position (0-bases index)
            for i, score in enumerate(scores):
                position_counts[i].append(score)
                all_scores.append(score)

                    #count GC AND N bases in the sequence 
            gc_count += sequence.count("G") + sequence.count("C")
            n_count += sequence.count("N")
            total_bases += read_length
                        # Compute GC and N percentages
    gc_content = (gc_count / total_bases * 100) if total_bases > 0 else 0.0
    n_content = (n_count / total_bases * 100) if total_bases > 0 else 0.0

    # Compute per‑base average, min, max
    per_base_stats = {}
    for pos, scores_list in position_counts.items():
        avg = sum(scores_list) / len(scores_list)
        min_s = min(scores_list)
        max_s = max(scores_list)
        per_base_stats[pos + 1] = (avg, min_s, max_s)   # +1 to make it 1‑based for human readability
    return total_reads, max_read_length, gc_content, n_content, per_base_stats, all_scores
def color_for_quality(avg_q):
    """Return ANSI colour code based on average quality score."""
    if avg_q >= 28:
        return GREEN
    elif avg_q >= 20:
        return YELLOW
    else:
        return RED
def print_report(filename, total_reads, max_len, gc, n, overall_avg, per_base):
    """Print a formatted quality report with colour coding."""
    # Header
    print("\n" + "=" * 60)
    print(f"  Phreddy Quality Report: {filename}")
    print("=" * 60)
    print(f"  Total reads       : {total_reads}")
    print(f"  Max read length   : {max_len} bp")
    print(f"  GC content        : {gc:.2f}%")
    print(f"  N content         : {n:.2f}%")
    print(f"  Overall avg qual  : {overall_avg:.2f}")
    print("\n  Per-base average quality:")
    print("  " + "-" * 56)
    print(f"  {'Pos':<5} {'Avg':<8} {'Min':<8} {'Max':<8} Status")
    print("  " + "-" * 56)

    # Per‑base rows
    for pos in sorted(per_base.keys()):
        avg, min_q, max_q = per_base[pos]
        colour = color_for_quality(avg)
        status = f"{colour}PASS{RESET}" if avg >= 20 else f"{RED}FAIL{RESET}"
        print(f"  {pos:<5} {avg:<8.2f} {min_q:<8} {max_q:<8} {status}")

    # Footer
    print("  " + "-" * 56)  
def main():
    print("Welcome to Phreddy!")

    filename = "sample_data/sample.fastq"

    reads, max_len, gc, n, per_base, all_scores = analyze_fastq(filename)


    overall_avg = sum(all_scores) / len(all_scores) if all_scores else 0.0
    print_report(filename, reads, max_len, gc, n, overall_avg, per_base)

    print(f"\nFile: {filename}")
    print(f"Total reads: {reads}")
    print(f"Max read length: {max_len}")
    print(f"GC content: {gc:.2f}%")
    print(f"N content: {n:.2f}%")
    print(f"Overall avg quality: {overall_avg:.2f}")

    print("\nPer-base quality (1-indexed):")
    for pos in sorted(per_base.keys()):
        avg, min_q, max_q = per_base[pos]
        print(f"  Pos {pos:2d}: avg={avg:.2f}, min={min_q}, max={max_q}")


if __name__ == "__main__": #this line checks if the script is being run directly or imported as a module
    #quick test of decode_quaity 
    test_qual = "E?;@"  #a fake quality line 
    result = decode_quality(test_qual)
    print("Quality line:", test_qual)
    print("Decoded scores:", result)
    #expected output: [36,30,26,31]
    main() #calls the main function to execute the code within it
