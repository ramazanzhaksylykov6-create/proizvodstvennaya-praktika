from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1909@localhost/praktika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))

@app.route('/')
def mainmenu():
    return render_template('mainmenu.html')

@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@app.route('/contacts')
def show_contacts():           # ← имя функции может быть любым
    return render_template(' contacts.html')

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    return redirect('/catalog')

@app.route('/cart')
def cart():
    items = []
    total = 0
    for pid in session.get('cart', []):
        p = Product.query.get(pid)
        if p:
            items.append(p)
            total += p.price
    return render_template('cart.html', cart_items=items, total=total)

@app.route('/remove/<int:pid>', methods=['POST'])
def remove(pid):
    cart = session.get('cart', [])
    if pid in cart:
        cart.remove(pid)
        session['cart'] = cart
    return redirect('/cart')

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ВСЁ, что выше — оставляем как есть
# Ниже — запуск сервера (должно быть в самом конце файла!)
if __name__ == '__main__':
    app.run(debug=True, port=5001)