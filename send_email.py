import json as js
import csv
import sys
import jinja2
import os
from datetime import datetime
# import smtplib

# read customers file to get information about customers 
def get_customers(customers_file, error):
    TITLE = []
    FIRST_NAME = [] 
    LAST_NAME = [] 
    EMAIL = []

    with open(customers_file, mode='r') as csv_file:
        customers = csv.DictReader(csv_file, delimiter=',')
        errorData = []
        for customer in customers:
            if customer["EMAIL"] != '':
                TITLE.append(customer["TITLE"])
                FIRST_NAME.append(customer["FIRST_NAME"])
                LAST_NAME.append(customer["LAST_NAME"])
                EMAIL.append(customer["EMAIL"])
            else:
                errorData.append([customer["TITLE"], customer["FIRST_NAME"], customer["LAST_NAME"], customer["EMAIL"]])
        with open(error, mode='w', newline='') as f:
            errorCustomer = csv.writer(f)
            errorCustomer.writerow(['TITLE','FIRST_NAME','LAST_NAME','EMAIL'])
            for customer in errorData:
                errorCustomer.writerow(customer)

    return TITLE, FIRST_NAME, LAST_NAME, EMAIL

def read_template(email_template_file):
    with open(email_template_file, mode='r') as email_template:
        template = js.load(email_template)
    return template 

# Can use CLI Python Library to parse agv from CMD such as argparse, getopt,... 
def main(email_template, customers, path_output_emails, error):
    # how to use smtp send email 
    # s = smtplib.SMTP(host='host_address', port=port)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)
    TITLE, FIRST_NAME, LAST_NAME, EMAIL = get_customers(customers, error)
    template = read_template(email_template)
    if os.path.isdir(path_output_emails):
        os.chdir(path_output_emails)
    else:
        os.mkdir(path_output_emails)
        os.chdir(path_output_emails)

    now = datetime.now()
    env = jinja2.Environment()
    outputJsonFile = open("output.json", "w")
    resultData = []
    for title, first_name, last_name, email in zip(TITLE, FIRST_NAME, LAST_NAME, EMAIL):
        data = {}
        body_template = env.from_string(template["body"])
        data["from"] = template["from"]
        data["to"] = email
        data["subject"] = template["subject"]
        data["mineType"] = template["mineType"]
        data["body"] = body_template.render(TITLE=title, FIRST_NAME=first_name, LAST_NAME=last_name, TODAY=now.strftime('%d %b %Y'))
        resultData.append(data)
        # s.send_message(data)
        # del data
    output = js.dumps(resultData, indent=4)
    outputJsonFile.write(output)
    outputJsonFile.close()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])