import yaml


with open("./crunchydata-postgres-crd.yaml", "r") as stream:
    crd = yaml.safe_load(stream)


schemaRoot = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]


def analyze(schema: dict) -> None:
    stats = [0, 0, 0]                 #    totalNodeCount, leafNodeCount, totaldepths

    def dfs(node: dict, depth = 0) -> None:

        stats[0] += 1
        properties = node.get("properties", {})
        nodeType = node.get("type")

        if nodeType != "object":      # primitive types
            stats[1] += 1
            stats[2] += depth
            return 
        
        for p in properties.values():
            dfs(p, depth + 1)
    
    dfs(schema)
    stats[2] = round(stats[2] / stats[1])

    totalNodeCount, leafNodeCount, avgDepths = stats

    result = "totalNodes: {}, leafNodes: {}, average depth: {}".format(totalNodeCount, leafNodeCount, avgDepths)
    print(result)


analyze(schemaRoot)






