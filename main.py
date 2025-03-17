import os
import time
import json
import requests
import logging
from pathlib import Path
import pyautogui
import pygetwindow as gw
from botcity.core import DesktopBot


class NotepadBot(DesktopBot):
    def __init__(self):
        super().__init__()
        # Setup logger
        self.logger = logging.getLogger('NotepadBot')

    def find_window_by_title(self, title, matching=1.0):
        """Custom method to find a window by title"""
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error finding window: {e}")
            return False

    def action(self, execution=None):
        # Create directory for saving files if it doesn't exist
        desktop_path = Path.home() / "Desktop" / "tjm-project"
        desktop_path.mkdir(parents=True, exist_ok=True)

        # Fetch posts from the API
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            posts = response.json()
            # Limit to the first 10 posts
            posts = posts[:10]
        except Exception as e:
            self.logger.error(f"Failed to fetch posts: {e}")
            return

        for post in posts:
            post_id = post["id"]
            title = post["title"]
            body = post["body"]

            try:
                # Launch Notepad
                self.execute("notepad.exe")
                time.sleep(1)  # Wait for Notepad to open

                # Check if Notepad is open
                if not self.find_window_by_title("Untitled - Notepad"):
                    self.logger.error("Failed to launch Notepad")
                    continue

                # Make Notepad the active window
                notepad_window = gw.getWindowsWithTitle("Untitled - Notepad")[0]
                notepad_window.activate()
                time.sleep(0.5)

                # Type the title in uppercase with underline
                pyautogui.write(f"{title.upper()}\n")
                pyautogui.write("=" * len(title) + "\n\n")

                # Type the body text
                pyautogui.write(body)

                # Save the document
                pyautogui.hotkey('ctrl', 's')
                time.sleep(1)

                # Set the file path and name
                file_name = f"post {post_id}.txt"  # Using space as per the project requirements
                file_path = os.path.join(desktop_path, file_name)

                # Type the file path
                pyautogui.write(str(file_path))
                time.sleep(0.5)

                # Press Save button
                pyautogui.press('enter')
                time.sleep(1)

                # Handle potential "Replace" dialog if file exists
                if self.find_window_by_title("Confirm Save As"):
                    pyautogui.press('left')  # Select "Yes"
                    pyautogui.press('enter')
                    time.sleep(0.5)

                # Close Notepad
                pyautogui.hotkey('alt', 'f4')
                time.sleep(1)

                self.logger.info(f"Successfully saved post {post_id}")

            except Exception as e:
                self.logger.error(f"Error processing post {post_id}: {e}")
                # Try to close Notepad if it's still open
                try:
                    notepad_windows = gw.getWindowsWithTitle("Notepad")
                    for window in notepad_windows:
                        window.close()
                except:
                    pass

            # Small delay between iterations
            time.sleep(2)


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize and run the bot
    bot = NotepadBot()
    bot.action()


if __name__ == "__main__":
    main()



























































































#
# import requests
# import pyautogui
# import time
# import os
# import subprocess
#
#
#
# url = "https://jsonplaceholder.typicode.com/posts"
# response = requests.get(url)
# posts = response.json()[:10]  # Get first 10 posts
#
#
# # Directory to save files
# save_dir = os.path.join(os.path.expanduser("~"), "Desktop", "tjm-project")
# os.makedirs(save_dir, exist_ok=True)
#
#
# # Function to open Notepad
# def open_notepad():
#     subprocess.Popen("notepad.exe")
#     time.sleep(2)  # Wait for Notepad to open
#
#
# # Function to type and save text
# def type_and_save(post):
#     title = post['title']
#     body = post['body']
#     file_name = f"post {post['id']}.txt"
#     file_path = os.path.join(save_dir, file_name)
#
#     pyautogui.typewrite(f"Title: {title}\n\n{body}")
#     time.sleep(1)
#
#     # Save File: Ctrl+S, type filename, Enter
#     pyautogui.hotkey("ctrl", "s")
#     time.sleep(1)
#     pyautogui.typewrite(file_path)
#     time.sleep(1)
#     pyautogui.press("enter")
#     time.sleep(1)
#     pyautogui.hotkey("alt", "f4")  # Close Notepad
#
# if __name__=="__main__":
#     # Main loop
#     for post in posts:
#         open_notepad()
#         type_and_save(post)
