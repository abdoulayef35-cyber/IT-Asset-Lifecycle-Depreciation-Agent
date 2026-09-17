from datetime import date, datetime, timedelta

EOL_WARNING_DAYS = 90
WARRANTY_WARNING_DAYS = 90

def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()

def calculate_eol_date(purchase_date, useful_life_years):
    days = useful_life_years * 365.25
    return purchase_date + timedelta(days=days)

def classify(days_remaining, warning_days):
    if days_remaining < 0:
        return "past"
    elif days_remaining <= warning_days:
        return "near"
    else:
        return "active"

def get_lifecycle_flags(asset, today=None):
    if today is None:
        today = date.today()


    purchase_date = parse_date(asset["purchase_date"])
    useful_life_years = float(asset["useful_life_years"])
    eol_date = calculate_eol_date(purchase_date, useful_life_years)
    days_until_eol = (eol_date - today).days
    eol_status = classify(days_until_eol, EOL_WARNING_DAYS)

    warranty_end_date = parse_date(asset["warranty_end_date"])
    days_until_warranty = (warranty_end_date - today).days
    warranty_status = classify(days_until_warranty, WARRANTY_WARNING_DAYS)

    return {
        "asset_id": asset["asset_id"],
        "eol_date": eol_date,
        "days_until_eol": days_until_eol,
        "eol_status": eol_status,
        "warranty_end_date": warranty_end_date,
        "days_until_warranty_expiration": days_until_warranty,
        "warranty_status": warranty_status,
    }

if __name__ == "__main__":
    from depreciation import load_assets

    assets = load_assets("data/asset_register.csv")
    for asset in assets:
        flags = get_lifecycle_flags(asset)
        if flags["eol_status"] != "active" or flags["warranty_status"] != "active":
            print(asset["asset_id"], "-", asset["description"])
            print("  ", flags)