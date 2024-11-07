import re
import csv
import html

def extract_options(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'<option value="(\d+)">([^<]+)</option>')
    matches = pattern.findall(content)

    decoded_matches = [(id, html.unescape(name)) for id, name in matches]

    return decoded_matches

def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'nome_entidade'])
        writer.writerows(data)

input_file = 'response.txt'
output_file = 'entidades.csv'

options = extract_options(input_file)
save_to_csv(options, output_file)

print(f"CSV gerado com sucesso em: {output_file}")
