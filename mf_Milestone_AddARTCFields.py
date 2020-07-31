
#
#---------------------------------------------------------------------------
#C:\Users\Michael.Fleming\OneDrive - Aurecon Group\ArcMap\Scripts\Milestone_AddARTCFields.py
# Milestone_AddARTCFields.py
# Mike Fleming michael.fleming@aurecongroup.com
# Created: 18/04/2019
# Last updated 24/04/2019
# Description: Adds ARTC Spec-2 fields to feature classes. Schema used is determined by feature class name prefix. 
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, os

# User-supplied parameters
gdb = arcpy.GetParameterAsText(0)

# Local variables
update_dict = {'ProjName': '270 North Star to Border', 'PROJ_ID': 'NS2B', 'MGA_Z': 56, 'ProjID': 'NS2B', 'MGA_Zone': 56, 'Project': '270 North Star to Border', 'ProjPhase': 2, 'ProjectPhase': 2, "PROJ_PHASE": 2, 'PROJ_NAME': '270 North Star to Border'}

udpdate_list = ["ProjID", "Project", "ProjName", "ProjPhase", "ProjectPhase", "PROJ_PHASE", "MGA_Z", "PROJ_ID", "PROJ_NAME", "MGA_Zone"]

design_fields_dict = {"ProjID": ("TEXT", 50), "ProjName": ("TEXT", 50), "ProjChainage": ("DOUBLE", ""), "ProjPhase": ("TEXT", 50), "SName": ("TEXT", 50), "S_ID": ("TEXT", 50), "CL": ("TEXT", 50), "LotPlan": ("TEXT", 50), "PropID": ("TEXT", 50), "MGA_Z": ("TEXT", 50), "East": ("DOUBLE", ""), "North": ("DOUBLE", ""), "Lat": ("DOUBLE", ""), "Long": ("DOUBLE", "")}

design_fields_list = ["ProjID", "ProjName", "ProjChainage", "ProjPhase", "SName", "S_ID", "CL", "LotPlan", "PropID", "MGA_Z", "East", "North", "Lat", "Long"]

environment_fields_dict = {"AssessmentGroup": ("TEXT", 50), "ResponsibleParty": ("TEXT", 50), "State": ("TEXT", 5), "MGA_Northing": ("DOUBLE", 8), "Latitude": ("DOUBLE", 8), "SiteArea_m2": ("DOUBLE", 8), "ShapeLength_m": ("DOUBLE", 8), "ActivityWithinHighRiskAreas": ("TEXT", 50), "UniqueIdentifier": ("TEXT", 50), "SiteName": ("TEXT", 50), "AttributeStyle": ("TEXT", 50), "LotPlan": ("TEXT", 50), "ProjectPhase": ("TEXT", 50), "LandClearanceStatus": ("TEXT", 50), "ActivityDate": ("DATE", 8), "MGA_Easting": ("DOUBLE", 8), "AssessmentReferences": ("TEXT", 250), "BufferRadius_m": ("DOUBLE", 8), "AssessmentSupervisor": ("TEXT", 250), "Notes": ("TEXT", 250), "Longitude": ("DOUBLE", 8), "Project": ("TEXT", 50), "PhotographicRecord": ("TEXT", 250), "Activity": ("TEXT", 50), "AttributeDescription": ("TEXT", 50), "KeyFindings": ("TEXT", 250), "Datasets_3rd_PartyUsed": ("TEXT", 250), "BusinessUnit": ("TEXT", 50), "SiteDescription": ("TEXT", 50), "MGA_Zone": ("TEXT", 10), "AssessmentType": ("SHORT", 2), "AssessmentNotes": ("TEXT", 250)}

