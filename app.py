"""Written in flask and in a more modular way than directed and provides further examples"""
from flask import Flask, request, url_for, render_template
from caesar import rotate_string
from caesar import basic_external_method_example
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!doctype html>
    <html>
        <style>
            form {
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }
            textarea {
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }
        </style>
        <body>
            <form action="/encrypt" method="post">
            <div>
                <label for="rot">Rotate by:</label>
                <input id="rot" type="rot" name="rot" value='1'/>

                <textarea id="text" type="text" name="text">example text to rotate</textarea>

                <input type="submit" />
            </div>
            </form>
        </body>
    </html>
"""

@app.route("/")
def index():
    """templates/index.html http://localhost:5000/
    runs encrypt method and provides query params, easily repeatable
    http://localhost:5000/?rot=3&text=a"""
    return form

@app.route("/encrypt", methods=['POST', 'GET'])
def encrypt():
    """ie hitting submit querry over and over and both urls below work
    http://localhost:5000/encrypt # defaults to 1, a
    http://localhost:5000/encrypt?rot=3&text=p can be clicked again and again """
    if request.args:
        text = request.args.get('text')
        rot = int(request.args.get('rot'))
    elif request.form:
        text = request.form['text']
        rot = int(request.form['rot'])

    result_text = rotate_string(text, rot)
    result_rot = rot

    # option 1: just render result, not form
    # return result

    # option 2
    return render_template('index.html', result_text=result_text, result_rot=result_rot)

@app.route('/basic_encrypt')
def basic_encrypt():
    """http://localhost:5000/basic_encrypt"""
    text = 'abc'
    rot = 3
    result = rotate_string(text, rot)
    return result

@app.route('/encrypt_once', methods=['POST', 'GET'])
def encrypt_once(result_rot=None, result_text=None):
    """How to render a global variable form, used with rotate_string to encrypt a message"""
    if request.args:
        result_rot = int(request.args.get('rot'))
        result_text = request.args.get('text')
    else:
        # option 1: set default values
        # result_rot = 1
        # result_text = 'abc'

        # option 2: just render empty form
        return form

    result_text = rotate_string(result_text, result_rot)

    # option 1: simply return a new html page with the results
    return render_template('result.html', result_rot=result_rot, result_text=result_text)

    # option 2: render a similar template page to form called index.html, that inserts the results
    # return render_template('index.html', result_rot=result_rot, result_text=result_text)

@app.route('/hello')
def hello():
    """http://localhost:5000/hello
    very basic example how to route and return"""
    return 'Hello, World'

@app.route('/will_return_string')
def will_return_string():
    """http://localhost:5000/will_return_string
    will_return_string() calls call_to_basic_function"""
    return call_to_basic_function()
def call_to_basic_function():
    """will_return_string() calls call_to_basic_function"""
    return basic_external_method_example('will return this string')

@app.route('/will_return_given/<given>')
def will_return_given(given):
    """http://localhost:5000/will_return_given/here it is
    http://localhost:5000/will_return_given/here%20it%20is
    OUTPUT: User here it is"""
    return 'User %s' % given

@app.route('/strings')
def strings():
    """http://localhost:5000/strings"""
    text = 'guten tag'
    return basic_external_method_example(text)

@app.route('/integers')
def integers():
    """http://localhost:5000/integers
    without type conversion to str -> NameError: name 'rot' is not defined"""
    rot = str(11)
    return basic_external_method_example(rot)

@app.route('/cat')
def cat():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <p>Hello, It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
