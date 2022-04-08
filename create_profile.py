import os
from PIL import Image

path = os.path.dirname(__file__)

class CreateProfile:
    def __init__(self, sirka): 
        self.sirka = sirka

    def create_profile(self):
        width = int(self.sirka*100)
        length = 1000
        street = Image.open(os.path.join(path, 'im/street.png'))
        car = Image.open(os.path.join(path, 'im/car.png'))
        bicycle = Image.open(os.path.join(path, 'im/bicycle.png'))
        car = car.resize((car.width//4, car.height//4))
        im = street.resize((width, length))
        im.paste(car,(width*3//4-car.width//2,800), car)
        im.paste(bicycle,(width*3//4-bicycle.width//2,200), bicycle)
        im.save(os.path.join(path, 'im/profil.png'))
        im.show()
