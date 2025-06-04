# CoinGecko API Integration Configuration Guide

## Overview
This document provides comprehensive guidance on configuring the CoinGecko API integration library.

## Configuration Options

### Environment Variables
The library supports configuration through environment variables. Create a `.env` file in the project root with the following options:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `COINGECKO_API_KEY` | Optional API key for CoinGecko Pro | `None` | No |
| `COINGECKO_BASE_URL` | Base URL for CoinGecko API | `https://api.coingecko.com/api/v3` | No |
| `REQUEST_TIMEOUT` | Default timeout for API requests (in seconds) | `10` | No |
| `CACHE_EXPIRY` | Default cache expiration time (in seconds) | `300` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | No |

## Configuration Examples

### Basic Configuration
```python
from coingecko_api import CoinGeckoClient

# Uses default settings
client = CoinGeckoClient()
```

### Custom Configuration
```python
from coingecko_api import CoinGeckoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom configuration
client = CoinGeckoClient(
    api_key=os.getenv('COINGECKO_API_KEY'),
    base_url=os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'),
    timeout=int(os.getenv('REQUEST_TIMEOUT', 10)),
    cache_expiry=int(os.getenv('CACHE_EXPIRY', 300))
)
```

## Best Practices
1. Never commit sensitive information like API keys to version control
2. Use `.env` file for local development
3. Use environment-specific configurations for different deployment environments
4. Implement proper error handling when configuration is incomplete

## Troubleshooting
- Ensure all required dependencies are installed
- Check that environment variables are correctly set
- Verify network connectivity
- Review API key permissions and validity