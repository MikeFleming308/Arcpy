
#---------------------------------------------------------------------------
#C:\Users\Michael.Fleming\Documents\Coding\Python Scripts\Py\REDecomposer.py
# REDecomposer.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 04/11/2018
# Last updated 04/11/2018
# Description: 
# RE polygons are heterogenous in that they may represent up to 5 regional ecosystems each. 
# The names are held in the RE1, RE2, RE3, RE4 & RE5 fields and their respective proportion in
# proportion in the PC1, PC2, PC3, PC4 & PC5 fields. The out put of this script is a list of 
# each component Re and its area in hectares.
#
#
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, csv, os

# User-supplied parameters
refc = arcpy.GetParameterAsText(0)
outputdir = arcpy.GetParameterAsText(1)
# refc = r"C:\Users\Michael.Fleming\Documents\Ecology\ClippedToEcologyStudyArea.gdb\mga56\Regional_Ecosystem_v10"
# outputdir = r"C:\Users\Michael.Fleming\Documents\Ecology"


# Local variables
flist = ["RE1", "RE2", "RE3", "RE4", "RE5", "PC1", "PC2", "PC3", "PC4", "PC5", "SHAPE@AREA"]
sqmdict = {}
out_csv = os.path.join(outputdir, "DecomposedREs.csv")
fieldNames = ['RE_NAME', 'HA']
halist = []

# Setup status output
scriptName = 'REDecomposer.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
# Create and open a csv file to write to:
outfn = open(out_csv, "wb")
RE_Writer = csv.writer(outfn, dialect='excel', delimiter=',')
RE_Writer.writerow(fieldNames)


# Main
with arcpy.da.SearchCursor(refc, flist) as cur:
	for row in cur:
		re1, re2, re3, re4, re5, pc1, pc2, pc3, pc4, pc5, sqm = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
		if re1 not in sqmdict:
			sqmdict[re1] = sqm * (pc1 / 100.0)
		else:
			sqmdict[re1] += sqm * (pc1 / 100.0)
			
		if re2 is not None:
			if re2 not in sqmdict:
				sqmdict[re2] = sqm * (pc2 / 100.0)
			else:
				sqmdict[re2] += sqm * (pc2 / 100.0)
				
			if re3 is not None:
				if re3 not in sqmdict:
					sqmdict[re3] = sqm * (pc3 / 100.0)
				else:
					sqmdict[re3] += sqm * (pc3 / 100.0)
					
				if re4 is not None:
					if re4 not in sqmdict:
						sqmdict[re4] = sqm * (pc4 / 100.0)
					else:
						sqmdict[re4] += sqm * (pc4 / 100.0)
						
					if re5 is not None:
						if re5 not in sqmdict:
							sqmdict[re5] = sqm * (pc5 / 100.0)
						else:
							sqmdict[re5] += sqm * (pc5 / 100.0)

for i in sqmdict:
	val = sqmdict[i]
	if val is not None:
		ha = (val/10000.0)
	halist.append([i, ha])

for re in halist:
	RE_Writer.writerow(re)

outfn.close()

os.startfile(out_csv)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

