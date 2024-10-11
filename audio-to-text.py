
import smtplib
import os
import whisper
import warnings
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, StringVar, Toplevel
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PW = os.getenv('LOGIN_PW')
# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

class AudioTranscriberApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Transcriber")
        self.master.geometry("500x300")
        self.master.configure(bg="#2c3e50")

        # Create UI elements
        self.label = Label(master, text="Upload Audio File:", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.upload_button = Button(master, text="Upload", command=self.upload_audio, bg="#3498db", fg="white", font=("Helvetica", 12))
        self.upload_button.pack(pady=10)

        self.email_label = Label(master, text="Enter your email:", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        self.email_label.pack(pady=10)

        self.email_entry = Entry(master, width=30, font=("Helvetica", 12))
        self.email_entry.pack(pady=10)

        self.transcribe_button = Button(master, text="Transcribe", command=self.transcribe_and_send, bg="#3498db", fg="white", font=("Helvetica", 12))
        self.transcribe_button.pack(pady=10)

        self.audio_file_path = ""
        self.loading_label = None

    def upload_audio(self):
        # Open a file dialog to select an audio file
        self.audio_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if self.audio_file_path:
            messagebox.showinfo("File Selected", f"Selected file: {os.path.basename(self.audio_file_path)}")

    def transcribe_and_send(self):
        if not self.audio_file_path:
            messagebox.showerror("Error", "Please upload an audio file.")
            return

        recipient_email = self.email_entry.get()
        if not recipient_email:
            messagebox.showerror("Error", "Please enter your email address.")
            return

        # Show loading window
        self.show_loading_screen()

        # Transcribe and send in a separate thread
        threading.Thread(target=self.transcribe_and_email, args=(recipient_email,)).start()

    def show_loading_screen(self):
        self.loading_window = Toplevel(self.master)
        self.loading_window.geometry("300x100")
        self.loading_window.title("Processing...")
        self.loading_window.configure(bg="#2c3e50")

        loading_label = Label(self.loading_window, text="Processing, please wait...", fg="white", bg="#2c3e50", font=("Helvetica", 12))
        loading_label.pack(pady=20)

    def hide_loading_screen(self):
        self.loading_window.destroy()

    def transcribe_and_email(self, recipient_email):
        # Transcribe the audio
        transcription = self.transcribe_with_whisper(self.audio_file_path)

        # Send the transcription via email
        self.send_email(recipient_email, "Your Transcription Result", transcription)

        # Hide loading window after processing
        self.hide_loading_screen()
        messagebox.showinfo("Success", "Transcription completed and sent to your email!")

    def transcribe_with_whisper(self, audio_file_path):
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
        return result["text"]

    def send_email(self, recipient_email, subject, body):
        # Set your email and app password
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Create a secure SSL context

            # with smtplib.SMTP('smtp.gmail.com', 587) as server:
            #     server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            #     server.login(sender_email, sender_password)
            #     server.send_message(msg)
            #     messagebox.showinfo("Success", "Email sent successfully!")
            with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
                server.starttls()
                server.login(LOGIN_EMAIL , LOGIN_PW)
                server.send_message(msg)
                messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

if __name__ == "__main__":
    root = Tk()
    app = AudioTranscriberApp(root)
    root.mainloop()
