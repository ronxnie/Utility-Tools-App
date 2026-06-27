from datetime import date, datetime


def calculate_age(birth_date: str) -> dict:
    born = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    months = (today.year - born.year) * 12 + today.month - born.month
    if today.day < born.day:
        months -= 1
    days = (today - born).days
    return {"years": years, "months": months, "days": days}


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    monthly_rate = annual_rate / (12 * 100)
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        factor = (1 + monthly_rate) ** tenure_months
        emi = principal * monthly_rate * factor / (factor - 1)
    total = emi * tenure_months
    return {
        "emi": round(emi, 2),
        "total_payment": round(total, 2),
        "total_interest": round(total - principal, 2),
    }
