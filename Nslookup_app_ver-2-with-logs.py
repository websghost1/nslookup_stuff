import subprocess
import csv
from datetime import datetime
import os
import ipaddress
import re

info_file = "saved_info.csv"
nslookup_history = "looked_up_history.txt"

while True:
    user_choose_save_or_not_logs = input("Do you want to save logs of searches by dat in separete files? (y/n): ")
    if user_choose_save_or_not_logs.lower() == "y":
        # if user wants separate logs and press "y"
        separete_log_by_date = True
        break
    elif user_choose_save_or_not_logs.lower() == "n":
        # if user dont want separate logs and press "n"
        separete_log_by_date = False
        break
    else:
        print("Please press only y/n")


#separete search history by files
def write_log(content):
    if separete_log_by_date:
        log_file = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
    else:
        log_file = "looked_up_history.txt"

    with open(log_file, mode='a',encoding="utf-8") as file:
        file.write(content)



#check if file exists if not creat it
if not os.path.exists(nslookup_history):
    with open(nslookup_history,'w',encoding="utf-8") as history_file:
        history_file.write("=====NSLOOKUP HISTORY START===\n")

#check if csv is not exist:

if not os.path.exists(info_file) or os.path.getsize(info_file) ==0:
    with open(info_file,'w',newline='',encoding="utf-8")as file:
        create_csv = csv.writer(file)
        create_csv.writerow(["IP Address","Domain name"])

#check if user write domain correctly
def is_valid_domain(domain):
    pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None


# הגדרת הפונקציה להרצת nslookup
def run_nslookup(domain):
    result = subprocess.run(['nslookup', domain], capture_output=True, text=True)
    print(result.stdout)
    # קריאת התוכן מההיסטוריה
    with open(nslookup_history, 'r', encoding='utf-8') as read_file:
        content = read_file.read()
    # בדיקה אם התוצאה כבר קיימת
    if result.stdout not in content:
        with open(nslookup_history, 'a', encoding='utf-8') as write_file:
            write_file.write(f"This lookup was made at: {datetime.now()}\n")
            write_file.write("======A RECORD=====\n")
            write_file.write(f"Domain:{domain}\n")
            write_file.write(result.stdout + "\n")
            write_file.write("--------------------------------------------\n\n")
#nslookup - check Cname:

def run_nslookup_cname(domain):
    result = subprocess.run(['nslookup','-type=CNAME',domain], capture_output=True, text=True)
    print(result.stdout)
    #נבדוק אם יש אותו דבר
    with open(nslookup_history, 'r',encoding="utf-8") as history_file:
        content = history_file.read()
        if result.stdout not in content:
            with open(nslookup_history, 'a',encoding="utf-8") as history_file:
                history_file.write(f"This lookup was made at: {datetime.now()}\n")
                history_file.write("====== CNAME RECORD ======\n")
                history_file.write(f"Domain:{domain}\n")
                history_file.write(result.stdout + "\n")
                history_file.write("------------------------------\n")
                history_file.write("\n")

#check MX
def run_nslookup_mx(domain):
    result = subprocess.run(['nslookup', '-type=MX', domain],capture_output=True, text=True)
    print(result.stdout)
    with open(nslookup_history, 'r',encoding="utf-8") as history_file:
        content = history_file.read()
        if result.stdout not in content:
            with open(nslookup_history, 'a',encoding="utf-8") as history_file:
                history_file.write(f"This lookup was made at: {datetime.now()}\n")
                history_file.write("====== MX RECORD ======\n")
                history_file.write(f"Domain: {domain}\n")
                history_file.write(result.stdout + "\n")
                history_file.write("------------------------\n")
                history_file.write("\n")


#check NS
def run_nslookup_NS(domain):
    result = subprocess.run(['nslookup', '-type=NS', domain],capture_output=True, text=True)
    print(result.stdout)
    with open(nslookup_history, 'r',encoding="utf-8") as history_file:
        content = history_file.read()
        if result.stdout not in content:
            with open(nslookup_history,'a',encoding="utf-8") as history_file:
                history_file.write(f"This lookup was made at: {datetime.now()}\n")
                history_file.write("======== NS Record =======\n")
                history_file.write(f"Domain: {domain}\n")
                history_file.write(result.stdout + "\n")
                history_file.write("----------------------------\n")
                history_file.write("\n")

