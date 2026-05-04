import csv
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def add_right_click_menu(widget):
    """Adds right-click copy/paste/cut menu to a widget."""
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label="Select All", command=lambda: widget.event_generate("<<SelectAll>>"))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)  # Right-click on Windows/Linux
    widget.bind("<Button-2>", show_menu)  # Right-click on macOS

def browse_file():
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile="my_scraped_data.csv"
    )
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)

def run_scraper():
    btn_run.config(state='disabled')
    url = entry_url.get()
    do_login = var_login.get()
    link_txt = entry_link.get()
    u_id = entry_user_id.get()
    p_id = entry_pass_id.get()
    u_val = entry_user_val.get()
    p_val = entry_pass_val.get()
    btn_css = entry_btn_css.get()
    q_class = entry_quote_class.get()
    a_class = entry_author_class.get()
    filename = entry_file.get()

    if not url or not q_class or not filename:
        messagebox.showwarning("Input Error", "Please fill in URL, Class Name, and Filename.")
        btn_run.config(state='normal')
        return

    log_display.insert(tk.END, "Initializing Chrome Driver...\n")
    log_display.see(tk.END)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 10)
        driver.get(url)

        if do_login:
            log_display.insert(tk.END, "Attempting Login...\n")
            log_display.see(tk.END)
            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_txt))).click()
            wait.until(EC.presence_of_element_located((By.ID, u_id))).send_keys(u_val)
            driver.find_element(By.ID, p_id).send_keys(p_val)
            driver.find_element(By.CSS_SELECTOR, btn_css).click()

        log_display.insert(tk.END, f"Scraping classes: {q_class}...\n")
        log_display.see(tk.END)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, q_class)))
        items = driver.find_elements(By.CLASS_NAME, q_class)
        sub_items = driver.find_elements(By.CLASS_NAME, a_class)

        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Column A", "Column B"])
            for i, s in zip(items, sub_items):
                writer.writerow([i.text, s.text])

        log_display.insert(tk.END, f"SUCCESS! Saved {len(items)} rows to:\n{filename}\n")
        log_display.see(tk.END)
        messagebox.showinfo("Finished", f"Scraped {len(items)} items successfully!")

    except Exception as e:
        log_display.insert(tk.END, f"ERROR: {str(e)}\n")
        log_display.see(tk.END)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()
        btn_run.config(state='normal')

def start_scraping_thread():
    scraper_thread = threading.Thread(target=run_scraper)
    scraper_thread.daemon = True
    scraper_thread.start()


root = tk.Tk()
root.title("Universal Web Scraper")
root.geometry("550x750")

fields = [
    ("Target URL:", "entry_url", "https://quotes.toscrape.com"),
    ("Login Link Text:", "entry_link", "Login"),
    ("Username Field ID:", "entry_user_id", "username"),
    ("Password Field ID:", "entry_pass_id", "password"),
    ("Your Username:", "entry_user_val", "admin"),
    ("Your Password:", "entry_pass_val", "1234"),
    ("Login Button (CSS):", "entry_btn_css", "input.btn-primary"),
    ("Data Class (e.text):", "entry_quote_class", "text"),
    ("Sub-Data Class (author):", "entry_author_class", "author"),
]

entries = {}
for text, var_name, default in fields:
    frame = tk.Frame(root)
    frame.pack(fill='x', padx=10, pady=2)
    lbl = tk.Label(frame, text=text, width=20, anchor='w')
    lbl.pack(side='left')
    ent = tk.Entry(frame)
    ent.insert(0, default)
    ent.pack(side='right', expand=True, fill='x')
    add_right_click_menu(ent) # Enable Copy/Paste
    entries[var_name] = ent

file_frame = tk.Frame(root)
file_frame.pack(fill='x', padx=10, pady=5)
lbl_file = tk.Label(file_frame, text="Save as (Filename):", width=20, anchor='w')
lbl_file.pack(side='left')
entry_file = tk.Entry(file_frame)
entry_file.insert(0, "my_scraped_data.csv")
entry_file.pack(side='left', expand=True, fill='x', padx=(0, 5))
add_right_click_menu(entry_file) # Enable Copy/Paste
btn_browse = tk.Button(file_frame, text="Browse...", command=browse_file)
btn_browse.pack(side='right')

entry_url = entries["entry_url"]
entry_link = entries["entry_link"]
entry_user_id = entries["entry_user_id"]
entry_pass_id = entries["entry_pass_id"]
entry_user_val = entries["entry_user_val"]
entry_pass_val = entries["entry_pass_val"]
entry_btn_css = entries["entry_btn_css"]
entry_quote_class = entries["entry_quote_class"]
entry_author_class = entries["entry_author_class"]

var_login = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Enable Login Flow?", variable=var_login).pack(pady=10)

btn_run = tk.Button(root, text="START SCRAPER", command=start_scraping_thread, bg="green", fg="white",
                    font=('Arial', 12, 'bold'))
btn_run.pack(pady=10)

log_display = scrolledtext.ScrolledText(root, height=10)
log_display.pack(padx=10, pady=10, fill='both', expand=True)
add_right_click_menu(log_display) # Enable Copy from logs

root.mainloop()