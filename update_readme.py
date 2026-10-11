import json
import os
import re
from glob import glob

README_PATH = "README.md"

def find_latest_year_json():
    files = glob("headcounts_*.json")
    years = []
    for f in files:
        match = re.search(r"headcounts_(\d{4})\.json", f)
        if match:
            years.append((int(match.group(1)), f))
    if not years:
        raise FileNotFoundError("No headcount JSON files found (expected headcounts_YYYY.json).")
    years.sort(key=lambda x: x[0], reverse=True)
    return years[0]

def calculate_totals(rows):
    companies = ["google", "amazon", "microsoft", "apple", "meta", "adobe"]
    col_totals = {c: 0 for c in companies}
    has_plus = {c: False for c in companies}
    has_tilde = {c: False for c in companies}

    for row in rows:
        # compute row total if not given or to verify
        row_sum = 0
        row_has_plus = False
        row_has_tilde = False
        for c in companies:
            val_str = str(row.get(c, "—")).strip()
            if val_str in ["—", "-", ""]:
                continue
            if "+" in val_str:
                has_plus[c] = True
                row_has_plus = True
            if "~" in val_str:
                has_tilde[c] = True
                row_has_tilde = True
            num_match = re.search(r"[\d,]+", val_str)
            if num_match:
                num = int(num_match.group(0).replace(",", ""))
                col_totals[c] += num
                row_sum += num

        # Format row total if not explicitly provided or to update
        if "total" not in row or not row["total"]:
            prefix = "~" if row_has_tilde else ""
            suffix = "+" if row_has_plus else ""
            row["total"] = f"{prefix}{row_sum:,}{suffix}"

    total_sum = sum(col_totals.values())
    col_totals_formatted = {}
    for c in companies:
        prefix = "~" if has_tilde[c] else ""
        suffix = "+" if has_plus[c] else ""
        col_totals_formatted[c] = f"{prefix}{col_totals[c]:,}{suffix}"
    
    # overall grand total
    grand_prefix = "~" if any(has_tilde.values()) else ""
    grand_suffix = "+" if any(has_plus.values()) else ""
    col_totals_formatted["total"] = f"{grand_prefix}{total_sum:,}{grand_suffix}"

    return col_totals_formatted

def build_table_markdown(rows):
    col_totals = calculate_totals(rows)
    lines = [
        "| Tech Hub Region 📍 | Google 🔍 | Amazon 📦 | Microsoft 💻 | Apple 🍎 | Meta ♾️ | Adobe 🎨 | Row Total 📊 |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for row in rows:
        region_str = f"**{row['region']}**"
        if row.get("subtext"):
            region_str += f"<br>*{row['subtext']}*"
        if row.get("emoji"):
            region_str += f" {row['emoji']}"

        r_line = f"| {region_str} | {row.get('google', '—')} | {row.get('amazon', '—')} | {row.get('microsoft', '—')} | {row.get('apple', '—')} | {row.get('meta', '—')} | {row.get('adobe', '—')} | **{row.get('total')}** |"
        lines.append(r_line)

    col_line = f"| **Column Total** 📈 | **{col_totals['google']}** | **{col_totals['amazon']}** | **{col_totals['microsoft']}** | **{col_totals['apple']}** | **{col_totals['meta']}** | **{col_totals['adobe']}** | **{col_totals['total']}** |"
    lines.append(col_line)
    return "\n".join(lines)

def update_readme():
    latest_year, json_file = find_latest_year_json()
    print(f"Loading data for year {latest_year} from {json_file}...")
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    usa_table_md = build_table_markdown(data.get("usa", []))
    india_table_md = build_table_markdown(data.get("india", []))

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Replace USA table
    usa_pattern = r"(## 🇺🇸 USA Tech Hubs: Estimated Core Engineering & R&D 🚀\n\n)(.*?)(?=\n\n---|\Z)"
    readme_content = re.sub(usa_pattern, r"\1" + usa_table_md, readme_content, flags=re.DOTALL)

    # Replace India table
    india_pattern = r"(## 🇮🇳 India Tech Hubs: Estimated Core Engineering & R&D 💡\n\n)(.*?)(?=\n\n---|\Z)"
    readme_content = re.sub(india_pattern, r"\1" + india_table_md, readme_content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Successfully updated {README_PATH} using {json_file} (Year {latest_year}).")

if __name__ == "__main__":
    update_readme()
