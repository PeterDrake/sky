from netCDF4 import Dataset

data = Dataset("data/sgptsiskycoverC1.b1.20160414.000000.cdf", "w", format="NETCDF4")
print(data.data_model)
