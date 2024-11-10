import speech_recognition as sr
import pyttsx3
import webbrowser
import random
import os
import subprocess
from datetime import datetime
import tkinter as tk
import threading
import yt_dlp as youtube_dl
import wikipedia 

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def introduce_self():
    introductions = [
                "Hello! My name is Jarvis. I'm your virtual assistant here to help you with tasks, answer questions, and keep you entertained.",
                "Hello there. i'm jarvis , why did you summon me ?",
                "Jarvis at your service",
    ]
    introduction = random.choice(introductions)
    speak(introduction)


def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")



def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? It was two-tired!",
        "What do you call fake spaghetti? An impasta!",
    ]
    joke = random.choice(jokes)
    speak(joke)

def search_google(query):
    speak(f"Searching Google for {query}.")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def play_youtube_video(video_title):
    speak(f"Playing {video_title} on YouTube.")
    try:
        
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{video_title}", download=False)
            first_video = result['entries'][0]
            video_url = first_video['webpage_url']
            webbrowser.open(video_url)
    except Exception as e:
        speak("I couldn't play the video on YouTube.")
        print(e)


def launch_app(app_name):
    try:
        if "notepad" in app_name:
            speak("Opening Notepad.")
            os.system("notepad.exe")
        elif "spotify" in app_name:
            speak("Opening Spotify.")
            os.system("spotify.exe")  
        elif "calculator" in app_name:
            speak("Opening Calculator.")
            os.system("calc.exe")
        elif "camera" in app_name:
            speak("Opening Camera.")
            subprocess.run("start microsoft.windows.camera:", shell=True)
        elif "command prompt" in app_name or "cmd" in app_name:
            speak("Opening Command Prompt.")
            os.system("cmd.exe")
        elif "paint" in app_name:
            speak("Opening Paint.")
            os.system("mspaint.exe")
        elif "file explorer" in app_name:
            speak("Opening File Explorer.")
            os.system("explorer.exe")
        elif "task manager" in app_name:
            speak("Opening Task Manager.")
            subprocess.Popen("Taskmgr.exe")
        else:
            speak("Sorry, I don't know how to open that application.")
    except Exception as e:
        speak(f"Failed to open {app_name} due to an error.")
import wikipedia


def search_wikipedia(query):
    speak(f"Searching Wikipedia for {query}.")
    try:
        # 
        summary = wikipedia.summary(query, sentences=2)
        speak(f"Here's what I found: {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("Sorry, I could not fetch results from Wikipedia.")
    except wikipedia.exceptions.RequestError:
        speak("Sorry, I could not connect to Wikipedia at the moment.")
    except Exception as e:
        speak("Sorry, I couldn't find anything related to that.")
        print(e)


def process_command(command):
    command = command.lower()
    if "time" in command:
        tell_time()
    elif "joke" in command and "website" not in command:
        tell_joke()
    elif "search for" in command or "tell me about" in command:
        query = command.replace("search for", "").replace("tell me about", "").strip()
        search_google(query)
    elif "play" in command and "on youtube" in command:
        video_title = command.replace("play", "").replace("on youtube", "").strip()
        play_youtube_video(video_title)
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        launch_app(app_name)
    elif "what is your name" in command or "who are you" in command:
        introduce_self() 
    elif "wikipedia" in command or "wiki" in command:
        query = command.replace("search wikipedia for", "").strip()
        search_wikipedia(query)       
    else:
        speak("I'm sorry, I didn't understand that command.")


def listen_for_commands():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that. Please repeat.")
        except sr.RequestError:
            speak("Could not request results from the service.")


def activate_assistant():
    speak("How can I help you?")
    command = listen_for_commands()
    if command:
        process_command(command)


def listen_for_wake_word():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")
                if "jarvis" in command:  
                    activate_assistant()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                speak("Could not request results from the service.")
                break

def restart_assistant():
    speak("activating assistant.")
    introduce_self()  
    global wake_word_thread
    if wake_word_thread.is_alive():
        wake_word_thread.join()  
    wake_word_thread = threading.Thread(target=listen_for_wake_word, daemon=True)
    wake_word_thread.start()
    speak("The assistant is now ready.")


app = tk.Tk()
app.title("Voice Assistant")
app.geometry("400x300")
app.configure(bg="#282C34")  
label = tk.Label(
    app,
    text="Voice Assistant is running",
    font=("Helvetica", 16, "bold"),
    fg="white",
    bg="#282C34",
)
label.pack(pady=20)


activate_button = tk.Button(
    app,
    text="activate Assistant",
    command=restart_assistant,
    font=("Helvetica", 14, "bold"),
    bg="#61AFEF",  
    fg="white",
    activebackground="#56B6C2",
    activeforeground="white",
    relief="raised",
    borderwidth=0,
    padx=20,
    pady=10
)
activate_button.pack(pady=20)


footer_label = tk.Label(
    app,
    text="Say 'Jarvis' to activate",
    font=("Helvetica", 12, "italic"),
    fg="#ABB2BF",  
    bg="#282C34"
)
footer_label.pack(pady=40)


wake_word_thread = threading.Thread(target=listen_for_wake_word, daemon=True)
wake_word_thread.start()

app.mainloop()
