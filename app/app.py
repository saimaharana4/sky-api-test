from flask import Flask, jsonify, request
import requests
import pytest
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger Configs
SWAGGER_URL ='/swagger'
API_URL= '/static/swagger.json'
SWAGGER_BLUEPRINT =get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"SKY API "
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/markets/summaries', methods=['GET'])
def get_market_summaries():
    """
    This function will get all market summaries from the Bittrex API
    and return them in JSON format
    """

    # make the GET request to the Bittrex API
    response = requests.get('https://api.bittrex.com/v3/markets/summaries')

    # if the response is successful, convert it to JSON and return it
    if response.status_code == 200:
        return jsonify(response.json())

@app.route('/markets/<marketSymbol>/summary', methods=['GET'])
def get_market_summary(marketSymbol):
    """
    This function will get a market summary for a specific market from the
    Bittrex API and return it in JSON format
    """

    # make the GET request to the Bittrex API
    response = requests.get(f'https://api.bittrex.com/v3/markets/{marketSymbol}/summary')

    # if the response is successful, convert it to JSON and return it
    if response.status_code == 200:
        return jsonify(response.json())

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_get_market_summaries(client):
    """
    This function tests the get_market_summaries function to ensure that it
    is returning the correct data
    """

    # make the GET request and store the response
    response = client.get('/markets/summaries')

    # convert the response data to JSON
    data = response.get_json()

    # assert that the response status code is correct
    assert response.status_code == 200

    # assert that the JSON data is not empty
    assert data != []

def test_get_market_summary(client):
    """
    This function tests the get_market_summary function to ensure that it
    is returning the correct data
    """

    # make the GET request and store the response
    response = client.get('/markets/ltc-btc/summary')

    # convert the response data to JSON
    data = response.get_json()

    # assert that the response status code is correct
    assert response.status_code == 200

    # assert that the JSON data is not empty
    assert data != []

if __name__=='__main__':
    app.run(debug=True)