import sys
import os
import copy
import collections
from compiler.ast import flatten
import json

def newReachableGraph(state_space_file, output_file, path, screenWidth, screenHeight, satisfyingStates):
	write_part(firstpart_1, output_file, "w")
	write_size(screenWidth, screenHeight, output_file)
	write_part(firstpart_21, output_file, "a")
	write_size(screenWidth, screenHeight, output_file)
	write_part(firstpart_22, output_file, "a")
	write_part(str(screenWidth - 50), output_file, "a")
	write_part(firstpart_3, output_file, "a")

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

	satisfyingStates = convertStatesToStrings(satisfyingStates)
	satisfyingStates = convertStatesToIDs(satisfyingStates, IDs)
	initial = IDs[data['initial']]
			
	write_part(secondpart_1, output_file, "a")
	write_reachability_part(initial, satisfyingStates, output_file, "a")
	write_part(secondpart_2, output_file, "a")
	write_part(str(screenWidth - 50), output_file, "a")
	write_part(secondpart_3, output_file, "a")
	write_part(str(screenWidth - 50), output_file, "a")
	write_part(secondpart_4, output_file, "a")

	fixPath(output_file, path)

	return output_file

def convertStatesToStrings(states):
	return map(lambda state: "|".join(map(str, state)), states)

def convertStatesToIDs(states, IDdict):
	return map(lambda state: IDdict[state], states)

def fixPath(output_file, path):
	with open(output_file, 'r') as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('**FULLPATH**', path)

	# Write the file out again
	with open(output_file, 'w') as file:
		file.write(filedata)

def write_reachability_part(init, states, output_file, mode):
	with open(output_file, mode) as file:
		file.write("	var fromNode = " + str(init) + ";\n")
		file.write("	var toNode = " + str(states) + ";\n")

"""
Writes one of the two static parts to output.
Both are statically included at the end of this file.
:param me: this file
:param output_file: output html file
:param start: string determining beginning of the part
:param end: string determining end of the part
:param mode: append or write
"""
def write_part(part, output_file, mode):
	with open(output_file, mode) as file:
		file.write(part)

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

def write_size(screenWidth, screenHeight, output_file):
	with open(output_file, "a") as file:
		file.write("            width: " + str(screenWidth-50) + "px;\n")
		file.write("            height: " + str(screenHeight-100) + "px;")


firstpart_1 = \
'''<!doctype html>
<html>
<head>
	<title>Network | Interaction events</title>

	<script type="text/javascript" src="**FULLPATH**/.vis/vis.js"></script>
	<link href="**FULLPATH**/.vis/vis.css" rel="stylesheet" type="text/css"/>

	<style type="text/css">
	   #mynetwork {
'''

firstpart_21 = '''
			border: 1px solid lightgray;
		}
		#rectangle {
			text-align: center;
			font-weight: bold;
		}
		#loadingBar {
			position:absolute;
			top:10px;
			left:10px;
'''
firstpart_22 = '''
			background-color:rgba(200,200,200,0.8);
			-webkit-transition: all 0.5s ease;
			-moz-transition: all 0.5s ease;
			-ms-transition: all 0.5s ease;
			-o-transition: all 0.5s ease;
			transition: all 0.5s ease;
			opacity:1;
		}
		#wrapper {
			position:relative;
			width:900px;
			height:900px;
		}

		#text {
			position:absolute;
			top:8px;
			left:530px;
			width:30px;
			height:50px;
			margin:auto auto auto auto;
			font-size:22px;
			color: #000000;
		}


		div.outerBorder {
			position:relative;
			top:400px;
			width:600px;
			height:44px;
			margin:auto auto auto auto;
			border:8px solid rgba(0,0,0,0.1);
			background: rgb(252,252,252); /* Old browsers */
			background: -moz-linear-gradient(top,  rgba(252,252,252,1) 0%, rgba(237,237,237,1) 100%); /* FF3.6+ */
			background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,rgba(252,252,252,1)), color-stop(100%,rgba(237,237,237,1))); /* Chrome,Safari4+ */
			background: -webkit-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* Chrome10+,Safari5.1+ */
			background: -o-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* Opera 11.10+ */
			background: -ms-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* IE10+ */
			background: linear-gradient(to bottom,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* W3C */
			filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fcfcfc', endColorstr='#ededed',GradientType=0 ); /* IE6-9 */
			border-radius:72px;
			box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
		}

		#border {
			position:absolute;
			top:10px;
			left:10px;
			width:500px;
			height:23px;
			margin:auto auto auto auto;
			box-shadow: 0px 0px 4px rgba(0,0,0,0.2);
			border-radius:10px;
		}

		#bar {
			position:absolute;
			top:0px;
			left:0px;
			width:20px;
			height:20px;
			margin:auto auto auto auto;
			border-radius:11px;
			border:2px solid rgba(30,30,30,0.05);
			background: rgb(0, 173, 246); /* Old browsers */
			box-shadow: 2px 0px 4px rgba(0,0,0,0.4);
		}
}
	</style>
</head>
<body>

<div id="mynetwork"></div>
<div id="rectangle"style="width:'''

