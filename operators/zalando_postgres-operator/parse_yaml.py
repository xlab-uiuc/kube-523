#!/usr/bin/env python3

import yaml

with open('./acid.zalan.do_postgresqls.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    postgresql_crd = yaml.load(file, Loader=yaml.FullLoader)

    # get keys under spec
    top_level = postgresql_crd['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties']
    top_level_keys = postgresql_crd['spec']['versions'][0]['schema']['openAPIV3Schema']['properties']['spec']['properties'].keys()
    print('Top level keys under spec:')
    for key in top_level_keys:
        print('`'+key+'`')

    print()
    # get keys under preparedDatabases
    print('`prepareDatabases` key under spec:')
    prepareDatabases_keys = top_level['preparedDatabases']['additionalProperties']['properties'].keys()
    for key in prepareDatabases_keys:
        print('`'+key+'`')

    print()
    # get keys under postgresql
    print('`postgresql` key under spec:')
    postgresql_keys = top_level['postgresql']['properties'].keys()
    for key in postgresql_keys:
        print('`'+key+'`')

    print()
    # get keys under patroni
    print('`patroni` key under spec:')
    patroni_keys = top_level['patroni']['properties'].keys()
    for key in patroni_keys:
        print('`'+key+'`')

    print()
    # get keys under resources
    print('`resources` key under spec:')
    resources_keys = top_level['resources']['properties'].keys()
    for key in resources_keys:
        print('`'+key+'`')
        for sub_key in top_level['resources']['properties'][key]['properties'].keys():
            print('    `'+sub_key+'`')

    print()
    # get keys under clone
    print('`clone` key under spec:')
    clone_keys = top_level['clone']['properties'].keys()
    for key in clone_keys:
        print('`'+key+'`')

    # calculate the complexity of the CRD
    # complexity = number of keys under spec * depth of the this keys
    complexity = 0
    deepest_depth = 0
    for key in top_level_keys:
        def calculate_complexity(key,relative_top_level=top_level, depth=1) -> int:
            if type(relative_top_level) == dict and key in relative_top_level and 'properties' in relative_top_level[key]:
                max_depth = 0
                for sub_key in relative_top_level[key]['properties'].keys():
                    tmp_depth = depth + 1
                    tmp_depth = calculate_complexity(sub_key, relative_top_level=relative_top_level[key]['properties'], depth=tmp_depth)
                    if tmp_depth > max_depth:
                        max_depth = tmp_depth
                return max_depth
            elif type(relative_top_level) == dict and key in relative_top_level and 'additionalProperties' in relative_top_level[key]\
                    and 'properties' in relative_top_level[key]['additionalProperties']:
                max_depth = 0
                for sub_key in relative_top_level[key]['additionalProperties']['properties'].keys():
                    tmp_depth = depth + 1
                    tmp_depth = calculate_complexity(sub_key, relative_top_level=relative_top_level[key]['additionalProperties'], depth=tmp_depth)
                    if tmp_depth > max_depth:
                        max_depth = tmp_depth
                return max_depth
            else:
                return depth

        depth = calculate_complexity(key, relative_top_level=top_level, depth=1)
        print('Depth of `'+key+'`:', depth)
        if depth > deepest_depth:
            deepest_depth = depth
        complexity += depth

    print()
    print('Complexity:', complexity)
    print('Deepest depth:', deepest_depth)
