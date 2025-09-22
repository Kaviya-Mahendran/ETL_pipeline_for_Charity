import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def extract_data():
    """
    Extracts data from the source CSV files.
    """
    print("Step 1: Extracting data...")
    try:
        donations_df = pd.read_csv('donations.csv')
        events_df = pd.read_csv('events.csv')
        campaigns_df = pd.read_csv('campaigns.csv')
        print("Extraction complete.")
        return donations_df, events_df, campaigns_df
    except FileNotFoundError as e:
        print(f"Error: One of the source files was not found. {e}")
        return None, None, None

def transform_data(donations_df, events_df, campaigns_df):
    """
    Cleans, standardizes, and merges the dataframes.
    This is where all the data quality issues are resolved.
    """
    print("Step 2: Transforming data...")

    # Handle duplicate columns and standardize names
    # For donations_df, drop the unnamed supporter_id column and rename the main one
    if 'supporter_id' in donations_df.columns and 'Supporter ID' in donations_df.columns:
        donations_df.drop(columns='supporter_id', inplace=True)
        donations_df.rename(columns={'Supporter ID': 'supporter_id'}, inplace=True)

    # For events_df, rename user_id and User ID to supporter_id
    if 'user_id' in events_df.columns and 'User ID' in events_df.columns:
        # Use fillna to combine values if one column has missing data
        events_df['supporter_id'] = events_df['user_id'].fillna(events_df['User ID'])
        events_df.drop(columns=['user_id', 'User ID'], inplace=True)
    
    # Standardize all date columns to a consistent YYYY-MM-DD format
    for df in [donations_df, events_df, campaigns_df]:
        for col in df.columns:
            if 'date' in str(col).lower():
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)

    # Handle missing values: fill missing donation_amount with 0
    donations_df['donation_amount'] = pd.to_numeric(donations_df['donation_amount'], errors='coerce')
    donations_df['donation_amount'].fillna(0, inplace=True)

    # Drop rows with a missing supporter_id, as it's the primary key
    donations_df.dropna(subset=['supporter_id'], inplace=True)
    events_df.dropna(subset=['supporter_id'], inplace=True)

    # Clean leading/trailing whitespace from campaign names
    campaigns_df['campaign_name'] = campaigns_df['campaign_name'].str.strip()

    # Merge the dataframes based on common IDs
    merged_df = pd.merge(donations_df, events_df, on='supporter_id', how='left', suffixes=('_donations', '_events'))
    final_df = pd.merge(merged_df, campaigns_df, on='campaign_id', how='left')

    print("Transformation complete.")
    return final_df

def load_data(df, db_name='charity_data.db'):
    """
    Loads the final dataframe into a SQLite database.
    """
    print(f"Step 3: Loading data into {db_name}...")
    try:
        engine = create_engine(f'sqlite:///{db_name}')
        df.to_sql('supporter_interactions', engine, if_exists='replace', index=False)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Run the full pipeline
if __name__ == "__main__":
    donations_df, events_df, campaigns_df = extract_data()
    if all([isinstance(df, pd.DataFrame) for df in [donations_df, events_df, campaigns_df]]):
        final_dataframe = transform_data(donations_df, events_df, campaigns_df)
        if final_dataframe is not None:
            load_data(final_dataframe)

            # Also save the final DataFrame to a CSV file for your portfolio
            final_dataframe.to_csv('analytics_ready_data.csv', index=False)
            print("\nFinal data also saved to analytics_ready_data.csv.")
            
            print("\nPreview of Final Merged Data:")
            print(final_dataframe.head())