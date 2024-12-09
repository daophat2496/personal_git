import dlt
import duckdb
from sources import trip_source

def main():
    db = duckdb.connect("trip_duck.duckdb")
    
    p = dlt.pipeline(
        pipeline_name = "Yellow Trip Pipeline"
        , destination = dlt.destinations.duckdb(db)
        , dataset_name = "public"
    )

    info = p.run(trip_source().with_resources("YellowTripResouce"))
    print(f"Pipeline info: \n{info}")

if __name__ == "__main__":
    main()