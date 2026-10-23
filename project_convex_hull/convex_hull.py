# Uncomment this line to import some functions that can help
# you debug your algorithm

from plotting import draw_line, draw_hull, circle_point



def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    points = sorted(set(points))

    if not points:
        return []

    return divideAndConquer(points)


def divideAndConquer(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) <= 3:
        return baseHull(points)

    mid = len(points) // 2

    leftHull = divideAndConquer(points[:mid])
    rightHull = divideAndConquer(points[mid:])

    return mergeHulls(leftHull, rightHull)


def baseHull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) <= 2:
        return points[:]

    a, b, c = points
    orientation = cross(a, b, c)

    if (orientation > 0):
        return [a, b, c]
    elif (orientation < 0):
        return [a, c, b]
    else:
        return [a, c]


def findUpperTangent(left, right):
    i = max(range(len(left)), key=lambda k: (left[k][0], left[k][1]))
    j = min(range(len(right)), key=lambda k: (right[k][0], -right[k][1]))

    changed = True

    while (changed):
        changed = False

        while (cross(right[j], left[i], left[nextIndex(i, left)]) < 0):
            i = nextIndex(i, left)
            changed = True

        while (cross(left[i], right[j], right[prevIndex(j, right)]) > 0):
            j = prevIndex(j, right)
            changed = True

    return i, j


def findLowerTangent(left, right):
    i = max(range(len(left)), key=lambda k: (left[k][0], -left[k][1]))
    j = min(range(len(right)), key=lambda k: (right[k][0], right[k][1]))

    changed = True

    while changed:
        changed = False

        while (cross(right[j], left[i], left[prevIndex(i, left)]) > 0):
            i = prevIndex(i, left)
            changed = True

        while (cross(left[i], right[j], right[nextIndex(j, right)]) < 0):
            j = nextIndex(j, right)
            changed = True

    return i, j


def mergeHulls(left, right):
    upperLeft, upperRight = findUpperTangent(left, right)
    lowerLeft, lowerRight = findLowerTangent(left, right)

    merged = []

    # Left hull
    i = upperLeft

    while True:
        merged.append(left[i])

        if( i == lowerLeft):
            break

        i = nextIndex(i, left)

    # Right hull
    i = lowerRight

    while True:
        merged.append(right[i])

        if( i == upperRight):
            break

        i = nextIndex(i, right)

    return merged


def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))


def nextIndex(i, hull):
    return (i + 1) % len(hull)


def prevIndex(i, hull):
    return (i - 1) % len(hull)

def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull using Jarvis March."""

    points = sorted(set(points))

    if len(points) <= 2:
        return points

    # Start at the leftmost point (lowest y breaks ties).
    start = points[0]
    current = start
    hull = []

    while True:
        hull.append(current)

        candidate = points[0] if points[0] != current else points[1]

        for point in points:
            if point == current or point == candidate:
                continue

            orientation = cross(current, candidate, point)

            if orientation < 0:
                candidate = point
            elif orientation == 0:
                candidate_distance = (
                    (candidate[0] - current[0]) ** 2
                    + (candidate[1] - current[1]) ** 2
                )
                point_distance = (
                    (point[0] - current[0]) ** 2
                    + (point[1] - current[1]) ** 2
                )

                if point_distance > candidate_distance:
                    candidate = point

        current = candidate

        if current == start:
            break

    return hull
