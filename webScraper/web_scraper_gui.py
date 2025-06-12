import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = url_entry.get()
    tag = tag_var.get()
    keyword = keyword_entry.get().lower()

    if not url or not tag:
        messagebox.showwarning("Input Error", "Please enter a URL and select a tag.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(tag)

        output_text.delete("1.0", tk.END)  # Clear previous results
        count = 0

        for i, elem in enumerate(elements, 1):
            text = elem.get_text(strip=True)
            if keyword == "" or keyword in text.lower():
                count += 1
                output_text.insert(tk.END, f"{count}. {text}\n\n")

        if count == 0:
            output_text.insert(tk.END, "No matching content found for that keyword.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", str(e))

def save_results():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("No Content", "There is no content to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("Saved", f"Results saved to {file_path}")

# GUI Setup
root = tk.Tk()
root.title("Web Scraper with Keyword Filter")
root.geometry("650x550")
root.resizable(False, False)

# URL Input
tk.Label(root, text="Enter URL:").pack(pady=5)
url_entry = tk.Entry(root, width=70)
url_entry.pack(pady=5)

# Tag Selector
tk.Label(root, text="Select HTML Tag:").pack(pady=5)
tag_var = tk.StringVar()
tag_dropdown = ttk.Combobox(root, textvariable=tag_var, values=["h1", "h2", "h3", "p", "a", "div", "span"], state="readonly")
tag_dropdown.current(0)
tag_dropdown.pack(pady=5)

# Keyword Input
tk.Label(root, text="Enter Keyword (optional):").pack(pady=5)
keyword_entry = tk.Entry(root, width=40)
keyword_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Scrape", command=scrape_website, bg="#4CAF50", fg="white", width=20).pack(pady=10)
tk.Button(root, text="Save Results", command=save_results, bg="#2196F3", fg="white", width=20).pack(pady=5)

# Output Box
output_frame = tk.Frame(root)
output_frame.pack(pady=10, fill="both", expand=True)

output_scroll = tk.Scrollbar(output_frame)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_frame, wrap=tk.WORD, yscrollcommand=output_scroll.set, height=15)
output_text.pack(side=tk.LEFT, fill="both", expand=True)
output_scroll.config(command=output_text.yview)

# Start GUI
root.mainloop()
