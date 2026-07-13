
"""
Phreddy - A friendly FASTQ quality inspector.
This is the main file. It connects all the other files together.
Run with --help to see all the options.
"""
import argparse #argparse is built in python library allows user to give inputs through the command line 
from quality_calculator import analyze_fastq
from report_printer import print_report
from export_csv import export_csv
from export_json import export_json
from export_db import export_sqlite

#main function 
def main():
    parser = argparse.ArgumentParser(description="Phreddy - FASTQ quality inspector") 
    parser.add_argument('fastq', help='Path to the input FASTQ file (.fastq or .fastq.gz)') #User must proveide FASTQ filename without it , program cannot perform any analysis 
    parser.add_argument('--csv', metavar='FILE', help='Save report as a CSV file')
    parser.add_argument('--json', metavar='FILE', help='Save report as a JSON file')
    parser.add_argument('--db', metavar='FILE', help='Save report into an SQLite database')
    parser.add_argument('--no-display', action='store_true', help='Skip printing the report on screen')
    #The store_true action creates a Boolean flag . if the user specifies --no-display, the value becomes True and the report is not printed 
    args = parser.parse_args() #reads everything the user typed 

    print(f"🔬 Analyzing {args.fastq} ...") #this tells the user that the process is starting 

    try:
        reads, max_len, min_len, gc, n, per_base, all_scores = analyze_fastq(args.fastq)
    except FileNotFoundError:
        print(f"❌ File not found: {args.fastq}")
        return
    except ValueError as e:
        print(f"❌ Problem with the file: {e}")
        return

    overall = (sum(all_scores) / len(all_scores)) if all_scores else 0.0
    #the overall avergae is calculated only if quality scores exist; otherwise zero is returned to prevent dividion by zero 

    if not args.no_display:
        print_report(args.fastq, reads, max_len, gc, n, overall, per_base) #if false report is printed and if true the report is skipped 

    if args.csv:
        export_csv(args.csv, reads, max_len, min_len,gc, n, overall, per_base)
    if args.json:
        export_json(args.json, reads, max_len, min_len, gc, n, overall, per_base)
    if args.db:
        export_sqlite(args.db, reads, max_len, min_len, gc, n, overall, per_base)

        #export the type of report when required 

    print("\n✅ Phreddy analysis complete.\n")


if __name__ == "__main__":
    main() #calls the main function and begins the execution properly 

    #pyhton automatically creates  SPECIAL VARIABLE CALLED __name__
    #the if statement above ensures that the program starts only when this file is executed directly , not when it is imported as a module.
    """
    "The main.py file is the controller of the Phreddy project. It uses the argparse library to accept command-line arguments such as the input FASTQ file 
    and optional export formats like CSV, JSON, or SQLite. It then calls the analyze_fastq() function to perform all quality calculations.
    Error handling using try and except ensures that missing or invalid FASTQ files are handled gracefully. 
    After analysis, the program computes the overall average quality score and optionally displays the report or exports the results based on the user's
    command-line options. Finally, the if __name__ == '__main__' block ensures that the program starts only when the file is executed directly, 
    making the code modular and reusable."
    """