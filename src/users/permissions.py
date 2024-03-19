from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": ["admin", "anonymous"],
            "effect": "allow",
        },
        {
            "action": [
                "create",
                "update",
                "partial_update",
                "destroy",
                "list",
                "retrieve",
                "me",
            ],
            "principal": "authenticated",
            "effect": "allow",
        },
    ]
