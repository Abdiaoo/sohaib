import requests

def get_data_from_service(service_url, headers={}, timeout=5):
    try:
        response = requests.get(service_url, timeout=timeout, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the GET request: {e}")
        return None

def post_data_from_service(service_url, headers={}, timeout=5, data={}):
    try:
        response = requests.post(service_url, timeout=timeout, headers=headers, json=data)
        response.raise_for_status() 
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

def delete_data_from_service(service_url, headers={}, timeout=5):
    try:
        response = requests.delete(service_url, timeout=timeout, headers=headers)
        response.raise_for_status() 
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the DELETE request: {e}")
        return None
