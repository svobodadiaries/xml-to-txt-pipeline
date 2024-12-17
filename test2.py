from collections import defaultdict
import xml.etree.ElementTree as ET
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
# Set desired XML, TXT using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]'] # List of words to exclude in TXT
tree = ET.parse(xml_file)
root = tree.getroot()

# Assuming margin_notes and matched_notes are already defined
# margin_notes: {date or (n_value): [note_text]}
# matched_notes: set of (date or (n_value), note_text)

from collections import defaultdict

def extract_margin_notes(root, ns):
    margin_notes = defaultdict(list)  # Default dict to store notes with keys as date or n value
    # Find all <note> elements with 'place' attribute set to 'margin'
    notes_with_place = [note for note in root.findall('.//tei:note[@place]', namespaces=ns) if 'place' in note.attrib]
    for note in notes_with_place:
        place_attribute = note.attrib.get('place', '')
        if 'margin' in place_attribute:
            print("REACHED")
            note_text = note.text.strip() if note.text else ''
    entry_divs = root.findall(".//tei:div[@type='entry']", namespaces=ns)
    for entry in entry_divs:
        entry_n = entry.attrib.get('n', '')
        print("N", entry_n)
    margin_notes[entry_n].append(note_text)
    return margin_notes

def store_match(matched_notes, key, margin_text):
    matched_notes.add((key, margin_text))

def process_text_for_matches(root, ns):
    margin_notes = extract_margin_notes(root, ns)
    matched_notes = set()  # Set to store matched notes
    current_page_text = ""  # Ongoing page text
    current_n = None

    for elem in root.iter():
        # Check for page breaks <pb> and if it's part of the current page text
        if elem.tag == '{http://www.tei-c.org/ns/1.0}pb' and 'n' in elem.attrib:
            # Check if there's a match with the margin notes for the current page
            if current_n and current_n in margin_notes:
                margin_text = ' '.join(margin_notes[current_n])
                print(f"Checking margin notes for n={current_n}: {margin_text}")
                if margin_text in current_page_text:
                    print(f"Match found for entry n={current_n}")
                    store_match(matched_notes, current_n, margin_text)
            
            # Reset for the new page
            current_page_text = ""

        # Check for <div type="entry">, where we process the page text and handle date/n value
        if elem.tag == '{http://www.tei-c.org/ns/1.0}div' and elem.attrib.get("type") == "entry":
            n_value = elem.attrib.get("n")  # Use 'n' value if no date is found
            current_n = n_value  # Use entry n for matching if no date is found
            
            # Process the page text within this entry
            entry_text = ''.join([t for t in elem.itertext() if t.strip()])  # Extract all text in the entry
            current_page_text += ' ' + entry_text  # Accumulate the page text
            # print(f"Accumulating text for entry {current_n_value}: {entry_text}")
            
    # After the loop, make sure to check for the last page before exiting
    if current_n and current_n in margin_notes:
        margin_text = ' '.join(margin_notes[current_n])
        if margin_text in current_page_text:
            store_match(matched_notes, current_n, margin_text)
    
    return matched_notes

# Example usage
# Assuming root is the parsed XML tree and ns is the namespace dictionary
matched_notes = process_text_for_matches(root, ns)

# Output matched notes
print("Matched Notes:", matched_notes)
