import smtplib
import ssl
from email.message import EmailMessage
import MySQLdb
from database import get_connection

def sendemail(email):
    email_sender = 'interstellar.teamhack@gmail.com'
    email_password = 'cpoyinoslifitcxc'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("")
    email_receiver = email

    # File name of the QR code
    qr_code_file = 'StyledQRCode.png'  # or whatever your filename is

    # Create the EmailMessage object
    msg = EmailMessage()
    msg['Subject'] = '🎟️ Your Entry Pass – Event Name Here'
    msg['From'] = email_sender
    msg['To'] = ', '.join(email_receiver)

    # Set both plain text and HTML content (fallback for non-HTML readers)
    msg.set_content('Hi there,\nYour event pass is attached as a QR code. Please show it at the entrance.\n\nThanks!')

    # HTML body for prettier formatting
    html = """
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          <h2 style="color: #4CAF50;">You're Invited! 🎉</h2>
          <p>Hello!</p>
          <p>Thank you for registering. Your event pass is attached below as a QR code. Please present it at the entrance to gain access to the event.</p>
          <p><strong>Event:</strong> <span style="color:#555;">Interstellar Innovation Hackathon</span></p>
          <p><strong>Date:</strong> <span style="color:#555;">March 25, 2025</span></p>
          <p><strong>Venue:</strong> <span style="color:#555;">CygnusX1 Campus Auditorium</span></p>
          <p>We're excited to see you there!</p>
          <br>
          <p style="color:#888;">If you have any questions, reply to this email.</p>
        </div>
      </body>
    </html>
    """

    msg.add_alternative(html, subtype='html')

    # Attach the QR code image
    with open(qr_code_file, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=qr_code_file)

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)

    print("Event email sent successfully!")
