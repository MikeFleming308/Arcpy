#
#---------------------------------------------------------------------------
# M:\SIS\Mapping\ReportTools\Scripts\ListFileGDBSandContents.py
# ListFileGDBSandContents.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 20/04/2018
# Last updated 24/04/2018
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
        for d in dirs:
            if d.endswith(".gdb"): # For each geodatabase
                path = os.path.join(root, d) # Create path to current gdb.
                arcpy.env.workspace = path # Set workspace to current gdb.
                
                print("{}Geodatabase: {}".format("\n" * 2, d), sep='', end="\n", file=outF)
                print("{}".format("-" * underlinelen),  sep='', end="\n", file=outF)
                print("Location: {}".format(path),  sep='', end="\n", file=outF)
                
                fclasses = arcpy.ListFeatureClasses() # Create list of feature classes in the current workspace
                fdatasets = arcpy.ListDatasets(feature_type='feature') # Create list of feature datasets in current workspace
                countfc = len(fclasses)
                countfd = len(fdatasets)
                if countfd > 0:
                    if countfd == 1:
                        fdmsg = "There is a single feature dataset in {} and {} feature classes at the same level\n".format(d, countfc)
                        print(fdmsg, sep='', end="\n", file=outF)

                        if countfc > 0:
                            print("The Feature Classes are:\n", sep='', end="\n", file=outF)
                            for fc in fclasses:
                                print(fc, sep='', end="\n", file=outF)
                                    
                        arcpy.env.workspace = os.path.join(path, fdatasets[0])
                        
                        print("\nFeature Dataset: {}".format(fdatasets[0]), sep='', end="\n", file=outF)
                        
                        fdfclasses = arcpy.ListFeatureClasses() # Create list of feature classes in the current workspace
                        countfdfc = len(fdfclasses)
                        
                        print("{}".format("." * underlinelen),  sep='', end="\n", file=outF)
                        print(os.path.join(path, fdatasets[0]), sep='', end="\n" * 2, file=outF)
                        print("\nThere are {} feature classes in feature dataset: {}.".format(countfdfc, fdatasets[0]), sep='', end="\n" * 2, file=outF)
                        for fc in fdfclasses:
                                print("\t{}".format(fc), sep='', end="\n", file=outF)
                        
                    else:
                        fdmsg = "There are {} feature datasets in {} and {} feature classes at the same level".format(countfd, d, countfc)
                        print(fdmsg, sep='', end="\n", file=outF)
                        
                        for fd in fdatasets: 
                            arcpy.env.workspace = os.path.join(path, fd)
                            fdfclasses = arcpy.ListFeatureClasses() # Create list of feature classes in the current workspace
                            countfdfc = len(fdfclasses)
                            
                            print("{}".format("." * underlinelen),  sep='', end="\n", file=outF)
                            print(arcpy.env.workspace,  sep='', end="\n", file=outF)
                            print("\nThere are {} feature classes in feature dataset: {}.".format(countfdfc, fd), sep='', end="\n" * 2, file=outF)
                            for fc in fdfclasses:
                                print("\t{}".format(fc), sep='', end="\n", file=outF)
                    
                else:
                    if countfc > 0:
                    
                        print("There are no feature datasets in {} but there are {} feature classes.".format(d, countfc), sep='', end="\n", file=outF)
                        print("The Feature Classes are:", sep='', end="\n" * 2, file=outF)
                        for fc in fclasses:
                            print("\t{}".format(fc), sep='', end="\n", file=outF)
                    else:
                        print("There are no features in {}.".format(d), sep='', end="\n", file=outF)
                        
    print("{}{}{}".format("\n", hashes, "\n"), sep='', end="\n", file=outF)
    print("Non-geodatabase folders and files.\n", sep='', end="\n", file=outF)
    for root, dirs, files in os.walk(dir):
        if len(files) > 0:
            
            for name in files:
                if not root.endswith(".gdb"):
                    print(os.path.join(root, name), sep='', end="\n", file=outF)
        elif len(files) == 0:
            print("No non-geodatabase folders and files were found.", sep='', end="\n", file=outF)
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
