import os
import random
import configparser
from PIL import Image, ImageOps, ImageFilter

image_dir = "./img"
result_dir = "./output"

### credit to intangere on github ###
# https://github.com/intangere/PIL-dropshadow

def dropShadow(image, shadow=(0,0,0,255), offset=(0,0), background = (0,0,0,0), iterations=3, radius=15):

	back = image

	for x in range(0, back.width):
			for y in range(0, back.height):
					if back.getpixel((x,y))[3] != 0:
						 back.putpixel((x,y), shadow)
					else:
						 back.putpixel((x,y), background)

	n = 0
	while n < iterations:
		back = back.filter(ImageFilter.BoxBlur(radius))
		n += 1

	back.paste(image, offset, image)
	return back

### CREDIT END ###

config = configparser.ConfigParser()
config.read("settings.txt")

size = int(config["DEFAULT"]["result_size"])
poster_size = float(config["DEFAULT"]["poster_size"])
maxrot = int(config["DEFAULT"]["max_rotation"])
variants = int(config["DEFAULT"]["variants"])
shadow_offset_x = float(config["DEFAULT"]["shadow_offset_x"])
shadow_offset_y = float(config["DEFAULT"]["shadow_offset_y"])
shadow_transparency = int(config["DEFAULT"]["shadow_transparency"])
shadow_radius = float(config["DEFAULT"]["shadow_radius"])
prefix = config["DEFAULT"]["prefix"]

if __name__ == "__main__":
	if not os.path.exists(result_dir):
		os.makedirs(result_dir)
	files = os.listdir(image_dir)
	if len(files) == 0:
		print("There are no files in the input folder! Put images in ./img to generate posters out of them")
	itr = 0
	image_counter = 0
	for file in files:
		image_counter += 1
		print("generating variants for image {} out of {}...".format(image_counter, len(files)))
		for i in range(0, variants):
			itr += 1
			with Image.open(image_dir + "/" + file) as img:
				img = img.convert("RGBA")
				img = ImageOps.contain(img, (int(size*poster_size), int(size*poster_size)), Image.BICUBIC)
				w, h = img.size
				img = ImageOps.pad(img, (w, size), color="#00000000")
				img = ImageOps.pad(img, (size, size), color="#00000000")
				img = img.rotate(random.randrange(-maxrot, maxrot), Image.BICUBIC)
				if shadow_transparency != 0:
					shadow = img.copy()
					shadow = dropShadow(shadow, shadow=(0, 0, 0, shadow_transparency), offset=(size*10000, size*10000), radius=int(size*shadow_radius))
					shadow.paste(img, (int(size*shadow_offset_x), int(size*shadow_offset_y)), img)
					shadow.save("{}/{}{}.png".format(result_dir, prefix, itr))
				else:
					img.save("{}/{}{}.png".format(result_dir, prefix, itr))
			print("{}/{}".format(i+1, variants))
