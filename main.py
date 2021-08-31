import requests
from datetime import datetime
import smtplib
import time



# You might need to update your email client's security preferences to allow for connections to "less secure apps".
# THIS IS NOT ADVISABLE IF YOU ARE NOT 100% SURE WHAT YOU ARE DOING!
# Host this anywhere (e.g. www.pythonanywhere.com) to be executed every hour and you will receive the notification :)

# Enter your mail address as a string for the MY_EMAIL global variable.
MY_EMAIL = "YOUR.EMAIL@ADDRESS"
# Enter your email password as a string for the MY_PASSWORD global variable.
MY_PASSWORD = "PASSWORD"

#  Enter your latitude as a float, you can get it from e.g. https://www.latlong.net
MY_LAT = 47.376888
#  Enter your longitude as a float, you can get it from e.g. https://www.latlong.net
MY_LONG = 8.541694


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # defining a margin of error for the position of the ISS, as it does not need to be directly overhead.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        # Enter your email on the next line again as a string, global variable won't work here.
        connection = smtplib.SMTP("EMAIL")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )
