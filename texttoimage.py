import os
from PIL import Image
from math import sqrt
import cv2
import numpy as np

os.chdir("C:/Users/egon_/Desktop/git/lasercnc/images")
chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ', 'Ā', 'ā', 'Ă', 'ă', 'Ą', 'ą', 'Ć', 'ć', 'Ĉ', 'ĉ', 'Ċ', 'ċ', 'Č', 'č', 'Ď', 'ď', 'Đ', 'đ', 'Ē', 'ē', 'Ĕ', 'ĕ', 'Ė', 'ė', 'Ę', 'ę', 'Ě', 'ě', 'Ĝ', 'ĝ', 'Ğ', 'ğ', 'Ġ', 'ġ', 'Ģ', 'ģ', 'Ĥ', 'ĥ', 'Ħ', 'ħ', 'Ĩ', 'ĩ', 'Ī', 'ī', 'Ĭ', 'ĭ', 'Į', 'į', 'İ', 'ı', 'Ĳ', 'ĳ', 'Ĵ', 'ĵ', 'Ķ', 'ķ', 'ĸ', 'Ĺ', 'ĺ', 'Ļ', 'ļ', 'Ľ', 'ľ', 'Ŀ', 'Ł']
# chars = chars[::-1]


def strtoimg(text, color, scale, dims=[], chars=chars):
	data = [chars.index(i) for i in text]				# Mapping each character to integer value
	if len(dims) == 0:									# Calculating dimensions
		imglen = len(text) / 3 if color else len(text) 
		dimx = round(sqrt(imglen))
		dimy = round(imglen / dimx)
		datalost = round((dimx * dimy) - imglen)
	else:
		dimx = dims[0]
		dimy = dims[1]

	mode = 'RGB' if color else 'L'
	while True:
		try:
			a = Image.frombytes(mode, (dimx, dimy), bytes(data))
			a = a.resize((a.size[0] * scale, a.size[1] * scale), resample=Image.BOX)
			return a
		except:
			data.append(0)								# Adding blank data to fill out image resoultion
	

def imgtostr(img, color, scale, chars=chars, res=[]):

	img = img.resize((int(img.size[0] / scale), int(img.size[1] / scale)), resample=Image.BOX)
	# checking whether inputted image is file or image object
	try:
		img = img.convert('L') if not color else img 			# Converting to Grayscale if not color
		grid = img.load()										# Creating image grid
		row, column = img.size

	except:
		im = Image.open(img)									# same thing but loading image first
		im = im.convert('L') if not color else im
		grid = im.load()
		row, column = im.size

	# COLOR: Getting the value for each color of pixel (RGB) and mapping it to character
	# GRAYSCALE: Getting the value of each pixel and mapping it to character

	data = [chars[grid[x,y][p]] for y in range(column) for x in range(row) for p in range(3)] if color else [chars[grid[x,y]] for y in range(column ) for x in range(row)]
	return ''.join(data).rstrip(' ').rstrip('Ł')						# Removing filler data


def Limgtostr(img, highchar, lowchar): # USED FOR LASER CNC, WORKS FOR BW IMAGES
	im = Image.open(img)
	grid = im.load()
	row, column = im.size
	data = [highchar if grid[x, y][0] == 0 else lowchar for y in range(column) for x in range(row)]
	return ''.join(data)
	# return [data[i:i+row] for i in range(0, len(data), row)]


def texttovid(text, framelength, name, fps, scale, color, test):
	
	# splitting text into sections (framelength)
	text = [text[i:i + framelength] for i in range(0, len(text), framelength)]
	print('split text')

	# creating images for each text section
	res = [strtoimg((i + 'ŁŁ'), color, scale) for i in text]
	print('created images')

	if test:
		tests = [True if imgtostr(res[i], color, scale).rstrip('ŁŁŁ') == text[i] else False for i in range(len(text))]
		print(tests)
		return None

	# creating video
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(f'{name}.mp4', codec, fps, (round(sqrt(framelength) * scale), round(sqrt(framelength) * scale))) 
	print('created video')

	# writing each image to video
	if color:
		grading = cv2.COLOR_RGB2BGR
	else:
		grading = cv2.COLOR_GRAY2BGR

	for i in res:
		video.write(cv2.cvtColor(np.array(i), grading))
	print('wrote files')

	# releasing video
	cv2.destroyAllWindows()
	video.release()
	print('video released')


def test(text, color, scale):
	a = strtoimg(text, color, scale)
	a.show()
	print(imgtostr(a, color, scale))