firstpart_3 = '''px;height:100%;border:1px solid #000;"> </div>
<div id="loadingBar">
		<div class="outerBorder">
			<div id="text">0%</div>
			<div id="border">
				<div id="bar"></div>
			</div>
		</div>
</div>

<script type="text/javascript">
	// create an array with nodes
		var nodes = new vis.DataSet([
'''

secondpart_1 = '''
	]);

	// create a network
	var container = document.getElementById('mynetwork');
	var data = {
		nodes: nodes,
		edges: edges
	};
	
	var stabil = true;
	
	var options = {
		layout: {randomSeed:2},
		physics: {
			enabled: true,
			barnesHut: {
				gravitationalConstant: -25000,
				centralGravity: 0.5,
				springConstant: 0.5,
				springLength: 200,
				damping: 0.15
			},
			maxVelocity: 50,
			minVelocity: 7.5,
			solver: 'barnesHut',
			timestep: 0.5,
			stabilization: {
						enabled:true,
						iterations:5000,
					},
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
'''

secondpart_2 = '''	var paths = [];
	
	var highlightNodes = [];
	var highlightEdges = [];
	
	var network = new vis.Network(container, data, options);

	network.on("stabilizationProgress", function(params) {
				var maxWidth = 496;
				var minWidth = 20;
				var widthFactor = params.iterations/params.total*10;
				var width = Math.max(minWidth,maxWidth * widthFactor);

				document.getElementById('bar').style.width = width + 'px';
				document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '%';
			});
	network.once("stabilizationIterationsDone", function() {
				document.getElementById('text').innerHTML = '100%';
				document.getElementById('bar').style.width = '496px';
				document.getElementById('loadingBar').style.opacity = 0;
				// really clean the dom element
				setTimeout(function () {document.getElementById('loadingBar').style.display = 'none';}, 500);
	});
	
	network.setOptions(options);

	network.on("click", function (params) {
		params.event = "[original event]";
		
		if(toNode.includes(params.nodes[0])) {
		if(highlightNodes.length >= 1) {
			for (var i = 1; i < highlightNodes.length-1; i++) {		
				var clickedNode = nodes.get(highlightNodes[i]);
				if(!toNode.includes(clickedNode[0]) && fromNode != clickedNode[0]){
					clickedNode.color = {
					border: '#2B7CE9',
					background: '#97C2FC',
					highlight: {
						border: '#B20F0F',
						background: 'red'
						}
					}
					nodes.update(clickedNode);
				}
			}
		}
		if(highlightEdges.length >= 1) {
			for (var i = 0; i < highlightEdges.length; i++) {
					var clickedEdge = highlightEdges[i];
						clickedEdge.color = {
							color:'#2B7CE9',
							hover:'#2B7CE9',
							highlight: 'red'
						}	
					edges.update(clickedEdge);
			};
		}
		
		highlightNodes = [];
			for (var i = 0; i <= toNode.length; i++) {
				if(toNode[i] == params.nodes[0]) {
					for (var j = 0; j < paths[i].length; j++) {
					highlightNodes.push(paths[i][j]);
					}
				}
			}
			highlightEdges = [];
		
		//highlightEdges = [];
		
		
		for (var i = 1; i < highlightNodes.length; i++) {
			for (var j = 1; j <= edges.length; j++) {
				if ((edges.get(j).from == highlightNodes[i]) && (edges.get(j).to == highlightNodes[i-1])) {
					highlightEdges.push(edges.get(j));
					
					var clickedEdge = edges.get(j);
					clickedEdge.color = {
						color: 'LightGreen',
						hover: 'LightGreen',
						highlight: 'LightGreen'
					}	
				edges.update(clickedEdge);
				break;
				}
			}
		}
		
		for (var i = 0; i < highlightNodes.length; i++) {
			for (var j = 1; j <= edges.length; j++) {
				if ((edges.get(j).from == highlightNodes[i]) && (edges.get(j).to == highlightNodes[i-1])) {
					var clickedEdge = edges.get(j);
					clickedEdge.color = {
						color: 'LightGreen',
						hover: 'LightGreen',
						highlight: 'LightGreen'
					}	
				edges.update(clickedEdge);
				break;
				};
			};
		};
		
		if(highlightNodes.length > 1) {
			for (var i = 1; i < highlightNodes.length-1; i++) {		
				var clickedNode = nodes.get(highlightNodes[i]);
				if(!toNode.includes(clickedNode[0]) && fromNode != clickedNode[0]){
					clickedNode.color = {
					border: 'LightGreen',
					background: 'LightGreen',
					highlight: {
						border: 'LightGreen',
						background: 'LightGreen'
						}
					}
					nodes.update(clickedNode);
				}
			}
		}
		}
		
		var tmp = " ";

		for (var i = 1; i <= nodes.length; i++) {
			if (nodes.get(i).id == params.nodes) {
				tmp = nodes.get(i).text;
				break;
			};
		};

		if(params.nodes.length === 0 && params.edges.length > 0) {
			for (var i = 1; i <= edges.length; i++) {
				if (edges.get(i).id == params.edges) {
					tmp = edges.get(i).text;
					break;
				};
			};
		};
		document.getElementById('rectangle').innerHTML = '<div style="width:'''

