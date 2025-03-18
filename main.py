import os
import time
import json
import requests
import logging
from pathlib import Path
import pyautogui
import pygetwindow as gw
from botcity.core import DesktopBot
from src.logger.custom_logger import CustomLoggerTracker
from tqdm import tqdm

# Create an instance first
logger_tracker = CustomLoggerTracker()
# Get a logger for the registration module
logger = logger_tracker.get_logger("registration")
# logger.info("These is a test message")



class NotepadBot(DesktopBot):
    def __init__(self):
        super().__init__()

    def find_window_by_title(self, title, matching=1.0):
        """Custom method to find a window by title"""
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return True
            return False
        except Exception as e:
            logger.error(f"Error finding window: {e}")
            return False

    def action(self, execution=None):
        # Create directory for saving files if it doesn't exist
        desktop_path = Path.home() / "PycharmProjects/autoE_2DA" / "temp"/ "tjm-project"
        desktop_path.mkdir(parents=True, exist_ok=True)

        # Create logs directory
        logs_path = desktop_path / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Files will be saved to: {desktop_path}")
        logger.info(f"Logs will be saved to: {logs_path}")

        # Fetch posts from the API
        try:
            logger.info("Fetching posts from JSONPlaceholder API...")
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            posts = response.json()
            # Limit to the first 10 posts
            posts = posts[:10]
            logger.info(f"Successfully fetched {len(posts)} posts")
        except Exception as e:
            logger.error(f"Failed to fetch posts: {e}")
            return

        # Track processed posts
        processed_posts = []
        skipped_posts = []

        for post in tqdm(len(posts), desc="Processing posts", colour="greem"):
            user_id = post["userId"]
            post_id = post["id"]
            title = post["title"]
            body = post["body"]

            # Ask user if they want to save this post
            save_post = input(f"\nProcess post {post_id} with title: '{title}'? (y/n): ").strip().lower()
            if save_post != 'n':
                logger.info(f"Skipping post {post_id}")
                skipped_posts.append(post_id)
                continue

            try:
                logger.info(f"Processing post {post_id}...")

                # Launch Notepad
                self.execute("notepad.exe")
                time.sleep(1)  # Wait for Notepad to open
                logger.info("Notepad launched")

                # Check if Notepad is open
                if not self.find_window_by_title("Untitled - Notepad"):
                    logger.error("Failed to launch Notepad")
                    continue

                # Make Notepad the active window
                notepad_window = gw.getWindowsWithTitle("Untitled - Notepad")[0]
                notepad_window.activate()
                time.sleep(0.5)
                logger.info("Notepad activated")

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
                logger.info("File path typed")

                # Press Save button
                pyautogui.press('enter')
                time.sleep(1)
                logger.info("File saved")

                # Handle potential "Replace" dialog if file exists
                if self.find_window_by_title("Confirm Save As"):
                    pyautogui.press('left')  # Select "Yes"
                    pyautogui.press('enter')
                    time.sleep(0.5)

                # Close Notepad
                pyautogui.hotkey('alt', 'f4')
                time.sleep(1)
                logger.info("Notepad closed")

                logger.info(f"Successfully saved post {post_id} to {file_path}")
                processed_posts.append(post_id)

            except Exception as e:
                logger.error(f"Error processing post {post_id}: {e}")
                # Try to close Notepad if it's still open
                try:
                    notepad_windows = gw.getWindowsWithTitle("Notepad")
                    for window in notepad_windows:
                        window.close()
                except:
                    pass

            # Small delay between iterations
            time.sleep(1)

        # Save a summary report
        summary_path = logs_path / "summary_report.txt"
        with open(summary_path, 'w') as f:
            f.write("=== NOTEPAD BOT SUMMARY REPORT ===\n\n")
            f.write(f"Date and Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total posts fetched: {len(posts)}\n")
            f.write(f"Posts processed: {len(processed_posts)}\n")
            f.write(f"Posts skipped: {len(skipped_posts)}\n\n")

            f.write("Processed post IDs:\n")
            for pid in processed_posts:
                f.write(f"- Post {pid}\n")

            f.write("\nSkipped post IDs:\n")
            for pid in skipped_posts:
                f.write(f"- Post {pid}\n")

        logger.info(f"Summary report saved to {summary_path}")

        # Print final summary to terminal
        logger.info("\n=== PROCESSING COMPLETE ===")
        logger.info(f"Total posts fetched: {len(posts)}")
        logger.info(f"Total posts fetched: {len(posts)}")
        logger.info(f"Posts processed: {len(processed_posts)}")
        logger.info(f"Posts skipped: {len(skipped_posts)}")
        logger.info(f"Files saved to: {desktop_path}")
        logger.info(f"Summary report saved to: {summary_path}")




def main():
    # Create directory for saving files if it doesn't exist
    desktop_path = Path.home() / "Desktop" / "tjm-project"
    desktop_path.mkdir(parents=True, exist_ok=True)

    # Create logs directory
    logs_path = desktop_path / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)

    # # Setup logging
    # log_file = logs_path / f"notepad_bot_{time.strftime('%Y%m%d_%H%M%S')}.log"
    # setup_logging(log_file)

    # Initialize and run the bot
    print("\n=== Notepad Data Entry Bot ===")
    print("This script will fetch posts from JSONPlaceholder API and create text files in Notepad")
    print(f"Files will be saved to: {desktop_path}")
    print(f"Logs will be saved to: {logs_path}")
    print("You can choose which posts to process\n")
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
