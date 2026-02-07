from emailer import send_email

def send_missed_potd_email(email, platform, scheduled_time, problem_url):
    subject = f"You missed today’s {platform.capitalize()} POTD"

    body = f"""
Hi,

Your system was offline at {scheduled_time}.

You missed today’s {platform.capitalize()} Problem of the Day.

Solve it here:
{problem_url}

Happy coding 🚀
from idea2deploy
"""

    send_email(email, subject, body)