secondpart_3 = '''px;height:100%;text-align:center;border:0px solid #000;">' + tmp + '</div>';
	});

	network.on("stabilized", function (params) {
	if(stabil) {
		network.fit();
		if(nodes.length > 50)
		options.physics.enabled = false;
		network.setOptions(options);
	};
	stabil = false;
	
	for (var i = 0; i < toNode.length; i++) {
		paths.push(shortestPath([], [], fromNode, toNode[i]));
		clickedNode = nodes.get(toNode[i]);
		clickedNode.color = {
			border: 'green',
			background: 'green',
			highlight: {
				border: 'green',
				background: 'green'
			}
		}
		nodes.update(clickedNode);
	}
	
	clickedNode = nodes.get(fromNode);
	clickedNode.color = {
			border: 'orange',
			background: 'orange',
			highlight: {
				border: 'orange',
				background: 'orange'
			}
		}
		nodes.update(clickedNode);
});

	network.on("doubleClick", function (params) {
		params.event = "[original event]";
		//set to original colors
		if(highlightNodes.length >= 1) {
			for (var i = 1; i < highlightNodes.length-1; i++) {		
				var clickedNode = nodes.get(highlightNodes[i]);
				if(!toNode.includes(clickedNode[0]) && fromNode != clickedNode[0]){
					clickedNode.color = {
					border: '#2B7CE9',
					background: '#97C2FC',
					highlight: {
						border: '#B20F0F',
						background: 'red'
						}
					}
					nodes.update(clickedNode);
				}
			}
		}
		if(highlightEdges.length >= 1) {
			for (var i = 0; i < highlightEdges.length; i++) {
					var clickedEdge = highlightEdges[i];
						clickedEdge.color = {
							color:'#2B7CE9',
							hover:'#2B7CE9',
							highlight: 'red'
						}	
					edges.update(clickedEdge);
			};
		}
		
		highlightNodes = [];
		if(toNode.includes(params.nodes[0])) {
			for (var i = 0; i <= toNode.length; i++) {
				if(toNode[i] == params.nodes[0]) {
					for (var j = 0; j < paths[i].length; j++) {
						highlightNodes.push(paths[i][j]);
					}
				}
			}
			highlightEdges = [];		
		
		for (var i = 1; i < highlightNodes.length; i++) {
			for (var j = 1; j <= edges.length; j++) {
				if ((edges.get(j).from == highlightNodes[i]) && (edges.get(j).to == highlightNodes[i-1])) {
					highlightEdges.push(edges.get(j));
					
					var clickedEdge = edges.get(j);
					clickedEdge.color = {
						color: 'LightGreen',
						hover: 'LightGreen',
						highlight: 'LightGreen'
					}	
				edges.update(clickedEdge);
				break;
				}
			}
		}
		
		for (var i = 0; i < highlightNodes.length; i++) {
			for (var j = 1; j <= edges.length; j++) {
				if ((edges.get(j).from == highlightNodes[i]) && (edges.get(j).to == highlightNodes[i-1])) {
					var clickedEdge = edges.get(j);
					clickedEdge.color = {
						color: 'LightGreen',
						hover: 'LightGreen',
						highlight: 'LightGreen'
					}	
				edges.update(clickedEdge);
				break;
				};
			};
		};
		
		if(highlightNodes.length > 1) {
			for (var i = 1; i < highlightNodes.length-1; i++) {		
				var clickedNode = nodes.get(highlightNodes[i]);
				if(!toNode.includes(clickedNode[0]) && fromNode != clickedNode[0]){
					clickedNode.color = {
						border: 'LightGreen',
						background: 'LightGreen',
						highlight: {
							border: 'LightGreen',
							background: 'LightGreen'
						}
					}
					nodes.update(clickedNode);
				}
			}
		}
	}
});
	

function shortestPath(visited, path, source, target) {
	if(source == target){
		return(source);
	}	
	var tmpNeighbours = [];
	var parents = []
	
	for (var i = 1; i <= edges.length; i++) {
				if (edges.get(i).from == source) {
					if(!visited.includes(edges.get(i).to)){
						tmpNeighbours.push(edges.get(i).to);
						visited.push(edges.get(i).to);
						parents.push([edges.get(i).from,edges.get(i).to]);
					}						
				};
			};
			
	var index = 0;
	while(index < tmpNeighbours.length) {
		
		
		for (var i = 1; i <= edges.length; i++) {
					if (edges.get(i).from == tmpNeighbours[index]) {
						if(!visited.includes(edges.get(i).to)){
							tmpNeighbours.push(edges.get(i).to);
							visited.push(edges.get(i).to);
							parents.push([edges.get(i).from,edges.get(i).to]);
							if(edges.get(i).to == target) {
								var outputX = getShortestPath(source, target, [], parents);
								return outputX;
							}
						}						
					};
				};
				
		index = index + 1;
	}
	return [];
}

function getShortestPath(source, nextNode, path, parents) {
	if(source == nextNode) {
		path.push(nextNode);
		return path;
	} else {
		for (var i = 0; i < parents.length; i++) {
			if(parents[i][1] == nextNode) {
				path.push(nextNode);
				return getShortestPath(source, parents[i][0], path, parents);
			}
		}
	}
}

function print(s) {  // A quick and dirty way to display output.
  s = s || '';
  document.getElementById('rectangle').innerHTML = '<div style="width:'''

secondpart_4 = '''px;height:100%;text-align:center;border:0px solid #000;">' + s + '</div>';
}

function getHexColor(number){
	return "#"+((number)>>>0).toString(16).slice(-6);
}

</script>
</body>
</html>
'''