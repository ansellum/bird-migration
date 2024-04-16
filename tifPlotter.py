import os
import zipfile
import rasterio
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the directory where the zip files are located
zip_files_dir = 'tif_files'  # Adjust this to your directory containing the zip files
save_dir = 'images/tif'  # Directory to save the images

# Create the directory to save images if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# List all zip files in the directory
zip_files = sorted([f for f in os.listdir(zip_files_dir) if f.endswith('.zip')])

# Loop over each zip file
for zip_file in zip_files:
    # Extract the climate variable from the file name
    variable = zip_file.split('_')[-1].split('.')[0]
    
    # Define the path to the zip file and the directory to extract to
    zip_path = os.path.join(zip_files_dir, zip_file)
    extract_to_dir = os.path.join(zip_files_dir, variable)
    
    # Create the directory to extract to if it doesn't exist
    Path(extract_to_dir).mkdir(parents=True, exist_ok=True)
    
    # Unzip the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)
    
    # List all .tif files in the directory
    tif_files = sorted([f for f in os.listdir(extract_to_dir) if f.endswith('.tif')])
    
    # Initialize an empty list to hold the data
    time_series_data_list = []
    
    # Loop over each .tif file
    for file_name in tif_files:
        # Extract information from the file name
        month = int(file_name.split('_')[-1].split('.')[0])
        
        # Open the .tif file
        with rasterio.open(os.path.join(extract_to_dir, file_name)) as src:
            # Read the data for the entire .tif file
            data = src.read(1)
            
            # Flatten the array and filter out invalid values
            valid_data = data.flatten()
            valid_data = valid_data[~src.dataset_mask().flatten() == 0]  # Mask out the nodata cells
            valid_data = valid_data[valid_data < 1e30]  # Filter out extreme values that could cause overflow
            
            mean_value = valid_data.mean() if valid_data.size > 0 else float('nan')
    
            # Append the data to the list
            time_series_data_list.append({'Month': month, 'Mean_Value': mean_value})
    
    # Convert the list of dictionaries to a DataFrame
    time_series_data = pd.DataFrame(time_series_data_list)
    
    # Visualize the mean values for each month
    plt.figure(figsize=(12, 6))
    plt.plot(time_series_data['Month'], time_series_data['Mean_Value'])
    plt.xlabel('Month')
    plt.ylabel('Mean Value')
    plt.title(f'Mean Values of {variable.capitalize()} by Month')
    plt.tight_layout()
    
    # Save the plot with variable name as label
    plt.savefig(os.path.join(save_dir, f'{variable}_mean_values_plot.png'))
    
    # Close the plot to release memory
    plt.close()
