from flask import Flask, render_template, request, redirect, flash
import db
app = Flask('__name__')
app.config['SECRET_KEY'] ="super secret key"

db.vytvor()

@app.route('/', methods=['GET','POST'])
def start_page():
    return render_template('index.html')

@app.route('/generovani', methods=['GET','POST'])
def gen():
    if request.method == 'POST':
        db.generuj()
    return render_template('generovani.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    