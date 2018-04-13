from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


# Test to see if the python script is being called natively or from another program
# If called from another script, the __name__ environmental variable would not be __main__
if __name__ == "__main__":
    app.run(debug=True)
