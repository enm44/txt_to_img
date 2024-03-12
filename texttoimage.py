import os
from PIL import Image
from math import sqrt
import cv2
import numpy as np

os.chdir("C:/Users/egon_/Desktop/lasercnc/images")
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
	

def imgtostr(img, color, chars=chars, res=[]):
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
	return ''.join(data).rstrip('Ł')							# Removing filler data


def Limgtostr(img, highchar, lowchar): # USED FOR LASER CNC, WORKS FOR BW IMAGES
	im = Image.open(img)
	grid = im.load()
	row, column = im.size
	data = [highchar if grid[x, y][0] == 0 else lowchar for y in range(column) for x in range(row)]
	return ''.join(data)
	# return [data[i:i+row] for i in range(0, len(data), row)]


def texttovid(text, framelength, name, fps, scale, color):
	
	# splitting text into sections (framelength)
	text = [text[i:i + framelength] + '`' for i in range(0, len(text), framelength)]
	print('split text')

	# creating images for each text section
	res = [np.array(strtoimg(i, color)) for i in text]
	print('created images')

	# creating video
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(f'{name}.mp4', codec, fps, (round(sqrt(framelength) * scale), round(sqrt(framelength) * scale))) 
	print('created video')

	# writing each image to video
	for i in res:
		if color:
			video.write(cv2.cvtColor(i, cv2.COLOR_RGB2BGR))
		else:
			video.write(cv2.cvtColor(i, cv2.COLOR_GRAY2BGR))
	print('wrote files')

	# releasing video
	cv2.destroyAllWindows()
	video.release()
	print('video released')

text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse feugiat sollicitudin arcu, vel volutpat nulla gravida ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed et augue vitae felis porta commodo ut at lectus. Sed pellentesque felis justo, nec pharetra lectus faucibus et. Donec ullamcorper sapien at fermentum tempus. Integer pharetra nunc vel ipsum tempor, sit amet dictum ligula feugiat. Aenean interdum pharetra velit in rhoncus. Sed ut diam ornare, dictum tellus non, molestie enim. Sed et commodo ipsum. Duis quis magna risus. Curabitur efficitur ut lorem in hendrerit. Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse id elit consequat, tempus lectus vel, tristique ipsum.Proin risus leo, convallis nec leo id, blandit lobortis felis. In hac habitasse platea dictumst. Etiam pretium ullamcorper augue a facilisis. Nunc sagittis at sapien quis eleifend. Nulla lobortis tortor ex, vitae molestie magna finibus eu. Vestibulum nec porta ex. Curabitur sodales velit et augue dignissim, eu placerat augue malesuada. Integer posuere vel leo vitae ultrices. Curabitur non libero mi. Phasellus bibendum venenatis nulla, et placerat mauris molestie at. Vivamus hendrerit in felis sit amet venenatis. Curabitur euismod elementum feugiat. Maecenas nec ante et metus tempus facilisis ac nec massa.Aenean sit amet pulvinar velit, vel dapibus nulla. Vestibulum aliquam vulputate ligula, quis dictum purus ultricies in. Donec imperdiet lacus in eros lacinia, sit amet suscipit risus congue. Donec dapibus turpis nec orci molestie, ac ullamcorper nibh congue. Suspendisse et ex malesuada, fermentum lorem nec, tempus enim. Aliquam erat volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eu luctus felis. Pellentesque iaculis condimentum arcu, quis sodales massa tempus in. Pellentesque maximus tincidunt lobortis. Nulla non massa tincidunt, malesuada libero a, tincidunt orci. Nulla mollis eleifend libero ac mattis. Etiam dignissim ultrices urna. Ut id dui a purus scelerisque consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse vel consectetur urna.'''
# texttovid(text, 4, 'test1', 4, 1, False)
a = strtoimg(text, True, 10)
a.show()
