# Project Report - Alignment

## Baseline

### Design Experience

For my design experience I worked with Claire Daley and Megan Stone. We went over the basics of how the formula works. I planned to use basic 2d arrays for the scoring and traceback matrices. The rows would represent Sequence 1, and the columns would represent Sequence 2. Each cell would calculate the optimal alignment score using three possible operations: diagonal for a match or substitution, left for an insertion, and up for a deletion. This largly ended up working quite well however I did end up cutting out my helper functions and simply implmenting them directly in the code. I did this because I realised that there wasn't alot of use for having them pulled out as they are only ever used in there spot.  

### Theoretical Analysis - Unrestricted Alignment

#### Time 


```python
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
        # O(m) to construct gap * m

    if m == 0:
        return n * indel_penalty, seq1, gap * n
        # O(n) to construct gap * n

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    # O(nm) initialization

    traceback = [[None] * (m + 1) for _ in range(n + 1)]
    # O(nm) initialization

    for i in range(1, n + 1):
        dp[i][0] = i * indel_penalty
        traceback[i][0] = "U"

    for j in range(1, m + 1):
        dp[0][j] = j * indel_penalty
        traceback[0][j] = "L"

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # O(nm) total iterations

            if seq1[i - 1] == seq2[j - 1]:
                diagonal = dp[i - 1][j - 1] + match_award
            else:
                diagonal = dp[i - 1][j - 1] + sub_penalty

            left = dp[i][j - 1] + indel_penalty

            up = dp[i - 1][j] + indel_penalty

            best = min(diagonal, left, up)
            dp[i][j] = best

            if diagonal == best:
                traceback[i][j] = "D"
            elif left == best:
                traceback[i][j] = "L"
            else:
                traceback[i][j] = "U"

    aligned1 = []
    aligned2 = []

    i, j = n, m

    while i > 0 or j > 0:
        # O(n + m) maximum iterations

        direction = traceback[i][j]

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

    aligned1.reverse()
    aligned2.reverse()
    # O(n + m) combined

    return dp[n][m], "".join(aligned1), "".join(aligned2)
    # O(n + m) to construct output strings
```

The function fills each cell of the scoring matrix once in constant time per cell. Therefore, the time complexity is O(nm). The traceback takes as much as an additional O(n+m), so the time complexity is **O(nm)**

#### Space

```python
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
        # O(m) space for gap * m

    if m == 0:
        return n * indel_penalty, seq1, gap * n
        # O(n) space for gap * n

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    # O(nm) space

    traceback = [[None] * (m + 1) for _ in range(n + 1)]
    # O(nm) space

    for i in range(1, n + 1):
        dp[i][0] = i * indel_penalty
        traceback[i][0] = "U"

    for j in range(1, m + 1):
        dp[0][j] = j * indel_penalty
        traceback[0][j] = "L"

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            if seq1[i - 1] == seq2[j - 1]:
                diagonal = dp[i - 1][j - 1] + match_award
            else:
                diagonal = dp[i - 1][j - 1] + sub_penalty

            left = dp[i][j - 1] + indel_penalty

            up = dp[i - 1][j] + indel_penalty

            best = min(diagonal, left, up)
            dp[i][j] = best

            if diagonal == best:
                traceback[i][j] = "D"
            elif left == best:
                traceback[i][j] = "L"
            else:
                traceback[i][j] = "U"

    aligned1 = []
    aligned2 = []
    # O(n + m) worst-case space

    i, j = n, m

    while i > 0 or j > 0:

        direction = traceback[i][j]

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

    aligned1.reverse()
    aligned2.reverse()
    # O(1) auxiliary space for in-place reversal

    return dp[n][m], "".join(aligned1), "".join(aligned2)
    # O(n + m) output string space
```
The function stores two (n+1)\times(m+1) arrays. one for scores and one for traceback directions. Each matrix requires O(nm) space so the overall space complexity is **O(nm)**.

### Empirical Data - Unrestricted Alignment


