#
#---------------------------------------------------------------------------
#
# FID_homogeniser.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 04/03/2019
# Last updated 04/03/2019
# Description: Operates on all fields with name prefix of "FID_" Values of -1 retained, all positive integers converted to 1
#              For use with appended datasets the have 'FID' (Feature ID) fields. 
#---------------------------------------------------------------------------

# Import modules
import arcpy, time


# User-supplied parameters
featclass = arcpy.GetParameterAsText(0)

# Local variables
# Environment Settings

# Setup status output
scriptName = 'FID_homogeniser.py'
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

# Main
for f in fields:
    if f.name.startswith("FID_"):
        with arcpy.da.UpdateCursor(featclass, f.name) as cur:
            for row in cur:
                if row[0] <= 0:
                    row[0] = -1
                else:
                    row[0] = 1
                cur.updateRow(row)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

