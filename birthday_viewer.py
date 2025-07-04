import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import platform
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random

class BirthdayViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("ISCF Birthdays")
        self.root.geometry("1000x700")
        
        # Enhanced Color scheme
        self.colors = {
            'navy': '#000080',  # Navy Blue
            'light_navy': '#1E3F66',  # Lighter Navy Blue
            'white': '#FFFFFF',  # Pure White
            'off_white': '#F8F8FF',  # Ghost White
            'red': '#FF0000',          # Bright Red
            'dark_red': '#8B0000',     # Dark Red
            'crimson': '#DC143C',      # Crimson
            'complementary': '#FF1493',  # Deep pink
            'accent1': '#FF4500',  # Orange-red
            'accent2': '#9370DB',  # Medium purple
            'text_dark': '#4B0082',  # Indigo
            'text_light': '#E6E6FA',  # Lavender
            'text_hover': '#FF69B4',  # Hot Pink
            'highlight': '#2F4F4F',  # Dark Slate Gray (changed from gold)
            'text_header': '#800080'  # Purple
        }
        
        self.root.configure(bg=self.colors['off_white'])
        
        # Check if we're on Windows
        self.is_windows = platform.system() == 'Windows'
        
        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background=self.colors['off_white'])
        
        # Main button style with red text
        style.configure(
            "Custom.TButton",
            padding=10,
            font=("Arial", 10, "bold"),
            background=self.colors['off_white'],
            foreground=self.colors['red']  # Bright Red text
        )
        
        # Secondary button style
        style.configure(
            "Secondary.TButton",
            padding=10,
            font=("Arial", 10, "bold"),
            background=self.colors['off_white'],
            foreground=self.colors['red']  # Bright Red text
        )
        
        # Treeview headers with red text
        style.configure(
            "Treeview.Heading",
            background=self.colors['off_white'],
            foreground=self.colors['red'],  # Bright Red text
            font=("Arial", 11, "bold")
        )
        
        # Notebook tabs with red text
        style.configure(
            "TNotebook.Tab",
            background=self.colors['off_white'],
            foreground=self.colors['red'],  # Bright Red text
            padding=[15, 8],
            font=("Arial", 11, "bold")
        )
        
        # Mapping for hover states
        style.map("Custom.TButton",
                 background=[('active', self.colors['off_white'])],
                 foreground=[('active', self.colors['dark_red'])])  # Dark Red on hover
                 
        style.map("Secondary.TButton",
                 background=[('active', self.colors['off_white'])],
                 foreground=[('active', self.colors['dark_red'])])  # Dark Red on hover
                 
        style.map("TNotebook.Tab",
                 background=[("selected", self.colors['off_white'])],
                 foreground=[("selected", self.colors['red']),      # Bright Red when selected
                           ("active", self.colors['crimson'])])     # Crimson on hover

        # Form labels with red text
        style.configure(
            "Form.TLabel",
            background=self.colors['off_white'],
            foreground=self.colors['red'],  # Bright Red text
            font=("Arial", 11)
        )
        
        # Title style with red text
        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold"),
            background=self.colors['off_white'],
            foreground=self.colors['red']  # Bright Red text
        )
        
        # Info label style with red text
        style.configure(
            "Info.TLabel",
            font=("Arial", 12),
            background=self.colors['off_white'],
            foreground=self.colors['red']  # Bright Red text
        )
        
        # Treeview with red text
        style.configure(
            "Treeview",
            background=self.colors['white'],
            fieldbackground=self.colors['white'],
            foreground=self.colors['red'],  # Bright Red text
            font=("Arial", 10)
        )
        
        # Configure Treeview with alternating colors
        style.configure("Treeview",
                       background=self.colors['white'],
                       fieldbackground=self.colors['white'],
                       foreground=self.colors['text_dark'],
                       font=("Arial", 10))
        
        style.configure("Treeview.Heading",
                       background=self.colors['navy'],
                       foreground=self.colors['white'],
                       font=("Arial", 11, "bold"))
        
        style.map("Treeview",
                 background=[('selected', self.colors['light_navy'])],
                 foreground=[('selected', self.colors['text_light'])],
                 fieldbackground=[('selected', self.colors['light_navy'])])
        
        # Configure Notebook with more prominent tabs
        style.configure("TNotebook",
                       background=self.colors['off_white'])
        
        style.configure("TNotebook.Tab",
                       background=self.colors['off_white'],
                       padding=[15, 8],
                       font=("Arial", 11, "bold"),
                       foreground=self.colors['red'])
        
        style.map("TNotebook.Tab",
                 background=[("selected", self.colors['off_white'])],
                 foreground=[("selected", self.colors['red']),
                           ("active", self.colors['dark_red'])])
                           
        # Entry style
        style.configure("TEntry",
                       fieldbackground=self.colors['white'],
                       foreground=self.colors['text_dark'])
        
        # Main container
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with decorative elements and larger font
        title_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        title_frame.pack(pady=(0, 20))
        
        title = ttk.Label(title_frame,
                         text="✨ ISCF Birthdays 🎂",
                         style="Title.TLabel")
        title.pack()
        
        # Subtitle with accent color
        subtitle = ttk.Label(title_frame,
                           text="Celebrating Special Days Together",
                           style="Info.TLabel",
                           font=("Arial", 14, "italic"))
        subtitle.pack(pady=(5, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Today's Birthdays Tab
        self.today_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.today_frame, text="Today's Birthdays")
        
        # All Contacts Tab
        self.contacts_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.contacts_frame, text="All Contacts")
        
        # Upcoming Birthdays Tab
        self.upcoming_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.upcoming_frame, text="Upcoming Birthdays")
        
        # Setup each tab
        self._setup_today_tab()
        self._setup_contacts_tab()
        self._setup_upcoming_tab()
        
        # Status bar at bottom
        self.status_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame,
                                    text="✨ Ready",
                                    style="Info.TLabel")
        self.status_label.pack()
        
        # Load data on startup
        self.refresh_all()
    
    def _format_day(self, day):
        """Format day number removing leading zeros"""
        return str(int(day))
    
    def _get_date_str(self, date_obj):
        """Get date string in the format 'd-MMM'"""
        if self.is_windows:
            # Windows doesn't support the '-' flag, so we need to handle it manually
            day = self._format_day(date_obj.strftime('%d'))
            return f"{day}-{date_obj.strftime('%b')}"
        else:
            return date_obj.strftime('%-d-%b')
    
    def _setup_today_tab(self):
        """Setup the Today's Birthdays tab"""
        # Today's date
        date_frame = ttk.Frame(self.today_frame)
        date_frame.pack(fill=tk.X, pady=(10, 20))
        
        today = datetime.now().strftime("%B %d, %Y")
        date_label = ttk.Label(date_frame, text=f"Today: {today}", style="Info.TLabel")
        date_label.pack()
        
        # Birthday list
        self.today_tree = ttk.Treeview(self.today_frame, columns=("Name", "Phone"), show="headings")
        self.today_tree.heading("Name", text="Name")
        self.today_tree.heading("Phone", text="Phone")
        self.today_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons frame
        btn_frame = ttk.Frame(self.today_frame)
        btn_frame.pack(pady=10)
        
        # Refresh button with secondary style
        refresh_btn = ttk.Button(btn_frame, text="Refresh", 
                               command=self.refresh_all, style="Secondary.TButton")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Send Wishes button with primary style
        send_wishes_btn = ttk.Button(btn_frame, text="Send Wishes", 
                                   command=self._show_birthday_wishes, style="Custom.TButton")
        send_wishes_btn.pack(side=tk.LEFT, padx=5)
        
        # No Wishes button with secondary style
        no_wishes_btn = ttk.Button(btn_frame, text="No Wishes", 
                                 command=self._skip_wishes, style="Secondary.TButton")
        no_wishes_btn.pack(side=tk.LEFT, padx=5)
    
    def _setup_contacts_tab(self):
        """Setup the All Contacts tab"""
        # Search frame
        search_frame = ttk.Frame(self.contacts_frame)
        search_frame.pack(fill=tk.X, pady=(10, 20))
        
        ttk.Label(search_frame, text="Search:", style="Form.TLabel").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._filter_contacts)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry")
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # Contacts list
        self.contacts_tree = ttk.Treeview(self.contacts_frame, 
                                        columns=("Name", "Phone", "Birthday"), 
                                        show="headings")
        self.contacts_tree.heading("Name", text="Name", command=lambda: self._sort_contacts("name"))
        self.contacts_tree.heading("Phone", text="Phone", command=lambda: self._sort_contacts("phone"))
        self.contacts_tree.heading("Birthday", text="Birthday", command=lambda: self._sort_contacts("birthday"))
        self.contacts_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.contacts_frame, orient=tk.VERTICAL, command=self.contacts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contacts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.contacts_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        add_btn = ttk.Button(btn_frame, text="Add Contact", 
                           command=self._show_add_dialog, style="Custom.TButton")
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(btn_frame, text="Edit Contact", 
                            command=self._edit_contact, style="Custom.TButton")
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete Contact", 
                              command=self._delete_contact, style="Custom.TButton")
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def _setup_upcoming_tab(self):
        """Setup the Upcoming Birthdays tab"""
        # Controls frame
        controls_frame = ttk.Frame(self.upcoming_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 20))
        
        ttk.Label(controls_frame, text="Show next:").pack(side=tk.LEFT)
        self.days_var = tk.StringVar(value="30")
        days_entry = ttk.Entry(controls_frame, textvariable=self.days_var, width=5)
        days_entry.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Label(controls_frame, text="days").pack(side=tk.LEFT)
        
        update_btn = ttk.Button(controls_frame, text="Update", 
                              command=self._refresh_upcoming, style="Custom.TButton")
        update_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Upcoming birthdays list
        self.upcoming_tree = ttk.Treeview(self.upcoming_frame, 
                                        columns=("Name", "Birthday", "Days"), 
                                        show="headings")
        self.upcoming_tree.heading("Name", text="Name")
        self.upcoming_tree.heading("Birthday", text="Birthday")
        self.upcoming_tree.heading("Days", text="Days Until")
        self.upcoming_tree.pack(fill=tk.BOTH, expand=True)
    
    def _show_add_dialog(self):
        """Show dialog to add new contact"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Contact")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.configure(bg=self.colors['off_white'])
        
        # Form fields
        ttk.Label(dialog, text="Name:", style="Form.TLabel").pack(pady=(20, 5))
        name_entry = ttk.Entry(dialog, style="TEntry")
        name_entry.pack(fill=tk.X, padx=20)
        
        ttk.Label(dialog, text="Phone:", style="Form.TLabel").pack(pady=(10, 5))
        phone_entry = ttk.Entry(dialog, style="TEntry")
        phone_entry.pack(fill=tk.X, padx=20)
        
        ttk.Label(dialog, text="Birthday:", style="Form.TLabel").pack(pady=(10, 5))
        birthday_entry = DateEntry(dialog, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        birthday_entry.pack()
        
        def save():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            birthday = self._get_date_str(birthday_entry.get_date())
            
            if not name or not phone:
                messagebox.showerror("Error", "Name and phone number are required!")
                return
            
            self._add_contact(name, phone, birthday)
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
    
    def _add_contact(self, name, phone, birthday):
        """Add a new contact to the CSV file"""
        try:
            # Read existing contacts
            try:
                df = pd.read_csv("contacts.csv")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["name", "phone", "birthday"])
            
            # Add new contact
            new_contact = pd.DataFrame({
                "name": [name],
                "phone": [phone],
                "birthday": [birthday]
            })
            
            df = pd.concat([df, new_contact], ignore_index=True)
            df.to_csv("contacts.csv", index=False)
            
            messagebox.showinfo("Success", "Contact added successfully!")
            self.refresh_all()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding contact: {str(e)}")
    
    def _edit_contact(self):
        """Edit selected contact"""
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit!")
            return
        
        # Get current values
        values = self.contacts_tree.item(selected[0])['values']
        name, phone, birthday = values
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Contact")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="Name:").pack(pady=(20, 5))
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, name)
        name_entry.pack(fill=tk.X, padx=20)
        
        ttk.Label(dialog, text="Phone:").pack(pady=(10, 5))
        phone_entry = ttk.Entry(dialog)
        phone_entry.insert(0, phone)
        phone_entry.pack(fill=tk.X, padx=20)
        
        ttk.Label(dialog, text="Birthday:").pack(pady=(10, 5))
        birthday_entry = DateEntry(dialog, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        # Set current birthday
        try:
            current_date = datetime.strptime(birthday, "%d-%b")
            birthday_entry.set_date(current_date.replace(year=datetime.now().year))
        except:
            pass
        
        birthday_entry.pack()
        
        def save_edit():
            new_name = name_entry.get().strip()
            new_phone = phone_entry.get().strip()
            new_birthday = self._get_date_str(birthday_entry.get_date())
            
            if not new_name or not new_phone:
                messagebox.showerror("Error", "Name and phone number are required!")
                return
            
            try:
                df = pd.read_csv("contacts.csv")
                # Find and update the contact
                mask = (df['name'] == name) & (df['phone'] == phone) & (df['birthday'] == birthday)
                df.loc[mask, ['name', 'phone', 'birthday']] = [new_name, new_phone, new_birthday]
                df.to_csv("contacts.csv", index=False)
                
                messagebox.showinfo("Success", "Contact updated successfully!")
                self.refresh_all()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error updating contact: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_edit).pack(pady=20)
    
    def _delete_contact(self):
        """Delete selected contact"""
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            return
        
        values = self.contacts_tree.item(selected[0])['values']
        name, phone, birthday = values
        
        try:
            df = pd.read_csv("contacts.csv")
            # Find and remove the contact
            mask = (df['name'] == name) & (df['phone'] == phone) & (df['birthday'] == birthday)
            df = df[~mask]
            df.to_csv("contacts.csv", index=False)
            
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.refresh_all()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting contact: {str(e)}")
    
    def _filter_contacts(self, *args):
        """Filter contacts based on search text"""
        search_text = self.search_var.get().lower()
        
        # Clear current display
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        
        try:
            df = pd.read_csv("contacts.csv")
            # Convert phone numbers to strings
            df['phone'] = df['phone'].astype(str)
            
            # Filter based on search text
            filtered_df = df[
                df['name'].str.lower().str.contains(search_text) |
                df['phone'].str.contains(search_text) |
                df['birthday'].str.lower().str.contains(search_text)
            ]
            
            # Display filtered results
            for _, row in filtered_df.iterrows():
                self.contacts_tree.insert("", tk.END, values=(row['name'], row['phone'], row['birthday']))
            
        except Exception as e:
            print(f"Error filtering contacts: {str(e)}")
    
    def _sort_contacts(self, column):
        """Sort contacts by column"""
        try:
            df = pd.read_csv("contacts.csv")
            df = df.sort_values(by=column)
            
            # Clear and repopulate the tree
            for item in self.contacts_tree.get_children():
                self.contacts_tree.delete(item)
            
            for _, row in df.iterrows():
                self.contacts_tree.insert("", tk.END, values=(row['name'], row['phone'], row['birthday']))
            
        except Exception as e:
            print(f"Error sorting contacts: {str(e)}")
    
    def _refresh_upcoming(self):
        """Refresh upcoming birthdays list"""
        try:
            days = int(self.days_var.get())
        except:
            days = 30
            self.days_var.set("30")
        
        # Clear current display
        for item in self.upcoming_tree.get_children():
            self.upcoming_tree.delete(item)
        
        try:
            df = pd.read_csv("contacts.csv")
            today = datetime.now()
            current_year = today.year
            
            upcoming = []
            for _, row in df.iterrows():
                bday = datetime.strptime(f"{row['birthday']} {current_year}", "%d-%b %Y")
                if bday < today:  # If birthday has passed this year, look at next year
                    bday = bday.replace(year=current_year + 1)
                
                days_until = (bday - today).days
                if days_until <= days:
                    upcoming.append((row['name'], row['birthday'], days_until))
            
            # Sort by days until birthday
            upcoming.sort(key=lambda x: x[2])
            
            # Display upcoming birthdays
            for name, birthday, days_until in upcoming:
                self.upcoming_tree.insert("", tk.END, values=(name, birthday, days_until))
            
        except Exception as e:
            print(f"Error refreshing upcoming birthdays: {str(e)}")
    
    def refresh_all(self):
        """Refresh all displays"""
        # Refresh today's birthdays
        for item in self.today_tree.get_children():
            self.today_tree.delete(item)
        
        try:
            df = pd.read_csv("contacts.csv")
            today = datetime.now()
            today_str = self._get_date_str(today)
            
            # Filter today's birthdays
            birthday_people = df[df['birthday'].str.lower() == today_str.lower()]
            
            if len(birthday_people) == 0:
                self.status_label.config(text="No birthdays today!")
            else:
                for _, person in birthday_people.iterrows():
                    self.today_tree.insert("", tk.END, values=(person['name'], person['phone']))
                self.status_label.config(text=f"Found {len(birthday_people)} birthday(s) today!")
            
            # Refresh other views
            self._filter_contacts()
            self._refresh_upcoming()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing data: {str(e)}")
            self.status_label.config(text="Error refreshing data!")

    def _create_birthday_image(self, name):
        """Create a personalized birthday image"""
        # List of available cake templates
        cake_templates = [
            "cake_template1.png",
            "cake_template2.png",
            "cake_template3.png",
            "cake_template4.png",
            "cake_template5.png"
        ]
        
        # Create cakes directory if it doesn't exist
        cakes_dir = "cakes"
        if not os.path.exists(cakes_dir):
            os.makedirs(cakes_dir)
            messagebox.showinfo("Info", "Created 'cakes' directory. Please add cake template images there!")
            return None

        # Get available cake templates
        available_cakes = [f for f in os.listdir(cakes_dir) if f.endswith('.png')]
        
        if not available_cakes:
            messagebox.showerror("Error", "No cake templates found in 'cakes' directory!")
            return None

        # Show cake selection dialog
        cake_window = tk.Toplevel(self.root)
        cake_window.title("Select Cake Template")
        cake_window.geometry("800x600")
        cake_window.configure(bg=self.colors['off_white'])
        
        # Variable to store selected cake and result
        selected_cake = {'image': None, 'path': None}
        
        def select_cake(cake_path):
            selected_cake['path'] = cake_path
            cake_window.destroy()
        
        # Create scrollable frame for cake options
        canvas = tk.Canvas(cake_window, bg=self.colors['off_white'])
        scrollbar = ttk.Scrollbar(cake_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title = ttk.Label(scrollable_frame, 
                         text="Choose a Cake Template",
                         style="Title.TLabel")
        title.pack(pady=20)
        
        # Create container for cake templates
        cakes_container = ttk.Frame(scrollable_frame, style="Custom.TFrame")
        cakes_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create rows of cake templates
        current_row = ttk.Frame(cakes_container, style="Custom.TFrame")
        current_row.pack(fill=tk.X, expand=True)
        col = 0
        
        for cake_file in available_cakes:
            cake_path = os.path.join(cakes_dir, cake_file)
            try:
                # Load and resize cake image for preview
                img = Image.open(cake_path)
                img = img.resize((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Create frame for each cake option
                cake_frame = ttk.Frame(current_row, style="Custom.TFrame")
                cake_frame.pack(side=tk.LEFT, padx=10, pady=10)
                
                # Add image and button
                img_label = ttk.Label(cake_frame, image=photo, background=self.colors['off_white'])
                img_label.image = photo
                img_label.pack(padx=5, pady=5)
                
                select_btn = ttk.Button(cake_frame, 
                                      text=f"Select {cake_file}",
                                      style="Custom.TButton",
                                      command=lambda p=cake_path: select_cake(p))
                select_btn.pack(pady=5)
                
                # Update position and create new row if needed
                col += 1
                if col >= 3:  # 3 cakes per row
                    col = 0
                    current_row = ttk.Frame(cakes_container, style="Custom.TFrame")
                    current_row.pack(fill=tk.X, expand=True)
                    
            except Exception as e:
                print(f"Error loading cake template {cake_file}: {str(e)}")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Wait for selection
        cake_window.wait_window()
        
        if not selected_cake['path']:
            return None
            
        try:
            img = Image.open(selected_cake['path'])
        except Exception as e:
            messagebox.showerror("Error", f"Error loading cake template: {str(e)}")
            return None

        draw = ImageDraw.Draw(img)
        
        try:
            # Adjust font size based on image dimensions
            base_font_size = 60
            # Scale font size based on image width
            font_size = int(base_font_size * (img.width / 800))  # 800 is the base width
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        message = f"Happy Birthday\n{name}!"
        
        # Get text size
        text_bbox = draw.textbbox((0, 0), message, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position (center of image)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        # Add text with outline for better visibility
        outline_color = 'black'
        outline_width = 2
        
        # Draw text outline
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), message, 
                            fill=outline_color, font=font, align="center")
        
        # Draw main text
        draw.text((x, y), message, fill='white', font=font, align="center")
        
        return img
    
    def _show_birthday_wishes(self):
        """Show birthday wishes with cake image"""
        selected = self.today_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a person to send wishes!")
            return
        
        values = self.today_tree.item(selected[0])['values']
        name = values[0]
        
        # Create cake image
        cake_img = self._create_birthday_image(name)
        if cake_img is None:
            return
        
        # Create a new window to display the cake
        cake_window = tk.Toplevel(self.root)
        cake_window.title(f"Happy Birthday {name}!")
        cake_window.geometry("800x600")
        cake_window.configure(bg=self.colors['off_white'])
        
        # Create a frame for the content with decorative border
        content_frame = ttk.Frame(cake_window, style="Custom.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Convert PIL image to PhotoImage
        cake_img = cake_img.resize((600, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(cake_img)
        
        # Create label to display image with decorative border
        img_frame = ttk.Frame(content_frame, style="Custom.TFrame")
        img_frame.pack(pady=10)
        
        img_label = ttk.Label(img_frame, image=photo, background=self.colors['accent1'])
        img_label.image = photo  # Keep a reference!
        img_label.pack(padx=3, pady=3)
        
        # Add a celebratory message with enhanced styling
        message = f"🎉 Happy Birthday {name}! 🎂\nWishing you a fantastic day filled with joy and happiness! 🎈"
        msg_label = ttk.Label(content_frame,
                            text=message,
                            style="Title.TLabel",
                            font=("Arial", 16, "bold"),
                            foreground=self.colors['accent1'],
                            wraplength=700)
        msg_label.pack(pady=20)
        
        # Close button with secondary style
        close_btn = ttk.Button(content_frame,
                             text="Close",
                             command=cake_window.destroy,
                             style="Secondary.TButton")
        close_btn.pack(pady=10)
    
    def _skip_wishes(self):
        """Handle skipping birthday wishes"""
        selected = self.today_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a person first!")
            return
        
        values = self.today_tree.item(selected[0])['values']
        name = values[0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to skip birthday wishes for {name}?"):
            self.today_tree.delete(selected[0])
            self.status_label.config(text=f"Skipped birthday wishes for {name}")

def main():
    root = tk.Tk()
    app = BirthdayViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 