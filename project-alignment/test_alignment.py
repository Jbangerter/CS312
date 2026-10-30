# ---------------------------------- Imports --------------------------------- #
import math
from pathlib import Path

import pytest
from byu_pytest_utils import with_import, test_files, tier

from test_utils import Timer, run_with_timeout

# -------------------------------- Test tiers -------------------------------- #
baseline = tier("baseline", 1)
core = tier("core", 2)
stretch2 = tier("stretch2", 3)


# ----------------------------- Global variables ----------------------------- #
def read_sequence(file: Path) -> str:
    return "".join(file.read_text().splitlines())

alignment_file = "alignment"

# ------------------------------- Baseline tests ------------------------------ #
@baseline
@with_import(alignment_file)
def test_small_alignment(align):
    score, aseq1, aseq2 = align("polynomial", "exponential")
    assert score == -1
    assert aseq1 == "polyn-omial"
    assert aseq2 == "exponential"


@baseline
@with_import(alignment_file)
def test_tiny_dna_alignment(align):
    score, aseq1, aseq2 = align("ATGCATGC", "ATGGTGC")
    assert score == -12
    assert aseq1 == "ATGCATGC"
    assert aseq2 == "ATG-GTGC"


@baseline
@with_import(alignment_file)
def test_tiny_dna_alignment_gaps(align):
    score, aseq1, aseq2 = align("ATATATATAT", "TATATATATA")
    assert score == -17
    assert aseq1 == "ATATATATAT-"
    assert aseq2 == "-TATATATATA"


@baseline
@with_import(alignment_file)
def test_small_dna_alignment_not_banded(align):
    score, aseq1, aseq2 = align("GGGGTTTTAAAACCCCTTTT", "TTTTAAAACCCCTTTTGGGG")
    assert score == -8
    assert aseq1 == "GGGGTTTTAAAACCCCTTTT----"
    assert aseq2 == "----TTTTAAAACCCCTTTTGGGG"


@baseline
@with_import(alignment_file)
def test_empty_sequences(align):
    score, aseq1, aseq2 = align("", "")
    assert score == 0
    assert aseq1 == ""
    assert aseq2 == ""


@baseline
@with_import(alignment_file)
def test_one_empty_sequence(align):
    score, aseq1, aseq2 = align("ACGT", "")
    assert score == 5 * 4  # Assuming gap penalty of 5
    assert aseq1 == "ACGT"
    assert aseq2 == "----"


@baseline
@with_import(alignment_file)
def test_identical_sequences(align):
    score, aseq1, aseq2 = align("GATTACA", "GATTACA")
    assert score == -21  # Assuming match score of -3
    assert aseq1 == "GATTACA"
    assert aseq2 == "GATTACA"


@baseline
@with_import(alignment_file)
def test_all_mismatch_sequences(align):
    score, aseq1, aseq2 = align("AAAA", "TTTT")
    assert score == 1 * 4  # Assuming mismatch penalty of 1
    assert aseq1 == "AAAA"
    assert aseq2 == "TTTT"


@baseline
@with_import(alignment_file)
def test_alignment_with_long_gaps(align):
    score, aseq1, aseq2 = align("ATTTATTTA", "AAA")
    assert aseq1 == "ATTTATTTA"
    assert aseq2 == "A---A---A"
    assert score == 21


@baseline
@with_import(alignment_file)
def test_different_match_score(align):
    score_default, a1_default, a2_default = align("ACGT", "ACGT")
    score_bonus, a1_bonus, a2_bonus = align("ACGT", "ACGT", match_award=-10)
    assert score_default == -12
    assert score_bonus == -40
    assert a1_bonus == a2_bonus == "ACGT"


@baseline
@with_import(alignment_file)
def test_different_indel_penalty(align):
    score_low_penalty, _, _ = align("ACGT", "AGT", indel_penalty=1)
    score_default_penalty, _, _ = align("ACGT", "AGT")
    score_high_penalty, _, _ = align("ACGT", "AGT", indel_penalty=10)
    assert score_low_penalty < score_default_penalty < score_high_penalty


@baseline
@with_import(alignment_file)
def test_different_substitution_penalty(align):
    score_default_sub, _, _ = align("ACGT", "AGT")
    score_high_sub, _, _ = align("AAAA", "TTTT", sub_penalty=10)
    assert score_default_sub < score_high_sub


