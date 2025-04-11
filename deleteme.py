import xarray as xr

url = "https://tds.hycom.org/thredds/dodsC/GLBu0.08/expt_19.1/2012/3hrly"
ds = xr.open_dataset(url, decode_times=False)  # Set decode_times to False

# Print dataset information to check available variables and dimensions
print(ds)
