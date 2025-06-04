# CoinGecko API Integration Library

## Configuration Guide

### Environment Configuration

The CoinGecko API integration library supports configuration through environment variables and a configuration file. This allows for flexible and secure configuration across different environments.

#### Configuration Options

1. **API Key (Optional)**
   - Environment Variable: `COINGECKO_API_KEY`
   - Purpose: Used for authenticated API requests (if required)
   - Default: None

2. **API Base URL**
   - Environment Variable: `COINGECKO_API_BASE_URL`
   - Default: `https://api.coingecko.com/api/v3`
   - Purpose: Allows customization of the API endpoint

3. **Request Timeout**
   - Environment Variable: `COINGECKO_REQUEST_TIMEOUT`
   - Default: `10` (seconds)
   - Purpose: Set maximum time for API requests

4. **Logging Level**
   - Environment Variable: `COINGECKO_LOG_LEVEL`
   - Default: `INFO`
   - Allowed Values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Configuration Methods

#### 1. Environment Variables

Set environment variables in your system or .env file:

```bash
export COINGECKO_API_KEY=your_api_key
export COINGECKO_API_BASE_URL=https://api.coingecko.com/api/v3
export COINGECKO_REQUEST_TIMEOUT=15
export COINGECKO_LOG_LEVEL=DEBUG
```

#### 2. Configuration File

Create a `config.py` file in your project:

```python
from coingecko_api import Config

# Custom configuration
config = Config(
    api_key=None,  # Optional API key
    base_url="https://api.coingecko.com/api/v3",
    request_timeout=10,
    log_level="INFO"
)
```

### Best Practices

- Never commit sensitive information like API keys to version control
- Use `.env` files for local development
- Use environment-specific configurations for different environments
- Implement proper error handling for configuration issues

### Troubleshooting

- Ensure all required environment variables are set
- Check that the API key is valid (if authentication is required)
- Verify network connectivity
- Review log files for detailed error information

## Example .env File

```
COINGECKO_API_KEY=
COINGECKO_API_BASE_URL=https://api.coingecko.com/api/v3
COINGECKO_REQUEST_TIMEOUT=10
COINGECKO_LOG_LEVEL=INFO
```

## Installation

```bash
pip install coingecko-api
```