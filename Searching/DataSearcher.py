import pandas as pd

def linear_search(column_name, filter_value, search_type):
    file_path = 'D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv'
    df = pd.read_csv(file_path)

    # Drop NaN values from the specified column
    df = df.dropna(subset=[column_name])
    
    if search_type == 'starts_with':
        result = df[df[column_name].str.startswith(filter_value)]
    elif search_type == 'ends_with':
        result = df[df[column_name].str.endswith(filter_value)]
    elif search_type == 'contains':
        result = df[df[column_name].str.contains(filter_value)]
    else:
        result = pd.DataFrame()  # Return an empty DataFrame for unknown search types
    
    search_data_df = pd.DataFrame(result)
    search_data_df.to_csv('SearchedResult.csv', index=False)
