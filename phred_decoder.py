"""
Phreddy Phred Decoder
-----------------------
This file's ONLY job is turning quality symbols into numbers.
This module converts FASTQ quality symbols into numecical phred scores.
The function recieves a quality strigs and processes it one character at a time.
Using the ord() function, it converts each character to its ASCII value 
and then subtracts the offset (33) to get the actual phred quality score.
Each score is stored in a list and after all character is processed, 
the complete ;ist of phred scores is returned.
"""

def decode_quality(q_line, offset=33):
    """
    Turns a quality string like '!!!IIIF' into a list of numbers.
    Each symbol = one number. Formula: number = ASCII value - offset.
    why 33?

FASTQ files don't store quality as numbers.
Instead, they store ASCII characters.
To recover the real quality score we use:
Phred Score=ASCII value−33
33 is the standard encoding used by Illumina and Sanger FASTQ files
    """
    scores = [] 
    """
    i first create an empty list called scores that will store the decoded
    phred quality values.
    """
    for char in q_line:
    #the for loop processes one character at a time beacuse each character corresponds to one dna base 
        score = ord(char) - offset 
        """
          FASTQ files stores quality vales as ASCII charcayters reather then numbers.
          The ord() function converts each character to its ASCII value,
          and subtracting the offset (33) gives he actual phred quality score.
        """

        scores.append(score)
        #Each decoded phred quality score is added to the scores list usning the append()method.
    return scores
#after every character is processed, complete list is returned.