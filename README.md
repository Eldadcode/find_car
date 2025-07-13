# Israeli Car Information Telegram Bot

A Python Telegram bot that retrieves car information from the Israeli government API using license plate numbers.

## Features

- 🔍 **Automatic License Plate Detection**: The bot automatically detects when a message contains a license plate number
- 🚗 **Car Information Retrieval**: Gets car details including manufacturer, model, year, color, engine, and fuel type
- 💬 **No Commands Required**: Simply send a license plate number and get instant results
- 🛡️ **Error Handling**: Robust error handling and user-friendly messages
- 📱 **Modern UI**: Clean, formatted responses with emojis and markdown

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram account
- Access to the Israeli government car database API

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided by BotFather

### 4. Configure Environment Variables

1. Copy `env_example.txt` to `.env`
2. Replace `your_telegram_bot_token_here` with your actual bot token
3. Update API configuration if needed

```bash
cp env_example.txt .env
```

### 5. Update API Configuration (Important!)

The current configuration uses example API endpoints. You'll need to:

1. Find the correct Israeli government API endpoint for car data
2. Update the `LICENSE_PLATE_RESOURCE_ID` in `config.py`
3. Verify the API response structure and update field mappings in `car_api.py` if needed

### 6. Run the Bot

```bash
python bot.py
```

## Usage

Once the bot is running:

1. Start a conversation with your bot on Telegram
2. Send any Israeli license plate number (e.g., "12-345-67" or "1234567")
3. The bot will automatically detect it's a license plate and return car information

## File Structure

```
car-telegram/
├── bot.py              # Main bot application
├── car_api.py          # API handling for car data
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── env_example.txt    # Environment variables template
└── README.md          # This file
```

## API Configuration

The bot is configured to work with the Israeli government's data.gov.il API. You may need to:

1. **Find the correct resource ID**: The current `LICENSE_PLATE_RESOURCE_ID` is an example
2. **Update field mappings**: The `format_car_info` method in `car_api.py` maps API fields to display names
3. **Test API responses**: Use the API directly to understand the response structure

## Customization

### Adding New Car Information Fields

Edit the `field_mappings` dictionary in `car_api.py`:

```python
field_mappings = {
    'manufacturer': ['manufacturer', 'make', 'brand'],
    'model': ['model', 'vehicle_model'],
    'year': ['year', 'model_year', 'manufacture_year'],
    # Add new fields here
    'new_field': ['api_field_name', 'alternative_field_name']
}
```

### Modifying License Plate Detection

Update the `_is_likely_license_plate` method in `bot.py` to match your specific license plate format.

## Troubleshooting

### Common Issues

1. **"BOT_TOKEN not found"**: Make sure you've created a `.env` file with your bot token
2. **"No car information found"**: Check if the API endpoint and resource ID are correct
3. **API errors**: Verify the Israeli government API is accessible and the endpoint is correct

### Debug Mode

Enable debug logging by modifying the logging level in `bot.py`:

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change from INFO to DEBUG
)
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 