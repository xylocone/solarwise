import datetime
import math

# Custom modules
from app.utils.dates import date_range, get_month_abbr
from .future import calculate_SDL
from .dataset import NetCDFRetriever, NetCDFExtractor, get_solar_decline

# The solar decline dataset
delta_map = get_solar_decline()


def get_sunlight_hours(lat: float, date: int, month: str) -> float:
    """
    Calculate the number of solar hours for a given latitude on a specified date.

    Parameters:
    - lat (float): The latitude in decimal degrees. Positive values represent the northern hemisphere, while negative values represent the southern hemisphere.
    - date (int): The day of the month (1-31) for which the solar hours are to be calculated.
    - month (str): The month name (e.g., "January", "February", etc.) for the specified date.

    Returns:
    - float: The adjusted solar hours for the given latitude and date. This value represents the solar time in hours based on the solar angle.

    Raises:
    - ValueError: If the date is out of range for the specified month.

    Note:
    - The function relies on external mappings and functions, including `delta_map`, `dms_to_decimal`, and `calculate_omegao`, which must be defined elsewhere in the code.
    """
    phi = lat

    def get_hours(date):
        delta = delta_map[date - 1][month]
        # If the value is none, return none
        if not delta or len(delta) == 0:
            return None

        # Convert the DMS string to decimal degrees
        delta_degrees = dms_to_decimal(*parse_dms(delta))
        # Get the omega (solar angle) for the delta and phi
        omega = calculate_omegao(delta_degrees, phi)
        # Adjust the omega to watch time
        return omega * (24 / math.pi)

    # If a particular date is in question, then return the result
    if date != -1:
        return get_hours(date)

    # Else, return an average answer
    hours = []

    # If the date is provided as -1, then range it from start to end
    for j in range(1, 13):
        for i in range(date_range(j, datetime.datetime.now().year)):
            delta = delta_map[i][month]

            # Skip the iteration of the data point is None
            if not delta or len(delta) == 0:
                continue

            # Convert the DMS string to decimal degrees
            delta_degrees = dms_to_decimal(*parse_dms(delta))
            # Get the omega (solar angle) for the delta and phi
            omega = calculate_omegao(delta_degrees, phi)
            # Adjust the omega to watch time
            hours.append(omega * (24 / math.pi))

    return sum(hours) / len(hours)


def parse_dms(dms_str: str) -> tuple:
    """
    Parse a DMS (Degrees, Minutes, Seconds) string into its components.

    Parameters:
    - dms_str (str): A string representing an angle in DMS format, e.g., "N 30° 15' 20"" or "S 45° 30'".

    Returns:
    - tuple: A tuple containing:
        - degrees (int): The degree component of the angle.
        - minutes (int): The minute component of the angle.
        - seconds (int): The second component of the angle (default is 0 if not provided).
        - direction (str): The direction component (e.g., 'N', 'S', 'E', 'W').

    Raises:
    - ValueError: If the input string does not conform to the expected DMS format.

    Note:
    - The direction should be the first character of the input string.
    """
    # Remove any extra spaces
    dms_str = dms_str.strip()

    # Extract the direction (last character)
    direction = "N"
    if dms_str[0] == "0":
        direction = "N"
    else:
        direction = dms_str[0]
        # Remove the direction from the string
        dms_str = dms_str[1:].strip()

    # Split the string by degree and minute symbols
    if "°" in dms_str:
        degrees, minutes = dms_str.split("°")
        degrees = degrees.encode("ascii", "ignore").decode().strip()
        degrees = int(degrees)

        if "'" in minutes:
            minutes, seconds = minutes.split("'")
            minutes = int(minutes.strip())
            seconds = 0  # Default to 0 if no seconds are provided
        else:
            minutes = int(minutes.strip())
            seconds = 0  # Default to 0 if no seconds are provided
    else:
        raise ValueError("Invalid DMS format")

    return degrees, minutes, seconds, direction


def dms_to_decimal(degrees, minutes=0, seconds=0, direction="N"):
    """
    Convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees.

    Parameters:
    degrees (int): Degrees part of the DMS.
    minutes (int): Minutes part of the DMS.
    seconds (float): Seconds part of the DMS.
    direction (str): Direction (N, S, E, W) to determine the sign of the result.

    Returns:
    float: Decimal degrees.
    """
    # Calculate decimal degrees
    decimal_degrees = abs(degrees) + (minutes / 60) + (seconds / 3600)

    # Adjust sign based on direction
    if direction in ["S", "W"]:
        decimal_degrees = -decimal_degrees

    return decimal_degrees


