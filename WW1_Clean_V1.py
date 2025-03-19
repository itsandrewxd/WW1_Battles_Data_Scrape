import pandas as pd
import re 
import numpy as np

df_ww1 = pd.read_csv('WW1_Battles_Detailed.csv', encoding="utf-8")
df_ww1_test = df_ww1.copy()

print(df_ww1["BattleName"].head())

def clean_date_str(date_str):
    """
    Remove text enclosed in square brackets [] or parentheses () and extra whitespace.
    """
    if pd.isnull(date_str):
        return ""
    # Remove anything between [] or ()
    cleaned = re.sub(r'[\[\(].*?[\]\)]', '', date_str)
    return cleaned.strip()

def parse_end_date(end_str, start_str=None):
    """
    Parse the end date.
    If the cleaned end date does not include any alphabetic characters (i.e. missing month info),
    then try to use the month (and year, if needed) from the corresponding start date.
    """
    cleaned_end = clean_date_str(end_str)
    
    # If the end date string contains letters, assume it has month info and parse normally.
    if re.search(r'[A-Za-z]', cleaned_end):
        return pd.to_datetime(cleaned_end, dayfirst=True, errors='coerce')
    
    # Otherwise, assume that the end date is missing month info.
    parts = re.findall(r'\d+', cleaned_end)
    if not parts:
        return pd.NaT
    day = int(parts[0])
    year = None
    if len(parts) > 1:
        try:
            year = int(parts[1])
            if year < 100:  # assume two-digit years are in the 1900s
                year += 1900
        except:
            pass
    
    # Use the start date to extract the missing month (and year if needed)
    month = None
    if start_str:
        cleaned_start = clean_date_str(start_str)
        dt_start = pd.to_datetime(cleaned_start, dayfirst=True, errors='coerce')
        if pd.notnull(dt_start):
            month = dt_start.month
            if year is None:
                year = dt_start.year
    if month is None or year is None:
        return pd.NaT
    
    try:
        return pd.Timestamp(year=year, month=month, day=day)
    except Exception:
        return pd.NaT

def parse_start_date(start_str, end_str):
    """
    Parse the start date.
    If the start date is just a day number, use the end date to infer month and year:
      - If start day is <= end date day, assume same month/year.
      - If start day is > end date day, assume the start date is in the previous month.
    If the start date lacks a year, append the year from the end date.
    """
    start_clean = clean_date_str(start_str)
    
    if re.fullmatch(r'\d+', start_clean):
        start_day = int(start_clean)
        end_dt = parse_end_date(end_str, start_str=start_str)
        if pd.notnull(end_dt):
            if start_day <= end_dt.day:
                return pd.Timestamp(year=end_dt.year, month=end_dt.month, day=start_day)
            else:
                prev_month = end_dt.month - 1 if end_dt.month > 1 else 12
                year = end_dt.year if end_dt.month > 1 else end_dt.year - 1
                try:
                    return pd.Timestamp(year=year, month=prev_month, day=start_day)
                except Exception:
                    return pd.NaT
        else:
            return pd.NaT
    else:
        dt = pd.to_datetime(start_clean, dayfirst=True, errors='coerce')
        if pd.isnull(dt):
            end_dt = parse_end_date(end_str, start_str=start_str)
            if pd.notnull(end_dt):
                dt = pd.to_datetime(start_clean + " " + str(end_dt.year), dayfirst=True, errors='coerce')
        return dt


def update_battle_dates(df, battle_name, new_start_date, new_end_date):
    """
    Update StartDate_clean and EndDate_clean for the specified battle.
    new_start_date and new_end_date should be strings in a recognizable date format (e.g., "mm-dd-yyyy").
    """
    # Convert the new date strings into Timestamp objects.
    new_start = pd.to_datetime(new_start_date, dayfirst=True, errors='coerce')
    new_end = pd.to_datetime(new_end_date, dayfirst=True, errors='coerce')
    
    if pd.isnull(new_start) or pd.isnull(new_end):
        print("Error: One of the dates could not be parsed. Please check your format.")
        return df
    
    # Locate the row(s) where the battle name matches
    mask = df['BattleName'] == battle_name
    if mask.sum() == 0:
        print("No battle found with that name.")
        return df

    # Update the cleaned date columns.
    df.loc[mask, 'StartDate_clean'] = new_start
    df.loc[mask, 'EndDate_clean'] = new_end
    print(f"Dates for '{battle_name}' have been updated.")
    return df


df_ww1_test['StartDate_clean'] = df_ww1_test.apply(
    lambda row: parse_start_date(row['StartDate'], row['EndDate']),
    axis=1)

df_ww1_test['EndDate_clean'] = df_ww1_test.apply(
    lambda row: parse_end_date(row['EndDate'], start_str=row['StartDate']),
    axis=1)


#Not a great method but there were some weird outliers so just do them by hand
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Segale", "27-10-1916","27-10-1916")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of the Lys (1918)", "07-04-1918","29-04-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Valenciennes (1918)", "28-10-1918","02-11-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of the San river (1914)", "22-09-1914","23-10-1914")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Rarańcza", "15-02-1918","16-02-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Kostiuchnówka", "04-07-1916","07-07-1916")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Albert (1918)", "21-08-1918","23-08-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of the Canal du Nord", "27-09-1918","01-10-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Cambrai (1917)", "20-11-1917","07-12-1917")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of the Four Rivers", "16-12-1914","16-01-1915")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Mulhouse", "07-08-1914","26-08-1914")
df_ww1_test = update_battle_dates(df_ww1_test,"Struma operation", "17-08-1916","23-08-1916")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Karakilisa", "25-05-1918","28-05-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of the Lys (1918)", "07-04-1918","29-04-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Laski and Anielin", "22-10-1914","26-10-1914")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Abaran", "23-05-1918","29-05-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Vimy Ridge", "09-04-1917","12-04-1917")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Manzikert (1915)", "10-07-1915","26-07-1915")
df_ww1_test = update_battle_dates(df_ww1_test,"First Battle of Przasnysz", "07-02-1915","28-02-1915")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Kraśnik", "23-08-1914","25-08-1914")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Rawa", "03-09-1914","11-09-1914")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Doiran (1916)", "09-08-1916","18-08-1916")
df_ww1_test = update_battle_dates(df_ww1_test,"Battle of Sharqat", "23-10-1918","30-10-1918")
df_ww1_test = update_battle_dates(df_ww1_test,"Atlantic U-boat campaign of World War I", "08-08-1914","20-08-1914")




df_ww1_test['StartDate_clean'] = df_ww1_test['StartDate_clean'].apply(
    lambda x: x.strftime("%Y-%m-%d") if pd.notnull(x) else ""
)
df_ww1_test['EndDate_clean'] = df_ww1_test['EndDate_clean'].apply(
    lambda x: x.strftime("%Y-%m-%d") if pd.notnull(x) else ""
)

print(df_ww1_test.head())

# Write the updated DataFrame to CSV with proper UTF-8 encoding and BOM.
df_ww1_test.to_csv("WW1_DatesNames1.csv", index=False, encoding="utf-8-sig")
