from flask import Flask, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///basket.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc =  db.Column(db.String(500) , nullable = False)
    date_created =db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"  
 

@app.route("/", methods = ['GET','POST'])

def hello_world():
    if request.method == 'POST':
        print('post...')
        title = request.form['title']
        desc = request.form['desc']
        print(title)
    # return "<h2>Hello, World!</h2>"
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allitems = Todo.query.all()

    return render_template('index.html',allitems = allitems)

@app.route("/items")
def items():
    allitems = Todo.query.all()
    print(allitems)
    return "<h2>No items Here !</h2>"

@app.route("/delete/<int:sno>")
def delete(sno):
    ditem = Todo.query.filter_by(sno=sno).first()
    db.session.delete(ditem)
    db.session.commit()

    # print(allitems)
    return redirect('/')

@app.route("/edit/<int:sno>",methods = ['GET','POST'])
def edit(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        ditem = Todo.query.filter_by(sno=sno).first()
        ditem.title = title
        ditem.desc = desc
        db.session.add(ditem)
        db.session.commit()
        return redirect('/')

    ditem = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',ditem=ditem)  

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__": 
    with app.app_context():
        db.create_all()
    app.run(debug=True, port = 8000)