def calculate_omegao(delta: float, phi: float):
    """
    Calculate omegao using the formula:
    omegao = acos(max(min(-tan(delta * rpd) * tan(phi * rpd), 1.0), -1.0)) * dpr
    omega: is the solar hour angle at either sunrise (when negative value is taken) or sunset (when positive value is taken);

    Parameters:
    phi (float): is the latitude of the observer on the Earth in degrees
    delta (float): is the sun declination in degrees

    Returns:
    float: The value of omegao (the solar hour angle at either sunrise (when negative value is taken) or sunset (when positive value is taken);) in degrees.
    """
    rpd = math.pi / 180  # Radians per degree

    # Calculate omegao
    omegao = math.acos(
        max(min(-math.tan(delta * rpd) * math.tan(phi * rpd), 1.0), -1.0)
    )

    return omegao


def get_estimated_energy(
    lat: float,
    lon: float,
    area: float,
    efficiency: float | None = 0.223,
    month: int | None = None,
    to_year: int | None = None,
) -> float | None:
    """
    Estimate the energy output of a solar panel system for a given location and month.

    Parameters:
    - lat (float): Latitude of the location (in decimal degrees).
    - lon (float): Longitude of the location (in decimal degrees).
    - area (float): Area of the solar panels (in square meters).
    - panel_efficiency (float): Efficiency of the solar panels (between 0 and 1).
      If None, defaults to 0.223 (22.3%).
    - month (int | None): The month for which to estimate energy (1 for January, ..., 12 for December).
      If None, returns the average energy output for the whole year.

    Returns:
    - float | None: Estimated energy output in kWh for the specified month or average yearly output.
      Returns None if data retrieval fails or if files are not found.

    Raises:
    - ValueError: If data for the specified year is not available.

    Note:
    - The function assumes the use of a class `NetCDFRetriever` to retrieve weather data,
      and a class `NetCDFExtractor` to extract solar radiation data.
    - The sunlight hours are adjusted with an empirical factor of 0.6 to account for peak hours.
    """
    current_year = datetime.datetime.now().year
    year = year or current_year + 1

    # Redefine efficiency with a constants
    efficiency = efficiency or 0.223
    # Round the month for inputs
    month = month % 12 if month is not None else None
    SDLR = []

    if year < current_year:
        # Retrieve for the last year
        files = None
        try:
            retriever = NetCDFRetriever()
            files = retriever.retrieve(year)
        except ValueError:
            print("The data is not up-to-date, for year:", year)
            return None

        # If the files aren't found, return None
        if files is None:
            return None

        # Extract the SDLR data
        SDLR = list(
            map(lambda dt: dt["sdlr"], NetCDFExtractor.get_sdlr(files, lat, lon))
        )
    else:
        raise "Cannot fetch for future dates, use prediction"

    total = 0
    # Return the energy for a particular month
    if month is not None:
        # Average sunlight received for the particular month
        hours = get_sunlight_hours(lat, -1, get_month_abbr(month))
        # Adjustment factor for sunlight, accounting for peak hours
        adjustment_factor = 0.6
        hours *= adjustment_factor
        # The SDLR for the particular month
        radiation = SDLR[month - 1]
        # Energy output for the scenario (in kWh) (in a single day)
        energy = (radiation * area * hours) / 1000
        # Account for the efficiency of the panel
        energy *= efficiency
        total = energy
        return {"order": 0, "month": get_month_abbr(month), "energy": energy}, total

    # Else, return an average energy for the whole year
    month_energies = []

    for i in range(1, 13):  # Corrected to loop through all months (1 to 12)
        # Average sunlight received for the particular month
        hours = get_sunlight_hours(lat, -1, get_month_abbr(i))
        # Adjustment factor for sunlight, accounting for peak hours
        adjustment_factor = 0.6
        hours *= adjustment_factor
        # The SDLR radiation for this month
        radiation = SDLR[i]
        energy = (radiation * area * hours) / 1000
        energy *= efficiency * date_range(i + 1, year)
        month_energies.append(energy)

    # Return an average, adjusted for efficiency
    for i, energy in enumerate(month_energies):
        month_energies[i] = {"order": i, "month": get_month_abbr(i), "energy": energy}
        total += energy

    return month_energies, total


