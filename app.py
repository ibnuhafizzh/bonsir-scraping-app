from flask import Flask, render_template, request, jsonify
from utils.scrape import scraping_result

app = Flask(__name__)

# Route for the homepage with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Route for Menu A
@app.route('/scraping')
def menu_a():
    return render_template('scrape.html')

# Route for Menu B
@app.route('/alfin')
def menu_b():
    return render_template('alfin.html')

# Route to handle the form submission
@app.route('/scrape', methods=['POST'])
def scrape():
    # Get user input from form
    company_names = request.form.getlist('company[]')

    # Call scraping function
    sorted_companies = scraping_result(company_names)

    if (sorted_companies == "99"): 
        return render_template('scrape.html', error=sorted_companies)
    # Render the same template with sorted companies
    return render_template('scrape.html', sorted_companies=sorted_companies)

if __name__ == '__main__':
    app.run(debug=True)
