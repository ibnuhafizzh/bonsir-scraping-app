import requests

# Your API Key and Search Engine ID
API_KEY = 'AIzaSyDLXFLRFaYtefgZy_3BwX9ADHguKSLhs6s'  # Replace with your API key
CX = '3495ed3f98c3e4196'  # Replace with your Custom Search Engine ID

# Function to fetch search results from Google Custom Search API
def google_search(company_name, api_key=API_KEY, cx=CX, num_results=10):
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
        return "99"

# Function to extract total search results (an indicator of company exposure)
def extract_total_results(search_results):
    try:
        total_results = int(search_results['searchInformation']['totalResults'])
        return total_results
    except KeyError:
        return 0

# Function to scrape results for companies
def scraping_result(companies):
    company_exposure = {}
    for company in companies:
        company = '"' + company + '"'
        search_results = google_search(company)
        if search_results == "99":
            print(f"Could not retrieve results for {company}")
            return "99"
        if search_results:
            total_results = extract_total_results(search_results)
            company_exposure[company] = total_results
            print(f"{company}: {total_results} results found")
        else:
            print(f"Could not retrieve results for {company}")
            return "99"
    sorted_exposure = sorted(company_exposure.items(), key=lambda x: x[1], reverse=True)
    return sorted_exposure
