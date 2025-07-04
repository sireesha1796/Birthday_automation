import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import pywhatkit
from datetime import datetime
import time
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_birthday_image(name):
    """Create a personalized birthday image"""
    # Load the base cake image
    try:
        img = Image.open(resource_path("cake_template.png"))
    except FileNotFoundError:
        print("Error: cake_template.png not found!")
        return None

    # Create drawing object
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(resource_path("arial.ttf"), 60)
    except:
        font = ImageFont.load_default()

    # Add text to image
    message = f"Happy Birthday\n{name}!"
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), message, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate position (center of image)
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    
    # Add text with outline for better visibility
    draw.text((x, y), message, fill='white', font=font, align="center")
    
    # Save the image
    output_path = f"birthday_{name}.png"
    img.save(output_path)
    return output_path

def send_birthday_message(phone_number, name, image_path):
    """Send WhatsApp message with birthday image"""
    try:
        message = f"🎉 Happy Birthday {name}! 🎂\nWishing you a fantastic day filled with joy and happiness! 🎈"
        pywhatkit.sendwhats_image(phone_number, image_path, message, wait_time=15)
        print(f"Birthday message sent successfully to {name}")
        time.sleep(5)  # Wait between messages to avoid rate limiting
    except Exception as e:
        print(f"Error sending message to {name}: {str(e)}")

def main():
    try:
        # Read contacts from CSV
        df = pd.read_csv(resource_path("contacts.csv"))
        
        print("Birthday Automation Started!")
        print("Reading contacts list...")
        
        today = datetime.now().strftime("%m-%d")
        
        # Filter contacts whose birthday is today
        birthday_people = df[df['birthday'].str.contains(today)]
        
        if len(birthday_people) == 0:
            print("No birthdays today!")
            return
        
        print(f"Found {len(birthday_people)} birthday(s) today!")
        
        for _, person in birthday_people.iterrows():
            print(f"\nProcessing birthday wish for {person['name']}...")
            
            # Create personalized image
            image_path = create_birthday_image(person['name'])
            if image_path:
                # Send WhatsApp message
                send_birthday_message(person['phone'], person['name'], image_path)
                
                # Clean up the generated image
                try:
                    os.remove(image_path)
                except:
                    pass
        
        print("\nBirthday automation completed!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 