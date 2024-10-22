import xml.etree.ElementTree as ET

def xml_to_txt(xml_file, txt_file, words_to_remove):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    #Helper method to not include specific words in txt
    def remove_words(text, words_to_remove):
         for word in words_to_remove:
              text = text.replace(word, '')
         return text

    # Open the text file in write mode
    with open(txt_file, 'w') as file:
        # Recursively extract text from XML tree
        def extract_text(element):
            if element.text:
                clean_text = remove_words(element.text, words_to_remove)
                file.write(clean_text.strip() + '')
                file.write('\n')

            # Recursively extract text from children
            for child in element:
                extract_text(child)

            # Handle element tail text if present
            if element.tail:
                 cleaned_tail = remove_words(element.tail, words_to_remove)
                 file.write(cleaned_tail.strip() + '')
                 file.write('\n')

        # Start extracting from the root element
        extract_text(root)

#Set desired xml,txt using pathname
xml_file = '/Users/chelsea/SDP files/SDP/texts/diary55fix?.xml'
txt_file = '/Users/chelsea/SDP files/SDP/texts/diary55.txt'
words_to_remove = ['[torn]', '[struck through]', '[strikethrough]', '[illegible]', '[crossed out]', '[Arabic]'] #list of words to remove
xml_to_txt(xml_file, txt_file, words_to_remove)