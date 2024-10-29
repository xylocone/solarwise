from datetime import datetime


# DO NOT CHANGE THIS
__from = 1979
# This can change to the current year by the operator
__to = 2024

__valid_year_range = range(__from, __to + 1)


def get_month_abbr(month: int) -> str:
    """
    Returns the 3 character code for a month given it's number
    """
    try:
        return [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ][month]
    except IndexError:
        return "JAN"


def get_valid_year_range():
    return __valid_year_range


def is_valid_date(date_string):
    """
    checks if a given date is valid in YYYY-MM-DD format
    """
    try:
        # Attempt to create a datetime object with the given string
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        # If it raises a ValueError, the date is not valid
        return False


def is_valid_year(year: int):
    """
    checks if the given year is within the valid range
    """
    return year in __valid_year_range


def get_month(month_number: int):
    """
    Converts the month number to the month name
    """
    date = datetime(1900, month_number, 1)
    return date.strftime("%B")


def date_range(month_number: int, year: int) -> int:
    """
    Returns the number of days in the specified month of a given year.

    Parameters:
    - month_number (int): The month number (1 for January, 2 for February, ..., 12 for December).
    - year (int): The year to check for leap years (e.g., 2024).

    Returns:
    - int: The number of days in the specified month.

    Raises:
    - ValueError: If the month_number is not between 1 and 12 (inclusive).

    Note:
    - This function correctly accounts for leap years.
    """
    if month_number < 1 or month_number > 12:
        raise ValueError("Month number must be between 1 and 12.")

    # Create a date for the first day of the next month
    if month_number == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month_number + 1, 1)

    # Create a date for the first day of the current month
    current_month = datetime(year, month_number, 1)

    # Calculate the difference in days
    days_in_month = (next_month - current_month).days

    return days_in_month


def get_current_year():
    date = datetime.now()
    return date.strftime("%Y")


"""
Tests
"""
if __name__ == "__main__":

    # The current year test
    print("year: ", get_current_year())
