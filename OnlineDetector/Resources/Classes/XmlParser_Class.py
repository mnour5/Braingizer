import os
import oct2py
from PyQt4 import QtCore, QtGui
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
import AppConfig

class XmlParser:
    def __init__(self):
        # Check if the file exists and if not, will create a new file
        if( not os.path.isfile(AppConfig.Profiles_File) ):
            self.createXmlFile(AppConfig.Profiles_File)
        if( not os.path.isfile(AppConfig.TrainingSessions_File) ):
            self.createXmlFile(AppConfig.TrainingSessions_File)
    
    def createXmlFile(self, path):
        if( os.path.isfile(path) ):
            os.rename(path, path + "_old")
        
        rt = ET.Element('List')
        tree = ET.ElementTree(rt)
        tree.write(path)
    
    def getElements(self, ElementName):
        #Select the XML file
        if(ElementName == "Profile"):
            XML_path = AppConfig.Profiles_File
        elif(ElementName == "TrainingSession"):
            XML_path = AppConfig.TrainingSessions_File
        else:
            return None
        
        # Get the data from the XML file
        tree = ET.parse(XML_path)
        root = tree.getroot()
        return root
    
    def addElement(self, NewElementName, NewElementData):
        #Select the XML file
        if(NewElementName == "Profile"):
            XML_path = AppConfig.Profiles_File
        elif(NewElementName == "TrainingSession"):
            XML_path = AppConfig.TrainingSessions_File
        else:
            return None
        
        # Get the data from the XML file
        tree = ET.parse(XML_path)
        root = tree.getroot()
        
        # Creating new-element
        NewElement = ET.SubElement(root, NewElementName)
        
        for Attribute in NewElementData:
            if(Attribute == "Description"):
                Discription         = ET.SubElement(NewElement, "Description")
                Discription.text    = str(NewElementData["Description"])
                
            elif(Attribute == "SubElement"):
                # Adding sub-elements
                for i, Attribute in enumerate( NewElementData["SubElement"] ):
                    SubElement = ET.SubElement(NewElement, Attribute)
                    
                    for i, SubAttribute in enumerate( NewElementData["SubElement"][Attribute] ):
                        SubElement.set(SubAttribute, str(NewElementData["SubElement"][Attribute][SubAttribute]))
                
            else:
                # Adding attributes
                NewElement.set(Attribute, str(NewElementData[Attribute]))
        
        # Saving the data to the XML file
        tree.write(XML_path)
        
        # Prettifing the XML file
        self.XmlPrettifier(XML_path)
    
    def XmlPrettifier(self, filename):
        with open(filename, "r+") as f:
            soup = BS(f, "xml")
            f.seek(0)
            f.write(soup.prettify())
            f.truncate()
    
    def elementExist(self, ElementName, Name):
        #Select the XML file
        if(ElementName == "Profile"):
            XML_path = AppConfig.Profiles_File
        elif(ElementName == "TrainingSession"):
            XML_path = AppConfig.TrainingSessions_File
        else:
            return None
        
        # Get the data from the XML file
        tree = ET.parse(XML_path)
        root = tree.getroot()
        
        for element in root.findall(ElementName):
            if element.attrib['Name'] == Name:
                return True
        
        return False