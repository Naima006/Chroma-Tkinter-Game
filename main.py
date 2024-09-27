import tkinter as tk
from tkinter import PhotoImage, messagebox
import random
from difficulty import Difficulty

difficulties = {
    "Easy": Difficulty("Difficulty: Easy", 20, 1,
                       ['Red', 'Blue', 'Green', 'White', 'Black','Gray']),
    
    "Medium": Difficulty("Difficulty: Medium", 30, 2,
                         ['Red', 'Blue', 'Green', 'White', 'Black', 'Gray',
                          'Silver', 'Yellow', 'Orange', 'Navy', 'Purple',
                          'Brown', 'Maroon', 'Lime']),
    
    "Hard": Difficulty("Difficulty: Hard", 40, 3,
                       ['Red', 'Blue', 'Green', 'White', 'Black', 'Gray',
                        'Silver', 'Yellow', 'Gold', 'Orange', 'Navy', 'Purple',
                        'Indigo', 'Lime', 'Pink', 'Magenta', 'Brown',
                        'Chocolate','Cyan', 'Ivory', 'Olive', 'Maroon'])
}


# 'highscore' dictionary to store highscore for each difficulty level.
highscore = {difficulty.label: 0 for difficulty in difficulties.values()}

score = 0
timeleft = 20
remaining_time = 20
game_started = False
selected_difficulty = difficulties["Easy"]     #default difficulty set to Easy.
colors = selected_difficulty.colors

def set_difficulty(difficulty):
    global selected_difficulty, timeleft, remaining_time, game_started, score
    
    selected_difficulty = difficulty
    timeleft = selected_difficulty.timeleft
    remaining_time = timeleft
    score = 0
    game_started = False
    timeLabel.config(text="Time left: " + str(remaining_time),fg="black")
    difficulty_label.config(text=selected_difficulty.label)
    scoreLabel.config(text="Score: " + str(score))
    highscoreLabel.config(text="Highscore: " + str(highscore[selected_difficulty.label]))
    label.config(text="")
    e.config(state=tk.NORMAL)
    e.delete(0, tk.END)
    root.bind('<Return>', startGame)
    hintButton.config(state=tk.DISABLED)
    hintLabel.config(text="")
    
def startGame(event):
    global game_started, timeColor

    if not game_started:
        game_started = True
        timeColor = "red" 
        
        countdown()
        hintButton.config(state=tk.NORMAL)
        pressEnterLabel.place_forget()
        instructionLabel.place_forget()
        showGameWidgets()

        colors = selected_difficulty.colors
        random.shuffle(colors)
        nextColor()
        
    elif game_started:
        nextColor()

def nextColor():
    global score, timeleft, timeColor
    
    if timeleft > 0 and game_started:
        e.focus_set()
        colors = selected_difficulty.colors

        if e.get().lower() == colors[1].lower():
            score += selected_difficulty.difficulty_multiplier

            if score > highscore[selected_difficulty.label]:
                highscore[selected_difficulty.label] = score
                highscoreLabel.config(text="Highscore: " + str(highscore[selected_difficulty.label]))
            highlightScore("green")

        elif selected_difficulty.label == "Difficulty: Hard":
            score -= 1
            if score < 0:
                score = 0
            highscoreLabel.config(text="Highscore: " + str(highscore[selected_difficulty.label]))
            highlightScore("red")

        else:
            highscoreLabel.config(text="Highscore: "
                                  + str(highscore[selected_difficulty.label]))
            highlightScore("red")

        e.delete(0, tk.END)
        random.shuffle(colors)
        label.config(fg=str(colors[1]), text=str(colors[0]))
        scoreLabel.config(text="Score: " + str(score))

    elif game_started:
        replayGame()

    
def highlightScore(color):
    scoreLabel.config(fg=color)
    root.after(700, lambda: scoreLabel.config(fg="black"))
    

def countdown():
    global remaining_time, timeColor, game_started, current_label

    if remaining_time > 0 and game_started:
        remaining_time -= 1
        timeLabel.config(text="Time left: " + str(remaining_time)) 

        if timeColor == "red":
            timeColor = "black"

        else:
            timeColor = "red"
        timeLabel.config(fg=timeColor)
        root.after(1000, countdown)

    elif game_started:
        timeLabel.config(fg="red", text="Time's up!  ")
        e.config(state=tk.DISABLED)
        root.unbind('<Return>', startGame)

        if current_label == difficulties["Easy"]:
            set_difficulty(difficulties["Easy"])
        elif current_label == difficulties["Medium"]:
            set_difficulty(difficulties["Medium"])
        elif current_label == difficulties["Hard"]:
            set_difficulty(difficulties["Hard"])

        reset_difficulty()


def reset_difficulty():
    set_difficulty(selected_difficulty)
    countdown()       # timer restarts when the difficulty is reset

def showHint():
    if game_started == True:
        hintLabel.config(text="Focus on the color hidden within the words!")
    
