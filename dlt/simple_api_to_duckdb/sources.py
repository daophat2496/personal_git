import dlt
from resources import yellow_trip_resource

@dlt.source(name = "TripSource")
def trip_source():
    # We can group more than one resources into a source
    # Best practice:
    # Return resource with corresponding URL here
    
    url = "https://storage.googleapis.com/dtc_zoomcamp_api/yellow_tripdata_2009-06.jsonl"

    return [
        yellow_trip_resource(url)
    ]