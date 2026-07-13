"""
Phreddy CSV Exporter
----------------------
This file's ONLY job is saving results as a CSV file
(so it can be opened in Excel or Google Sheets).
This module is responsible for exporting the analysis results into a csv file, which can be opened in spreaadsheet
applications such as microsoft excel or google sheeets.
"""

def export_csv(outfile, total, max_len, gc, n, overall, per_base):
    """This function recieves all the calculated statistics and saves them into a CSV file."""
    with open(outfile, 'w', newline='') as f: #opens the file , w means write mode , newline prevents python from insterting extra blank line into csv file.
        f.write("Metric,Value\n")
        f.write(f"Total Reads,{total}\n")
        f.write(f"Max Read Length,{max_len}\n")
        f.write(f"GC Content,{gc:.2f}\n")
        f.write(f"N Content,{n:.2f}\n")
        f.write(f"Overall Avg Quality,{overall:.2f}\n")
        f.write("\n")

        f.write("Position,Avg,Min,Max\n")
        for pos in sorted(per_base.keys()):
            avg, min_s, max_s = per_base[pos]
            f.write(f"{pos},{avg:.2f},{min_s},{max_s}\n")

    print(f"  📄 CSV report saved to {outfile}")
    #After writing all the program displays a confieramtion message showing the name of the saved csv file 