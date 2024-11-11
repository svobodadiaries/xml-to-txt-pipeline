import xml.etree.ElementTree as ET
import re

namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

def xml_to_txt_with_margin_notes_and_match(xml_file, txt_file, words_to_remove):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Helper method to exclude specific words from the text
        def remove_words(text, words_to_remove):
            for word in words_to_remove:
                text = text.replace(word, '')
            return text

        # Extract and store margin entry notes with their page numbers
        def extract_margin_notes(element):
            margin_notes = {}  # Dictionary to store notes with page numbers
            # Look for all <note> elements that have a 'place' attribute set to 'margin'
            notes_with_place = [note for note in root.findall('.//tei:note[@place]', namespaces=namespace) if 'place' in note.attrib]
            for note in notes_with_place:
                place_attribute = note.attrib.get('place', '')
                if 'margin' in place_attribute:
                    page_number = note.attrib.get('place', '').split()[-1] if place_attribute else 'unknown'  # Extract page number from 'place' attribute
                    note_text = note.text.strip() if note.text else ''
                
                # Debug print to see if we are extracting margin notes correctly
                print(f"Found margin note: {note_text} on page {page_number}")
                
                if page_number not in margin_notes:
                    margin_notes[page_number] = []
                margin_notes[page_number].append(note_text)

            return margin_notes

        # Function to check if the current text matches any margin notes
        # def check_for_margin_note_match(current_text, page_number, margin_notes, matched_notes):
        #     # Check if the page number exists in margin_notes
        #     if page_number in margin_notes:
        #         # Compare the current text with the margin note text (simple substring match or regex)
        #         for note in margin_notes[page_number]:
        #             if re.search(r'\b' + re.escape(note) + r'\b', current_text):  # Match whole words
        #                 matched_notes.add(note)  # Store the matched note

        # Function to write the text to the file, extracting the text from XML
        def extract_text(element, margin_notes):
            matched_notes = set()  # Set to store matched margin notes

            with open(txt_file, 'w') as file:
                def recursive_extract(element, current_page_number):
                    # If element has text, clean and write it
                    if element.text:
                        clean_text = remove_words(element.text, words_to_remove)
                        file.write(clean_text.strip() + '\n')

                        # Check for margin note match
                        # check_for_margin_note_match(clean_text, current_page_number, margin_notes, matched_notes)

                    # Handle margin notes and their page number
                    if element.tag == 'div' and 'type' in element.attrib and element.attrib['type'] == 'entry_notes':
                        # Check if there are any margin notes and write them
                        for page_number, notes in margin_notes.items():
                            for note in notes:
                                file.write(f"[Page {page_number}] {note}\n")

                    # Recursively extract text from children
                    for child in element:
                        # Pass the current page number down recursively (modify as needed for real page numbers)
                        if 'page' in element.attrib:  # Example of how page might be stored in an element
                            current_page_number = element.attrib['page']
                        else:
                            current_page_number = current_page_number  # Default to last page number
                        recursive_extract(child, current_page_number)

                    # Handle element tail text if present
                    if element.tail:
                        cleaned_tail = remove_words(element.tail, words_to_remove)
                        file.write(cleaned_tail.strip() + '\n')

                        # Check for margin note match
                        # check_for_margin_note_match(cleaned_tail, current_page_number, margin_notes, matched_notes)

                # Begin recursive extraction
                recursive_extract(element, current_page_number="")  # Start with an empty page number or modify as necessary

            # return matched_notes  # Return the set of matched margin notes

        # Step 1: Extract margin notes and their page numbers
        margin_notes = extract_margin_notes(root)

        # Debug print to check the extracted margin notes
        print("Extracted margin notes:")
        for page, notes in margin_notes.items():
            print(f"Page {page}: {notes}")

        # Step 2: Convert the XML to text and check for margin note matches
        # matched_notes = extract_text(root, margin_notes)

        # Step 3: Output matched margin notes (for debugging or further processing)
        # if matched_notes:
        #     print("Matched Margin Notes:")
        #     for note in matched_notes:
        #         print(note)

    except ET.ParseError:
        print("Error: Failed to parse XML file.")
    except IOError as e:
        print(f"Error: {e}")

# Set desired XML, TXT using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55TEST.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55TEST.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]']  # List of words to exclude in TXT

# Run the function to convert XML to TXT and capture margin notes
xml_to_txt_with_margin_notes_and_match(xml_file, txt_file, words_to_remove)

