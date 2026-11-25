import os
import hashlib
import csv
from datetime import datetime

def file_information(file_info): 
    try:
        filee_size = os.path.getsize(file_info)

        modtime = os.path.getmtime(file_info)
        moddate = datetime.fromtimestamp(modtime) 

        file_call = os.path.basename(file_info)
        filext = os.path.splitext(file_call)[1]

        return {
            "filename": file_info,
            "file extension": filext,
            "filee_size": filee_size,
            "date": moddate
        }

    except OSError:
        print("An Error occured, couldnt access file", file_info)
        return None
    
def get_sha256(file_info):
    try:
        sha256_one = hashlib.sha256() 

        with open(file_info, "rb") as file: 
            file_datainf = file.read() 
            sha256_one.update(file_datainf)
            
        return sha256_one.hexdigest()

    except OSError:
        print("Error: Could not count hash for", file_info)

def show_hashes(csv_info):
    hashes = {} 
    try:
        with open(csv_info, "r") as file: 
            viewer = csv.DictReader(file)

            for row in viewer:
                hashes[row["sha256"]] = row["label"]

        return hashes

    except OSError:
        print("Error, couldnt read or find csv file")

def savefile_info(save_results):
    try:
        with open("triage_sumarry.txt", "w") as file:
            for result in save_results:
                file.write("File:" + result["File"] + "\n")
                file.write("Extension" + str(result["Extension"])  + "\n")
                file.write("Size" + str(result["Size"] )  + "\n")
                file.write("Modified:" + result["Modified"]  + "\n")
                file.write("SHA-256:" + result["SHA-256"]  + "\n")

    except OSError:
        print("error")


def three_defs(folder_info):
    hashes = show_hashes(os.path.join(folder_info,"hashes_reference.csv")) 
    dup_hashes = {}
    save_results = []
    for filename in os.listdir(folder_info): 
        if filename.endswith((".txt", ".bin")) and filename != "README.txt":
            file_info = os.path.join(folder_info, filename)
            file_painfo = file_information(file_info) 
            files_hashes = get_sha256(file_info) 

            if file_painfo is None or files_hashes is None: 
                continue

            print("File:", file_painfo["filename"])
            print("Extension:", file_painfo["file extension"])
            print("Modified:", file_painfo["date"])
            print("Size:", file_painfo ["filee_size"])
            print("SHA-256", files_hashes)

            save_results.append({
                "File": file_painfo["filename"],
                "Extension": file_painfo["file extension"],
                "Modified": str(file_painfo["date"]),
                "Size": file_painfo ["filee_size"],
                "SHA-256": files_hashes
            })

            if files_hashes in dup_hashes: 
                dup_hashes[files_hashes].append(filename)
                print("The duplicate was", filename)

            else:
                dup_hashes[files_hashes] = [filename]
                print("No duplicates") 
    savefile_info(save_results)


folder_info = input("Enter a folders path")
if os.path.isdir(folder_info):
    three_defs(folder_info)

else:
    print("error")