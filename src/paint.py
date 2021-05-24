import matplotlib.pyplot as plt


def material(fig1, fig2, resp):
    fig, ax = plt.subplots()
    plt.axhline(linewidth=1, color='k')
    plt.axvline(linewidth=1, color='k')
    plt.grid()
    ax.set_xlim((-20, 20))
    ax.set_ylim((-20, 20))
    ax.set_title(fig1.__str__() + "( " + resp + " )")
    if fig1.__str__() != "Круг":
        x1 = [i.x[0] for i in fig1.p]
        x2 = [i.x[0] for i in fig2.p]
        y1 = [i.x[1] for i in fig1.p]
        y2 = [i.x[1] for i in fig2.p]
        if fig1.__str__() not in ("Отрезок", "Ломаная"):
            x1.append(fig1.p[0].x[0])
            x2.append(fig2.p[0].x[0])
            y1.append(fig1.p[0].x[1])
            y2.append(fig2.p[0].x[1])
        # Create a Rectangle patch
        plt.plot(x1, y1, x2, y2, marker="o")
        plt.show()
    else:
        circle1 = plt.Circle(fig1.p.x, fig1.r, color="r")
        circle2 = plt.Circle(fig2.p.x, fig2.r, color="blue")

        ax.add_artist(circle1)
        ax.add_artist(circle2)
        plt.show()
