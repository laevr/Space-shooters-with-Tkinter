from tkinter import *
from tkinter import messagebox
import random

#globālie 
logs = Tk()
logs.title("Space Shooters")
logs.geometry("500x600")
logs.configure(bg="black")
score = 0
meteors = []
bullets = []
meteor_speed = 5
bullet_speed = 10
max_meteors = 6
time = 30
game_over = False

#Sign up logs
def signup():
  canvas2.destroy()
  global entry_signup_pas
  global entry_signup_user
  global label_signup
  global label_signup_user
  global label_signup_pas
  global button_submit
  button_signup.destroy()

  label_signup = Label(logs, text="Sign up",bg="black", fg="white", font=("Arial",20))
  label_signup.grid(row=1,column=3)
  
  label_signup_user = Label(logs, text="New username", bg = "black", fg="white")
  label_signup_user.grid(row=2, column=1)

  entry_signup_user = Entry(logs, width =8, bg="black", fg= "white")
  entry_signup_user.grid(row=2,column=2)
  
  label_signup_pas = Label(logs, text="New password", bg="black", fg="white")
  label_signup_pas.grid(row=3,column=1)

  entry_signup_pas = Entry(logs, width=8,show="*",bg="black", fg="white")
  entry_signup_pas.grid(row=3,column=2)

  button_submit = Button(logs, text="Submit",bg="black", fg="white",command= submit_signup)
  button_submit.grid(row=4,column=2)

#Sign up paroles un user pārbaude (aizsūta uz login)
def submit_signup():
  new_username = entry_signup_user.get()
  new_password = entry_signup_pas.get()

  if new_username.strip() == "":
    messagebox.showerror("Error","Please enter a username.")
    return

  if new_password.strip() == "":
    messagebox.showerror("Error","Please enter a password.")
    return
    
  print(new_username,new_password)

  try: #ar izņēmumu būs kaut kas (chat gpt palīdzība)
    with open("users.txt", "a") as f_users:
      f_users.write(new_username + "\n")

    with open("passwords.txt", "a") as f_passwords:
      f_passwords.write(new_password + "\n")

    messagebox.showinfo("Success!","Account created successfully! Please log in.")
    label_signup.destroy()
    label_signup_user.destroy()
    entry_signup_user.destroy()
    label_signup_pas.destroy()
    entry_signup_pas.destroy()
    button_submit.destroy()
    button_signup.destroy()
    login()
      
  except IOError as e:
    messagebox.showerror("Error", "Failed to write to files: " +str(e))
  except Exception as e:
    messagebox.showerror("Error", "An unexpected error occured: " +str(e))



#Login logs
def login():
  global entry_user
  global entry_pas
  global label
  global label_user
  global label_pas
  global button_login
  button_signup.destroy()
  canvas2.destroy()
  
  label = Label(logs, text="Login",bg="black", fg="white", font=("Arial",20))
  label.grid(row=1,column=3)

  label_user = Label(logs,text="Username",bg="black", fg="white")
  label_user.grid(row=2,column=1)

  entry_user = Entry(logs,width=8,bg="black", fg="white")
  entry_user.grid(row=2,column=2)

  label_pas = Label(logs,text="Password",bg="black", fg="white")
  label_pas.grid(row=3,column=1)

  entry_pas = Entry(logs, width=8, show="*",bg="black", fg="white")
  entry_pas.grid(row=3,column=2)

  button_login = Button(logs, text="Login", width=6,bg="black", fg="white",command = attempt_login)
  button_login.grid(row=4,column=2)

