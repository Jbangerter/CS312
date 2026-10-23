# Project Report - Convex Hull

## Baseline

### Design Discussion

*Fill me in*

### Theoretical Analysis - Convex Hull Divide-and-Conquer

#### Time 

```python
def compute_hull_dvcq(
    points: list[tuple[float, float]]
) -> list[tuple[float, float]]:

    points = sorted(set(points))   # O(n) 
                                   # O(u log u) to sort unique points

    if not points:                 # O(1)
        return []                  # O(1)

    return divideAndConquer(points)  # O(u log u) overall


def divideAndConquer(points):

    if len(points) <= 3:           # O(1)
        return baseHull(points)    # O(1), at most 3 points

    mid = len(points) // 2         # O(1)

    leftHull = divideAndConquer(
        points[:mid]               # O(n) to create the slice
    )

    rightHull = divideAndConquer(
        points[mid:]               # O(n) to create the slice
    )

    return mergeHulls(
        leftHull, rightHull
    )                              # O(n) per merge, assuming
                                   # linear tangent searches


def baseHull(points):

    if len(points) <= 2:           # O(1)
        return points[:]           # O(1), at most 2 points

    a, b, c = points               # O(1)
    orientation = cross(a, b, c)   # O(1)

    if orientation > 0:            # O(1)
        return [a, b, c]           # O(1)
    elif orientation < 0:          # O(1)
        return [a, c, b]           # O(1)
    else:
        return [a, c]              # O(1)


def findUpperTangent(left, right):

    i = max(
        range(len(left)),
        key=lambda k: (left[k][0], left[k][1])
    )                              # O(hL)

    j = min(
        range(len(right)),
        key=lambda k: (right[k][0], -right[k][1])
    )                              # O(hR)

    changed = True

    while changed:                 # O(hL + hR) total movement
        changed = False

        while cross(
            right[j], left[i], left[nextIndex(i, left)]
        ) < 0:                     # O(1) per check
            i = nextIndex(i, left) # O(1)
            changed = True

        while cross(
            left[i], right[j], right[prevIndex(j, right)]
        ) > 0:                     # O(1) per check
            j = prevIndex(j, right)  # O(1)
            changed = True

    return i, j                    # O(1)


def findLowerTangent(left, right):

    i = max(
        range(len(left)),
        key=lambda k: (left[k][0], -left[k][1])
    )                              # O(hL)

    j = min(
        range(len(right)),
        key=lambda k: (right[k][0], right[k][1])
    )                              # O(hR)

    changed = True

    while changed:                 # O(hL + hR) total movement
        changed = False

        while cross(
            right[j], left[i], left[prevIndex(i, left)]
        ) > 0:                     # O(1) per check
            i = prevIndex(i, left) # O(1)
            changed = True

        while cross(
            left[i], right[j], right[nextIndex(j, right)]
        ) < 0:                     # O(1) per check
            j = nextIndex(j, right)  # O(1)
            changed = True

    return i, j                    # O(1)


def mergeHulls(left, right):

    upperLeft, upperRight = findUpperTangent(
        left, right
    )                              # O(hL + hR)

    lowerLeft, lowerRight = findLowerTangent(
        left, right
    )                              # O(hL + hR)

    merged = []                    # O(1)

    # Left hull
    i = upperLeft

    while True:
        merged.append(left[i])     # O(1) 

        if i == lowerLeft:         # O(1)
            break

        i = nextIndex(i, left)     # O(1)

    # Right hull
    i = lowerRight

    while True:
        merged.append(right[i])    # O(1) 

        if i == upperRight:        # O(1)
            break

        i = nextIndex(i, right)    # O(1)

    return merged                  # O(hL + hR)


def cross(
    o: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float]
) -> float:

    return (
        (a[0] - o[0]) * (b[1] - o[1])
        - (a[1] - o[1]) * (b[0] - o[0])
    )                              # O(1)


def nextIndex(i, hull):
    return (i + 1) % len(hull)     # O(1)


def prevIndex(i, hull):
    return (i - 1) % len(hull)     # O(1)
```

