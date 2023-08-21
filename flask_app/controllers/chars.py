from flask_app import app
from flask_app.models.char import Char
from flask_app.models.user import User
from flask import render_template, redirect, request, session

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data) , all_chars=Char.get_all())

@app.route('/chars/new')
def new_char():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    return render_template('char_new.html', user=User.get_by_id(data))

@app.route('/chars/new/create/fighter', methods=['POST'])
def create_new_char_fighter():
    if 'user_id' not in session:
        return redirect('/')
    if not Char.validate_char(request.form):
        return redirect('/chars/new')
    if 'user_id' not in session:
        return redirect('/')
    Char.create_char_fighter(request.form)
    return redirect('/chars/new/race')

@app.route('/chars/new/race')
def create_new_race():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    Char.create_char_race(request.form)
    return render_template('char_new_race.html', user=User.get_by_id(data),char=Char.get_one_char_by_id(data))

@app.route('/chars/new/choose/race', methods=['POST'])
def choose_new_char_race():
    # if 'user_id' not in session:
    #     return redirect('/')
    # if not Char.validate_char(request.form):
    #     return redirect('/chars/new')
    data ={
        'id': session['user_id']
    }
    Char.choose_char_race(request.form)
    return redirect('/chars/new/fighter/fighter_options')

@app.route('/chars/new/fighter/fighter_options')
def choose_fighter_options():
    data ={
        'id': session['user_id']
    }
    return render_template('char_new_fighter.html', user=User.get_by_id(data), char=Char.get_one_char_by_id(data))
# @app.route('/chars/new/submit', methods=['POST'])
# def submit_char():
#     if 'user_id' not in session:
#         return redirect('/')
#     if not Char.validate_char(request.form):
#         return redirect('/chars/new')
#     Char.create_char(request.form)
#     return redirect('/dashboard')

@app.route('/chars/new/create/options', methods=['POST'])
def create_char_other_options():
    # if 'user_id' not in session:
    #     return redirect('/')
    # if not Char.validate_char(request.form):
    #     return redirect('/chars/new')
    Char.create_char_options(request.form)
    return redirect('/chars/show/<int:id>')

@app.route('/chars/show/<int:id>')
def show_char(id):
    # if 'user_id' not in session:
    #     return redirect('/')
    data={
        'id':id
    }
    return render_template('char_show.html',char=Char.get_one_char(data), user=User.get_by_id(data))

@app.route('/chars/edit/<int:id>')
def edit_char(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('char_edit.html',char=Char.get_one_char_by_id(data), user=User.get_by_id(id))

@app.route('/chars/edit/submit', methods=['POST'])
def edit_submit_char():
    Char.update_char(request.form)
    return redirect(f"/chars/show/{request.form['id']}")

@app.route('/chars/delete/<int:id>')
def delete_char(id):
    if 'user_id' not in session:
        return redirect('/')

    Char.delete_char({'id':id})
    return redirect('/dashboard')