#Login pārbauda vai eksistē tāds user un pārbauda vai sakrīt parole
def attempt_login():
  global entered_user
  entered_user = entry_user.get()
  entered_pas = entry_pas.get()
  try: #tas pats kas f= open, bet nav tik confusing
    with open("users.txt", "r") as f_users, open("passwords.txt", "r") as f_passwords:
      users = [users.strip() for users in f_users.readlines()]
      passwords = [passwords.strip() for passwords in f_passwords.readlines()]
  
      if entered_user in users:
        userindex = users.index(entered_user)
        if entered_pas == passwords[userindex]:
          messagebox.showinfo("Loged in!","Successfully logged in!")
          label.destroy()
          label_user.destroy()
          entry_user.destroy()
          label_pas.destroy()
          entry_pas.destroy()
          button_login.destroy()
          main_application()
  
  
        else:
          messagebox.showerror("Error","Error: Incorrect password!")#ja nav pareizs
  
      elif entered_user.strip() == "":
        pass
  
      else:
        messagebox.showerror("Error","Error: Invalid login!") #ja nav pareizs
  
  except IOError as e:
    messagebox.showerror("Error","Failed to read the files: "+str(e))
  
  except Exception as e:
    messagebox.showerror("Error", "An unexpected error occured: " +str(e))
    

#Space Shooters spēle
def main_application():
  global game_over
  game_over = False
    
  canvas = Canvas(logs, width="500", height="600", bg="black") 
  canvas.grid(row=1,column=1)
  
  #Saglabā score highscores
  def save_score():
    try:
      with open("highscores.txt","a") as file:
        file.write(entered_user + ": " + str(score) + "\n")

    except IOError as e:
      messagebox.showerror("Error","Failed to read the files: "+str(e))

    except Exception as e:
      messagebox.showerror("Error", "An unexpected error occured: " +str(e))
        
      
  #Beidz spēli
  def end_game():
    global game_over
    if not game_over:
      game_over = True
      messagebox.showwarning("Game Over", "Time is up! Your final score is: " + str(score))
      print("caw")
      save_score()
      clear_canvas()
      highscores()

  def highscores():
    
    try:
      with open("highscores.txt", "r") as file:
        scores = file.readlines()

    except IOError as e:
      messagebox.showerror("Error","Failed to read the files: "+str(e))
      return

    Highscores_label = Label(logs, text="Highscores", bg="black", fg="white",font=("Arial",16))
    Highscores_label.grid(row=1,column=2)
    start_row = 2
    start_column = 0
    
    #chatgpt 
    for idx, score in enumerate(scores):
      row = start_row + idx // 5
      column = start_column + idx % 5
      Scores_label = Label(logs, text=score ,bg="black", fg="white", font=("Arial",12))
      Scores_label.grid(row=row, column=column, padx= 10, pady=5)
         
  def clear_canvas():
    canvas.delete("all")
    canvas.destroy()
    
    #spaceship kustības
  def flying(event): 
    taustins = event.keysym
    if taustins == "Left":
      canvas.move(spaceship, -20, 0)
    elif taustins == "Right":
      canvas.move(spaceship, 20, 0)
      
  def spawn_meteors():
    while len(meteors) < max_meteors:
      x = random.randint(20,480)
      y = random.randint(-100,-20)
      meteor = canvas.create_oval(x, y, x+30, y+30, fill="white")
      meteors.append(meteor)
      if game_over:
        return
    logs.after(2000, spawn_meteors)
          
  def move_meteors():
    for meteor in meteors:
      canvas.move(meteor, 0, meteor_speed)
      x1, y1, x2, y2 = canvas.coords(meteor)
      if y2 > 550:
        canvas.delete(meteor)
        meteors.remove(meteor)   
    logs.after(100, move_meteors)
    #logs.after(50, crash_check)
          
  def shoot(event):
    x1, y1, x2, y2 = canvas.coords(spaceship)
    x = (x1 + x2) / 2
    y = y1
    bullet = canvas.create_rectangle(x-2, y-10, x+2, y, fill = "red")
    bullets.append(bullet)
    move_bullets()
  
  def move_bullets():
    global score
    for bullet in bullets:
      canvas.move(bullet, 0, -bullet_speed)
      x1, y1, x2, y2 = canvas.coords(bullet)
      if y1 < 0:
        canvas.delete(bullet)
        bullets.remove(bullet)
        continue
      for meteor in meteors:
        ax1, ay1, ax2, ay2 = canvas.coords(meteor)
        if x1 > ax1 and x2 < ax2 and y1 > ay1 and y2 < ay2:
          canvas.delete(bullet)
          bullets.remove(bullet)
          canvas.delete(meteor)
          meteors.remove(meteor)
          score += 1
          canvas.itemconfig(score_text, text="Score: " + str(score))
          break
    logs.after(50, move_bullets)
        
  def update_timer():
    global time
    global game_over
    time -= 1
    if time <= 0:
      if not game_over: 
        end_game()
    else:
      print(time)
      canvas.itemconfig(timer_text, text = "Time: " +str(time))
      if not game_over:  
        logs.after(1000, update_timer)
  
    #def laba_bultinja_press(event):
      
      
  spaceship = canvas.create_rectangle(220,520,280,555,fill="white") 
                                              #north west anchor
  score_text = canvas.create_text(20, 20, anchor="nw", fill="white", font=("Arial", 16))
  game_score = canvas.itemconfig(score_text, text="Score: " + str(score))
      
     
  lbm = canvas.create_rectangle(430,515,440,535, fill= "#DC143C")
  l_bultinja = canvas.create_polygon(440,500,480,525, 440,550, fill="#DC143C")
  lbmd = canvas.create_rectangle(433,518,443,532, fill="#FF6A6A")
  l_bultinja_d = canvas.create_polygon(443,505,475,525, 443,545, fill="#FF6A6A")
      
  kbm = canvas.create_rectangle(70,515,55,535, fill= "#DC143C")
  k_bultinja = canvas.create_polygon(60,500,20,525, 60,550, fill="#DC143C")
  kbmd = canvas.create_rectangle(67,518,55,532, fill= "#FF6A6A")
  k_bultinja_d = canvas.create_polygon(57,505,25,525, 57,545, fill="#FF6A6A")
      
  
  global timer_label
                                                #northe east anc
  timer_text = canvas.create_text(480, 20, anchor="ne", fill="white",font=("Arial", 16), text="Time: " + str(time))
  game_time = canvas.itemconfig(timer_text, text="Time: "+str(time))
      
      
  
  canvas.focus_set()
  canvas.bind_all("<Key>", flying)
  canvas.bind("<space>", shoot)
  
  spawn_meteors()
  move_meteors()
  update_timer()