environment_fields_list = ["UniqueIdentifier", "BusinessUnit", "Project", "ProjectPhase", "State", "LotPlan", "SiteName", "SiteDescription", "Activity", "ActivityDate", "ResponsibleParty", "KeyFindings", "LandClearanceStatus", "ActivityWithinHighRiskAreas", "AssessmentType", "AssessmentGroup", "AssessmentNotes", "AssessmentSupervisor", "AssessmentReferences", "Datasets_3rd_PartyUsed", "Notes", "AttributeStyle", "AttributeDescription", "PhotographicRecord", "MGA_Zone", "MGA_Easting", "MGA_Northing", "Latitude", "Longitude", "BufferRadius_m", "ShapeLength_m", "SiteArea_m2"]

tunnel_fields_dict = {"ProjName": ("TEXT", 50), "TunneltHeight_m": ("DOUBLE", 8), "TunnelType": ("TEXT", 50), "TunnelName": ("TEXT", 50), "TunnelWidth_m": ("DOUBLE", 8), "ProjID": ("TEXT", 50), "Elem": ("TEXT", 50), "Long": ("DOUBLE", 8), "TunnelLength_m": ("DOUBLE", 8), "ProjType": ("TEXT", 50), "TunnelN0": ("TEXT", 50), "Lat": ("DOUBLE", 8), "North": ("DOUBLE", 8), "East": ("DOUBLE", 8), "ProjChainage": ("DOUBLE", 8)}

tunnel_fields_list = ["ProjID", "ProjName", "ProjChainage", "ProjType", "TunnelN0", "TunnelName", "TunnelType", "TunnelLength_m", "TunnelWidth_m", "TunneltHeight_m", "East", "North", "Lat", "Long", "Elem"]

level_xing_a_fields_dict = {"ProjName": ("TEXT", 50), "RdName": ("TEXT", 50), "LX_Type": ("TEXT", 50), "Alkam_km": ("DOUBLE", 8), "AlcamID": ("LONG", 4), "PropTr": ("TEXT", 50), "ProjID": ("TEXT", 50), "Elem": ("TEXT", 50), "Long": ("DOUBLE", 8), "ProjType": ("TEXT", 50), "RdMgr": ("TEXT", 50), "North": ("DOUBLE", 8), "Lat": ("DOUBLE", 8), "RdType": ("TEXT", 50), "DsgnVeh": ("TEXT", 50), "East": ("DOUBLE", 8), "Tsr": ("TEXT", 5), "RailMgr": ("TEXT", 50), "LX": ("TEXT", 50)}

level_xing_a_fields_list = ["ProjID", "ProjName", "Alkam_km", "ProjType", "AlcamID", "RdName", "RdType", "LX", "LX_Type", "Tsr", "RdMgr", "RailMgr", "DsgnVeh", "PropTr", "East", "North", "Lat", "Long", "Elem"]

level_xing_b_fields_dict = {"ProjName": ("TEXT", 50), "RdName": ("TEXT", 50), "LX_Type": ("TEXT", 50), "Alkam_km": ("DOUBLE", 8), "AlcamID": ("LONG", 4), "PropTr": ("TEXT", 50), "ProjID": ("TEXT", 50), "Elem": ("TEXT", 50), "Long": ("DOUBLE", 8), "ProjType": ("TEXT", 50), "RdMgr": ("TEXT", 50), "North": ("DOUBLE", 8), "Lat": ("DOUBLE", 8), "RdType": ("TEXT", 50), "DsgnVeh": ("TEXT", 50), "East": ("DOUBLE", 8), "Tsr": ("TEXT", 5), "RailMgr": ("TEXT", 50), "Interface": ("TEXT", 50)}

level_xing_b_fields_list = ["ProjID", "ProjName", "Alkam_km", "ProjType", "AlcamID", "RdName", "RdType", "Interface", "LX_Type", "Tsr", "RdMgr", "RailMgr", "DsgnVeh", "PropTr", "East", "North", "Lat", "Long", "Elem"]

