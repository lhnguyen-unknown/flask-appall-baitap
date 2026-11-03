import re
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khoa_bi_mat_csrf_va_session'
app.permanent_session_lifetime = timedelta(days=7)
USERS = {
    "admin": "admin123",
    "an": "an123456"
}
class RegisterForm(FlaskForm):
    username = StringField(
        'Tên đăng nhập',
        validators=[
            DataRequired(message='Vui lòng nhập tên đăng nhập.'),
            Length(min=4, max=20, message='Độ dài từ 4 đến 20 ký tự.')
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message='Vui lòng nhập email.'),
            Email(message='Email không đúng định dạng.')
        ]
    )
    password = PasswordField(
        'Mật khẩu',
        validators=[
            DataRequired(message='Vui lòng nhập mật khẩu.'),
            Length(min=8, message='Mật khẩu tối thiểu 8 ký tự.')
        ]
    )
    confirm_password = PasswordField(
        'Nhập lại mật khẩu',
        validators=[
            DataRequired(message='Vui lòng xác nhận mật khẩu.'),
            EqualTo('password', message='Mật khẩu nhập lại không khớp.')
        ]
    )
    agree = BooleanField(
        'Tôi đồng ý với các điều khoản dịch vụ',
        validators=[
            DataRequired(message='Bạn phải đồng ý với điều khoản.')
        ]
    )
    submit = SubmitField('Đăng ký')

    def __init__(self, users_dict=None, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.users_dict = users_dict

    def validate_username(self, field):
        pattern = r'^[a-z0-9_]+$'
        if not re.match(pattern, field.data):
            raise ValidationError('Chỉ cho phép chữ thường không dấu, số và dấu gạch dưới (_).')
        if self.users_dict and field.data in self.users_dict:
            raise ValidationError('Tên đăng nhập đã được sử dụng.')
def validate_score(val_str, name_vi):
    if not val_str:
        return None, 'Trống'
    try:
        val = float(val_str.replace(',', '.'))
    except ValueError:
        return None, f'Lỗi ô {name_vi}: Vui lòng nhập một số.'
    
    if val < 0 or val > 10:
        return None, f'Lỗi ô {name_vi}: Điểm phải từ 0 đến 10.'
    return val, ''
@app.route('/bai1', methods=['GET', 'POST'])
def bai1():
    a_raw = ''
    b_raw = ''
    op = '+'
    error_a = ''
    error_b = ''
    error_op = ''
    result = ''

    if request.method == 'POST':
        a_raw = request.form.get('a', '').strip()
        b_raw = request.form.get('b', '').strip()
        op = request.form.get('op', '+')

        a_val = None
        if not a_raw:
            error_a = 'Trống'
        else:
            try:
                a_val = float(a_raw.replace(',', '.'))
            except ValueError:
                error_a = 'Lỗi ô a: Vui lòng nhập một số.'

        b_val = None
        if not b_raw:
            error_b = 'Trống'
        else:
            try:
                b_val = float(b_raw.replace(',', '.'))
            except ValueError:
                error_b = 'Lỗi ô b: Vui lòng nhập một số.'

        if not a_raw and not b_raw:
            error_a = 'Trống'
            error_b = 'Lỗi cả hai ô'

        valid_ops = ['+', '-', '*', '/']
        if op not in valid_ops:
            error_op = 'Phép toán không hợp lệ.'

        if not error_a and not error_b and not error_op:
            if op == '/' and b_val == 0:
                error_b = 'Lỗi ô b: Không thể chia cho 0.'
            else:
                if op == '+':
                    res = a_val + b_val
                elif op == '-':
                    res = a_val - b_val
                elif op == '*':
                    res = a_val * b_val
                elif op == '/':
                    res = a_val / b_val

                res_display = int(res) if res.is_integer() else res
                a_display = int(a_val) if a_val.is_integer() else a_val
                b_display = int(b_val) if b_val.is_integer() else b_val

                result = f"{a_display} {op} {b_display} = {res_display}"

    return render_template('bai1.html', 
                           a=a_raw, 
                           b=b_raw, 
                           op=op, 
                           error_a=error_a, 
                           error_b=error_b, 
                           error_op=error_op, 
                           result=result)

@app.route('/bai2', methods=['GET', 'POST'])
def bai2():
    cc_raw = ''
    gk_raw = ''
    ck_raw = ''
    error_cc = ''
    error_gk = ''
    error_ck = ''
    result = ''

    if request.method == 'POST':
        cc_raw = request.form.get('cc', '').strip()
        gk_raw = request.form.get('gk', '').strip()
        ck_raw = request.form.get('ck', '').strip()

        if not cc_raw and not gk_raw and not ck_raw:
            error_cc = 'Trống'
            error_gk = 'Trống'
            error_ck = 'Lỗi cả 3 ô'
        else:
            cc_val, error_cc = validate_score(cc_raw, 'CC')
            gk_val, error_gk = validate_score(gk_raw, 'GK')
            ck_val, error_ck = validate_score(ck_raw, 'CK')

        if not error_cc and not error_gk and not error_ck:
            total = cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6
            total_rounded = round(total, 1)

            if ck_val < 1:
                letter = 'F (điểm thi dưới 1)'
            elif total_rounded >= 8.5:
                letter = 'A'
            elif total_rounded >= 7.0:
                letter = 'B'
            elif total_rounded >= 5.5:
                letter = 'C'
            elif total_rounded >= 4.0:
                letter = 'D'
            else:
                letter = 'F'

            result = f"{total_rounded} - {letter}"

    return render_template('bai2.html',
                           cc=cc_raw,
                           gk=gk_raw,
                           ck=ck_raw,
                           error_cc=error_cc,
                           error_gk=error_gk,
                           error_ck=error_ck,
                           result=result)

@app.route('/bai3', methods=['GET', 'POST'])
def bai3():
    height_raw = ''
    weight_raw = ''
    error_height = ''
    error_weight = ''
    result = ''
    alert_class = ''

    if request.method == 'POST':
        height_raw = request.form.get('height', '').strip()
        weight_raw = request.form.get('weight', '').strip()

        if not height_raw and not weight_raw:
            error_height = 'Trống'
            error_weight = 'Lỗi cả hai ô'
        else:
            height_val = None
            if not height_raw:
                error_height = 'Trống'
            else:
                try:
                    height_val = float(height_raw.replace(',', '.'))
                except ValueError:
                    error_height = 'Lỗi ô chiều cao: Vui lòng nhập một số.'

            weight_val = None
            if not weight_raw:
                error_weight = 'Trống'
            else:
                try:
                    weight_val = float(weight_raw.replace(',', '.'))
                except ValueError:
                    error_weight = 'Lỗi ô cân nặng: Vui lòng nhập một số.'

            if height_val is not None and not error_height:
                if height_val < 50 or height_val > 250:
                    error_height = 'Giá trị phải từ 50 đến 250.'

            if weight_val is not None and not error_weight:
                if weight_val < 10 or weight_val > 300:
                    error_weight = 'Lỗi ô cân nặng: Giá trị phải từ 10 đến 300.'

            if not error_height and not error_weight:
                h_m = height_val / 100.0
                bmi = weight_val / (h_m ** 2)
                bmi_rounded = round(bmi, 1)

                min_w = round(18.5 * (h_m ** 2), 1)
                max_w = round(22.9 * (h_m ** 2), 1)

                if bmi_rounded < 18.5:
                    status = 'Thiếu cân'
                    alert_class = 'alert-warning'
                elif bmi_rounded < 23.0:
                    status = 'Bình thường'
                    alert_class = 'alert-success'
                elif bmi_rounded < 25.0:
                    status = 'Thừa cân'
                    alert_class = 'alert-warning'
                else:
                    status = 'Béo phì'
                    alert_class = 'alert-danger'

                result = f"{bmi_rounded} - {status}; nên có {min_w} – {max_w} kg"

    return render_template('bai3.html',
                           height=height_raw,
                           weight=weight_raw,
                           error_height=error_height,
                           error_weight=error_weight,
                           result=result,
                           alert_class=alert_class)
@app.route('/dangki', methods=['GET', 'POST'])
def dangki():
    if 'user' in session:
        return redirect(url_for('bai1'))

    form = RegisterForm(users_dict=USERS)
    if form.validate_on_submit():
        USERS[form.username.data] = form.password.data
        flash('Đăng ký thành công.', 'success')
        return redirect(url_for('login'))

    return render_template('dangki.html', form=form)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('bai1'))

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
            return redirect(url_for('bai1'))
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
    return redirect(url_for('bai1'))

if __name__ == '__main__':
    app.run(debug=True, port=5004)