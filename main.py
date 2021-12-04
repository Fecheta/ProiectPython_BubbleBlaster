from tkinter import *
from tkinter import Canvas

from PIL import Image
from PIL import ImageTk
import random
import time


def tk_test():
    root = Tk()
    root.geometry("500x500")

    labes0 = Label(root, text="Ana are mere")
    labes0.grid(row=0, column=0)

    labes1 = Label(root, text="Ana are mere mere m")
    labes1.grid(row=1, column=1)

    # labes0.pack()
    # labes1.pack()

    root.mainloop()


def generate_hexagon(x, y, radius):
    pointList = []

    x = x
    y = y

    calcul1 = radius / 2
    calcul2 = ((3 ** (1 / 2)) * radius) / 4
    calcul = calcul1

    pointList.append(x)
    pointList.append(y - radius)

    pointList.append(x + radius)
    pointList.append(y - calcul)

    pointList.append(x + radius)
    pointList.append(y + calcul)

    pointList.append(x)
    pointList.append(y + radius)

    pointList.append(x - radius)
    pointList.append(y + calcul)

    pointList.append(x - radius)
    pointList.append(y - calcul)

    return pointList


def move(canvas, image, x, y, t):
    # time.sleep(t)

    canvas.move(image, x, y)


def tk_canvas_test():
    root = Tk()

    mainFrame = Frame(root, width=300, height=300)
    mainFrame.pack(expand=True, fill=BOTH)

    canvas = Canvas(mainFrame, bg="white", width=300, height=300)
    canvas.pack()

    # testShape = canvas.create_line(10, 10, 100, 100, dash=(1, 2), width=2)
    # shape = canvas.create_rectangle(50, 50, 150, 150, width=2, outline='red')
    # testShape1 = canvas.create_oval(150, 150, 50, 50, width=2)
    testShape2 = canvas.create_polygon(generate_hexagon(50, 50, 50), width=1, fill='', outline="black")
    testShape2 = canvas.create_polygon(generate_hexagon(150, 50, 50), width=1, fill='', outline="black")
    testShape2 = canvas.create_polygon(generate_hexagon(250, 50, 50), width=1, fill='', outline="black")
    testShape2 = canvas.create_polygon(generate_hexagon(350, 50, 50), width=1, fill='', outline="black")

    testShape2 = canvas.create_polygon(generate_hexagon(0, 125, 50), width=1, fill='', outline="black")
    testShape2 = canvas.create_polygon(generate_hexagon(100, 125, 50), width=1, fill='', outline="black")

    # testShape = canvas.create_oval(140, 82, 260, 168, width=1, fill='')
    image = Image.open('Assets/Images/BlueKinda.png')
    image = image.resize((120, 105), Image.ANTIALIAS)
    photoImage = ImageTk.PhotoImage(image)

    circleImage = canvas.create_image(140, 73, image=photoImage, anchor=NW)
    testShape2 = canvas.create_polygon(generate_hexagon(200, 125, 60), width=1, fill='', outline="black")

    testShape2 = canvas.create_polygon(generate_hexagon(300, 125, 50), width=1, fill='', outline="black")

    # time.sleep(5)
    # canvas.move(circleImage, 10, 10)

    root.mainloop()


def create_circle_center(canvas, radius, x, y):
    actual_x1 = x - radius
    actual_y1 = y - radius
    actual_x2 = x + radius
    actual_y2 = y + radius

    canvas.create_oval(actual_x1, actual_y1, actual_x2, actual_y2, fill='red', outline='')


def generate_hexagon2(x, y, radius):
    result = []
    rad2 = 2 ** (1 / 2)
    rad3 = 3 ** (1 / 2)
    l = 2 * rad3 * radius
    buc = l / 3
    upsize = (2 * buc) ** 2 - (2 * radius) ** 2

    result.append(x)
    result.append(y - buc)

    result.append(x + radius)
    result.append(y - buc / 2)

    result.append(x + radius)
    result.append(y + buc / 2)

    result.append(x)
    result.append(y + buc)

    result.append(x - radius)
    result.append(y + buc / 2)

    result.append(x - radius)
    result.append(y - buc / 2)

    return result


def generate_square(x, y, radius):
    result = []

    result.append(x - radius)
    result.append(y - radius)

    result.append(x + radius)
    result.append(y - radius)

    result.append(x + radius)
    result.append(y + radius)

    result.append(x - radius)
    result.append(y + radius)

    return result


def generate_romb(x, y, radius):
    rad2 = 2 ** (1 / 2)
    result = []

    result.append(x)
    result.append(y - radius * rad2)

    result.append(x + radius * rad2)
    result.append(y)

    result.append(x)
    result.append(y + radius * rad2)

    result.append(x - radius * rad2)
    result.append(y)

    return result


def generate_triangle(x, y, radius):
    result = []
    rad3 = 3 ** (1 / 2)

    result.append(x - 2 * radius)
    result.append(y)

    result.append(x + radius)
    result.append(y + radius * rad3)

    result.append(x + radius)
    result.append(y - radius * rad3)

    return result


