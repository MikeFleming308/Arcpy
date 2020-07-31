#C:\Users\Michael.Fleming\OneDrive - Aurecon Group\ArcMap\Scripts\RegisterToASCII_csv_table.py
#---------------------------------------------------------------------------
#
# RegisterToASCII_csv_table.py
# Mike Fleming 
# michael.fleming@aurecongroup.com
# Created: 10/07/2018
# Last updated 21/07/2019

""" Description: 
    Takes an spreadsheet with multiple header rows, merged cells, incompatible field names and symbols. 
    Formats an output, "Simplified_Register.csv" to be compatible with ArcGIS for import as a table. 
    
    Takes the path to an Excel register as the first parameter. 
    The worksheet number is the second parameter, the row number of the last row holding the field names is the third parameter and the row number of the last row to process is the fourth and final parameter.
    The output csv will open upon successful completion of the script.
    Output may contain field names such as "FIELD_1, FIELD_2" which have been created where the header had no text.
    Output may contain empty rows
    Output "Simplified_Register.csv" will be in the same directory as the input workbook
"""
#---------------------------------------------------------------------------


# Import modules
import arcpy, time, xlrd, os, collections, unicodedata, re, sys, csv
reload(sys)

# User-supplied parameters
excel_path = arcpy.GetParameterAsText(0)
sheetNo = arcpy.GetParameterAsText(1)
headerRowNo = arcpy.GetParameterAsText(2)
stop = arcpy.GetParameterAsText(3)

# Local variables
dir_path = os.path.split(excel_path)[0]
register = os.path.join(dir_path, "Simplified_Register.csv")
outfn = open(register, "wb")
csv_writer = csv.writer(outfn, dialect='excel', delimiter=',')
row_list = []
col_count = 0
headcount = -1
headings = []
rowNo = 0
symbols_to_remove = u'\x40\x60\x23\x24\x25\x26\x27\x2A\x5E\x7E' # Create a string holding unicode data points of symbols not allowed in field names
headerIndexNo = int(headerRowNo)-1 # Convert user-input Excel row number to Python index number

# Environment Settings
arcpy.env.overwriteOutput = True
sys.setdefaultencoding('utf8')

# Setup status output
scriptName = 'RegisterToASCII_csv_table.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Functions
def Chomper(txt, length=250, symbols=''):
    """Removes non-printing characters from given text. Takes a string, optional maximum length of output and an optional string of unicode data points defining symbols for removal """
    utxt = unicode(txt)
    control_chars_remove = ''.join(map(unichr, range(0,32))) + '\x7f' # Create a string holding Unicode control characters
    chars_remove = control_chars_remove + symbols # Combine the strings (unicode data points)
    escaped_chars = u"[{}]".format(re.escape(chars_remove)) # Escape the chars for loading into an re
    char_re = re.compile(escaped_chars) # Compile a regular expression pattern into a regular expression object
    normalised = unicodedata.normalize('NFKD', utxt).encode('ascii','ignore') # Normalise (replace all compatibility characters with their equivalents)
    chars_removed = char_re.sub('', normalised) # Remove Unicode control characters and unwanted symbols
    stripped = " ".join(chars_removed.split()) # Remove excess white space
    return stripped[:length]

