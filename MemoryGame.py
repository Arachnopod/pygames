# implementation of card game - Memory
# Author: John Liu
# Date: 2014-May-03

import simplegui
import random
cardlist = []
exposed = []
state = 0
prev_1 = -1
prev_2 = 0
count = 0

# helper function to initialize globals
def new_game():
    global cardlist, exposed, count, state
    cardlist = range(8) + range(8)
    random.shuffle(cardlist)
    exposed = [False for n in range(16)]
    count = 0
    state = 0
    label.set_text("Turns = "+str(count))
    
     
# define event handlers
def mouseclick(pos):
    global exposed, state, prev_1, prev_2, count
    cardindex = pos[0] //50
    if not exposed[cardindex]:
        exposed[cardindex] = True
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
            count += 1
            label.set_text("Turns = "+str(count))
        else:
            state = 1
            if cardlist[prev_2] != cardlist[prev_1]:
                exposed[prev_2] = False
                exposed[prev_1] = False
        prev_2 = prev_1
        prev_1 = cardindex

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cardlist, exposed
    for i in range(len(cardlist)):
        if exposed[i]:
            canvas.draw_text(str(cardlist[i]), [i*50, 80] , 92, "White")
        else:
            points = [[i*50,1],[i*50,99],[i*50+50,99],[i*50+50,1]]
            canvas.draw_polygon(points, 2, "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = "+str(count))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric