from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lukasfontanilla:LifeofRicee69@localhost:5432/smedb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Potluck(db.Model):
    __tablename__ = 'potluck'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    item = db.Column(db.String(200))
    deetz = db.Column(db.String(200))

    def __init__(self, name, item, deetz):
        self.name = name
        self.item = item
        self.deetz = deetz

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random')
def random():
    return render_template('random.html')

@app.route('/submit', methods=['POST'])
def submit():
  if request.method == 'POST':
      name = request.form['Name']
      item = request.form['Items']
      deetz = request.form['dish_deetz']
      print(name,item,deetz)
      if name == '' or item == '':
          return render_template('index.html', message="Please enter fields")
      if db.session.query(Potluck).filter(Potluck.name == name).count() == 0:
          data = Potluck(name, item, deetz)
          db.session.add(data)
          db.session.commit()
          return render_template('index.html')
      return render_template('index.html', message="Ypu have already submitted your potluck deetz")

     


if __name__ == '__main__':
    app.run()