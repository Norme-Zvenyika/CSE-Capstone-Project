import csv
import requests
import pandas as pd
import os
import time
import certifi

def pa_scrape():
    url = "https://api.pjm.com/api/v1/da_hrl_lmps"
    headers = {
        "Ocp-Apim-Subscription-Key": "816157a779b1411496c97414535c0e6d"
    }

    # Define the years you want to process
    years =  [2017, 2018, 2019,2020,2021,2022,2023]  # Modify or extend this list as needed

    # Define zones of interest
    zones_of_interest =  ['APS','DUQ','METED','PECO','PENELEC','PPL']

    # Specify the CSV fieldnames
    fieldnames = ['Date', 'PNName', 'Voltage', 'Zone', 'Price', 'LMP', 'CongestionPrice', 'MarginalLoss']

    for year in years:
        print(f"\nStarting processing for year {year}...")
        # Define the beginning and final time for the year
        beginning_time = f"1/1/{year} 00:00"
        final_time = f"1/1/{year + 1} 00:00"

        # Parse the times using pandas
        start_date = pd.to_datetime(beginning_time)
        end_date = pd.to_datetime(final_time)

        # Create a folder for the current year if it doesn't exist
        output_folder = str(year)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created folder: {output_folder}")

        # Define chunk size (2 hours per chunk) and generate the list of date ranges
        chunk_size = pd.Timedelta(hours=2)
        current_date = start_date
        chunks = []
        while current_date < end_date:
            next_date = min(current_date + chunk_size, end_date)
            chunks.append((current_date, next_date))
            current_date = next_date

        total_chunks = len(chunks)
        print(f"Total chunks for year {year}: {total_chunks}")

        last_price = None

        # Iterate over chunks and make API requests
        for idx, (start, end) in enumerate(chunks):
            print(f"Year {year}: Processing chunk {idx + 1} of {total_chunks} "
                  f"({start.strftime('%m/%d/%Y %H:%M')} to {end.strftime('%m/%d/%Y %H:%M')})")
            datetime_range = f"{start.strftime('%m/%d/%Y %H:%M')} to {end.strftime('%m/%d/%Y %H:%M')}"
            params = {
                "download": "true",
                "startRow": 1,
                "isActiveMetadata": "true",
                "datetime_beginning_ept": datetime_range
            }

            try:
                response = requests.get(url, params=params, headers=headers, verify=certifi.where())
                response.raise_for_status()  # Check for HTTP errors
                items = response.json()  # Parse JSON response
                print(f"Retrieved {len(items)} records for current chunk.")

                for item in items:
                    current_price = item['total_lmp_da']
                    zone = item['zone']

                    # Process only if the zone is of interest and the price is different from the last recorded one
                    if zone in zones_of_interest and current_price != last_price:
                        # Optionally verify the record's year matches the year being processed
                        record_time = pd.to_datetime(item['datetime_beginning_utc'])
                        record_year = record_time.year
                        # Fallback to the loop's year if there is any discrepancy
                        record_year = record_year if record_year == year else year
                        output_filename = f"{output_folder}/{zone}{record_year}.csv"

                        row = {
                            'Date': item['datetime_beginning_utc'],
                            'PNName': item['pnode_name'],
                            'Voltage': item['voltage'],
                            'Zone': zone,
                            'Price': item['system_energy_price_da'],
                            'LMP': current_price,
                            'CongestionPrice': item['congestion_price_da'],
                            'MarginalLoss': item['marginal_loss_price_da']
                        }

                        file_exists = os.path.isfile(output_filename)
                        with open(output_filename, mode='a', newline='') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            if not file_exists:
                                writer.writeheader()  # Write header only if the file is new
                            writer.writerow(row)

                        last_price = current_price  # Update the last recorded price

                # Wait every 6 chunks to respect the API rate limit
                if idx < total_chunks - 1 and idx % 6 == 5:
                    print("Rate limit reached. Waiting for 1 minute...")
                    time.sleep(60)

            except requests.exceptions.RequestException as e:
                print("Error making request:", e)

        print(f"Data scraping complete for year {year}. Files saved in folder '{output_folder}'.")

    print("\nAll years processed. Data scraping complete.")

# Run the scraping function
pa_scrape()
