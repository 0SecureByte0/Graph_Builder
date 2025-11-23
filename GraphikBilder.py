from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import math


def cmAbout():
    about_window = Toplevel(form1)
    about_window.title("О программе")
    about_window.geometry("300x150")
    Label(about_window,
          text="Построитель графиков v1.4\nСпасибо моим родителям\nАлександру Валентиновичу\nи \nАнне Анатольевне\nVoronenkoVA\n2025 год",
          font=("Arial", 12)).pack(expand=True)
    Button(about_window, text="Закрыть", command=about_window.destroy).pack(pady=10)


def cmPA():
    support_window = Toplevel(form1)
    support_window.title("Поддержка автора")
    support_window.geometry("300x150")
    Label(support_window, text="Если вам понравилось приложение,\nподдержите автора :)\n+7-921-257-40-53\nСБЕР",
          font=("Arial", 12)).pack(expand=True)
    Button(support_window, text="Закрыть", command=support_window.destroy).pack(pady=10)

def cmClean():
    canvas1.delete("all")

def cmDraw():
    width = 400
    height = 400
    scale = 20
    center_x = width // 2
    center_y = height // 2

    try:
        x_min = float(entry_x_min.get())
        x_max = float(entry_x_max.get())
        y_min = float(entry_y_min.get())
        y_max = float(entry_y_max.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Неверные ограничения.")
        return

    for i in range(0, width, scale):
        canvas1.create_line(i, 0, i, height, fill="#ddd")
    for i in range(0, height, scale):
        canvas1.create_line(0, i, width, i, fill="#ddd")

    canvas1.create_line(0, center_y, width, center_y, arrow=LAST, width=2)  # Ось X
    canvas1.create_line(center_x, 0, center_x, height, arrow=FIRST, width=2)  # Ось Y

    canvas1.create_text(width - 10, center_y - 10, text="x", font=("Arial", 12))
    canvas1.create_text(center_x + 10, 10, text="y", font=("Arial", 12))

    for x in range(int(x_min), int(x_max) + 1):
        canvas1.create_text(center_x + x * scale, center_y + 10, text=str(x), font=("Arial", 10))

    for y in range(int(y_min), int(y_max) + 1):
        canvas1.create_text(center_x - 10, center_y - y * scale, text=str(y), font=("Arial", 10), anchor=E)

    formula = entry_formula.get()

    safe_dict = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "math": math
    }

    if formula:
        prev_x = x_min
        try:
            prev_y = eval(formula, {**safe_dict, "x": prev_x})
        except:
            messagebox.showerror("Ошибка", "Невозможно вычислить значение для x = " + str(x_min))
            return

        step = 0.01
        x = x_min
        while x <= x_max:
            try:
                y = eval(formula, {**safe_dict, "x": x})
                if math.isnan(y) or math.isinf(y):
                    messagebox.showerror("Ошибка", f"Невозможно вычислить значение для x = {x}.")
                    return
                if y >= y_min and y <= y_max:
                    canvas1.create_line(
                        center_x + prev_x * scale,
                        center_y - prev_y * scale,
                        center_x + x * scale,
                        center_y - y * scale,
                        fill=selected_color.get()
                    )
                prev_x, prev_y = x, y
                x += step
            except:
                messagebox.showerror("Ошибка", f"Невозможно вычислить значение для x = {x}.")
                break
    else:
        messagebox.showerror("Ошибка", "Введите формулу.")


form1 = Tk()
#form1.iconbitmap(default="4.ico")
form1.geometry("450x640")
form1.title("Построитель графиков")

form1.bind("<F1>", lambda event: cmAbout())
form1.bind("<Escape>", lambda event: entry_formula.delete(0, END))
form1.bind("<Return>", lambda event: cmDraw())


canvas1 = Canvas(bg="white", width=400, height=400)
canvas1.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

entry_formula = Entry(width=30)
entry_formula.grid(row=1, column=1, columnspan=1, pady=10)
entry_formula.insert(0, "x**2 - x - 1")

Label(form1, text="x min:").grid(row=2, column=0, padx=10, pady=5, sticky=E)
entry_x_min = Entry(width=5)
entry_x_min.grid(row=2, column=1, padx=10, pady=5)
entry_x_min.insert(0, "-10")

Label(form1, text="x max:").grid(row=3, column=0, padx=10, pady=5, sticky=E)
entry_x_max = Entry(width=5)
entry_x_max.grid(row=3, column=1, padx=10, pady=5)
entry_x_max.insert(0, "10")

Label(form1, text="y min:").grid(row=2, column=2, padx=10, pady=5, sticky=E)
entry_y_min = Entry(width=5)
entry_y_min.grid(row=2, column=3, padx=10, pady=5)
entry_y_min.insert(0, "-10")

Label(form1, text="y max:").grid(row=3, column=2, padx=10, pady=5, sticky=E)
entry_y_max = Entry(width=5)
entry_y_max.grid(row=3, column=3, padx=10, pady=5)
entry_y_max.insert(0, "10")


selected_color = StringVar(value="blue")
red_btn = ttk.Radiobutton(form1, text="Red", value="red", variable=selected_color)
red_btn.grid(row=4, column=0, padx=10, pady=5)
blue_btn = ttk.Radiobutton(form1, text="Blue", value="blue", variable=selected_color)
blue_btn.grid(row=4, column=1, padx=10, pady=5)
green_btn = ttk.Radiobutton(form1, text="Green", value="green", variable=selected_color)
green_btn.grid(row=4, column=2, padx=10, pady=5)
black_btn = ttk.Radiobutton(form1, text="Black", value="black", variable=selected_color)
black_btn.grid(row=4, column=3, padx=10, pady=5)

Button(form1, text="Очистить поле", command=cmClean).grid(row=1, column=2, padx=5)
Button(form1, text="Построить график", command=cmDraw).grid(row=5, column=1, columnspan=2, pady=10)
Button(form1, text="(?)", command=cmAbout).grid(row=5, column=0, pady=10)
Button(form1, text="(₽)", command=cmPA).grid(row=5, column=3, pady=10)

form1.mainloop()