bridge_fields_dict = {"BrdgHeight_m": ("DOUBLE", 8), "SpanType": ("TEXT", 50), "East": ("DOUBLE", 8), "BrdgN0": ("TEXT", 50), "ProjName": ("TEXT", 50), "North": ("DOUBLE", 8), "SpanMaterial": ("TEXT", 50), "BrdgName": ("TEXT", 50), "BrdgLength_m": ("DOUBLE", 8), "Lat": ("DOUBLE", 8), "BrdgWidth_m": ("DOUBLE", 8), "BrdgType": ("TEXT", 50), "RLm": ("DOUBLE", 8), "SpanLength_m": ("DOUBLE", 8), "StructureRetention": ("TEXT", 50), "Elem": ("TEXT", 50), "ProjType": ("TEXT", 50), "Long": ("DOUBLE", 8), "SpanN0": ("DOUBLE", 8), "ProjChainage": ("DOUBLE", 8), "ProjID": ("TEXT", 50)}

bridge_fields_list = ["ProjID", "ProjName", "ProjChainage", "ProjType", "BrdgN0", "BrdgName", "BrdgType", "BrdgLength_m", "BrdgWidth_m", "BrdgHeight_m", "SpanMaterial", "SpanType", "SpanN0", "SpanLength_m", "RLm", "StructureRetention", "East", "North", "Lat", "Long", "Elem"]

culvert_fields_dict = {"ClvrtWidth_m": ("DOUBLE", 8), "Long": ("DOUBLE", 8), "SpanType": ("TEXT", 50), "SkewAngle": ("DOUBLE", 8), "East": ("DOUBLE", 8), "ProjName": ("TEXT", 50), "North": ("DOUBLE", 8), "ClvrtType": ("TEXT", 50), "SpanLength_m": ("DOUBLE", 8), "Lat": ("DOUBLE", 8), "RLm": ("DOUBLE", 8), "ClvrtName": ("TEXT", 50), "ClvrtMaterial": ("TEXT", 50), "ClvrtLength_m": ("DOUBLE", 8), "BatterSlope": ("DOUBLE", 8), "StructureRetention": ("TEXT", 50), "Elem": ("TEXT", 50), "ClvrtN0": ("TEXT", 50), "ProjType": ("TEXT", 50), "SpanN0": ("DOUBLE", 8), "ProjChainage": ("DOUBLE", 8), "ClvrtHeight_m": ("DOUBLE", 8), "ProjID": ("TEXT", 50)}

culvert_fields_list = ["ProjID", "ProjName", "ProjChainage", "ProjType", "ClvrtN0", "ClvrtName", "ClvrtType", "ClvrtLength_m", "ClvrtWidth_m", "ClvrtHeight_m", "ClvrtMaterial", "SkewAngle", "BatterSlope", "SpanType", "SpanN0", "SpanLength_m", "RLm", "StructureRetention", "East", "North", "Lat", "Long", "Elem"]

geo_fields_dict = {"HOLE_LOCX": ("DOUBLE", 8), "HOLE_LOCY": ("DOUBLE", 8), "PROJ_ID": ("TEXT", 50), "FILE_FSET": ("TEXT", 255), "PROJ_ENG": ("TEXT", 50), "I_CNGE": ("DOUBLE", 8), "T_TYPE": ("TEXT", 50), "S_ID": ("TEXT", 50), "S_NAME": ("TEXT", 50), "ROAD": ("TEXT", 255), "PROJ_NAME": ("TEXT", 50), "METHOD": ("TEXT", 255), "DEPTH": ("DOUBLE", 8)}

geo_fields_list = ["PROJ_ID", "PROJ_NAME", "PROJ_ENG", "FILE_FSET", "I_CNGE", "S_NAME", "S_ID", "T_TYPE", "METHOD", "HOLE_LOCX", "HOLE_LOCY", "DEPTH", "ROAD"]

