# Automated Data Entry Bot for Desktop Application


## Project Overview
This project automates data entry into Notepad using **Python**, **BotCity**, and **PyAutoGUI**. The script fetches blog posts from the **JSONPlaceholder API**, types them into Notepad, and saves them with specific filenames.

---
## Features
## Project Requirements & Progress Tracking

| Task ID | Category | Description | Status | Tag |
|---------|----------|-------------|---------|-----|
| S1 | Setup | Install **Python** and create a virtual environment | ✅ Done | #environment |
| S2 | Setup | Install **BotCity** and **PyAutoGUI** | ✅ Done | #dependencies |
| S3 | Setup | Ensure **Notepad** is installed on system | ✅ Done | #system |
| A1 | Automation | **Launch Notepad** using Python | ✅ Done | #automation |
| A2 | Automation | **Fetch Posts** from JSONPlaceholder API | ✅ Done | #api |
| A3 | Automation | **Type each post** as formatted blog entry | ✅ Done | #content |
| A4 | Automation | Include **title** and **body** | ✅ Done | #formatting |
| A5 | Automation | **Save document** in `tjm-project` on desktop | ✅ Done | #files |
| A6 | Automation | Use filename format `post_<id>.txt` | ✅ Done | #naming |
| E1 | Error Handling | Ensure **Notepad opens correctly** | 🚧 In Progress | #validation |
| E2 | Error Handling | Handle **missing UI elements** | 🚧 In Progress | #errors |
| E3 | Error Handling | Validate **API response** | ✅ Done | #api |
| D1 | Discussion | Technical choices: **BotCity & PyAutoGUI** | ✅ Done | #architecture |
| D2 | Discussion | Limitations and improvements | 🚧 In Progress | #improvements |
---

## Installation
### Step 1: Clone the Repository
```bash
git clone https://github.com/Ahmed-El-Zainy/auto_data_entry_descktop_application.git
cd automated-data-entry-bot
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

or 

```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Run the Script
```bash
python main.py
```

---

## Folder Structure
```
/automated-data-entry-bot
│── src
    │──logger
        │──logger.py
        │──logging_config.yaml
    │──tests
        │──unittest_main.py
    │──utlities.py

│── main.py  # Main automation script
│── README.md  # Project documentation
│── requirements.txt  # Dependencies
│── setup.sh  # Setup script
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



