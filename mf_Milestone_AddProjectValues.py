#
#---------------------------------------------------------------------------
# C:\Users\Michael.Fleming\OneDrive - Aurecon Group\ArcMap\Scripts\Milestone_AddProjectValues.py
# Milestone_AddProjectValues.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 26/04/2019
# Last updated 10/06/2019
# Description: Populates standard ARTC fields for all feature classes in the nominated gdb.
# Currently hard-coded, needs to be updated to take parameters 
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, os

# User-supplied parameters
infc = arcpy.GetParameterAsText(0)
projname = arcpy.GetParameterAsText(1)
projid = arcpy.GetParameterAsText(2)


# Local variables
mgaZone = 56
phase = 2

update_dict = {'ProjName': projname, 'PROJ_ID': projid, 'MGA_Z': mgaZone, 'ProjID': projid, 'MGA_Zone': mgaZone, 'Project': projname, 'ProjPhase': phase, 'ProjectPhase': phase, "PROJ_PHASE": phase, 'PROJ_NAME': projname}

udpdate_list = ["ProjID", "Project", "ProjName", "ProjPhase", "ProjectPhase", "PROJ_PHASE", "MGA_Z", "PROJ_ID", "PROJ_NAME", "MGA_Zone"]

# Environment Settings

# Setup status output
scriptName = 'Milestone_AddProjectValues.py'
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
fcfields = arcpy.ListFields(infc)
fnameList = [f.name for f in fcfields]
for fname in fnameList:
    if fname in udpdate_list:
        with arcpy.da.UpdateCursor(infc, fname) as cur:
            for row in cur:
                row[0] = update_dict[fname]
                cur.updateRow(row)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