def generate_triangle_upd(x, y, radius):
    result = []
    rad3 = 3 ** (1 / 2)

    result.append(x + 2 * radius)
    result.append(y)

    result.append(x - radius)
    result.append(y - radius * rad3)

    result.append(x - radius)
    result.append(y + radius * rad3)

    return result


def generate_grid(radius, lines, columns):
    hexagons = []
    coord = []

    rad3 = 3 ** (1 / 2)
    side = 2 * rad3 * radius
    buc = side / 3

    x = 2 + radius
    y = 2 + buc

    parity = 1

    for i in range(lines):
        if i > 0:
            y = y + 3 / 2 * buc
            if i % 2 == 1:
                parity = 2
                x = x + radius
            else:
                parity = 1
                x = x - radius
        coord.append(x)
        coord.append(y)
        hexagons.append(generate_hexagon2(x, y, radius))
        for j in range(columns - parity):
            c1 = x + ((j + 1) * 2 * radius)
            c2 = y
            coord.append(c1)
            coord.append(c2)
            hexagons.append(generate_hexagon2(c1, c2, radius))

    return hexagons, coord


def generate_image_in_center(radius, image):
    image = Image.open(image)
    image = image.resize((2 * radius, 2 * radius), Image.ANTIALIAS)

    p = ImageTk.PhotoImage(image)
    return p


def event_test(event):
    print('Event x: ' + str(event.x) + '\nEvent y: ' + str(event.y))


start = False
coord_x = 0
coord_y = 0
vx = 25
vy = 25
def tk_circle():
    global coord_x
    global coord_y

    root = Tk()

    main_frame = Frame(root, width=300, height=300)
    main_frame.pack(expand=True, fill=BOTH)

    rad3 = 3 ** (1 / 2)
    side = 2 * rad3 * 25
    buc = side / 3

    canvas: Canvas = Canvas(main_frame, bg="gray", width=600 + 1, height=15 * buc + 16 * buc // 2 + 2)
    canvas.pack()

    # canvas.create_oval(50, 50, 100, 100, outline="black")
    # canvas.create_line(100, 100, 150, 100)
    # create_circle_center(canvas, 50, 100, 100)
    # canvas.create_polygon(generate_triangle(100, 100, 50), fill='', outline='black')
    # canvas.create_polygon(generate_triangle_upd(100, 100, 50), fill='', outline='black')
    # canvas.create_polygon(generate_romb(100, 100, 50), fill='', outline='black')

    hexes = generate_grid(25, 15, 12)
    print(hexes)
    for hex1 in hexes[0]:
        canvas.create_polygon(hex1, width=1, fill='', outline='white')

    bubbles = []
    b_images = ['Assets/Images/BlueKinda.png',
                'Assets/Images/GreenCircle.png',
                'Assets/Images/RedCircle.png',
                'Assets/Images/YellowCircle.png']

    # for hex2 in range(0, len(hexes[1]), 2):
    index = random.randint(0, 3)
    x = generate_image_in_center(25, b_images[index])
    bubbles.append(x)
    # canvas.create_image(hexes[1][hex2], hex[1][hex2+1], image=x, anchor=NW)
    i = 0
    # for i in range(0, len(bubbles)):
    coord_x = hexes[1][2 * i] - 25
    coord_y = hexes[1][2 * i + 1] - 25
    img = canvas.create_image(hexes[1][2 * i] - 25, hexes[1][2 * i + 1] - 25, image=x, anchor=NW)

    # image = Image.open('Assets/Images/BlueKinda.png')
    # image = image.resize((100, 100), Image.ANTIALIAS)
    # photoImage = ImageTk.PhotoImage(image)
    # canvas.create_image(2, 10, image=photoImage, anchor=NW)

    def event_func1(event):
        print('Event x: ' + str(event.x) + '\nEvent y: ' + str(event.y))
        # canvas.create_oval(100, 100, 150, 150, fill='red')
        canvas.move(img, 10, 10)

    def event_func2(event):
        canvas.move(img, -10, -10)


    img2 = x
    def event_func3(event):
        global img2

        v = random.randint(0, 3)
        img2 = generate_image_in_center(25, b_images[v])
        canvas.itemconfig(img, image=img2)
        # canvas.delete(img)

    def move_cc(event):
        global start

        if not start:
            start = True



    def move_circle_bounce(event):
        global coord_x
        global coord_y
        global vx
        global vy

        coord_x = coord_x + vx
        coord_y = coord_y + vy

        if coord_x > 575 or coord_x < 25:
            vx = -vx
        if coord_y < 25 or coord_y > 625:
            vy = -vy
        canvas.move(img, vx, vy)

    root.bind('<Button-1>', move_circle_bounce)
    # root.bind('<Button-3>', event_func2)
    # root.bind('<Button-2>', event_func3)

    # root.after(1000, move_circle_bounce)
    root.mainloop()


if __name__ == '__main__':
    # tk_canvas_test()
    tk_circle()
