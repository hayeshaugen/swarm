import base64

class DataProcessor:
    @staticmethod
    def hex_to_int(hex_value):
        return int(hex_value, 16)
    
    @staticmethod
    def encode_data(data):
        return base64.b64encode(data.encode()).decode()
