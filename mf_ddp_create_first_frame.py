# Z:\GIS\GIS_General\Tools\Scripts\mf_ddp_create_first_frame.py
#---------------------------------------------------------------------------
#
# mf_ddp_create_first_frame.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 23/07/2020
# Last updated: 23/07/2020
# Description: Creates a polygon feature class to use as a data-driven index. Populates the 
# feature class with a single polygon from the current data frame extent. This polygon can
# then be copied and replicated within the same feature class to build up an index in a 
# subsequent edit session. The comleted index can be used as-is or as input to the 
# DDP_Create_Index tool
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, os


# User-supplied parameters
ddpindex = arcpy.GetParameterAsText(0)
outgdb = arcpy.GetParameterAsText(1)

# Local variables
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
fields = ["FRAME_ORDER", "SCALE"]
fdict = {"FRAME_ORDER": "SHORT", "SCALE": "LONG"}
fpath = os.path.join(outgdb, ddpindex)

# Setup status output
scriptName = 'mf_ddp_create_first_frame.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Setup 
def makeFrame(dataframe):
    ex = dataframe.extent
    spr = dataframe.spatialReference
    v1 = arcpy.Point(ex.XMin,ex.YMin) # Point coords clockwise from bottom left of frame
    v2 = arcpy.Point(ex.XMin,ex.YMax)
    v3 = arcpy.Point(ex.XMax,ex.YMax)
    v4 = arcpy.Point(ex.XMax,ex.YMin)
    v5 = arcpy.Point(ex.XMin,ex.YMin) # back at start
    frame = arcpy.Polygon(arcpy.Array([[v1, v2, v3, v4, v5]]),spr)
    return frame

# Main
# Create new empty polygon feature class 
msg = "\nCreating {} feature class...".format(ddpindex)
arcpy.AddMessage(msg)

arcpy.CreateFeatureclass_management(outgdb, ddpindex, "POLYGON", "", "DISABLED", "DISABLED", df.spatialReference)

msg = "\n{} feature class created".format(ddpindex)
arcpy.AddMessage(msg)

arcpy.RefreshCatalog(fpath)

# Create a polygon (rectangle) from the current map extent
newframe = makeFrame(df)

# Add the polygon to the new feature class
arcpy.CopyFeatures_management(newframe, fpath) 

# Add the fields to the new feature class
for f in fields:
    arcpy.AddField_management(fpath, f, fdict[f])

# Create a feature layer from the feature class and add it to the map TOC
layer = arcpy.mapping.Layer(fpath)
arcpy.mapping.AddLayer(df, layer, "TOP")

# Refresh the TOC and map
arcpy.RefreshTOC()
arcpy.RefreshActiveView()


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

