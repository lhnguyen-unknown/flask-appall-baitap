from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def sodiem():
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

    return render_template('hocphan/hocphan.html',
                           cc=cc_raw,
                           gk=gk_raw,
                           ck=ck_raw,
                           error_cc=error_cc,
                           error_gk=error_gk,
                           error_ck=error_ck,
                           result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)