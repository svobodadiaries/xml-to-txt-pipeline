import xml.etree.ElementTree as ET

def xml_to_txt(xml_file, txt_file, indent_level):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the text file in write mode
    with open(txt_file, 'w') as file:
        initial_spacing = 6
        file.write('\n' * initial_spacing)
        # Recursively extract text from the XML tree
        def extract_text(element, current_indent=indent_level):
            indent = ' ' * current_indent
            # For specific elements, write the corresponding text
            if element.tag in ['title', 'p', 'name', 'date', 'head']:
                if element.text:
                    file.write(indent + element.text.strip() + '\n')
            if element.tag in ['author']:
                if element.text:
                    spacing(current_indent, spacing_level = 1)
                    file.write(indent + element.text.strip() + '\n')
            if element.tag in ['resp']:
                if element.text:
                    file.write(indent + '\n' * 2 + indent + element.text.strip() + '\n')
            # Recursively extract text from children
            for child in element:
                extract_text(child)

            # Handle element tail text if present
            if element.tail:
                file.write(indent + element.tail.strip() + '\n')
    
    def spacing(current_indent=indent_level, spacing_level):
        indent = ' ' * current_indent
        for x in spacing:

            file.write(indent + '\n')

        # Start extracting from the root element
        extract_text(root)
# Usage example
xml_file = '/Users/chelsea/SDP files/SDP/texts/d47pt1.xml' #may need to copy pathname
txt_file = '/Users/chelsea/SDP files/SDP/texts/d47pt1me.txt'
xml_to_txt(xml_file, txt_file, indent_level=10)