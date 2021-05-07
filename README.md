# Covid-19 Vaccination Slot Notifier

Automatically sends an e-mail notification when a vaccination slot becomes available in a district

## Usage Instructions
1. Clone the repository and `cd` into the directory
    ```
    > git clone https://github.com/PercySpecter/covid-vaccination-slot-notifier.git
    ```
2. Install required dependencies
    ```
    > pip install -r requirements.txt
    ```
3. Run the script
    ```
    > python notifier.py <district_id> <age> <full path to recipients file>
    ```
    The recipients file contains the e-mail ids of the recipients to be notified, one in each line.
    
    For Example,
    ```
    > python notifier.py 725 22 recipients.txt
    ```
    Here `725` is the district ID of Kolkata, `22` is the age and `recipients.txt` contained the email ids of the notification recipients.
