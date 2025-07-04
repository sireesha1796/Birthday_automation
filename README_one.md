# Birthday WhatsApp Automation

This application automatically sends personalized birthday wishes with customized cake images via WhatsApp. It includes both a command-line version and a graphical user interface (GUI) version.

## Setup Instructions

1. Make sure you have Python 3.8 or higher installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Prepare your contacts list:
   - Use the provided `contacts.csv` file as a template
   - Format: name, phone number (with country code), birthday (DD-MMM format)
   - Example: `John Doe,+1234567890,15-Mar`

4. Add a cake image:
   - Name it `cake_template.png`
   - Place it in the same directory as the script

## Using the GUI Version

1. Run the GUI version:
   ```
   python birthday_automation_gui.py
   ```

2. The GUI provides:
   - A list of today's birthdays
   - Option to refresh the birthday list
   - Select contacts and send wishes manually
   - Status updates for all operations

## Using the Command-Line Version

Run the command-line version:
```
python birthday_automation.py
```

## Building the Executable

To create standalone executables:

For the GUI version:
```
pyinstaller --onefile --add-data "cake_template.png;." --add-data "contacts.csv;." birthday_automation_gui.py
```

For the command-line version:
```
pyinstaller --onefile --add-data "cake_template.png;." --add-data "contacts.csv;." birthday_automation.py
```

The executables will be created in the `dist` directory.

## Usage

1. Launch the application (GUI or command-line version)
2. The program will:
   - Check for birthdays on the current date
   - Create personalized cake images
   - Send WhatsApp messages automatically (or manually in GUI version)
3. First-time usage:
   - You'll need to scan the QR code to log into WhatsApp Web
   - Keep your phone connected to the internet

## Notes

- The program uses WhatsApp Web, so you need an internet connection
- Your phone must be connected to the internet while the program runs
- Messages are sent with a delay to avoid rate limiting
- The program will clean up temporary image files after sending
- The GUI version allows manual selection of recipients and real-time status updates 