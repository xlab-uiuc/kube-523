import yaml


with open("./crunchydata-postgres-crd.yaml", "r") as stream:
    crd = yaml.safe_load(stream)


schemaRoot = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]


def analyze(schema: dict) -> None:
    stats = [0, 0, 0]                 #    totalNodeCount, leafNodeCount, totaldepths

    def dfs(node: dict, depth = 0) -> None:
        stats[0] += 1
        nodeType = node.get("type")
        children = node.get("properties", {}) if nodeType == "object" else node.get("items", {}).get("properties", {})
        if nodeType not in  ["object", "array"] or len(children) == 0:      # leaf node
            stats[1] += 1
            stats[2] += depth
            return 
        
        for c in children.values():
            dfs(c, depth + 1)
    
    dfs(schema)
    stats[2] = "{:0.2f}".format(stats[2] / stats[1])

    totalNodeCount, leafNodeCount, avgDepths = stats

    result = "totalNodes: {}, leafNodes: {}, average depth: {}".format(totalNodeCount, leafNodeCount, avgDepths)
    print(result)


analyze(schemaRoot)






