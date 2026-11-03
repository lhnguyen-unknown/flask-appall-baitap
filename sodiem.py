from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    redirect,
    render_template_string,
    request,
    url_for,
)

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {
        "name": "nguyễn văn an",
        "lop": "k47a",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0},
    },
    "23T1020002": {
        "name": "trần thị bình",
        "lop": "k47a",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0},
    },
    "23T1020003": {
        "name": "lê hoàng cường",
        "lop": "k47b",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0},
    },
    "23T1020004": {
        "name": "phạm minh dũng",
        "lop": "k47b",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0},
    },
    "23T1020005": {"name": "hoàng thu hà", "lop": "k47a", "scores": {}},
    "23T1020006": {
        "name": "võ quốc khánh",
        "lop": "k47c",
        "scores": {"PMMNM": 7.5, "MMT": 8.0},
    },
}


def calculate_grade(scores):
  if not scores:
    return None, "-"
  avg_score = round(sum(scores.values()) / len(scores), 2)
  if avg_score >= 8.5:
    rank = "Xuất sắc/Giỏi"
  elif avg_score >= 7.0:
    rank = "Khá"
  elif avg_score >= 5.0:
    rank = "Trung bình"
  else:
    rank = "Yếu/Kém"
  return avg_score, rank


@app.route("/")
def home():
  total_students = len(STUDENTS)
  classes = set(s["lop"] for s in STUDENTS.values())
  total_classes = len(classes)

  html = """
    <h1>Trang chủ</h1>
    <p>Tổng số sinh viên: <strong>{{ total_students }}</strong></p>
    <p>Tổng số lớp: <strong>{{ total_classes }}</strong></p>

    <form action="{{ url_for('search') }}" method="get">
        <input type="text" name="q" placeholder="Nhập tên hoặc MSSV..." required>
        <button type="submit">Tìm kiếm</button>
    </form>
    <br>

    <ul>
        <li><a href="{{ url_for('student_list') }}">Xem danh sách sinh viên (/students)</a></li>
        <li><a href="{{ url_for('api_students') }}">API sinh viên (/api/students)</a></li>
    </ul>
    """
  return render_template_string(
      html, total_students=total_students, total_classes=total_classes
  )


@app.route("/api/students")
def api_students():
  return jsonify(STUDENTS)


@app.route("/students")
def student_list():
  selected_lop = request.args.get("lop", "").strip()
  all_classes = sorted(list(set(s["lop"] for s in STUDENTS.values())))

  filtered_students = []
  for mssv, info in STUDENTS.items():
    avg_score, rank = calculate_grade(info["scores"])

    student_data = {
        "mssv": mssv,
        # Sử dụng filter |title để viết hoa chữ cái đầu mỗi từ cho tên và lớp
        "name": info["name"],
        "lop": info["lop"],
        "avg_score": avg_score if avg_score is not None else "-",
        "rank": rank,
    }

    if selected_lop:
      if info["lop"].lower() == selected_lop.lower():
        filtered_students.append(student_data)
    else:
      filtered_students.append(student_data)

  html = """
    <h2>Danh sách sinh viên</h2>
    
    <div>
        <strong>Lọc theo lớp: </strong>
        <a href="{{ url_for('student_list') }}">Tất cả</a> | 
        {% for c in all_classes %}
            <!-- Dùng filter |upper cho tên lớp -->
            <a href="{{ url_for('student_list', lop=c) }}">{{ c|upper }}</a> {% if not loop.last %}|{% endif %}
        {% endfor %}
    </div>
    <br>

    {% if filtered_students %}
    <table border="1" cellpadding="8" cellspacing="0">
        <thead>
            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm TB</th>
                <th>Xếp loại</th>
            </tr>
        </thead>
        <tbody>
            {% for s in filtered_students %}
            <tr>
                <td><a href="{{ url_for('student_detail', mssv=s.mssv) }}">{{ s.mssv }}</a></td>
                <!-- Dùng filter |title để tự động viết hoa tên sinh viên -->
                <td>{{ s.name|title }}</td>
                <!-- Dùng filter |upper để viết hoa mã lớp -->
                <td>{{ s.lop|upper }}</td>
                <td>{{ s.avg_score }}</td>
                <td>{{ s.rank }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <!-- Dùng filter |length để đếm số lượng sinh viên đang hiển thị -->
    <p><em>Hiển thị tổng cộng {{ filtered_students|length }} sinh viên trong danh sách.</em></p>
    {% else %}
        <p><strong>Không có sinh viên phù hợp.</strong></p>
    {% endif %}
    <br>
    <a href="{{ url_for('home') }}">Trở về trang chủ</a>
    """
  return render_template_string(
      html,
      filtered_students=filtered_students,
      all_classes=all_classes,
      selected_lop=selected_lop,
  )


