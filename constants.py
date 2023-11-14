from environment import get_environment

# email_sender
email_sender = "ishchuka.mail.sender@gmail.com"
email_password = get_environment("EMAIL_PASSWORD")
email_receiver = "ishchuka.mail.sender@gmail.com"
subject = "Notification"
user_confirm_body = """
Your balance is {}. Please fund your balance. Services will be suspended in {} days.
"""
user_subscribe_service_body = """
You subscribed {} service. Thank you for your choice.
"""
user_suspended_notif_body = """
Your balance is {}. Please fund your balance. Services is suspended.
"""
