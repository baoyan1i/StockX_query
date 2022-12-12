from flask import Flask, request, render_template
from flask_cors import CORS
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search_autocomplete():
    query = request.args['q']
    tmp = query.split("=")
    tokenss = tmp[0]
    tokens = tokenss.split(" ")
    for i in range(len(tokens)):
        print(tokens[i])

    gte = tmp[1]
    lte = tmp[2]
    print(len(gte), len(lte))
    if len(gte) == 0 and len(lte) == 0:
        gte = 250
        lte = 500
    if len(lte) == 0 and len(gte) != 0:
        lte = gte
    print(gte, lte)

    clauses = [{
                "span_multi": {
                  "match": {
                    "fuzzy": {
                      "Sneaker Name": {
                        "value": tokens[i],
                        "fuzziness": "AUTO"
                      }
                    }
                  }
                }
              }
        for i in range(len(tokens))
        ]
    payload = {
        "bool": {
            "must": [{
                "span_near": {
                    "clauses": clauses,
                    "slop": 12,
                    "in_order": False
                }
            }
        ],
            "filter": [{
                "range": {
                    "Sale Price": {
                        "gte": gte,
                        "lte": lte
                    }
                }
            }
            ],

    }
    }

    print(clauses)
    print(payload)
    resp = es.search(index="stockx", query=payload, size=50)
    print(resp)
    return [res['_source']['Sneaker Name'] + ", Sale Price: " + res['_source']['Sale Price'] for res in resp['hits']['hits']]


if __name__ == '__main__':
    app.run(debug=True)
