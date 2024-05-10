import yaml

stream = open('apps.kubeblocks.io_clusters.yaml', 'r')
obj = yaml.safe_load(stream)

target = obj['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
print(target.keys())

def find_depth(node, depths): 
    if type(node) == dict: 
        for child in node.values():
            child_depths = []
            find_depth(child, child_depths)
            depths.append(max(child_depths) + 1)

    elif type(node) == list:
        for child in node:
            child_depths = []
            find_depth(child, child_depths)
            depths.append(max(child_depths) + 1)

    else:
        depths.append(0)

targetTest = []
find_depth(target, targetTest)
print(list(zip(target.keys(), targetTest)))

compSpecsTest = []
find_depth(target['componentSpecs'], compSpecsTest)
print(list(zip(target['componentSpecs'].keys(), compSpecsTest)))

shardingSpecsTest = []
find_depth(target['shardingSpecs'], shardingSpecsTest)
print(list(zip(target['shardingSpecs'].keys(), shardingSpecsTest)))
