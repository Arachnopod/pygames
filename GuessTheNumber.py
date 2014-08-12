# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# Author: John Liu
# Date: 2014-Apr-12

import simplegui, random, math

# initialize global variables used in your code

right_answer = 0
max_choice = 100
guesses_left = 7

# helper function to start and restart the game
def new_game():
    global right_answer, guesses_left
    right_answer = random.randrange(0,max_choice)
    guesses_left = int(math.ceil(math.log(max_choice,2)))
    print "I'm thinking of a number between 0 and",max_choice
    print

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global max_choice, guesses_left
    max_choice = 100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global max_choice, guesses_left
    max_choice = 1000
    new_game()

def input_guess(guess):
    # main game logic goes here	
    global guesses_left
    guesses_left = guesses_left - 1
    player_guess = int(guess)
    print "Player guesses",player_guess
    if player_guess < right_answer:
        print "Sorry. It's Higher."
    elif player_guess > right_answer:
        print "Sorry. It's Lower."
    else:
        print "Correct!"
        print "You win!!!"
        print
        new_game()
        return
    if guesses_left > 0:
        print "You have",guesses_left,"guesses left."
        print
    else:
        print "You ran out of guesses!"
        print "You lose."
        print
        new_game()

def exit_game():
    print
    print "Thank you for playing."
    print
    exit()
    
# create frame

f = simplegui.create_frame("Guess a Number",200,200)

# register event handlers for control elements

f.add_button("Range: 0 - 100",range100)
f.add_button("Range: 0 - 1000",range1000)
f.add_input("Guess",input_guess,50)
f.add_button("Exit Game",exit_game)


# call new_game and start frame

new_game()
f.start()

# always remember to check your completed program against the grading rubric
