"""
Phreddy FASTQ Parser
---------------------
This file's ONLY job is to read a FASTQ file and hand back
one record (read) at a time. It does not do any maths.
"""
from utils import open_fastq


def read_records(filename):
    """
    the read_records function accepts the FASTQ filename 
    as input and processes the file one seq record at a time.
    
    Goes through a FASTQ file 4 lines at a time (that's how FASTQ works):
        Line 1: header (starts with @)
        Line 2: the DNA sequence
        Line 3: a '+' line (we don't need this)
        Line 4: the quality string

    Gives back one record at a time using 'yield' instead of loading
    the whole file into memory at once.
    """
    with open_fastq(filename) as fh:
       
        """
        This line does several things , first is open either FASTQ
        or FASTQ.GZ file using the open_fastq function from utils.py 
        It returns a file object that object is stroed inside fh variable 
        which stands for file handle (simple pyhtons way of referring to an opened file)

        TO automatically close the file after we are done with it,
        we use the with statement which ensures that the file is closed.  
        """


        while True: #infinite loop to read the file until the end
            header = fh.readline().strip()
            """
        The readline() method reads a single line from the file,
        and the strip() method removes any leading or trailing whitespace
        (including newline characters) from that line.

            """
            if header == '': #reached the end of the file, readline() returns an empty string when it reaches the end of the file
                break  # end of file

            seq  = fh.readline().strip() #for SEQ line 
            fh.readline()                  # skip the '+' line
            qual = fh.readline().strip() #for quality line returns a qualit string

            if not seq or not qual:
                break  
            """
            If either the sequence or quality line is empty, 
            we break out of the loop, instead of crashing the parser stops.
            """

            if len(seq) != len(qual):
                raise ValueError(f"Broken record: sequence and quality lengths don't match for {header}")
            """
            A valid FASTQ record must contain exactly one quality
            score for every DNA base.If the sequence length and quality
            length differ,the file is considered corrupted, and the 
            parser raises a ValueError
            
            """


            yield seq, qual
            """
            Instead of loading the entire FASTQ file into memory,
            I use yield to create a generator.
            It returns one sequencing record at a time,
            pauses the function, and resumes when the next record is
            requested. This makes the parser efficient even for very large sequencing datasets.
            """