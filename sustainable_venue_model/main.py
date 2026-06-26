import csv
import math
import itertools
import os
from pathlib import Path

import matplotlib.pyplot as plt


def read_venues(csv_path):
    """
    Read venue data from a CSV file.
    """
    venues = []

    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            venue = {
                "venue": row["venue"],
                "visitor_flow": int(row["visitor_flow"]),
                "food_supply_kg": float(row["food_supply_kg"]),
                "waste_rate": float(row["waste_rate"]),
                "waste_kg": float(row["waste_kg"]),
                "x": float(row["x"]),
                "y": float(row["y"])
            }
            venues.append(venue)

    return venues


def calculate_distance(venue_a, venue_b):
    """
    Calculate the Euclidean distance between two venues.
    """
    dx = venue_a["x"] - venue_b["x"]
    dy = venue_a["y"] - venue_b["y"]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance


def build_distance_matrix(venues):
    """
    Build a distance matrix for all venues.
    """
    distance_matrix = []

    for venue_a in venues:
        row = []
        for venue_b in venues:
            distance = calculate_distance(venue_a, venue_b)
            row.append(distance)
        distance_matrix.append(row)

    return distance_matrix


def calculate_total_waste(venues):
    """
    Calculate the total food waste from all venues except the treatment centre.
    """
    total_waste = 0.0

    for venue in venues:
        if venue["venue"] != "Treatment Centre":
            total_waste += venue["waste_kg"]

    return total_waste


def calculate_route_distance(route, distance_matrix):
    """
    Calculate the total distance of a route.
    """
    total_distance = 0.0

    for i in range(len(route) - 1):
        from_index = route[i]
        to_index = route[i + 1]
        total_distance += distance_matrix[from_index][to_index]

    return total_distance


def calculate_emissions(distance_km, emission_factor):
    """
    Calculate carbon emissions.
    """
    return distance_km * emission_factor


