import json
from pathlib import Path

# Base data directory
base_path = Path("D:\DirectEd\Geni AI\The-Gilded-Fork-API\data")

# Input files
files = {
    "Hours": base_path / "hours.json",
    "Contact": base_path / "info.json",
    "Menu": base_path / "menu.json"
}

# Output file
output_file = base_path / "combined_output.txt"

# Function to format JSON content
def format_paragraph(data, title):
    paragraph = f"{title}:\n"
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                value = ", ".join(value)
            elif isinstance(value, dict):
                value = ", ".join(f"{k.replace('_', ' ').title()}: {str(v)}" for k, v in value.items())
            paragraph += f"- {key.replace('_', ' ').title()}: {value}\n"
    return paragraph.strip() + "\n\n"

# Process each file and write to output
with open(output_file, 'w', encoding='utf-8') as outfile:
    for title, filepath in files.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            formatted = format_paragraph(data, title)
            outfile.write(formatted)

print(f"Combined content saved to: {output_file}")
