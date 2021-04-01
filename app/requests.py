import urllib.request, json
from .models import Quote

quote_url = None

def configure_request(app):
    global quote_url
    quote_url = app.config['QUOTE_API_URL']

def get_quote():
    '''
    Function that gets the json response to our url request
    '''

    get_quote_url = quote_url

    print(get_quote_url)

    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)
        print(get_quote_response)

        quote_object = None

        if get_quote_response:
            quote_object = Quote(get_quote_response['id'], get_quote_response['author'], get_quote_response['quote'])

        print(quote_object)

    return quote_object