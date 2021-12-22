@app.route('/')
def customer():
    return render_template('')

    @app.route('/', methods = ['POST', 'GET'])
    def result():
    url = "/"
    if request.method == 'POST':


import requests
 api_url = "/"
 response = requests.get(api_url)
 response.json()
{'profile': 1, 'list': 1, 'title': 'Customer profile', 'completed': False}
