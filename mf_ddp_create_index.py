# Z:\GIS\GIS_General\Tools\Scripts\mf_ddp_create_index.py
# ---------------------------------------------------------------------------
#
# mf_ddp_create_index.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 23/07/2020
# Last updated 24/07/2020
# Description: Creates a customised set of polygon features for use as a data-driven driven 
# index where a map series requires the display of unevenly distributed features. For example,
# a map series along a linear feature showing fauna habitat for several different species.
#
# Requirements: 
#
# 1.
# A "frame" polygon feature class that covers the map subject data. This feature
# class must have a field populated with unique identifiers ordered in the desired map sequence.
#
# 2.
# A map subject feature class with a field to identify the different subjects within a theme.
# For example, a map series showing habitat by species would require a "name" field.
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, os, collections


# User-supplied parameters
frames = arcpy.GetParameterAsText(0) # File path for the map extents feature class
frameSortField = arcpy.GetParameterAsText(1) # Name of field with unique vales to order map serie by
mapdata = arcpy.GetParameterAsText(2) # File path for the map subject feature class
mapDataSortField = arcpy.GetParameterAsText(3) # Name of field with map subject names (sub-series)
outDDPindex = arcpy.GetParameterAsText(4) # Name of new map index

# Preliminary setup
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0] # Dataframe object
lyrList = arcpy.mapping.ListLayers(df) # list the layers in the data frame
sr = df.spatialReference # Obtain the the spatial reference from the data frame

# Locate the frames layer in the TOC and obtain the path to the data source
for lyr in lyrList:
    if lyr.name == frames:
        if not lyr.isGroupLayer: # check if layer is a group layer
            if lyr.supports("DATASOURCE"): # check if layer supports 'datasource'
                dsrc = lyr.dataSource
outgdb = os.path.split(dsrc)[0] # Get the path to the gdb the frames FC is in.

# Local variables
fielddetails = [("MAP_SUBSERIES_NO", "SHORT", "", "", ""), ("MAP_SUBSERIES_ALPHA", "TEXT", "", "", 5), ("MAP_SUBSERIES_TOTAL", "SHORT", "", "", ""), ("DDP_SEQUENCE", "SHORT", "", "", "")]
tempFC = r"in_memory\tempFC" # File path for in-memory feature class
newIndex = os.path.join(outgdb, outDDPindex) # File path for the new ddp index
uniqueList = []
rowList = []
geomDict = {}
frameIntDict = {}
sortAlphaDict = {}
count = 0
countlist = []
seqCount = 0
previousName = False

# Environment Settings

# Setup status output
scriptName = 'mf_ddp_create_index.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Functions
def makeAlpha():
    alph = "abcdefghijklmnopqrstuvwxyz"
    alphaList = []
    for char in alph:
        alphaList.append(char)
    for char1 in alph:
        for char2 in alph:
            alphaList.append("{}{}".format(char1, char2)) 
    return alphaList

# Setup
msg = "\n\tCommencing setup..."
arcpy.AddMessage(msg)

# Obtain geometry objects from frame FC, add to dictionary with sort-field value as key
with arcpy.da.SearchCursor(frames, ["SHAPE@", frameSortField]) as cur:
    for row in cur:
        geomDict[row[1]] = row[0]

# Populate dictionary with sorted values from frames as keys and sequential integers as values
sortlist = list(geomDict)
sortlist.sort()
for i in sortlist:
    count += 1
    frameIntDict[i] = count

# Main

arcpy.AddMessage("\n\tCommencing intersect...")

# Intersection of polygon FCs to create tempFC in memory
arcpy.arcpy.Intersect_analysis([frames, mapdata], tempFC)

arcpy.AddMessage("\n\tIntersect completed")
msg = "\n\tCreating {}...".format(outDDPindex)
arcpy.AddMessage(msg)

# Create FC on disk with same schema and feature type as tempFC. Access via variable newIndex.
arcpy.CreateFeatureclass_management(outgdb, outDDPindex, "POLYGON", tempFC, "DISABLED", "DISABLED", sr)
arcpy.RefreshCatalog(newIndex)

