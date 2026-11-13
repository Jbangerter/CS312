
from pathlib import Path
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


if __name__ == "__main__":
    main()
