from scipy.io import netcdf
import matplotlib.pyplot as plt
import netCDF4

ncfile1 = netCDF4.Dataset('../ShCu_times/sgpshcusummaryC1.c1.20120501.000000.custom.nc','r')
# print(ncfile1.variables)

print(ncfile1['shallowcumulus_event_tests'][:])
print('HI')
print(ncfile1['shallowcumulus_event'][:,:])

plt.imshow(ncfile1['shallowcumulus_event'][:,:])
plt.colorbar()
plt.show()

plt.imshow(ncfile1['shallowcumulus_event_tests'][:,:])
plt.colorbar()
plt.show()

# ncfile2 = netcdf.NetCDFFile('../ShCu_times/sgpshcusummaryC1.c1.20120501.000000.custom.nc','r')
