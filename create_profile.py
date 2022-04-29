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
        self.hspec = (0,self.sirka)
        self.vspec = (0,length)

    def create_profile(self):
        # load images
        street = Image.open(os.path.join(path, 'im/street.png'))
        white = Image.open(os.path.join(path, 'im/white.png'))
        treebig = Image.open(os.path.join(path, 'im/treebig.png'))

        # dimension definition
        width = int(self.sirka)
        oneway = self.jednosmerka
        top = street.resize((width, length))

        # sem prijde rozhodovaci metoda
        if width < 600:
            sides_curb = 0
            sides_park = 0
            left = 0
            right = width
        elif width >= 600 and width < 750:
            sides_curb = 1
            sides_park = 0
            left = 150
            right = width
        elif width >= 1000:
            sides_curb = 1
            sides_park = 1
            left = 150
            right = width-250
        else:
            sides_curb = 1
            sides_park = 1
            left = 150
            right = width-250


        typ_park = 1
        w_curb = 150

        self.add_curb(top, width, sides_curb, w_curb)
        self.add_parking(top, width, sides_park, typ_park, sides_curb, w_curb)
        self.add_cars(top, oneway, left, right)
        
        hspec = sorted(self.hspec)
        vspec = sorted(self.vspec)

        # koty
        all = white.resize((width+200,length+200))
        all.paste(top,(100,100),top)
        self.hkota(all)
        self.hkota(all, hspec)
        self.vkota(all, vspec)

        all.save(os.path.join(path, 'im/profil.png'))
        all.show()

    def add_curb(self, top, width, sides_curb, w_curb):
        ped1 = Image.open(os.path.join(path, 'im/ped1.png'))
        ped2 = Image.open(os.path.join(path, 'im/ped2.png'))
        ped3 = Image.open(os.path.join(path, 'im/ped3.png'))
        ped4 = Image.open(os.path.join(path, 'im/ped4.png'))
        chodnik = ImageDraw.Draw(top)
        black = (0,0,0)
        if sides_curb == 2:
            chodnik.line((w_curb,0)+(w_curb,length), fill = black)
            chodnik.line((width-w_curb,0)+(width-w_curb,length), fill = black)
            self.pastem(top,ped1,75,200)
            self.pastem(top,ped2,75,1800)
            self.pastem(top,ped3,width-75,500)
            self.pastem(top,ped4,width-75,2200)
            addh = (w_curb, width-w_curb)
        elif sides_curb == 1:
            chodnik.line((w_curb,0)+(w_curb,length), fill = black)
            self.pastem(top,ped1,75,200)
            self.pastem(top,ped2,75,1800)
            addh = (w_curb,)
        else: # no curbs
            self.pastem(top,ped1,75,200)
            self.pastem(top,ped2,75,1800)
            addh = ()
        self.hspec = self.hspec + addh

    def add_parking(self, top, width, sides_park, typ, sides_curb, w_curb):
        # park = Image.open(os.path.join(path, 'im/park.png'))
        if typ == 1:
            line1 = Image.open(os.path.join(path, 'im/line1.png'))

            line = Image.new(mode = "RGBA", size = (400, 2800))
            line.paste(line1, (100, 0), line1)
            treesmall = Image.open(os.path.join(path, 'im/treesmall.png'))
            tree = Image.open(os.path.join(path, 'im/treesmall.png'))
            tree.putalpha(255)
            line.paste(tree, (50, 250), treesmall)
            line.paste(tree, (50, 2250), treesmall)
            pas = 200

            # line = Image.new(mode = "RGBA", size = (pas, length))
            # line.paste(park, (0,500), park)
            # line.paste(park, (0,1100), park)
            # line.paste(park, (0,1700), park)
            # line.paste(park, (0,-300), park)
            # line.paste(park, (0,2500), park)
            # line.save(os.path.join(path, 'im/line1.png'))

        if sides_park == 1 and (sides_curb == 1 or sides_curb == 0):
            self.pastem(top, line, width-pas//2-50, length//2)
            addh = (width-pas-50,width-50)
        elif sides_park == 1 and sides_curb == 2:
            self.pastem(top, line, width-w_curb-pas//2, length//2)
            addh = (width-w_curb-pas,)
        elif sides_park == 2 and sides_curb == 0:
            self.pastem(top, line, 50+pas//2, length//2)
            self.pastem(top, line, width-pas//2-50, length//2)
            addh = (50,50+pas,width-pas-50,width-50)
        elif sides_park == 2 and sides_curb == 1:
            self.pastem(top, line, w_curb+pas//2, length//2)
            self.pastem(top, line, width-pas//2-50, length//2)
            addh = (w_curb+pas,width-pas-50,width-50)
        elif sides_park == 2 and sides_curb == 2:
            self.pastem(top, line, w_curb+pas//2, length//2)
            self.pastem(top, line, width-w_curb-pas//2, length//2)
            addh = (pas+w_curb,width-w_curb-pas)
        else: # (sides_park = 0)
            addh = ()
            pass
        self.hspec = self.hspec + addh

    def add_cars(self, top, oneway, left, right):
        car = Image.open(os.path.join(path, 'im/car.png'))
        bicycle = Image.open(os.path.join(path, 'im/bicycle.png'))
        bus = Image.open(os.path.join(path, 'im/bus.png'))
        width = right-left
        if oneway == 1:
            self.pastem(top, car, left+round(width*7/11), 500)
            self.pastem(top, car, left+round(width*7/11), 2300)
        else:
            self.pastem(top, car, left+round(width*3/4), 500)
            self.pastem(top, car, left+round(width*3/4), 2300)
            self.pastem(top, car.rotate(180), left+round(width*1/4), 1400)

        self.pastem(top, bicycle, left+round(width*3/4), 1100)
        self.pastem(top, bicycle.rotate(180), left+round(width*1/4), 400)

        
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