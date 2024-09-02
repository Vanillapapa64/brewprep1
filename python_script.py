import sys
import re
import pytesseract
from PIL import Image
import json

def ocr(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    name_match = re.search(r'Name\s*:\s*(.*?)\n', text)
    name = name_match.group(1).strip() if name_match else "Name not found"

    age_match = re.search(r'Age\s*:\s*(\d+)\s*Years', text)
    age = age_match.group(1).strip() if age_match else "Age not found"

    gender_match = re.search(r'Gender\s*:\s*(\w+)', text)
    gender = gender_match.group(1).strip() if gender_match else "Gender not found"

    hemoglobin_match = re.search(r'Hemoglobin\s+([\d.]+)\s+g/dl', text)
    hemoglobin = hemoglobin_match.group(1) if hemoglobin_match else "Hemoglobin not found"

    rbc_match = re.search(r'RBC Count\s+([\d.]+)\s+mill/mm3', text)
    rbc = rbc_match.group(1) if rbc_match else "RBC Count not found"

    data = {
        "name": name,
        "age": age,
        "gender": gender,
        "hemoglobin": hemoglobin,
        "rbc": rbc
    }

    return data

if __name__ == "__main__":
    image_path = sys.argv[1]
    extracted_data = ocr(image_path)
    print(json.dumps(extracted_data))  # Only print the JSON data
