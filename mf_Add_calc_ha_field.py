#
#---------------------------------------------------------------------------
#
# ha.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 00/03/2019
# Last updated 00/03/2019
# Description: Checks if field "HA" or "ha" exists, if so, is it of type Double. If not, create new. Calculates area in hectrares 
#              Calculates area in hectares if coordinate system in metres
#---------------------------------------------------------------------------

# Import modules
import arcpy, time


# User-supplied parameters
featclass = arcpy.GetParameterAsText(0)
# = arcpy.GetParameterAsText(1)

# Local variables
existingHAfield = None
# Environment Settings

# Setup status output
scriptName = 'ha.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
fields = arcpy.ListFields(featclass)
for f in fields: # Check if field exists
    if f.name in ["HA", "ha"]:
        if f.type == 'Double':
            existingHAfield = f
            fieldname = f.name

# Main
if existingHAfield is not None: # Update existing field
    with arcpy.da.UpdateCursor(featclass, [fieldname, "SHAPE@AREA"]) as cur:
        for row in cur:
            row[0] = row[1]/10000
            cur.updateRow(row)
else: # Create field
    arcpy.AddField_management(featclass, "HA", "DOUBLE", "", "", "", "ha")
    with arcpy.da.UpdateCursor(featclass, ["HA", "SHAPE@AREA"]) as cur:
        for row in cur:
            row[0] = row[1]/10000
            cur.updateRow(row)

# arcpy.RefreshCatalog(featclass)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

