from datetime import datetime

# Custom
from .dataset import get_model_files, fetch_model

FILE_NAMES = get_model_files()
LOCATIONS = [(float(i.split("_")[0]), float(i.split("_")[1])) for i in FILE_NAMES]

# DON'T CHANGE, START DATE
REFERENCE_DATE = datetime(2024, 8, 1)

"""
Utilities
"""


def find_closest_point(locations, latitude, longitude):
    min_distance = float("inf")
    closest_point = None

    print("lat: ", latitude, "lon: ", longitude, "locations: ", locations)

    for x, y in locations:
        distance = (x - latitude) ** 2 + (y - longitude) ** 2
        if distance < min_distance**2:
            min_distance = distance
            closest_point = (x, y)

    return closest_point


def months_from_august_2024(target_date):
    # Constants for now

    # target_date = datetime.strptime(target_date, "%Y-%m-%d")
    target_date = datetime.strptime(target_date, "%Y-%m-%d")

    year_diff = target_date.year - REFERENCE_DATE.year
    month_diff = target_date.month - REFERENCE_DATE.month

    total_months = year_diff * 12 + month_diff
    return total_months


def predict_SDL(file_name, date):
    month_diff = months_from_august_2024(date)
    loaded_model = fetch_model(file_name)
    SDL = loaded_model.forecast(steps=month_diff)
    return SDL.tolist()


# Main function to be called
def calculate_SDL(latitude, longitude, date):
    file_name = "_".join(
        [str(i) for i in find_closest_point(LOCATIONS, latitude, longitude)]
    )
    SDL = predict_SDL(file_name, date)
    return SDL


"""
Calculates SDL by prediction
"""


def predict_SDL(file_name, date):
    month_diff = months_from_august_2024(date)
    loaded_model = fetch_model(file_name)
    SDL = loaded_model.forecast(steps=month_diff)
    return SDL.tolist()
