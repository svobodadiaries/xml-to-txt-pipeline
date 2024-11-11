# Author: Chelsea Lee
# The xml2txt converts TEI-XML files to TXT files
# It excludes certain structural tags in the TXT found in the XML
# To run this program, input your specific pathname for the XML and TXT file

import xml.etree.ElementTree as ET
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def xml_to_txt(xml_file, txt_file, words_to_remove):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Helper method to exclude specific words found in XML from TXT
        def remove_words(text, words_to_remove):
            for word in words_to_remove:
                text = text.replace(word, '')
            return text
        
        # Finds and stores margin notes with their page numbers
        def extract_margin_notes(element):
            margin_set = {}  # Dictionary to store notes with page numbers
            # Search for all <note> elements that have a 'place' attribute set to 'margin'
            place = [note for note in root.findall('.//tei:note[@place]', namespaces=ns) if 'place' in note.attrib]
            for note in place:
                place_attribute = note.attrib.get('place', '')
                if 'margin' in place_attribute:
                    page_number = note.attrib.get('place', '').split()[-1] if place_attribute else 'unknown'  # Extract page number from 'place' attribute
                    margin_text = note.text.strip() if note.text else ''
                
                print(f"Found margin note: {margin_text} on page {page_number}") #Checking margin search is correct
                
                if page_number not in margin_set:
                    margin_set[page_number] = []
                margin_set[page_number].append(margin_text)

            return margin_set

        # Open text file in write mode
        with open(txt_file, 'w') as file:
            # Recursively extract & clean text from XML tree
            def extract_text(element, margin_set):
                # If element has text, clean and write into TXT
                if element.text:
                    clean_text = remove_words(element.text, words_to_remove)
                    file.write(clean_text.strip() + '\n')
                
                # Finding margin notes
                    if element.tag == 'div' and 'type' in element.attrib and element.attrib['type'] == 'entry_notes':
                        # Check if there are any margin notes and write them
                        for page_number, notes in margin_set.items():
                            for note in notes:
                                file.write(f"[Page {page_number}] {note}\n")

                # Recursively extract text from children
                for child in element:
                    extract_text(child)

                # Handle element tail text if present
                if element.tail:
                    cleaned_tail = remove_words(element.tail, words_to_remove)
                    file.write(cleaned_tail.strip() + '\n')

            # Start extracting from the root element
            extract_text(root)
    
    except ET.ParseError:
        print("Error: Failed to parse XML file.")
    except IOError as e:
        print(f"Error: {e}")

# Set desired XML, TXT using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55TEST.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55TEST.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]'] # List of words to exclude in TXT

# Run XML to TXT function
xml_to_txt(xml_file, txt_file, words_to_remove)
