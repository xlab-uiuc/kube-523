import json

def breadth(x):
    queue = [x]
    curr_breadth = 0
    while len(queue) > 0:
        curr = queue.pop()
        if type(curr) is dict and curr:
            for key in curr:
                queue.append(curr[key])
        if type(curr) is list:
            for item in curr:
                queue.append(item)
        else:
            curr_breadth += 1
    return curr_breadth

def depth(x):
    # Code from https://stackoverflow.com/questions/30928331/how-to-find-the-maximum-depth-of-a-python-dictionary-or-json-object
    # Seems very similar to depth first search, but we are finding the maximum depth here
    if type(x) is dict and x:
        return 1 + max(depth(x[a]) for a in x)
    if type(x) is list and x:
        return 1 + max(depth(a) for a in x)
    return 0

if __name__ == "__main__":
    f = open('scaledobjectscrd.json')
 
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    print("Depth of entire CRD:", depth(data))
    print("Breadth of entire CRD:", breadth(data))
    # print(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"])
    # print("Depth of openAPIV3Schema: ", depth(data["spec"]["versions"]))
    print("Depth of openAPIV3Schema: ", depth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]))
    print("Breadth of openAPIV3Schema: ", breadth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]))
    print("Depth of horizontalPodAutoscalerConfig: ", depth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["horizontalPodAutoscalerConfig"]))
    print("Breadth of horizontalPodAutoscalerConfig: ", breadth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["horizontalPodAutoscalerConfig"]))
    print("Depth of restoreToOriginalReplicaCount: ", depth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["restoreToOriginalReplicaCount"]))
    print("Breadth of restoreToOriginalReplicaCount: ", breadth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["restoreToOriginalReplicaCount"]))
    print("Depth of scalingModifiers: ", depth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["scalingModifiers"]))
    print("Breadth of scalingModifiers: ", breadth(data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]["advanced"]["properties"]["scalingModifiers"]))

    # Closing file
    f.close()