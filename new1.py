import csv
import psycopg2
from datetime import datetime

DB_HOST = "localhost"
DB_NAME = "balot_new"
DB_USER = "tanishq"
DB_PASS = "tanishq"

CSV_FILE_PATH = r"C:\Users\admin\Downloads\balots_new.csv"

COLUMNS = [
    'ba_index', 'charg', 'thinavgbodywt', 'thinnedea', 'thinnedkg', 'thindate',
    'liftqtyea', 'liftqtykg', 'balancebirds', 'fieldfcr', 'balancebirdskg', 'liftper',
    'bodyweight', 'lotclosedate', 'liftinggap', 'currentage', 'lastliftdt', 'firstliftdt',
    'status', 'ernam', 'erdat', 'erzeit', 'relernam', 'relerdat', 'relerzeit', 'chickdate',
    'zregion', 'last5lotgrade', 'linesupervisor', 'ecshed', 'shedtext', 'regiontext',
    'branch', 'branchtext', 'lgort', 'lgorttext', 'partner', 'farmername', 'hplant',
    'hplanttext', 'liftcount', 'liftnocount', 'hatchdate', 'zmeanage', 'curlotclosedate',
    'grade', 'costshtdt', 'settledt', 'zfcr', 'chickqty', 'stodate', 'stoqty', 'b1consumed',
    'b2consumed', 'b3consumed', 'chicksconsumed', 'chicksreceipt', 'chickstransitmort',
    'chickstransitshortfinal', 'downtimedays', 'chickmort', 'zshortqty', 'fieldvalue',
    'notif', 'farmerchikmort', 'bresult', 'remarks', 'bizone', 'bizonetext', 's_name',
    'p_code', 'p_name', 'age_group'
]

def convert_value(value, colname):
    value = value.strip()
    if value == "":
        return None

    try:
        if "date" in colname.lower() or colname.lower().endswith("dt"):
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            return None

        elif any(x in colname.lower() for x in ["qty", "count", "age", "gap", "days"]):
            return int(float(value))

        elif any(x in colname.lower() for x in
                 ["fcr", "bodywt", "wt", "kg", "per", "mean", "value", "mort", "consumed", "short", "zfcr"]):
            return float(value)

        elif colname.lower() == "bresult":
            if value.lower() in ("true", "yes", "1"):
                return True
            elif value.lower() in ("false", "no", "0"):
                return False
            else:
                return None

        else:
            return value

    except Exception:
        return None

def convert_row(row, headers):
    return tuple(convert_value(v, h) for v, h in zip(row, headers))

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database='balot_new',
        user='tanishq',
        password='tanishq'
    )
    cur = conn.cursor()
    print("Connected to database")

    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)

        if header and len(header) != len(COLUMNS):
            print(f"CSV column count ({len(header)}) doesn't match expected ({len(COLUMNS)}). Check headers!")

        for idx, row in enumerate(reader, start=2):
            if not any(row):
                continue

            data_tuple = convert_row(row, COLUMNS)

            try:
                placeholders = ','.join(['%s'] * len(COLUMNS))
                cur.execute(f"CALL insert_data({placeholders});", data_tuple)
                conn.commit()
            except Exception as inner_e:
                print(f"Skipped row {idx} due to error: {inner_e}")
                conn.rollback()

    print("Data import completed successfully!")

except Exception as e:
    print("Fatal error:", e)
    if conn:
        conn.rollback()

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Connection closed.")
