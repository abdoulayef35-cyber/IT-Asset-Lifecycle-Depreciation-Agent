import csv
from datetime import date, datetime

def parse_currency(value):
    return float(str(value).replace(",", "").replace("$", ""))

def load_assets(filepath):
    assets = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["asset_id"]:
                assets.append(row)
    return assets

def calculate_schedule(asset):
    cost = parse_currency(asset["cost"])
    salvage_value = parse_currency(asset["salvage_value"])
    useful_life_years = float(asset["useful_life_years"])
    annual_depreciation = (cost - salvage_value) / useful_life_years

    schedule = []
    accumulated = 0.0
    remaining_life = useful_life_years
    year = 1

    while remaining_life > 0:
        year_fraction = min(1.0, remaining_life)
        depreciation_expense = annual_depreciation * year_fraction
        accumulated += depreciation_expense
        book_value = max(cost - accumulated, salvage_value)

        schedule.append({
            "year": year,
            "depreciation_expense": round(depreciation_expense, 2),
            "accumulated_depreciation": round(accumulated, 2),
            "book_value": round(book_value, 2),
        })

        remaining_life -= year_fraction
        year += 1


    return schedule

def get_book_value_as_of(asset, as_of_date=None):
    if as_of_date is None:
        as_of_date = date.today()

    cost = parse_currency(asset["cost"])
    salvage_value = parse_currency(asset["salvage_value"])
    useful_life_years = float(asset["useful_life_years"])
    purchase_date = datetime.strptime(asset["purchase_date"], "%Y-%m-%d").date()

    days_elapsed = (as_of_date - purchase_date).days
    years_elapsed = min(days_elapsed / 365.25, useful_life_years)

    annual_depreciation = (cost - salvage_value) / useful_life_years
    accumulated = annual_depreciation * years_elapsed
    book_value = max(cost - accumulated, salvage_value)

    return round(book_value, 2)

if __name__ == "__main__":
    assets = load_assets("data/asset_register.csv")
    for asset in assets:
        print(asset["asset_id"], "-", asset["description"])
        for row in calculate_schedule(asset):
            print("  ", row)