#Check PTR
def run_nslookup_PTR(ip_adress):
    result = subprocess.run(['nslookup', '-type=PTR',ip_adress],capture_output= True,text=True)
    print(result.stdout)
    with open(nslookup_history, 'r',encoding="utf-8") as history_file:
        content = history_file.read()
        #check what we have in file
        if result.stdout not in content:
            with open(nslookup_history,'a',encoding="utf-8") as history_file:
                history_file.write(f"This lookup was made at: {datetime.now()}\n")
                history_file.write("======== PTR Record =====\n")
                history_file.write(f"Ip Adress: {ip_adress}\n")
                history_file.write(result.stdout+ "\n")
                history_file.write("\n")

#Check TXT
def run_nslookup_TXT(domain):
    result = subprocess.run(['nslookup','-type=TXT',domain],capture_output=True, text=True)
    print(result.stdout)
    with open(nslookup_history,'r',encoding="utf-8") as history_file:
        content = history_file.read()
        if result.stdout not in content:
            with open(nslookup_history,'a',encoding="utf-8") as history_file:
                history_file.write(f"This lookup was made at: {datetime.now()}\n")
                history_file.write("======== TXT Record ======\n")
                history_file.write(f"Domain: {domain}\n")
                history_file.write(result.stdout + "\n")
                history_file.write("\n")


