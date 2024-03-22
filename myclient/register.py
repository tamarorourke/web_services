import requests

def register(agency_name, agency_url, agency_code):
    directory_url = "https://newssites.pythonanywhere.com/api/directory/"
    
    payload = {
        "agency_name": agency_name,
        "url": agency_url,
        "agency_code": agency_code
    }
    
    response = requests.post(directory_url, json=payload)
    
    if response.status_code == 201:
        print(f"Agency '{agency_name}' registered.")
    else:
        print(f"Failed to register. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Replace these with actual values for your news agency
    name_of_agency = "Tamar ORourke News Agency"
    url_of_agency = "https://sc21tor.pythonanywhere.com"
    code_of_agency = "TRO00"
    
    register(name_of_agency, url_of_agency, code_of_agency)