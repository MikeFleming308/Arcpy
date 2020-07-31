# Z:\GIS\GIS_General\Tools\Scripts\mf_SummariseZoneAreas.py
# Also..
# C:\Users\Michael.Fleming\OneDrive - Aurecon Group\ArcMap\Scripts\SummariseZoneAreas.py
# C:\Users\Michael.Fleming\AppData\Roaming\ESRI\Desktop10.5\ArcToolbox\My Toolboxes\Scripts\SummariseZoneAreas.py
#---------------------------------------------------------------------------
# 
# SummariseZoneAreas.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 29/01/2019
# Last updated 12/04/2020
# Description: Designed for use with specific input feature class. (Any poly FC interscted with a "Zone" FC) First param is target FC. Second param is the field in target FC to group output (areas in ha) by. There are 4 columns of output, allowing up to 4 zone fields (with values of -1 or 1) to be added. If less fields required, just enter one or more of the desired fields.
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, xlwt, os

# User-supplied parameters
intersectedFC = arcpy.GetParameterAsText(0)
group_by_field = arcpy.GetParameterAsText(1)
col_1_FID = arcpy.GetParameterAsText(2)
col_2_FID = arcpy.GetParameterAsText(3)
col_3_FID = arcpy.GetParameterAsText(4)
col_4_FID = arcpy.GetParameterAsText(5)
outputdir = arcpy.GetParameterAsText(6)

# Function
def parseoutpath(outfolder,instring): 
    fname = "{}.xls".format(instring)
    rename = False
    for i in [":", ":\\", "\\", ".gdb"]:
        if i in instring:
            rename = True
    if rename:
        newname = os.path.split(instring)[1]
        fname = "{}.xls".format(newname)
    outputpath = os.path.join(outfolder, fname)
    return outputpath


# Local variables
# headerlist = ["CASE_ID", col_1_FID[4:], col_2_FID[4:], col_3_FID[4:], col_4_FID[4:]] # ["CASE_ID", "COL_1", "COL_2", "COL_3", "COL_4"]
headerlist = [group_by_field, col_1_FID[4:], col_2_FID[4:], col_3_FID[4:], col_4_FID[4:]] # ["CASE_ID", "COL_1", "COL_2", "COL_3", "COL_4"]
fieldlist = ["SHAPE@AREA", group_by_field, col_1_FID, col_2_FID, col_3_FID, col_4_FID]
casedict = {}
outpath = parseoutpath(outputdir, intersectedFC)
col_count = 0
rowNo = 0

# Environment settings
arcpy.env.overwriteOutput = True

# Setup status output
scriptName = 'SummariseZoneAreas.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Setup 

book = xlwt.Workbook()
sheet = book.add_sheet("Register")

# Main
with arcpy.da.SearchCursor(intersectedFC, fieldlist) as cur:
    for row in cur:
        ha = row[0]/10000
        case_id = row[1]
        if case_id not in casedict:
            casedict[case_id] = {"col_1": 0.0, "col_2": 0.0, "col_3": 0.0, "col_4": 0.0}
        if row[2] != -1:
            casedict[case_id]["col_1"] += ha
        if row[3] != -1:
            casedict[case_id]["col_2"] += ha
        if row[4] != -1:
            casedict[case_id]["col_3"] += ha
        if row[5] != -1:
            casedict[case_id]["col_4"] += ha

for f in headerlist: # Create field names in output table
    sheet.write(0, col_count, f)
    col_count += 1
# print casedict
caselist = list(casedict)
cases = sorted(caselist)

for case in cases:
    rowdict = casedict[case]
    rowvals = [case, rowdict["col_1"], rowdict["col_2"], rowdict["col_3"], rowdict["col_4"]]
    rowNo += 1
    colNo = 0
    for val in rowvals:
        sheet.write(rowNo, colNo, val)
        colNo += 1

book.save(outpath)
os.startfile(outpath)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

