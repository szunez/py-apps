import xarray as xr
import numpy as np
import dask

# Open the dataset with Dask for chunking
url = "https://tds.hycom.org/thredds/dodsC/GLBu0.08/expt_19.1/2012/3hrly"
ds = xr.open_dataset(url, decode_times=False, chunks={'time': 10, 'lat': 100, 'lon': 100, 'depth': 10})

print("Dataset loaded successfully")

# Define coordinates for the start, midpoint, and end
start_coords = (19.0725, 95.2711)
end_coords = (18.716, 95.6017)
midpoint_coords = ((start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2)

# List of coordinates to query
coordinates = [start_coords, midpoint_coords, end_coords]

def get_data_at_coords(coords):
    results = {}
    for lat, lon in coords:
        print(f"Retrieving data for coordinates: ({lat}, {lon})")
        u_data = ds['water_u'].sel(lat=lat, lon=lon, method='nearest').mean(dim='time')
        v_data = ds['water_v'].sel(lat=lat, lon=lon, method='nearest').mean(dim='time')
        
        velocity_magnitude = np.sqrt(u_data**2 + v_data**2)
        average_velocity = velocity_magnitude.mean(dim='depth')
        results[(lat, lon)] = average_velocity.compute().values  # Compute Dask arrays
    return results

# Get data for the specific points
velocity_results = get_data_at_coords(coordinates)

# Print the results
for coords, velocity in velocity_results.items():
    print(f"Average ocean current velocity at coordinates {coords}: {velocity:.2f} m/s")
