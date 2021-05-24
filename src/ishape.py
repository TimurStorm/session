from shapely.geometry import LineString
from point import Point2d
from math import pi


class IShape:
    def print_points(self):
        print("Точки: ")
        for point in self.p:
            print(point)

    def length(self):
        """
        Длина периметра
        """
        n = len(self.p)
        return sum(
            [
                (
                    ((self.p[i].x[0] - self.p[i - 1].x[0]) ** 2)
                    + (self.p[i].x[1] - self.p[i - 1].x[1]) ** 2
                )
                ** 0.5
                for i in range(n)
            ]
        )

    def shift(self, point2):
        """
        Двигает фигуру
        """
        if type(self.p) is list:
            self.p = [point.sum_two_points(point2) for point in self.p]
        else:
            self.p = self.p.sum_two_points(point2)

    def rotate(self, phi):
        """
        Вращает фигуру
        """
        if type(self.p) is list:
            for point in self.p:
                point.rotate(phi=phi)
        else:
            self.p.rotate(phi)

    def sym_axis(self, num: int):
        """
        Строит симметричную фигуру
        """
        if type(self.p) is list:
            for point in self.p:
                point.x[num] *= -1
        else:
            self.p.x[num] *= -1

    def print_params(self):
        return self.length(), self.square()


class Segment(IShape):
    def __init__(self, points: list):
        assert (
            len(points) == 2
        ), "Ожидалось 2 точки, получены неверные данные для прямой"
        self.start = points[0]
        self.finish = points[1]
        self.p = points
        self.coord = [
            self.finish.x[i] - self.start.x[i] for i in range(len(self.start.x))
        ]
        self.coord.append(
            -1
            * (self.start.x[0] * self.finish.x[1] + self.start.x[1] * self.finish.x[0])
        )
        self.module = (
            sum([self.coord[i] ** 2 for i in range(len(self.coord) - 1)]) ** 0.5
        )


    def square(self):
        return 0

    def length(self):
        """
        Длина периметра
        """
        return self.module

    def __str__(self):
        return "Прямая"

    def print_points(self):
        print("Точки: ")
        print(self.start)
        print(self.finish)

    def cross(self, fig1):
        A = tuple(self.start.x)
        B = tuple(self.finish.x)
        C = tuple(fig1.start.x)
        D = tuple(fig1.finish.x)
        line1 = LineString([A, B])
        line2 = LineString([C, D])

        int_pt = line1.intersection(line2)
        try:
            print(f"Пересечение: {Point2d(coord=[int_pt.x, int_pt.y])}")
            return True
        except Exception:
            return False


class Polyline(IShape):
    def __init__(self, points: list):
        self.n = len(points)
        self.p = points

    def __str__(self):
        return "Ломаная"

    def length(self):
        le = 0
        for point_id in range(self.n - 1):
            le += Segment(points=[self.p[point_id], self.p[point_id + 1]]).module

        return le

    def square(self):
        return 0

    def cross(self, fig2):
        for point_id in range(self.n - 1):
            line = Segment(points=[self.p[point_id], self.p[point_id + 1]])
            for cross_id in range(fig2.n - 1):
                cross_line = Segment(points=[fig2.p[cross_id], fig2.p[cross_id + 1]])
                if cross_line.cross(line) is not False:
                    return True
        return False


class Circle(IShape):
    def __init__(self, r: int, point: Point2d):
        self.r = r
        self.po = point
        self.p = [point]


    def square(self):
        return pi * (self.r ** 2)

    def length(self):
        return 2 * pi * self.r

    def cross(self, fig1):
        if fig1.__str__() == "Круг":
            x1 = self.po.x[0]
            y1 = self.po.x[1]
            x2 = fig1.po.x[0]
            y2 = fig1.po.x[1]
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < (self.r + fig1.r) ** 2:
                return True
            return False

    def __str__(self):
        return f"Круг"

    def print_points(self):
        print(f"Радиус: {self.r}")
        print("Центр окружности:")
        print(self.po)


