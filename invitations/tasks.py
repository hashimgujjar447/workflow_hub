from celery import shared_task
import resend
from decouple import config

@shared_task(bind=True, max_retries=3)
def send_invite_email_task(self, to_email, invite_link, workspace_name):
    try:
        resend.api_key = config("RESEND_API_KEY")

    

        resend.Emails.send({
        "from": "WorkflowHub Team <noreply@workflowhub.me>",
        "to": [to_email],
        "subject": f"You're invited to join {workspace_name}",
        
        "html": f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px;">
            <h2>You're invited to join {workspace_name}</h2>

            <p>You have been invited to collaborate on <b>{workspace_name}</b>.</p>

            <p style="margin: 20px 0;">
                <a href="{invite_link}" 
                style="background:#2563eb;color:white;padding:12px 20px;
                        text-decoration:none;border-radius:6px;">
                    Accept Invitation
                </a>
            </p>

            <p>If you did not expect this email, you can safely ignore it.</p>

            <hr style="margin:20px 0;"/>

            <p style="font-size:12px;color:gray;">
                WorkflowHub • Team Collaboration Platform<br/>
                This email was sent automatically.
            </p>
        </div>
        """,

        "text": f"You are invited to join {workspace_name}. Open this link: {invite_link}",
        "reply_to": "support@workflowhub.me",
    })
    except Exception as e:
        raise self.retry(exc=e, countdown=10)