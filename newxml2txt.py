import xml.etree.ElementTree as ET

# Helper method to format text with specified indentation and spacing
def format_text(indent_level, spacing_level, text):
    indent = ' ' * indent_level
    spacing = '\n' * spacing_level
    return f"{spacing}{indent}{text.strip()}"

def xml_to_txt(xml_file, txt_file, initial_indent_level, initial_spacing_level):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the text file in write mode
    with open(txt_file, 'w') as file:
        # initial indentation and spacing (at start of file)
        file.write(format_text(initial_indent_level, initial_spacing_level, ''))
        # Recursively extract text from XML tree
        def extract_text(element, indent_level=10, spacing_level=1):
            if element.text:
                 file.write(element.text.strip() + '\n')
            
            # For specific elements, write the corresponding text
            # if element.tag in ['title', 'list', 'revisionDesc', 'div']:
            #     if element.text:
            #         formatted_text = format_text(indent_level, spacing_level, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['p', 'head']:
            #     if element.text:
            #         formatted_text = format_text(indent_level+2, spacing_level, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['author', 'date']:
            #     if element.text:
            #         formatted_text = format_text(indent_level, 2, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['name']:
            #     if element.text:
            #         formatted_text = format_text(indent_level+2, 2, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['resp']:
            #     if element.text:
            #         formatted_text = format_text(indent_level+2, 3, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['distributor', 'idno', 'bibl', 'projectDesc']:
            #     if element.text:
            #         formatted_text = format_text(indent_level, 3, element.text)
            #         file.write(formatted_text)
            # if element.tag in ['availability']:
            #     if element.text:
            #         formatted_text = format_text(indent_level+2, 2, element.text)
            #         file.write(formatted_text)

            # Recursively extract text from children
            for child in element:
                    extract_text(child)

            # Handle element tail text if present
            if element.tail:
                file.write(element.tail.strip()+ '\n')
        # Start extracting from the root element
        extract_text(root)

#Set desired xml,txt using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55fix?.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55.txt'
xml_to_txt(xml_file, txt_file, initial_indent_level=10, initial_spacing_level=4)