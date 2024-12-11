from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)
# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/povvisot")

# Test the connection
connection = engine.connect()


@app.route('/')
@app.route('/product')
def crud():
    result = connection.execute(text("SELECT * FROM product"))
    return render_template('product.html', data=result)


@app.route('/submit1', methods=['POST'])
def submit1():
    # Get form values
    name = request.form.get('name')
    cost = request.form.get('cost')
    price = request.form.get('price')
    result = connection.execute(text(f"INSERT INTO `product` (Name, Cost, Price) VALUES ('{name}', {cost}, {price})"))
    connection.commit()
    return redirect('/product')


@app.route('/delete')
def delete():
    product_id = request.args.get('id')
    result = connection.execute(text(f"DELETE FROM product WHERE Id = {product_id}"))
    connection.commit()
    return redirect('/product')


@app.route('/edit')
def edit():
    product_id = request.args.get('id')
    result = connection.execute(text(f"SELECT * FROM product where Id = {product_id}"))
    data = []
    for product in result:
        data.append({
            'Id': product[0],
            'Name': product[1],
            'Cost': product[2],
            'Price': product[3]
        })
    return render_template('edit.html', product=data)


@app.route('/submit', methods=['POST'])
def submit():
    # Get form values
    name = request.form.get('name')
    cost = request.form.get('cost')
    price = request.form.get('price')
    product_id = request.form.get('id')

    result = connection.execute(
        text(f"UPDATE `product` SET Name = '{name}', Cost = {cost}, Price = {price} WHERE Id={product_id}"))
    connection.commit()

    # Redirect or return a response
    return redirect('/product')


if __name__ == '__main__':
    app.run()
