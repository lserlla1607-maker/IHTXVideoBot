import re

def trim_after_link(text):
    # Regex to find common URL patterns (http/https followed by non-whitespace characters)
    # This pattern captures the entire URL.
    url_pattern = r'https?://\S+' 
    
    match = re.search(url_pattern, text)
    
    if match:
        # Get the start and end index of the matched URL
        start_index = match.start()
        end_index = match.end()
        
        # Keep the text up to and including the URL
        trimmed_text = text[:end_index]
        return trimmed_text
    else:
        # If no link is found, return the original text
        return text

# Example usage
text_with_link = "This is some text with a link https://www.example.com/page and more text after it."
trimmed = trim_after_link(text_with_link)
print(f"Original: {text_with_link}")
print(f"Trimmed: {trimmed}")

text_without_link = "This text has no link."
trimmed_no_link = trim_after_link(text_without_link)
print(f"Original: {text_without_link}")
print(f"Trimmed: {trimmed_no_link}")