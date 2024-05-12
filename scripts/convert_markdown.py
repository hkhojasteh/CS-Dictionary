import pandas as pd
import yaml
import os

def markdown_to_dataframe(markdown_path):
    """ Convert Markdown table to DataFrame """
    with open(markdown_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    for i, line in enumerate(lines):
        if i == 1:  # skip the formatting line
            continue
        parts = [part.strip() for part in line.split('|')]
        if len(parts) == 5:
            data.append(parts)

    df = pd.DataFrame(data[2:], columns=data[0])  # first two row as headers
    return df

def dataframe_to_csv(df, csv_path):
    """ Save DataFrame to CSV """
    if not os.path.exists(os.path.dirname(csv_path)):
        os.makedirs(os.path.dirname(csv_path))

    df.to_csv(csv_path, index=False)

def dataframe_to_yaml(df, yaml_path):
    if not os.path.exists(os.path.dirname(yaml_path)):
        os.makedirs(os.path.dirname(yaml_path))

    """ Convert DataFrame to YAML and save """
    df.rename(columns={
        'واژهٔ انگلیسی': 'english_word',
        'معادل مصوب فرهنگستان': 'official_equivalent',
        'معادل پیشنهادی': 'suggested_equivalent',
        'معادل (های) دیگر': 'other_equivalents',
        'رشته': 'field'
    }, inplace=True)

    records = df.to_dict(orient='records')
    yaml_data = {record['english_word']: {k: v for k, v in record.items() if k != 'english_word'} for record in records}

    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(yaml_data, file, allow_unicode=True)

# File paths
markdown_file_path = './README.md'
csv_file_path = './data/table_converted.csv'
yaml_file_path = './data/table_converted.yaml'

# Conversion process
df = markdown_to_dataframe(markdown_file_path)
dataframe_to_csv(df, csv_file_path)
dataframe_to_yaml(df, yaml_file_path)
