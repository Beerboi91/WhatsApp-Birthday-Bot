import pandas as pd
import datetime
import pywhatkit
import os

def send_birthday_messages():
    today = datetime.date.today()
    
    # Read data from GitHub repository (file path will be relative in the repo)
    try:
        df = pd.read_excel('schedule.xlsx')
    except FileNotFoundError:
        print("Error: schedule.xlsx file not found")
        return

    for _, row in df.iterrows():
        birthday = pd.to_datetime(row['Birthday']).date()
        
        # Check if today is their birthday
        if birthday.day == today.day and birthday.month == today.month:
            message = row['Nachricht']
            phone_number = os.getenv('WHATSAPP_PHONE_NUMBER')  # Get from GitHub secrets
            
            if not phone_number:
                print("Error: WhatsApp phone number not configured")
                continue

            # Schedule message to send 1 minute from now
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 1

            print(f"Attempting to send message to {row['Name']} at {hour}:{minute}...")
            try:
                pywhatkit.sendwhatmsg(
                    phone_number, 
                    message, 
                    hour, 
                    minute, 
                    wait_time=10, 
                    tab_close=True
                )
                print(f"Message sent successfully to {row['Name']}")
            except Exception as e:
                print(f"Failed to send message to {row['Name']}: {str(e)}")

if __name__ == "__main__":
    send_birthday_messages()
