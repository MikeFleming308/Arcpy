# Z:\GIS\GIS_General\Tools\Scripts\mf_ddp_extents_to_frame_set.py
#---------------------------------------------------------------------------
#
# mf_ddp_extents_to_frame_set.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 27/07/2020
# Last updated 00/07/2020
# Description: Creates a polygon "frames "feature class representing the map extents for a data driven pages mxd using points or an event table as the index layer.
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, os
from arcpy import env  
from arcpy import mapping  

# User-supplied parameters
wkspace = arcpy.GetParameterAsText(0)
fcname = arcpy.GetParameterAsText(1)
field_names = ["SHAPE@", "DDP_PAGE_NO"]

# Environment
env.workspace = wkspace

# Local variables
framerows = []
compare = []
outfc = os.path.join(wkspace, fcname)

#  Function


# Setup status output
scriptName = 'mf_ddp_extents_to_polys.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
mxd = arcpy.mapping.MapDocument("CURRENT")  
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
spr = df.spatialReference

# indexLayer = mxd.dataDrivenPages.indexLayer
# fields = arcpy.ListFields(indexLayer)
# field_names = [f.name for f in fields]
# lyrList = arcpy.mapping.ListLayers(df)
# for lyr in lyrList:
    # if lyr.name == indexLayer.name:
        # dsrc = lyr.dataSource

# pnfield = mxd.dataDrivenPages.pageNameField
# pname = pnfield.name
  
# Main
arcpy.CreateFeatureclass_management(wkspace, fcname, "POLYGON", "", "DISABLED", "DISABLED", spr)
arcpy.RefreshCatalog(fcname)

arcpy.AddField_management(outfc, "DDP_PAGE_NO", "TEXT", "", "", 50)


with arcpy.da.InsertCursor(fcname, field_names) as cur:
    for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):  
        mxd.dataDrivenPages.currentPageID = pageNum
        pageNumText = str(pageNum)
        ex = df.extent
        test = (ex.XMin, ex.YMin, ex.XMax, ex.YMax)
        if test not in compare:
            v1 = arcpy.Point(ex.XMin,ex.YMin) # Point coords clockwise from bottom left of frame
            v2 = arcpy.Point(ex.XMin,ex.YMax)
            v3 = arcpy.Point(ex.XMax,ex.YMax)
            v4 = arcpy.Point(ex.XMax,ex.YMin)
            v5 = arcpy.Point(ex.XMin,ex.YMin) # back at start
            frame = arcpy.Polygon(arcpy.Array([[v1, v2, v3, v4, v5]]),spr)
            row = (frame, pageNumText)
            cur.insertRow(row)
        else:
            pass

# Add new ddp index to TOC
layer = arcpy.mapping.Layer(outfc)
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

