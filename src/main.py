from src.ishape import *
from src.ifigure import *
from src.paint import material

all_2d_figure = []
all_3d_figure = []

all_2d_figure.append(Circle(r=1, point=Point2d(coord=[1, 1])))
all_2d_figure.append(
    NGon(
        points=[
            Point2d(coord=[1, 1]),
            Point2d(coord=[2, 3]),
            Point2d(coord=[4, 6]),
            Point2d(coord=[3, 0]),
            Point2d(coord=[1, 0]),
        ]
    )
)
all_2d_figure.append(
    TGon(
        points=[
            Point2d(coord=[1, 5]),
            Point2d(coord=[2, 10]),
            Point2d(coord=[3, 8]),
        ]
    )
)
all_2d_figure.append(
    QGon(
        points=[
            Point2d(coord=[5, 7]),
            Point2d(coord=[9, 8]),
            Point2d(coord=[10, 3]),
            Point2d(coord=[2, 2]),
        ]
    )
)
all_2d_figure.append(
    Rectangle(
        points=[
            Point2d(coord=[0, 4]),
            Point2d(coord=[8, 10]),
            Point2d(coord=[11, 6]),
            Point2d(coord=[3, 0]),
        ]
    )
)

all_2d_figure.append(
    Trapeze(
        points=[
            Point2d(coord=[-1, 4]),
            Point2d(coord=[1, 10]),
            Point2d(coord=[5, 9]),
            Point2d(coord=[2, 0]),
        ]
    )
)

all_2d_figure.append(Segment(points=[Point2d(coord=[0, 2]), Point2d(coord=[1, 1])]))

all_2d_figure.append(
    Polyline(
        points=[Point2d(coord=[0, 3]), Point2d(coord=[2, 1]), Point2d(coord=[1, 1])]
    )
)

all_3d_figure.append(
    Pyramid(
        p0=Point3d(coord=[1, 3, 5]),
        n=4,
        p=[
            Point3d(coord=[0, 1, 0]),
            Point3d(coord=[2, 3, 4]),
            Point3d(coord=[2, 3, 3]),
            Point3d(coord=[1, 2, 1]),
        ],
    )
)

all_3d_figure.append(Ball(r=2, p=Point3d(coord=[1, 1, 1])))

all_3d_figure.append(
    Prism(
        n=6,
        p1=[
            Point3d(coord=[0, 0, 1]),
            Point3d(coord=[2, 3, 2]),
            Point3d(coord=[3, 4, 1]),
        ],
        p2=[
            Point3d(coord=[1, 1, 2]),
            Point3d(coord=[3, 4, 3]),
            Point3d(coord=[4, 5, 2]),
        ],
    )
)

all_3d_figure.append(
    Parallelepiped(
        p1=[
            Point3d(coord=[1, 2, 0]),
            Point3d(coord=[3, 3, 1]),
            Point3d(coord=[5, 3, 3]),
            Point3d(coord=[3, 2, 2]),
        ],
        p2=[
            Point3d(coord=[2, 3, 1]),
            Point3d(coord=[4, 4, 2]),
            Point3d(coord=[6, 4, 4]),
            Point3d(coord=[4, 3, 3]),
        ],
    )
)


def d_figure_params():
    s_2d = 0
    l_2d = 0
    for figure in all_2d_figure:
        print("")
        print(f"Фигура: {figure}")
        figure.print_points()
        l, s = figure.print_params()
        print(f"......Площадь: {s}")
        print(f"......Периметр: {l}")
        s_2d += s
        l_2d += l
    print("==========Параметры==========")
    print(f"Суммарная площадь: {s_2d}")
    print(f"Средняя площадь: {s_2d / (len(all_2d_figure) - 2)}")
    print(f"Суммарный периметр: {l_2d}")
    print("=============================")


def d_cross_figure_params():
    for figure in all_2d_figure:
        print(figure)
        points = []
        """
        figure.__str__() == "Круг" ---> True
        """
        if figure.__str__() in ["Ломаная"]:
            if figure.__str__() == "Круг":
                count = 1
            elif figure.__str__() == "Отрезок":
                count = 2
            else:
                count = len(figure.p)

            for point_id in range(count):
                points.append(Point2d(coord=[float(input("Координата x: ")), float(input("Координата y: "))]))
            if figure.__str__() == "Круг":
                cross_figure = figure.__class__(point=points[0], r=float(input("Радиус круга: ")))
            else:
                cross_figure = figure.__class__(points=points)

            cross_figure.print_points()
            l, s = cross_figure.print_params()
            print(f"......Площадь: {s}")
            print(f"......Периметр: {l}")
            print("")

            print("--------------------")
            per = figure.cross(cross_figure)
            if per:
                resp = "Пересекаются"
                print("Пересекаются")
            else:
                resp = "Не пересекаются"
                print("Не пересекаются")
            print("--------------------")
            material(figure, cross_figure, resp)
            go = ["поворот", "сдвиг", "симметрия"]
            ch = input(f"Введите тип передвижения({go}): ")

            if ch == "поворот":
                cross_figure.rotate(phi=float(input("Угол поворота: ")))
            elif ch == "сдвиг":
                cross_figure.shift(Point2d(coord=[float(input("Координата x: ")), float(input("Координата y: "))]))
            elif ch == "симметрия":
                cross_figure.sym_axis(int(input("Тип передвижения: ")))
            input()
            cross_figure.print_points()

            material(figure, cross_figure, ch)


def t_figure_params():
    s_3d = 0
    v_3d = 0
    for figure in all_3d_figure:
        print(figure)
        figure.print_points()
        v = figure.volume()
        s = figure.square()
        print(f"......Площадь: {s}")
        print(f"......Объем: {v}")
        s_3d += s
        v_3d += v
        print("")
    print("==========Параметры==========")
    print(f"Суммарная площадь: {s_3d}")
    print(f"Суммарный объем: {v_3d}")
    print(f"Средний объем: {v_3d / len(all_3d_figure)}")
    print("=============================")


def main():
    d_figure_params()
    d_cross_figure_params()
    t_figure_params()


if __name__ == "__main__":
    main()
