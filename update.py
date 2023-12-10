import pandas as pd
from os import listdir

XLSX_BASE_REPORTS = "./reports/"
CSV_BASE_REPORTS = "./csv_reports/"

def convert(file: str):
    excel = pd.DataFrame(pd.read_excel(XLSX_BASE_REPORTS + file, skiprows=[0]))

    bases = list(filter(lambda col : "Unnamed" not in col, excel.columns))[1:]
    new_columns = ["Channels"]
    for i in range(6):
        new_columns.append(f"{bases[i // 2]}.{excel.values[0][1:][i]}")
    replace_columns = list(zip(excel.columns, new_columns))

    excel.rename(columns={k : v for k, v in replace_columns}).drop(0).to_csv(CSV_BASE_REPORTS + f"{file.split('.')[0]}.csv", index=None, header=True)

def main():
    for file in listdir(XLSX_BASE_REPORTS):
        convert(file)

if __name__ == "__main__":
    main()
