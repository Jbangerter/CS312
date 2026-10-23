

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
import re
import urllib.request
import zipfile

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

try:
    # Keep your algorithm in a separate file named convex_hull.py.
    from convex_hull import compute_hull_other
except ImportError as exc:
    raise SystemExit(
        "Could not import compute_hull_other from convex_hull.py.\n"
        "Save your hull functions in a file named convex_hull.py and add:\n\n"
        "def compute_hull_other(points):\n"
        "    return compute_hull_dvcq(points)\n"
    ) from exc


ZIP_PATH = Path("DixieFire_2021_perimeters.zip")
DATA_DIR = Path("dixie_perimeters")
OUTPUT_DIR = Path("fire_hull_plots")

DATASET_URL = (
    "https://zenodo.org/records/15492982/files/"
    "DixieFire_2021_perimeters.zip?download=1"
)

# Northern California: use a planar coordinate system with meters as units.
PROJECTED_CRS = "EPSG:32610"  # WGS 84 / UTM zone 10N

# Match YYYYMMDD, YYYY-MM-DD, or YYYY_MM_DD in a shapefile filename.
DATE_PATTERN = re.compile(
    r"(?<!\d)(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?!\d)"
)

DATE_FIELDS = (
    "poly_PolygonDateTime",
    "poly_DateCurrent",
    "DateCurrent",
    "Date",
    "datetime",
    "date",
)


