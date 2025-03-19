import pandas as pd
import re 
import numpy as np

df_ww1 = pd.read_csv('WW!1.csv', encoding="utf-8")

df_ww1_test = df_ww1.copy()

subset_df = df_ww1_test[df_ww1_test['StartDate_clean'].isnull()]


#subset_df.to_csv("Quick.csv")

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



df_ww1_test.to_csv("WW1_DatesDone1.csv",encoding='utf-8-sig')
