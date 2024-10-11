import os
from tkinter import Tk, Button, Label, Entry, messagebox, Toplevel
from gtts import gTTS
import threading
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PW = os.getenv('LOGIN_PW')

class TextToAudioApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Text to Audio Converter")
        self.master.geometry("500x300")
        self.master.configure(bg="#2c3e50")

        # Create UI elements
        self.label = Label(master, text="Enter Text:", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.text_entry = Entry(master, width=50, font=("Helvetica", 12))
        self.text_entry.pack(pady=10)

        self.file_label = Label(master, text="Enter Audio File Name:", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        self.file_label.pack(pady=10)

        self.file_entry = Entry(master, width=30, font=("Helvetica", 12))
        self.file_entry.pack(pady=10)

        self.convert_button = Button(master, text="Convert to Audio", command=self.convert_text_to_audio, bg="#3498db", fg="white", font=("Helvetica", 12))
        self.convert_button.pack(pady=10)

        self.loading_label = None

    def convert_text_to_audio(self):
        text = self.text_entry.get().strip()
        audio_file_name = self.file_entry.get().strip()

        if not text:
            messagebox.showerror("Error", "Please enter the text to convert.")
            return
        if not audio_file_name:
            messagebox.showerror("Error", "Please enter the audio file name.")
            return

        # Show loading window
        self.show_loading_screen()

        # Convert text to audio in a separate thread
        threading.Thread(target=self.generate_audio, args=(text, audio_file_name)).start()

    def show_loading_screen(self):
        self.loading_window = Toplevel(self.master)
        self.loading_window.geometry("300x100")
        self.loading_window.title("Processing...")
        self.loading_window.configure(bg="#2c3e50")

        loading_label = Label(self.loading_window, text="Processing, please wait...", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        loading_label.pack(pady=20)

    def hide_loading_screen(self):
        self.loading_window.destroy()

    def generate_audio(self, text, audio_file_name):
        try:
            tts = gTTS(text, lang='en')
            audio_path = f"{audio_file_name}.mp3"
            tts.save(audio_path)

            self.hide_loading_screen()
            messagebox.showinfo("Success", f"Audio saved as {audio_path}!")
        except Exception as e:
            self.hide_loading_screen()
            messagebox.showerror("Error", f"Failed to convert text to audio: {e}")

if __name__ == "__main__":
    root = Tk()
    app = TextToAudioApp(root)
    root.mainloop()
