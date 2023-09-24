import os
import shutil

# Given IDs
ids = [
    5961860, 5934892, 5980222, 5978639, 5975374, 5980260,
    5968821, 5961894, 5961890, 5952975, 5958354, 5911249,
    5934906, 5874358, 5878088
]

# Project folder
project_folder = "D:\Aalto University\\B.Sc Econ - Immigration & Public Transportation\\Immigrant Pattern & Public Transport Accessibility\\Data"

# Main folders
folders = [
    "HelsinkiRegion_TravelTimeMatrix2013",
    "HelsinkiRegion_TravelTimeMatrix2015",
    "HelsinkiTravelTimeMatrix2018"
]

for folder in folders:
    # Formulate the path
    path = os.path.join(project_folder, folder)
    
    # Check if the path exists
    if os.path.exists(path):
        print(f"Path {path} exists")
    else:
        print(f"Path {path} does not exist")

# Central folder path
central_folder = "D:\Aalto University\\B.Sc Econ - Immigration & Public Transportation\\Immigrant Pattern & Public Transport Accessibility\\Data\\Travel_Time_Matrix_tables"

# Ensure the central folder exists or create it
if not os.path.exists(central_folder):
    os.mkdir(central_folder)

# Iterate over main folders
for folder in folders:
    # Extract the year from the folder name
    year = folder.split('Matrix')[-1]
    print()
    print(f"Year {year}")
    
    # Iterate over each ID
    for id_ in ids:
        # Create the subfolder name based on ID
        sub_folder_name = f"{str(id_)[:4]}xxx"
        sub_folder_path = os.path.join(folder, sub_folder_name)
        print(f"{year}-{sub_folder_name}")
        
        # If sub folder exists
        if os.path.exists(sub_folder_path):
            # Formulate the file name
            file_name = f"travel_times_to_ {id_}.txt"
            file_path = os.path.join(sub_folder_path, file_name)
            print(f"{year}-{sub_folder_name}-{id_}")
            print(file_path)
            
            # Check if the file exists
            if os.path.exists(file_path):
                # Create a new name for the file based on year and ID
                new_file_name = f"{year}-{id_}.txt"
                new_file_path = os.path.join(central_folder, new_file_name)
                
                # Copy the file to the central folder with the new name
                shutil.copyfile(file_path, new_file_path)
                print(f"Copied {file_path} to {new_file_path}")

print("\nProcess Completed!")