To prepare the data we intialy remove any possible duplicates and then sort the the data. These take O(n) and O(n log n) respectively. Then the points are split in half recusivly and then merged into their corresponding hull. This takes O(n) time for each level. With this established we find the recurrence T(n)=2T(n/2)+O(n). Thus we have a total overall time complexity of **O(n log n)**.

#### Space
```python
def compute_hull_dvcq(
    points: list[tuple[float, float]]
) -> list[tuple[float, float]]:

    points = sorted(set(points))   # O(n) auxiliary space for the set
                                   # and O(u) for the sorted list

    if not points:                 # O(1) additional space
        return []                  # O(1)

    return divideAndConquer(points)


def divideAndConquer(points):

    if len(points) <= 3:           # O(1)
        return baseHull(points)    # O(1), at most 3 points

    mid = len(points) // 2         # O(1)

    leftHull = divideAndConquer(
        points[:mid]               # O(n) space for the slice
    )

    rightHull = divideAndConquer(
        points[mid:]               # O(n) space for the slice
    )

    return mergeHulls(
        leftHull, rightHull
    )                              # O(n) worst-case output space


def baseHull(points):

    if len(points) <= 2:
        return points[:]           # O(1), at most 2 points

    a, b, c = points               # O(1)
    orientation = cross(a, b, c)   # O(1)

    if orientation > 0:
        return [a, b, c]            # O(1)
    elif orientation < 0:
        return [a, c, b]            # O(1)
    else:
        return [a, c]               # O(1)


def findUpperTangent(left, right):

    i = max(
        range(len(left)),
        key=lambda k: (left[k][0], left[k][1])
    )                              # O(1)

    j = min(
        range(len(right)),
        key=lambda k: (right[k][0], -right[k][1])
    )                              # O(1)

    changed = True

    while changed:
        changed = False

        while cross(
            right[j], left[i], left[nextIndex(i, left)]
        ) < 0:
            i = nextIndex(i, left) # O(1)
            changed = True

        while cross(
            left[i], right[j], right[prevIndex(j, right)]
        ) > 0:
            j = prevIndex(j, right)  # O(1)
            changed = True

    return i, j                    # O(1)


def findLowerTangent(left, right):

    i = max(
        range(len(left)),
        key=lambda k: (left[k][0], -left[k][1])
    )                              # O(1) 

    j = min(
        range(len(right)),
        key=lambda k: (right[k][0], right[k][1])
    )                              # O(1) 

    changed = True

    while changed:
        changed = False

        while cross(
            right[j], left[i], left[prevIndex(i, left)]
        ) > 0:
            i = prevIndex(i, left) # O(1)
            changed = True

        while cross(
            left[i], right[j], right[nextIndex(j, right)]
        ) < 0:
            j = nextIndex(j, right)  # O(1)
            changed = True

    return i, j                    # O(1)


def mergeHulls(left, right):

    upperLeft, upperRight = findUpperTangent(
        left, right
    )                              # O(1)

    lowerLeft, lowerRight = findLowerTangent(
        left, right
    )                              # O(1)

    merged = []                    # O(hL + hR) space

    # Left hull
    i = upperLeft

    while True:
        merged.append(left[i])     # O(1)  space per item

        if i == lowerLeft:
            break

        i = nextIndex(i, left)     # O(1)

    # Right hull
    i = lowerRight

    while True:
        merged.append(right[i])    # O(1) space per item

        if i == upperRight:
            break

        i = nextIndex(i, right)    # O(1)

    return merged                  # O(hL + hR) output space


def cross(
    o: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float]
) -> float:

    return (
        (a[0] - o[0]) * (b[1] - o[1])
        - (a[1] - o[1]) * (b[0] - o[0])
    )                              # O(1)


def nextIndex(i, hull):
    return (i + 1) % len(hull)     # O(1)


def prevIndex(i, hull):
    return (i - 1) % len(hull)     # O(1)
```

