## 📖 How to Use

### 1. Basic Scraping
1.  **Target URL**: Enter the full URL of the site you want to scrape.
2.  **Data Class**: Enter the **CSS Class Name** of the main items you want to grab (e.g., `text` for quotes).
3.  **Sub-Data Class**: Enter the **CSS Class Name** of the secondary data (e.g., `author`).
4.  **Save as**: Click **Browse...** to choose where to save your `.csv` file.
5.  Click **START SCRAPER**.

### 2. Login Flow (Optional)
If the data is behind a login wall:
1.  Check the **Enable Login Flow?** box.
2.  Provide the **Login Link Text** (the text on the button that takes you to the login page).
3.  Provide the **ID** attributes for the Username and Password input fields.
4.  Provide the **CSS Selector** for the "Submit" or "Login" button.

---

## 🔍 Finding the "Classes"
To find the correct Class Names for a new website:
1.  Open the website in Chrome.
2.  Right-click the text you want to scrape and select **Inspect**.
3.  Look for the `class="..."` attribute in the highlighted code. Use that name in the "Data Class" field of the scraper.

---

## 💻 Troubleshooting (Common Errors)

### "CreateProcess error=2" or "Interpreter Not Found"
If you download this project and see an error regarding the `python.exe` path, it is likely because your local environment path differs from the original creator's.
*   **In PyCharm**: Go to `File > Settings > Project > Python Interpreter`.
*   Add a **New Local Interpreter**.
*   In the terminal, run `pip install selenium webdriver-manager` again to refresh the libraries for your specific machine.

## 📦 Exporting to .exe
To create a standalone Windows application:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all selenium --collect-all webdriver_manager SrapeTest.py
