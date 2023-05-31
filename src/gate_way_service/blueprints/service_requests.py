import requests
from rest_framework.exceptions import AuthenticationFailed
import jwt
JWT_KEY= "django-insecure-8h7v$dffhmb3w^u+qz#v=x%jmpu%=16%c1q-vik%p2wllwt9bh"
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


def auth(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    payload = jwt.decode(token,JWT_KEY,algorithms=['HS256'],options={"verify_exp": False})
    
    payload.pop('exp')
    payload.pop('iat')
    return payload


def cookies(request):
    is_authenticated = False
    session = requests.get("http://localhost:8040/api/v1/session/validate",cookies=request.COOKIES)
    if session.status_code != 200:
        if session.status_code == 403:
            session = requests.get("http://localhost:8040/api/v1/session/refresh", cookies=request.COOKIES)
            is_authenticated = True
        elif session.status_code != 401:
            pass
        else:
            request.delete_cookie('jwt')
    else:
        is_authenticated = True
    return is_authenticated,request,session