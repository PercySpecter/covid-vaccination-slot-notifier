import sys
import time
import requests
import datetime

import Algorithmia

def notify_free_slot(recipients, message):
    input = {
        "recipients": recipients,
        "slots": message
    }

    client = Algorithmia.client('simOdJdArOcSvyWc/P4vMcH4li61')
    algo = client.algo('percys/mail_notifier/1.0.1')
    algo.set_options(timeout=300)

    print(algo.pipe(input).result)


def find_free_slots(start_date, district_id, age=45):
    headers = {
        "Content-Type": "application/json",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.259"
    }

    slot_query_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_id, start_date)

    r = requests.get(url=slot_query_url, headers=headers)

    data = r.json()

    centers = []
    for center in data["centers"]:
        sessions = []
        for session in center["sessions"]:
            # if session["min_age_limit"] <= age:
            if session["available_capacity"] > 0 and session["min_age_limit"] <= age:
                tmp_session = {
                    "Date": session["date"],
                    "Available Capacity": session["available_capacity"],
                    "Minimum Age Limit": session["min_age_limit"],
                    "Vaccine": session["vaccine"]
                }
                sessions.append(tmp_session)
        
        if sessions:
            tmp_center = {
                "Name": center["name"],
                "Address": center["address"],
                "Pincode": center["pincode"],
                "Slots": sessions
            }
            centers.append(tmp_center)

    return centers


def parse_sessions(sessions):
    msg = ""
    
    for session in sessions:
        msg += "Date: {} | Available Capacity: {} | Minimum Age Limit: {} | Vaccine: {}\n".format(session["Date"], session["Available Capacity"], session["Minimum Age Limit"], session["Vaccine"])

    return msg

def form_notification_message(free_slots):
    message = []

    for center in free_slots:
        msg = "Center: {}\n{}\nPincode: {}\n Slots:\n{}\n".format(center["Name"], center["Address"], center["Pincode"], parse_sessions(center["Slots"]))
        message.append(msg)
        message.append("-" * 70)

    return message


def get_recipients(recipients_file_path):
    with open(recipients_file_path, "r") as f:
        emails = f.readlines()
        return [email.strip() for email in emails]


if __name__=="__main__":
    district_id = int(sys.argv[1])
    age = int(sys.argv[2])
    recipients_file_path = sys.argv[3]

    recipients = get_recipients(recipients_file_path)

    today = datetime.date.today()
    week1 = today.strftime("%d-%m-%Y")
    week2 = (today + datetime.timedelta(days=7)).strftime("%d-%m-%Y")
    week3 = (today + datetime.timedelta(days=14)).strftime("%d-%m-%Y")
    week4 = (today + datetime.timedelta(days=28)).strftime("%d-%m-%Y")

    # print(week1, week2, week3, week4)

    while True:
        try:
            slots = find_free_slots(week1, district_id, age)
            slots.extend(find_free_slots(week2, district_id, age))
            slots.extend(find_free_slots(week3, district_id, age))
            slots.extend(find_free_slots(week4, district_id, age))
            print(slots)
            if slots:
                notify_free_slot(recipients, form_notification_message(slots))
                break
        except:
            print("Error fetching Vaccination Information")
        time.sleep(10)
