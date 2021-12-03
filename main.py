from tkinter import *
from PIL import Image
from PIL import ImageTk
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

    for i in range(lines):
        if i > 0:
            y = y + 3 / 2 * buc
            if i % 2 == 1:
                x = x + radius
            else:
                x = x - radius
        coord.append(x)
        coord.append(y)
        hexagons.append(generate_hexagon2(x, y, radius))
        for j in range(columns - 1):
            c1 = x + ((j + 1) * 2 * radius)
            c2 = y
            coord.append(c1)
            coord.append(c2)
            hexagons.append(generate_hexagon2(c1, c2, radius))

    return hexagons, coord


def tk_circle():
    root = Tk()

    main_frame = Frame(root, width=300, height=300)
    main_frame.pack(expand=True, fill=BOTH)

    canvas = Canvas(main_frame, bg="gray", width=1000, height=1000)
    canvas.pack()

    # canvas.create_oval(50, 50, 100, 100, outline="black")
    # canvas.create_line(100, 100, 150, 100)
    # create_circle_center(canvas, 50, 100, 100)
    # canvas.create_polygon(generate_triangle(100, 100, 50), fill='', outline='black')
    # canvas.create_polygon(generate_triangle_upd(100, 100, 50), fill='', outline='black')
    # canvas.create_polygon(generate_romb(100, 100, 50), fill='', outline='black')

    hexes = generate_grid(30, 10, 7)
    print(hexes)
    for hex1 in hexes[0]:
        canvas.create_polygon(hex1, width=1, fill='', outline='white')
    for hex2 in range(0, len(hexes[1]), 2):
        create_circle_center(canvas, 30, hexes[1][hex2], hexes[1][hex2 + 1])

    image = Image.open('Assets/Images/BlueKinda.png')
    image = image.resize((100, 100), Image.ANTIALIAS)
    photoImage = ImageTk.PhotoImage(image)
    canvas.create_image(2, 10, image=photoImage, anchor=NW)

    # create_circle_center(canvas, 50, 52, 60)
    # canvas.create_polygon(generate_hexagon2(152, 60, 30), width=1, fill='', outline='white')
    # canvas.create_polygon(generate_hexagon2(252, 60, 50), width=1, fill='', outline='white')
    # canvas.create_polygon(generate_hexagon2(102, 147, 50), width=1, fill='', outline='white')
    # canvas.create_polygon(generate_hexagon2(202, 147, 50), width=1, fill='', outline='white')

    root.mainloop()


if __name__ == '__main__':
    # tk_canvas_test()
    tk_circle()
