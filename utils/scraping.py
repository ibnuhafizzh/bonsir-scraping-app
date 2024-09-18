import requests
import json

# Your API Key and Search Engine ID from Google
API_KEY = 'AIzaSyDLXFLRFaYtefgZy_3BwX9ADHguKSLhs6s'  # Replace with your API key
CX = '3495ed3f98c3e4196'  # Replace with your Custom Search Engine ID

# Function to fetch search results from Google Custom Search API
def google_search(company_name, api_key, cx, num_results=10):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': company_name,
        'num': num_results,
    }
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to extract total search results (an indicator of company exposure)
def extract_total_results(search_results):
    try:
        total_results = int(search_results['searchInformation']['totalResults'])
        return total_results
    except KeyError:
        return 0

companies_example = {"Bank Mandiri", "Bank BCA", "Bank BRI"}
def scraping_result(companies):
# List of companies to analyze
    print(companies)
    # Arrays to store company and its exposure (total search results)
    company_exposure = {}

    # Iterate over each company and perform a search
    for company in companies:
        company = '"'+company+'"'
        search_results = google_search(company, API_KEY, CX)
        if search_results:
            total_results = extract_total_results(search_results)
            company_exposure[company] = total_results
            print(f"{company}: {total_results} results found")
        else:
            print(f"Could not retrieve results for {company}")

    # Sort companies (from highest to lowest)
    sorted_exposure = sorted(company_exposure.items(), key=lambda x: x[1], reverse=True)

    # Display sorted results
    print("\nSorted Company:")
    for company, exposure in sorted_exposure:
        print(f"{company}: {exposure} results")

    return sorted_exposure