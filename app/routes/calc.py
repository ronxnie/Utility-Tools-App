from flask import Blueprint, flash, render_template, request

from app.services.calculators import calculate_age, calculate_emi

calc_bp = Blueprint("calc", __name__)


@calc_bp.route("/age", methods=["GET", "POST"])
def age():
    birth_date = request.form.get("birth_date", "")
    result = None
    if request.method == "POST":
        try:
            result = calculate_age(birth_date)
        except Exception:
            flash("Enter a valid birth date.", "error")
    return render_template("tools/age.html", title="Age Calculator", birth_date=birth_date, result=result)


@calc_bp.route("/emi", methods=["GET", "POST"])
def emi():
    result = None
    values = {
        "principal": request.form.get("principal", "500000"),
        "rate": request.form.get("rate", "8.5"),
        "months": request.form.get("months", "60"),
    }
    if request.method == "POST":
        try:
            result = calculate_emi(float(values["principal"]), float(values["rate"]), int(values["months"]))
        except Exception:
            flash("Enter valid EMI inputs.", "error")
    return render_template("tools/emi.html", title="EMI Calculator", values=values, result=result)
