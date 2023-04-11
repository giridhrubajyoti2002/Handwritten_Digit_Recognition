from tkinter import *
from turtle import pensize
import numpy as np
import os
from PIL import ImageGrab, ImageTk, Image
# import pyscreenshot as ImageGrab
import pygetwindow as gw
import win32gui
# from pyrsistent import b
# from Prediction import predict
from tensorflow import keras
from keras.models import load_model

title = "Handwritten digit recognition"
window = Tk()
window.title(title)
l1 = Label()


# def callback(hwnd, extra):
#     rect = win32gui.GetWindowText(hwnd)
#     print(rect)


# win32gui.EnumWindows(callback, None)


def MyProject():
    global l1, cv
    l1.destroy()
    widget = cv
    # Setting co-ordinates of canvas
    win = gw.getWindowsWithTitle(title)[0]
    # x = win.left + widget.winfo_x() + 40
    x = window.winfo_rootx() + widget.winfo_x() + 28  # 38
    # y = win.top + widget.winfo_y() + 40
    y = window.winfo_rooty() + widget.winfo_y() + 28   # 38
    x1 = x + widget.winfo_width() + 92  # 82
    y1 = y + widget.winfo_height() + 80  # 82

    print(x, y, x1, y1)
    # Image is captured from canvas and is resized to (28 X 28) px
    img = ImageGrab.grab(bbox=(x, y, x1, y1)).resize((28, 28)).convert('L')
    # img = img.crop((2, 2, 30, 30))
    img.save("temp.png")
    # Converting rgb to grayscale image
    # img = img.convert('L')

    # Extracting pixel matrix of image and converting it to a vector of (1, 784)
    vec = np.asarray(img)
    vec = np.expand_dims(vec, axis=0)
    vec = np.expand_dims(vec, axis=3)
    # vec = vec.reshape(1, 784)
    # vec = np.zeros((1, 784))
    # k = 0
    # for i in range(28):
    #     for j in range(28):
    #         vec[0][k] = x[i][j]
    #         k += 1

    # Loading Thetas
# Theta1 = np.loadtxt('Theta1.txt')
# Theta2 = np.loadtxt('Theta2.txt')

    # Calling function for prediction
    model = load_model(
        f'{os.getcwd()}/model_experiments/MNIST_model_6')  # Replace with model name
    pred = model.predict(vec / 255)

    # Displaying the result
    l1 = Label(window, text=f"Digit = {str(np.argmax(pred))}({100*max(pred[0]):.2f}%)", font=(
        'Algerian', 20))
    l1.place(x=190, y=500)


lastx, lasty = None, None


# Clears the canvas
def clear_widget():
    global cv, l1
    cv.delete("all")
    l1.destroy()


# Activate canvas
def event_activation(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y


# To draw on canvas
def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width=30, fill='white',
                   capstyle=ROUND, smooth=TRUE, splinesteps=12)
    lastx, lasty = x, y


# Label
L1 = Label(window, text="Handwritten Digit Recoginition",
           font=('Algerian', 25), fg="blue")
L1.place(x=90, y=5)
L2 = Label(window, text="Draw a digit in the middle of the canvas in medium size",
           font=('Algerian', 12), fg="black")
L2.place(x=110, y=45)

# Button to clear canvas
b1 = Button(window, text="Clear", font=('Algerian', 16),
            bg="white", fg="red", command=clear_widget)
b1.place(x=200, y=440)

# Button to predict digit drawn on canvas
b2 = Button(window, text="Predict", font=('Algerian', 16),
            bg="white", fg="green", command=MyProject)
b2.place(x=320, y=440)

# Setting properties of canvas
cv = Canvas(window, width=400, height=350, bg='black')
cv.place(x=100, y=70)
cv.bind('<Button-1>', event_activation)

window.state('zoomed')
# window.geometry("630x560")
# window.geometry("%dx%d" % (window.winfo_screenwidth, window.winfo_screenheight))
window.resizable(False, False)
window.mainloop()
