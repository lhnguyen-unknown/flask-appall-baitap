from flask import Flask, jsonify, url_for
from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
  regex = r"-?\d+(?:,-?\d+)*"

  def to_python(self, value):
    return [int(x) for x in value.split(",")]

  def to_url(self, value):
    return ",".join(str(x) for x in value)


app = Flask(__name__)

app.url_map.converters["list"] = ListConverter


@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
  return "Hello, World!"


@app.route("/chia-nhom")
def chia_nhom():
  so_bai = 12
  so_nhom = 0
  return f"Mỗi nhóm làm {so_bai / so_nhom} bài"


@app.route("/user/<username>")
def uses_profile(username):
  rs = f"Xin chào bạn: {username}"
  return rs


@app.route("/square/<float:x>")
def square(x):
  rs = f"Bình phương của {x} la {x * x}"
  return rs


@app.route("/sum/<list:numbers>", endpoint="sum_numbers")
def sum_numbers(numbers):
  return jsonify({"numbers": numbers, "sum": sum(numbers)})


if __name__ == "__main__":
  app.run(debug=True, port=8000)