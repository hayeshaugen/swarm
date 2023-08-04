# Formatter

The `formatter` offers a modular and extensible solution for data formatting. It's designed to be flexible, accommodating various formatting rules and configurations.

## Examples

### Formatting Email Data

Here's how you can use the package to format email data:

```python
from formatter import FormatterConfig, EmailFormatStrategy, Formatter

# Setting up configuration and strategy
config = FormatterConfig(max_byte_length=50)
strategy = EmailFormatStrategy()
formatter = Formatter(config, strategy)

# Formatting data
result = formatter.format_data("test@example.com", "Hello", "This is a test body of the email.")
print(result)  # Outputs: 'test@example.com|Hello|This is a test body of the '
```

With the provided configuration and strategy, the email body is truncated to ensure the overall formatted string does not exceed the specified byte length.

### Extending with New Strategies

To extend the package with a new strategy, create a strategy class that inherits from `FormatterStrategy` and implement the required `format` method.

Example:

```python
class CustomFormatStrategy(FormatterStrategy):
    def format(self, config, *args):
        # Your custom formatting logic here
        pass

# Usage:
strategy = CustomFormatStrategy()
formatter = Formatter(config, strategy)
result = formatter.format_data(your_data_here)
print(result)
```
