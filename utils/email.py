from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_invite_email(to_email, invite_link, workspace_name):
    try:
        subject = f"You are invited to join {workspace_name}"

        text_content = f"""
        You have been invited to join {workspace_name}.
        Click the link below to join:
        {invite_link}
        """

        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>You're invited 🎉</h2>
            <p>You have been invited to join <b>{workspace_name}</b></p>
            
            <a href="{invite_link}" 
               style="
                display:inline-block;
                padding:10px 20px;
                background:#2563eb;
                color:white;
                border-radius:6px;
                text-decoration:none;
                margin-top:10px;
               ">
                Join Workspace
            </a>

            <p style="margin-top:20px;font-size:12px;color:gray;">
                If you didn’t expect this, you can ignore this email.
            </p>
        </div>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"✅ Invite email sent to {to_email}")

        return True

    except Exception as e:
        logger.error(f"❌ Email failed: {str(e)}")
        return False