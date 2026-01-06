import pandas as pd
import re
import numpy as np
from datetime import datetime
import statistics

def parse_row(row):
    
    # Check if the row starts with a quoted house name (e.g., "Kungsklippan 12, 3tr")
    if row.startswith('"'):
        # Find the closing quote for the house name
        match = re.match(r'"([^"]+)",(.*)', row)
        if match:
            house_name = match.group(1).strip()
            rest_of_row = match.group(2)
        else:
            raise ValueError("Invalid format for row with quoted house name")
        # The first numeric field after the quoted name is final price
        parts = rest_of_row.split(',', 1)
        final_price = float(parts[0].strip())/1000000
        rest = parts[1] if len(parts) > 1 else ''
    else:
        # Normal case without quoted house name
        parts = row.split(",", 2)
        house_name = parts[0].strip()
        final_price = float(parts[1].strip())/1000000
        rest = parts[2] if len(parts) > 2 else ''

    info = {}
    for m in re.finditer(r"(Starting price|Price trend|Property type|Tenure type|Number of rooms|Living area|Biarea|Tomtarea|Year built|Driftskostnad|Arrende|Uteplats|Number of visits|Other_area):? *([^,]*)", rest):
        key = m.group(1).strip()
        val = m.group(2).strip()
        info[key] = val

    # Normalize fields and extract numeric values where needed
    info['Living_area'] = re.sub(r'[^\d]', '', info.get('Living area', ''))
    info['Other_area'] = re.sub(r'[^\d]', '', info.get('Biarea', ''))
    if 'Uteplats' in info and info.get('Uteplats', '').lower() == 'ja':
        info['Other_area'] = 'Balcony'
    info['Plot_area'] = re.sub(r'[^\d]', '', info.get('Tomtarea', ''))
    info['Rooms'] = info.get('Number of rooms', '')
    info['Built_on'] = info.get('Year built', '')
    start_price = info.get('Starting price', '')
    if start_price:
        m = re.search(r'(\d+)', start_price.replace(' ',''))
        info['Starting_price'] = m.group(1) if m else ''
    else:
        info['Starting_price'] = ''
    price_trend = info.get('Price trend', '')
    price_change = ''
    if price_trend:
        m = re.search(r'([+\-]?\d+[ ]?\d*) kr', price_trend.replace(' ',''))
        if m:
            price_change = m.group(1).replace(' ','')
    info['Price_Change'] = price_change
    info['Operating_cost'] = re.sub(r'[^\d]', '', info.get('Driftskostnad',''))
    info['Charge'] = re.sub(r'[^\d]', '', info.get('Arrende',''))
    part = info['Floor'].str.split(",").str[0].str.split("av")
    part2 = info['Floor'].str.split(",").str[1]
    info['Lift'] = part2.str.strip().apply(
        lambda x: 'Yes' if x == 'hiss finns' else ('No' if x == 'hiss finns ej' else np.nan))
    info['Floor'] = part.str[0]
    info['Total_no_Floors'] = part.str[1]
    info['Balcony'] = 'Yes' if 'Uteplats' in info and info.get('Uteplats','').lower() == 'ja' else ''
    info['House_type'] = info.get('Property type', '')
    info['Sold_date'] = info['Location'].str[-12:]
    info['Location'] = info['Location'].str.split("-").str[1]
    loc_list = info['Location'].str.split(",").str[0]
    info['Location'] = info['Location'].str.replace(" ", "")
    info['Municipality'] = info['Location'].str.split(",").str[1]
    info['Municipality'] = info["Municipality"].str[:-7]
    info['Municipality'] = info["Municipality"].str.replace(" ", "")
    info['Location'] = loc_list
    info['Release_form'] = info['Release_form'].str.replace(" ", "")
    info['Release_form'] = info['Release_form'].str.replace( ["3 rum", "2 rum", "1 rum", "1,5 rum", "11 rum", "12 rum", "5 rum", "6 rum"], np.nan)
    

    final_row = {
        'House_Name': house_name,
        'Location': info['Location'],
        'Municipality': info['Municipality'],
        'House_type': info['House_type'],
        'Release_form': info['Release_form'],
        'Rooms': info['Rooms'],
        'Floor': info['Floor'],
        'Total_no_Floors': info['Total_no_Floors'],
        'Lift': info['Lift'],
        'Balcony': info['Balcony'],
        'Living_area': info['Living_area'],
        'Plot_area': info['Plot_area'],
        'Other_area': info['Other_area'],
        'Built_on': info['Built_on'],
        'Charge': info['Charge'],
        'Operating_cost': info['Operating_cost'],
        'Sold_date': info['Sold_date'],
        'Starting_price': info['Starting_price'],
        'Price_Change': info['Price_Change'],
        'Final_Price': final_price,
    }
    return final_row

def read_and_parse_files(filenames):
    all_rows = []
    for file in filenames:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Skip the first row (header with numbers)
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parsed = parse_row(line)
                    all_rows.append(parsed)
    return pd.DataFrame(all_rows)

def parse_date(date_str):
    date_str = date_str.strip()
    return datetime.strptime(date_str, '%d %B %Y')

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return np.nan

if __name__ == '__main__':
    input_files = ['Fritidshus_data.csv', 'Kedjehus_data.csv', 'Lägenhet_data.csv', 'Parhus_data.csv', 'Tomt_data.csv', 'Villa_data.csv']  # update with actual filenames
    df_combined = read_and_parse_files(input_files)
    
    #Upon initial investigation I found that the data type for various columns are not correct, so fixing them.
    df_combined['Sold_date'] = df_combined['Sold_date'].apply(parse_date)
    df_combined["Location"] = df_combined["Location"].str.replace(" ", "")
    df_combined['Location'] = df_combined.Location.astype('category')
    df_combined['House_type'] = df_combined.House_type.astype('category')
    df_combined['Release_form'] = df_combined.Release_form.astype('category')
    df_combined['Rooms'] = df_combined.Rooms.astype('int')
    df_combined['Balcony'] = df_combined.Balcony.astype('category')
    df_combined['Floor'] = df_combined.Floor.astype('int')
    df_combined["Built_on"] = df_combined["Built_on"].apply(convert_to_float)

    df_combined["Built_on"] = df_combined["Built_on"].fillna(
        statistics.median(df_combined["Built_on"]))
    df_combined['Municipality'] = df_combined.Municipality.astype('category')
    df_combined['Lift'] = df_combined.Lift.astype('category')
    df_combined['Total_no_Floors'] = df_combined.Total_no_Floors.astype('int')
    df_combined = df_combined[["House_Name", "Location", "Municipality", "House_type", 
                               "Release_form", "Rooms", "Floor", "Total_no_Floors", "Lift",
                               "Balcony", "Living_area", "Plot_area", "Other_area", "Built_on",
                               "Charge", "Operating_cost", "Sold_date", "Starting_price", 
                               "Price_Change","Final_Price"]]

    df_combined.to_csv('Initial_data.csv', index=False)
