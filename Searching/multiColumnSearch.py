import pandas as pd

def MultiColumnSearch(searchText, listOfColumns, filter):
    result = []
    file_path = 'D:\\FasiTahir\\DSA\\Mid Project\\ScrapedData.csv'
    df = pd.read_csv(file_path,encoding="utf-8")
    df = df.astype(str)
    df = df.dropna()

    print(searchText)
    print(listOfColumns)
    print(filter)
    matched = False
    for index, row in df.iterrows():
        
        if filter == 'AND':
            matched = all(term.lower().strip() in str(row[column]).lower().strip() for column, term in zip(listOfColumns, searchText))
        elif filter == 'OR':
            matched = any(term.lower().strip() in str(row[column]).lower().strip() for column, term in zip(listOfColumns, searchText))
        elif filter == 'NOT':
            matched = all(term.lower().strip() not in str(row[column]).lower().strip() for column, term in zip(listOfColumns, searchText))
        if matched:
            result.append(row)
    search_data_df = pd.DataFrame(result)
    search_data_df.to_csv('SearchedResult.csv', index=False)
