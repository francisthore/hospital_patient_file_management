#!/usr/bin/python3
"""Handles email sending"""
import requests
from flask import current_app, render_template, flash

def send_verification_email(to_address, subject, username,
                            verification_token):
    """Sends a verification email"""
    try:
        # Set the Mailgun API key and domain
        api_key = current_app.config.get('MAILGUN_API_KEY')
        domain = current_app.config.get('MAILGUN_DOMAIN')
        from_email = f"MTS Info <info@{domain}>"
        mailgun_api_url = f"https://api.mailgun.net/v3/{domain}/messages"
        rendered_html = render_template('email/verification_email.html',
                                        username=username,
                                        verification_token=verification_token)

        response = requests.post(
            mailgun_api_url,
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": to_address,
                "subject": subject,
                "html": rendered_html
            }
        )

        if response.status_code == 200:
            flash(f"Verification email sent to {to_address} successfully.", 'success')
        else:
            flash(f"Failed to send verification email to {to_address}. Status code: {response.status_code}, Response: {response.text}", 'danger')

    except Exception as e:
        flash(f"An error occurred while sending verification email to {to_address}", 'danger')

