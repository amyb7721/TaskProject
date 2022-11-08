from MyProject import app,db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from MyProject.models import User, Task
from MyProject.forms import LoginForm, RegistrationForm, AddForm, DelForm


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

    return render_template('login.html',form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registeration')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_task():

    form=AddForm()

    if form.validate_on_submit():

        name = form.name.data

        new_task = Task(name)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('list_task'))

    return render_template('add.html', form=form)




@app.route('/list')
def list_task():

    task = Task.query.all()
    return render_template('list_task.html', task=task)


@app.route('/delete', methods=['GET', 'POST'])
def del_task():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        t = Task.query.get(id)
        db.session.delete(t)
        db.session.commit()

        return redirect(url_for('list_task'))
    return render_template('delete.html', form=form)





if __name__ == '__main__':
    app.run(debug=True, port=2000, host="localhost")
