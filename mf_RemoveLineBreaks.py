#
#---------------------------------------------------------------------------
#
# RemoveLineBreaks.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 19/06/2016
# Last updated 19/06/2016
# Description: Removes line breaks and excess spaces from the specified text field.
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time

# User-supplied parameters
feat_layer = arcpy.GetParameterAsText(0)
fieldname = arcpy.GetParameterAsText(1)

# Setup status output
scriptName = 'RemoveLineBreaks.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Main
with arcpy.da.UpdateCursor(feat_layer, fieldname) as cur:
        for row in cur:
            if row[0] != None:
                noreturn = " ".join(row[0].split())
                row[0] = noreturn 
                cur.updateRow(row)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

