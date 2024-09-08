import netCDF4 as nc
import numpy as np
import os


# Custom modules
from app.utils.dates import is_valid_year, get_month

"""
Constants
"""
DATA_FOLDER = os.path.join("app", "static", "nc")


class NetCDFRetriever:
    """
    NetCDF file reading utility
    """

    def __init__(self, data_folder: str = DATA_FOLDER):
        self.filelist = os.listdir(data_folder)

    def retrieve(self, year: int):
        """
        Retrieves the matching
        """
        if not is_valid_year(year):
            raise ValueError(f"unexpected input for year: '{year}'")

        # Else get the files required for the data handling
        return self.__resolve_files(year)

    def retrieve_all(self, from_: int, to_: int):
        """
        Retrieves all the years from and to
        """
        if not is_valid_year(from_):
            raise ValueError(f"unexpected year input range start for year: '{from_}'")
        if not is_valid_year(to_):
            raise ValueError(f"unexpected year input range end for year: '{to_}'")

        # Retrieve all the filename matches for the range
        return [self.retrieve(year) for year in range(from_, to_ + 1)]

    def __resolve_files(self, year: int):
        """
        Finds all the matching files for the given time period
        """
        files = filter(
            lambda name: name.startswith("SDLmm" + str(year)) and name.endswith(".nc"),
            self.filelist,
        )
        return self.__resolve_filepaths(files)

    def __resolve_filepaths(self, file_names: list[str]):
        return list(
            # Resolve the file path name for better access
            map(lambda file_name: os.path.join(DATA_FOLDER, file_name), file_names)
        )


class NetCDFExtractor:
    """
    Extracts the data from a netcdf file
    specialized for SDLR dataset
    """

    @staticmethod
    def get_sdl(files: list[str], lat: float, lon: float):
        # Check that all the files are NetCDF supported
        try:
            assert all([file.endswith(".nc") for file in files])
        except AssertionError:
            raise ValueError(
                f"Expected NetCDF files ending with .nc got this instead: {files.__str__()}"
            )
        # After the check let's get the data from the files
        sdl_data = []

        for i, file in enumerate(files):
            # Load the NetCDF4 file
            dataset = nc.Dataset(file, "r")

            # Print the dataset information
            # print(dataset)

            # Get the latitude and longitude variables
            latitudes = dataset.variables["lat"][:]
            longitudes = dataset.variables["lon"][:]

            # Find the index of the nearest point to your coordinates
            target_lat = lat
            target_lon = lon

            lat_idx = np.abs(latitudes - target_lat).argmin()
            lon_idx = np.abs(longitudes - target_lon).argmin()

            # Extract the time variable (optional: depending on what you want to analyze)
            time = dataset.variables["time"][:]

            # Extract the radiation data (SID - Surface Incoming Direct Radiation)
            # You might need to adjust the variable name depending on the dataset
            sdl_data.append(
                {
                    "order": i,
                    "month": get_month(i + 1),
                    "sdlr": float(dataset.variables["SDL"][..., lat_idx, lon_idx][0]),
                }
            )

            # Close the dataset
            dataset.close()

        return sdl_data


if __name__ == "__main__":

    year = 2003
    reader = NetCDFRetriever()
    files = reader.retrieve(year)

    # Get the data for the files
    data = NetCDFExtractor.get_sdl(files, 28.676226, 77.202619)

    for d in data:
        print(d)
