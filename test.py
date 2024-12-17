
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement, ElementTree, tostring
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
# Set desired XML, TXT using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55SHORT.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]'] # List of words to exclude in TXT
tree = ET.parse(xml_file)
root = tree.getroot()

def extract_margin_notes(root, ns):
    margin_notes = {}
    current_n = None  # To track the current entry's n value

    # Iterate through all elements in the XML
    for elem in root.iter():
        # Identify <div> elements with type="entry"
        if elem.tag == '{http://www.tei-c.org/ns/1.0}div' and elem.attrib.get("type") == "entry":
            # Get the entry's n attribute
            current_n = elem.attrib.get("n")
        
        # Identify <note> elements with margin notes
        elif elem.tag == '{http://www.tei-c.org/ns/1.0}note' and current_n:
            # Ensure the note has a "place" attribute (indicating margin notes)
            if 'place' in elem.attrib and 'margin' in elem.attrib['place']:
                note_text = ''.join(elem.itertext()).strip()  # Extract the note's text
                if current_n:  # Only add the note if there is a valid entry n
                    margin_notes[current_n] = note_text

    return margin_notes

def store_match(matched_notes, key, margin_text):
    matched_notes.add((key, margin_text))
def store_unmatched(unmatched_notes, key, margin_text):
    unmatched_notes.add((key, margin_text))

def find_matches(root, ns):
    margin_notes = extract_margin_notes(root, ns)
    matched_notes = set()
    processed_entries = set()
    unmatched_notes = set()
    current_page_text = ""
    current_n = None

    for elem in root.iter():
    # Check for page breaks <pb> and process current page text
        if elem.tag == '{http://www.tei-c.org/ns/1.0}pb' and 'n' in elem.attrib:
        # Check if there's a match with the margin notes for the current page
            if current_n and current_n in margin_notes:
                margin_text = ''.join(margin_notes[current_n])
                if margin_text in current_page_text:
                    print(f"Match found for entry n={current_n}")
                    store_match(matched_notes, current_n, margin_text)
                    processed_entries.add(current_n)
  
            # Reset for new page
            current_page_text = ""

        if elem.tag == '{http://www.tei-c.org/ns/1.0}div' and elem.attrib.get("type") == "entry":
            current_n = elem.attrib.get("n")
        # Process the page text within this entry
            entry_text = ''.join([t for t in elem.itertext() if t.strip()])  # Extract all text in the entry
            current_page_text += ' ' + entry_text  # Accumulate the page text

    # After the loop, make sure to check for the last page before exiting
    if current_n and current_n in margin_notes:
        margin_text = ' '.join(margin_notes[current_n])
        if margin_text in current_page_text:
            store_match(matched_notes, current_n, margin_text)
            processed_entries.add(current_n)

    for n, margin_text in margin_notes.items():
        if n not in processed_entries:
            store_unmatched(unmatched_notes, n, margin_text)

    print("Processed Entries:", processed_entries)
    return matched_notes, unmatched_notes



# Assuming root is the parsed XML tree and ns is the namespace dictionary
matched_notes, _ = find_matches(root, ns)
print("Matched Notes:", matched_notes)
_, unmatched_notes = find_matches(root, ns)
print("Unmatched Notes:", unmatched_notes)

def store_unmatched_notes(root, unmatched_notes):
    notes_to_insert = []
    for elem in root.iter():
        # Check if this is an entry <div>
        if elem.tag == '{http://www.tei-c.org/ns/1.0}div' and elem.attrib.get("type") == "entry":
            entry_n = elem.attrib.get("n")  # Get the entry number

            # Check if this entry number is in the unmatched notes
            for unmatched in unmatched_notes:
                unmatched_key, margin_text = unmatched

                # If this entry number matches and the margin text matches, store the note
                if entry_n == unmatched_key:
                    # Create the <div type="entry_notes"> with the corresponding note
                    entry_notes_div = etree.Element("{http://www.tei-c.org/ns/1.0}div", type="entry_notes")
                    note = etree.SubElement(entry_notes_div, "{http://www.tei-c.org/ns/1.0}note", place=f"margin page {unmatched_key}", rend="vertical")
                    note.text = margin_text

                    # Store the new entry_notes_div for reinsertion later
                    notes_to_insert.append(entry_notes_div)
                    print(f"Stored note for entry {entry_n}: {margin_text}")
                    break  # No need to continue checking other unmatched_notes for this entry

    return notes_to_insert

def add_notes_to_xml(root, notes_to_insert):
    # Loop through each unmatched note and add it after the corresponding <div type="entry">
    for entry_notes_div in notes_to_insert:
        # Find the <div type="entry" with the corresponding n="key"
        entry_div = None
        entry_n = entry_notes_div.find(".//{http://www.tei-c.org/ns/1.0}note").attrib.get('place').split(' ')[-1]  # Extract the page number from place
        for elem in root.iter():
            if elem.tag == '{http://www.tei-c.org/ns/1.0}div' and elem.attrib.get("type") == "entry" and elem.attrib.get("n") == entry_n:
                entry_div = elem
                break
        
        if entry_div is not None:
            # Insert the <div type="entry_notes"> after the <div type="entry" n="key">
            entry_div.addnext(entry_notes_div)

with open("updated_file.xml", "wb") as file:
    ElementTree(root).write(file, encoding="utf-8", xml_declaration=True)



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

        # Open text file in write mode
        with open(txt_file, 'w') as file:
            # Recursively extract & clean text from XML tree
            entry_n = None  # Declare at outer scope to persist between calls

            def extract_text(element):
                global entry_n  # Use outer-scope entry_n
    # Check for entry <div>
                if element.tag == '{http://www.tei-c.org/ns/1.0}div' and element.attrib.get("type") == "entry":
                    entry_n = element.attrib.get("n")
    
    # Check for entry_notes <div>
                elif element.tag == '{http://www.tei-c.org/ns/1.0}div' and element.attrib.get("type") == "entry_notes":
                    place_notes = root.findall('.//tei:note[@place]', namespaces=ns)
                    for note in place_notes:
                        text = note.text.strip() if note.text else ""
                        if (entry_n, text) in matched_notes:
                            print(f"Matched note for ENTRY N={entry_n}: {text}")
                            return
                # Instead of returning, write to file or collect results
                
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

# Run XML to TXT function
xml_to_txt(xml_file, txt_file, words_to_remove)
print("TXT file created")