We store the unique points, sorted list, recursive slices, intermediate hulls, and merged output. each of these require no more then 0(n) Space each. In turn the recursion requires O(log n) space. In total overall space complexity is **O(n)**

## Core

### Design Discussion

All the tests worked well using initial baseline code.

### Empirical Data - Convex Hull Divide-and-Conquer

|  Size  | Time (ms) |
| ------ | --------- |
| 10     | 0.0342    |
| 100    | 0.293     |
| 1000   | 3.776     |
| 10000  | 34.932    |
| 20000  | 71.048    |
| 40000  | 141.154   |
| 50000  | 169.357   |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: **O(N * log(N))**
- Empirical order of growth (if different from theoretical): The empirical growth looks to be marginally lower than the calculated expected values. The difference isn't large and it looks to be off by some constant multiple of n. Based on that I believe that the cause of this may be that the data being passed during the test is pre sorted allowing to cut that portion of the proccess out.

![empirical.svg](empirical.svg)



## Stretch 1

### Design Discussion

I chose to implment Jarvis March as my secoundary alorithim. I am expecting it to be less efficent then DVCQ.

### Chosen Convex Hull Implementation Description

I chose to implement Jarvis March algorithm. This algorithm works by tacking the left most point in the data set and projecting a ray north. This ray is then rotated clockwise until it intersects another point in the dataset. This new point is then used as a new pivot point until the next point is intersected. This process continues until the algorithim gets back to ware it stated at the initial point at the left. All the points visited in this traversal form the convex hull.

O(nh), where n is the number of unique input points and h is the number of convex hull vertices. In the worst case, this is **O(n^2)**.

### Comparison of Chosen Algorithm with Divide-and-Conquer Convex Hull

#### Algorithmic Differences

Jarvis March and DVCQ use very different approaches algorithmicaly. DVCQ uses a divide and conquer solution to split the data into a series of smaller hulls that are easy to find the convex of. It then takes those subHulls and by combining them with other hulls around them is able to determine the final convex hull. On the other hand Jarvis March basically just circumnavigates the exterior of the hull by finding the edges that are the furthest away from the rest by rotating around the data.

#### Performance Differences
![dvcq_v_other1.svg](dvcq_v_other1.svg)

For performance Jarvis March is definitely the worse of the two algorithms for efficacy however it is usually able to perform suprisingly well on the data we are testing on. This is because it performs well when few points lie on the hull. The fewer points on the hull the closer it gets to O(N). As such I found one test case where it almost outperformed DVCQ. I wasn't able to get a similar sufficiently deviant bit of data so there isnt a graph of this sadly. On the other hand DVCQ performs very consistently at O(N log(N)).

## Stretch 2

### Design Discussion

I Determined that I wanted to see what I coud do with some wildfire data sets. It seemed like an interesting opportunity to do somthing that often has real impact here in utah.

### Dataset 

I found a data set for a wild fires in California. I ended up needing to use chat to figure out hoe to parse the data as it was in some very weird formats. After the data was removed and parsed I realised that convex hulls are actually very pore ways to estimate the impact area of wildfire as they often form highly abnormal shapes(See image 3). Despite this imperfection there is some use for Convex hulls as a safey margin or somthing similar to warn people of impending risks that are posed.

![dixie_hull_2021-07-15.png](dixie_hull_2021-07-15.png)
![dixie_hull_2021-08-20.png](dixie_hull_2021-08-20.png)
![dixie_hull_2021-09-27.png](dixie_hull_2021-09-27.png)

## Project Review

I talked with Mason Lewis about his project. We had very similar methods for baseline and Core. We both chose to implement Jarvis march. Due to its simplicity those were also similar. I was able to help explain how it works to him using an example I found while researching for this project. For his Stretch 2 he implmented the Covid data set. Convex hulls worked very well for him as a method for determing the total distance and area effected across various times.

