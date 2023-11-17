import json

with open("./Bio-Medical.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    data = [
        {
            "id": data[i]["id"],
            "user_query": data[i]["user_query"],
        }
        for i in range(len(data))
    ]
with open("./Open-Domain_demo.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
