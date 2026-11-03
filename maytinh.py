from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
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

    return render_template('maytinh/maytinh.html', 
                           a=a_raw, 
                           b=b_raw, 
                           op=op, 
                           error_a=error_a, 
                           error_b=error_b, 
                           error_op=error_op, 
                           result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)