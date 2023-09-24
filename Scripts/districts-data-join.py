import arcpy
import os
from arcpy import env

env.workspace = "D:\\Aalto University\\B.Sc Econ - Immigration & Public Transportation\\Immigrant Pattern & Public Transport Accessibility"

central_folder = os.path.join(env.workspace, "Data\\Travel_Time_Matrix_tables")
ykr_grid_table = os.path.join(env.workspace, "Data\\MetropAccess_YKR_grid\\MetropAccess_YKR_grid_EurefFIN.shp")
district_table = os.path.join(env.workspace, "Data\\HMA_districts\\HEV_districts.shp")

# Check if larger_district_file already exists and delete if true
larger_district_file = os.path.join(env.workspace, "Data", "joined-districts.shp")
if arcpy.Exists(larger_district_file):
    arcpy.Delete_management(larger_district_file)

# Create a larger district file by copying the original district file
arcpy.Copy_management(district_table, larger_district_file)

file_list = [os.path.join(central_folder, f) for f in os.listdir(central_folder) if f.endswith('.txt')]

for file in file_list:
    year_id = file.split("\\")[-1].replace(".txt", "")
    year, file_id = year_id.split('-')

    in_table = os.path.join(central_folder, file)

    # Create a temporary table view specifying the delimiter as ';'
    temp_view = "temp_view"
    
    try:
        arcpy.MakeTableView_management(in_table, temp_view, "", "", field_info="from_id from_id VISIBLE NONE;to_id to_id VISIBLE NONE;walk_t walk_t VISIBLE NONE;walk_d walk_d VISIBLE NONE;pt_m_tt pt_m_tt VISIBLE NONE;pt_m_t pt_m_t VISIBLE NONE;pt_m_d pt_m_d VISIBLE NONE;car_m_t car_m_t VISIBLE NONE;car_m_d car_m_d VISIBLE NONE")
    except Exception as e:
        print(f"Error creating the temp view for {in_table}. Error: {str(e)}")
        continue

    # Join with YKR grid table
    arcpy.JoinField_management(ykr_grid_table, "YKR_ID", temp_view, "from_id")

    # Remove rows with values of -1
    with arcpy.da.UpdateCursor(ykr_grid_table, "*") as cursor:
        for row in cursor:
            if -1 in row:
                cursor.deleteRow()

    # Spatial join with the district table
    spatial_join_output = "spatial_join_" + year_id
    field_mappings = arcpy.FieldMappings()
    for field in arcpy.ListFields(ykr_grid_table):
        if field.name not in ["from_id", "to_id"]:
            field_map = arcpy.FieldMap()
            field_map.addInputField(ykr_grid_table, field.name)
            field_map.mergeRule = "Min"
            field_mappings.addFieldMap(field_map)

    arcpy.SpatialJoin_analysis(target_features=ykr_grid_table, join_features=district_table,
                                out_feature_class=spatial_join_output, join_type="KEEP_COMMON", field_mapping=field_mappings)

   # Rename columns
    for field in arcpy.ListFields(spatial_join_output):
        if field.name not in ["from_id", "to_id"]:
            new_name = f"{year}-{file_id}-{field.name}"
            arcpy.AlterField_management(spatial_join_output, field.name, new_name)

    # Join the new fields to the larger district file
    arcpy.JoinField_management(larger_district_file, "from_id", spatial_join_output, "from_id")

    # Cleanup the joins from the ykr_grid_table for the next iteration
    for field in arcpy.ListFields(ykr_grid_table):
        if field.name.startswith(year + "-" + file_id):
            arcpy.DeleteField_management(ykr_grid_table, field.name)

print(f"Final updated file saved at: {larger_district_file}")
print("Process completed!")
