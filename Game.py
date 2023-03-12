from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

#Main Window
height = 500
width = 800
window = Tk()
window.title('Bubble Blaster')
c = Canvas(window, height=height, width=width, bg='blue' )
c.pack()


#Submarine
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill= 'red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline= 'red')
ship_R = 15
mid_x = width/2
mid_y = height/2
c.move(ship_id, mid_x , mid_y)
c.move(ship_id2, mid_x , mid_y)

#Submarine Control
ship_spd = 10

def move_ship(event):
    if event.keysym == 'Up' or event.keysym == 'w':
        c.move(ship_id, 0, -ship_spd)
        c.move(ship_id2, 0, -ship_spd)
    elif event.keysym == 'Down' or event.keysym == 's':
        c.move(ship_id, 0, ship_spd)
        c.move(ship_id2, 0, ship_spd)
    elif event.keysym == 'Left' or event.keysym == 'a':
        c.move(ship_id, -ship_spd, 0)
        c.move(ship_id2, -ship_spd, 0)
    elif event.keysym == 'Right' or event.keysym == 'd':
        c.move(ship_id, ship_spd, 0)
        c.move(ship_id2, ship_spd, 0)
        
c.bind_all('<Key>', move_ship)


#Bubbles
bub_id = list()
bub_r = list()
bub_spd = list()
min_bub_r = 10
max_bub_r = 30
max_bub_spd = 10
gap = 100

def create_bubble():
    x = width + gap
    y = randint(0, height)
    r = randint(min_bub_r, max_bub_r)
    id1 = c.create_oval(x-r, y-r, x+r, y + r, outline='white')
    bub_id.append(id1)
    bub_r.append(r)
    bub_spd.append(randint(1, max_bub_spd))
    
#Make Bubbles move
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_spd[i], 0)
        
#Get bubble co ordinates
def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0]+pos[2])/2
    y = (pos[1]+pos[3])/2
    return x, y 

#remove bubbles
def del_bubbles(i):
    del bub_r[i]
    del bub_spd[i]
    c.delete(bub_id[i])
    del bub_id[i]

#Clean up bubbles off screen
def clean_bubbles():
    for i in range(len(bub_id)-1,-1,-1):
        x,y = get_coords(bub_id[i])
        if x < -gap:
            del_bubbles(i)

#Get distance between two points
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2-x1)**2 + (y2-y1)**2)

#Collison function
def collision():
    points = 0
    for bub in range(len(bub_id)-1,-1,-1):
        if distance(ship_id2,bub_id[bub]) < (ship_R + bub_r[bub]):
            points += (bub_r[bub] + bub_spd[bub])
            del_bubbles(bub)
    return points

#Display score
c.create_text(50, 30, text='TIME', fill='white')
c.create_text(150, 30, text='SCORE', fill='white')
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')
def show_score(score):
    c.itemconfig(score_text, text=str(score))
def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))
    
#Time limit + bonus time                
bub_chance = 10
time_limit = 30
bonus_score = 1000
score = 0
bonus = 0
end = time() + time_limit
#MAIN GAME LOOP

while time() < end:
    if randint(1, bub_chance) == 1:
        create_bubble()
    move_bubbles()
    clean_bubbles()
    score += collision()
    if (int(score/bonus_score)) > bonus:
        bonus += 1
        end += time_limit
    show_score(score)
    show_time(int(end - time()))
    window.update()
    sleep(0.01)
    
#Game Over graphic
c.create_text(mid_x,mid_y,  
                  text= 'Game Over', fill='white', font=('Helvetica', 30))
c.create_text(mid_x, mid_y + 30,
                  text ='Score: ' + str(score), fill='white', font=('Helvetica', 30))
c.create_text(mid_x, mid_y + 45,
                  text = 'Bonus time: ' + str(bonus*time_limit), fill='white')

window.mainloop()



           


