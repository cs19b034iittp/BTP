import tabula
import pandas as pd
import os

def getTable(path):
    folder_path = "./csvFile"
    for filename in os.listdir(folder_path):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


    # Set the path to your PDF file
    pdf_path = path

    # Use tabula to extract the tables from the PDF file
    tables = tabula.read_pdf(pdf_path, pages='all')

    # Convert each extracted table into a DataFrame and save it as a CSV file
    for i, table in enumerate(tables):
        # Set the output path for the CSV file
        csv_output_path = f'./csvFile/output{i+1}.csv'
        # Convert the table to a DataFrame
        df = pd.DataFrame(table)
        # Save the DataFrame to a CSV file
        df.to_csv(csv_output_path, index=False)