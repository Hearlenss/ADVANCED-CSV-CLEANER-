import csv
import re
import json
import os
from datetime import datetime
from openpyxl import Workbook
1

# =========================
# ALIAS & KORUMA
# =========================

FIELD_ALIASES = {
    "name": [
        "name", "username", "fname", "full_name", "cnic", "studentname"
    ],
    "email": [
        "email", "mail", "useremail", "normalized_email"
    ],
    "phone": [
        "phone", "cell", "cell_no", "mobile", "mobile_no",
        "contact", "usermobile"
    ],
    "title": [
        "title", "qualification", "program", "degree",
        "userprogram", "ftitle"
    ],
    "date": [
        "date", "datetime", "year", "fyear",
        "created", "registered"
    ]
}

BLOCKED_FOR_NAME = ["father", "parent", "guardian"]


def detect_columns(headers):
    colmap = {}
    for key, aliases in FIELD_ALIASES.items():
        for h in headers:
            if not h:
                continue

            hl = h.lower()

            if key == "name" and any(b in hl for b in BLOCKED_FOR_NAME):
                continue

            if any(a in hl for a in aliases):
                colmap[key] = h
                break
    return colmap


def auto_output_names(input_file):
    base = os.path.basename(input_file)
    name, _ = os.path.splitext(base)
    return (
        f"{name}_clean.csv",
        f"{name}_clean.json",
        f"{name}_clean.log",
        f"{name}_clean.xlsx"
    )


# =========================
# VALIDATION
# =========================

def is_valid_email(email):
    if not email:
        return False
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(email)) is not None


def normalize_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits if 10 <= len(digits) <= 15 else ""


def is_valid_url(url):
    if not url:
        return True
    return re.match(
        r'^(https?://)?([\w\-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$',
        str(url)
    ) is not None


def normalize_date(date_str):
    if not date_str:
        return ""
    for fmt in ("%Y%m%d%H%M%S", "%Y-%m-%d", "%d/%m/%Y", "%Y"):
        try:
            return datetime.strptime(str(date_str), fmt).strftime("%Y-%m-%d")
        except:
            continue
    return ""


# =========================
# EXCEL EXPORT
# =========================

def write_excel(output_xlsx, headers, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cleaned Data"

    ws.append(headers)

    for row in rows:
        ws.append([row.get(h, "") for h in headers])

    wb.save(output_xlsx)


# =========================
# CORE CLEANER
# =========================

def clean_single_csv(input_file, output_csv, output_json, log_file, output_xlsx):
    cleaned_rows = []
    seen = set()
    logs = []
    headers_union = set()

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            logs.append("Empty or invalid CSV")
            return

        headers_union.update(h for h in reader.fieldnames if h)
        colmap = detect_columns(reader.fieldnames)

        for idx, row in enumerate(reader, start=1):
            row = {k: v for k, v in row.items() if k}

            name  = row.get(colmap.get("name", ""), "").strip()
            email = row.get(colmap.get("email", ""), "").strip()
            phone = row.get(colmap.get("phone", ""), "")
            title = row.get(colmap.get("title", ""), "")
            date  = row.get(colmap.get("date", ""), "")

            if not name:
                logs.append(f"Row {idx}: missing name")
                continue

            if email and not is_valid_email(email):
                logs.append(f"Row {idx}: invalid email")
                continue

            phone_norm = normalize_phone(phone)
            date_norm  = normalize_date(date)

            for k in row:
                if any(x in k.lower() for x in ["url", "link", "website", "photo", "profile"]):
                    if not is_valid_url(row[k]):
                        row[k] = ""
                        logs.append(f"Row {idx}: bad url cleaned ({k})")

            uniq = (name.lower(), email.lower() if email else phone_norm)
            if uniq in seen:
                continue
            seen.add(uniq)

            row["normalized_name"]  = name
            row["normalized_email"] = email or ""
            row["normalized_phone"] = phone_norm
            row["normalized_title"] = title or ""
            row["normalized_date"]  = date_norm

            cleaned_rows.append(row)

    headers = sorted(headers_union | {
        "normalized_name",
        "normalized_email",
        "normalized_phone",
        "normalized_title",
        "normalized_date"
    })

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(cleaned_rows)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(cleaned_rows, f, indent=4, ensure_ascii=False)

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    write_excel(output_xlsx, headers, cleaned_rows)

    print(f"✔ {input_file} → {len(cleaned_rows)} kayıt")


# =========================
# UI
# =========================

def print_logo():
    print(r"""
╔════════════════════════════════════════════════════╗
║                                                    ║
║        █████╗ ███╗   ██╗██╗  ██╗ █████╗            ║
║       ██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗           ║
║       ███████║██╔██╗ ██║█████╔╝ ███████║           ║
║       ██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║           ║
║       ██║  ██║██║ ╚████║██║  ██╗██║  ██║           ║
║       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝           ║
║                                                    ║
║     ANKA TEAM – ADVANCED CSV CLEANER v2.3          ║
║     Schema-Agnostic Data Engine                    ║
║                                                    ║
╚════════════════════════════════════════════════════╝
""")


def print_menu():
    print("┌──────────────────────────────────────────┐")
    print("│                ANA MENÜ                  │")
    print("├──────────────────────────────────────────┤")
    print("│  [1] CSV Temizle (Tek / Çoklu)           │")
    print("│  [2] Çıkış                               │")
    print("└──────────────────────────────────────────┘")


if __name__ == "__main__":
    print_logo()
    print_menu()

    if input("\nSeçiminiz ➜ ").strip() == "1":
        files = [f.strip() for f in input("\nCSV yolları (virgül): ").split(",") if f.strip()]

        for file in files:
            if not file.lower().endswith(".csv"):
                print(f"⚠ Atlandı: {file}")
                continue

            if not os.path.exists(file):
                print(f"✖ Bulunamadı: {file}")
                continue

            out_csv, out_json, out_log, out_xlsx = auto_output_names(file)

            clean_single_csv(
                file,
                out_csv,
                out_json,
                out_log,
                out_xlsx
            )

    else:
        print("Çıkılıyor…")
