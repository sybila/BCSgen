import sys
import os
import copy
import collections
from compiler.ast import flatten
import json

def fixPath(output_file, path):
    with open(output_file, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('**FULLPATH**', path)

    # Write the file out again
    with open(output_file, 'w') as file:
        file.write(filedata)

"""
Writes one of the two static parts to output.
Both are statically included at the end of this file.
:param me: this file
:param output_file: output html file
:param start: string determining beginning of the part
:param end: string determining end of the part
:param mode: append or write
"""
def write_part(me, output_file, start, end, mode):
    f = open(output_file, mode)
    fp = open(me)
    allowed_to_read = False
    for i, line in enumerate(fp):
        line = line.rstrip()
        if start == line:
            allowed_to_read = True
        elif end == line:
            allowed_to_read = False
        elif allowed_to_read:
            f.write(line + '\n')
    f.close()

"""
Creates collection from given side
:param side: given string containing side of a rule
:return: collection
"""
def create_collection(side):
	return collections.Counter(flatten(map(lambda (k, v): [k]*int(v), side.iteritems())))

"""
Removes pairs of same agents from left and right side, i.e. creates a reaction.
:param From: left-hand-side
:param To: right-hand-side
:return: sides with reduced agents
"""
def create_reaction(From, To):
    From = create_collection(From)
    To = create_collection(To)

    left = From - To
    right = To - From

    left = map(lambda (a,b): b.__str__() + " " + a, left.items())
    right = map(lambda (a,b): b.__str__() + " " + a, right.items())

    return " + ".join(left), " + ".join(right)

"""
Writes new vertex to output file
:param vertex_id: internal ID of the vertex
:param ID: external ID of the vertex (hash)
:param label: explicit information about content of the vertex
:param output_file: output html file
"""
def write_entity(vertex_id, ID, label, output_file):
    output = open(output_file, 'a')
    output.write("\t{id: " + vertex_id.__str__() + ", label: '" + vertex_id.__str__() + "', title: 'ID " + ID.__str__() + "', text: '" + label.__str__() + "'},\n")
    output.close()

"""
Writes new edge to output file
:param edge_id: ID of the edge
:param left_index: internal ID of out-coming vertex
:param right_index: internal ID of in-coming vertex
:param From: left-hand-side of reaction
:param To: right-hand-side of the reaction
:param output_file: output html file
"""
def write_reaction(edge_id, left_index, right_index, From, To, output_file):
    output = open(output_file, 'a')
    output.write("\t{id: " + edge_id.__str__() + ", from: " + left_index.__str__() + ", to: " + right_index.__str__() +
                 ", arrows:'to', text: '" + From.__str__() + " => " + To.__str__() + "'},\n")
    output.close()

def createGraph(state_space_file, output_file):
    me = "../Core/Visualisation/create_graph.py"
    path = os.path.dirname(os.path.abspath(me))

    write_part(me, output_file, "FIRST PART START", "FIRST PART END", "w")

    with open(state_space_file, 'r') as f:
    	data = json.load(f)

    IDs = dict()
    vertex_id = 0
    for key, value in data['nodes'].iteritems():
    	vertex_id += 1
    	label = ""
    	for k, v in value.iteritems():
    		label += v + " " + k + "<br>"
    	write_entity(vertex_id, key, label, output_file)
    	IDs[key] = vertex_id

    output = open(output_file, 'a')
    output.write("\t]);\n\n\t// create an array with edges\n\tvar edges = new vis.DataSet([\n")
    output.close()

    for edge_id, value in data['edges'].iteritems():
    	From, To = create_reaction(data['nodes'][value['from']], data['nodes'][value['to']])
    	write_reaction(edge_id, IDs[value['from']], IDs[value['to']], From, To, output_file)
    		
    write_part(me, output_file, "SECOND PART START", "SECOND PART END", "a")

    fixPath(output_file, path)

'''
FIRST PART START
<!doctype html>
<html>
<head>
    <title>Network | Interaction events</title>

    <script type="text/javascript" src="**FULLPATH**/vis/vis.js"></script>
    <link href="**FULLPATH**/vis/vis.css" rel="stylesheet" type="text/css"/>

    <style type="text/css">
       #mynetwork {
            width: 800px;
            height: 500px;
            border: 1px solid lightgray;
        }
	    #rectangle {
		    text-align: center;
		    font-weight: bold;
	    }
}
    </style>
</head>
<body>

<div id="mynetwork"></div>
<div id="rectangle"style="width:800px;height:100%;border:1px solid #000;"> </div>

<script type="text/javascript">
    // create an array with nodes
        var nodes = new vis.DataSet([
FIRST PART END
'''

'''
SECOND PART START
	]);

    // create a network
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
		layout:{randomSeed:2},
		physics: {
			stabilization: false,
			barnesHut: {
				gravitationalConstant: -10000,
				centralGravity: 0.75,
				springConstant: 0.08,
				springLength: 150
			},
			maxVelocity: 146,
            solver: 'barnesHut',
            timestep: 0.50,
            stabilization: {iterations: 150}
        },
		nodes: {
            size: 15,
            font: {
                size: 20
            },
            borderWidth: 2,
			borderWidthSelected: 4,
            color:{highlight:{border: '#B20F0F', background: 'red'}}
        },
        edges: {
            width: 4,
			selectionWidth: function (width) {return width*2.5;},
            color:{color:'#2B7CE9', hover:'#2B7CE9', highlight: 'red'}
        },
		interaction: {
          navigationButtons: true,
          keyboard: true,
		  hover: true,
		  tooltipDelay: 500,
          multiselect: true
        }
	};
    var network = new vis.Network(container, data, options);
	var stabil = true;

    network.on("click", function (params) {
        params.event = "[original event]";
		var tmp = " ";


		for (var i = 1; i <= nodes.length; i++) {
        	if (nodes.get(i).id == params.nodes) {
				tmp = nodes.get(i).text;
			};
    	};

		if(params.nodes.length === 0 && params.edges.length > 0) {
			for (var i = 1; i <= edges.length; i++) {
				if (edges.get(i).id == params.edges) {
					tmp = edges.get(i).text;
				};
			};
		};

		document.getElementById('rectangle').innerHTML = '<div style="width:800px;height:100%;text-align:center;border:0px solid #000;">' + tmp + '</div>';
    });

	network.on("stabilized", function (params) {
	if(stabil) {
		network.fit();
		stabil = false;
	};
	});

	network.on("doubleClick", function (params) {
        params.event = "[original event]";
		network.focus(params.nodes);
	});

</script>

<script src="../../googleAnalytics.js"></script>
</body>
</html>
SECOND PART END
'''