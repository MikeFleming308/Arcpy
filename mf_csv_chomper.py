#
#---------------------------------------------------------------------------
#
# Chomper.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 26/02/2018
# Last updated 26/02/2018
# Description: Reads an input .csv, filters text to remove any characters that 
#              might cause grief in FME, writes filtered text to a new .csv
#              The filter removes all non ASCII characters, then removes the
#              non-printing ASCII controls and specific symbols ( @ ` # $ % & ' * ^ ~)
#              Also truncates text to 250 characters per field
#
# teststr = "Klüft @ # $ % ^ & * ~  \t\t skräms  inför \npå fédéral éle`ctor'al große"
# u_teststr = u"Klüft @ # $ % ^ & * ~  \t\t skräms inför \npå fédéral éle`ctor'al große"
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, unicodedata, re, sys, csv
reload(sys)

# encoding=utf8  
sys.setdefaultencoding('utf8')

# User-supplied parameters
in_csv_file = arcpy.GetParameterAsText(0)
out_csv_file = arcpy.GetParameterAsText(1)

# Local variables
# control_chars = ''.join(map(unichr, range(0,32)))
# delete = '\x7f'
# control_chars = control_chars + delete
# control_char_re = re.compile('[%s]' % re.escape(control_chars))
# symbol_chars = u'\x40\x60\x23\x24\x25\x26\x27\x2A\x5E\x7E'
# symbol_chars_re = re.compile('[%s]' % re.escape(symbol_chars))
rows = []
 
# Functions
def Chomper(txt):
    utxt = unicode(txt)
    control_chars_remove = ''.join(map(unichr, range(0,32))) + '\x7f'
    text_symbol_remove = u'\x40\x60\x23\x24\x25\x26\x27\x2A\x5E\x7E'
    chars_remove = control_chars_remove + text_symbol_remove
    escaped_chars = u"[{}]".format(re.escape(chars_remove))
    char_re = re.compile(escaped_chars)
    normalised = unicodedata.normalize('NFKD', utxt).encode('ascii','ignore')
    chars_removed = char_re.sub('', normalised)
    stripped = " ".join(chars_removed.split())
    return stripped

# Setup status output
scriptName = 'Chomper.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Main            
with open(in_csv_file, 'rb') as in_csv:
    csv_reader = csv.reader(in_csv)
    for row in csv_reader:
        newrow = []
        for cell in row:
            newrow.append(Chomper(cell[:250]))
        rows.append(newrow)

with open(out_csv_file, 'wb') as out_csv:
    writer = csv.writer(out_csv)
    writer.writerows(rows)



# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

