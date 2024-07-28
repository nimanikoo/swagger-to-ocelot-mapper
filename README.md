# Ocelot API Gateway Swagger Configurator

A tool for generating Ocelot API Gateway configuration from Swagger (OpenAPI) specifications. This script automates the mapping of Swagger paths to Ocelot routes, supporting both URL and local file inputs for Swagger definitions.

![Ocelot API Gateway Swagger Configurator](https://www.scottbrady91.com/img/logos/swagger-banner.png)

## Features

- Generate Ocelot configuration from Swagger JSON.
- Fetch Swagger JSON from a URL or load from a local file.
- Save output with a timestamp if the file already exists.
- Log each generated route with success and failure counts.
- Unit tests included for verifying configuration generation.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/nimanikoo/swagger-to-ocelot-mapper.git
    cd swagger-to-ocelot-mapper
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command Line

1. **Prepare your Swagger JSON file or have a URL to the Swagger JSON.**
2. **Prepare your Ocelot template JSON file.**

3. **Run the script:**
    ```sh
    python mapper.py
    ```

### Parameters

- `swagger_url` (Optional): URL to fetch Swagger JSON from. Example: `http://example.com/swagger/v1/swagger.json`
- `swagger_path` (Optional): Path to the local Swagger JSON file. Example: `swagger.json`
- `template_path` (Required): Path to the Ocelot template JSON file. Example: `ocelot_template.json`
- `output_path` (Optional): Path to save the generated Ocelot JSON file. Example: `ocelot.json`

### Example Usage

**Using Swagger URL:**
```sh
python mapper.py --swagger_url http://example.com/swagger/v1/swagger.json --template_path ocelot_template.json --output_path ocelot.json
```

**Using local Swagger JSON file:**
```sh
python mapper.py --swagger_path swagger_mock.json --template_path ocelot_template.json --output_path ocelot.json
```

### Example Output

Running the script with the provided command will generate an Ocelot configuration file with the following structure:

```json
{
  "Routes": [
    {
      "DownstreamPathTemplate": "/api/test/endpoint1",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [
        {
          "Host": "TempDownStreamHost",
          "Port": 5000
        }
      ],
      "UpstreamPathTemplate": "/api/test/endpoint1",
      "UpstreamHttpMethod": [
        "GET"
      ],
      "AuthenticationOptions": {
        "AuthenticationProviderKey": "Bearer",
        "AllowedScopes": []
      },
      "RateLimitOptions": {
        "ClientWhitelist": [],
        "EnableRateLimiting": true,
        "Period": "1m",
        "PeriodTimespan": 60,
        "Limit": 66
      },
      "RouteIsCaseSensitive": true,
      "SwaggerKey": "core"
    },
    {
      "DownstreamPathTemplate": "/api/test/endpoint2",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [
        {
          "Host": "TempDownStreamHost",
          "Port": 5000
        }
      ],
      "UpstreamPathTemplate": "/api/test/endpoint2",
      "UpstreamHttpMethod": [
        "POST"
      ],
      "AuthenticationOptions": {
        "AuthenticationProviderKey": "Bearer",
        "AllowedScopes": []
      },
      "RateLimitOptions": {
        "ClientWhitelist": [],
        "EnableRateLimiting": true,
        "Period": "1m",
        "PeriodTimespan": 60,
        "Limit": 40
      },
      "RouteIsCaseSensitive": true,
      "SwaggerKey": "core"
    }
  ]
}
```

### Console Output

During execution, the script will log the progress and results:

```
Successfully generated route for endpoint: /api/test/endpoint1
Successfully generated route for endpoint: /api/test/endpoint2
Total routes generated successfully: 2
Total routes failed to generate: 0
```

## Sample Files

### Ocelot Template (`ocelot_template.json`)

```json
{
  "Routes": [
    {
    "DownstreamPathTemplate": "DownStreamPath",
    "DownstreamScheme": "http",
    "DownstreamHostAndPorts": [
      {
        "Host": "TempDownStreamHost",
        "Port": 5000
      }
    ],
    "UpstreamPathTemplate": "UpStreamPath",
    "UpstreamHttpMethod": [ "UpStreamMethod" ],
    "AuthenticationOptions": 
    {
      "AuthenticationProviderKey": "Bearer",
      "AllowedScopes": []
    },
    "RateLimitOptions": {
      "ClientWhitelist": [],
      "EnableRateLimiting": true,
      "Period": "1m",
      "PeriodTimespan": 60,
      "Limit": 3
    },
    "RouteIsCaseSensitive": true,
    "SwaggerKey": "base"
  }
  ]
}
```

### Swagger Mock (`swagger.json`)

```json
{
  "paths": {
    "/api/test/endpoint1": {
      "get": {
        "tags": ["Test"],
        "responses": {
          "200": {
            "description": "Success"
          }
        }
      }
    },
    "/api/test/endpoint2": {
      "post": {
        "tags": ["Test"],
        "responses": {
          "200": {
            "description": "Success"
          }
        }
      }
    }
  }
}


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.
