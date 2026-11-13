import math


def align(
    seq1: str,
    seq2: str,
    match_award=-3,
    indel_penalty=5,
    sub_penalty=1,
    banded_width=-1,
    gap="-",
) -> tuple[float, str | None, str | None]:
    """
    Align seq1 against seq2 using Needleman-Wunsch
    Put seq1 on left (j) and seq2 on top (i)
    => matrix[i][j]
    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
    :param gap: the character to use to represent gaps in the alignment strings
    """

    n = len(seq1)
    m = len(seq2)

    if n == 0:
        return m * indel_penalty, gap * m, seq2
    if m == 0:
        return n * indel_penalty, seq1, gap * n

    banded = banded_width != -1

    if banded:
        d = banded_width

        if d < 0:
            raise ValueError("banded_width must be -1 or nonnegative")

        if abs(n - m) > d:
            return math.inf, None, None

        width = 2 * d + 1
        dp = [[math.inf] * width for _ in range(n + 1)]
        traceback = [[None] * width for _ in range(n + 1)]

        def get(matrix, i, j):
            offset = j - (i - d)
            if 0 <= i <= n and 0 <= offset < width:
                return matrix[i][offset]
            return math.inf

        def put(matrix, i, j, value):
            offset = j - (i - d)
            if 0 <= offset < width:
                matrix[i][offset] = value

    else:
        d = max(n, m)
        dp = [[math.inf] * (m + 1) for _ in range(n + 1)]
        traceback = [[None] * (m + 1) for _ in range(n + 1)]

        def get(matrix, i, j):
            if 0 <= i <= n and 0 <= j <= m:
                return matrix[i][j]
            return math.inf

        def put(matrix, i, j, value):
            matrix[i][j] = value

    put(dp, 0, 0, 0)

    for i in range(1, n + 1):
        if abs(i) <= d:
            put(dp, i, 0, i * indel_penalty)
            put(traceback, i, 0, "U")

    for j in range(1, m + 1):
        if abs(j) <= d:
            put(dp, 0, j, j * indel_penalty)
            put(traceback, 0, j, "L")

    for i in range(1, n + 1):

        start = max(1, i - d)
        end = min(m, i + d)

        for j in range(start, end + 1):

            if seq1[i - 1] == seq2[j - 1]:
                diagonal = get(dp, i - 1, j - 1) + match_award
            else:
                diagonal = get(dp, i - 1, j - 1) + sub_penalty

            left = get(dp, i, j - 1) + indel_penalty

            up = get(dp, i - 1, j) + indel_penalty

            best = min(diagonal, left, up)
            put(dp, i, j, best)

            if diagonal == best:
                put(traceback, i, j, "D")
            elif left == best:
                put(traceback, i, j, "L")
            else:
                put(traceback, i, j, "U")

    score = get(dp, n, m)

    if score == math.inf:
        return math.inf, None, None

    aligned1 = []
    aligned2 = []

    i, j = n, m

    while i > 0 or j > 0:

        direction = get(traceback, i, j)

        if direction == "D":
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1

        elif direction == "L":
            aligned1.append(gap)
            aligned2.append(seq2[j - 1])
            j -= 1

        elif direction == "U":
            aligned1.append(seq1[i - 1])
            aligned2.append(gap)
            i -= 1

        else:
            return math.inf, None, None

    aligned1.reverse()
    aligned2.reverse()

    return score, "".join(aligned1), "".join(aligned2)




def local_align(
    seq1: str,
    seq2: str,
    match_award=-3,
    indel_penalty=5,
    sub_penalty=3,
    banded_width=-1,
    gap="-",
) -> tuple[float, str | None, str | None]:
    """
    Align seq1 against seq2 using Smith-Waterman
    Put seq1 on left (j) and seq2 on top (i)
    => matrix[i][j]
    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
    :param gap: the character to use to represent gaps in the alignment strings
    """

    n = len(seq1)
    m = len(seq2)

    if n == 0 or m == 0:
        return 0, "", ""

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    traceback = [[None] * (m + 1) for _ in range(n + 1)]

    def get(matrix, i, j):
        if 0 <= i <= n and 0 <= j <= m:
            return matrix[i][j]
        return math.inf

    def put(matrix, i, j, value):
        matrix[i][j] = value

    best_score = 0
    best_i = 0
    best_j = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            if seq1[i - 1] == seq2[j - 1]:
                diagonal = get(dp, i - 1, j - 1) + match_award
            else:
                diagonal = get(dp, i - 1, j - 1) + sub_penalty

            left = get(dp, i, j - 1) + indel_penalty
            up = get(dp, i - 1, j) + indel_penalty

            best = min(diagonal, left, up, 0)

            put(dp, i, j, best)

            if best == 0:
                put(traceback, i, j, None)
            elif diagonal == best:
                put(traceback, i, j, "D")
            elif left == best:
                put(traceback, i, j, "L")
            else:
                put(traceback, i, j, "U")

            if best < best_score:
                best_score = best
                best_i = i
                best_j = j

    aligned1 = []
    aligned2 = []

    i = best_i
    j = best_j

    while i > 0 and j >= 0:

        if get(dp, i, j) == 0:
            break

        direction = get(traceback, i, j)

        if direction == "D":
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1

        elif direction == "L":
            aligned1.append(gap)
            aligned2.append(seq2[j - 1])
            j -= 1

        elif direction == "U":
            aligned1.append(seq1[i - 1])
            aligned2.append(gap)
            i -= 1

        else:
            break

    aligned1.reverse()
    aligned2.reverse()

    return best_score, "".join(aligned1), "".join(aligned2)
