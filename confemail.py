def sendemail(email, event_name, event_date, venue):
    ...
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          <h2 style="color: #4CAF50;">You're Invited!</h2>
          <p>Hello!</p>
          <p>Thank you for registering. Your event pass is attached below as a QR code. Please present it at the entrance.</p>
          <p><strong>Event:</strong> <span style="color:#555;">{event_name}</span></p>
          <p><strong>Date:</strong> <span style="color:#555;">{event_date}</span></p>
          <p><strong>Venue:</strong> <span style="color:#555;">{venue}</span></p>
          <p>We're excited to see you there!</p>
          <br>
          <p style="color:#888;">If you have any questions, reply to this email.</p>
        </div>
      </body>
    </html>
    """
    ...
