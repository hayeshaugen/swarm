from abc import ABC, abstractmethod

class FormatterStrategy(ABC):
    
    @abstractmethod
    def format(self, config, *args):
        pass


class EmailFormatStrategy(FormatterStrategy):
    
    def format(self, config, address, subject, body):
        # Initial concatenation
        formatted_output = config.delimiter.join([address, subject, body])
        
        # Check if the byte length exceeds the max limit
        while len(formatted_output.encode('utf-8')) > config.max_byte_length:
            # If it does, truncate one character from the body and reformat
            body = body[:-1]
            formatted_output = config.delimiter.join([address, subject, body])
        
        return formatted_output
