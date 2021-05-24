import eel
from ishape import *
from point import Point2d

FIGURES = []


def main():
    eel.init("web")

    @eel.expose
    def re_figures():
        resp = []
        for fig in FIGURES:
            str = fig.__str__()
            x = [round(point.x[0], 3) for point in fig.p]
            y = [round(point.x[1], 3) for point in fig.p]
            if str not in ["Прямая", "Ломаная", "Круг"]:
                for i in range(len(x) - 1):
                    eel.draw_line(x[i], y[i], x[i + 1], y[i + 1])
                eel.draw_line(x[0], y[0], x[len(x) - 1], y[len(x) - 1])
                resp.append({"id": FIGURES.index(fig),
                             "name": str,
                             "x": x,
                             "y": y,
                             "length": round(fig.length(), 2),
                             "square": round(fig.square(), 2)})
            elif str == "Круг":
                eel.draw_circle(x[0], y[0], fig.r)
                resp.append({"id": FIGURES.index(fig),
                             "name": str,
                             "x": x[0],
                             "y": y[0],
                             "r": fig.r,
                             "length": round(fig.length(), 2),
                             "square": round(fig.square(), 2)})
            elif str in ["Ломаная", "Прямая"]:
                for i in range(len(x) - 1):
                    eel.draw_line(x[i], y[i], x[i + 1], y[i + 1])
                resp.append({"id": FIGURES.index(fig),
                             "name": str,
                             "x": x,
                             "y": y,
                             "length": round(fig.length(), 2)})
        return resp

    @eel.expose
    def sym_figures(i, ax):
        i = int(i)
        ax = int(ax)
        fig = FIGURES[i]
        for point in fig.p:
            point.sym_axis(ax)

    @eel.expose
    def pere_figures(i, x, y):
        i = int(i)
        x = int(x)
        y = int(y)
        fig = FIGURES[i]
        for point in fig.p:
            point.sum_two_points(Point2d(coord=[x, y]))

    @eel.expose
    def pow_figures(i, phi):
        phi = float(phi)
        i = int(i)
        fig = FIGURES[i]
        for point in fig.p:
            point.rotate(phi)


    @eel.expose
    def count_figures():
        return len(FIGURES)

    @eel.expose
    def del_figure(i):
        del FIGURES[i]

    @eel.expose
    def del_all():
        FIGURES.clear()

    @eel.expose
    def peres_figures(i, j):
        i = int(i)
        j = int(j)
        fig1 = FIGURES[i]
        fig2 = FIGURES[j]
        resp = fig1.cross(fig2)
        print(resp)
        return resp

    @eel.expose
    def create_figure(cls: str, x: list, y: list, r=None):
        x = [int(i) for i in x]
        y = [int(i) for i in y]
        if r is not None:
            r = int(r)
        if cls in ["Многоугольник", "Четырёхугольник", "Треугольник", "Прямоугольник", "Трапеция"]:
            for i in range(len(x) - 1):
                eel.draw_line(x[i], y[i], x[i + 1], y[i + 1])
            eel.draw_line(x[0], y[0], x[len(x) - 1], y[len(x) - 1])
            if cls == "Многоугольник":
                fig = NGon(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            elif cls == "Четырёхугольник":
                fig = QGon(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            elif cls == "Треугольник":
                fig = TGon(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            elif cls == "Прямоугольник":
                fig = Rectangle(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            elif cls == "Трапеция":
                fig = Trapeze(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            FIGURES.append(fig)
            return {"id": len(FIGURES) - 1,
                    "name": fig.__str__(),
                    "x": [point.x[0] for point in fig.p],
                    "y": [point.x[1] for point in fig.p],
                    "length": round(fig.length(), 2),
                    "square": round(fig.square(), 2)}
        elif cls in ["Прямая", "Ломаная"]:
            for i in range(len(x) - 1):
                eel.draw_line(x[i], y[i], x[i + 1], y[i + 1])
            if cls == "Прямая":
                fig = Segment(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            else:
                fig = Polyline(points=[Point2d(coord=[x[i], y[i]]) for i in range(len(x))])
            FIGURES.append(fig)
            return {"id": len(FIGURES) - 1,
                    "name": fig.__str__(),
                    "x": [point.x[0] for point in fig.p],
                    "y": [point.x[1] for point in fig.p],
                    "length": round(fig.length(), 2)}
        elif cls == "Круг":
            fig = Circle(point=Point2d([x[0], y[0]]), r=r)
            eel.draw_circle(x[0], y[0], r)
            FIGURES.append(fig)
            return {"id": len(FIGURES) - 1,
                    "name": fig.__str__(),
                    "x": x[0],
                    "y": y[0],
                    "r": r,
                    "length": round(fig.length(), 2),
                    "square": round(fig.square(), 2)}

    eel.start("main.html", port=5000, size=(700, 620))


if __name__ == "__main__":
    main()
