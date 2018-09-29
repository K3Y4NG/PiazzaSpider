import json
from datetime import datetime


with open ('data.json') as f:
    data = json.load(f)

result = {}
def append_result(x):
    index = x.find("(")
    if index != -1:
        x = x[:index - 1]
    if x not in result:
        result[x] = []
    result[x].append(info)
    
for i in range(len(data)):
    post = data[i]
    authors = data[i]["author"]
    for j in range(len(authors)):
        info = {}
        author = authors[j]
        info["time"]= data[i]["time"]
        info["type"] = "New Post"
        info["title"]= data[i]["title"]
        info["text"] = data[i]["text"]
        append_result(author)

    student_answers = data[i]["student_answer"]
    for j in range(len(student_answers)):
        student_answer = student_answers[j]
        for k in range(len(student_answer["author"])):
            info = {}
            author = student_answer["author"][k]
            info["time"] = student_answer["time"]
            info["type"] = "Selected Answer"
            info["text"] = student_answer["text"]
            append_result(author)


    followups = data[i]["followup"]
    for j in range(len(followups)):
        followup = followups[j]
        info = {}
        author = followup["name"]
        info["time"] = followup["time"]
        info["type"] = "Normal Answer"
        info["text"] = followup["text"]
        append_result(author)


        replies = followup["replies"]
        for k in range(len(replies)):
            reply = replies[k]
            info = {}
            author = reply["name"]
            info["time"] = reply["time"]
            info["type"] = "Reply"
            info["text"] = reply["text"]
            append_result(author)


def compare(item):
    date_str = item["time"][4:24]
    date_obj = datetime.strptime(date_str, '%b %d %Y %H:%M:%S')
    return date_obj

count = 0
for res in result:
    count += len(result[res])
    result[res].sort(key=compare)
    print("\n" + res + ": " + str(len(result[res])), end="")
    for i in range(len(result[res])):
        print(", " + result[res][i]["time"][4:24], end="")
print("\nTotal item number:" +str(count))

with open("data_student.json", 'w') as outfile:
    json.dump(result, outfile)








    


