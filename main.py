# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import networkx
import obonet
import sys
import json
app = Flask(__name__)

url = 'data.obo'
graph = obonet.read_obo(url)


@app.route("/")
def home():
    res = {}
    return render_template('index.html', res=res)

# http://127.0.0.1:5000/display_all


@app.route("/display_all")
def display_all():
    res = dict(graph.nodes)
    return jsonify(res)

# http://127.0.0.1:5000/search/?key=angiosarcoma


@app.route("/search/", methods=['GET'])
def search():
    key = request.args.get('key')
    id_to_name = {id_: data.get('name')
                  for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_,
                  data in graph.nodes(data=True) if 'name' in data}

    res = {}
    if(key in name_to_id.keys()):
        doc_id = name_to_id[key]
        res[key] = graph.nodes[doc_id]
        # 尋找子類別
        for child, parent_id, key in graph.out_edges(doc_id, keys=True):
            parent_name = id_to_name[parent_id]
            res[parent_name] = graph.nodes[parent_id]
    else:
        res = "no key in database"

    return jsonify(res)


# 之後要改成post，輸入文章
# http://127.0.0.1:5000/show


@app.route("/show", methods=['POST', 'GET'])
def showArticle():
    article = ""
    if request.method == 'POST':
        article = request.form.get('article')
    #article = "Hemangioendothelioma is the term used to name those vascular neoplasms that show a borderline biological behavior, intermediate between entirely benign hemangiomas and highly malignant angiosarcomas. Although originally spindle cell hemangioendothelioma was proposed as a specific clinicopathologic variant of hemangioendothelioma, currently, it is considered as an entirely benign lesion, and thus, the name spindle cell hemangioma seems to be the most accurate for this lesion. Authentic hemangioendotheliomas involving the skin and soft tissues include papillary intralymphatic angioendothelioma (also known as Dabska tumor), retiform hemangioendothelioma, kaposiform hemangioendothelioma, epithelioid hemangioendothelioma, pseudomyogenic hemangioendothelioma (also known as epithelioid sarcoma-like hemangioendothelioma), and composite hemangioendothelioma. Each of these neoplasms exhibit characteristic histopathologic features. The most characteristic finding of papillary intralymphatic hemangioendothelioma consists of papillary tufts, with a central hyaline core lined by hobnail-like endothelial cells protruding into the lumina. Retiform hemangioendothelioma is an infiltrative neoplasm composed of elongated arborizing vessels, arranged in an anastomosing pattern that resembles that of the rete testis, and lined by a single layer of hobnail-like endothelial cells that protrude within the narrow lumina. Kaposiform hemangioendothelioma is composed of several solid poorly circumscribed nodules, and each nodule is composed of a mixture of small capillaries and solid lobules of endothelial cells arranged in a glomeruloid pattern. A frequent finding consists of the presence of areas of lymphangiomatosis adjacent to the solid nodules. Epithelioid hemangioendothelioma is composed of cords, strands, and solid aggregates of round, oval, and polygonal cells, with abundant pale eosinophilic cytoplasm, vesicular nuclei, and inconspicuous nucleoli, embedded in a fibromyxoid or sclerotic stroma. Many neoplastic cells exhibit prominent cytoplasmic vacuolization as an expression of primitive vascular differentiation. Pseudomyogenic hemangioendothelioma is a poorly circumscribed, fascicular lesion with infiltrative borders composed of round or oval neoplastic cells, with vesicular nuclei and inconspicuous nucleoli, and ample homogeneous eosinophilic cytoplasm, giving them a rhabdomyoblastic appearance. Finally, composite hemangioendothelioma is the term used to name locally aggressive vascular neoplasms of low-grade malignancy showing varying combinations of benign, low-grade malignant, and high-grade malignant vascular components. From the immunohistochemical point of view, proliferating cells of all hemangioendotheliomas express a lymphatic endothelial cell immunophenotype. Most hemangioendotheliomas are low-grade vascular neoplasms, with a tendency to recur locally and a low metastatic potential, mostly to regional lymph nodes. Epithelioid hemangioendothelioma, especially large lesions and those located in deep soft tissues, seems to have a more aggressive biological behavior."

    id_to_name = {id_: data.get('name')
                  for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_,
                  data in graph.nodes(data=True) if 'name' in data}
    res = {}
    for word in article.split(" "):
        key = word
        if(key in name_to_id.keys()):
            name = name_to_id[key]
            res[word] = graph.nodes[name]
        else:
            res[word] = False

    return dictHTML(res)


def dictHTML(d):
    out = "<p>"

    # Human disease ontology
    id_to_name = {id_: data.get('name')
                  for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_,
                  data in graph.nodes(data=True) if 'name' in data}

    key = list(d.keys())
    value = list(d.values())
    for k in range(len(key)):
        # 有在 database
        if value[k]:
            out += " <a href=http://127.0.0.1:5000/search/?key=" + \
                key[k]+">" + key[k] + "</a> "
        else:
            out += " " + key[k] + " "
    return out + "</p>"


if __name__ == '__main__':
    app.debug = True
    app.run()
