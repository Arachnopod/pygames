# "Stopwatch: The Game"
# Author: John Liu
# Date: 2014-Apr-19

import simplegui, time

# define global variables

count_time = 0L
num_stopped = 0
num_right = 0
running = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenths = t % 10
    secs = t/10L % 60
    minutes = t/600L
    return '%(min)01d:%(sec)02d.%(ten)1d' % { "min":minutes, "sec":secs, "ten":tenths}
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global running
    t.start()
    running = True
    
def stop():
    global num_stopped, running, num_right
    t.stop()
    if running:
        num_stopped += 1
        running = False
        if(count_time % 10 == 0):
            num_right += 1
    
def reset():
    global count_time, num_stopped, num_right
    t.stop()
    count_time = 0L
    num_stopped = 0
    num_right = 0

    
# define event handler for timer with 0.1 sec interval

def timer():
    global count_time
    count_time += 1
    print count_time

# define draw handler

def draw(canvas):
    global count_time
    canvas.draw_text(format(count_time), [90,110], 48, "White")
    canvas.draw_text(str(num_stopped)+"/"+str(num_right), [250,30], 24, "Red")


# create frame

f = simplegui.create_frame("Stopwatch",300,200)
f.set_draw_handler(draw)

t = simplegui.create_timer(100, timer)

# register event handlers

f.add_button("Start",start)
f.add_button("Stop",stop)
f.add_button("Reset",reset)

# start frame

f.start()

# Please remember to review the grading rubric
