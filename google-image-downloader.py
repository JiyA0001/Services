
import os
import zipfile
import smtplib
import time
from tkinter import Tk, Label, Entry, Button, messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PW = os.getenv('LOGIN_PW')

# Function to download images
def download_images(keyword, limit):
    # Removed headless option
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
    images_dir = os.path.join(os.getcwd(), keyword.replace(" ", "_") + "_images")

    try:
        # Create directory to save images if not exists
        os.makedirs(images_dir, exist_ok=True)

        # Open Google Images
        driver.get("https://www.google.com/imghp")

        # Wait for the search box to become visible (up to 10 seconds)
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # Wait for images to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
        )

        # Find image elements
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        downloaded = 0

        for image in images:
            if downloaded >= limit:
                break
            try:
                # Using 'data-src' to ensure we get the full-sized image if available
                image_url = image.get_attribute("src") or image.get_attribute("data-src")
                if image_url:
                    # Download the image
                    image_data = requests.get(image_url).content  # Use requests to download the image
                    with open(os.path.join(images_dir, f"{keyword}_{downloaded + 1}.jpg"), "wb") as file:
                        file.write(image_data)
                    downloaded += 1
            except StaleElementReferenceException:
                print("StaleElementReferenceException encountered, trying to re-fetch images.")
                # Refresh the images list and retry
                images = driver.find_elements(By.CSS_SELECTOR, "img")
                continue
            except Exception as e:
                print(f"Could not download image {downloaded + 1}: {e}")

        print(f"Downloaded {downloaded} images.")
        return images_dir

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Function to zip the downloaded images
def zip_images(images_dir):
    zip_filename = images_dir + ".zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(images_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    return zip_filename

# Function to send email with the zip file
def send_email(zip_file, email_id):
    # Replace with your email credentials
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    # Set up the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_id
    message['Subject'] = "Images Downloaded"

    # Attach the zip file
    with open(zip_file, "rb") as f:
        mime = MIMEBase('application', 'zip')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        mime.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file)}')
        message.attach(mime)

    # Send the email
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(LOGIN_EMAIL, LOGIN_PW)
        server.send_message(message)
        messagebox.showinfo("Success", "Email sent successfully!")

# Function to handle the input and process
def handle_input():
    keyword = keyword_entry.get()
    limit = int(limit_entry.get())
    email_id = email_entry.get()

    if not keyword or not limit or not email_id:
        messagebox.showerror("Input Error", "Please fill out all fields.")
        return

    images_dir = download_images(keyword, limit)
    if images_dir:
        zip_file = zip_images(images_dir)
        send_email(zip_file, email_id)
        messagebox.showinfo("Success", f"Images downloaded and sent to {email_id}")
        
        # Clean up: Delete downloaded images and zip file
        for root, _, files in os.walk(images_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(images_dir)  # Remove the empty directory
        os.remove(zip_file)    # Remove the zip file

    else:
        messagebox.showerror("Error", "Failed to download images.")

# Set up the Tkinter window
root = Tk()
root.title("Image Downloader")
root.geometry("400x200")

Label(root, text="Keyword:").pack(pady=5)
keyword_entry = Entry(root)
keyword_entry.pack(pady=5)

Label(root, text="Number of images:").pack(pady=5)
limit_entry = Entry(root)
limit_entry.pack(pady=5)

Label(root, text="Email ID:").pack(pady=5)
email_entry = Entry(root)
email_entry.pack(pady=5)

Button(root, text="Download and Send", command=handle_input).pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
