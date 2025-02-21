import pywhatkit as kit
import time
import re
import pandas as pd

# اي اشي مكتوب زي هيك هو بس تعليق عشان يساعدكم بقراءة الكود و ما بأثر على شغله
def format_number(number):
    number = str(number).strip()
    if re.match(r"^079\d{7}$", number):
        return "+962" + number[1:]
    elif re.match(r"^79\d{7}$", number):
        return "+962" + number
    elif re.match(r"^\+962\d{8,9}$", number):
        return number
    else:
        raise ValueError(f"Invalid phone number format: {number}")

# هان بتحطو اسم الفايل اللي مخزنين فيه الداتا
dataset = pd.read_csv('جدول بيانات بدون عنوان - الورقة1 (1).csv')

# هان بدلوهم باسم الصف او العمود اللي عندكم
names = dataset['الاسم'].values
numbers = dataset['الرقم'].values

formatted_numbers = [format_number(num) for num in numbers]

# هان بتحطو الرسالة اللي بدكم اياها بهذا الفورمات
message_template = "Hello {name}, this is a test message from an automated script!"

failed_numbers = []

for name, number in zip(names, formatted_numbers):
    try:
        message = message_template.format(name=name)  # Customize the message
        kit.sendwhatmsg_instantly(number, message, 20, tab_close=True)  # Sends instantly
        print(f"Message sent to {name} ({number})")

    except Exception as e:
        print(f"Failed to send message to {name} ({number}): {e}")
        failed_numbers.append(number)
    time.sleep(2)

if failed_numbers:
    print("\nFailed to send messages to the following numbers:")
    for number in failed_numbers:
        print(number)
else:
    print("\nAll messages were sent successfully!")
