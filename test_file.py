import csv

def ai_facts():
    fax_list = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            fax_list.append({
                f"ai_responses{i}": value for i, value in enumerate(row)
            })

    fax_list.pop(1)
    print(fax_list)

ai_facts()