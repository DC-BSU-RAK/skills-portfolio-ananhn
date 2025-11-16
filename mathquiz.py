from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Create main window
root = Tk()
root.title("Math Quiz")

# ---- FULL SCREEN MODE ----
#sets the main window to occupy the screen.
root.attributes("-fullscreen", True)         
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False)) 

root.configure(bg='lightblue')

# Load background image 
def load_bg(path):
    try:
        img = Image.open(path)
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        # Uses LANCZOS (high quality resampling) for resizing.
        img = img.resize((screen_w, screen_h), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None

bg_start = load_bg("bgimage.png")
bg_instruction = load_bg("instruction.jpg")
bg_difficulty = load_bg("difficulty.jpg")
bg_problem = load_bg("problem.jpg")
bg_results = load_bg("results.jpg")

difficulty = None
score = 0
question_number = 0
attempt = 1
timer_seconds = 15
timer_job = None

current_problem = {
    "num1": None,
    "num2": None,
    "operation": None,
    "correct": None
}

# ------------ PAGE SYSTEM ------------
container = Frame(root)
#container fills the root window
container.pack(fill="both", expand=True)

pages = {}
for p in ("StartPage", "InstructionPage", "DifficultyPage", "ProblemPage", "ResultPage"):
    frame = Frame(container)
    #Frame uses relative width and height for ensuring it fills the container.
    frame.place(relwidth=1, relheight=1)  
    pages[p] = frame
#show_page and clear_frame are essential for managing the page transitions.
def show_page(name):
    pages[name].tkraise()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# ------------ RANDOM FUNCTIONS ------------
def randomInt(level):
    if level == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation(level):
    if level == "Easy":
        return random.choice(["+", "-"])
    elif level == "Moderate":
        return random.choice(["+", "-", "×"])
    else:
        return random.choice(["+", "-", "×", "÷"])


# ------------ START PAGE ------------
def build_start_page():
    frame = pages["StartPage"]
    clear_frame(frame)

    if bg_start:
        bg_label = Label(frame, image=bg_start)
    # Sets the background label to cover the entire frame.
        bg_label.place(relwidth=1, relheight=1)
    #prevent the PhotoImage from being garbage collected.
        bg_label.image = bg_start
#Button placement using relative coordinate
    Button(frame, text="Start Game", font=("Arial", 16, "bold"), bg="#a476c1",
       fg="white",
       activebackground="#a45ec9",
       relief="flat",
        width=8,height=1, command=lambda: show_page("InstructionPage")).place(
               relx=0.5, rely=0.92, anchor="center"   # <-- ADJUST HEIGHT HERE
           )


# ------------ INSTRUCTION PAGE ------------
def build_instruction_page():
    frame = pages["InstructionPage"]
    clear_frame(frame)

    if bg_instruction:
        bg_label = Label(frame, image=bg_instruction)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_instruction

    Button(frame, text="Continue", font=("Arial", 18, "bold"),
       activebackground="#a45ec9",relief="flat",
         width=8,height=1, bg="#a476c1", fg="white",
           command=lambda: show_page("DifficultyPage")).place(
               relx=0.5, rely=0.92, anchor="center"   # <-- ADJUST HEIGHT HERE
           )


# ------------ DIFFICULTY PAGE ------------
def displayMenu():
    build_difficulty_page()
    show_page("DifficultyPage")


def build_difficulty_page():
#initialize and show the difficulty page.
    frame = pages["DifficultyPage"]
    clear_frame(frame)
#Background Image loading and placement
#using relwidth and rel height=1 for bg_label to ensure image covers the screen.
    if bg_difficulty:
        bg_label = Label(frame, image=bg_difficulty)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_difficulty

# relative positioning variables
#relx is used to position the entire column of buttons.
    relx_start = 0.75
# Easy button setup
    rely_easy=0.3

    Button(frame, text="1. Easy", font=("Arial", 13, "bold"),
           width=11, bg="teal", fg="white",
           command=lambda: start_quiz("Easy")).place(relx=relx_start, rely=rely_easy, anchor="center")
# Label providing context for the level.
    Label(frame, text="(Single digit numbers)", fg="white", bg="#330066",
          font=("Arial", 11)).place(relx=relx_start, rely=rely_easy + 0.05, anchor="center")
    #Moderate button setup
    rely_moderate = 0.5

    Button(frame, text="2. Moderate", font=("Arial", 13, "bold"),
           width=11, bg="orange", fg="white",
           command=lambda: start_quiz("Moderate")).place(relx=relx_start, rely=rely_moderate, anchor="center")

    Label(frame, text="(Double digit numbers)", fg="white", bg="#330066",
          font=("Arial", 11)).place(relx=relx_start, rely=rely_moderate + 0.05, anchor="center")
    #Advanced button setup
    rely_advanced = 0.7
    Button(frame, text="3. Advanced", font=("Arial", 13, "bold"),
           width=11, bg="red", fg="white",
           command=lambda: start_quiz("Advanced")).place(relx=relx_start, rely=rely_advanced, anchor="center")
    Label(frame, text="(Four digit numbers)", fg="white", bg="#330066",
          font=("Arial", 11)).place(relx=relx_start, rely=rely_advanced + 0.05, anchor="center")


# ------------ START QUIZ ------------
def start_quiz(level):
    global difficulty, score, question_number, attempt, current_problem
    #sets global difficulty based on the level selected.
    difficulty = level
    #reset scores and counters
    #ensures player starts fresh when game is initiated,
    score = 0
    question_number = 0
    attempt = 1
    #resets the current problem state
    current_problem = {"num1": None, "num2": None, "operation": None, "correct": None}
    # Calls the function that generates and displays the first math problem.
    displayProblem()
    # Shows the frame where the math problems and timer appear.
    show_page("ProblemPage")


# ------------ QUESTION PAGE ------------
def displayProblem():
    global timer_seconds, question_number, attempt, current_problem, timer_job

    frame = pages["ProblemPage"]
    clear_frame(frame)

    if bg_problem:
        bg_label = Label(frame, image=bg_problem)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_problem

    if timer_job:
        # Correctly cancels any running timer before starting a new one.
        root.after_cancel(timer_job)

    # --- POSITIONING VARIABLES ---
    # These must be defined every time the function runs!
    relx_center = 0.7
    rely_question_num = 0.23
    y_start_content = 0.35
    rely_timer = 0.08
    # ------------------------------------------------------

    # New question only on attempt 1
    if attempt == 1:
        question_number += 1
        if question_number > 10:
            displayResults()
            return

        num1, num2 = randomInt(difficulty)
        op = decideOperation(difficulty)

        if op == "÷":
            num2 = random.randint(2, 20)
            num1 = num2 * random.randint(2, 20)
            correct = round(num1 / num2, 2)
        elif op == "×":
            correct = num1 * num2
        elif op == "+":
            correct = num1 + num2
        else:
            correct = num1 - num2

        current_problem.update({"num1": num1, "num2": num2, "operation": op, "correct": correct})

    # Timerlabel creation and placement:
    timer_seconds = 15
    timer_label = Label(frame, text=f"Time: {timer_seconds}s",font=("Arial", 16, "bold"), bg="#0F0E0F", fg="yellow")
    timer_label.place(relx=relx_center, rely=rely_timer, anchor="center")
    frame.timer_label = timer_label

    # Question Number
    Label(frame, text=f"Question {question_number}/10",
          font=("Arial", 18, "bold"), bg="#D44CD0", fg="yellow").place(relx=relx_center, rely=rely_question_num, anchor="center")

    # Math Problem
    Label(frame, text=f"{current_problem['num1']} {current_problem['operation']} {current_problem['num2']} =",
          font=("Arial", 32, "bold"), bg="#2B2A2A", fg="white").place(
              relx=relx_center, rely=y_start_content + 0.05, anchor="center")

    # Entry Box
    entry = Entry(frame, font=("Arial", 22), width=12, justify="center")
    entry.place(relx=relx_center, rely=y_start_content + 0.2, anchor="center")
    entry.focus()
    entry.bind("<Return>", lambda e: isCorrect(entry))

    # Submit Button
    Button(frame, text="Submit", font=("Arial", 13, "bold"),
           bg="blue", fg="white", width=10,
           command=lambda: isCorrect(entry)).place(relx=relx_center, rely=y_start_content + 0.35, anchor="center")

    updateTimer()


# ------------ TIMER ------------
def updateTimer():
    global timer_seconds, timer_job, attempt

    frame = pages["ProblemPage"]
    frame.timer_label.config(text=f"Time: {timer_seconds}s")

    if timer_seconds > 0:
        timer_seconds -= 1
        timer_job = root.after(1000, updateTimer)
    else:
        messagebox.showwarning("Time's up!", f"Correct answer: {current_problem['correct']}")
        attempt = 1
        displayProblem()


# ------------ CHECK ANSWER ------------
def isCorrect(entry_widget):
    global score, attempt, timer_job, current_problem

    if timer_job:
        #prevent the time from running, while the answer is being checked.
        root.after_cancel(timer_job)

    try:
        #converts user entry to float for division answers.
        user = float(entry_widget.get())
    except:
        # If conversion fails (non-numeric input), alerts the user and redraws the problem to reset the timer/entry.
        messagebox.showwarning("Error!", "Please enter a number.")
        displayProblem()
        return
# compares players answer with storred answer.
    if round(user, 2) == round(current_problem["correct"], 2):
        # Uses the 'attempt' global variable correctly to award 10 or 5 points.
        points = 10 if attempt == 1 else 5
        score += points
        messagebox.showinfo("Correct!", f"+{points} points!")
    #state reset and transition(correct answer)
        attempt = 1
        current_problem = {"num1": None, "num2": None, "operation": None, "correct": None}
        displayProblem()
        #Incorrect answer handling
    else:
        if attempt == 1:
            attempt = 2 #second attempt
            messagebox.showwarning("Try Again", "Incorrect! You have one more chance.")
            displayProblem()
            #state reset and transition(Failed)
        else:
            messagebox.showinfo("Incorrect",f"The correct answer was: {current_problem['correct']}")
            attempt = 1
            current_problem = {"num1": None, "num2": None, "operation": None, "correct": None}
            displayProblem() #moves to the next question or results if done.


# ------------ RESULTS PAGE ------------
def get_grade(score):
    #simple conditional logic to assign letter grade based on  final score.
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def displayResults():
    frame = pages["ResultPage"]
    clear_frame(frame)

    if bg_results:
        bg_label = Label(frame, image=bg_results)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image =bg_results

    show_page("ResultPage")

    grade = get_grade(score)
#central x-axis position for all elements.
    relx_center = 0.5
    #Quiz Complete
    Label(frame, text="Quiz Complete!", font=("Arial", 20, "bold"),
          fg="white", bg="#0A0A0A").place(relx=relx_center, rely=0.1, anchor="center")
    # y-postion for main metrics.
    y_content_start = 0.20
#Final score.
    Label(frame, text=f"Final Score: {score}/100", font=("Arial", 26, "bold"),
          fg="white", bg="#33002B").place(relx=relx_center, rely=y_content_start, anchor="center")
#Grade Label
#uses foreground colors (white/red) for emphising on fail/pass.
    Label(frame, text=f"Grade: {grade}", font=("Arial", 26, "bold"),
          fg="white" if score >= 70 else "red", bg="#003300").place(relx=relx_center, rely=y_content_start + 0.12, anchor="center")
#Play Again Button
# Command restarts the quiz flow by calling the start page builder and showing the start page.
    Button(frame, text="Play Again", font=("Arial", 14, "bold"),
           bg="blue", fg="white", width=10,
           command=lambda: [build_start_page(), show_page("StartPage")]).place(relx=relx_center, rely=y_content_start + 0.28, anchor="center")
# Quit Button
# Command correctly uses root.destroy to close the application.
    Button(frame, text="Quit", font=("Arial", 14, "bold"),
           bg="red", fg="white", width=10,
           command=root.destroy).place(relx=relx_center, rely=y_content_start + 0.45, anchor="center")


# ------------ INIT ------------
build_start_page()
build_instruction_page()
displayMenu()
show_page("StartPage")

root.mainloop()
