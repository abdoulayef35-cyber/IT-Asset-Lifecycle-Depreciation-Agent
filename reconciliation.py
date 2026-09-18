from depreciation import load_assets, get_book_value_as_of

def reconcile(register_assets, count_assets):
    register_by_id = {asset["asset_id"]: asset for asset in register_assets}
    count_by_id = {asset["asset_id"]: asset for asset in count_assets}

    register_ids = set(register_by_id.keys())
    count_ids = set(count_by_id.keys())

    ghost_ids = register_ids - count_ids
    unrecorded_ids = count_ids - register_ids

    ghost_assets = []
    for asset_id in ghost_ids:
        asset = register_by_id[asset_id]
        ghost_assets.append({
            "asset_id": asset_id,
            "description": asset["description"],
            "book_value_at_risk": get_book_value_as_of(asset),
        })

    unrecorded_assets = []
    for asset_id in unrecorded_ids:
        asset = count_by_id[asset_id]
        unrecorded_assets.append({
            "asset_id": asset_id,
            "description": asset["description"],
            "location": asset["location"],
            "count_date": asset["count_date"],
        })
    return {
        "ghost_assets": ghost_assets,
        "unrecorded_assets": unrecorded_assets,
    }

if __name__ == "__main__":
    register_assets = load_assets("data/asset_register.csv")
    count_assets = load_assets("data/physical_count.csv")

    results = reconcile(register_assets, count_assets)

    print("GHOST ASSETS (on the books, not found):")
    for asset in results["ghost_assets"]:
        print("  ", asset)

    print("\nUNRECORDED ASSETS (found, not on the books):")
    for asset in results["unrecorded_assets"]:
        print("  ", asset)