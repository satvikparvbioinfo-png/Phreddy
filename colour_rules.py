"""
Phreddy Colour Rules
-----------------------
This file's ONLY job is deciding which colour and status word
(PASS / WARN / FAIL) matches a given quality score.
It does NOT print anything itself.
"""
from utils import GREEN, YELLOW, RED, RESET
"""
I imported the colour constants from the utilities module so they can
reused throughout the project without redefining them
"""
def color_for_quality(avg_q):
    """Picks a colour based on how good the average quality is."""
    if avg_q >= 28:
    #If the average quality score is 28 or higher, the sequencing data is considered high quality.
        return GREEN
    #if the quality is high, the function returns the green colour code.
    elif avg_q >= 20: #means else if, python only checks this if the first condition was False.
        return YELLOW #This function returns yellow colour then stops 
    #if the quality score is below 20, the program considers it poor quality 
    else: #returns red colour 
        return RED


def status_for_quality(avg_q):
    """Picks the word PASS / WARN / FAIL, already coloured."""
    colour = color_for_quality(avg_q)
    #this function converts an average quality score into a coloured status lable such as PASS , WARN or FAIL.
    if colour == GREEN:
        text = "PASS" #THE program checks whether the returned colour is green 
    elif colour == YELLOW:
        text = "WARN"
    else:
        text = "FAIL"
    """ 
    the function combines the colour code, the status word, and reset code 
    into one formatted string. This allows the terminal to display PASS, 
    WARN or FAIL in different colours while ensuring later text returns to the default colour
    """
    return f"{colour}{text}{RESET}"