
from datetime import date

from django.core.mail import send_mail
from django.conf import settings

from .models import Users, Child, vaccine_information


# ---------------------------------------------------
# Store already sent notifications
# ---------------------------------------------------

sent_notifications = set()


# ---------------------------------------------------
# Calculate age from Date of Birth
# ---------------------------------------------------

def calculate_age(dob):

    today = date.today()

    age = today.year - dob.year

    # If birthday has not occurred this year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


# ---------------------------------------------------
# Send Vaccine Email
# ---------------------------------------------------

def send_vaccine_email(email, name, vaccine):

    subject = "Vaccine Reminder - VaxiCare"

    message = f"""
Hello {name},

This is a vaccine reminder from VaxiCare.

Your age matches the recommended age for the following vaccine.

Vaccine Name: {vaccine.Vaccinename}

Recommended Age: {vaccine.Age} years

Dose Number: {vaccine.Dose_number}

Description:
{vaccine.Description}

Possible Side Effects:
{vaccine.Side_effect}

Manufacturer:
{vaccine.Manufacture}

Please consult a healthcare professional for vaccination.

Thank you,
VaxiCare
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )


# ---------------------------------------------------
# Check Vaccines for Registered Users
# ---------------------------------------------------

def check_user_vaccines():

    vaccines = vaccine_information.objects.all()

    users = Users.objects.all()

    for user in users:

        # Check DOB
        if not user.Dob:
            continue

        # Check email
        if not user.email:
            continue

        # Calculate current age
        age = calculate_age(user.Dob)

        print(
            f"Checking user: {user.name} | Age: {age}"
        )

        # Check every vaccine
        for vaccine in vaccines:

            # Match user age with vaccine age
            if age == vaccine.Age:

                # Unique ID for this user and vaccine
                notification_id = (
                    "user",
                    user.AUTHUSER.id,
                    vaccine.id
                )

                # Check whether email was already sent
                if notification_id not in sent_notifications:

                    try:

                        send_vaccine_email(
                            user.email,
                            user.name,
                            vaccine
                        )

                        # Remember this notification
                        sent_notifications.add(
                            notification_id
                        )

                        print(
                            f"Email sent to {user.email} "
                            f"for {vaccine.Vaccinename}"
                        )

                    except Exception as e:

                        print(
                            f"Email failed for {user.email}: {e}"
                        )


# ---------------------------------------------------
# Check Vaccines for Children
# ---------------------------------------------------

def check_child_vaccines():

    vaccines = vaccine_information.objects.all()

    # Get child and related parent/user
    children = Child.objects.select_related("USER").all()

    for child in children:

        # Check DOB
        if not child.Dob:
            continue

        # Get parent/user
        parent = child.USER

        # Parent email
        if not parent.email:
            continue

        # Calculate child's age
        age = calculate_age(child.Dob)

        print(
            f"Checking child: {child.Name} | Age: {age}"
        )

        # Check every vaccine
        for vaccine in vaccines:

            # Match child's age with vaccine age
            if age == vaccine.Age:

                # Unique ID for child and vaccine
                notification_id = (
                    "child",
                    child.id,
                    vaccine.id
                )

                # Check whether already sent
                if notification_id not in sent_notifications:

                    try:

                        send_vaccine_email(
                            parent.email,
                            child.Name,
                            vaccine
                        )

                        # Remember this notification
                        sent_notifications.add(
                            notification_id
                        )

                        print(
                            f"Child vaccine email sent to "
                            f"{parent.email} "
                            f"for {child.Name} - "
                            f"{vaccine.Vaccinename}"
                        )

                    except Exception as e:

                        print(
                            f"Child email failed for "
                            f"{parent.email}: {e}"
                        )


# ---------------------------------------------------
# Main Notification Function
# ---------------------------------------------------

def check_all_notifications():

    print("----------------------------------------")
    print("VaxiCare Vaccine Notification Checking")
    print("----------------------------------------")

    # Check registered users
    check_user_vaccines()

    # Check children
    check_child_vaccines()

    print("----------------------------------------")
    print("Notification checking completed")
    print("----------------------------------------")
