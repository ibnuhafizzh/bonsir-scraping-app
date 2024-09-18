from flask import Flask, render_template, request, jsonify
from utils.scraping import scraping_result

app = Flask(__name__)

# Route for the homepage with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Route for Menu A
@app.route('/scraping')
def menu_a():
    return render_template('scraping.html')

# Route for Menu B
@app.route('/alfin')
def menu_b():
    return render_template('alfin.html')

@app.route('/scraping-generator', methods=['POST'])
def scraping():
    # Get the list and sorting order from the request
    data = request.json
    items = data.get('items', [])

    # Sort the list using the imported function
    result = scraping_result(items)
    
    # Return the sorted list as JSON
    return jsonify({'sorted_items': result})

if __name__ == '__main__':
    app.run(debug=True)
