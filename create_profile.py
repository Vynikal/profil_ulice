import os
from PIL import Image, ImageDraw, ImageFont
from random import randint

path = os.path.dirname(__file__)
length = 2800
meritko = 100  # 1 cm = 1 pixel

class Street:
    def __init__(self, sirka = 4, mhd = 1, cyklo = 1, jednosmerka = 0):
        self.sirka = sirka*meritko
        self.mhd = mhd
        self.cyklo = cyklo
        self.jednosmerka = jednosmerka

    def create_profile(self):
        # load images
        street = Image.open(os.path.join(path, 'im/street.png'))
        white = Image.open(os.path.join(path, 'im/white.png'))
        car = Image.open(os.path.join(path, 'im/car.png'))
        bicycle = Image.open(os.path.join(path, 'im/bicycle.png'))
        bus = Image.open(os.path.join(path, 'im/bus.png'))
        treebig = Image.open(os.path.join(path, 'im/treebig.png'))
        treesmall = Image.open(os.path.join(path, 'im/treesmall.png'))
        ped1 = Image.open(os.path.join(path, 'im/ped1.png'))
        ped2 = Image.open(os.path.join(path, 'im/ped2.png'))
        ped3 = Image.open(os.path.join(path, 'im/ped3.png'))
        ped4 = Image.open(os.path.join(path, 'im/ped4.png'))

        # dimension definition
        width = int(self.sirka)
        top = street.resize((width, length))
        if width < 600:
            self.pastem(top,car,width*2//3,2000)
            self.pastem(top,car,width*2//3,500)
            self.pastem(top,bicycle,width*3//4,1000)
            self.pastem(top,bicycle.rotate(180),width//4,1500)
            self.pastem(top,ped1.rotate(randint(0,360)),width-50,randint(100,length-100))
            self.pastem(top,ped3.rotate(randint(0,360)),50,randint(100,length-100))
            hspec = (0,width)
            vspec = (0,length)

        # elif width >= 600 & width < 800:
        #     self.

        # koty
        all = white.resize((width+200,length+200))
        all.paste(top,(100,100),top)
        self.hkota(all)
        self.hkota(all, hspec)
        self.vkota(all, vspec)

        all.save(os.path.join(path, 'im/profil.png'))
        all.show()

    def hkota(self, image, sec=None):
        koty = ImageDraw.Draw(image)
        red = (255,0,0)

        if sec == None:
            width = self.sirka
            sec = (0, width)
            l = -100
        else:
            l = length

        for i in range(len(sec)-1):
            koty.line((sec[i]+100,l+150) + (sec[i+1]+100,l+150), fill = red)

            koty.line((sec[i]+100,l+140) + (sec[i]+100,l+160), fill = red)
            koty.line((sec[i+1]+100,l+140) + (sec[i+1]+100,l+160), fill = red)

            koty.line((sec[i]+100,l+150) + (sec[i]+110,l+160), fill = red)
            koty.line((sec[i]+100,l+150) + (sec[i]+110,l+140), fill = red)
            koty.line((sec[i+1]+100,l+150) + (sec[i+1]+90,l+140), fill = red)
            koty.line((sec[i+1]+100,l+150) + (sec[i+1]+90,l+160), fill = red)
            fontpath = os.path.join(path, 'arimo.ttf')
            font = ImageFont.truetype(fontpath, 18)
            koty.text((100+(sec[i]+sec[i+1])/2, l+125), str(int(10*(sec[i+1]-sec[i]))), red, font, anchor='mt')

    def vkota(self, image, sec=None):
        width = 0
        koty = ImageDraw.Draw(image)
        red = (255,0,0)

        if sec == None:
            sec = (0, length)

        for i in range(len(sec)-1):
            koty.line((width+50,sec[i]+100) + (width+50,sec[i+1]+100), fill = red)

            koty.line((width+40,sec[i]+100) + (width+60,sec[i]+100), fill = red)
            koty.line((width+40,sec[i+1]+100) + (width+60,sec[i+1]+100), fill = red)

            koty.line((width+50,sec[i]+100) + (width+60,sec[i]+110), fill = red)
            koty.line((width+50,sec[i]+100) + (width+40,sec[i]+110), fill = red)
            koty.line((width+50,sec[i+1]+100) + (width+40,sec[i+1]+90), fill = red)
            koty.line((width+50,sec[i+1]+100) + (width+60,sec[i+1]+90), fill = red)
            # cant rotate text, use a new method to crop text and rotate
            self.draw_text_90_into(str(10*(sec[i+1]-sec[i])), image, (width+25, 100+int((sec[i]+sec[i+1])/2)))

    def draw_text_90_into (self, text: str, into, at):
        # Measure the text area
        fontpath = os.path.join(path, 'arimo.ttf')
        font = ImageFont.truetype(fontpath, 18)
        wi, hi = font.getsize(text)
        # Copy the relevant area from the source image
        img = into.crop ((at[0]-hi/2, at[1]-wi/2, at[0] + hi/2, at[1] + wi/2))
        # Rotate it backwards
        img = img.rotate (270, expand = 1)
        # Print into the rotated area
        d = ImageDraw.Draw (img)
        d.text ((0, 0), text, font = font, fill = (255, 0, 0))
        # Rotate it forward again
        img = img.rotate (90, expand = 1)
        # Insert it back into the source image
        # Note that we don't need a mask
        into.paste (img, (at[0]-hi//2, at[1]-wi//2))

    def pastem(self, im1: Image, im2: Image, x, y):
        # method for pasting image by its center
        xs = x-im2.width//2
        ys = y-im2.height//2
        im1.paste(im2,(xs,ys),im2)