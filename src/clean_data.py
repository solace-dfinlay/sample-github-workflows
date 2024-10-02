import pandas as pd
import re

def clean_log_file(file_path):
    with open(file_path, 'r') as file:
        log_data = file.readlines()

    timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s*")

    cleaned_logs = []
    for line in log_data:
        cleaned_line = re.sub(timestamp_pattern, '', line)
        cleaned_logs.append(cleaned_line.strip())

    df = pd.DataFrame(cleaned_logs, columns=['LogEntry'])

    return df

def save_cleaned_logs(df, output_path):
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_file = 'FAILURE_LOG.txt'
    output_file = 'CLEANED_LOG.csv'

    cleaned_df = clean_log_file(input_file)
    save_cleaned_logs(cleaned_df, output_file)
    print(f"Cleaned log file saved as {output_file}")
