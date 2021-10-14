from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///basic.sqlite"
db = SQLAlchemy(app)


class Grocerry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocerry(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."
    else:
        groceries = Grocerry.query.order_by(Grocerry.created_at).all()
        return render_template('home.html', groceries=groceries)


@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocerry.query.get_or_404(id)
    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocerry.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data"
    else:
        title = 'Update Data'
        return render_template('update.html', title=title, grocery=grocery)


@app.route('/contact/')
def contact_page():
    return 'Call me 512-673-9650'


@app.route('/about/')
def about():
    return 'My About page'


if __name__ == '__main__':
    app.run()
