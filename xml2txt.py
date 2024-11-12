# Author: Chelsea Lee
# The xml2txt converts TEI-XML files to TXT files
# It excludes certain structural tags in the TXT found in the XML
# Removes margin text when it is emphasized in main page text
# Output: States all matched margin notes and its page number, confirms TXT file is generated
# To run this program, input your specific pathname for the XML and TXT file

import xml.etree.ElementTree as ET
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
tree = ET.parse('/Users/chelsea/SDP files/SDP/texts/diary55SHORT.xml')
root = tree.getroot()

def extract_margin_notes(element):
            margin_notes = {}  # Dictionary to store notes with page numbers
            # Look for all <note> elements that have a 'place' attribute set to 'margin'
            notes_with_place = [note for note in root.findall('.//tei:note[@place]', namespaces=ns) if 'place' in note.attrib]
            for note in notes_with_place:
                place_attribute = note.attrib.get('place', '')
                if 'margin' in place_attribute:
                    # Get page number (last part after 'page')
                    page_number = note.attrib.get('place', '').split()[-1] if place_attribute else 'unknown'  # Extract page number from 'place' attribute
                    note_text = note.text.strip() if note.text else ''
                # Store note with page number
                if page_number not in margin_notes:
                    margin_notes[page_number] = []
                margin_notes[page_number].append(note_text)

            # Return collected margin notes
            return margin_notes

# Helper method to store matched margin text and page numbers
def store_match(matched_set, page_number, margin_text):
    matched_set.add((page_number, margin_text))

margin_notes = extract_margin_notes(root)
matched_notes = set()  # Set to store matched notes

current_page_text = ""
current_page_number = None
recording_text = False

for elem in root.iter():
    # Check if element is a page break
    if elem.tag == '{http://www.tei-c.org/ns/1.0}pb' and 'n' in elem.attrib:
        # If there's an ongoing page, check for a match before moving to the next page
        if current_page_number and current_page_number in margin_notes:
            margin_text = ' '.join(margin_notes[current_page_number])
            if margin_text in current_page_text:
                store_match(matched_notes, current_page_number, margin_text)
        
        # Reset for new page
        current_page_number = elem.attrib['n']
        current_page_text = ""
        recording_text = False

    # Gather text for the current page (skip <pb> tags themselves)
    elif current_page_number and current_page_number in margin_notes:
        if elem.tag == '{http://www.tei-c.org/ns/1.0}lb' and 'n' in elem.attrib and elem.attrib['n'] == "1" and not recording_text:
            recording_text = True
    if recording_text and elem.tag != '{http://www.tei-c.org/ns/1.0}pb': 
        current_page_text += ''.join(elem.itertext()).strip() + " "

# Final check for the last page after exiting the loop
if current_page_number and current_page_number in margin_notes:
    margin_text = ' '.join(margin_notes[current_page_number])
    if margin_text in current_page_text:
        store_match(matched_notes, current_page_number, margin_text)

print("All matched margin notes and their page numbers:")
for page, note in matched_notes:
    print(f"Page {page}: {note}")

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
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]'] # List of words to exclude in TXT

# Run XML to TXT function
xml_to_txt(xml_file, txt_file, words_to_remove)
print("TXT file has been generated.")
