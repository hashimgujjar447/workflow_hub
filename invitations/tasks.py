from celery import shared_task
import resend
from decouple import config

@shared_task(bind=True, max_retries=3)
def send_invite_email_task(self, to_email, invite_link, workspace_name):
    try:
        resend.api_key = config("RESEND_API_KEY")

        subject = f"You are invited to join {workspace_name}"

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

        resend.Emails.send({
            "from": "WorkflowHub Team <noreply@workflowhub.me>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        })

    except Exception as e:
        raise self.retry(exc=e, countdown=10)