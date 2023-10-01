# File Manager with Automatic File Organization and Error Notifications

This Python-based file manager is designed to automatically organize files in a specified directory based on their file types, such as mp3, pdf, jpg, png, and mp4, into respective folders. Additionally, it features an error notification system through email to keep you informed in case of any errors during file handling.

## Features
+ Automatic File Organization: Files are automatically sorted into designated folders based on their file types, promoting better organization and easier access to your files.

+ Real-time Monitoring: The file manager continuously monitors a specified directory (e.g., Downloads) for any file modifications, including creations, deletions, and movements.

+ Error Notification System: In the event of an error during file handling, the system will send you an email alert to promptly inform you of the issue, enabling you to take necessary actions.

## Usage
1. Clone or download this repository.

2. Modify the configurations:

    + Set the download_directory to the path of the directory you want to monitor.
    + Configure the sender_email, receiver_email, password, smtp_server, and port in the send_email function to match your email provider details.

3. Run the script:


```python
file_manager_template.py
```

## Dependencies
+ Python 3.x
+ Required Python packages can be installed using pip:

  ```bash
  pip install watchdog
  ```
+ watchdog: Python library for file system monitoring
+ smtplib: Python library for sending emails

## Contributing
Contributions are welcome! If you have suggestions, improvements, or would like to report issues, please open an issue or create a pull request.
