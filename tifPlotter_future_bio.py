import os
import zipfile
import rasterio
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

# Path to the zip file containing the .tif files
zip_path = 'tif_files/future_bioclimate_dat.zip'

# Directory to extract the .tif files to
extract_to_dir = 'extracted_tif_files'

# Create the directory to extract to if it doesn't exist
Path(extract_to_dir).mkdir(parents=True, exist_ok=True)

# Unzip the file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_dir)

# List all .tif files in the extraction directory
tif_files = sorted([f for f in os.listdir(extract_to_dir) if f.endswith('.tif')])

# Initialize an empty list to hold the data
bio_clim_data_list = []

# Loop over each .tif file
for file_name in tif_files:
    period = file_name.split('_')[3].split('-')[0]  # Extract time period from file name
    
    # Open the .tif file
    with rasterio.open(os.path.join(extract_to_dir, file_name)) as src:
        # Read the data for the entire .tif file
        data = src.read(1)
        
        # Flatten the array and filter out invalid values
        valid_data = data.flatten()
        valid_data = valid_data[valid_data < 1e30]  # Filter out extreme values
        
        mean_value = valid_data.mean() if valid_data.size > 0 else float('nan')
        
        # Append the data to the list
        bio_clim_data_list.append({'Period': period, 'Mean_Value': mean_value})

# Convert the list of dictionaries to a DataFrame
bio_clim_data = pd.DataFrame(bio_clim_data_list)

# Normalize the 'Mean_Value' column
scaler = MinMaxScaler()
bio_clim_data['Normalized_Mean_Value'] = scaler.fit_transform(bio_clim_data[['Mean_Value']])

# Print the resulting DataFrame with normalized values
print(bio_clim_data)

# Visualize the normalized mean values
plt.figure(figsize=(12, 6))
plt.bar(bio_clim_data['Period'], bio_clim_data['Normalized_Mean_Value'])
plt.xlabel('Time Period')
plt.ylabel('Normalized Mean Value')
plt.title('Normalized Mean Values of Future Bioclimatic Data')
plt.xticks(rotation=45)
plt.tight_layout()

# Create the directory to save the plot if it doesn't exist
save_dir = 'images/tif'
Path(save_dir).mkdir(parents=True, exist_ok=True)

plt.show()
