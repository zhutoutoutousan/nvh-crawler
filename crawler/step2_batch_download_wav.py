import subprocess
import csv

def main():

    __remove_spaces = lambda s: s.replace(' ', '_')
    __add_quotes = lambda s: f'"{s}"'

    powershell_execution_policy = ["PowerShell.exe", "-ExecutionPolicy", "Unrestricted", "-File", "yt-dlp.ps1"]

    # powershell_download = lambda ytid, directory, outname: ["powershell.exe", "./yt-dlp.ps1", "--videoid", ytid, " ", "--dir" , directory, " ", "--outname", f"{__remove_spaces(outname)}"]
    powershell_download = lambda ytid, directory, outname: ["powershell.exe", "./yt-dlp.ps1", "-dir" , directory, "-videoid", ytid, "-outname", f"{__remove_spaces(outname)}"]
    # csv read ./data/sound/noise.csv
    with open('./data/manifest/noise.csv', encoding='utf—8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['YTID'], row['title'])
            print(powershell_download(row['YTID'], './data/sound/noise', row['title']))
            p = subprocess.Popen(powershell_download(row['YTID'], './data/sound/noise', row['title']))
            p.communicate()
    # csv read ./data/sound/healthy.csv
    with open('./data/manifest/healthy.csv', encoding='utf—8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['YTID'], row['title'])
            h = subprocess.Popen(powershell_download(row['YTID'], './data/sound/healthy', row['title']))
            h.communicate()

if __name__ == '__main__':
    main()