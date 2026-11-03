from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khoa_bi_mat_csrf_va_session'
app.permanent_session_lifetime = timedelta(days=7)

USERS = {
    "admin": "admin123",
    "an": "an123456"
}

@app.route('/')
def index():
    return render_template('indexlogin.html')

@app.route('/dangki', methods=['GET', 'POST'])
def dangki():
    if 'user' in session:
        return redirect(url_for('index'))

    form = RegisterForm(users_dict=USERS)
    if form.validate_on_submit():
        USERS[form.username.data] = form.password.data
        flash('Đăng ký thành công.', 'success')
        return redirect(url_for('login'))

    return render_template('dangki.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))

    username = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember')

        if not username or not password:
            flash('Sai tên đăng nhập hoặc mật khẩu.', 'danger')
            return render_template('login.html', username=username)

        if username in USERS and USERS[username] == password:
            session['user'] = username
            session.permanent = bool(remember)
            flash(f'Đăng nhập thành công. Xin chào {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu.', 'danger')
            return render_template('login.html', username=username)

    return render_template('login.html', username=username)

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Vui lòng đăng nhập...', 'warning')
        return redirect(url_for('login'))
    return render_template('profile.html', user=session['user'])

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5004)