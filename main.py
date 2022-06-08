import math
import os

from flask import Flask, render_template, request
from db.database import ServerStorage
import threading

storage = ServerStorage('./db/database.db3')
storage_thread = threading.Thread(storage.fill_random_db())
storage_thread.start()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/task_1/", methods=["GET", "POST"])
def task_1(x=None, x1=None, x2=None):
    if request.method == "POST":

        # Считываем введенные значения
        root_a = float(request.form['a'])
        root_b = float(request.form['b'])
        root_c = float(request.form['c'])

        # Считаем дискриминант
        discriminant = root_b ** 2 - 4 * root_a * root_c

        # Проверяем сколько уравнение имеет корней
        if discriminant < 0:
            x = 0
        elif discriminant == 0:
            x = - root_b / (2 * root_a)
        else:
            x1 = (-root_b + math.sqrt(discriminant)) / (2 * root_a)
            x2 = (-root_b - math.sqrt(discriminant)) / (2 * root_a)

        context = {
            "root_a": root_a,
            "root_b": root_b,
            "root_c": root_c,
            "discriminant": discriminant,
            "x": x,
            "x1": x1,
            "x2": x2,
        }

        return render_template('task_1.html', context=context)

    context = {
        "root_a": 0,
        "root_b": 0,
        "root_c": 0,
        "discriminant": 0,
        "x": 0,
        "x1": 0,
        "x2": 0,
    }
    return render_template('task_1.html', context=context)


@app.route('/task_2/', methods=["GET", "POST"])
def task_2():
    if request.method == "POST":
        color_id = request.form['color_id']
        color = request.form['color'].lower()
        color_db = storage.find_color_by_id(color_id)

        if color != color_db:
            result = 'Вы не угадали цвет'
        else:
            result = 'Вы угадали цвет'

        context = {
            'color_id': color_id,
            'color_db': color_db,
            'color': color,
            'result': result
        }

        return render_template('task_2.html', context=context)

    context = {
        'color_id': 'пусто',
        "color": 'пусто'
    }
    return render_template('task_2.html', context=context)


if __name__ == '__main__':
    app.run('127.0.0.1', 8000, debug=True)
