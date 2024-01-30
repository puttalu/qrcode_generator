import qrcode

filename = ""

# Function to generate and save QR code
def generate_qr(data, filename="qrcode.png"):
  """
  Generates a QR code from the given data and saves it as an image.

  Args:
    data: The data to encode in the QR code.
    filename: The filename (including extension) to save the QR code as.

  Returns:
    None
  """
  # Create QR code object
  qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
  qr_code.add_data(data)
  qr_code.make(fit=True)

  # Create image of QR code
  img = qr_code.make_image(fill_color="black", back_color="white")

  # Save image to file
  img.save(filename)


# Get input from user
data = input("Enter the data you want to encode in the QR code: ")

# Generate and save QR code
generate_qr(data)

print(f"QR code generated and saved as '{filename}'.")
