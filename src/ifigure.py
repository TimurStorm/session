from math import pi

from src.ishape import Segment, TGon, QGon
from src.point import Point3d


def plos(points: list):
    """
    Возвращает координаты плоскости в пространстве
    """
    line1 = Segment(points=[points[0], points[1]])
    line2 = Segment(points=[points[0], points[2]])
    A = line1.coord[1] * line2.coord[2] - line1.coord[2] * line2.coord[1]
    B = line1.coord[2] * line2.coord[0] - line1.coord[0] * line2.coord[2]
    C = line1.coord[0] * line2.coord[1] - line1.coord[1] * line2.coord[0]
    D = -1*points[0].x[0] * A - points[0].x[1] * B - points[0].x[2] * C
    return [A, B, C, D]


class Pyramid:
    def __init__(self, p0: Point3d or None, n: int, p: list):
        if p0 is None:
            self.p0 = p[0]
            del p[0]
        else:
            self.p0 = p0
        assert (
            n != len(p) + 1
        ), "Конфликт данных: количество точек не соответствует действительности"
        self.p = p

        assert n >= 4, "Ожидалось что количество точек будет больше или равно 4"
        self.n = n

    def print_points(self):
        print(f"Вершина пирамиды: {self.p0}")
        print(f"Количество точек: {self.n}")
        print("Точки: ")
        for point in self.p:
            print(point)

    def square(self):
        s = 0
        s += QGon(points=self.p).square()
        for i in range(len(self.p)-1):
            line1 = Segment(points=[self.p0, self.p[i]])
            line2 = Segment(points=[self.p0, self.p[i+1]])
            cs = abs(sum([line1.coord[i]*line2.coord[i] for i in range(3)]))/(line2.module*line1.module)
            sn = (1-cs**2)**0.5
            s += line1.module * line2.module * 0.5 * sn
        line1 = Segment(points=[self.p0, self.p[len(self.p)-1]])
        line2 = Segment(points=[self.p0, self.p[0]])
        cs = abs(sum([line1.coord[i] * line2.coord[i] for i in range(3)])) / (line2.module * line1.module)
        sn = (1 - cs ** 2) ** 0.5
        s += line1.module * line2.module * 0.5 * sn
        s += TGon(points=[self.p0, self.p[0], self.p[len(self.p)-1]]).square()
        return s

    def __str__(self):
        return "Пирамида"

    def volume(self):
        points = [self.p[i] for i in range(3)]

        normal = plos(points=points)
        print(normal)
        d = [self.p0.x[i]*normal[i] for i in range(3)]
        d.append(normal[3])
        d = sum(d)/((sum([normal[i]**2 for i in range(3)]))**0.5)
        print(d)
        s = QGon(points=self.p).square()

        return (1/3)*d*s


class Ball:
    def __init__(self, r: float, p: Point3d):
        self.r = r
        self.p = p

    def __str__(self):
        return f"Шар"

    def print_points(self):
        print(f"Радиус шара: {self.r}")
        print(f"Центр шара: {self.p}")

    def square(self):
        return 4 * pi * (self.r ** 2)

    def volume(self):
        return 4 / 3 * pi * (self.r ** 3)



class Prism:
    def __init__(self, n: int, p1: list, p2: list):

        assert n % 2 == 0, " Число точек призмы чётно"
        assert n >= 6 or len(p1) >= 3 or len(p2) >= 3, "Недостаточно точек"
        assert len(p1) == len(p2), "Основания призмы не равны"
        assert n == len(p1) + len(
            p2
        ), "Конфликт данных: количество точек не соответствует действительности"

        self.n = n
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Призма"

    def print_points(self):
        print("Точки: ")
        print(f"Количество точек: {self.n}")
        print("Первая плоскость:")
        for point in self.p1:
            print(point)

        print("Вторая плоскость:")
        for point in self.p2:
            print(point)

    def square(self):
        s = 0
        a = int(self.n / 2 - 1)
        line1 = Segment(points=[self.p1[0],self.p2[0]])
        for i in range(a):
            line2 = Segment(points=[self.p1[i], self.p1[i+1]])
            cs = abs(sum([line1.coord[i] * line2.coord[i] for i in range(3)])) / (line2.module * line1.module)
            sn = (1 - cs ** 2) ** 0.5
            s += line1.module * line2.module * sn
        line2 = Segment(points=[self.p1[a], self.p1[0]])
        cs = abs(sum([line1.coord[i] * line2.coord[i] for i in range(3)])) / (line2.module * line1.module)
        sn = (1 - cs ** 2) ** 0.5
        s += line1.module * line2.module * sn
        if self.__str__() == "Призма":
            s += TGon(points=self.p1).square()
        else:
            s += QGon(points=self.p1).square()
        return s

    def volume(self):
        normal1 = plos(points=self.p1)
        normal2 = plos(points=self.p2)
        print(normal2, normal1)
        d = abs(normal1[3]-normal2[3])/(sum([normal1[i]**2 for i in range(3)])**0.5)
        print(d)
        if self.__str__() == "Призма":
            s = TGon(points=self.p1).square()
        else:
            s = QGon(points=self.p1).square()
        print(s)
        return d * s


class Parallelepiped(Prism):
    def __init__(self, p1, p2):
        super().__init__(p1=p1, p2=p2, n=8)

    def __str__(self):
        return "Параллелепипед"


