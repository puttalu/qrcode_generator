import io
from PIL import Image
import segno


def logo_inthe_middle():
    out = io.BytesIO()
    # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
    qrcode = segno.make('https://www.linkedin.com/in/ravindran-arun/', error='h').save(out, scale=8, kind='png')
    out.seek(0)  # Important to let Pillow load the PNG
    img = Image.open(out).convert('RGBA')
    #img = img.convert('RGBA')  # Ensure colors for the output

    img_width, img_height = img.size
    logo_max_size = img_height // 5  # May use a fixed value as well
    logo_img = Image.open('./LinkedIn_logo_initials.png')  # The logo

    # Resize the logo to logo_max_size
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    # Calculate the center of the QR code
    box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box)
    img.save('qrcode_logo_inthe_middle.png')


def logo_background():
    
    qrcode = segno.make('https://www.linkedin.com/in/ravindran-arun/', error='h')
    #out = io.BytesIO()
    qrcode.to_artistic(background='./LinkedIn_logo_initials.png', target='./qrcode_with_background.png', scale=8)



def main():
    #logo_background()
    logo_inthe_middle()


if __name__ == '__main__':
        main()