import pandas
file_path = "/Users/solbergh/Documents/GitHub/simple_python_projects/session.jsonl"
dataframe = pandas.read_json(path_or_buf=file_path, lines=True)

def data_and_times_from_column_type(column_type):
    #returns a list of tuples
    #tuples are (data, time)
    #data is dict of relevent data for the event, time is milliseconds since the epoch
    rows = dataframe.loc[dataframe['type'] == column_type]
    data_and_times = []
    for row in rows.iterrows():
        row_values = row[1].values #0 is row number, 1 is values as pandas series object
        data = row_values[0]
        time = row_values[1]
        data_and_times.append((data, time))
    return data_and_times
