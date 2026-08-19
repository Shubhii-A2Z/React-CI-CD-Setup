from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


def send_mail(workflow_name, repo_name, workflow_run_id):
  sender_email = os.getenv("SENDER_EMAIL")
  sender_password = os.getenv("SENDER_PASSWORD")
  receiver_email = os.getenv("RECEIVER_EMAIL")

  # Generate direct link to GitHub Actions log
  action_url = f"https://github.com/{repo_name}/actions/runs/{workflow_run_id}"

  # Email subject
  subject = f"🚨 ALERT: Workflow '{workflow_name}' FAILED on {repo_name}"

  # HTML Email Body with Inline CSS Styling
  html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border: 1px solid #e1e4e8;">
            
            <!-- Header Banner -->
            <div style="background-color: #cb2431; padding: 20px; text-align: center;">
                <h2 style="color: #ffffff; margin: 0; font-size: 20px; font-weight: 600;">
                    Workflow Execution Failed
                </h2>
            </div>
            
            <!-- Content Container -->
            <div style="padding: 24px; color: #24292e;">
                <p style="font-size: 15px; line-height: 1.5; margin-top: 0;">
                    Hello, <br>
                    The continuous integration pipeline encountered an error during execution.
                </p>
                
                <!-- Status Badge & Details Table -->
                <div style="background-color: #fafbfc; border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                        <tr>
                            <td style="padding: 8px 0; color: #586069; font-weight: 600; width: 130px;">Status:</td>
                            <td style="padding: 8px 0;">
                                <span style="background-color: #ffeef0; color: #d73a49; border: 1px solid rgba(215,58,73,0.4); padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px;">
                                    FAILED
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #586069; font-weight: 600;">Repository:</td>
                            <td style="padding: 8px 0; font-family: monospace; color: #0366d6;">{repo_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #586069; font-weight: 600;">Workflow:</td>
                            <td style="padding: 8px 0; font-weight: 500;">{workflow_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #586069; font-weight: 600;">Run ID:</td>
                            <td style="padding: 8px 0; font-family: monospace;">{workflow_run_id}</td>
                        </tr>
                    </table>
                </div>

                <!-- Action Button -->
                <div style="text-align: center; margin: 28px 0 12px 0;">
                    <a href="{action_url}" style="background-color: #2da44e; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 600; font-size: 14px; display: inline-block;">
                        View Failed Workflow Logs →
                    </a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f6f8fa; padding: 12px; text-align: center; border-top: 1px solid #e1e4e8; font-size: 12px; color: #6a737d;">
                Automated notification sent by GitHub Actions
            </div>
        </div>
    </body>
    </html>
    """

  msg = MIMEMultipart("alternative")
  msg["From"] = sender_email
  msg["To"] = receiver_email
  msg["Subject"] = subject

  # Attach as 'html' instead of 'plain'
  msg.attach(MIMEText(html_body, "html"))

  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
  except Exception as e:
    print(f"Error: {e}")


send_mail(
    os.getenv("WORKFLOW_NAME"),
    os.getenv("REPO_NAME"),
    os.getenv("WORKFLOW_RUN_ID"),
)