from flask import Flask, request, render_template
import os
import urlchecker
import sitemapper
import _pickle as cPickle
import json
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)


def map(url):

    #print(url)
    obj = sitemapper.url(url)
    obj.run_check(url)
    
    nodes = ""
    drawn = []
    for key, values in obj.sites.items():
        label = key.rsplit('/')[-1]
        if label == "":
            label = key.rsplit('/')[-2]
        nodes += '{' + 'id: "{}", label: "{}", group: {}'.format(key, label, 0) + '},\n'
        drawn.append(key)

    for key, values in obj.sites.items():
        for value in values:
            if value not in drawn and value not in obj.sites:
                nodes += '{' + 'id: "{}", label: "{}", group: {}'.format(value, value, 1) + '},\n'
                drawn.append(value)

    nodes = nodes[:-2] + "\n"

    edges = ""
    for key, values in obj.sites.items():
        for value in values:
            edges += '{' + 'from: "{}", to: "{}"'.format(key, value) + '},\n'
    edges = edges[:-2] + "\n"

    with open('./cached/' + url.rsplit('/')[2] + '.txt', 'w') as f:
        f.write(nodes + "\n")
        f.write(edges)

    return nodes, edges


def load(url):
    nodes = ""
    edges = ""
    end = False
    with open('./cached/{}.txt'.format(url)) as f:
        for line in f:
            if  "end" in line:
                end = True
                continue
            if not end:
                nodes += line
            else:
                edges += line

    return nodes, edges

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/test/')
def index():
    url = request.args.get("url")
    cached = os.listdir("./cached")
    if url + '.txt' not in cached:
        nodes, edges = map(url)
    else:
        nodes, edges = load(url)

    return render_template('graph.html', nodes = nodes, edges = edges)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    sys.setrecursionlimit(2000)
    load('www.google.de')
    app.run(host='0.0.0.0', port=port)


    



