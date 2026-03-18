
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# training data (synthetic but better spread)
X = []
y = []

for l in range(0,11,2):
    for n in range(0,11,2):
        for v in range(0,11,2):
            X.append([l,n,v])
            if l+n > v+5:
                y.append("Science")
            elif n > l:
                y.append("Commerce")
            else:
                y.append("Arts")

model = RandomForestClassifier()
model.fit(X,y)

def get_recommendation(responses, interest):
    scores = np.sum(responses, axis=0)
    pred = model.predict([scores])[0]

    # interest override weights
    interest_map = {
        "Engineer":"Science",
        "Doctor":"Science",
        "Scientist":"Science",
        "CA":"Commerce",
        "Entrepreneur":"Commerce",
        "Lawyer":"Arts",
        "Designer":"Arts",
        "Writer":"Arts",
        "Diploma Engineer":"Diploma"
    }

    if interest in interest_map:
        pred = interest_map[interest]

    data = {
        "Science":{
            "careers":["Engineering","Medicine","Research","AI/ML"],
            "roadmap":"10th → Science → JEE/NEET → Degree",
            "skills":["Maths","Problem Solving","Coding"]
        },
        "Commerce":{
            "careers":["CA","Finance","Business","Economics"],
            "roadmap":"10th → Commerce → B.Com → CA/MBA",
            "skills":["Accounting","Analysis","Economics"]
        },
        "Arts":{
            "careers":["Law","Design","Journalism","Psychology"],
            "roadmap":"10th → Arts → BA → Specialization",
            "skills":["Creativity","Communication","Writing"]
        },
        "Diploma":{
            "careers":["Polytechnic","Technical Jobs","Engineering Lateral Entry"],
            "roadmap":"10th → Diploma → Job or B.Tech lateral",
            "skills":["Technical Skills","Practical Work","Machine Handling"]
        }
    }

    result = data[pred]
    result["stream"] = pred
    result["scores"] = scores.tolist()
    return result
