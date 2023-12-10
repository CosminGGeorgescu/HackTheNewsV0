from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 
import subprocess

ARMA_ADDR = 'https://www.arma.org.ro/rapoarte-de-audienta/'
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

def update_xlsxs() -> set :
    html_body = requests.get(ARMA_ADDR, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}).text
    soup = BeautifulSoup(html_body, 'html.parser')

    already = set(os.listdir(XLSX_BASE_REPORTS))
    return list(filter(lambda link : link[-3 :] not in ["pdf", "xls"] and link.split("/")[-1 :][0] not in already, [el.find("a")['href'] for el in soup.find_all("tr", attrs={"class" : "tr"})]))

def curl(url: str):
    process = subprocess.Popen(['curl', '--output-dir', './reports', '-O', '-J', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print("Output:\n", stdout.decode('utf-8'))
    print("Errors:\n", stderr.decode('utf-8'))
    
    # Check if the process was successful
    if process.returncode == 0:
        print(f"File downloaded successfully from {url}")
    else:
        print(f"Error downloading file from {url}")

def main():
    for url in update_xlsxs():
        curl(url)
        convert(url.split("/")[-1 :][0])

if __name__ == "__main__":
    main()
