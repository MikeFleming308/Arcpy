
#---------------------------------------------------------------------------
# M:\SIS\Mapping\ReportTools\Scripts\ListFileGDBSandContents.py
# ListFileGDBSandContents.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 20/04/2018
# Last updated 04/05/2018
# Description: 
#
#---------------------------------------------------------------------------

# Import modules
from __future__ import print_function
import os, arcpy, time

# User-supplied parameters
dir = arcpy.GetParameterAsText(0)

# Local variables
outFile = os.path.join(dir, "File List.txt") 
msg1 = "This file provides geodatabase, feature dataset, feature class, folder, and file{}locations for the directory at: {}".format("\n", dir)
msg2 = "File geodatabases, feature datasets and feature classes are listed first.{}Folders and files are listed below the ESRI format data.".format("\n")
hashes = "#" * 80
underlinelen = 80
flag = True
exclude = set()
shpnames = set()
shapefilesuffix = [".shp", ".cpg", ".dbf", ".prj", ".shx", ".sbn", ".sbx", ".aux"]
shapefiles = set()

# Functions
def WriteGDBdetails(lists, featuretype):
    for flist, ftype in zip(lists, featuretype):
        if len(flist) > 0:
            cw = os.path.split(arcpy.env.workspace)[1]
            print("\n{} in {}".format(ftype, cw),  sep='', end="\n", file=outF)
            for i in flist:
                print("\t{}".format(i),  sep='', end="\n", file=outF)

def Get_and_write_gdb_details():
    fclist = arcpy.ListFeatureClasses() # Create list of feature classes in the current workspace
    fdlist = arcpy.ListDatasets(feature_type='feature') # Create list of feature datasets in current workspace
    rasterlist = arcpy.ListRasters() # Create list of raster datasets in current workspace
    tablelist = arcpy.ListTables() # Create list of tables in current workspace
    lists = [fclist, fdlist, rasterlist, tablelist]
    featuretype = ["FEATURE CLASS:", "FEATURE DATASET:", "RASTER:", "TABLE:"]
    WriteGDBdetails(lists, featuretype)
    if len(fdlist) > 0:
        for fd in fdlist:
            arcpy.env.workspace = os.path.join(path, fd)
            fclist = arcpy.ListFeatureClasses() # Create list of feature classes in the current feature dataset
            rasterlist = arcpy.ListRasters() # Create list of raster datasets in current feature dataset
            tablelist = arcpy.ListTables() # Create list of tables in current feature dataset
            lists = [fclist, rasterlist, tablelist]
            featuretype = ["FEATURE CLASS:", "RASTER:", "TABLE:"]
            WriteGDBdetails(lists, featuretype)

# Setup status output
scriptName = 'ListFileGDBSandContents.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Main
with open(outFile, "w") as outF:

    print("{}".format("\n" * 2), sep='', end="\n", file=outF)
    print("{}".format(hashes), sep='', end="\n" * 2, file=outF)
    print(msg1, sep='', end="\n" * 2, file=outF)
    print("This file was created on {}.".format(StartTime), sep='', end="\n" * 2, file=outF)
    print(msg2, sep='', end="\n" * 2, file=outF)
    print("{}".format(hashes), sep='', end="\n" * 2, file=outF)
    
    for root, dirs, files in os.walk(dir):
        fileslist = os.listdir(root)
        if len(fileslist) > 0:
            for fname in fileslist:
                if fname.endswith(".shp"):
                    shppath = os.path.join(root, fname)
                    shapefiles.add(shppath)
                    shpnames.add(fname)
                elif fname.endswith(".shp.xml"):
                    exclude.add(os.path.join(root, fname))
            shpabbrv = [shp[:-4] for shp in shpnames]
            for fname in fileslist:
                if fname[:-4] in shpabbrv and fname[-4:] in shapefilesuffix:
                    exclude.add(os.path.join(root, fname))
        for d in dirs:
            path = os.path.join(root, d) # Create path to current directory
            arcpy.env.workspace = path # Set workspace to current directory
            if d.endswith(".gdb"): # For each geodatabase
                exclude.add(path)
                
                print("{}Geodatabase: {}".format("\n" * 2, d), sep='', end="\n", file=outF)
                print("{}".format("-" * underlinelen),  sep='', end="\n", file=outF)
                print("Location: {}".format(path),  sep='', end="\n", file=outF)
                Get_and_write_gdb_details()

    print("{}{}{}".format("\n", hashes, "\n"), sep='', end="\n", file=outF) 
    print("Shapefiles.\n", sep='', end="\n", file=outF)
    shapes = sorted(list(shapefiles))
    for shp in shapes:
        if shp is not None:
            print(shp, sep='', end="\n", file=outF)
    print("{}{}{}".format("\n", hashes, "\n"), sep='', end="\n", file=outF) 
    print("Non-geodatabase folders and files.\n", sep='', end="\n", file=outF)
    for root, dirs, files in os.walk(dir):
        if len(files) > 0:
            for name in files:
                if not root.endswith(".gdb"):
                    cp = os.path.join(root, name)
                    if cp not in exclude:
                        print(cp, sep='', end="\n", file=outF)

    print("\nEnd of file.{}{}".format("\n" * 2, hashes), sep='', end="\n", file=outF)

#Open resulting text file
os.startfile(outFile)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")
