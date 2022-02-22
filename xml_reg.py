from xml_read import XML_READ
import xml.etree.ElementTree as ET

class XML_REG(XML_READ):
	def __init__(self, zip_folder, xml_tags):
		super().__init__(zip_folder, xml_tags)
	

	def parse_xml(self):
		mytree = ET.parse(self.zip_folder)
		myroot = mytree.getroot()
		'''
		an option of saving x,y vectors in two lists:
		time = []
		values = []
		for x in myroot.findall(self.xml_tags[0]):
			time.append(float(x.text))
		for y in myroot.findall(self.xml_tags[1]):
			values.append(float(y.text))
		'''
		# saving the time and values as keys and values of a dict, respectively
		# meaning, each time has its appropriate value
		for key in myroot.findall(self.xml_tags[0]):
			for val in myroot.findall(self.xml_tags[1]):
				self.results_dict[float(key.text)] = float(val.text)
		return self.results_dict



