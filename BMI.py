from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bmi():
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
                bmi_val = weight_val / (h_m ** 2)
                bmi_rounded = round(bmi_val, 1)

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

    return render_template('BMI/BMI.html',
                           height=height_raw,
                           weight=weight_raw,
                           error_height=error_height,
                           error_weight=error_weight,
                           result=result,
                           alert_class=alert_class)

if __name__ == '__main__':
    app.run(debug=True, port=5003)