def download_dataset_if_needed() -> None:
    """Download the published Dixie Fire perimeter ZIP if not present."""
    if ZIP_PATH.exists():
        return

    print("Downloading the Dixie Fire perimeter dataset (~26 MB)...")
    request = urllib.request.Request(
        DATASET_URL,
        headers={"User-Agent": "ConvexHullCourseProject/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            ZIP_PATH.write_bytes(response.read())
    except Exception as exc:
        if ZIP_PATH.exists():
            ZIP_PATH.unlink()
        raise RuntimeError(
            "Could not download the dataset. Download it manually from "
            "https://zenodo.org/records/15492982 and save the file as "
            f"{ZIP_PATH.name} next to this script. Details: {exc}"
        ) from exc


def extract_dataset_if_needed() -> list[Path]:
    """Extract the ZIP if necessary and return discovered shapefiles."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    shapefiles = list(DATA_DIR.rglob("*.shp"))

    if not shapefiles:
        with zipfile.ZipFile(ZIP_PATH, "r") as archive:
            # Extract the published dataset into a dedicated directory.
            archive.extractall(DATA_DIR)
        shapefiles = list(DATA_DIR.rglob("*.shp"))

    if not shapefiles:
        raise FileNotFoundError(
            f"No .shp files found after extracting {ZIP_PATH.name}. "
            "Check that the ZIP contains the shapefile components."
        )

    return sorted(shapefiles)


def parse_date_value(value) -> date | None:
    """Interpret common string, datetime, or ArcGIS timestamp formats."""
    if value is None or pd.isna(value):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        # ArcGIS timestamps are commonly milliseconds since 1970.
        try:
            timestamp = float(value)
            if abs(timestamp) > 10_000_000_000:
                timestamp /= 1000.0
            return datetime.fromtimestamp(
                timestamp, tz=timezone.utc
            ).date()
        except (ValueError, TypeError, OverflowError, OSError):
            return None

    try:
        parsed = pd.to_datetime(value, errors="coerce", utc=True)
        if pd.isna(parsed):
            return None
        return parsed.date()
    except (ValueError, TypeError, OverflowError):
        return None


def get_perimeter_date(path: Path, frame: gpd.GeoDataFrame) -> date | None:
    """Find a snapshot date first in the filename, then in attributes."""
    match = DATE_PATTERN.search(path.stem)
    if match:
        try:
            return date(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
            )
        except ValueError:
            pass

    columns_lower = {str(column).lower(): column for column in frame.columns}
    fields = [
        columns_lower[field.lower()]
        for field in DATE_FIELDS
        if field.lower() in columns_lower
    ]
    for column in frame.columns:
        name = str(column).lower()
        if ("date" in name or "datetime" in name) and column not in fields:
            fields.append(column)

    for column in fields:
        for value in frame[column].dropna():
            parsed_date = parse_date_value(value)
            if parsed_date is not None:
                return parsed_date

    return None


def load_perimeters(shapefiles: list[Path]):
    """Load dated snapshots, reproject them, and group them by date."""
    perimeters_by_date = defaultdict(list)

    for path in shapefiles:
        try:
            frame = gpd.read_file(path)
        except Exception as exc:
            print(f"Skipping unreadable shapefile {path.name}: {exc}")
            continue

        if frame.empty or frame.geometry.isna().all():
            continue
        if frame.crs is None:
            print(f"Skipping {path.name}: the file has no CRS metadata.")
            continue

        perimeter_date = get_perimeter_date(path, frame)
        if perimeter_date is None:
            print(f"Skipping {path.name}: couldn't identify its date.")
            continue

        frame = frame.to_crs(PROJECTED_CRS)
        perimeters_by_date[perimeter_date].append(frame)

    if len(perimeters_by_date) < 3:
        found = ", ".join(str(d) for d in sorted(perimeters_by_date))
        raise ValueError(
            "Fewer than three distinct perimeter dates were identified. "
            "Check the date patterns in the filenames/attributes. "
            f"Dates identified: {found or 'none'}"
        )

    return perimeters_by_date


def exterior_points(geometry) -> list[tuple[float, float]]:
    """Return exterior vertices from Polygon/MultiPolygon geometries."""
    if geometry is None or geometry.is_empty:
        return []

    if geometry.geom_type == "Polygon":
        # Drop the duplicate closing coordinate in each ring.
        return [
            (float(x), float(y))
            for x, y, *_ in list(geometry.exterior.coords)[:-1]
        ]

    if geometry.geom_type in ("MultiPolygon", "GeometryCollection"):
        points: list[tuple[float, float]] = []
        for part in geometry.geoms:
            points.extend(exterior_points(part))
        return points

    return []


def plot_snapshot(perimeter_date: date, frames: list[gpd.GeoDataFrame]) -> Path:
    """Compute the hull for one date and save its plot."""
    combined = gpd.GeoDataFrame(
        pd.concat(frames, ignore_index=True),
        geometry="geometry",
        crs=frames[0].crs,
    )

    points = sorted({
        point
        for geometry in combined.geometry
        for point in exterior_points(geometry)
    })

    if len(points) < 3:
        raise ValueError(
            f"Only {len(points)} unique perimeter vertices on {perimeter_date}."
        )

    hull = compute_hull_other(points)
    if hull is None or len(hull) < 3:
        raise ValueError(
            f"The algorithm returned an invalid hull on {perimeter_date}. "
            "Check your compute_hull_other implementation."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"dixie_hull_{perimeter_date.isoformat()}.png"

    fig, ax = plt.subplots(figsize=(8, 7))
    combined.boundary.plot(
        ax=ax,
        color="gray",
        linewidth=0.8,
        label="Mapped fire perimeter",
    )
    ax.scatter(
        [point[0] for point in points],
        [point[1] for point in points],
        s=3,
        alpha=0.35,
        label="Input boundary points",
    )

    closed_hull = list(hull)
    if closed_hull[-1] != closed_hull[0]:
        closed_hull.append(closed_hull[0])
    ax.plot(
        [point[0] for point in closed_hull],
        [point[1] for point in closed_hull],
        linewidth=2,
        label=f"Convex hull ({len(hull)} vertices)",
    )

    ax.set_title(f"Dixie Fire Convex Hull — {perimeter_date}")
    ax.set_xlabel("UTM easting (meters)")
    ax.set_ylabel("UTM northing (meters)")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(
        f"{perimeter_date}: {len(points)} input points; "
        f"{len(hull)} hull vertices. Saved: {output_path}"
    )
    return output_path


def main() -> None:
    download_dataset_if_needed()
    shapefiles = extract_dataset_if_needed()
    perimeters_by_date = load_perimeters(shapefiles)
    available_dates = sorted(perimeters_by_date)

    print(f"Found {len(available_dates)} distinct perimeter dates.")
    print("Available dates:", ", ".join(str(d) for d in available_dates))

    # Select early, middle, and late dates from the records that actually exist.
    indices = sorted({0, len(available_dates) // 2, len(available_dates) - 1})
    selected_dates = [available_dates[index] for index in indices]

    print("Selected timepoints:", ", ".join(str(d) for d in selected_dates))

    for perimeter_date in selected_dates:
        plot_snapshot(perimeter_date, perimeters_by_date[perimeter_date])

    print(f"\nDone. Check the {OUTPUT_DIR.resolve()} folder for the plots.")


if __name__ == "__main__":
    main()