geo_prop_fields_dict = {"HOLE_LOCX": ("DOUBLE", 8), "PROJ_PHASE": ("SmallInteger", 2), "PROJ_ID": ("TEXT", 50), "FILE_FSET": ("TEXT", 50), "HOLE_FDEP": ("DOUBLE", 8), "PROJ_ENG": ("TEXT", 50), "HOLE_CLST": ("TEXT", 50), "HOLE_CNGE": ("DOUBLE", 8), "SURVEY_METHOD": ("TEXT", 50), "HOLE_OFFS": ("DOUBLE", 8), "HOLE_ID": ("TEXT", 50), "HOLE_GL": ("DOUBLE", 8), "HOLE_TYPE": ("TEXT", 5), "HOLE_LOCY": ("DOUBLE", 8), "HOLE_LOCM": ("DOUBLE", 8), "HOLE_REF": ("TEXT", 50), "PROJ_NAME": ("TEXT", 50)}

geo_prop_fields_list = ["PROJ_ID", "PROJ_NAME", "PROJ_PHASE", "PROJ_ENG", "FILE_FSET", "HOLE_CLST", "HOLE_ID", "HOLE_TYPE", "HOLE_GL", "HOLE_FDEP", "HOLE_LOCX", "HOLE_LOCY", "HOLE_CNGE", "HOLE_OFFS", "HOLE_LOCM", "HOLE_REF", "SURVEY_METHOD"]

util_fields_dict = {"Structure_name": ("TEXT", 50), "Svy_type": ("TEXT", 50), "Point_No": ("TEXT", 50), "Comments": ("TEXT", 50), "Quality_level": ("TEXT", 50), "East": ("TEXT", 50), "Rel_V_Pos_m": ("Single", 4), "Status": ("TEXT", 50), "IR_WBS_No": ("SmallInteger", 2), "Data_Source": ("TEXT", 50), "North": ("TEXT", 50), "Rail_Code": ("TEXT", 50), "Material": ("TEXT", 50), "Agreement": ("TEXT", 50), "NSW_Code": ("TEXT", 50), "Excav_type": ("TEXT", 50), "Svy_origin": ("TEXT", 50), "Rel_H_Pos_m": ("Single", 4), "V_Pos_ToR": ("Single", 4), "Configuration": ("TEXT", 50), "Diameter_cell": ("TEXT", 50), "Diameter_type": ("TEXT", 50), "Utility_Type": ("TEXT", 50), "Consultant": ("TEXT", 50), "Date_Survey": ("SmallInteger", 2), "VIC_Code": ("TEXT", 50), "String_No": ("TEXT", 50), "Rel_H_Pos_txt": ("TEXT", 50), "Datum": ("TEXT", 50), "Rel_V_Pos_txt": ("TEXT", 50), "AS5488_Code": ("TEXT", 50), "Height": ("TEXT", 50), "IR_WBS_Name": ("TEXT", 50), "Owner": ("TEXT", 50), "QLD_Code": ("TEXT", 50)}

util_fields_list = ["IR_WBS_No", "IR_WBS_Name", "Structure_name", "VIC_Code", "NSW_Code", "QLD_Code", "Rail_Code", "AS5488_Code", "String_No", "Point_No", "Utility_Type", "East", "North", "Height", "Datum", "Quality_level", "Date_Survey", "Data_Source", "Diameter_cell", "Diameter_type", "Svy_origin", "Svy_type", "Rel_H_Pos_m", "Rel_H_Pos_txt", "Rel_V_Pos_m", "Rel_V_Pos_txt", "V_Pos_ToR", "Owner", "Status", "Material", "Configuration", "Excav_type", "Comments", "Consultant", "Agreement"]

