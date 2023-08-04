# formatter

`formatter` provides utilities to format data based on various rules and configurations.

## Example Usage:

```
from formatter import FormatterConfig, EmailFormatStrategy, Formatter

config = FormatterConfig(max_byte_length=50, delimiter='!')
strategy = EmailFormatStrategy()
formatter = Formatter(config, strategy)

result = formatter.format_data("test@example.com", "Hello", "This is a test body of the email.")
print(result)
```

```
'test@example.com!Hello!This is a test body of the '
```