@baseline
@with_import(alignment_file)
def test_tie_breaking(align):
    # generate a 3 way tie by modifying the match/sub awards
    score_3_way_tie, aseq1, aseq2 = align(
        "ABDE", "BADE", match_award=-2, sub_penalty=4, indel_penalty=5
    )
    assert aseq1 == "ABDE"
    assert aseq2 == "BADE"
    assert score_3_way_tie == 4

    score_diag_left_tie, bseq1, bseq2 = align("AA", "A")
    assert score_diag_left_tie == 2
    assert bseq1 == "AA"
    assert bseq2 == "-A"

    # generate another 2 way tie between left and up
    score_left_top_tie, cseq1, cseq2 = align("AT", "AG", sub_penalty=15)
    assert score_left_top_tie == 7
    assert cseq1 == "AT-"
    assert cseq2 == "A-G"


@baseline
@with_import(alignment_file)
def test_alignment_scoring_effects(align):
    # alignment with default parameters
    score_default, aseq1_default, aseq2_default = align("AAAA", "CCCC")

    # alignment with different scoring
    score_diff_scoring, aseq1_diff_scoring, aseq2_diff_scoring = align(
        "AAAA", "CCCC", match_award=-1, indel_penalty=1, sub_penalty=5
    )

    assert aseq1_default == "AAAA" and aseq2_default == "CCCC"
    assert score_default == 4

    assert aseq1_diff_scoring == "AAAA----" and aseq2_diff_scoring == "----CCCC"
    assert score_diff_scoring == 8


@baseline
@with_import(alignment_file)
def test_medium_dna_alignment(align):
    seq1 = "ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatctctttataaacggcacttcc"
    seq2 = "ataagagtgattggcgtccgtacgtaccctttctactctcaaactcttgttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat"

    score, aseq1, aseq2 = align(seq1, seq2)

    expected_align1 = "ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatct---ctttataaacggca----c----t-tcc--"
    expected_align2 = "ataagagtgatt-g-g----c-g-tccgtacgtaccctttctactctcaaactctt----gttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat"

    assert score == -116
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@baseline
@with_import(alignment_file)
def test_text_alignment_minor_differences(align):
    # Isaiah 48:5 KJV
    seq1 = ("I have even from the beginning declared it to thee; before it came to pass I shewed it thee: lest thou "
            "shouldest say, Mine idol hath done them, and my graven image, and my molten image, hath commanded them.")
    # 1 Nephi 20:5
    seq2 = ("And I have even from the beginning declared to thee; before it came to pass I showed them thee; and I "
            "showed them for fear lest thou shouldst say—Mine idol hath done them, and my graven image, and my molten "
            "image hath commanded them.")

    score, aseq1, aseq2 = align(seq1, seq2)

    print()
    print(aseq1)
    print(aseq2)

    expected_align1 = ("----I have even from the beginning declared it to thee; before it came to pass I shewed "
                       "----it----------------- the-------e-: lest thou shouldest say, Mine idol hath done them, "
                       "and my graven image, and my molten image, hath commanded them.")
    expected_align2 = ("And I have even from the beginning declared--- to thee; before it came to pass I showed them "
                       "thee; and I showed them for fear lest thou should-st say-—Mine idol hath done them, "
                       "and my graven image, and my molten image- hath commanded them.")

    assert score == -389
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@baseline

def test_large_dna_alignment():
    run_with_timeout(240, _test_large_dna_alignment)

@with_import(alignment_file)
def _test_large_dna_alignment(align):
    timer = Timer()
    times = [10, 10, 20, 40, 80, 120]
    Ns = [10, 100, 1000, 1500, 2000, 3000]
    for max_time_allowed, N in zip(times, Ns):

        seq1 = read_sequence(test_files / "bovine_coronavirus.txt")[:N]
        seq2 = read_sequence(test_files / "murine_hepatitus.txt")[:N]

        timer.start_lap()
        score, aseq1, aseq2 = align(seq1, seq2)

        with open(test_files / f"large_bovine_murine_align_{N}.txt") as file:
            expected_score, expected_align1, expected_align2 = file.read().splitlines()

        assert score == int(expected_score)
        assert aseq1 == expected_align1
        assert aseq2 == expected_align2

        if timer.lap_time() > max_time_allowed:
            pytest.fail(f"The alignment of size {N} took longer than {max_time_allowed} seconds")


