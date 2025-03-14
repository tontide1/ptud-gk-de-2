from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from models import db, User, Task, Category
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dH7kJ9mN3pQ8vR4xL2yT5wC6bE1aZ0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

# Update the index route
@app.route('/dashboard')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all()
    return render_template('index.html', tasks=tasks, categories=categories)

# Update login route to redirect to dashboard after successful login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            if user.is_banned:
                flash('Your account has been banned.', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if username or email already exists
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
            
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')

        file = request.files['avatar']
        avatar_path = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            avatar_path = f'avatars/{filename}'

        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password']),
            avatar=avatar_path
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully!')
    
    # Get all categories and their associated tasks for the current user
    categories = Category.query.all()
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Create a dictionary of tasks grouped by category
    categorized_tasks = {}
    for category in categories:
        categorized_tasks[category] = [task for task in user_tasks if task.category_id == category.id]
    
    # Get tasks with no category
    uncategorized_tasks = [task for task in user_tasks if task.category_id is None]
    
    return render_template('categories.html', 
                         categories=categories, 
                         categorized_tasks=categorized_tasks,
                         uncategorized_tasks=uncategorized_tasks)

@app.route('/task/add', methods=['POST'])
@login_required
def add_task():
    # Get or create category
    category_name = request.form.get('category_name')
    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
    
    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        category_id=category.id if category_name else None,
        user_id=current_user.id,
        created=datetime.utcnow()  # Add creation date
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/update_category', methods=['POST'])
@login_required
def update_task_category(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id or current_user.is_admin:
        category_name = request.form.get('category_name')
        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()
            task.category_id = category.id
        else:
            task.category_id = None
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id or current_user.is_admin:
        task.status = request.form['status']
        if task.status == 'completed':
            task.finished = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id or current_user.is_admin:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            # Delete old avatar file if it exists
            if current_user.avatar:
                old_avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.avatar.split('/')[-1])
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
            
            # Save new avatar
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.avatar = f'avatars/{filename}'
            db.session.commit()
            flash('Avatar updated successfully!')
            return redirect(url_for('profile'))
    return render_template('profile.html')

# Add admin_required decorator definition
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:user_id>/change_password', methods=['POST'])
@login_required
@admin_required
def admin_change_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get('new_password')
    if new_password:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash(f'Password changed for user {user.username}', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/user/<int:user_id>/toggle_ban', methods=['POST'])
@login_required
@admin_required
def admin_toggle_ban(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = not user.is_banned
    db.session.commit()
    flash(f'User {user.username} {"banned" if user.is_banned else "unbanned"}', 'success')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
