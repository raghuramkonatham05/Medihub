import json

def find_nearby_labs(recommended_tests):
    with open("data/labs.json") as f:
        labs = json.load(f)

    matched_labs = []
    for lab in labs:
        if any(test in lab["tests"] for test in recommended_tests):
            matched_labs.append(lab)

    return matched_labs