def find_optimal_route(venues, distance_matrix):
    """
    Find the shortest route by testing all possible venue orders.

    Treatment Centre is fixed as the start and end point.
    Index 0 is Treatment Centre.
    Other venues are visited once.
    """
    treatment_centre_index = 0
    venue_indices = list(range(1, len(venues)))

    best_route = None
    best_distance = float("inf")

    for permutation in itertools.permutations(venue_indices):
        route = [treatment_centre_index] + list(permutation) + [treatment_centre_index]
        distance = calculate_route_distance(route, distance_matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


def route_to_text(venues, route):
    """
    Convert route index list into venue name text.
    """
    route_names = []

    for index in route:
        route_names.append(venues[index]["venue"])

    return " -> ".join(route_names)


def print_venues(venues):
    """
    Print venue data in a readable format.
    """
    print("Venue data loaded successfully.")
    print("-" * 80)
    print(f"{'Venue':25s} {'Visitors':>10s} {'Food kg':>10s} {'Waste kg':>10s} {'X':>6s} {'Y':>6s}")
    print("-" * 80)

    for item in venues:
        print(
            f"{item['venue']:25s} "
            f"{item['visitor_flow']:10d} "
            f"{item['food_supply_kg']:10.1f} "
            f"{item['waste_kg']:10.1f} "
            f"{item['x']:6.1f} "
            f"{item['y']:6.1f}"
        )

    print("-" * 80)


def print_route_results(
    title,
    venues,
    route,
    total_distance,
    diesel_emissions,
    ev_emissions
):
    """
    Print route and emission results.
    """
    print(f"\n{title}")
    print("-" * 80)
    print(route_to_text(venues, route))
    print("-" * 80)
    print(f"Total route distance:       {total_distance:.2f} km")
    print(f"Diesel vehicle emissions:   {diesel_emissions:.2f} kg CO2")
    print(f"Electric vehicle emissions: {ev_emissions:.2f} kg CO2")
    print("-" * 80)


def print_comparison(
    baseline_distance,
    optimal_distance,
    baseline_diesel_emissions,
    optimal_diesel_emissions,
    baseline_ev_emissions,
    optimal_ev_emissions
):
    """
    Compare baseline route and optimised route.
    """
    distance_reduction = (baseline_distance - optimal_distance) / baseline_distance * 100
    diesel_emission_reduction = (
        baseline_diesel_emissions - optimal_diesel_emissions
    ) / baseline_diesel_emissions * 100
    ev_emission_reduction = (
        baseline_ev_emissions - optimal_ev_emissions
    ) / baseline_ev_emissions * 100

    print("\nComparison between baseline route and optimised route:")
    print("-" * 80)
    print(f"Baseline distance:          {baseline_distance:.2f} km")
    print(f"Optimised distance:         {optimal_distance:.2f} km")
    print(f"Distance reduction:         {distance_reduction:.2f}%")
    print("-" * 80)
    print(f"Baseline diesel emissions:  {baseline_diesel_emissions:.2f} kg CO2")
    print(f"Optimised diesel emissions: {optimal_diesel_emissions:.2f} kg CO2")
    print(f"Diesel emission reduction:  {diesel_emission_reduction:.2f}%")
    print("-" * 80)
    print(f"Baseline EV emissions:      {baseline_ev_emissions:.2f} kg CO2")
    print(f"Optimised EV emissions:     {optimal_ev_emissions:.2f} kg CO2")
    print(f"EV emission reduction:      {ev_emission_reduction:.2f}%")
    print("-" * 80)


def plot_route(venues, route, title, output_path):
    """
    Plot a route map and save it as an image.
    """
    x_values = []
    y_values = []

    for index in route:
        x_values.append(venues[index]["x"])
        y_values.append(venues[index]["y"])

    plt.figure(figsize=(10, 7))

    plt.plot(x_values, y_values, marker="o", linewidth=2)

    for venue in venues:
        plt.scatter(venue["x"], venue["y"], s=80)
        plt.text(
            venue["x"] + 0.15,
            venue["y"] + 0.15,
            venue["venue"],
            fontsize=9
        )

    for i in range(len(route) - 1):
        from_index = route[i]
        to_index = route[i + 1]

        x_mid = (venues[from_index]["x"] + venues[to_index]["x"]) / 2
        y_mid = (venues[from_index]["y"] + venues[to_index]["y"]) / 2

        plt.text(
            x_mid,
            y_mid,
            str(i + 1),
            fontsize=9
        )

    plt.title(title)
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_emissions_comparison(
    baseline_diesel_emissions,
    optimal_diesel_emissions,
    baseline_ev_emissions,
    optimal_ev_emissions,
    output_path
):
    """
    Plot carbon emission comparison and save it as an image.
    """
    labels = [
        "Baseline Diesel",
        "Optimised Diesel",
        "Baseline EV",
        "Optimised EV"
    ]

    values = [
        baseline_diesel_emissions,
        optimal_diesel_emissions,
        baseline_ev_emissions,
        optimal_ev_emissions
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)

    plt.title("Carbon Emissions Comparison")
    plt.xlabel("Scenario")
    plt.ylabel("Carbon emissions, kg CO2")

    for i, value in enumerate(values):
        plt.text(
            i,
            value,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def set_current_directory_permissions(project_root):
    """
    Set files in the current project directory to 755 permissions.

    On Windows, this may have limited effect, but the function is kept safe.
    """
    try:
        for item in project_root.iterdir():
            os.chmod(item, 0o755)
    except Exception as error:
        print(f"Permission update skipped: {error}")


def main():
    project_root = Path(__file__).parent
    csv_path = project_root / "data" / "venues.csv"
    output_dir = project_root / "outputs"

    output_dir.mkdir(exist_ok=True)

    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return

    venues = read_venues(csv_path)
    distance_matrix = build_distance_matrix(venues)

    total_waste = calculate_total_waste(venues)

    diesel_emission_factor = 0.25
    ev_emission_factor = 0.08

    baseline_route = [0, 1, 2, 3, 4, 5, 0]
    baseline_distance = calculate_route_distance(baseline_route, distance_matrix)

    baseline_diesel_emissions = calculate_emissions(
        baseline_distance,
        diesel_emission_factor
    )

    baseline_ev_emissions = calculate_emissions(
        baseline_distance,
        ev_emission_factor
    )

    optimal_route, optimal_distance = find_optimal_route(venues, distance_matrix)

    optimal_diesel_emissions = calculate_emissions(
        optimal_distance,
        diesel_emission_factor
    )

    optimal_ev_emissions = calculate_emissions(
        optimal_distance,
        ev_emission_factor
    )

    baseline_route_image = output_dir / "baseline_route_map.png"
    optimal_route_image = output_dir / "optimised_route_map.png"
    emissions_image = output_dir / "emissions_comparison.png"

    plot_route(
        venues,
        baseline_route,
        "Baseline Food Waste Collection Route",
        baseline_route_image
    )

    plot_route(
        venues,
        optimal_route,
        "Optimised Food Waste Collection Route",
        optimal_route_image
    )

    plot_emissions_comparison(
        baseline_diesel_emissions,
        optimal_diesel_emissions,
        baseline_ev_emissions,
        optimal_ev_emissions,
        emissions_image
    )

    print_venues(venues)

    print(f"\nTotal collected food waste: {total_waste:.2f} kg")

    print_route_results(
        "Baseline route analysis:",
        venues,
        baseline_route,
        baseline_distance,
        baseline_diesel_emissions,
        baseline_ev_emissions
    )

    print_route_results(
        "Optimised route analysis:",
        venues,
        optimal_route,
        optimal_distance,
        optimal_diesel_emissions,
        optimal_ev_emissions
    )

    print_comparison(
        baseline_distance,
        optimal_distance,
        baseline_diesel_emissions,
        optimal_diesel_emissions,
        baseline_ev_emissions,
        optimal_ev_emissions
    )

    print("\nFigures saved successfully:")
    print("-" * 80)
    print(f"Baseline route map:     {baseline_route_image}")
    print(f"Optimised route map:    {optimal_route_image}")
    print(f"Emissions comparison:   {emissions_image}")
    print("-" * 80)

    set_current_directory_permissions(project_root)


if __name__ == "__main__":
    main()