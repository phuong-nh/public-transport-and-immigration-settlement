import pandas as pd
import os

# Given IDs and folders as before
ids = [
    5961860, 5934892, 5980222, 5978639, 5975374, 5980260,
    5968821, 5961894, 5961890, 5952975, 5958354, 5911249,
    5934906, 5874358, 5878088
]

folders = [
    "HelsinkiRegion_TravelTimeMatrix2013",
    "HelsinkiRegion_TravelTimeMatrix2015",
    "HelsinkiTravelTimeMatrix2018"
]

central_folder = "D:\Aalto University\\B.Sc Econ - Immigration & Public Transportation\\Immigrant Pattern & Public Transport Accessibility\\Data\\Travel_Time_Matrix_tables"

# Initialize a DataFrame to store merged data
merged_df = pd.DataFrame()

# Iterate over main folders
for folder in folders:
    year = folder.split('Matrix')[-1]
    
    for id_ in ids:
        sub_folder_name = f"{str(id_)[:4]}xxx"
        file_name = f"{year}-{id_}.txt"
        file_path = os.path.join(central_folder, file_name)
        
        if os.path.exists(file_path):
            # Read the file into a DataFrame
            df = pd.read_csv(file_path, sep=';')
            
            # Set 'from_id' and 'to_id' as index
            df.set_index(['from_id', 'to_id'], inplace=True)
            
            # Update column names based on year
            new_columns = [f"{year}_{col}" for col in df.columns]
            df.columns = new_columns
            
            # Merge this data into merged_df
            if merged_df.empty:
                merged_df = df
            else:
                merged_df = merged_df.combine_first(df)

# Save the merged DataFrame
merged_df.reset_index(inplace=True) # Reset the multi-index if needed
merged_df.to_csv(os.path.join(central_folder, "merged_data.csv"), sep=';', index=False)

print("Data merged and saved!")
