# City of Brampton Automation

This automation tool is designed to streamline the process of adding new fees and removing outdated fees from the City of Brampton's Xplor Software. It logs all changes (added and deleted fees) to a CSV file for easy tracking and reference.

## Features
* Automates the addition of new fees
* Removes outdated fees from the system
* Logs all changes (added and deleted fees) in a CSV file

## Quickstart
1. Download the `requirements.txt` file from the repository.
2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt

## Setup Instructions
1. Set the `TEST` constant variable to `true` or `false`
2. Log in to the Xplor Software platform.
3. Navigate to the "Manage Facilities" section.
4. Follow the prompts in the terminal to complete the process.
5. Press `ENTER` to begin the automation process.

## Additional Notes:
* Ensure you have the necessary permissions to add or delete fees within Xplor Software.
* - The tool will generate a CSV file that logs all the fees that were added or deleted.
* Testing mode is recommended to ensure the tool operates as expected before making any changes to production.
