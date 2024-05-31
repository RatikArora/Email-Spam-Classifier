import joblib
from django.shortcuts import render,redirect
from django.urls import reverse
from scipy.sparse import csr_matrix
import numpy as np
import csv
# Load the trained models
model1 = joblib.load("LogisticRegression()trained.joblib")
model2 = joblib.load("SVC()trained.joblib")
model3 = joblib.load("RandomForestClassifier()trained.joblib")
tfidf_vectorizer = joblib.load("tfidf_vectorizer.joblib")

# Function to classify email
def classify_email(a):
    predictions = []
    a_f = tfidf_vectorizer.transform([f'''{a}'''])
    print(a,"\n",a_f)
    # a_f = a_f.reshape(1, -1)
    print(a_f)
    op1 = model1.predict(a_f)
    op2 = model2.predict(a_f)
    op3 = model3.predict(a_f)
    print(op1,op2,op3)

    # predictions.append(model1.predict(a_f).item())
    # predictions.append(model2.predict(a_f).item())
    predictions.append(model3.predict(a_f).item())
    return predictions

def save_to_file(body,label):
    filename = "input_emails.csv"
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        data = [body,label]
        writer.writerow(data)


def delete_last_row_from_csv():
    dl = None
    with open('input_emails.csv', 'r', newline='') as file:
        lines = list(csv.reader(file))
    if len(lines) > 1:
        # Remove the last row
        dl = lines[-1]
        lines = lines[:-1]
        # print(dl)
        with open('input_emails.csv', 'w', newline='') as file:
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
        return dl
        
    else:
        print("CSV file is empty or has only one row, so no rows were deleted.")
        return None


def main(request):
    result = None
    email_text = ""
    last_email = None
    delbutton = "No"

    if request.method == 'POST':
        if 'classify' in request.POST:
            email_text = request.POST.get('email_text', '')
            if email_text:
                result = classify_email(email_text)
                # print("result is : ", result[0])
                save_to_file(email_text, result[0])
                count_0 = result.count(0)
                count_1 = result.count(1)

                if count_0 > count_1:
                    result = 0
                else:
                    result = 1

                delbutton = "Yes"

        if 'delete_last_row' in request.POST:
            # Call the function to delete the last row
            dl = delete_last_row_from_csv()
            email_text = dl[0]
            result = dl[1]
            result = int(result)
            # print(dl)
            if result == 1:
                result = 0
            elif result == 0:
                result = 1

    print(result,email_text)
    return render(request, 'index.html', {'result': result, 'email_text': email_text,'delbutton':delbutton})

