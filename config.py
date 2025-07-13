import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Israeli government API configuration
ISRAELI_API_BASE_URL = "https://data.gov.il/api/3/action/datastore_search"
LICENSE_PLATE_RESOURCE_ID = "053cea08-09bc-40ec-8f7a-156f0677aff3"  # Resource ID for private-and-commercial-vehicles dataset
LICENSE_PLATE_RESOURCE_ID_2 = "0866573c-40cd-4ca8-91d2-9dd2d7a492e5"  # Second resource ID for additional car data

# API headers
API_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
} 