import csv
import re
import sys
from typing import Dict, List, Tuple

PATTERN = re.compile(r"^([\S\s]+)\|(\(\d+(?:-\d+)?,[\s\S]+\))+$")
TOKEN_PATTERN = re.compile(r"\((\d+(?:-\d+)?),([^\)]+)\)")


class Replacement:
    def __init__(self, text, start_pos, last_pos, annotation):
        self.text = text
        self.start_pos = start_pos
        self.last_pos = last_pos
        self.annotation = annotation


def get_file_output_path(file_input_path: str) -> str:
    if not file_input_path.endswith("csv"):
        raise ValueError("File should use csv as extension.")

    return re.sub("csv$", "out.csv", file_input_path)


def is_to_replace(text: str) -> bool:
    match_results = PATTERN.match(text)
    return match_results is not None


def build_ruby(text, annotation):
    return f"<ruby>{text}<rt>{annotation}</rt></ruby>"


def replace_text(text: str) -> str:
    match_results = PATTERN.match(text)
    original_text = match_results.group(1)
    token_text = match_results.group(2)
    tokens: List[Tuple[str, str]] = TOKEN_PATTERN.findall(token_text)

    replacements: Dict[int, Replacement] = {}

    for token in tokens:
        pos, annotation = token
        if "-" in pos:
            start_pos, end_pos = (int(i) - 1 for i in pos.split("-"))
        else:
            start_pos = end_pos = int(pos) - 1
        replacements[start_pos] = Replacement(original_text[start_pos:end_pos + 1], start_pos, end_pos, annotation)

    out = ""

    length = len(original_text)

    i = 0
    while i < length:
        if i not in replacements:
            out += original_text[i]
            i += 1
        else:
            replacement = replacements[i]
            out += build_ruby(replacement.text, replacement.annotation)
            i = replacement.last_pos + 1
    return out


def handle_row(row: Dict[str, str]) -> Dict[str, str]:
    result = {}
    for key in row.keys():
        if is_to_replace(row[key]):
            result[key] = replace_text(row[key])
        else:
            result[key] = row[key]
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <CSV file path>")
        exit(1)

    f_input_path = sys.argv[1]
    f_output_path = get_file_output_path(f_input_path)

    with open(f_input_path) as csv_input_file:
        reader = csv.DictReader(csv_input_file)
        fieldnames = reader.fieldnames
        rows = [row for row in reader]

    out_rows = [handle_row(row) for row in rows]

    with open(f_output_path, "w") as csv_output_file:
        writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)
