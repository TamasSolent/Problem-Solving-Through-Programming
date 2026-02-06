"""
Data processing functions for the Disneyland reviews dataset.

This module is responsible for reading and processing the data.  It exposes
functions that other parts of the program (e.g. `main` and `tui`) can use to
obtain useful information in a convenient format.

The dataset in `data/disneyland_reviews.csv` has the following columns:

    Review_ID, Rating, Year_Month, Reviewer_Location, Branch

Where:

- `Review_ID` is a unique integer identifier for the review.
- `Rating` is an integer rating (typically from 1–5).
- `Year_Month` is a string like ``"2019-04"`` representing the review date.
- `Reviewer_Location` is a country/region name.
- `Branch` identifies the Disneyland branch (e.g. ``"Disneyland_HongKong"``).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import csv


@dataclass(frozen=True)
class Review:
    """Simple representation of a single review row."""

    review_id: int
    rating: int
    year: int
    month: int
    reviewer_location: str
    branch: str


def _parse_year_month(year_month: str) -> Tuple[int, int]:
    """Parse a ``YYYY-M`` or ``YYYY-MM`` string into ``(year, month)``.

    Any parsing errors are raised as :class:`ValueError`.
    """

    year_str, month_str = year_month.split("-", maxsplit=1)
    return int(year_str), int(month_str)


def load_reviews(path: Path | str) -> List[Review]:
    """Load all reviews from the CSV file.

    Parameters
    ----------
    path:
        Path to the ``disneyland_reviews.csv`` file.

    Returns
    -------
    list[Review]
        A list of :class:`Review` objects, one for each row in the file.
    """

    csv_path = Path(path)
    reviews: List[Review] = []

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                year, month = _parse_year_month(row["Year_Month"])
                review = Review(
                    review_id=int(row["Review_ID"]),
                    rating=int(row["Rating"]),
                    year=year,
                    month=month,
                    reviewer_location=row["Reviewer_Location"].strip() or "Unknown",
                    branch=row["Branch"].strip(),
                )
            except (KeyError, ValueError):
                # If a row is malformed we simply skip it.
                continue

            reviews.append(review)

    return reviews


def summarise_reviews(reviews: Sequence[Review]) -> Dict[str, object]:
    """Return a high-level summary of the dataset.

    The summary dictionary contains simple values that can easily be displayed
    in the TUI, such as total number of reviews, rating range, number of
    branches, and the overall time span.
    """

    if not reviews:
        return {
            "total_reviews": 0,
            "branches": [],
            "min_rating": None,
            "max_rating": None,
            "years": [],
        }

    total_reviews = len(reviews)
    branches = sorted({r.branch for r in reviews})
    ratings = [r.rating for r in reviews]
    years = sorted({r.year for r in reviews})

    return {
        "total_reviews": total_reviews,
        "branches": branches,
        "min_rating": min(ratings),
        "max_rating": max(ratings),
        "years": years,
    }


def _group_ratings_by_key(
    reviews: Iterable[Review],
    key_func,
) -> Dict[object, float]:
    """Helper to compute average rating grouped by an arbitrary key."""

    totals: Dict[object, int] = defaultdict(int)
    counts: Dict[object, int] = defaultdict(int)

    for review in reviews:
        key = key_func(review)
        totals[key] += review.rating
        counts[key] += 1

    averages: Dict[object, float] = {}
    for key, total in totals.items():
        count = counts[key]
        averages[key] = round(total / count, 2) if count else 0.0

    return averages


def average_rating_by_branch(reviews: Sequence[Review]) -> Dict[str, float]:
    """Return the average rating for each branch."""

    return _group_ratings_by_key(reviews, key_func=lambda r: r.branch)


def average_rating_by_month(
    reviews: Sequence[Review],
    branch: Optional[str] = None,
) -> Dict[Tuple[int, int], float]:
    """Return average rating grouped by ``(year, month)``.

    If *branch* is provided, only reviews for that branch are considered.
    """

    filtered: Iterable[Review]
    if branch is not None:
        filtered = (r for r in reviews if r.branch == branch)
    else:
        filtered = reviews

    return _group_ratings_by_key(filtered, key_func=lambda r: (r.year, r.month))


def top_locations_for_branch(
    reviews: Sequence[Review],
    branch: str,
    limit: int = 10,
) -> List[Tuple[str, int]]:
    """Return the most common reviewer locations for a given branch.

    Parameters
    ----------
    reviews:
        All reviews loaded from the dataset.
    branch:
        The Disneyland branch to filter by.
    limit:
        Maximum number of locations to return.
    """

    locations = [r.reviewer_location for r in reviews if r.branch == branch]
    counter = Counter(locations)
    return counter.most_common(limit)


def review_counts_by_park_and_location(
    reviews: Sequence[Review],
) -> Dict[str, Dict[str, int]]:
    """Count number of reviews for each (park, reviewer location) pair.

    Returns a nested dictionary of the form:

        {branch: {location: count, ...}, ...}

    which is easy for the TUI to display.
    """

    counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))  # type: ignore[assignment]

    for review in reviews:
        counts[review.branch][review.reviewer_location] += 1

    # Convert inner defaultdicts to plain dicts for a cleaner API.
    return {branch: dict(loc_counts) for branch, loc_counts in counts.items()}


def average_score_per_year_by_park(
    reviews: Sequence[Review],
) -> Dict[str, Dict[int, float]]:
    """Compute average rating for each park per year.

    Returns a nested dictionary of the form:

        {branch: {year: average_rating, ...}, ...}
    """

    # key: (branch, year) -> (total_rating, count)
    totals: Dict[Tuple[str, int], int] = defaultdict(int)
    counts: Dict[Tuple[str, int], int] = defaultdict(int)

    for review in reviews:
        key = (review.branch, review.year)
        totals[key] += review.rating
        counts[key] += 1

    result: Dict[str, Dict[int, float]] = defaultdict(dict)  # type: ignore[assignment]
    for (branch, year), total in totals.items():
        count = counts[(branch, year)]
        avg = round(total / count, 2) if count else 0.0
        result[branch][year] = avg

    return dict(result)


def average_rating_by_location_for_branch(
    reviews: Sequence[Review],
    branch: str,
) -> Dict[str, float]:
    """Average rating for each reviewer location for a given park/branch."""

    totals: Dict[str, int] = defaultdict(int)
    counts: Dict[str, int] = defaultdict(int)

    for review in reviews:
        if review.branch != branch:
            continue
        loc = review.reviewer_location
        totals[loc] += review.rating
        counts[loc] += 1

    averages: Dict[str, float] = {}
    for loc, total in totals.items():
        count = counts[loc]
        if count:
            averages[loc] = round(total / count, 2)

    return averages


def average_rating_by_calendar_month_for_branch(
    reviews: Sequence[Review],
    branch: str,
) -> Dict[int, float]:
    """Average rating per calendar month (1–12) for a given park, years merged.

    For example, May 2018 and May 2019 are both treated as \"May\".
    """

    totals: Dict[int, int] = defaultdict(int)
    counts: Dict[int, int] = defaultdict(int)

    for review in reviews:
        if review.branch != branch:
            continue
        month = review.month
        totals[month] += review.rating
        counts[month] += 1

    averages: Dict[int, float] = {}
    for month in range(1, 13):
        if counts[month]:
            averages[month] = round(totals[month] / counts[month], 2)

    return averages


def average_score_per_park_by_reviewer_location(
    reviews: Sequence[Review],
) -> Dict[str, Dict[str, float]]:
    """Average score per park by reviewer location.

    Returns a nested dictionary of the form:

        {branch: {location: average_rating, ...}, ...}
    """

    totals: Dict[Tuple[str, str], int] = defaultdict(int)
    counts: Dict[Tuple[str, str], int] = defaultdict(int)

    for review in reviews:
        key = (review.branch, review.reviewer_location)
        totals[key] += review.rating
        counts[key] += 1

    result: Dict[str, Dict[str, float]] = defaultdict(dict)  # type: ignore[assignment]
    for (branch, location), total in totals.items():
        count = counts[(branch, location)]
        avg = round(total / count, 2) if count else 0.0
        result[branch][location] = avg

    return dict(result)


__all__ = [
    "Review",
    "load_reviews",
    "summarise_reviews",
    "average_rating_by_branch",
    "average_rating_by_month",
    "top_locations_for_branch",
    "review_counts_by_park_and_location",
    "average_score_per_year_by_park",
    "average_rating_by_location_for_branch",
    "average_rating_by_calendar_month_for_branch",
    "average_score_per_park_by_reviewer_location",
]