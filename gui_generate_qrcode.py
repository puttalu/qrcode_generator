#import tkinter as Tk
from tkinter import (Tk, ttk, Label, Entry, StringVar, Frame, Button, Checkbutton, Radiobutton, IntVar, HORIZONTAL, filedialog)
import io
from PIL import Image, ImageTk
import segno
import os
import qrcode as qr


class QRGenerator(Tk):

    def __init__(self):
        super().__init__()
        self.initWindows()

    def initWindows(self):
        self.title("QR Code Generator")
        self.minsize(800, 800)
        self.geometry("400x350+50+50")
        self.config(border=20)
        self.qrwindow()

    def qrwindow(self):
        """Setup controls"""

        title = Label(self, text="QR Code Generator",
            font=('Calibri', 20), bd=10)
        title.pack()

        line = ttk.Separator(self, orient=HORIZONTAL)
        line.pack(fill='x')        

        self.input_label = Label(text="Text to encode: ")
        self.input_label.pack(anchor='w')


        self.txt_to_encode = StringVar()
        self.txt_to_encode.set('')
        self.input_entry = Entry(textvariable=self.txt_to_encode, width=60)
        self.input_entry.pack(anchor='w')
        

        self.rd_selected = IntVar()
        self.rd_selected.set(0)
        self.rd_options = ['QR Code', 'QR Code with Logo In Background', 'QR Code with Logo in the Middle']
        for ind, option in enumerate(self.rd_options):
            self.rd_button = Radiobutton(self, text=option, variable=self.rd_selected, value=ind)
            self.rd_button.pack(anchor='w')

        self.button_generateQR = Button(text='Generate QR Code', command=self.generateQRCode)
        self.button_generateQR.pack(anchor='w')

        self.label_select_bgfile = Label(text='')
        self.label_select_bgfile.pack(anchor='e')

        '''
        if(self.rd_selected != 0):
            self.label_select_bgfile = Label(text='abcd')
            self.button_select_bgfile = Button(text='Select Background Image', command=self.select_background)
            #self.generate_button_logo_in_middle = Button(text='Logo in Middle', command=logo_inthe_middle)
            #self.generate_button_logo_background = Button(text='Logo In Background', command=logo_background)
            if(self.rd_selected == 1):
                self.button_generateQR = Button(text='Generate QR Code', command=self.logo_background)
                self.button_generateQR.pack(anchor='w')
            else:
                self.button_generateQR = Button(text='Generate QR Code', command=self.logo_inthe_middle)
                self.button_generateQR.pack(anchor='w')
        else:
            self.button_generateQR = Button(text='Generate QR Code', command=self.qrcode_nologo)
            self.button_generateQR.pack(anchor='w')
        '''

        self.frame_code = Frame(width=500, height=500)
        self.frame_code.place(anchor='center', relx=0.5, rely=0.5)
        self.show_imgfile = Label(self.frame_code)


    def select_background(self):
        #self.label_select_bgfile.config(text='')
        self.bg_img = filedialog.askopenfilename(initialdir="./", 
                                            title="Select Background File", 
                                            filetypes=(("PNG Files","*.png*"), ("All Files","*.*")))
        
        #self.label_select_bgfile.config(text=self.bg_img)
        #return bg_img
    

    def generateQRCode(self):

        self.label_select_bgfile.config(text='')

        

        '''No Logo'''
        if(self.rd_selected.get() == 0):
            qr_code = qr.QRCode(error_correction=qr.constants.ERROR_CORRECT_L)
            qr_code.add_data(self.txt_to_encode.get())
            qr_code.make(fit=True)

            # Create image of QR code
            img = qr_code.make_image(fill_color="black", back_color="white")

            # Save image to file
            img.save('qrcode_nologo.png')
            self.show_qrcode('qrcode_nologo.png')

        
        elif(self.rd_selected.get() == 1):  #With Logo Inthe background'''
            qrcode = segno.make(self.txt_to_encode.get(), error='h')
            #out = io.BytesIO()
            #qrcode.to_artistic(background='./LinkedIn_logo_initials.png', target='./qrcode_with_background.png', scale=8)
            self.select_background()

            if(os.path.exists(self.bg_img)):
                qrcode.to_artistic(background=self.bg_img, target='./qrcode_with_background.png', scale=8)
                self.show_qrcode('qrcode_with_background.png')
            else:
                self.label_select_bgfile.config(text='Invalid Imagefile', fg='red')

        else:                       #With Logo Inthe Middle of the code'''
            #code_txt = txt_to_encode.get()
            out = io.BytesIO()
            # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
            qrcode = segno.make(self.txt_to_encode.get(), error='h').save(out, scale=8, kind='png')
            out.seek(0)  # Important to let Pillow load the PNG
            img = Image.open(out).convert('RGBA')
            #img = img.convert('RGBA')  # Ensure colors for the output

            img_width, img_height = img.size
            logo_max_size = img_height // 5  # May use a fixed value as well
            #logo_img = Image.open('./LinkedIn_logo_initials.png')  # The logo

            self.select_background()

            if(os.path.exists(self.bg_img)):
                logo_img = Image.open(self.bg_img)  # The logo
                # Resize the logo to logo_max_size
                logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                # Calculate the center of the QR code
                box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
                img.paste(logo_img, box)

                img.save('qrcode_logo_inthe_middle.png')

                self.show_qrcode('qrcode_logo_inthe_middle.png')
            else:
                self.label_select_bgfile.config(text='Invalid Imagefile', fg='red')



    def logo_background(self):
    
        qrcode = segno.make(self.txt_to_encode.get(), error='h')
        #out = io.BytesIO()
        #qrcode.to_artistic(background='./LinkedIn_logo_initials.png', target='./qrcode_with_background.png', scale=8)

        if(os.path.exists(self.bg_img)):
            qrcode.to_artistic(background=self.bg_img, target='./qrcode_with_background.png', scale=8)
            self.show_qrcode(self, 'qrcode_with_background.png')
        else:
            self.label_select_bgfile.config(text='Invalid Imagefile', fg='red')


    def logo_inthe_middle(self):
    
        #code_txt = txt_to_encode.get()
        out = io.BytesIO()
        # Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
        qrcode = segno.make(self.txt_to_encode.get(), error='h').save(out, scale=8, kind='png')
        out.seek(0)  # Important to let Pillow load the PNG
        img = Image.open(out).convert('RGBA')
        #img = img.convert('RGBA')  # Ensure colors for the output

        img_width, img_height = img.size
        logo_max_size = img_height // 5  # May use a fixed value as well
        #logo_img = Image.open('./LinkedIn_logo_initials.png')  # The logo

        if(os.path.exists(self.bg_img)):
            logo_img = Image.open(self.bg_img)  # The logo
            # Resize the logo to logo_max_size
            logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
            # Calculate the center of the QR code
            box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
            img.paste(logo_img, box)

            img.save('qrcode_logo_inthe_middle.png')

            self.show_qrcode(self, 'qrcode_logo_inthe_middle.png')
        else:
            self.label_select_bgfile.config(text='Invalid Imagefile', fg='red')


    def qrcode_nologo(self):
        qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr_code.add_data(self.txt_to_encode.get())
        qr_code.make(fit=True)

        # Create image of QR code
        img = qr_code.make_image(fill_color="black", back_color="white")

        # Save image to file
        img.save('qrcode_nologo.png')
        self.show_qrcode(self, 'qrcode_nologo.png')


    def show_qrcode(self, img_filename):
        img = ImageTk.PhotoImage(Image.open(img_filename))
        self.show_imgfile.config(image=img)
        self.show_imgfile.image = img
        self.show_imgfile.pack(anchor='center')


if  __name__  ==  "__main__":
    app = QRGenerator()
    app.mainloop()