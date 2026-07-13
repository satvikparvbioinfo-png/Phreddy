"""
Phreddy Report Printer
--------------------------
This file's ONLY job is printing the report on screen.
It uses color_rules.py to know what colour to use, but doesn't
decide the colours itself.
"""
from utils import RESET
"""I imported the RESET colour code so that after printing coloured 
text, the terminal returns to its default colour.
"""
from colour_rules import color_for_quality, status_for_quality
"""I imported the colour functions so this module can display the correct colours ad status labels without 
containing the decision logic itself 
"""


def print_report(filename, total, max_len, gc, n, overall, per_base):
    """Prints the full quality report to the terminal, it receives all the 
    statistics calculated earlier 
    """
    print("\n" + "=" * 55)
    """=+55 means repeat = 55 times 
    this creates a separator line to make the output easier to read
    """
    print(f"  Phreddy Quality Report: {filename}")
    #An f-string is used to insert the filename dynamiclly into the report title
    print("=" * 55) #Another Separator
    print(f"  Total reads      : {total}")
    print(f"  Max read length  : {max_len} bp")
    print(f"  GC content       : {gc:.2f}%") #shows two decimal places
    print(f"  N content        : {n:.2f}%")
    print(f"  Overall avg qual : {overall:.2f}")#Displays overall Phred scores 

    if not per_base:
        print("\n  No reads were found in this file.")
        return
    """This checks wheather the dictionary conatains any quality statistics, an emoty dictionary means 
       no sequencing reads were found.
    """


    print("\n  Per-base average quality:") #prints section title 
    print("  " + "-" * 51) #seperator 
    print(f"  {'Pos':<5} {'Avg':<8} {'Min':<8} {'Max':<8} Status")
    print("  " + "-" * 51)
    """
    Alignment specifiers such as <5 and<8 ensures that all table columns line 
    up neatly regardless of the numbers of digits.
    """

    for pos in sorted(per_base.keys()):
        #positions are sorted before printing so the report is always n biological order.
        avg, min_q, max_q = per_base[pos] #Tuple unpacking 
        colour = color_for_quality(avg)
        coloured_avg = f"{colour}{avg:<8.2f}{RESET}"
        status = status_for_quality(avg)
        print(f"  {pos:<5} {coloured_avg} {min_q:<8} {max_q:<8} {status}")

    print("  " + "-" * 51)
    #prints the bottom border of the table 
    """
    The print_report() function is responsible for displaying the ananlysis results.
    It prints the formatted report containng teh filename, totak reads, maximumm read
    length , gc content , n content and overall average quality. if no sequencung reads are present , 
    it prints an appropriate message and exits.
    This keeps display logic seperate from the analuysis logic, making the program modular and easier to 
    maintain. 
    """
