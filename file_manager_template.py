import logging
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the file types and their corresponding folders
file_types = {
    'mp3': 'mp3_folder',
    'pdf': 'pdf_folder',
    'jpg': 'jpg_folder',
    'png': 'png_folder',
    'mp4': 'mp4_folder',
    'jpeg': 'jpeg_folder'
}

# Create folders if they don't exist
for folder in file_types.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Directory to monitor (e.g., Downloads directory)
download_directory = r"PATH_TO_YOUR_DOWNLOADS_DIRECTORY"

def send_email(subject, body):
    # Email configuration
    sender_email = 'YOUR_SENDER_EMAIL@gmail.com'
    receiver_email = 'YOUR_RECEIVER_EMAIL@gmail.com'
    password = 'YOUR_EMAIL_PASSWORD'
    smtp_server = 'YOUR_SMTP_SERVER'
    port = YOUR_PORT_NUMBER

    # Create the email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Usage
# send_email('Error Alert', 'An error occurred in your file manager.')

class FileHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
        try:
            for filename in os.listdir(download_directory):
                # Get the file extension
                _, extension = os.path.splitext(filename)
                extension = extension[1:].lower()  # Remove the dot and convert to lowercase

                # Check if the extension is in our file_types dictionary
                if extension in file_types:
                    source_file = os.path.join(download_directory, filename)
                    destination_folder = file_types[extension]

                    # Move the file to the corresponding folder
                    destination_file = os.path.join(destination_folder, filename)
                    os.rename(source_file, destination_file)
                    print(f"Moved {filename} to {destination_folder}")
        except Exception as e:
            logging.error(f"An error occurred in on_modified: {str(e)}")
            send_email('Error Alert', 'An error occurred in your file manager.')
    
    def on_created(self, event):
        try:
            if not event.is_directory:
                filename = os.path.basename(event.src_path)
                _, extension = os.path.splitext(filename)
                extension = extension[1:].lower()

                if extension in file_types:
                    source_file = os.path.join(download_directory, filename)
                    destination_folder = file_types[extension]
                    destination_file = os.path.join(destination_folder, filename)

                    os.rename(source_file, destination_file)
                    print(f"Moved {filename} to {destination_folder}")
        except Exception as e:
            logging.error(f"An error occurred in on_created: {str(e)}")
            send_email('Error Alert', 'An error occurred in your file manager.')

    def on_deleted(self, event):
        try:
            if not event.is_directory:
                filename = os.path.basename(event.src_path)
                _, extension = os.path.splitext(filename)
                extension = extension[1:].lower()

                if extension in file_types:
                    logging.info(f"File {filename} was deleted.")
        except Exception as e:
            logging.error(f"An error occurred in on_deleted: {str(e)}")
            send_email('Error Alert', 'An error occurred in your file manager.')

    def on_moved(self, event):
        try:
            if not event.is_directory:
                try:
                    src_filename = os.path.basename(event.src_path)
                    _, extension = os.path.splitext(src_filename)
                    extension = extension[1:].lower()

                    if extension in file_types:
                        src_folder = file_types[extension]
                        src_path = os.path.join(src_folder, src_filename)

                        dest_filename = os.path.basename(event.dest_path)
                        dest_extension = os.path.splitext(dest_filename)[1][1:].lower()

                        if dest_extension in file_types:
                            dest_folder = file_types[dest_extension]
                            dest_path = os.path.join(dest_folder, dest_filename)

                            os.rename(src_path, dest_path)
                            print(f"Moved {src_filename} from {src_folder} to {dest_folder}")
                except Exception as e:
                    logging.error(f"An error occurred while moving {src_filename}: {str(e)}")
        except Exception as e:
            logging.error(f"An error occurred in on_moved: {str(e)}")
            send_email('Error Alert', 'An error occurred in your file manager.')

event_handler = FileHandler()
observer = Observer()
observer.schedule(event_handler, path=download_directory, recursive=False)
observer.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
    send_email('File Manager Stopped', 'The file manager was manually stopped.')
observer.join()