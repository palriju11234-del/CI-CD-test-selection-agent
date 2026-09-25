import math
import hashlib

class ComplexProcessor:
    def __init__(self, data_list):
        self.data_list = data_list

    def process_data(self):
        result = []
        for item in self.data_list:
            if isinstance(item, (int, float)):
                result.append(self._math_operations(item))
            elif isinstance(item, str):
                result.append(self._string_operations(item))
            else:
                result.append(None)
        return result

    def _math_operations(self, number):
        if number < 0:
            return abs(number) ** 2
        elif number == 0:
            return 0
        else:
            return math.sqrt(number) * math.pi

    def _string_operations(self, text):
        if not text:
            return ""
        
        # Reverse string
        reversed_text = text[::-1]
        
        # Calculate SHA256 hash
        sha_signature = hashlib.sha256(reversed_text.encode()).hexdigest()
        
        return f"{reversed_text}-{sha_signature[:10]}"

    def aggregate_results(self, processed_data):
        if not processed_data:
            return 0
            
        numerical_sum = 0
        string_count = 0
        
        for item in processed_data:
            if isinstance(item, (int, float)):
                numerical_sum += item
            elif isinstance(item, str):
                string_count += 1
                
        return numerical_sum + string_count