util_impact_fields_dict = {"IR_WBS_No": ("SHORT", 8), "IR_WBS_Name": ("TEXT", 50), "UTL_ID": ("TEXT", 50), "UTL_Owner": ("TEXT", 50), "UTL_Type": ("TEXT", 50), "UTL_Treatment": ("TEXT", 50), "UTL_New": ("TEXT", 50), "UTL_Length": ("DOUBLE", 8), "UTL_PermanentProtect": ("TEXT", 50), "UTL_PermanentProtect_Length": ("DOUBLE", 8), "UTL_Abandoned_Length": ("DOUBLE", 8), "East": ("DOUBLE", 8), "North": ("DOUBLE", 8), "Height": ("DOUBLE", 8), "Datum": ("DOUBLE", 8), "UTL_RegisterN0": ("TEXT", 50), "UTL_ClashDetection_ID": ("TEXT", 50), "UTL_Chainage": ("TEXT", 50), "UTL_VerticalPosition": ("TEXT", 50), "UTL_HorizontalOrientation": ("TEXT", 50), "UTL_RiskRating": ("TEXT", 50), "UTLQualityLevel": ("TEXT", 50)}

util_impact_fields_list = ["IR_WBS_No", "IR_WBS_Name", "UTL_ID", "UTL_Owner", "UTL_Type", "UTL_Treatment", "UTL_New", "UTL_Length", "UTL_PermanentProtect", "UTL_PermanentProtect_Length", "UTL_Abandoned_Length", "East", "North", "Height", "Datum", "UTL_RegisterN0", "UTL_ClashDetection_ID", "UTL_Chainage", "UTL_VerticalPosition", "UTL_HorizontalOrientation", "UTL_RiskRating", "UTLQualityLevel"]


# Setup status output
scriptName = 'Milestone_AddARTCFields.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
arcpy.env.workspace = gdb
fcs = arcpy.ListFeatureClasses()


# Main
for fc in fcs:
    fcpath = os.path.join(gdb, fc)
    msg = "\n\tListing fields in {}".format(fc)
    arcpy.AddMessage(msg)
    fcfields = arcpy.ListFields(fc)
    fnameList = [f.name.lower() for f in fcfields]
    if fc[:5] in ["TRAN_", "STRU_", "BOUND"]:
        if fc.startswith("STRU_Bridge"):
            fld_list, fld_dict = bridge_fields_list, bridge_fields_dict
        elif fc.startswith("STRU_Level"):
            fld_list, fld_dict = level_xing_a_fields_list, level_xing_a_fields_dict
        elif fc.startswith("STRU_Tunnel"):
            fld_list, fld_dict = tunnel_fields_list, tunnel_fields_dict
        elif fc.startswith("STRU_Culvert"):
            fld_list, fld_dict = culvert_fields_list, culvert_fields_dict
        else:
            fld_list, fld_dict = design_fields_list, design_fields_dict
        
    elif fc[:4] == "GEO_":
        if fc.startswith("GEO_ProposedExpl"):
            fld_list, fld_dict = geo_prop_fields_list, geo_prop_fields_dict
        else:
           fld_list, fld_dict = geo_fields_list, geo_fields_dict
    elif fc[:5] == "UTIL_":
        if fc.startswith("UTIL_Impact"):
            fld_list, fld_dict = util_impact_fields_list, util_impact_fields_dict
        else:
           fld_list, fld_dict = util_fields_list, util_fields_dict
    elif fc[:4] in ["ENV_", "BIOT", "HYDR", "Env_", "FARM", "GEOS", "HEAL", "PLAN"]:
           fld_list, fld_dict = environment_fields_list, environment_fields_dict
    else:
        fld_list, fld_dict = design_fields_list, design_fields_dict
    for fname in fld_list:
        if fname.lower() not in fnameList:
            arcpy.AddField_management(fcpath, fname, fld_dict[fname][0], "", "", fld_dict[fname][1])
            msg = "Adding field: {}".format(fname)
            arcpy.AddMessage(msg)
    fnameList = [f.name for f in fcfields]
    for fname in fnameList:
        if fname in udpdate_list:
            with arcpy.da.UpdateCursor(fcpath, fname) as cur:
                for row in cur:
                    row[0] = update_dict[fname]
                    cur.updateRow(row)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

