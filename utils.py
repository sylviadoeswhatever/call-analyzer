import re
import csv
import io

def clean_text(text: str) -> str:
    """Removes special characters from text, keeping only alphanumeric and basic punctuation."""
    if not text:
        return ""
    # Remove characters that are not word characters, whitespace, or basic punctuation
    cleaned = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def format_timestamp(seconds: float) -> str:
    """Converts float seconds to MM:SS format."""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def segments_to_csv(segments: list[dict]) -> str:
    """Converts the list of segment dictionaries to a CSV string."""
    if not segments:
        return ""
    
    # We want to use StringIO to write CSV data to a string
    output = io.StringIO()
    # Define the fields expected in the list of dicts based on the shape in rule 3
    fieldnames = ['start', 'end', 'text', 'sentiment', 'sentiment_score', 'intent']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    
    for segment in segments:
        # Format the timestamps to MM:SS before writing to CSV, or keep raw seconds?
        # Let's keep raw data in CSV, it's more standard for data export, but let's format it nicely for the CSV as well if we want to be user-friendly. The rule says "converts data list to CSV string".
        # Let's write the raw dict data.
        row = segment.copy()
        # Optional: format timestamps in the CSV too
        if 'start' in row:
            row['start'] = format_timestamp(row['start'])
        if 'end' in row:
            row['end'] = format_timestamp(row['end'])
        
        writer.writerow(row)
        
    return output.getvalue()
