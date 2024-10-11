import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
import threading
import time


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity

    if sentiment_polarity > 0:
        sentiment = "Positive"
    elif sentiment_polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, sentiment_polarity

def start_analysis():
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showerror("Input Error", "Please enter some text for sentiment analysis.")
        return
    
    # Display the loading message
    loading_label.config(text="Analyzing sentiment...")
    analyze_button.config(state="disabled")

    # Use threading to avoid freezing the UI during analysis
    threading.Thread(target=perform_analysis, args=(text,)).start()

def perform_analysis(text):
    time.sleep(1)  # Simulate a short delay for loading
    sentiment, polarity = analyze_sentiment(text)

    # Update the result in the main thread
    result_text = f"Sentiment: {sentiment}\nPolarity Score: {polarity:.2f}"
    loading_label.config(text="")
    analyze_button.config(state="normal")
    result_label.config(text=result_text)

def create_app():
    window = tk.Tk()
    window.title("Sentiment Analysis")
    window.geometry("400x300")
    window.config(bg="#f0f8ff")
    window.resizable(False, False)

    # Title label
    title_label = tk.Label(window, text="Text Sentiment Analyzer", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333")
    title_label.pack(pady=10)

    # Text input area
    global text_input
    text_input = tk.Text(window, height=5, width=40, font=("Arial", 12))
    text_input.pack(pady=10)

    # Analyze button
    global analyze_button
    analyze_button = tk.Button(window, text="Analyze Sentiment", font=("Arial", 12), bg="#007acc", fg="#fff", activebackground="#005f99", command=start_analysis)
    analyze_button.pack(pady=10)

    # Loading label (to show during processing)
    global loading_label
    loading_label = tk.Label(window, text="", font=("Arial", 10), bg="#f0f8ff", fg="#007acc")
    loading_label.pack()

    # Result label to display the output
    global result_label
    result_label = tk.Label(window, text="", font=("Arial", 12), bg="#f0f8ff", fg="#333")
    result_label.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_app()
