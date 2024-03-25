import tkinter as tk
import texttoimage
from PIL import Image, ImageTk

res = None
def submitdata(mode, data):
	if mode == 1:
		test = texttoimage.test(data[0], data[2], data[1])

		res = texttoimage.strtoimg(data[0], data[2], data[1])
		display = tk.Label(m, image=ImageTk.PhotoImage(res))
		display.grid(row=6)

	if mode == 2:
		texttoimage.texttovid(data[0], data[1], data[2], data[3], data[4], data[5])

def renderchoice(mode):
	if mode == 1:
		color = tk.IntVar()

		tk.Label(m, text='Enter image text').grid(row=2)
		tk.Label(m, text='Enter scale').grid(row=3)

		text = tk.Entry(m)
		scale = tk.Entry(m)
		colorb = tk.Checkbutton(m, text='Color', variable=color, onvalue=True, offvalue=False)

		text.grid(row=2, column=1)
		scale.grid(row=3, column=1)
		colorb.grid(row=4)
		# texttoimage.strtoimg(text.get(), int(scale.get()), True if color.get() == 1 else False)
		submit = tk.Button(m, text='Submit', command=lambda: submitdata(1, [text.get(), int(scale.get()), True if color.get() == 1 else False])).grid(row=5)

	if mode == 3:
		color = tk.IntVar()

		tk.Label(m, text='Enter video text').grid(row=2)
		tk.Label(m, text='Enter the length of each frame').grid(row=3)
		tk.Label(m, text='Enter scale').grid(row=4)
		tk.Label(m, text='Enter fps of video').grid(row=5)
		tk.Label(m, text='Enter name of video').grid(row=6)

		text = tk.Entry(m)
		framelength = tk.Entry(m)
		scale = tk.Entry(m)
		fps = tk.Entry(m)
		vidname = tk.Entry(m)
		
		colorb = tk.Checkbutton(m, text='Color', variable=color, onvalue=True, offvalue=False)

		text.grid(row=2, column=1)
		framelength.grid(row=3, column=1)
		scale.grid(row=4, column=1)
		fps.grid(row=5, column=1)
		vidname.grid(row=6, column=1)
		colorb.grid(row=7)
		# text, framelength, name, fps, scale, color, test
		submit = tk.Button(m, text='Submit', command=lambda: submitdata(1, [text.get(), int(framelength.get()), vidname.get(), int(fps.get()), int(scale.get()), True if color.get() == 1 else False, False])).grid(row=8)






m = tk.Tk()
# root.geometry('1000x1000')
m.title = 'Texttoimage beta'

title = tk.Label(m, text='Choose an option').grid(row=0)

sti = tk.Button(m, text='String to Image', command=lambda: renderchoice(1)).grid(row=1, column=0)
its = tk.Button(m, text='Image to String', command=lambda: renderchoice(2)).grid(row=1, column=1)
stv = tk.Button(m, text='String to Video', command=lambda: renderchoice(3)).grid(row=1, column=2)
vts = tk.Button(m, text='Video to String', command=lambda: renderchoice(4)).grid(row=1, column=3)


m.mainloop()