def get_estimated_energy_by_year(
    lat: float,
    lon: float,
    area: float,
    to_year: int,
    efficiency: float | None = 0.223,
) -> float | None:
    """
    Estimate the energy output of a solar panel system for a given location and month.

    Parameters:
    - lat (float): Latitude of the location (in decimal degrees).
    - lon (float): Longitude of the location (in decimal degrees).
    - area (float): Area of the solar panels (in square meters).
    - to_year (int | None): The year up until which the prediction is needed
    - panel_efficiency (float): Efficiency of the solar panels (between 0 and 1).
      If None, defaults to 0.223 (22.3%).

    Returns:
    - float | None: Estimated energy output in kWh for the specified month or average yearly output.
      Returns None if data retrieval fails or if files are not found.

    Raises:
    - ValueError: If data for the specified year is not available.

    Note:
    - The function assumes the use of a class `NetCDFRetriever` to retrieve weather data,
      and a class `NetCDFExtractor` to extract solar radiation data.
    - The sunlight hours are adjusted with an empirical factor of 0.6 to account for peak hours.
    """
    current_year = datetime.datetime.now().year
    to_year = to_year or current_year + 1

    # Redefine efficiency with a constants
    efficiency = efficiency or 0.223
    SDLR = []

    # Retrieve for the all year
    date = datetime.datetime(to_year, 12, 31).strftime("%Y-%m-%d")
    # Get the prediction for the SDLR
    SDLR.extend(calculate_SDL(lat, lon, date))

    # Else, return an average energy for the whole year
    yearly_energies = []

    # The starting date for the prediction
    date = datetime.datetime(2024, 9, 1)  # Start month + 1

    total = 0
    for i, radiation in enumerate(SDLR):
        # Average sunlight received for the particular month
        hours = get_sunlight_hours(lat, -1, get_month_abbr(date.month - 1))
        # Adjustment factor for sunlight, accounting for peak hours
        adjustment_factor = 0.6
        hours *= adjustment_factor
        # The SDLR radiation for this month
        energy = (radiation * area * hours) / 1000
        energy *= efficiency * date_range(date.month, date.year)
        yearly_energies.append(
            {
                "radiation": radiation,
                "order": i,
                "year": date.year,
                "month": get_month_abbr(date.month - 1),
                "energy": energy,
                "peak-sunlight-hours": hours * 0.6,
            }
        )
        # Increment the date
        date += datetime.timedelta(days=date_range(date.month, date.year))

    # Return an average, adjusted for efficiency
    for i, object in enumerate(yearly_energies):
        total += object["energy"]

    return yearly_energies, total


if __name__ == "__main__":

    """
    omega: is the solar hour angle at either sunrise (when negative value is taken) or sunset (when positive value is taken);
    phi: is the latitude of the observer on the Earth;
    delta: is the sun declination.
    """
    # lat, lon = 59.878600, 8.602518 # Oslo, Norway
    # lat, lon = 65.103108, -18.533889 # For Iceland
    lat, lon = 32.270349, 75.653447  # For Pathankot, Punjab
    # lat, lon = 28.670076, 77.203393 # Delhi, India
    # lat, lon = 8.617664, 77.121907 # Southern Kerala
    # lat, lon = 26.125889, 91.700524  # Guwahati, Assam

    print("hours: ", get_sunlight_hours(lat, 29, "OCT"))

    # Convert the W/m^ to kWh based on the hours from sunlight
    radiation = 364.5896911621094  # in W/m^2

    area = 10  # in square metres, rough estimate
    # Getting the hours estimation, and we'll use the peak hours
    hours = get_sunlight_hours(lat, 29, "OCT")

    # Let the adjustment factor be 0.5 because only half of the time is peak hours
    adjustment_factor = 0.6
    hours *= adjustment_factor

    # Get the energy output in Wh
    energy = radiation * area * hours

    # Adjustment for the efficieny of grid and system
    efficiency = 0.223
    energy *= efficiency

    print("energy in Wh: ", energy)
    print("energy in kWh: ", energy / 1000)

    # Goal to check: 2,850 kWh of energy in a year
    print("In a year: ", (energy / 1000) * 30.5)
