from flask import Blueprint, request

# Custom modules
from app.lib.dataset import NetCDFExtractor, NetCDFRetriever
from app.utils.validators import get_or_none
from app.utils.dates import get_current_year

# Custom Responses
from app.utils.responses import APIBaseException, BadRequestException, Success

"""
The APIs for accessing data portal
"""
data_bp = Blueprint("data", __name__)


# The route for data login
@data_bp.route("/sdlr", methods=["POST"])
def get_sdlr():
    """
    Returns the SDLR for the given lat, lon
    """
    json = request.get_json()

    # Get the required values
    year = get_or_none(json, "year", default=get_current_year())
    lat = get_or_none(json, "lat")
    lon = get_or_none(json, "lon")

    # Run through the extractor
    retriever = NetCDFRetriever()

    files = None
    try:
        # get the files, !throws exception
        files = retriever.retrieve(year)
    except Exception as e:
        return BadRequestException(msg=str(e)).response

    # Get the date for the files
    sdlr_data = None
    try:
        sdlr_data = NetCDFExtractor.get_sdlr(files, lat, lon)
    except Exception as e:
        return APIBaseException(
            msg="Internal Server error", code=500, payload={"error": str(e)}
        )

    return Success(
        msg="found SDLR data", payload={"year": year, "sdlr": sdlr_data}
    ).response
