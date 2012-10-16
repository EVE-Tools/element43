# Models
from eve_db.models import InvMarketGroup


def group_breadcrumbs(groupid):
    """
    Recursively searches through all parent groups for generating breadcrumbs.
    """
    breadcrumbs = []
    current_group = groupid
    generating = True

    while generating:
        if InvMarketGroup.objects.get(id=current_group).parent != None:
            current_group_object = InvMarketGroup.objects.get(id=current_group)
            breadcrumbs.append(current_group_object)
            current_group = current_group_object.parent.id
        else:
            current_group_object = InvMarketGroup.objects.get(id=current_group)
            breadcrumbs.append(current_group_object)
            generating = False

    return reversed(breadcrumbs)


def group_ids(groupid):
    """
    Recursively searches through all parent groups for generating tree paths.
    """
    breadcrumbs = []
    current_group = groupid
    generating = True

    while generating:
        if InvMarketGroup.objects.get(id=current_group).parent != None:
            current_group_object = InvMarketGroup.objects.get(id=current_group)
            breadcrumbs.append(current_group_object.id)
            current_group = current_group_object.parent.id
        else:
            current_group_object = InvMarketGroup.objects.get(id=current_group)
            breadcrumbs.append(current_group_object.id)
            generating = False

    return reversed(breadcrumbs)
