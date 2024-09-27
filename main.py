from PIL import Image
import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
import speech_recognition as sr
from threading import Thread
import queue

# Initialize a queue to communicate between threads
image_queue = queue.Queue()

root = tk.Tk()
root.title("Text/Voice to Hand Gesture Conversion")
root.geometry("500x400")
var = tk.StringVar()

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

r = sr.Recognizer()

COMMON_WORDS_GESTURES = {
    "hello": r"D:\programming\web project\words\hello.jpeg",
    "thank you": r"D:\programming\web project\words\thank_you.jpeg",
    "yes": r"D:\programming\web project\words\yes.png",
    "no": r"D:\programming\web project\words\no.jpg",
    "please": r"D:\programming\web project\words\please.png",
}

LETTER_GESTURES = {    
    "a": r"D:\programming\web project\alphabet\a.jpg",
    "b": r"D:\programming\web project\alphabet\b.jpg",
    "c": r"D:\programming\web project\alphabet\c.png",
    "d": r"D:\programming\web project\alphabet\d.png",
    "e": r"D:\programming\web project\alphabet\e.jpeg",
    "f": r"D:\programming\web project\alphabet\f.png",
    "g": r"D:\programming\web project\alphabet\g.png",
    "h": r"D:\programming\web project\alphabet\h.png",
    "i": r"D:\programming\web project\alphabet\i.png",
    "j": r"D:\programming\web project\alphabet\j.gif",
    "k": r"D:\programming\web project\alphabet\k.gif",
    "l": r"D:\programming\web project\alphabet\l.gif",
    "m": r"D:\programming\web project\alphabet\m.gif",
    "n": r"D:\programming\web project\alphabet\n.gif",
    "o": r"D:\programming\web project\alphabet\o.gif",
    "p": r"D:\programming\web project\alphabet\p.gif",
    "q": r"D:\programming\web project\alphabet\q.gif",
    "r": r"D:\programming\web project\alphabet\r.gif",
    "s": r"D:\programming\web project\alphabet\s.gif",
    "t": r"D:\programming\web project\alphabet\t.gif",
    "u": r"D:\programming\web project\alphabet\u.gif",
    "v": r"D:\programming\web project\alphabet\v.gif",
    "w": r"D:\programming\web project\alphabet\w.gif",
    "x": r"D:\programming\web project\alphabet\x.gif",
    "y": r"D:\programming\web project\alphabet\y.gif",
    "z": r"D:\programming\web project\alphabet\z.gif"
}

def get_gesture_images(text_input):
    gesture_images = []
    if text_input in COMMON_WORDS_GESTURES:
        gesture_images.append(COMMON_WORDS_GESTURES[text_input])
    else:
        for char in text_input.lower():
            if char in [' ', '\t', '\n']:
                continue
            image_path = LETTER_GESTURES.get(char, None)
            if image_path:
                gesture_images.append(image_path)
            else:
                print(f"No gesture found for '{char}'")
    return gesture_images

def display_images(image_paths):
    if not image_paths:
        print("No images to display")
        return

    fig, axs = plt.subplots(1, len(image_paths), figsize=(len(image_paths) * 3, 3))
    if len(image_paths) == 1:
        axs = [axs]

    for i, img_path in enumerate(image_paths):
        img = Image.open(img_path)
        axs[i].imshow(img)
        axs[i].axis('off')
    plt.show()

def handle_text_input():
    text_input = var.get() 
    gesture_images = get_gesture_images(text_input)
    image_queue.put(gesture_images)  # Put images into the queue for main thread to handle

def transcribe_live_audio():
    """Capture and transcribe live audio from the microphone."""
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=1)  
        print("Ready to record... Start speaking!")
        
        try:
            audio_listened = r.listen(source, timeout=10, phrase_time_limit=5)  
            print("Transcribing your speech...")
            text = r.recognize_google(audio_listened)
            print("You said: ", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return ""

def handle_voice_input():
    print("Starting voice recognition...")
    Thread(target=transcribe_and_convert).start()

def transcribe_and_convert():
    recognized_text = transcribe_live_audio()
    if recognized_text: 
        var.set(recognized_text)
        gesture_images = get_gesture_images(recognized_text)
        image_queue.put(gesture_images)  # Put images into the queue for main thread to handle

def update_display():
    """Check the image queue for any images to display (run in main thread)."""
    try:
        gesture_images = image_queue.get_nowait()
        if gesture_images:
            display_images(gesture_images)
    except queue.Empty:
        pass
    root.after(100, update_display)  # Continuously check the queue every 100 ms

label = ctk.CTkLabel(root, text="Enter the text or use voice input:", text_color="black")
label.pack(padx=10, pady=10)

text = ctk.CTkEntry(root, textvariable=var, fg_color="white", border_color="black", border_width=2, text_color="black")
text.pack(padx=10, pady=20)

button_text = ctk.CTkButton(
    master=root,
    text="Convert Text to Gesture",
    width=200,
    height=50,
    fg_color="#A30EF3", 
    text_color="white", 
    hover_color="#FF7043",  
    corner_radius=8, 
    command=handle_text_input
)
button_text.pack(padx=20, pady=20)

button_voice = ctk.CTkButton(
    master=root,
    text="Convert Voice to Gesture",
    width=200,
    height=50,
    fg_color="#CD0EF3",  
    text_color="white", 
    hover_color="#A30EF3", 
    corner_radius=8, 
    command=handle_voice_input
)
button_voice.pack(padx=20, pady=20)

# Start checking the image queue on the main thread
root.after(100, update_display)

if __name__ == "__main__":
    root.mainloop()
