

import pandas as pd
import re

notes_df = pd.read_csv('dataprep/notes.csv')
terms_df = pd.read_csv('dataprep/terms.csv')

def create_xml_tag(term, type, finding):
    return f'<{finding}_{type}>{term}</{finding}_{type}>'

terms_df['xml_tag'] = terms_df.apply(lambda row: create_xml_tag(row['term'], row['type'], row['finding']), axis=1)

merged_df = pd.merge(notes_df, terms_df, on='note_id')

def replace_terms_with_xml(note, terms, xml_tags, start_chars, end_chars):
    offset = 0
    for term, xml_tag, start_char, end_char in zip(terms, xml_tags, start_chars, end_chars):
        start_char += offset
        end_char += offset
        note = note[:start_char] + xml_tag + note[end_char:]
        offset += len(xml_tag) - len(term)
    return note

# Group the terms by note
grouped_df = merged_df.groupby('note')

# Apply the replace_terms_with_xml function to each group
output_df = grouped_df.apply(lambda x: replace_terms_with_xml(
    x['note'].iloc[0],
    x['term'].tolist(),
    x['xml_tag'].tolist(),
    x['start_char'].tolist(),
    x['end_char'].tolist()
)).reset_index(name='XML input')

print(output_df)

output_df.to_csv("dataprep/output.csv")