def MakeFieldNamesUnique(alist):
    """ """
    dups = []
    txtlist = []
    for val in alist:
        if type(val) == type("text"):
            val.replace(unicode('%'), 'pc') # swap out '%' for 'pc'
        txtlist.append(val)
    blist = [Chomper(txt, 30, symbols_to_remove) for txt in txtlist] # Ensure the max length for the input field names is 30 characters and remove unwanted chars
    counter = collections.Counter(blist)
    counts = counter.most_common()
    for i in counts: # Populate the list of duplicated field names
        if not i[0] == "": # Check there is a value (field name) to work with in the count dictionary 
            if i[1] > 1: # If the count is greater than 1... 
                dups.append(i[0]) # append the field name to a list of duplicated names
    if len(dups) > 0: # If there are duplicated field names identified...
        index_dup_dict = dict() # create a dictionary to hold a list of index numbers for each of the duplicated field names
        index_no = -1 # create a variable to hold the index number
        for i in dups: 
            index_dup_dict[i] = [] # Populate dictionary with identified duplicate field names as keys and an empty list as value
        for i in blist: # For each value in the list of truncated field names...
            index_no += 1 # increment the index number by 1 
            if i in dups: # If the field name is identified as being in the list of duplicated names...
                index_dup_dict[i].append(index_no) # Populate the respective lists in the duplicates dictionary with the index nos of each occurrence of the duplicated field names
        for i in dups: # For each value in the list of duplicated field names...
            fcount = 1 # create a variable to hold the count number
            for j in index_dup_dict[i]: # For each index number in the list for the current duplicated field name...
                del blist[j] # remove the duplicated field name at the current index location
                newfname = "{}_{}".format(i, fcount) # Create the new field name by appending the count number to the duplicated name
                blist.insert(j, newfname) # Insert the new field name at current index location
                fcount += 1 # Increment the count
    return blist

def CreateFieldName(alist):
    """Takes a list of strings and formats them as valid field names, returns a dictionary of keys=FIELD_NAME and values=string. Ordered list of field names included as key == "F_ORDER"."""
    txtlist = MakeFieldNamesUnique(alist)
    fieldnames = [] # Create a list to maintain ordering of field names
    fdict = dict() # Create a dictionary to return
    swaplist = ("-", "_", "/", "\n") # List of characters, new line to be replaced with a space
    nums = [str(num) for num in range(10)] # Create a list of numbers 0-9 as text 
    removelist = ["(", ")", ".", "#", "*", "'", "%"] 
    fnum = 1
    for val in txtlist: # for each field name in the list
        txt = str(val) # coerce to string
        newtxt = "" # create empty text object
        if txt == "": # if no field name, create one using the fnum variable
            txt = "FIELD_{}".format(fnum)
            fnum += 1 # increment the fnum variable by 1
        if txt[0] in nums: # if the first character is numeric, add an "X"
            newtxt = "X" 
        for char in txt: # iterate through every character, do nothing if char in removelist, change char to single space if char in swaplist, add all other to newtxt
            if char not in removelist:
                if char in swaplist:
                    char = " "
                newtxt += char
        UP = newtxt.upper() # set to uppercase
        fname = "_".join(UP.split()) # remove multiple spaces, replace single spaces with underscores
        fieldnames.append(fname)
        fdict[fname] = txt
    fdict["F_ORDER"] = fieldnames
    return fdict
    
# Setup 
xl_workbook = xlrd.open_workbook(excel_path) # Open the workbook
sheetIndex = int(sheetNo)-1
xl_sheet = xl_workbook.sheet_by_index(sheetIndex)

if headerIndexNo == 0: # If field names in first row of excel sheet, process only that row.
    rowHa = xl_sheet.row(headerIndexNo) # Grab the row holding the field names
    raw_name = [val.value for val in rowHa] # Create list of field names.
    for ra in raw_name:
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

# If the header of the first column of your CSV is "ID", Excel will complain when opening the file.
if headings[0].lower() == 'id': # Check if first heading is 'ID', if so, remove it.
    _ = headings.pop(0)
    headings.insert(0, 'PRIMARY_ID') # replace with 'PRIMARY_ID'

fieldname_dict = CreateFieldName(headings) # Feed the finalised list of field names into the 'CreateFieldName' function to output a dictionary
field_order = fieldname_dict["F_ORDER"] # Get the field name order list from the dictionary

for rowNum in range(int(headerRowNo), int(stop)):
    thisrow = []
    for col in range(0, len(field_order)): #
        cell_obj = xl_sheet.cell(rowNum, col)
        if cell_obj.ctype == 1: # determine if value is a string
            cellval = cell_obj.value # set value to variable
            strip_space = " ".join(cellval.split())
            outval = Chomper(strip_space)
            thisrow.append(outval)
        else:
            thisrow.append(cell_obj.value)
    row_list.append(thisrow)

csv_writer.writerow(field_order)

for row in row_list: #
    csv_writer.writerow(row)
del row_list, csv_writer

os.startfile(register)


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