msg = "\n\t{} created".format(outDDPindex)
arcpy.AddMessage(msg)

# Obtain list of field names
fields = [f.name for f in arcpy.ListFields(tempFC)]

# Obtain index numbers for the sort fields
mapDataSortFieldindex = fields.index(mapDataSortField)
frameSortFieldindex = fields.index(frameSortField)

# Filter unique frame-mapdata-intersects from tempFC and add to a list as a tuple.
with arcpy.da.SearchCursor(tempFC, "*") as cur:
    for row in cur:
        sorter = "{}{}".format(row[mapDataSortFieldindex], row[frameSortFieldindex])
        if sorter not in uniqueList:
            uniqueList.append(sorter)
            rowvals = row[1:]
            rowList.append((sorter, (rowvals)))

del tempFC  # we don't need it anymore and it may be occupying a lot of memory

# Sort the list of tuples
rowList.sort()

msg = "\n\tPopulating {} values".format(outDDPindex)
arcpy.AddMessage(msg)

# Populate newIndex with sorted rows from list
with arcpy.da.InsertCursor(newIndex, fields[1:]) as incursor:
    for r in rowList:
        incursor.insertRow(r[1])

msg = "\n\tReplacing goemetry in {}".format(outDDPindex)
arcpy.AddMessage(msg)

# Replace geometry created in intersect operation with frame geometry from frames FC.
with arcpy.da.UpdateCursor(newIndex, ["SHAPE@", frameSortField, mapDataSortField]) as cur:
    for row in cur:
        countlist.append(row[2])  # Assemble a list of frameSortField values to count for later use
        row[0] = geomDict[row[1]]  # Replace geometry
        cur.updateRow(row)

msg = "\n\tAdding DDP fields to {}".format(outDDPindex)
arcpy.AddMessage(msg)

# Add the new fields: MAP_SUBSERIES_NO, MAP_SUBSERIES_ALPHA, MAP_SUBSERIES_TOTAL & DDP_SEQUENCE
for fd in fielddetails:
    arcpy.AddField_management(newIndex, fd[0], fd[1], fd[2], fd[3])

# Create Counter object to produce totals of map sub-series
mapSubSeriesTotals = collections.Counter(countlist)

msg = "\n\tPopulating new DDP fields in {}".format(outDDPindex)
arcpy.AddMessage(msg)

with arcpy.da.UpdateCursor(newIndex, [frameSortField, mapDataSortField, "MAP_SUBSERIES_NO", "MAP_SUBSERIES_ALPHA", "MAP_SUBSERIES_TOTAL", "DDP_SEQUENCE"]) as cur:
    for row in cur:
        seqCount += 1   # Increment counter
        row[5] = seqCount   # Add value to DDP_SEQUENCE field
        if previousName != row[1]:   # Check if sub-series name has changed
            a = makeAlpha()  # Create list of sequential alphabetic characters
            previousName = row[1]   # Add current sub-series name
            row[2] = frameIntDict[row[0]]   # Populate MAP_SUBSERIES_NO with integer (1)
            row[3] = a.pop(0)   # Populate MAP_SUBSERIES_ALPHA with alphabetic char ('a')
            row[4] = mapSubSeriesTotals[row[1]]   # Populate MAP_SUBSERIES_TOTAL with total for sub-series
        else: # If sub-series name has not changed
            row[2] = frameIntDict[row[0]]   # Populate MAP_SUBSERIES_NO with next integer
            row[3] = a.pop(0)   # Populate MAP_SUBSERIES_ALPHA with next alphabetic char
            row[4] = mapSubSeriesTotals[row[1]]   # Populate MAP_SUBSERIES_TOTAL with total for sub-series
        cur.updateRow(row)


# Add new ddp index to TOC
layer = arcpy.mapping.Layer(newIndex)
arcpy.mapping.AddLayer(df, layer, "TOP")
arcpy.RefreshTOC()

# Refresh the map element
arcpy.RefreshActiveView()


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

