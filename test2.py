import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('/Users/chelsea/SDP files/SDP/texts/diary55TEST.xml')
root = tree.getroot()
namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}
# Step 1: Extract margin notes with their page numbers
def extract_margin_notes(element):
            margin_notes = {}  # Dictionary to store notes with page numbers
            # Look for all <note> elements that have a 'place' attribute set to 'margin'
            notes_with_place = [note for note in root.findall('.//tei:note[@place]', namespaces=namespace) if 'place' in note.attrib]
            # print("noteswithplace", notes_with_place)
            for note in notes_with_place:
                place_attribute = note.attrib.get('place', '')
                if 'margin' in place_attribute:
                    page_number = note.attrib.get('place', '').split()[-1] if place_attribute else 'unknown'  # Extract page number from 'place' attribute
                    note_text = note.text.strip() if note.text else ''
                
                # Debug print to see if we are extracting margin notes correctly
                # print(f"Found margin note: {note_text} on page {page_number}")
                
                if page_number not in margin_notes:
                    margin_notes[page_number] = []
                margin_notes[page_number].append(note_text)

            return margin_notes
margin_notes = extract_margin_notes(root)
# print("Extracted margin notes:")
# for page, notes in margin_notes.items():
#             print(f"Page {page}: {notes}")

current_page_text = ""
current_page_number = None

for elem in root.iter():
    # Check if the element is a page break
    # print(elem.tag)
    if elem.tag == '{http://www.tei-c.org/ns/1.0}pb' and 'n' in elem.attrib:
        # If there's an ongoing page, check for a match before moving to the next page
        if current_page_number and current_page_number in margin_notes:
            print("check", current_page_number, current_page_number in margin_notes)
            margin_text = ' '.join(margin_notes[current_page_number])
            print("margintext", margin_text)
            print("currtext", current_page_text)
            # if isinstance(margin_text, list):
            #     print("currtext", current_page_text)
            #     match_found = any(text in current_page_text for text in margin_text)
            # else:
            #     match_found = margin_text in current_page_text
            # print("matchfound", match_found)
            # if match_found:
            #     print(f"Match found on page {current_page_number}:\nMargin Note: {margin_text}")
            # else:
            #     print(f"No match for margin note on page {current_page_number}.")
            if margin_text in current_page_text:
                print(f"Match found on page {current_page_number}:\nMargin Note: {margin_text}")
            else:
                print(f"No match for margin note on page {current_page_number}.")
        
        # Reset for the new page
        current_page_number = elem.attrib['n']
        current_page_text = ""  # Reset the text for the new page
    
    # Accumulate text for the current page (skip <pb> tags themselves)
    elif elem.text:
        current_page_text += elem.text.strip() + " "

# Final check for the last page after exiting the loop
if current_page_number and current_page_number in margin_notes:
    margin_text = margin_notes[current_page_number]
    if margin_text in current_page_text:
        print(f"Match found on page {current_page_number}:\nMargin Note: {margin_text}")
    else:
        print(f"No match for margin note on page {current_page_number}.")