#
#---------------------------------------------------------------------------
#
# RegisterToXls.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 10/07/2018
# Last updated 11/07/2018
# Description: 
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, xlrd, os, xlwt

# User-supplied parameters
excel_path = arcpy.GetParameterAsText(0)
sheetNo = arcpy.GetParameterAsText(1)
headerRowNo = arcpy.GetParameterAsText(2)
stop = arcpy.GetParameterAsText(3)

# Local variables
dir_path = os.path.split(excel_path)[0]
RegisterExcel = os.path.join(dir_path, "Simplified_Register.xls")
book = xlwt.Workbook()
sheet = book.add_sheet("Register")
row_list = []
col_count = 0
headcount = -1
headings = []
rowNo = 0


# Environment Settings
arcpy.env.overwriteOutput = True

# Setup status output
scriptName = 'RegisterToXls.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Functions
def CreateFieldName(txtlist):
	"""Takes a list of strings and formats them as valid field names, returns a dictionary of keys=FIELD_NAME and values=string. Ordered list of field names included as key == "F_ORDER"."""
	fieldnames = [] # Create a list to maintain ordering of field names
	fdict = dict() # Create a dictionary to return
	swaplist = ("-", "_", "/", "\n") # List of characters, new line to be replaced with a space
	nums = [str(num) for num in range(10)] # Create a list of numbers 0-9 as text 
	removelist = ["(", ")", ".", "#", "*", "'"] 
	fnum = 1
	for val in txtlist:
		txt = str(val)
		newtxt = ""
		if txt == "":
			txt = "FIELD_{}".format(fnum)
			fnum += 1
		if txt[0] in nums:
			newtxt = "X"
		for char in txt:
			if char not in removelist:
				if char in swaplist:
					char = " "
				newtxt += char
		UP = newtxt.upper()
		fname = "_".join(UP.split())
		fieldnames.append(fname)
		fdict[fname] = txt
	fdict["F_ORDER"] = fieldnames
	return fdict
	
# Setup 
xl_workbook = xlrd.open_workbook(excel_path) # Open the workbook
sheetIndex = int(sheetNo)-1
xl_sheet = xl_workbook.sheet_by_index(sheetIndex)
# num_cols = xl_sheet.ncols   # Number of columns
headerIndexNo = int(headerRowNo)-1 # Convert user-input Excel row number to Python index number

if headerIndexNo == 0: # If field names in first row of excel sheet, process only that row.
	rowHa = xl_sheet.row(headerIndexNo) # Grab the row holding the field aliases
	raw_alias = [val.value for val in rowHa] # Create list of field aliases.
	for ra in raw_alias:
		if not ra is None: # If cell value is not null...
			headings.append(ra) # Write value to header list
		else:
			headings.append("") # If cell value is null, write an empty string to the header list
else: # If field names are not all in the first row, we need to search the primary row and each row above it to row 1 until we find text.
	head_row_list = [] # Create a list to hold the header rows.
	for hr in range(0,  int(headerRowNo)): # Iterate through rows in Excel from 1 down to and including main header row.
		
		head_row_list.append(xl_sheet.row(hr)) # Append each row to the list
		
	head_row_list.reverse() # Reverse list so that main header row is the first item in the list of rows
	for cell_obj in head_row_list[0]: # Iterate through values in main header row list
		val = cell_obj.value
		headcount += 1 # Increment heading count
		if not val in ("", None): # If cell value is not empty or null...
			headings.append(val) # Write value to header list
		else:
			val_list = [] # Create a list to hold values from the same column in rows above the primary row .
			for nextrowup in head_row_list[1:]: #  Iterate through the other rows...
				val = nextrowup[headcount].value # Grab the value from the respective column.
				if not val in  ("", None): # If cell value is not empty or null...
					val_list.append(val) # Write value to value list
			if len(val_list) == 0: # If no values are written to the list, they must have been all "" or None
				headings.append("") # Write an empty string to the header list
			else:
				headings.append(val_list[0]) # Grab the first value in the value list and add it to the header list

fname_alias_dict = CreateFieldName(headings) # Feed the finalised list of field names into the 'CreateFieldName' function to output a dictionary
field_order = fname_alias_dict["F_ORDER"] # Get the field name order list from the dictionary

for f in field_order: # Create field names in output table
	sheet.write(0, col_count, f)
	col_count += 1

for rowNum in range(int(headerRowNo), int(stop)):
	thisrow = []
	for col in range(0, len(field_order)): #
		cell_obj = xl_sheet.cell(rowNum, col)
		thisrow.append(cell_obj.value)
	row_list.append(thisrow)
	
for tup in row_list:
	rowNo += 1
	colNo = 0
	for t in tup:
		sheet.write(rowNo, colNo, t)
		colNo += 1

book.save(RegisterExcel)
os.startfile(RegisterExcel)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