#Sākuma ekrāns
canvas2 = Canvas(logs,width="500", height="600", bg="black") 
canvas2.grid(row=1,column=1,columnspan=3)

button_login = Button(canvas2, text="Login", width=6,bg="black", fg="white",command = login)

button_signup = Button(canvas2, text="Sign up", width=6,bg="black", fg="white",command = signup)

space_shooters = "Space Shooters"
main_label = Label(canvas2, text=space_shooters, bg="black", fg="white", font=("Tahoma", 30))

canvas2.create_window(200,300, window=button_login)
canvas2.create_window(300,300, window=button_signup)
canvas2.create_window(250,400, window=main_label)

galva = canvas2.create_oval(125,100,375,260,fill="#458B74")
kreisa_auss = canvas2.create_oval(125,50,160,85,fill="#458B74")
k_auss = canvas2.create_line(140,60,180,140,fill="#458B74",width=15)
laba_auss = canvas2.create_oval(340,50,375,85,fill="#458B74")
l_auss = canvas2.create_line(360,60,320,140,fill="#458B74",width=15)

acs = canvas2.create_oval(155,130,240,210, fill="black")
tt = canvas2.create_polygon(165,130,200,128,154,167,fill="black")
ttt = canvas2.create_polygon(240,210,242,166,200,212,fill="black")
spidums = canvas2.create_oval(165,140,195,170,fill="white")
spidums_1 = canvas2.create_oval(205,155,225,175,fill="white")

acs2 = canvas2.create_oval(345,130,260,210, fill="black")
tt2 = canvas2.create_polygon(335,130,300,128,346,167,fill="black")
ttt2 = canvas2.create_polygon(260,210,258,166,300,212,fill="black")
spidums1 = canvas2.create_oval(335,140,305,170,fill="white")
spidums_2 = canvas2.create_oval(295,155,275,175,fill="white")

coord = 200, 195, 300, 240
mute = canvas2.create_arc(coord, start=180, extent=180,fill="#8B2323")

logs.mainloop()
