import smtplib
from email.message import EmailMessage
import os

# Load environment variables from credentials.env if it exists
credentials_path = os.path.join(os.path.dirname(__file__), "credentials.env")
if os.path.exists(credentials_path):
    with open(credentials_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                # Strip spaces and quotes
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

email = os.environ.get("SMTP_EMAIL", "pratap.vijay.singh.in@gmail.com")
reciever = os.environ.get("SMTP_RECEIVER", "goforsomethingelse@gmail.com")
app_pass = os.environ.get("SMTP_APP_PASSWORD", "sjipipaepuuqzmzd")


def contact_query_fetcher():
    from models import ContactQuery
    from app import app
    with app.app_context():
        latest_query = ContactQuery.query.order_by(ContactQuery.id.desc()).first()
        return latest_query

def html_email_writer(query_data):

    if not query_data:
        return "<p>No query data available.</p>"
        
    created_time = query_data.created_at.strftime('%Y-%m-%d %H:%M:%S') if query_data.created_at else 'N/A'
    phone_val = query_data.phone if query_data.phone else 'Not Provided'
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333333; margin: 0; padding: 20px; }}
    .email-container {{ max-width: 600px; background-color: #ffffff; margin: 0 auto; border-radius: 12px; border: 1px solid #e1e8ed; overflow: hidden; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); }}
    .email-header {{ background-color: #0b2545; color: #ffffff; padding: 24px; text-align: center; }}
    .email-header h1 {{ margin: 0; font-size: 22px; font-weight: 600; }}
    .email-body {{ padding: 30px; line-height: 1.6; }}
    .email-body h2 {{ font-size: 18px; color: #0b2545; margin-top: 0; margin-bottom: 20px; border-bottom: 2px solid #c9a84c; padding-bottom: 8px; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
    .info-table td {{ padding: 10px 0; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
    .info-table td.label {{ font-weight: 600; color: #64748b; width: 30%; }}
    .info-table td.value {{ color: #1e293b; width: 70%; }}
    .message-box {{ background-color: #f8fafc; border-left: 4px solid #c9a84c; padding: 15px; border-radius: 4px; margin-top: 10px; font-style: italic; color: #334155; white-space: pre-wrap; }}
    .email-footer {{ background-color: #f1f5f9; padding: 20px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="email-header">
      <h1>St. Xavier's High School</h1>
    </div>
    <div class="email-body">
      <h2>New Query Received</h2>
      <p>Hello Administrator,</p>
      <p>A new query has been submitted via the school website's contact form. Below are the details:</p>
      
      <table class="info-table">
        <tr>
          <td class="label">Name:</td>
          <td class="value">{query_data.first_name} {query_data.last_name}</td>
        </tr>
        <tr>
          <td class="label">Email:</td>
          <td class="value"><a href="mailto:{query_data.email}" style="color: #134074; text-decoration: none;">{query_data.email}</a></td>
        </tr>
        <tr>
          <td class="label">Phone:</td>
          <td class="value">{phone_val}</td>
        </tr>
        <tr>
          <td class="label">Subject:</td>
          <td class="value" style="text-transform: capitalize;">{query_data.subject}</td>
        </tr>
        <tr>
          <td class="label">Date/Time:</td>
          <td class="value">{created_time}</td>
        </tr>
      </table>
      
      <strong>Message:</strong>
      <div class="message-box">{query_data.message}</div>
    </div>
    <div class="email-footer">
      <p>This is an automated notification. Please do not reply directly to this email.</p>
      <p>&copy; 2026 St. Xavier's High School. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""
    return html_content

def html_email_fetcher():
    data = contact_query_fetcher()
    if not data:
        return None
    
    html_content = html_email_writer(data)
    
    msg = EmailMessage()
    msg['Subject'] = f"New Enquiry: {data.subject.capitalize()}"
    msg['From'] = email
    msg['To'] = reciever
    
    msg.set_content("Please use an HTML-compatible email client to read this message.")
    msg.add_alternative(html_content, subtype='html')
    return msg

def email_sender(email, reciever, msg):
    if not msg:
        print("No email message to send.")
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email, app_pass)
            server.send_message(msg)
            return None
    except Exception as e:
        return f"Failed to send email. Error: {e}"

def admission_query_fetcher():
    from models import AdmissionQuery
    from app import app
    with app.app_context():
        latest_query = AdmissionQuery.query.order_by(AdmissionQuery.id.desc()).first()
        return latest_query


def html_admission_email_writer(query_data):
    if not query_data:
        return "<p>No admission query data available.</p>"
        
    created_time = query_data.created_at.strftime('%Y-%m-%d %H:%M:%S') if query_data.created_at else 'N/A'
    phone_val = query_data.phone if query_data.phone else 'Not Provided'
    prev_school_val = query_data.prev_school if query_data.prev_school else 'None / Not Provided'
    message_val = query_data.message if query_data.message else 'No message'
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333333; margin: 0; padding: 20px; }}
    .email-container {{ max-width: 600px; background-color: #ffffff; margin: 0 auto; border-radius: 12px; border: 1px solid #e1e8ed; overflow: hidden; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); }}
    .email-header {{ background-color: #134074; color: #ffffff; padding: 24px; text-align: center; }}
    .email-header h1 {{ margin: 0; font-size: 22px; font-weight: 600; }}
    .email-body {{ padding: 30px; line-height: 1.6; }}
    .email-body h2 {{ font-size: 18px; color: #134074; margin-top: 0; margin-bottom: 20px; border-bottom: 2px solid #c9a84c; padding-bottom: 8px; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
    .info-table td {{ padding: 10px 0; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
    .info-table td.label {{ font-weight: 600; color: #64748b; width: 35%; }}
    .info-table td.value {{ color: #1e293b; width: 65%; }}
    .message-box {{ background-color: #f8fafc; border-left: 4px solid #c9a84c; padding: 15px; border-radius: 4px; margin-top: 10px; font-style: italic; color: #334155; white-space: pre-wrap; }}
    .email-footer {{ background-color: #f1f5f9; padding: 20px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="email-header">
      <h1>St. Xavier's High School</h1>
    </div>
    <div class="email-body">
      <h2>New Admission Inquiry Received</h2>
      <p>Hello Administrator,</p>
      <p>A new admission application/inquiry has been submitted. Below are the details:</p>
      
      <table class="info-table">
        <tr>
          <td class="label">Applicant Name:</td>
          <td class="value">{query_data.first_name} {query_data.last_name}</td>
        </tr>
        <tr>
          <td class="label">Date of Birth:</td>
          <td class="value">{query_data.dob}</td>
        </tr>
        <tr>
          <td class="label">Class Applying For:</td>
          <td class="value" style="font-weight: bold; color: #134074;">{query_data.class_applying}</td>
        </tr>
        <tr>
          <td class="label">Parent/Guardian Name:</td>
          <td class="value">{query_data.parent_name} ({query_data.relationship})</td>
        </tr>
        <tr>
          <td class="label">Email:</td>
          <td class="value"><a href="mailto:{query_data.email}" style="color: #134074; text-decoration: none;">{query_data.email}</a></td>
        </tr>
        <tr>
          <td class="label">Phone:</td>
          <td class="value">{phone_val}</td>
        </tr>
        <tr>
          <td class="label">Previous School:</td>
          <td class="value">{prev_school_val}</td>
        </tr>
        <tr>
          <td class="label">Date/Time:</td>
          <td class="value">{created_time}</td>
        </tr>
      </table>
      
      <strong>Additional Message/Note:</strong>
      <div class="message-box">{message_val}</div>
    </div>
    <div class="email-footer">
      <p>This is an automated notification. Please do not reply directly to this email.</p>
      <p>&copy; 2026 St. Xavier's High School. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""
    return html_content


def html_admission_email_fetcher():
    data = admission_query_fetcher()
    if not data:
        return None
    
    html_content = html_admission_email_writer(data)
    
    msg = EmailMessage()
    msg['Subject'] = f"New Admission Inquiry: {data.first_name} {data.last_name} - Class {data.class_applying}"
    msg['From'] = email
    msg['To'] = reciever
    
    msg.set_content("Please use an HTML-compatible email client to read this message.")
    msg.add_alternative(html_content, subtype='html')
    return msg


# if __name__ == '__main__':
#     msg = html_email_fetcher()
#     email_sender(email, reciever, msg)

# server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
# server.ehlo()
# server.starttls()
# server.ehlo
# server.login(email, app_pass)
# server.sendmail(email, reciever, message)