def replayGame():
    global highscore, score, timeleft, remaining_time, game_started

    set_difficulty(selected_difficulty)
    highscoreLabel.config(text="Highscore: " + str(highscore[selected_difficulty.label]))
    e.config(state=tk.NORMAL)
    e.delete(0, tk.END)
    root.bind('<Return>', startGame)

    score = 0
    timeleft = remaining_time
    remaining_time = timeleft
    game_started = False
    scoreLabel.config(text="Score: " + str(score))
    timeLabel.config(text="Time left: " + str(timeleft), fg="black")
    label.config(text="")
    hintButton.config(state=tk.DISABLED)
    hintLabel.config(text="")

    e.focus_set()
    pressEnterLabel1.place(relx=0.5, rely=0.67, anchor="center")

    # 1st page widgets
    pressEnterLabel.place_forget()
    instructionLabel.place_forget()
    
    # 2nd page widgets
    showGameWidgets()
    nextColor()


def showGameWidgets():
   timeLabel.pack(pady=160)
   scoreLabel.place(relx=0.448, rely=0.2, anchor="center")
   highscoreLabel.place(relx=0.5, rely=0.15, anchor="center")
   label.place(relx=0.5, rely=0.37, anchor="center")
   hintButton.place(relx=0.5, rely=0.50, anchor="center")
   hintLabel.place(relx=0.5, rely=0.55, anchor="center")
   e.pack(pady=58)
   replayButton.place(relx=0.24, rely=0.72, anchor="nw")
   exitButton.place(relx=0.6, rely=0.72, anchor="nw")
    

def hideGameWidgets():
    timeLabel.pack_forget()
    scoreLabel.place_forget()
    highscoreLabel.place_forget()
    label.place_forget()
    hintButton.place_forget()
    hintLabel.place_forget()
    e.pack_forget()
    replayButton.place_forget()
    exitButton.place_forget()
    
    
def create_menu():
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    difficulty_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Difficulty", menu=difficulty_menu)

    difficulty_menu.add_command(label="Easy", command=lambda: set_difficulty(difficulties["Easy"]))
    difficulty_menu.add_command(label="Medium", command=lambda: set_difficulty(difficulties["Medium"]))
    difficulty_menu.add_command(label="Hard", command=lambda: set_difficulty(difficulties["Hard"]))

    about_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", menu=about_menu)
    about_menu.add_command(label="About", command=about)
    
    return menubar


def about():
    about_message = (
        "Welcome to 'CHROMA'\n\n"
        "A thrilling game of colors developed by Triads. "
        "Test your reflexes and color recognition skills in this fast-paced challenge. "
        "The objective is simple: type the name of the color you see displayed, not the word itself. "
        "Pay attention, stay focused, and see how high you can score before time runs out!\n\n"
        "Developed by Triads\nVersion 1.0\n\n"
        "© [Metropolitan University/Triads] 2023"
    )
    messagebox.showinfo("About", about_message)
    
    


# Main window and setting up game interface
root = tk.Tk()
root.title("'CHROMA' | Developed by Triads")
root.geometry("500x707")
background_image = PhotoImage(file="colorbg.png")


# Canvas to display images and other graphical elements
canvas = tk.Canvas(root, width=500, height=707)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=background_image)

menu_bar = create_menu()

difficulty_label = tk.Label(root, text="Difficulty: Easy", font=("Arial", 12))
difficulty_label.pack()


# Create labels, buttons, and other widgets for the game interface
instructionLabel = tk.Label(canvas, text="Let the colorful chaos begin!",
                            font=("Consolas", 14, ""), fg="red")
instructionLabel.place(relx=0.5, rely=0.48, anchor="center")
instructionLabel.pack_forget()

pressEnterLabel = tk.Label(canvas, text="Press 'Enter' to start", font=("Consolas", 18, "bold"))
pressEnterLabel.place(relx=0.5, rely=0.56, anchor="center")

pressEnterLabel1 = tk.Label(canvas, text="Press 'Enter' to start", font=("Consolas", 12), fg="dim gray")
pressEnterLabel1.place(relx=0.5, rely=0.67, anchor="center")
pressEnterLabel1.place_forget()


scoreLabel = tk.Label(canvas, text="Score: " + str(score), font=("Consolas", 16, "bold"))

highscoreLabel = tk.Label(canvas, text="Highscore: " + str(highscore), font=("Consolas", 16, "bold"))

timeLabel = tk.Label(canvas, text="Time left: " + str(timeleft), font=("Consolas", 16, "bold"))

label = tk.Label(canvas, font=("Helvica", 60))

hintButton = tk.Button(canvas, text="Hint", command=showHint, fg="red", font=("Consolas", 12, "bold"), state=tk.DISABLED)
hintLabel = tk.Label(canvas, text="", fg="dim gray", font=("Consolas", 12))

e = tk.Entry(canvas, font=("Consolas", 20))
root.bind('<Return>', startGame)

replayButton = tk.Button(canvas, text=" Replay ", command=replayGame, fg="white", bg="orange", font=("Consolas", 14, "bold"))

exitButton = tk.Button(canvas, text=" Exit ", command=root.destroy, fg="white", bg="red", font=("Consolas", 14, "bold"))

e.focus_set()

root.mainloop()
