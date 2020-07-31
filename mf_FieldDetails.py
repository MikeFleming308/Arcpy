#
#---------------------------------------------------------------------------
#
# FieldDetails.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 20/04/2016
# Last updated 20/04/2016
# Description: Creates a table of field names, type and length.
#              Opens a txt file "Field Details.txt" to display values
#---------------------------------------------------------------------------

# Import modules
from __future__ import print_function
import os, arcpy, time

# User-supplied parameters


# Local variables
table_ = arcpy.GetParameterAsText(0)
outFile = "C:/TEMP/Field Details.txt"
outDir = "C:/TEMP" 

# Setup status output
scriptName = 'FieldDetails.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
if not os.path.exists(outDir):
    os.makedirs(outDir)

outF = open(outFile, "w")

outF.close

fList = arcpy.ListFields(table_)
MaxNameLen = max([len(f.name) for f in fList]) + 2
lineLen = "_" * (MaxNameLen + 27)

# Main
with open(outFile, "w") as outF:
    headSpace = " " * (MaxNameLen - 10)
    print("{}{}{}\t{}".format("FIELD_NAME", headSpace, "FIELD_TYPE", "FIELD_LENGTH"), sep='', end='\n', file=outF)
    print(lineLen, sep='', end='\n', file=outF)
    for f in fList:
       n = f.name
       space1 = " " * (MaxNameLen - len(n))
       t = f.type
       space2 = " " * (15 - len(t))
       l = f.length
       print('{}{}{}{}{}'.format(n, space1, t, space2, l), sep=' ', end='\n', file=outF)

#Open resulting text file
os.startfile(outFile)


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

