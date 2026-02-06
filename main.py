"""
Main application entry point.

This module is responsible for the overall program flow. It controls how the
user interacts with the program and how the program behaves.  It relies on
other modules to perform specific responsibilities:

- any user input/output should be done in the module `tui`
- any processing should be done in the module `process`
- any visualisation should be done in the module `visual`
"""

from pathlib import Path

from process import (
    load_reviews,
    summarise_reviews,
    average_rating_by_branch,
    average_rating_by_month,
    top_locations_for_branch,
    review_counts_by_park_and_location,
    average_score_per_year_by_park,
    average_rating_by_location_for_branch,
    average_rating_by_calendar_month_for_branch,
    average_score_per_park_by_reviewer_location,
)
from tui import (
    print_welcome,
    print_goodbye,
    get_main_menu_choice,
    get_view_data_menu_choice,
    get_visualise_data_menu_choice,
    show_summary,
    choose_branch,
    choose_top_n,
    show_average_ratings_by_branch,
    show_average_ratings_by_month,
    show_top_locations,
    show_review_counts_by_park_and_location,
    show_average_score_per_year_by_park,
    show_average_score_per_park_by_reviewer_location,
    show_error,
)
from visual import (
    plot_average_rating_by_branch,
    plot_average_rating_by_month,
    plot_top_locations_for_branch,
    plot_top_locations_avg_rating,
    plot_avg_rating_by_calendar_month,
)


DATA_PATH = Path("data") / "disneyland_reviews.csv"


def run() -> None:
    """Run the main program loop."""
    if not DATA_PATH.exists():
        # Respect the responsibility rules: report the problem via TUI.
        show_error(f"Could not find data file at {DATA_PATH!s}")
        return

    # Load and cache the dataset once at program start.
    reviews = load_reviews(DATA_PATH)

    if not reviews:
        show_error("No reviews were loaded from the data file.")
        return

    branches = sorted({review.branch for review in reviews})

    print_welcome()

    while True:
        main_choice = get_main_menu_choice()

        if main_choice == "A":
            # View Data sub-menu
            view_choice = get_view_data_menu_choice()

            if view_choice == "A":
                # [A] View Reviews by Park – here we show average ratings by branch.
                avg_by_branch = average_rating_by_branch(reviews)
                show_average_ratings_by_branch(avg_by_branch)

            elif view_choice == "B":
                # [B] Number of Reviews by Park and Reviewer Location
                counts = review_counts_by_park_and_location(reviews)
                show_review_counts_by_park_and_location(counts)

            elif view_choice == "C":
                # [C] Average Score per year by Park
                averages = average_score_per_year_by_park(reviews)
                show_average_score_per_year_by_park(averages)

            elif view_choice == "D":
                # [D] Average Score per Park by Reviewer Location
                averages = average_score_per_park_by_reviewer_location(reviews)
                show_average_score_per_park_by_reviewer_location(averages)

            else:
                show_error("Unknown View Data menu option.")

        elif main_choice == "B":
            # Visualise Data sub-menu
            vis_choice = get_visualise_data_menu_choice()

            if vis_choice == "A":
                # [A] Most reviewed Parks – visualise ratings by branch.
                avg_by_branch = average_rating_by_branch(reviews)
                plot_average_rating_by_branch(avg_by_branch)

            elif vis_choice == "B":
                # [B] Park Ranking by Nationality – choose a park and
                # show top 10 locations by average rating.
                branch = choose_branch(branches)
                if branch is not None:
                    avg_by_location = average_rating_by_location_for_branch(
                        reviews, branch
                    )
                    if avg_by_location:
                        plot_top_locations_avg_rating(branch, avg_by_location, limit=10)
                    else:
                        show_error("No data available for that park.")

            elif vis_choice == "C":
                # [C] Most Popular Month by Park – choose a park and
                # show average rating per calendar month (years combined).
                branch = choose_branch(branches)
                if branch is not None:
                    avg_by_month = average_rating_by_calendar_month_for_branch(
                        reviews, branch
                    )
                    if avg_by_month:
                        plot_avg_rating_by_calendar_month(branch, avg_by_month)
                    else:
                        show_error("No data available for that branch.")

            else:
                show_error("Unknown Visualise Data menu option.")

        elif main_choice == "X":
            print_goodbye()
            break

        else:
            # user typed something other than A, B or X
            show_error("Unknown menu option selected.")


if __name__ == "__main__":
    run()