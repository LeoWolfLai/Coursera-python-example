# implementation of card game - Memory

import simplegui
import random

list_1=range(8)
list_2=list_1*2
expose=["False"]*16
state=[0]*8
click_time=0
list_index=[0,0]
Turns=0
# helper function to initialize globals
def new_game():
    global list_2,expose,state,click_time,list_index,Turns
    random.shuffle(list_2)
    expose=["False"]*16
    state=[0]*8
    click_time=0
    list_index=[0,0]
    Turns=0
    label.set_text('Turns = '+str(Turns))
    exposed=0
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global expose,exposed,click_time,list_index,state,state_index,Turns
    click_time+=1
    if (click_time==3):
        expose[list_index[0]]="False"
        expose[list_index[1]]="False"
        click_time=1
        list_index=[0,0]
        
    mouse_position=pos
    list_index[click_time-1]=mouse_position[0]/50
    expose[list_index[click_time-1]]="True"
    state_index=list_2[list_index[click_time-1]]
    
    if state[state_index] == 0:
        state[state_index] = 1
    elif state[state_index] == 1:
        state[state_index] = 2
    
    exposed=0
    for index in range(8):
        if state[index] == 2 and expose[index*2]=="True" and expose[index*2+1]=="True":
            exposed+=1
    
    if (click_time==2) and (state[state_index]==2):
        if exposed <= 8:                
            Turns+=1
        click_time=0
        list_index=[0,0]
    elif (click_time==2) and (state[state_index]!=2):
        if exposed <= 8:
            Turns+=1
        state[list_2[list_index[0]]]=0
        state[list_2[list_index[1]]]=0
    
    label.set_text('Turns = '+str(Turns))
           
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global expose
    for index in range(16):
        if expose[index]=="True":
            canvas.draw_polygon([(index*50, 0), (index*50+49, 0), (index*50+49, 99),(index*50, 99)], 5, 'Black', 'Black')
            canvas.draw_text(str(list_2[index]), [index*50+12, 65], 50, 'White')
        else:
            canvas.draw_polygon([(index*50, 0), (index*50+49, 0), (index*50+49, 99),(index*50, 99)], 5, 'Black', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
