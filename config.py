import os

# Load API key from environment variable or file
def get_api_key():
    # First try to get from environment variable
    api_key = os.getenv('CURSOR_API_KEY')
    
    # If not in environment, try to read from file
    if not api_key:
        try:
            with open('apy', 'r') as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            print("Warning: API key not found in environment or file")
            return None
    
    return api_key

# Export the API key
API_KEY = get_api_key() 