# לולאת התפריט
while True:
    # הצגת התפריט
    menu = input(
        "Please choose what you want to do:\n"
        "1) A: Specifies a computer's IP address.\n"
        "2) ANY: Specifies a computer's IP address.\n"
        "3) CNAME: Specifies a canonical name for an alias.\n"
        "4) MX: Specifies the mail exchanger.\n"
        "5) NS: Specifies a DNS name server for the named zone.\n"
        "6) PTR: Specifies a computer name if the query is an IP address; otherwise, specifies the pointer to other information.\n"
        "7) TXT: Specifies the text information.\n"
        "Q) Quit: Exit the program\n"
        
        "Enter your choice: "
    )

    if menu == "1":
        print("You chose to check 'A' record")
        while True:
            ask_user_for_domain_A_record = input("Please enter a domain to check (m'back to menu, 'q' exit program):  ")
            if ask_user_for_domain_A_record.lower() == 'q':
                print("Exiting program")
                exit()
            elif ask_user_for_domain_A_record.lower() == 'm':
                print("Going back to main menu")
                ask_user_for_domain_A_record = None
                break
            #check if domain is valid
            if not is_valid_domain(ask_user_for_domain_A_record):
                print("This is not a valid domain name.")
                continue  # חוזר לתפריט
            break

        if ask_user_for_domain_A_record is None:
            continue

        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)

            for row in read_file:
                if row[1] == ask_user_for_domain_A_record:
                    break
            else:
                with open(info_file,mode='a',encoding="utf-8") as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["",ask_user_for_domain_A_record])

            # הרצת פקודת nslookup
            run_nslookup(ask_user_for_domain_A_record)


    elif menu == "2":
        print("You choose to check 'ANY' record")
        while True:
            ask_user_for_domain_any_record = input("Please enter a domain to check (m'back to menu, 'q' exit program): ")
            if ask_user_for_domain_any_record.lower() == 'q':
                print("Exiting program")
                exit()
            elif ask_user_for_domain_any_record.lower() == 'm':
                print("Going back to main menu")
                ask_user_for_domain_any_record = None
                break

            #check if domain is valid
            if not is_valid_domain(ask_user_for_domain_any_record):
                print("This is not a valid domain name.")
                continue  # חוזר לתפריט
            break

        if ask_user_for_domain_any_record is None:
            continue
        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)

            for row in read_file:
                if row[1] == ask_user_for_domain_any_record:  # assuming domain is in the third column
                    break  # מצאנו את הדומיין, יצאנו מהלולאה
            else:

                with open(info_file, mode="a", newline="") as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["", ask_user_for_domain_any_record])  # הוסף את הדומיין לקובץ

        run_nslookup(ask_user_for_domain_any_record)

    elif menu == "3":
        print("You chose to check a 'Cname' record")
        while True:
            ask_user_for_domain_Cname_record = input("Enter a domain to check a CNAME (m'back to menu, 'q' exit program): ")
            if ask_user_for_domain_Cname_record.lower() == 'q':
                print("Exiting programs")
                exit()
            elif ask_user_for_domain_Cname_record.lower() =='m':
                print("Going back to main menu")
                ask_user_for_domain_Cname_record = None
                break

            #check if domain is valid
            if not is_valid_domain(ask_user_for_domain_Cname_record):
                print("This is not a valid domain name.")
                continue  # חוזר לתפריט
            break

        if ask_user_for_domain_Cname_record is None:
            continue

        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)

            for row in read_file:
                if row[1] == ask_user_for_domain_Cname_record:
                    break
            else:
                with open(info_file, mode="a", newline="")as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["", ask_user_for_domain_Cname_record])

        run_nslookup_cname(ask_user_for_domain_Cname_record)

    elif menu == "4":
        print("You choose to check an 'MX' record")
        while True:
            ask_user_for_domain_MX_record = input("Enter a domain name to check MX record (m'back to menu, 'q' exit program): ")
            if ask_user_for_domain_MX_record.lower() == 'q':
                print("Exiting program")
                exit()
            elif ask_user_for_domain_MX_record.lower() == 'm':
                print("Going back to main menu")
                ask_user_for_domain_MX_record = None
                break
            #check if domain is valid
            if not is_valid_domain(ask_user_for_domain_MX_record):
                print("This is not a valid domain name.")
                continue  # חוזר לתפריט
            break

        if ask_user_for_domain_MX_record is None:
            continue

        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)
            #נבדוק מה יש בשורות של הקובץ
            for row in read_file:
                if row[1] == ask_user_for_domain_MX_record:
                    break

            else:
                with open(info_file, mode="a",newline="")as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["",ask_user_for_domain_MX_record])

        run_nslookup_mx(ask_user_for_domain_MX_record)

    elif menu == "5":
        print("You choose to check an 'NS' record ")
        while True:
            ask_user_for_domain_NS_record = input("Please enter a domain name to check NS record (m'back to menu, 'q' exit program): ")
            if ask_user_for_domain_NS_record.lower() == 'q':
                print("Exiting program")
                exit()
            elif ask_user_for_domain_NS_record.lower() =='m':
                print("Going back to main menu")
                ask_user_for_domain_NS_record = None
                break
            #check if domain is valid
            if not is_valid_domain(ask_user_for_domain_NS_record):
                print("This is not a valid domain name.")
                continue  # חוזר לתפריט
            break

        if ask_user_for_domain_NS_record is None:
            continue

        #open fine
        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)
            #נבדוק מה יש בשורות של הקובץ
            for row in read_file:
                if row[1] == ask_user_for_domain_NS_record:
                    break
            else:
                with open(info_file, mode="a",newline="") as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["",ask_user_for_domain_NS_record])


        run_nslookup_NS(ask_user_for_domain_NS_record)

    elif menu == "6":
        print("You chose to check 'PTR' record")
        while True:
            ask_user_for_ip_adress_for_PTR_record = input("Enter an IP Address to check PTR (m'back to menu, 'q' exit program): ")
            if ask_user_for_ip_adress_for_PTR_record.lower() == "q":
                print("Exiting program")
                exit()
            elif ask_user_for_ip_adress_for_PTR_record.lower() == 'm':
                print("Going back to main menu \n")
                ask_user_for_ip_adress_for_PTR_record = None
                break

            #check if ip address is valid
            try:
                ipaddress.ip_address(ask_user_for_ip_adress_for_PTR_record)
                break
            except ValueError:
                print("This is not a valid IP address")
                continue
        if ask_user_for_ip_adress_for_PTR_record is None:
            continue

        with open(info_file, mode="r") as file:
            read_file = csv.reader(file)
            #נעבור שורה שורה ונבדוק מה יש שם
            for row in read_file:
                if row[0] == ask_user_for_ip_adress_for_PTR_record:
                    break
            else:
                with open(info_file, mode="a",newline="") as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow([ask_user_for_ip_adress_for_PTR_record,""])

        run_nslookup_PTR(ask_user_for_ip_adress_for_PTR_record)

    elif menu == "7":
        print("You choose to check 'TXT' record\n")
        while True:
            ask_user_for_domain_txt_record = input("Enter a domain name to check TXT ('m'back to menu, 'q' exit program ): ")
            if ask_user_for_domain_txt_record.lower() == 'q':
                print("Exiting program")
                exit()
            elif ask_user_for_domain_txt_record.lower() =='m':
                print("Going back to main menu")
                ask_user_for_domain_txt_record = None
                break
                # check if domain is valid
            if not is_valid_domain(ask_user_for_domain_txt_record):
                print("This is not a valid domain name.")
                continue
            break

        if ask_user_for_domain_txt_record is None:
            continue

        with open(info_file, mode='r',encoding="utf-8") as file:
            read_file = csv.reader(file)
            #check every row in file
            for row in read_file:
                if row[1] == ask_user_for_domain_txt_record:
                    break

            else:
                with open(info_file,mode='a',encoding="utf-8") as file:
                    create_csv = csv.writer(file)
                    create_csv.writerow(["",ask_user_for_domain_txt_record])

        run_nslookup_TXT(ask_user_for_domain_txt_record)



    elif menu == "Q" or menu.lower() == "q":
        print("Exiting program...")
        break  # יציאה מהלולאה

    else:
        print("You chose an option that is not implemented yet.")