class NGon(IShape):
    def __init__(self, points: list):
        self.p = points
        self.n = len(self.p)

    def __str__(self):
        return f"Многоугольник"

    def square(self):
        """
        Площадь фигуры формулой Гаусса
        """
        sum1 = sum([self.p[i].x[0] * self.p[i + 1].x[1] for i in range(self.n - 1)])
        sum2 = sum([self.p[i + 1].x[0] * self.p[i].x[1] for i in range(self.n - 1)])
        s = 0.5 * abs(
            sum1
            - sum2
            + self.p[self.n - 1].x[0] * self.p[0].x[1]
            - self.p[0].x[0] * self.p[self.n - 1].x[1]
        )
        return s

    def cross(self, fig1):
        for point_id in range(self.n - 1):
            line = Segment(points=[self.p[point_id], self.p[point_id + 1]])
            for cross_id in range(fig1.n - 1):
                cross_line = Segment(points=[fig1.p[cross_id], fig1.p[cross_id + 1]])
                if line.cross(cross_line):
                    return True
        line = Segment(points=[self.p[self.n - 1], self.p[0]])
        for cross_id in range(fig1.n - 1):
            cross_line = Segment(points=[fig1.p[cross_id], fig1.p[cross_id + 1]])
            if line.cross(cross_line):
                return True
        return False


class TGon(NGon):
    def __init__(self, points: list):
        assert (
            len(points) == 3
        ), "Ожидалось 3 точки, получены неверные данные для треугольника"
        super().__init__(points)

    def square(self):
        line1 = Segment(points=[self.p[1], self.p[0]]).module
        line2 = Segment(points=[self.p[2], self.p[1]]).module
        line3 = Segment(points=[self.p[2], self.p[0]]).module

        p = self.length()/2

        return (p*(p-line1)*(p-line2)*(p-line3))**0.5

    def __str__(self):
        return f"Треугольник"


class QGon(NGon):
    def __init__(self, points: list):
        assert (
            len(points) == 4
        ), "Ожидалось 4 точки, получены неверные данные для четырёхугольника"
        super().__init__(points)

    def square(self):
        line1 = Segment(points=[self.p[0], self.p[2]])
        line2 = Segment(points=[self.p[1], self.p[3]])
        try:
            cos = (
                line1.coord[0] * line2.coord[0] + line1.coord[1] * line2.coord[1]
            ) / (line1.module * line2.module)
        except ZeroDivisionError:
            print("тебе повезло, попытка деления на ноль")
            return 0
        sin = (1 - cos ** 2) ** 0.5
        return 0.5 * sin * line1.module * line2.module

    def __str__(self):
        return f"Четырёхугольник"


class Rectangle(QGon):
    def __init__(self, points: list):
        assert (
            len(points) == 4
        ), "Ожидалось 4 точки, получены неверные данные для четырёхугольника"
        lines = [
            Segment(points=[points[0], points[1]]),
            Segment(points=[points[1], points[2]]),
            Segment(points=[points[2], points[3]]),
            Segment(points=[points[3], points[0]]),
        ]
        for id_line in range(len(lines)):
            if id_line != 3:
                s = sum(
                    [
                        lines[id_line].coord[i] * lines[id_line + 1].coord[i]
                        for i in range(len(lines[id_line].coord) - 1)
                    ]
                )
                assert s == 0, "Указанные точки не образуют прямые под прямым углом"
            else:
                s = sum(
                    [
                        lines[3].coord[i] * lines[0].coord[i]
                        for i in range(len(lines[id_line].coord) - 1)
                    ]
                )
                assert s == 0, "Указанные точки не образуют прямые под прямым углом"
        super().__init__(points)

    def square(self):
        line1 = Segment(points=[self.p[0], self.p[1]])
        line2 = Segment(points=[self.p[1], self.p[2]])
        return sum(
            [line1.coord[i] ** 2 for i in range(len(line1.coord) - 1)]
        ) ** 0.5 * (
            sum([line2.coord[i] ** 2 for i in range(len(line2.coord) - 1)]) ** 0.5
        )

    def __str__(self):
        return "Прямоугольник"


class Trapeze(QGon):
    def __init__(self, points: list):
        line1 = Segment(points=[points[0], points[1]])
        line2 = Segment(points=[points[2], points[3]])
        coord1 = [abs(i) for i in line1.coord]
        coord2 = [abs(i) for i in line2.coord]
        coord3 = []
        for i in range(len(coord2) - 1):
            if (coord2[i] != 0 and coord1[i] != 0) or coord2[i] != 0:
                coord3.append(coord1[i] / coord2[i])
        assert (
            coord1 == coord2 or len(set(coord3)) == 1
        ), "Ожидаемый порядок точек нарушен, попробуйте ввести точки иначе"
        super().__init__(points)

    def __str__(self):
        return f"Трапеция"
