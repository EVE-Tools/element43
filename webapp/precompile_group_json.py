import json

from yaml import load

from django.db import connection

from apps.common.util import dictfetchall

#
# This script generated a JSON tree for the market browser and is automatically run with prepare_static.sh
#


def recadder(node):
    """
    Function for recursively traversing the tree.
    """

    if not node['has_items']:
        if not 'children' in node:
            node['children'] = []

        cursor.execute('SELECT * FROM (SELECT * FROM eve_db_invmarketgroup WHERE parent_id = ' + str(node['id']) + ' ORDER BY name) as main ORDER BY has_items')
        res = dictfetchall(cursor)

        for new_node in res:
            node['children'].append(recadder(new_node))

    # Casting and stuff to make dynatree happy
    isFolder = not bool(node['has_items'])
    del node['has_items']
    node['isFolder'] = isFolder
    node['noLink'] = isFolder

    title = node['name']
    del node['name']
    node['title'] = title

    tooltip = node['description']
    del node['description']
    node['tooltip'] = tooltip

    iconid = node['icon_id']
    del node['icon_id']

    # Add proper icon ids
    if (iconid):
        string = icons[iconid]['iconFile']

        # Handle different formats
        if 'res:/UI/Texture/Icons/' in string:
            node['icon'] = string.replace('res:/UI/Texture/Icons/', '')
        elif 'res:/UI/Texture/market/' in string:
            node['icon'] = '22_42.png'
        else:
            # Remove leading zeros
            for i in range(0, 10):
                string = string.replace('0'+str(i), str(i))
            node['icon'] = string.replace('_16_', '').replace('_32_', '').replace('_64_', '').replace('_128_', '') + '.png'
    else:
        # Default icon
        node['icon'] = '22_42.png'

    key = node['id']
    del node['id']
    node['key'] = key

    del node['parent_id']

    return node

icon_yaml = file('iconIDs.yaml', 'r')

icons = load(icon_yaml)

cursor = connection.cursor()

# Select Root Groups
cursor.execute("SELECT * FROM eve_db_invmarketgroup WHERE parent_id IS NULL ORDER BY name")
result = dictfetchall(cursor)

tree = []

# Start traversing
for node in result:
    tree.append(recadder(node))

# Write file into appropiate asset folder
json_file = open("element43/apps/market_data/static/javascripts/groups.json", "w")
json_file.write(json.dumps(tree))
json_file.close()