@app.route("/students/<mssv>")
def student_detail(mssv):
  if mssv not in STUDENTS:
    abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

  student = STUDENTS[mssv]
  avg_score, rank = calculate_grade(student["scores"])
  display_avg = avg_score if avg_score is not None else "-"

  html = """
    <h2>Chi tiết sinh viên</h2>
    <p><strong>Họ và tên:</strong> {{ student.name|title }}</p>
    <p><strong>MSSV:</strong> {{ mssv }}</p>
    <p><strong>Lớp:</strong> <a href="{{ url_for('student_list', lop=student.lop) }}">{{ student.lop|upper }}</a></p>
    <p><strong>Điểm trung bình:</strong> {{ display_avg }}</p>
    <p><strong>Xếp loại:</strong> {{ rank }}</p>
    <p><strong>Link rút gọn:</strong> <a href="{{ url_for('short_student_detail', mssv=mssv) }}">{{ request.host_url[:-1] }}{{ url_for('short_student_detail', mssv=mssv) }}</a></p>

    <h3>Bảng điểm từng học phần:</h3>
    {% if student.scores %}
    <table border="1" cellpadding="8" cellspacing="0">
        <thead>
            <tr>
                <th>Học phần</th>
                <th>Điểm số</th>
            </tr>
        </thead>
        <tbody>
            {% for subject, score in student.scores.items() %}
            <tr>
                <td>{{ subject }}</td>
                <td>{{ score }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <br>
    <a href="{{ url_for('export_student_scores', mssv=mssv) }}">📥 Tải bảng điểm (CSV)</a>
    {% else %}
        <!-- Ví dụ dùng filter default nếu sinh viên không có ghi chú -->
        <p><strong>Ghi chú:</strong> {{ student.note|default("Sinh viên chưa có ghi chú nào.", boolean=true) }}</p>
        <p><em>Sinh viên này chưa có điểm học phần nào.</em></p>
    {% endif %}

    <br><br>
    <a href="{{ url_for('student_list') }}">← Quay lại danh sách sinh viên</a>
    """
  return render_template_string(
      html,
      mssv=mssv,
      student=student,
      display_avg=display_avg,
      rank=rank,
  )


@app.route("/sv/<mssv>")
def short_student_detail(mssv):
  return redirect(url_for("student_detail", mssv=mssv), code=301)


@app.route("/students/<mssv>/export")
def export_student_scores(mssv):
  if mssv not in STUDENTS:
    abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

  student = STUDENTS[mssv]
  csv_lines = ["hoc_phan,diem"]
  for subject, score in student["scores"].items():
    csv_lines.append(f"{subject},{score}")

  csv_data = "\n".join(csv_lines)

  response = make_response(csv_data)
  response.headers["Content-Type"] = "text/csv; charset=utf-8"
  response.headers["Content-Disposition"] = (
      f"attachment; filename=diem_{mssv}.csv"
  )

  return response


@app.route("/search")
def search():
  query = request.args.get("q", "")
  query_lower = query.lower()

  results = []
  if query:
    for mssv, info in STUDENTS.items():
      if query_lower in mssv.lower() or query_lower in info["name"].lower():
        results.append(
            {"mssv": mssv, "name": info["name"], "lop": info["lop"]}
        )

  html = """
    <h2>Tìm kiếm sinh viên</h2>
    
    <form action="{{ url_for('search') }}" method="get">
        <input type="text" name="q" value="{{ query }}" placeholder="Nhập tên hoặc MSSV...">
        <button type="submit">Tìm kiếm</button>
    </form>
    <br>

    {% if query %}
        <!-- Sử dụng filter |length để đếm số kết quả -->
        <p>Tìm thấy <strong>{{ results|length }}</strong> kết quả cho "<strong>{{ query }}</strong>"</p>
        
        {% if results %}
        <ul>
            {% for s in results %}
            <li>
                <a href="{{ url_for('student_detail', mssv=s.mssv) }}">{{ s.mssv }} - {{ s.name|title }}</a> (Lớp: {{ s.lop|upper }})
            </li>
            {% endfor %}
        </ul>
        {% endif %}
    {% endif %}

    <br>
    <a href="{{ url_for('home') }}">Trở về trang chủ</a>
    """
  return render_template_string(html, query=query, results=results)


if __name__ == "__main__":
  app.run(debug=True, port=8000)