import math
from numpy import cross, linalg


class Point:
    def __init__(self, dim: int, coord: list or None):
        self.dim = dim
        assert (
                type(coord) == list or coord is None
        ), "Недопустимый формат координат, укажите координаты в виде массива численных переменных"
        if coord is None:
            self.x = [0] * dim
        else:
            assert (
                    len(coord) == dim or coord is None
            ), "Количество координат не соответствует размерности пространства"
            self.x = coord

    def __str__(self):
        return "..." + f"Точка с координатами: {self.x}"

    def dim_two_points(self, point2):
        """
        Проверка на соответствие размерностей двух точек
        """
        assert self.dim == point2.dim, "Размерности пространств точек не совпадают"

    def module_radius_vector(self):
        """
        Модуль радиус вектора
        """
        return sum([coord ** 2 for coord in self.x]) ** 0.5

    def sum_two_points(self, point2):
        """
        Сумма 2 точек
        """
        self.dim_two_points(point2)
        self.x = [self.x[i] + point2.x[i] for i in range(self.dim)]

    def raz_two_points(self, point2):
        """
        Разность 2 точек
        """
        self.dim_two_points(point2)
        new_point = Point(
            dim=self.dim, coord=[self.x[i] - point2.x[i] for i in range(self.dim)]
        )
        return new_point

    def multi_two_points(self, point2):
        """
        Скалярное произведение
        """
        self.dim_two_points(point2)
        return sum([self.x[i] * point2.x[i] for i in range(self.dim)])

    def multi_by_number(self, num: int or float):
        """
        Умножение координат на число
        """
        assert (
                type(num) == int or type(num) == float
        ), f"Невозможно умножить точку на объект {type(num)}"
        new_point = Point(dim=self.dim, coord=self.x)
        new_point.x = [num * coord for coord in self.x]
        return new_point

    def sym_axis(self, num: int):
        """
        Симметричная точка
        """
        ar = self.x
        for i in range(len(ar)):
            if i != num:
                ar[i] *= -1
        self.x = ar


class Point2d(Point):
    def __init__(self, coord, dim=2):
        super().__init__(dim, coord)

    def __str__(self):
        return "..." + f"Точка с координатами: {self.x}"

    def rotate(self, phi):
        """
        Поворот
        """
        x, y = self.x[0], self.x[1]
        self.x[0] = round(math.cos(phi) * x - math.sin(phi) * y, 6)
        self.x[1] = round(math.sin(phi) * x + math.cos(phi) * y, 6)


class Point3d(Point):
    def __init__(self, coord, dim=3):
        super().__init__(dim, coord)

    def __str__(self):
        return "..." + f"Точка с координатами: {self.x}"

    def cross_prod(self, point2):
        """
        Векторное произведение
        """
        self.dim_two_points(point2)
        return cross(self.x, point2.x)

    def mix_prod(self, point2, point3):
        """
        Смешанное произведение
        """
        self.dim_two_points(point2)
        return linalg.det([self.x, point2.x, point3.x])

    def convert(self):
        return Point2d([self.x[i] for i in range(2)])
