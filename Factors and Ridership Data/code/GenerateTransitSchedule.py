import gzip
import jsonlines
import pandas as pd
import numpy as np
import json
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
from pprint import pprint
import os.path


def GenerateTransitFiles(file_name, file_path):
    # get the transitStop data into a dictionary
    network_file = 'output_transitSchedule.xml.gz'
    stop_attrib = {}
    minimalTransferTimes = {}
    # for transit stops details
    transitrouteStops = {}
    routeId = []
    # for transit links paths
    transitrouteLinks = {}
    routes = []
    routedetails = {}
    count = 0
    routeMode = {}
    with gzip.open(network_file, 'rb') as f:
        file_content = f.read()
        root = ET.fromstring(file_content)
        for child in root.iter("transitSchedule"):
            for subchild in child.iter("stopFacility"):
                stop_attrib.update({count: subchild.attrib})
                count += 1
        count = 0
        for child in root.iter("minimalTransferTimes"):
            for subchild in child.iter("relation"):
                minimalTransferTimes.update({count: subchild.attrib})
                count += 1
        for child in root.iter("transitRoute"):
            count = 0
            routeStopProfile = {}
            if child.get("id") not in routeId:
                route_id = child.get("id")
                routeId.append(child.get("id"))
                for subchild in child.iter("stop"):
                    routeStopProfile.update({count: subchild.attrib})
                    count += 1
                #             print(route_id)
                #             print(routeStopProfile)
                #             print("\n")
                transitrouteStops.update({route_id: routeStopProfile})
        for child in root.iter("transitRoute"):
            count = 0
            routelinkProfile = {}
            if child.get("id") not in routes:
                route_id = child.get("id")
                routeId.append(child.get("id"))
                for subchild in child.iter("link"):
                    routelinkProfile.update({count: subchild.attrib})
                    count += 1
                #             print(route_id)
                #             print(routelinkProfile)
                #             print("\n")
                transitrouteLinks.update({route_id: routelinkProfile})
                for subchild in child.iter("transportMode"):
                    routeMode[route_id] = subchild.text

    # from xml.etree.ElementTree import Element, SubElement, Comment
    inumber = 0
    vehicle_number = "veh_" + str(inumber) + "_bus"
    veh_list = []
    vehicle_mode = {}
    root = ET.Element("transitSchedule")
    # get transitStops subtree inserted into transitSchedule root tree
    transitStops = ET.SubElement(root, "transitStops")
    for key, value in stop_attrib.items():
        stopFacility = ET.SubElement(transitStops, "stopFacility")
        stopFacility.attrib = value
    # get minimalTransferTimes subtree inserted into transitSchedule root tree
    minimalTransfTimes = ET.SubElement(root, "minimalTransferTimes")
    for key, value in minimalTransferTimes.items():
        minTransfTime = ET.SubElement(minimalTransfTimes, "relation")
        minTransfTime.attrib = value
    # create subelements of the root XML file
    for key, value in transitrouteLinks.items():
        #     print(key)
        # create transitLine tree
        transitLine = ET.SubElement(root, "transitLine")
        transitLine.set("id", key)
        # create transitLine --> transitRoute subTree
        transitRoute = ET.SubElement(transitLine, "transitRoute")
        transitRoute.set("id", key)
        # create transitLine --> transitRoute --> transitMode subTree
        transitMode = ET.SubElement(transitRoute, "transportMode")
        #     transitMode.text="bus"
        transitMode.text = routeMode.get(key)
        # create transitLine --> transitRoute --> routeProfile subTree
        route = ET.SubElement(transitRoute, "routeProfile")
        routeKey = key
        dict_routeProfile = transitrouteStops[routeKey]
        for k, v in dict_routeProfile.items():
            stop = ET.SubElement(route, "stop")
            stop.attrib = v
        # create transitLine --> transitRoute --> route subTree
        route = ET.SubElement(transitRoute, "route")
        for k, v in value.items():
            link = ET.SubElement(route, "link")
            link.attrib = v
        # create transitLine --> transitRoute --> route subTree
        departures = ET.SubElement(transitRoute, "departures")
        routeKey = key
        # get the dataframe loaded
        excel_file = "Atlanta_toolkit_v0.5_c-7.0_b_-4.0_r5.0.xlsx"
        work_sheet = "depTime_lowinc_after"
        df = pd.read_excel(excel_file, sheet_name=work_sheet, index_col=0, header=3)
        df = df.fillna(0)
        df[routeKey]
        for row in df[routeKey]:
            if row != 0:
                departure = ET.SubElement(departures, "departure")
                ids = routeKey + "_" + str(row)
                departureTimes = str(row)
                if transitMode == "bus":
                    vehicle_number = "veh_" + str(inumber) + "_bus"
                else:
                    vehicle_number = "veh_" + str(inumber) + "_rail"
                vehicleRefIds = vehicle_number
                v = {"id": ids, "departureTime": departureTimes, "vehicleRefId": vehicleRefIds}
                inumber += 1
                departure.attrib = v
                veh_list.append(vehicle_number)
                vehicle_mode[vehicle_number] = transitMode

    # now create matsim_transitVehicles.xml
    # register the namespace for XML
    ET.register_namespace('', "http://www.matsim.org/files/dtd")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    veh_tree = ET.parse('template.xml')
    veh_root = veh_tree.getroot()
    # tree.write("output.xml")
    for i in veh_list:
        # get transitStops subtree inserted into transitSchedule root tree
        vehicle = ET.SubElement(veh_root, "vehicle")
        veh_id = i
        type_id = vehicle_mode.get(veh_id)
        vehicle.set("id", veh_id)
        vehicle.set("type", type_id)

    # veh_tree.write('transitVehicles.xml')

    from xml.etree import ElementTree
    from xml.dom import minidom

    # save as transitSchedules.xml
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t", newl="\n")
    with open("matsim_transitSchedule_s1.xml", "w") as f:
        f.write(xmlstr)
    # save as transitVehicles.xml
    xmlstr = minidom.parseString(ET.tostring(veh_root)).toprettyxml(indent="\t", newl="\n")
    with open("matsim_transitVehicles_s1.xml", "w") as f:
        f.write(xmlstr)

    # tree.write("filename.xml")


def main():
    file_path = 'Model Estimation/Est11'
    file_name = 'FAC-11-19.csv'
    GenerateTransitFiles(file_name, file_path)


if __name__ == "__main__":
    main()
