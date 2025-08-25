import tkinter as tk
import threading
import main  # your main.py
import time

# GUI Setup
root = tk.Tk()
root.title("Jarvish GUI")
root.geometry("800x500")
root.configure(bg="#534747")  # dark background

# Timer at top
timer_label = tk.Label(root, text="", font=("Arial", 22, "bold"), bg="#2F7487", fg="white")
timer_label.pack(pady=8)

def update_timer():
    while True:
        current_time = time.strftime("%H:%M:%S")
        timer_label.config(text=current_time)
        time.sleep(1)

threading.Thread(target=update_timer, daemon=True).start()

# Chat box frame 
chat_frame = tk.Frame(root, bg="#0E0D0D", bd=2, relief=tk.RIDGE)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_box = tk.Text(
    chat_frame, wrap=tk.WORD, font=("Arial", 16),
    bg="#1e1e1e", fg="white", insertbackground="white", bd=0
)
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(state=tk.DISABLED)

# Chat bubble styles
chat_box.tag_config("user", foreground="white", background="#008CBA", justify="right", lmargin1=100, rmargin=10)
chat_box.tag_config("jarvis", foreground="white", background="#4CAF50", justify="left", lmargin1=10, rmargin=100)

# Update chat box function
def update_chat(user_input="", jarvis_output=""):
    chat_box.config(state=tk.NORMAL)
    if user_input:
        chat_box.insert(tk.END, f"{user_input}\n", "user")
    if jarvis_output:
        chat_box.insert(tk.END, f"{jarvis_output}\n", "jarvis")
    chat_box.see(tk.END)
    chat_box.config(state=tk.DISABLED)

# Glow effect when listening
def glow_border():
    chat_frame.config(highlightbackground="blue", highlightcolor="blue", highlightthickness=5)

def remove_glow():
    chat_frame.config(highlightthickness=0)

# Override main.speak to update GUI
original_speak = main.speak
def speak_gui(text):
    update_chat(jarvis_output=text)
    original_speak(text)

main.speak = speak_gui

# Override main.processCommand to show input in GUI
original_processCommand = main.processCommand
def processCommand_gui(command):
    update_chat(user_input=command)
    original_processCommand(command)

main.processCommand = processCommand_gui

# Voice listener thread
def voice_listener():
    main.speak("Hey, I am Jarvis. How can I help you?")
    recognizer = main.recognizer
    while True:
        try:
            # Listen for wake word
            with main.sr.Microphone() as source:
                glow_border()
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                remove_glow()
            word = recognizer.recognize_google(audio, language="en-IN")

            if "jarvis" in word.lower():
                main.speak("Ya...")

                # Display "Jarvis Active" in GUI
                update_chat(jarvis_output="Jarvis is active")

                # Listen for next command
                with main.sr.Microphone() as source:
                    glow_border()
                    audio = recognizer.listen(source)
                    remove_glow()
                    command = recognizer.recognize_google(audio)
                    main.processCommand(command)
        except:
            remove_glow()
            pass  # silently ignore errors

# Start voice listener in background thread
threading.Thread(target=voice_listener, daemon=True).start()

# Run GUI loop
root.mainloop()