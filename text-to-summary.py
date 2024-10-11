import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from transformers import pipeline
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PW = os.getenv('LOGIN_PW')

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

def summarize_text(text, min_length=40):
    input_length = len(text.split())
    max_length = min(150, max(50, input_length // 2))
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def send_email(to_email, summary):
    try:
        # Set up your email details here
        sender_email = "youremail@example.com"  # Replace with your email
        sender_password = "yourpassword"  # Replace with your password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = "Your Summarized Text"

        msg.attach(MIMEText(summary, 'plain'))

        # Create a secure SSL context

        # with smtplib.SMTP('smtp.gmail.com', 587) as server:
        #     server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        #     server.login(sender_email, sender_password)
        #     server.send_message(msg)
        #     messagebox.showinfo("Success", "Email sent successfully!")
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.starttls()
            server.login(LOGIN_EMAIL,LOGIN_PW)
            server.send_message(msg)
            messagebox.showinfo("Success", "Email sent successfully!")
        
        messagebox.showinfo("Success", "Summary sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")

def start_summarization():
    text = input_text.get("1.0", tk.END).strip()
    email = email_entry.get().strip()

    if not text:
        messagebox.showwarning("Input required", "Please enter some text to summarize.")
        return
    if not email:
        messagebox.showwarning("Input required", "Please enter a valid email address.")
        return

    # Display loading message
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Processing, please wait...")

    # Summarize the text
    summary = summarize_text(text)

    # Display the result in the result_text box
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, summary)

    # Send the summary to the provided email
    send_email(email, summary)

# Set up the GUI
window = tk.Tk()
window.title("Text Summarizer")
window.geometry("600x600")
window.config(bg="#f2f2f2")

# Label and input for text
tk.Label(window, text="Enter Text to Summarize:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=10)
input_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=10, font=("Arial", 10))
input_text.pack(pady=5)

# Email input
tk.Label(window, text="Enter Email ID:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=10)
email_entry = tk.Entry(window, width=40, font=("Arial", 12))
email_entry.pack(pady=5)

# Result text box
tk.Label(window, text="Summarized Text:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=10)
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=10, font=("Arial", 10))
result_text.pack(pady=5)

# Summarize button
summarize_button = tk.Button(window, text="Summarize and Send Email", command=start_summarization, bg="#4CAF50", fg="white", font=("Arial", 12))
summarize_button.pack(pady=20)

window.mainloop()
