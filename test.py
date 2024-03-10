def two(x, y):
    return (x, y)


def one():
    x, y = two(2, 3)
    print(x, y, x + y)


one()
