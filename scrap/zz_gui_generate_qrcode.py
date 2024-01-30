import io
from PIL import Image, ImageTk
import segno
import tkinter as tkinter
from tkinter import filedialog
import os
import qrcode as qr

window = tkinter.Tk()
txt_to_encode = tkinter.StringVar()
rb_selection = tkinter.StringVar(window, "1")
bg_logo = ''

def logo_inthe_middle():
    
    #code_txt = txt_to_encode.get()
    out = io.BytesIO()
    # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
    qrcode = segno.make(txt_to_encode.get(), error='h').save(out, scale=8, kind='png')
    out.seek(0)  # Important to let Pillow load the PNG
    img = Image.open(out).convert('RGBA')
    #img = img.convert('RGBA')  # Ensure colors for the output

    img_width, img_height = img.size
    logo_max_size = img_height // 5  # May use a fixed value as well
    #logo_img = Image.open('./LinkedIn_logo_initials.png')  # The logo

    if(os.path.exists(bg_logo)):
        logo_img = Image.open(bg_logo)  # The logo
        # Resize the logo to logo_max_size
        logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        # Calculate the center of the QR code
        box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
        img.paste(logo_img, box)

        img.save('qrcode_logo_inthe_middle.png')

        show_qrcode('qrcode_logo_inthe_middle.png')
    else:
        label_select_bgfile.config(text='Invalid Imagefile', fg='red')



def logo_background():
    
    qrcode = segno.make(txt_to_encode.get(), error='h')
    #out = io.BytesIO()
    #qrcode.to_artistic(background='./LinkedIn_logo_initials.png', target='./qrcode_with_background.png', scale=8)

    if(os.path.exists(bg_logo)):
        qrcode.to_artistic(background=bg_logo, target='./qrcode_with_background.png', scale=8)
        show_qrcode('qrcode_with_background.png')
    else:
        label_select_bgfile.config(text='Invalid Imagefile', fg='red')



def show_qrcode(img_filename):
    img = ImageTk.PhotoImage(Image.open(img_filename))
    show_imgfile.config(image=img)
    show_imgfile.image = img



def select_background():
    label_select_bgfile.config(text='')
    bg_img = filedialog.askopenfilename(initialdir="./", 
                                        title="Select Background File", 
                                        filetypes=(("PNG Files","*.png*"), ("All Files","*.*")))
    
    label_select_bgfile.config(text=bg_img)
    return bg_img



window.title("QR Code Generator")
window.geometry("800x800")
window.configure(borderwidth=30)


input_label = tkinter.Label(window, text="Text to encode: ")
input_entry = tkinter.Entry(window, textvariable=txt_to_encode, width=60)
label_select_bgfile = tkinter.Label(window, text='')

button_select_bgfile = tkinter.Button(text='Select Background Image', command=select_background)
generate_button_logo_in_middle = tkinter.Button(text='Logo in Middle', command=logo_inthe_middle)
generate_button_logo_background = tkinter.Button(text='Logo In Background', command=logo_background)


frame_rdbutton = tkinter.Frame(window, width=500, height=80)
frame_rdbutton.place(anchor='center', relx=0.5, rely=0.5)
radio_button1 = tkinter.Radiobutton(frame_rdbutton, text="QR Code", variable=rb_selection, value="1")
radio_button2 = tkinter.Radiobutton(frame_rdbutton, text="QR Code with Login in the middle", variable=rb_selection, value="2")
radio_button3 = tkinter.Radiobutton(frame_rdbutton, text="QR Code with Login in the background", variable=rb_selection, value="3")
show_rdbuttons = tkinter.Label(frame_rdbutton)

frame_code = tkinter.Frame(window, width=500, height=500)
frame_code.place(anchor='center', relx=0.5, rely=0.5)
show_imgfile = tkinter.Label(frame_code)

#command=logo_inthe_middle(txt_to_encode.get())

input_label.grid(row=0, column=0, padx=20)
input_entry.grid(row=0, column=1, padx=20)



show_rdbuttons.grid(row=0, column=2)

button_select_bgfile.grid(row=2, column=1, padx=20, pady=10)
label_select_bgfile.grid(row=3, column=1, padx=20)

generate_button_logo_in_middle.grid(row=4, column=1, padx=1, pady=10)
generate_button_logo_background.grid(row=5, column=1, padx=1, pady=10)

#rdbutton.grid(row=5, column=1)

show_imgfile.grid(row=6, column=1)


window.mainloop()


"""

def main():
    #logo_background()
    logo_inthe_middle()


if __name__ == '__main__':
        main()

"""