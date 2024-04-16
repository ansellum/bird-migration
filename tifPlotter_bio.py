import os
import rasterio
import matplotlib.pyplot as plt

# Define the file path to the TIFF file
tiff_file = 'extracted_tif_files/wc2.1_10m_bioc_ACCESS-CM2_ssp126_2021-2040.tif'  # Update with your path

# Extract the time period from the file name
time_period = tiff_file.split('_')[-1].replace('.tif', '')

# Open the TIFF file
with rasterio.open(tiff_file) as src:
    # Read the data
    data = src.read(1)
    
    # Flatten the array and filter out invalid values
    valid_data = data[data < 1e30]  # Assuming 1e30 is used for nodata values

    # Calculate the mean value
    mean_value = valid_data.mean() if valid_data.size > 0 else float('nan')

# For a single file, the time series is just one point, but we prepare the data as if more will be added
time_series_data = {
    'Time Period': [time_period],
    'Mean Value': [mean_value]
}

# Plotting the time series data
plt.figure(figsize=(10, 5))
plt.plot(time_series_data['Time Period'], time_series_data['Mean Value'], marker='o')
plt.title('Projected Bioclimatic Variable for 2021-2040')
plt.xlabel('Time Period')
plt.ylabel('Mean Bioclimatic Value')
plt.grid(True)
plt.show()

