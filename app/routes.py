from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Task, Comment
from app.forms import RegistrationForm, LoginForm, TaskForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Registro', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.tasks'))
        else:
            flash('Inicio de sesión fallido. Revisa el correo electrónico y la contraseña', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, author=current_user,
                    due_date=form.due_date.data, priority=form.priority.data)
        db.session.add(task)
        db.session.commit()
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('main.tasks'))
    return render_template('create_task.html', title='Nueva Tarea', form=form, legend='Nueva Tarea')

@main.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, task=task)
        db.session.add(comment)
        db.session.commit()
        flash('Comentario agregado', 'success')
        return redirect(url_for('main.task', task_id=task.id))
    return render_template('task.html', title=task.title, task=task, form=form)

@main.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        db.session.commit()
        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('main.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content
        form.due_date.data = task.due_date
        form.priority.data = task.priority
    return render_template('create_task.html', title='Actualizar Tarea', form=form, legend='Actualizar Tarea')

@main.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada exitosamente', 'success')
    return redirect(url_for('main.tasks'))

@main.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.filter_by(author=current_user)
    return render_template('tasks.html', tasks=tasks)
