import requests
import re
from typing import Optional, Dict, Any
from config import ISRAELI_API_BASE_URL, LICENSE_PLATE_RESOURCE_ID, LICENSE_PLATE_RESOURCE_ID_2, API_HEADERS

class CarDataAPI:
    """Class to handle API calls to Israeli government car database"""
    
    def __init__(self):
        self.base_url = ISRAELI_API_BASE_URL
        self.resource_id = LICENSE_PLATE_RESOURCE_ID
        self.resource_id_2 = LICENSE_PLATE_RESOURCE_ID_2
        self.headers = API_HEADERS
    
    def clean_license_plate(self, license_plate: str) -> str:
        """Clean and format license plate number"""
        # Remove spaces, dashes, and convert to uppercase
        cleaned = re.sub(r'[\s\-]', '', license_plate.upper())
        return cleaned
    
    def validate_license_plate(self, license_plate: str) -> bool:
        """Validate Israeli license plate format"""
        # Israeli license plates typically have 7-8 characters
        # Format: 12-345-67 or 123-45-678
        cleaned = self.clean_license_plate(license_plate)
        if len(cleaned) < 6 or len(cleaned) > 8:
            return False
        return True
    
    def _search_single_resource(self, license_plate: str, resource_id: str) -> Optional[Dict[str, Any]]:
        """Search for car information in a specific resource"""
        try:
            # Prepare API request parameters
            # Use filters for more efficient column-specific search
            params = {
                'resource_id': resource_id,
                'filters': f'{{"mispar_rechev": "{license_plate}"}}',
                'limit': 10
            }
            
            # Make API request
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"API request failed with status code: {response.status_code}")
                return None
            
            data = response.json()
            
            # Check if we got results
            if not data.get('success', False):
                print("API request was not successful")
                return None
            
            records = data.get('result', {}).get('records', [])
            
            if not records:
                return None
            
            # Return the first matching record
            return records[0]
            
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def search_car_by_license_plate(self, license_plate: str) -> Optional[Dict[str, Any]]:
        """Search for car information by license plate number in both resources"""
        try:
            cleaned_plate = self.clean_license_plate(license_plate)
            
            if not self.validate_license_plate(cleaned_plate):
                return None
            
            # Try first resource
            print(f"Searching in primary resource for license plate: {cleaned_plate}")
            car_data = self._search_single_resource(cleaned_plate, self.resource_id)
            
            if car_data:
                print("Found car data in primary resource")
                return car_data
            
            # If not found in first resource, try second resource
            print(f"Not found in primary resource, trying secondary resource for license plate: {cleaned_plate}")
            car_data = self._search_single_resource(cleaned_plate, self.resource_id_2)
            
            if car_data:
                print("Found car data in secondary resource")
                return car_data
            
            print("Car not found in either resource")
            return None
            
        except Exception as e:
            print(f"Error in search_car_by_license_plate: {e}")
            return None
    
    def format_car_info(self, car_data: Dict[str, Any]) -> str:
        """Format car information into a readable message"""
        try:
            # Extract relevant information from the Israeli CKAN database response
            car_info = []
            
            # Israeli database field mappings based on the actual response
            field_mappings = {
                'מספר רישוי': 'mispar_rechev',
                'יצרן': 'tozeret_nm',
                'דגם': 'degem_nm',
                'שם מסחרי': 'kinuy_mishari',
                'שנת ייצור': 'shnat_yitzur',
                'צבע': 'tzeva_rechev',
                'סוג דלק': 'sug_delek_nm',
                'בעלות': 'baalut',
                'מספר שלדה': 'misgeret',
                'מנוע': 'degem_manoa',
                'תאריך בדיקה אחרונה': 'mivchan_acharon_dt',
                'תוקף רישום': 'tokef_dt',
                'צמיגים קדמיים': 'zmig_kidmi',
                'צמיגים אחוריים': 'zmig_ahori'
            }
            
            for display_name, field_name in field_mappings.items():
                if field_name in car_data and car_data[field_name]:
                    value = str(car_data[field_name]).strip()
                    if value and value.lower() not in ['null', 'none', '']:
                        car_info.append(f"**{display_name}:** {value}")
            
            if not car_info:
                return "נמצא מידע על הרכב אך אין פרטים זמינים."
            
            return "\n".join(car_info)
            
        except Exception as e:
            print(f"Error formatting car info: {e}")
            return "שגיאה בעיצוב מידע על הרכב." 