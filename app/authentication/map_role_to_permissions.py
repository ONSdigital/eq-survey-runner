from app import settings


def map_role_to_permissions(roles):
    current_user_permissions = []

    for role in roles:
        role_permissions = settings.EQ_ROLE_PERMISSIONS.get(role)

        if role_permissions:
            current_user_permissions.extend(role_permissions)
    return current_user_permissions
