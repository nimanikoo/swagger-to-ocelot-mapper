import json
import requests
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_swagger(swagger_url):
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        logging.info(f"Successfully fetched Swagger from URL: {swagger_url}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Swagger from URL: {swagger_url}")
        raise ConnectionError(f"Failed to fetch Swagger from URL: {swagger_url}") from e

def load_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The specified file does not exist: {file_path}")
    with open(file_path, 'r') as file:
        logging.info(f"Successfully loaded JSON from file: {file_path}")
        return json.load(file)

def generate_ocelot_config(swagger, template):
    ocelot_config = {"Routes": []}
    success_count = 0
    failure_count = 0

    for path, methods in swagger['paths'].items():
        for method, details in methods.items():
            try:
                route = template["Routes"][0].copy()
                route["DownstreamPathTemplate"] = path
                route["UpstreamPathTemplate"] = path
                route["UpstreamHttpMethod"] = [method.upper()]
                ocelot_config["Routes"].append(route)
                success_count += 1
                logging.info(f"Generated route: {method.upper()} {path} successfully.")
            except Exception as e:
                failure_count += 1
                logging.error(f"Failed to generate route for {method.upper()} {path}: {e}")

    return ocelot_config, success_count, failure_count

def generate_output_filename(base_filename):
    if os.path.exists(base_filename):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{timestamp}-ocelot.json"
    return base_filename

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    logging.info(f"Configuration saved to {file_path}")

def main(swagger_url, swagger_path, template_path, output_path):
    if swagger_url:
        logging.info(f"Fetching Swagger from URL: {swagger_url}")
        swagger = fetch_swagger(swagger_url)
    elif swagger_path:
        logging.info(f"Loading Swagger from file: {swagger_path}")
        swagger = load_json_file(swagger_path)
    else:
        raise ValueError("No Swagger URL or file path provided. Please provide one.")

    template = load_json_file(template_path)
    ocelot_config, success_count, failure_count = generate_ocelot_config(swagger, template)
    output_filename = generate_output_filename(output_path)
    save_json_file(ocelot_config, output_filename)
    logging.info(f"Ocelot configuration generation completed successfully.")
    logging.info(f"Routes generated successfully: {success_count}")
    logging.info(f"Routes failed to generate: {failure_count}")

if __name__ == "__main__":
    swagger_url = os.environ.get('SWAGGER_URL', None)  # or 'replace your swagger/v1/swagger.json url' if you want to use the URL
    swagger_path = os.environ.get('SWAGGER_PATH', 'swagger.json')  # Path to the mock Swagger JSON file
    template_path = os.environ.get('TEMPLATE_PATH', 'ocelot_template.json')  # Path to the Ocelot template file
    output_path = os.environ.get('OUTPUT_PATH', 'ocelot.json')

    main(swagger_url, swagger_path, template_path, output_path)
