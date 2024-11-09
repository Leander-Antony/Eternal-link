from flask import Flask, render_template, request, jsonify, Response
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

app = Flask(__name__)


load_dotenv()
mongo_uri = os.getenv('MONGO_URII')


client = MongoClient(mongo_uri)
db = client['fate'] 
data_collection = db['fate'] 


def remove_match_char(list1, list2):
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                c = list1[i]
                list1.remove(c)
                list2.remove(c)
                list3 = list1 + list2
                return [list3, True]
    list3 = list1 + list2
    print(list3)
    return [list3, False]

def flames_game(name1, name2):
    name1 = name1.lower().replace(" ", "")
    name2 = name2.lower().replace(" ", "")

    p1_list = list(name1)
    p2_list = list(name2)

    proceed = True
    while proceed:
        ret_list = remove_match_char(p1_list, p2_list)
        con_list = ret_list[0]
        proceed = ret_list[1]
        

    count = len(con_list)
    result = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]

    while len(result) > 1:
        split_index = (count % len(result) - 1)
        if split_index >= 0:
            right = result[split_index + 1:]
            left = result[:split_index]
            result = right + left
        else:
            result = result[: len(result) - 1]

    return result[0]


@app.route('/never', methods=['GET'])
def download_data():
    """
    Endpoint to download user inputs data as CSV.
    """
    cursor = data_collection.find()

    data = list(cursor)
    if not data:
        return jsonify({"error": "No data available to download."}), 404

    for doc in data:
        doc['_id'] = str(doc['_id'])

    try:
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False)

        response = Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=user_inputs.csv"}
        )
        return response
    except Exception as e:
        return jsonify({"error": "Error generating CSV.", "message": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name1 = request.form['name1']
    name2 = request.form['name2']
    duration = request.form['duration']

    result = flames_game(name1, name2)

    user_input_data = {
        'name1': name1,
        'name2': name2,
        'duration': duration,
        'relationship_status': result,
    }

    data_collection.insert_one(user_input_data)

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
