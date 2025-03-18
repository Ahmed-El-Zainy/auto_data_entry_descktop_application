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
import traceback
import sys

# Create an instance first
logger_tracker = CustomLoggerTracker()
# Get a logger for the registration module
logger = logger_tracker.get_logger("main")


class NotepadBot(DesktopBot):
    def __init__(self):
        super().__init__()
        self.desktop_path = None
        self.logs_path = None

    def find_window_by_title(self, title, partial=False, timeout=5):
        """
        Enhanced method to find a window by title with timeout and partial matching
        Args:
            title (str): Window title to search for
            partial (bool): Whether to allow partial title matching
            timeout (int): Maximum seconds to wait for window

        Returns:
            bool: True if window found, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                windows = gw.getWindowsWithTitle(title)
                if windows:
                    if partial:
                        return True
                    else:
                        # Check for exact match
                        for window in windows:
                            if window.title == title:
                                return True
                time.sleep(0.2)
            except Exception as e:
                logger.error(f"Error finding window '{title}': {str(e)}")
                return False

        logger.warning(f"Window '{title}' not found after {timeout} seconds")
        return False

    def initialize_directories(self):
        """Set up necessary directories for files and logs"""
        try:
            # Create directory for saving files if it doesn't exist
            self.desktop_path = Path.home() / "PycharmProjects/autoE_2DA" / "temp" / "tjm-project"
            self.desktop_path.mkdir(parents=True, exist_ok=True)

            # Create logs directory
            self.logs_path = self.desktop_path / "logs"
            self.logs_path.mkdir(parents=True, exist_ok=True)

            logger.info(f"Files will be saved to: {self.desktop_path}")
            logger.info(f"Logs will be saved to: {self.logs_path}")
            return True
        except Exception as e:
            logger.critical(f"Failed to initialize directories: {str(e)}")
            logger.debug(traceback.format_exc())
            return False

    def fetch_posts(self, limit=10, retry_count=3, timeout=10):
        """
        Fetch posts from the API with retry logic

        Args:
            limit (int): Maximum number of posts to fetch
            retry_count (int): Number of retry attempts
            timeout (int): Request timeout in seconds

        Returns:
            list: List of posts or empty list if failed
        """
        posts = []
        attempt = 0

        while attempt < retry_count:
            try:
                logger.info(f"Fetching posts from JSONPlaceholder API (attempt {attempt + 1}/{retry_count})...")
                response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=timeout)

                if response.status_code == 200:
                    posts = response.json()
                    # Limit to the specified number of posts
                    posts = posts[:limit]
                    logger.info(f"Successfully fetched {len(posts)} posts")
                    return posts
                else:
                    logger.error(f"API returned status code {response.status_code}")
            except requests.exceptions.Timeout:
                logger.error(f"Request timed out (attempt {attempt + 1}/{retry_count})")
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error (attempt {attempt + 1}/{retry_count})")
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)} (attempt {attempt + 1}/{retry_count})")
            except Exception as e:
                logger.error(f"Unexpected error fetching posts: {str(e)}")
                logger.debug(traceback.format_exc())

            attempt += 1
            if attempt < retry_count:
                # Exponential backoff: 1s, 2s, 4s, etc.
                wait_time = 2 ** (attempt - 1)
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        logger.error("All attempts to fetch posts failed")
        return []

    def launch_notepad(self, retry_count=3):
        """
        Launch Notepad with retry logic

        Returns:
            bool: True if Notepad launched successfully, False otherwise
        """
        for attempt in range(retry_count):
            try:
                logger.info(f"Launching Notepad (attempt {attempt + 1}/{retry_count})...")

                # Close any existing Notepad instances to avoid confusion
                self.close_all_notepads()
                time.sleep(0.5)

                # Try different methods to launch Notepad
                if attempt == 0:
                    # First try using botcity
                    self.execute("notepad.exe")
                elif attempt == 1:
                    # Second try using os.system
                    os.system("start notepad.exe")
                else:
                    # Last try using subprocess
                    import subprocess
                    subprocess.Popen(["notepad.exe"], shell=True)

                # Wait for Notepad to open with increasing patience
                wait_time = 1 + attempt
                logger.info(f"Waiting {wait_time} seconds for Notepad to open...")
                time.sleep(wait_time)

                # Check if Notepad is open
                if self.find_window_by_title("Untitled - Notepad", timeout=3):
                    logger.info("Notepad launched successfully")
                    # Make Notepad the active window
                    notepad_windows = gw.getWindowsWithTitle("Untitled - Notepad")
                    if notepad_windows:
                        notepad_windows[0].activate()
                        time.sleep(0.5)
                        logger.info("Notepad activated")
                        return True
            except Exception as e:
                logger.error(f"Exception while launching Notepad (attempt {attempt + 1}): {str(e)}")
                logger.debug(traceback.format_exc())

        logger.error("All attempts to launch Notepad failed")
        return False

    def close_all_notepads(self):
        """Close all open Notepad windows"""
        try:
            notepad_windows = gw.getWindowsWithTitle("Notepad")
            for window in notepad_windows:
                try:
                    window.close()
                    logger.info(f"Closed Notepad window: {window.title}")
                except Exception as e:
                    logger.warning(f"Failed to close Notepad window: {str(e)}")

            # Give windows time to close
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error closing Notepad windows: {str(e)}")

    def safe_type(self, text, interval=0.01):
        """Type text safely with error handling"""
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            logger.error(f"Error typing text: {str(e)}")
            return False

    def safe_hotkey(self, *keys):
        """Press hotkey safely with error handling"""
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            logger.error(f"Error pressing hotkey {keys}: {str(e)}")
            return False

    def safe_press(self, key):
        """Press key safely with error handling"""
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            logger.error(f"Error pressing key {key}: {str(e)}")
            return False

    def process_post(self, post):
        """
        Process a single post by creating a text file with its content

        Args:
            post (dict): Post data

        Returns:
            bool: True if successful, False otherwise
        """
        user_id = post["userId"]
        post_id = post["id"]
        title = post["title"]
        body = post["body"]

        logger.info(f"Processing post {post_id}...")

        # Launch Notepad
        if not self.launch_notepad():
            logger.error(f"Failed to launch Notepad for post {post_id}")
            return False

        try:
            # Type the title in uppercase with underline
            self.safe_type(f"{title.upper()}\n")
            self.safe_type("=" * len(title) + "\n\n")

            # Add metadata
            self.safe_type(f"Post ID: {post_id}\n")
            self.safe_type(f"User ID: {user_id}\n\n")

            # Type the body text
            self.safe_type(body)

            # Add timestamp at the bottom
            self.safe_type(f"\n\n---\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Save the document
            if not self.save_file(post_id):
                return False

            # Close Notepad
            self.safe_hotkey('alt', 'f4')
            time.sleep(1)

            # Verify Notepad is closed
            if self.find_window_by_title("Untitled - Notepad", timeout=2):
                logger.warning("Notepad didn't close properly, forcing closure")
                self.close_all_notepads()

            logger.info(f"Successfully processed post {post_id}")
            return True

        except Exception as e:
            logger.error(f"Error processing post {post_id}: {str(e)}")
            logger.debug(traceback.format_exc())
            # Clean up
            self.close_all_notepads()
            return False

    def save_file(self, post_id):
        """
        Save the current Notepad file

        Args:
            post_id (int): ID of the post being saved

        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Create file name
            file_name = f"post_{post_id}.txt"
            file_path = self.desktop_path / file_name

            # Save using keyboard shortcuts
            logger.info(f"Saving file to: {file_path}")
            self.safe_hotkey('ctrl', 's')
            time.sleep(1)

            # Check if Save dialog is open
            if not self.find_window_by_title("Save As", partial=True, timeout=3):
                logger.error("Save dialog did not appear")
                return False

            # Type the file path
            self.safe_type(str(file_path))
            time.sleep(0.5)

            # Press Save button
            self.safe_press('enter')
            time.sleep(1)

            # Handle "File already exists" dialog
            if self.find_window_by_title("Confirm Save As", timeout=2):
                logger.info("File already exists - handling confirmation dialog")
                self.safe_press('left')  # Select "Yes"
                self.safe_press('enter')
                time.sleep(1)

            # Handle other potential dialogs
            for _ in range(3):  # Try up to 3 times
                if self.find_window_by_title("Error", timeout=1) or self.find_window_by_title("Warning", timeout=1):
                    logger.warning("Error or warning dialog detected - attempting to dismiss")
                    self.safe_press('enter')  # Try to dismiss dialog
                    time.sleep(0.5)

            # Verify the file was created
            if file_path.exists():
                logger.info(f"File verified at: {file_path}")
                return True
            else:
                logger.error(f"File was not created at: {file_path}")
                return False

        except Exception as e:
            logger.error(f"Exception during file saving process: {str(e)}")
            logger.debug(traceback.format_exc())
            return False

    def write_summary_report(self, posts, processed_posts, skipped_posts):
        """
        Write a summary report of the processing run

        Args:
            posts (list): All posts that were fetched
            processed_posts (list): IDs of successfully processed posts
            skipped_posts (list): IDs of skipped posts
        """
        try:
            summary_path = self.logs_path / f"summary_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"

            with open(summary_path, 'w') as f:
                f.write("=== NOTEPAD BOT SUMMARY REPORT ===\n\n")
                f.write(f"Date and Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total posts fetched: {len(posts)}\n")
                f.write(f"Posts processed: {len(processed_posts)}\n")
                f.write(f"Posts skipped: {len(skipped_posts)}\n\n")

                f.write("Processing success rate: {:.1f}%\n\n".format(
                    len(processed_posts) / (len(processed_posts) + len(skipped_posts)) * 100 if
                    (len(processed_posts) + len(skipped_posts)) > 0 else 0
                ))

                f.write("Processed post IDs:\n")
                for pid in processed_posts:
                    f.write(f"- Post {pid}\n")

                f.write("\nSkipped post IDs:\n")
                for pid in skipped_posts:
                    f.write(f"- Post {pid}\n")

                # Add system info
                f.write("\n=== SYSTEM INFORMATION ===\n")
                f.write(f"Python version: {sys.version}\n")
                f.write(f"PyAutoGUI version: {pyautogui.__version__}\n")
                f.write(f"PyGetWindow version: {gw.__version__}\n")

            logger.info(f"Summary report saved to {summary_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write summary report: {str(e)}")
            logger.debug(traceback.format_exc())
            return False

    def action(self, execution=None):
        """Main bot action method"""
        # Initialize directories
        if not self.initialize_directories():
            logger.critical("Failed to initialize directories, exiting")
            return

        # Fetch posts from the API
        posts = self.fetch_posts(limit=10)
        if not posts:
            logger.error("No posts to process, exiting")
            return

        # Track processed posts
        processed_posts = []
        skipped_posts = []

        # Set up pyautogui safety
        pyautogui.PAUSE = 0.1  # Add small pause between commands
        pyautogui.FAILSAFE = True  # Enable failsafe

        for post in tqdm(posts, desc="Processing posts", colour="green"):
            user_id = post["userId"]
            post_id = post["id"]
            title = post["title"]

            # Ask user if they want to save this post
            save_post = input(f"\nProcess post {post_id} with title: '{title}'? (y/n): ").strip().lower()
            if save_post != 'y':  # Fixed logical error
                logger.info(f"Skipping post {post_id}")
                skipped_posts.append(post_id)
                continue

            # Process the post
            success = self.process_post(post)
            if success:
                processed_posts.append(post_id)
            else:
                skipped_posts.append(post_id)

            # Small delay between iterations
            time.sleep(1)

        # Write summary report
        self.write_summary_report(posts, processed_posts, skipped_posts)

        # Print final summary to terminal
        logger.info("\n=== PROCESSING COMPLETE ===")
        logger.info(f"Total posts fetched: {len(posts)}")
        logger.info(f"Posts processed: {len(processed_posts)}")
        logger.info(f"Posts skipped: {len(skipped_posts)}")
        logger.info(f"Files saved to: {self.desktop_path}")
        logger.info(f"Logs directory: {self.logs_path}")


def main():
    try:
        print("\n=== Notepad Data Entry Bot ===")
        print("This script will fetch posts from JSONPlaceholder API and create text files in Notepad")
        print("You can choose which posts to process\n")

        # Check if required libraries are installed
        required_libraries = ["requests", "pyautogui", "pygetwindow", "botcity.core", "tqdm"]
        missing_libraries = []

        for lib in required_libraries:
            try:
                __import__(lib)
            except ImportError:
                missing_libraries.append(lib)

        if missing_libraries:
            print(f"ERROR: Missing required libraries: {', '.join(missing_libraries)}")
            print("Please install them using: pip install " + " ".join(missing_libraries))
            return

        # Initialize and run the bot
        bot = NotepadBot()
        bot.action()
    except Exception as e:
        print(f"Critical error: {str(e)}")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()