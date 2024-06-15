import easyocr
import re
from PIL import Image
from datetime import datetime

def extract_running_record(image_path):

    """
    Extracts running record information from an OCR-scanned image.

    Args:
    - image_path (str): Path to the screenshot image containing the running record.

    Returns:
    - dict: Dictionary containing extracted running record information:
        {
            'Date': 'YYYY-MM-DD',
            'Time': 'hh:mm AM/PM',
            'Distance': 'XXX.XX km',
            'Calories': 'XXX kcal'
        }
      Missing keys will not be included in the dictionary.
    """

    # Load the image using Pillow (PIL)
    img = Image.open(image_path)
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)  # Specify language, e.g., 'en' for English
    
    # Perform OCR on the image
    result = reader.readtext(image_path)

    # Extract all text into a single string
    all_text = ' '.join([text for (bbox, text, score) in result])
    
    # Initialize an empty dictionary to store the running record
    running_record = {}

    # Define regex patterns for extracting date, time, distance, and calories
    date_pattern = r'(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{1,2},\s*\d{4}\b)'  # Matches date in format 'Month day, year'
    time_pattern = r'(\b\d{1,2}\.\d{2}\s+(?:AM|PM)\b)'  # Matches time in format 'hh:mm AM/PM'
    distance_pattern = r'(\d+(\.\d+)?\s*(km)?)'  # Matches distance in format '123.45 km'
    calories_pattern = r'(\d+\s*kcal)'  # Matches calories in format '123 kcal'

    # Search for patterns in the all_text string
    date_match = re.search(date_pattern, all_text)
    print(date_match)
    time_match = re.search(time_pattern, all_text)
    print(time_match)
    distance_match = re.search(distance_pattern, all_text)
    calories_match = re.search(calories_pattern, all_text)

    # Extract and store matched information in the running_record dictionary
    if date_match: 
        running_record['Date'] = datetime.strptime(date_match.group(0), '%B %d,%Y').strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD format
    if time_match:
        running_record['Time'] = time_match.group(1)  # Get the matched time
    if distance_match:
        running_record['Distance'] = distance_match.group(1)  # Get the matched distance
    if calories_match:
        running_record['Calories'] = calories_match.group(1).strip()  # Get the matched calories

    return running_record

# main was used for testing
if __name__ == "__main__":
    # Path to the screenshot image
    image_path = 'run_record.jpg'  # Update this path accordingly
    running_record = extract_running_record(image_path)
    
    # Print the extracted running record
    print("Running Record:")
    print(running_record)