# -------------------------------- Core tests -------------------------------- #
@core
@with_import(alignment_file)
def test_small_dna_alignment_banded(align):
    score, aseq1, aseq2 = align(
        "GGGGTTTTAAAACCCCTTTT", "TTTTAAAACCCCTTTTGGGG", banded_width=2
    )
    assert score == 6
    assert aseq1 == "GGGGTTTTAAAACCCCTT--TT"
    assert aseq2 == "--TTTTAAAACCCCTTTTGGGG"


@core
@with_import(alignment_file)
def test_length_discrepancy_banded(align):
    score, aseq1, aseq2 = align("AAAA", "AAAHHHAHHHHHHHHHHHHHHHHHH", banded_width=2)
    assert score == math.inf
    assert aseq1 == None
    assert aseq2 == None


@core
@with_import(alignment_file)
def test_alignment_changes_with_banded_width(align):
    # banded width 1
    score_narrow, a1_narrow, a2_narrow = align(
        "tcgctcatatatccc",
        "atataccctggggtg",
        banded_width=1,
        match_award=-1,
        sub_penalty=1,
        indel_penalty=1,
    )
    assert score_narrow == 10
    assert a1_narrow == "-tcgctcatatatccc"
    assert a2_narrow == "atataccct-ggggtg"

    # banded width 2
    score_mid, a1_mid, a2_mid = align(
        "tcgctcatatatccc",
        "atataccctggggtg",
        banded_width=2,
        match_award=-1,
        sub_penalty=1,
        indel_penalty=1,
    )
    assert score_mid == 8
    assert a1_mid == "-t-cgctcat-atatccc"
    assert a2_mid == "atatac-cctggggt--g"

    # banded width 7
    score_wide, a1_wide, a2_wide = align(
        "tcgctcatatatccc",
        "atataccctggggtg",
        banded_width=7,
        match_award=-1,
        sub_penalty=1,
        indel_penalty=1,
    )
    assert score_wide == 6
    assert a1_wide == "tcgctcatatatccc-------"
    assert a2_wide == "------atata-ccctggggtg"


@core
@with_import(alignment_file)
def test_medium_dna_alignment_banded(align):
    seq1 = "ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatctctttataaacggcacttcc"
    seq2 = "ataagagtgattggcgtccgtacgtaccctttctactctcaaactcttgttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat"

    score, aseq1, aseq2 = align(seq1, seq2, banded_width=2)

    expected_align1 = "ataagagtgattggcg-atatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatctctttataaacggcacttcc--"
    expected_align2 = "ataagagtgattggcgtccgtacgtaccctttctactc-tcaaactcttgttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat"

    assert score == -79
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@core
def test_massive_dna_alignment_banded():
    run_with_timeout(60, _test_massive_dna_alignment_banded)

@with_import(alignment_file)
def _test_massive_dna_alignment_banded(align):
    timer = Timer()
    for N in [10, 100, 1000, 10000, 20000, 25000, 31000]:
        seq1 = read_sequence(test_files / "bovine_coronavirus.txt")[:N]
        seq2 = read_sequence(test_files / "murine_hepatitus.txt")[:N]

        timer.start_lap()

        score, aseq1, aseq2 = align(seq1, seq2, banded_width=3)

        with open(test_files / f"massive_bovine_murine_align_{N}.txt") as file:
            expected_score, expected_align1, expected_align2 = file.read().splitlines()

        assert score == int(expected_score)
        assert aseq1 == expected_align1
        assert aseq2 == expected_align2

        if timer.lap_time() > 10:
            pytest.fail(f"The unrestricted alignment of size {N} took too long")


# ------------------------------ Stretch 2 tests ----------------------------- #
@stretch2
@with_import(alignment_file)
def test_small_dna_alignment_end_match(local_align):
    score, aseq1, aseq2 = local_align("GGGGTTTTAAAACCCCTTTT", "TTTTAAAACCCCTTTTGGGG")
    assert score == -48
    assert aseq1 == "TTTTAAAACCCCTTTT"
    assert aseq2 == "TTTTAAAACCCCTTTT"


