import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import threading

# Global email list and theme
email_list = []
is_dark_mode = True

# Function to send email
def send_email():
    sender = sender_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)
    attachments = attachment_listbox.get(0, tk.END)

    if not email_list:
        log("Recipient list is empty!")
        return

    try:
        # Step 1: Setup SMTP connection
        progress_var.set(10)
        root.update_idletasks()

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()

        progress_var.set(25)
        root.update_idletasks()

        smtp.starttls()
        progress_var.set(40)
        root.update_idletasks()

        smtp.login(sender, password)
        progress_var.set(60)
        root.update_idletasks()

        # Step 2: Prepare email
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['Subject'] = subject
        msg.attach(MIMEText(body))

        for file in attachments:
            with open(file, 'rb') as f:
                part = MIMEApplication(f.read(), name=os.path.basename(file))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file)}"'
                msg.attach(part)

        msg['To'] = ", ".join(email_list)
        progress_var.set(80)
        root.update_idletasks()

        # Step 3: Send email
        smtp.sendmail(sender, email_list, msg.as_string())
        smtp.quit()

        progress_var.set(100)
        root.update_idletasks()

        log("✅ Email sent successfully!")

    except Exception as e:
        log(f"❌ Error: {e}")
        progress_var.set(0)


# Log messages
def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# Add email to list
def add_email():
    email = recipient_entry.get()
    if email and email not in email_list:
        email_list.append(email)
        recipient_listbox.insert(tk.END, email)
        recipient_entry.delete(0, tk.END)

# Remove selected email
def remove_email():
    selected = recipient_listbox.curselection()
    for i in selected[::-1]:
        email_list.pop(i)
        recipient_listbox.delete(i)

# Add attachment
def add_attachment():
    files = filedialog.askopenfilenames()
    for file in files:
        attachment_listbox.insert(tk.END, file)

# Toggle light/dark mode
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

# Apply theme
def apply_theme():
    bg = "#1e1e1e" if is_dark_mode else "#ffffff"
    fg = "#ffffff" if is_dark_mode else "#000000"
    entry_bg = "#2e2e2e" if is_dark_mode else "#f0f0f0"
    text_bg = "#2e2e2e" if is_dark_mode else "#ffffff"
    btn_bg = "#444444" if is_dark_mode else "#eeeeee"

    root.configure(bg=bg)
    main_frame.configure(bg=bg)
    form_frame.configure(bg=bg, highlightbackground=fg, highlightthickness=1)

    for widget in form_frame.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass

    for entry in [sender_entry, password_entry, subject_entry, recipient_entry]:
        entry.configure(bg=entry_bg, fg=fg, insertbackground=fg, relief=tk.FLAT, highlightthickness=1)

    body_text.configure(bg=text_bg, fg=fg, insertbackground=fg, relief=tk.FLAT)
    log_box.configure(bg=text_bg, fg=fg, insertbackground=fg, relief=tk.FLAT)
    toggle_btn.config(text="☀️ Light Mode" if is_dark_mode else "🌙 Dark Mode", bg=btn_bg, fg=fg)

# GUI setup
root = tk.Tk()
root.title("📧 Email Sender")
root.geometry("700x800")
root.configure(padx=20, pady=20)
root.attributes("-alpha", 0.0)

# Centralized and padded frame
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

form_frame = tk.Frame(main_frame, bd=10, relief="ridge")
form_frame.pack(padx=20, pady=20)

label_opts = {"padx": 5, "pady": 5, "anchor": "w"}
entry_opts = {"width": 50}

# Sender Email
tk.Label(form_frame, text="Your Email:", **label_opts).grid(row=0, column=0, sticky="w")
sender_entry = tk.Entry(form_frame, **entry_opts)
sender_entry.grid(row=0, column=1)

# Password
tk.Label(form_frame, text="App Password:", **label_opts).grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(form_frame, show='*', **entry_opts)
password_entry.grid(row=1, column=1)

# Subject
tk.Label(form_frame, text="Subject:", **label_opts).grid(row=2, column=0, sticky="w")
subject_entry = tk.Entry(form_frame, **entry_opts)
subject_entry.grid(row=2, column=1)

# Body
tk.Label(form_frame, text="Message:", **label_opts).grid(row=3, column=0, sticky="nw")
body_text = tk.Text(form_frame, height=5, width=50)
body_text.grid(row=3, column=1)

# Recipients
tk.Label(form_frame, text="Recipients:", **label_opts).grid(row=4, column=0, sticky="nw")
recipient_entry = tk.Entry(form_frame, **entry_opts)
recipient_entry.grid(row=4, column=1)
tk.Button(form_frame, text="Add", command=add_email).grid(row=4, column=2)
recipient_listbox = tk.Listbox(form_frame, height=4, width=50)
recipient_listbox.grid(row=5, column=1)
tk.Button(form_frame, text="Remove", command=remove_email).grid(row=5, column=2)

# Attachments
tk.Label(form_frame, text="Attachments:", **label_opts).grid(row=6, column=0, sticky="nw")
attachment_listbox = tk.Listbox(form_frame, height=4, width=50)
attachment_listbox.grid(row=6, column=1)
tk.Button(form_frame, text="Browse", command=add_attachment).grid(row=6, column=2)

# Send button
tk.Button(form_frame, text="🚀 Send Email", command=lambda: threading.Thread(target=send_email).start()).grid(row=7, column=1, pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill="x", pady=10)

# Log area
tk.Label(main_frame, text="Log:").pack(anchor="w")
log_box = tk.Text(main_frame, height=10)
log_box.pack(fill="both", expand=True)

# Theme toggle
toggle_btn = tk.Button(main_frame, text="🌙 Dark Mode", command=toggle_theme)
toggle_btn.pack(pady=10)

# Fade-in animation using after()
def fade_in(i=0):
    if i <= 10:
        root.attributes("-alpha", i / 10)
        root.after(30, fade_in, i + 1)

apply_theme()
root.after(0, fade_in)
root.mainloop()
