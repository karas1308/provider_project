from environment import get_environment

# email_sender
email_sender = "ishchuka.mail.sender@gmail.com"
email_password = get_environment("EMAIL_PASSWORD")
email_receiver = "ishchuka.mail.sender@gmail.com"
subject = "Notification"
user_confirm_body = """
Your balance is {}. Please fund your balance. Services will be suspended in {} days.
"""
user_suspended_notif_body = """
Your balance is {}. Please fund your balance. Services is suspended.
"""
