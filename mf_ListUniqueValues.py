#
#---------------------------------------------------------------------------
#
# ListUniqueValues.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 02/01/2015
# Last updated 02/01/2015
# Description: Creates a list of unique values and frequency for a specified field.
#              Opens a txt file "Frequency.txt" to display values
#---------------------------------------------------------------------------

# Import modules
import os, arcpy, time

# User-supplied parameters


# Local variables
table_ = arcpy.GetParameterAsText(0)
field_ = arcpy.GetParameterAsText(1)
frqDict = {}
outFile = "C:/TEMP/Frequency.txt"
outDir = "C:/TEMP" 

# Setup status output
scriptName = 'ListUniqueValues.py'
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


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

vals = unique_values(table_, field_)

def frq_count(table, field, inputValue):
    count = 0
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        for row in cursor:
            if row[0] == inputValue:
                count += 1
    return count

for v in vals:
    frqDict[v] = frq_count(table_, field_, v)

# Main
for e in vals:
    outF.write(str(frqDict[e]) + "\t" + e + "\n")

outF.close

#Open resulting text file
os.startfile(outFile)


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

