# Automated Data Entry Bot for Desktop Application


## Project Overview
This project automates data entry into Notepad using **Python**, **BotCity**, and **PyAutoGUI**. The script fetches blog posts from the **JSONPlaceholder API**, types them into Notepad, and saves them with specific filenames.

---
## Features
| Feature | Description |
|---------|-------------|
| **Fetches** blog posts from the [JSONPlaceholder API](https://jsonplaceholder.typicode.com/guide/) | Fetches blog posts from the JSONPlaceholder API |
| **Automates** Notepad to create and save documents | Automates Notepad to create and save documents |
| **Loops** through the first 10 posts | Loops through the first 10 posts |
| **Handles errors** such as application failures | Handles errors such as application failures |

---

## Requirements
### 1. Setup
| Step | Description | progress |
|------|-------------|-------------|
| Install **Python** and create a virtual environment | Install Python and create a virtual environment |
| Install **BotCity** and **PyAutoGUI** | Install BotCity and PyAutoGUI |
| Ensure **Notepad** is installed on your system | Ensure Notepad is installed on your system |

### 2. Automation Tasks
| Task | Description | progress |
|------|-------------|----------|
| **Launch Notepad** using Python | Launch Notepad using Python |
| **Fetch Posts** from JSONPlaceholder API | Fetch Posts from JSONPlaceholder API |
| **Type each post** as a formatted blog entry | Type each post as a formatted blog entry |
| Include a **title** and **body** | Include a title and body |
| **Save the document** in `tjm-project` on the desktop | Save the document in `tjm-project` on the desktop |
| Filename format: `post_<id>.txt` | Filename format: `post_<id>.txt` |
| Example: `post_1.txt`, `post_2.txt`, ..., `post_10.txt` | Example: `post_1.txt`, `post_2.txt`, ..., `post_10.txt` |

### 3. Error Handling
| Error Handling | Description | progress |
|----------------|-------------|-------------|
| Ensure **Notepad opens correctly** | Ensure Notepad opens correctly | 
| Handle **missing UI elements** | Handle missing UI elements |
| Validate **API response** | Validate API response |

### 4. Discussion Points
| Discussion Point | Description |
|------------------|-------------|
| Technical choices: Why **BotCity & PyAutoGUI**? | Technical choices: Why BotCity & PyAutoGUI? |
| Limitations and possible improvements | Limitations and possible improvements |

---

## Installation
### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd automated-data-entry-bot
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run the Script
```bash
python main.py
```

---

## Folder Structure
```
/automated-data-entry-bot
│── main.py  # Main automation script
│── README.md  # Project documentation
│── requirements.txt  # Dependencies
│── /tjm-project  # Directory for saved files
```

---

## Example Output
**post_1.txt** (Example)
```
Title: Sample Blog Post

This is a test post from JSONPlaceholder.
```

---

## Troubleshooting
- **Notepad doesn’t open?** Check if `notepad.exe` exists.
- **Posts not saving?** Verify write permissions on the desktop.
- **Typing issues?** Ensure PyAutoGUI is installed correctly.


---

## Author
Developed by [Your Name].



