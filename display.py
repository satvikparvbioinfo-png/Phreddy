"""
This module is responsible for dispalying the fina; FASTQ quality report.
It first determines the appropriate colour for each aberage qyuality score using thr colour_for_quality()
funtion. the print report function then prints thr filename, total reads , gc content , n content and overall average quality 
This module focuses only on presenting the results and does not perform any calculatins itself.
"""
from utils import GREEN, YELLOW, RED, RESET
"""
I imported the colour constants from the utilities module so they can be reused throughout 
the project.
"""
#This below function decides which colour should represent a quality score 
def color_for_quality(avg_q):
    if avg_q >= 28:
        return GREEN
    elif avg_q >= 20:
        return YELLOW
    else:
        return RED
    
#MAIN function 
def print_report(filename, total_reads, max_len, gc, n, overall_avg, per_base):
    #thid function prints complete FASTQ quality report , it recievers all the calculated statistics from the analysis function.
    print("\n" + "=" * 60) #first seperator 
    print(f"  Phreddy Quality Report: {filename}") #python replaces filename with actual name 
    print("=" * 60)
    print(f"  Total reads       : {total_reads}")
    print(f"  Max read length   : {max_len} bp")
    print(f"  GC content        : {gc:.2f}%")
    print(f"  N content         : {n:.2f}%")
    print(f"  Overall avg qual  : {overall_avg:.2f}")

    print("\n  Per-base average quality:") #prints the heading of the table 
    print("  " + "-" * 56) #Second seperator 
    print(f"  {'Pos':<5} {'Avg':<8} {'Min':<8} {'Max':<8} Status") 
    #the alignment specifirer ensures that all columns in report line up properly making the output easier to read.
    print("  " + "-" * 56)

    for pos in sorted(per_base.keys()):
        #to sort the dictionarues in numerical order instead of a random order we use sorted()
        avg, min_q, max_q = per_base[pos] #Tuple Unpacking 
        colour = color_for_quality(avg) #calls the earlier function 
        if avg >= 20:
            status = f"{colour}PASS{RESET}"
        else:
            status = f"{RED}FAIL{RESET}"
        print(f"  {pos:<5} {avg:<8.2f} {min_q:<8} {max_q:<8} {status}") #each column is aligned using formatting specifiers

    print("  " + "-" * 56)
    #prints the closing line of the table 