@stretch2
@with_import(alignment_file)
def test_small_dna_alignment_middle_substitution(local_align):
    score, seq1, seq2 = local_align("tcgctcatatatccc", "taactcgtatatgaaca")
    assert score == -21
    assert seq1 == "ctcatatat"
    assert seq2 == "ctcgtatat"


@stretch2
@with_import(alignment_file)
def test_text_alignment_common_phrase(local_align):
    # John 8:12
    seq1 = ("Then spake Jesus again unto them, saying, I am the light of the world: he that followeth me shall not "
            "walk in darkness, but shall have the light of life.")

    # John 9:4-5
    seq2 = ("I must work the works of him that sent me, while it is day: the night cometh, when no man can work. As "
            "long as I am in the world, I am the light of the world.")

    # 3 Nephi 9:18
    seq3 = "I am the light and the life of the world. I am Alpha and Omega, the beginning and the end."

    score_a, seq1_a, seq2_a = local_align(seq1, seq2)
    print()
    print(seq1_a)
    print(seq2_a)

    expected_align1 = ", I am the light of the world"
    expected_align2 = ", I am the light of the world"

    assert score_a == -87
    assert seq1_a == expected_align1
    assert seq2_a == expected_align2

    score_b, seq1_b, seq3_b = local_align(seq1, seq3, indel_penalty=2)
    print()
    print(seq1_b)
    print(seq3_b)

    assert score_b == -55
    assert seq1_b == 'I am the ligh------t------- of the world'
    assert seq3_b == 'I am the light and the life of the world'


@stretch2
@with_import(alignment_file,"local_align")
@with_import(alignment_file,"align")
def test_text_alignment_local_v_global(align,local_align):
    # Green (2015) translation of the Iliad
    seq1 = ("Wrath, goddess, sing of Achilles Peleus’s son’s calamitous wrath, which hit the Achaians with countless "
            "ills— many the valiant souls it saw off down to Hades, souls of heroes, their selves left as carrion for "
            "dogs and all birds of prey, and the plan of Zeus was fulfilled— from the first moment those two men "
            "parted in fury, Atreus’s son, king of men, and the godlike Achilles.")

    # Verity (2010) translation of the Iliad
    seq2 = ("Sing, goddess, the anger of Achilles, Peleus’ son, the accursed anger which brought the Achaeans "
            "countless agonies and hurled many mighty shades of heroes into Hades, causing them to become the prey of "
            "dogs and all kinds of birds; and the plan of Zeus was fulfilled. Sing from the time the two men were "
            "first divided in strife— Atreus’ son, lord of men, and glorious Achilles.")

    score, aseq1, aseq2 = local_align(seq1, seq2)
    print()
    print(aseq1)
    print(aseq2)

    assert score == -150
    assert (
            aseq1
            == " dogs and all birds of -prey, and the plan of Zeus was fulfilled-----— from the "
    )
    assert (
            aseq2
            == " dogs and all kinds of birds; and the plan of Zeus was fulfilled. Sing from the "
    )

    score, aseq1, aseq2 = align(seq1, seq2)

    print()
    print(aseq1)
    print(aseq2)

    assert score == -278
    assert (
            aseq1
            == "Wrath, goddess, ---sing-- of Achilles- Peleus’s son’s calamitous wrath, which ----hit the Achaians with countless -ills— many the valiant -souls it saw of-f down --to Hades, souls of heroes, their selves left as carrion for dogs and all birds of -prey, and the plan of Zeus was fulfilled-----— from the fi-rst moment those two men -parted in fur--y, Atreus’s son, king of men, and the godlike Achilles."
    )
    assert (
            aseq2
            == "-Sing, goddess, the anger of Achilles, Peleus’- son, the accursed anger which brought the Achaeans----- countless agonies and hurled many mighty shades of heroes into Hades, cau-s--------ing the-m to become t-he --pr-ey -of dogs and all kinds of birds; and the plan of Zeus was fulfilled. Sing from the time the two men were first divided in strife— Atreus’- son, lord of men, and ---glorious Achilles."
    )
