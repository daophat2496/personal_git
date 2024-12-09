import dlt 
import requests 
import json

@dlt.resource(name = "YellowTripResouce")
def yellow_trip_resource(endpoint):
    response = requests.get(endpoint, stream = True)
    for line in response.iter_lines():
        if line:
            yield json.loads(line)