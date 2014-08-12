# Rock-paper-scissors-lizard-Spock
# Author: John Liu
# Date: 2014-Mar-29

import math
import random

"""
 0 - rock
 1 - Spock
 2 - paper
 3 - lizard
 4 - scissors
"""

def name_to_number(name):
    """
    str -> int
    
    convert name to number
    
    >>> name_to_number("Spock")
    1
    """    
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    else:
        return 4


def number_to_name(number):
    """
    int -> str
    
    convert number to name
    
    >>> number_to_name(2)
    paper
    """
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    else:
        return "scissors"
    

def rpsls(player_choice): 
    """
    str -> None
    
    Play one round of Rock-Paper_Scissors-Lizard-Spock vs Computer
    Argument: Player Choice
    
    >>> rpsls("Spock")
    
    Player chooses Spock
    Computer chooses Spock
    Player and computer tie!
    >>> rpsls("paper")

    Player chooses paper
    Computer chooses scissors
    Computer wins!
    """    
    
    # print a blank line to separate consecutive games
    print
    
    # print out the message for the player's choice
    print "Player chooses",player_choice
    
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    computer_number = random.randrange(5)
    
    # convert comp_number to comp_choice using the function number_to_name()
    computer_choice = number_to_name(computer_number)
    
    # print out the message for computer's choice
    print "Computer chooses",computer_choice
    
    # compute difference of comp_number and player_number modulo five
    count = (player_number - computer_number) % 5
    
    # use if/elif/else to determine winner, print winner message
    if (count == 1 or count == 2):
        print "Player wins!"
    elif (count == 3 or count == 4):
        print "Computer wins!"
    else:
        print "Player and computer tie!"

    
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


