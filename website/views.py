from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db, admin, app
from .models import Inventory, User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView

admin.add_view(ModelView(Inventory, db.session))
admin.add_view(ModelView(User, db.session))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if(username == 'admin') and (password == 'admin'):
            flash('Logged in success!')
            login_user(user, remember=True)
            return redirect(url_for('inventory'))
        else: 
            flash('Logged in failed!')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/inventory')
@login_required
def inventory():
    data = Inventory.query.all()
    headings = ("Product Name", "Product Code", "Quantity", "Description", "Actions")
    return render_template('inventory.html', data=data, headings=headings)

@app.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        
        print(request.form)
        desc = request.form['desc']
        name = request.form['name']
        code = request.form['code']
        quantity = request.form['quantity']

        item = Inventory(name, desc, quantity, code)
        db.session.add(item)
        db.session.commit()

        flash("Item added!")

        return redirect(url_for('inventory'))

@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        item = Inventory.query.get(request.form.get('id'))

        item.description = request.form['desc']
        item.name = request.form['name']
        item.code = request.form['code']
        item.quantity = request.form['quantity']

        flash("Item edited!")
        db.session.commit()

        return redirect(url_for('inventory'))

@app.route('/delete', methods = ['GET', 'POST'])
@login_required
def delete():
    item = Inventory.query.get(request.form.get('id'))
    item.deleted = True
    item.deletion_comment = request.form['del_com']
    db.session.commit()
    flash("Item deleted")

    return redirect(url_for('inventory'))

@app.route('/deleted', methods = ['GET', 'POST'])
@login_required
def deleted():
    
    if request.method == 'POST':
        item = Inventory.query.get(request.form.get('id'))
        item.deleted = False
        item.deletion_comment = "n/a"
        db.session.commit()
        flash("Item restored")

    data = Inventory.query.all()
    headings = ("Product Name", "Product Code", "Quantity", "Description", "Deletion Comment", "Actions")
    return render_template('deleted_inventory.html', data=data, headings=headings)  
