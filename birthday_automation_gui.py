import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pywhatkit
from datetime import datetime
import time
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import threading

class BirthdayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Birthday Automation")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Custom.TButton", padding=10, font=("Arial", 10))
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#f0f0f0")
        style.configure("Info.TLabel", font=("Arial", 10), background="#f0f0f0")
        
        # Main container
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(self.main_frame, text="Birthday Automation Dashboard", style="Title.TLabel")
        title.pack(pady=(0, 20))
        
        # Today's date
        date_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        date_frame.pack(fill=tk.X, pady=(0, 20))
        
        today = datetime.now().strftime("%B %d, %Y")
        date_label = ttk.Label(date_frame, text=f"Today: {today}", style="Info.TLabel")
        date_label.pack()
        
        # Birthday list frame
        self.birthday_frame = ttk.LabelFrame(self.main_frame, text="Today's Birthdays", padding="10")
        self.birthday_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create Treeview for birthdays
        self.birthday_tree = ttk.Treeview(self.birthday_frame, columns=("Name", "Phone"), show="headings")
        self.birthday_tree.heading("Name", text="Name")
        self.birthday_tree.heading("Phone", text="Phone")
        self.birthday_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Refresh button
        refresh_btn = ttk.Button(button_frame, text="Refresh Birthdays", 
                               command=self.refresh_birthdays, style="Custom.TButton")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Send wishes button
        send_btn = ttk.Button(button_frame, text="Send Birthday Wishes", 
                            command=self.send_selected_wishes, style="Custom.TButton")
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.status_frame.pack(fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", style="Info.TLabel")
        self.status_label.pack()
        
        # Load birthdays on startup
        self.refresh_birthdays()
    
    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def refresh_birthdays(self):
        """Refresh the birthday list"""
        # Clear existing items
        for item in self.birthday_tree.get_children():
            self.birthday_tree.delete(item)
        
        try:
            # Read contacts from CSV
            df = pd.read_csv(self.resource_path("contacts.csv"))
            today = datetime.now().strftime("%d-%b")
            
            # Filter contacts whose birthday is today
            birthday_people = df[df['birthday'].str.contains(today, case=False)]
            
            if len(birthday_people) == 0:
                self.status_label.config(text="No birthdays today!")
                return
            
            # Add to treeview
            for _, person in birthday_people.iterrows():
                self.birthday_tree.insert("", tk.END, values=(person['name'], person['phone']))
            
            self.status_label.config(text=f"Found {len(birthday_people)} birthday(s) today!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading birthdays: {str(e)}")
            self.status_label.config(text="Error loading birthdays!")
    
    def create_birthday_image(self, name):
        """Create a personalized birthday image"""
        try:
            img = Image.open(self.resource_path("cake_template.png"))
        except FileNotFoundError:
            messagebox.showerror("Error", "cake_template.png not found!")
            return None

        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(self.resource_path("arial.ttf"), 60)
        except:
            font = ImageFont.load_default()

        message = f"Happy Birthday\n{name}!"
        
        text_bbox = draw.textbbox((0, 0), message, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        draw.text((x, y), message, fill='white', font=font, align="center")
        
        output_path = f"birthday_{name}.png"
        img.save(output_path)
        return output_path
    
    def send_birthday_message(self, phone_number, name, image_path):
        """Send WhatsApp message with birthday image"""
        try:
            message = f"🎉 Happy Birthday {name}! 🎂\nWishing you a fantastic day filled with joy and happiness! 🎈"
            pywhatkit.sendwhats_image(phone_number, image_path, message, wait_time=15)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error sending message to {name}: {str(e)}")
            return False
    
    def send_selected_wishes(self):
        """Send wishes to selected contacts"""
        selected_items = self.birthday_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select contacts to send wishes to!")
            return
        
        def send_wishes_thread():
            self.status_label.config(text="Sending wishes...")
            for item in selected_items:
                values = self.birthday_tree.item(item)['values']
                name, phone = values
                
                image_path = self.create_birthday_image(name)
                if image_path:
                    if self.send_birthday_message(phone, name, image_path):
                        self.status_label.config(text=f"Sent wishes to {name}")
                    try:
                        os.remove(image_path)
                    except:
                        pass
                    time.sleep(5)  # Wait between messages
            
            self.status_label.config(text="All wishes sent successfully!")
        
        # Run in separate thread to keep UI responsive
        threading.Thread(target=send_wishes_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = BirthdayApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 