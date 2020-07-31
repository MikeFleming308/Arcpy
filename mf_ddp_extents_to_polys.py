#
#---------------------------------------------------------------------------
#
# mf_ddp_extents_to_polys.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 18/11/2019
# Last updated 18/11/2019
# Description: Creates polygons representing the map extents for a data driven pages mxd using points or an event table as the index layer.
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time
from arcpy import env  
from arcpy import mapping  

# User-supplied parameters
wkspace = arcpy.GetParameterAsText(0)
fcname = arcpy.GetParameterAsText(1)

# Environment
env.workspace = wkspace

# Local variables
extents = []


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
mxd = mapping.MapDocument("CURRENT")  
dataframe = mapping.ListDataFrames(mxd, "*")[0]  

  
# Main

for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):  
     mxd.dataDrivenPages.currentPageID = pageNum  
     frameExtent = dataframe.extent    
     XMAX = frameExtent.XMax    
     XMIN = frameExtent.XMin    
     YMAX = frameExtent.YMax    
     YMIN = frameExtent.YMin    
     pnt1 = arcpy.Point(XMIN, YMIN)    
     pnt2 = arcpy.Point(XMIN, YMAX)    
     pnt3 = arcpy.Point(XMAX, YMAX)    
     pnt4 = arcpy.Point(XMAX, YMIN)    
     array = arcpy.Array()    
     array.add(pnt1)    
     array.add(pnt2)    
     array.add(pnt3)    
     array.add(pnt4)    
     array.add(pnt1)    
     polygon = arcpy.Polygon(array)   
     extents.append(polygon)  
  
arcpy.CopyFeatures_management(extents, fcname)   






# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

