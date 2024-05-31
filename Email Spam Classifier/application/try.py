import csv

def save_to_file(body,label):
    filename = "project\project\input_emails.csv"
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        data = [body,label]
        writer.writerow(data)


def delete_last_row_from_csv():
    dl = None
    with open('project\project\input_emails.csv', 'r', newline='') as file:
        lines = list(csv.reader(file))
    if len(lines) > 1:
        # Remove the last row
        dl = lines[-1]
        lines = lines[:-1]
        print(dl)
        with open('project\project\input_emails.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

        body = dl[0]
        label = dl[1]
        if int(label) == 1:
            newlabel = 0
        elif int(label) == 0:
            newlabel = 1

        print(body,newlabel)
        save_to_file(body,newlabel)
        
    else:
        print("CSV file is empty or has only one row, so no rows were deleted.")

# Example usage:
delete_last_row_from_csv()




