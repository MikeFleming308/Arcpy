#
#---------------------------------------------------------------------------
#
# <scriptname>
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 10/07/2018
# Last updated 10/07/2018
# Description: 
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time


# User-supplied parameters
# = arcpy.GetParameterAsText(0)
# = arcpy.GetParameterAsText(1)

# Local variables

# Environment Settings

# Setup status output
scriptName = 'Parking_Occupancy.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 




# Main







# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

