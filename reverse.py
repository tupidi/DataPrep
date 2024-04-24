

import pandas as pd
import re

def extract_terms_from_xml(xml_string):
    pattern = r'<(.*?)>(.*?)</\1>'
    matches = re.findall(pattern, xml_string)
    
    data = []
    for match in matches:
        finding, type = match[0].split('_')
        term = match[1]
        start_tag = f'<{match[0]}>'
        end_tag = f'</{match[0]}>'
        start_char = xml_string.index(start_tag)
        end_char = xml_string.index(end_tag) - len(start_tag)
        xml_string = xml_string.replace(start_tag, '', 1).replace(end_tag, '', 1)
        data.append([term, type, finding, start_char, end_char])
    
    return pd.DataFrame(data, columns=['term', 'type', 'finding', 'start_char', 'end_char'])

# Example usage
xml_input = "Nitish having no <negative_symptom>distress</negative_symptom>, and <negative_disease>diabetes</negative_disease>"
output_df = extract_terms_from_xml(xml_input)

print(output_df)