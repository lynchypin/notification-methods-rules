# PagerDuty User Export Script

This script exports all PagerDuty users, their contact methods, and notification rules to a CSV file.

## How to Use

### 1. Download the Script

- Click on `pagerduty_export.py` in this repository.
- Click the **"Raw"** button, then right-click and choose **"Save As..."** to download the file to your computer.

### 2. Install Python Dependencies

Open a terminal and run:pip install requests pandas


~~### 3. Set Your PagerDuty API Key

Set your PagerDuty API key as an environment variable. In your terminal, run:

export PAGERDUTY_API_TOKEN=your_api_key_here~~


Replace `your_api_key_here` with your actual PagerDuty API key.

### 4. Run the Script

In your terminal, run:

python pagerduty_export.py


### 5. Find Your CSV

The script will create a file called `pagerduty_users.csv` on your Desktop.

---

**Note:**  
- If your Desktop is in a different location, edit the line in the script that sets `output_path`.
- Never share your PagerDuty API key publicly.