| Size | Time (sec) |
| ---- | ---------- |
| 500  | 0.160      |
| 1000 | 0.687      |
| 1500 | 1.510      |
| 2000 | 2.738      |
| 2500 | 4.189      |
| 3000 | 6.066      |


### Comparison of Theoretical and Empirical Results - Unrestricted Alignment

- Theoretical order of growth: **O(n^2)**
- Empirical order of growth (if different from theoretical): matches Theoretical

![unbanded_align.svg](unbanded_align.svg)


## Core

### Design Experience

For my core design experience I worked with Claire Daley and Megan Stone. To add the ability to band the alignment I planned to modify the code that I had from the Baseline. This ended up working well however I ended up implementing it directly in place overiteting the code from before. My plan to use a compact matrix and a known offset to access the relative cells worked well although I had some initial issues with off by one errors.

### Theoretical Analysis - Banded Alignment

#### Time 

```python
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
        # O(m) to construct gap * m

    if m == 0:
        return n * indel_penalty, seq1, gap * n
        # O(n) to construct gap * n

    banded = banded_width != -1

    if banded:
        d = banded_width

        if d < 0:
            raise ValueError("banded_width must be -1 or nonnegative")

        if abs(n - m) > d:
            return math.inf, None, None

        width = 2 * d + 1

        dp = [[math.inf] * width for _ in range(n + 1)]
        # O(n(2d + 1)) initialization

        traceback = [[None] * width for _ in range(n + 1)]
        # O(n(2d + 1)) initialization

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
        # O(nm) initialization

        traceback = [[None] * (m + 1) for _ in range(n + 1)]
        # O(nm) initialization

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
            # K total iterations across all rows

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
        # O(n + m) maximum iterations

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
    # O(n + m) combined

    return score, "".join(aligned1), "".join(aligned2)
    # O(n + m) to construct the output strings
```
For banded alignment, the matrices have n+1 rows and 2d+1 columns. The loops only evaluate the cells in the band, but array initialization still takes O(n(2d+1)). The row and column loops take O(n+m). Therefore, for a valid banded alignment, the total time is **O(n(2d+1)+n+m)**.

#### Space

```python
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
        # O(m) space for the new gap string

    if m == 0:
        return n * indel_penalty, seq1, gap * n
        # O(n) space for the new gap string

    banded = banded_width != -1

    if banded:
        d = banded_width

        if d < 0:
            raise ValueError("banded_width must be -1 or nonnegative")

        if abs(n - m) > d:
            return math.inf, None, None

        width = 2 * d + 1

        dp = [[math.inf] * width for _ in range(n + 1)]
        # O(n(2d + 1)) space

        traceback = [[None] * width for _ in range(n + 1)]
        # O(n(2d + 1)) space

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
        # O(nm) space

        traceback = [[None] * (m + 1) for _ in range(n + 1)]
        # O(nm) space

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
    # O(n + m) combined worst-case space

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
    # O(1) auxiliary space for in-place reversal

    return score, "".join(aligned1), "".join(aligned2)
    # O(n + m) output string space
```
In banded alignment each array contains (n+1)*(2d+1) entries. This takes up O(n(2d+1)). The output lists and strings require O(n+m) space. That leaves a total space complexity of **O(n(2d+1)+n+m)**

### Empirical Data - Banded Alignment

|  Size  | Time (sec) |
| ------ | ---------- |
| 100    | 0.000596   |
| 1000   | 0.00643    |
| 5000   | 0.0353     |
| 10000  | 0.0705     |
| 15000  | 0.105      |
| 20000  | 0.137      |
| 25000  | 0.178      |
| 30000  | 0.211      |

### Comparison of Theoretical and Empirical Results - Banded Alignment

- Theoretical order of growth: **O(n(b+1)+n+n)**
- Empirical order of growth (if different from theoretical): Matches


![banded_align.svg](banded_align.svg)

### Relative Performance Of Unrestricted Alignment versus Banded Alignment

Banded runs in basicaly linear time compared to the exponential time of Unrestricted


## Stretch 1

### Design Experience

