import pandas as pd

def write_json_to_excel(data: dict, output_path: str):
    flat_data = {}  # merged dict for single-row underwriting data
    rent_roll_df = None

    for section_name, section_data in data.items():
        if section_name == "RENT ROLL & UNIT MIX":
            rent_roll = section_data.get("Rent Roll")
            if isinstance(rent_roll, list):
                rent_roll_df = pd.DataFrame(rent_roll)
        elif isinstance(section_data, dict):
            for k, v in section_data.items():
                # Flatten into top-level keys like "Property Name", "Cap Rate"
                flat_data[k] = v

    # Write main underwriting data to one sheet
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame([flat_data]).to_excel(writer, sheet_name="Underwriting Data", index=False)

        # Write Rent Roll to its own sheet if available
        if rent_roll_df is not None:
            # Normalize headers
            rent_roll_df.columns = [col.strip().capitalize().replace(" #", " Number").replace("#", "Number").replace("_", " ") for col in rent_roll_df.columns]
            rent_roll_df.to_excel(writer, sheet_name="Rent Roll", index=False)

    print(f"[📊] Excel file saved to: {output_path}")