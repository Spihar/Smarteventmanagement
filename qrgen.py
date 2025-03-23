import qrcode
from PIL import Image

qr = qrcode.QRCode(
    version=1,  # Controls size of the QR Code (1 = 21x21)
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "name"
qr.add_data(data)
qr.make(fit=True)

# Customize colors
img = qr.make_image(fill_color="black", back_color="white")

img.save("StyledQRCode.png")
img.show()