For my Stretch 1 design experience I worked with Claire Daley and Megan Stone. While planning this I planned to use my preexisting code from core to analyse the data from the file. My colaborators and I agreed that we thought the Mice did it. However, the actual comparison showed that the rats were the most likely perpetrators with an alignment score of -4343 and approximately 99.80% sequence match.

### Code

```python
    from alignment import align

SPECIES = {
    "hg38": "Human - Little Jack",
    "panTro4": "Chimpanzee - Bobby and Darla",
    "rheMac3": "Rhesus macaque - Rembrandt",
    "canFam3": "Dog - Zeus",
    "rn5": "Rat - Remy, Emile, and Django",
    "mm10": "Mouse - Zoo mice",
}


def read_fasta(filename):
    sequences = {}
    current_header = None

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                current_header = line[1:].split()[0]
                sequences[current_header] = ""
            else:
                sequences[current_header] += line.upper()

    return sequences


def main():
    sequences = read_fasta("lct_exon8.txt")

    unknown_header = next(
        header for header in sequences
        if header.split("_")[1] == "unknown"
    )

    unknown = sequences[unknown_header]

    results = []

    for header, sequence in sequences.items():

        species_code = header.split("_")[1]

        if species_code == "unknown":
            continue

        score, aligned_unknown, aligned_species = align(
            unknown,
            sequence,
            match_award=-3,
            indel_penalty=5,
            sub_penalty=1,
            banded_width=-1
        )

        # Count matches, excluding gaps.
        matches = sum(
            a == b and a != "-"
            for a, b in zip(aligned_unknown, aligned_species)
        )

        compared = sum(
            a != "-" and b != "-"
            for a, b in zip(aligned_unknown, aligned_species)
        )

        identity = (matches / compared) * 100 if compared else 0

        results.append({
            "species": SPECIES[species_code],
            "score": score,
            "matches": matches,
            "identity": identity
        })

    results.sort(key=lambda result: result["score"])

    print("\nDNA COMPARISON RESULTS")
    print("-" * 65)

    for result in results:
        print(f"Species: {result['species']}")
        print(f"Score: {result['score']}")
        print(f"Matches: {result['matches']}")
        print(f"Identity: {result['identity']:.2f}%")
        print("-" * 65)

    print("\nMost likely match:")
    print(results[0]["species"])
```

### Alignment Scores

| Species | Animal Name(s) | Alignment Score | Matches | Identity |
|---|---|---:|---:|---:|
| Rat | Remy, Emile, and Django | -4343 | 1507 | 99.80% |
| Mouse | Zoo mice | -3835 | 1380 | 91.39% |
| Rhesus macaque | Rembrandt | -3162 | 1214 | 80.45% |
| Human | Little Jack | -3113 | 1204 | 79.84% |
| Dog | Zeus | -3111 | 1199 | 79.40% |
| Chimpanzee | Bobby and Darla | -3097 | 1200 | 79.58% |

## Stretch 2

### Design Experience

For my Stretch 2 design experience I worked with Claire Daley and Megan Stone. We talked about the process of implimenting Smith–Waterman and decided that the bes way would likely be to adapt the code from Needleman-Wunsch. This mostly ended up working however I had a larger then hoped portion that it was easiest to just build over again to avoid dealing with some of the conflicts btought about be the differences the algorithms have.

### Alignment Outcome Comparisons

##### Sequences and Alignments

*Fill me in*

##### Chosen Parameters and Better Alignments Discussion

*Fill me in*

## Project Review

For my Review I worked with Owen Wertz. For both of us baseline was a simple implementation with a basic 2d array. For Core He used dictionaries rather than an offset to allow for the banding. He had some issues getting some of his alignments figured. We both ended up using letter codes in the traceback array rather then trying to properly use pointers for ease of use. For Stretch 1 Owen didn't get to this point, so I just shared my progress with him. We also talked a bit about the issues that I had with getting my file parser going. Lastly for Stretch 2 we discussed the differences between Needleman and Waterman and how they are used. Similarly to stretch 2 Owen didn't get here either.
