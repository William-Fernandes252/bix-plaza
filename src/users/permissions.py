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
                "update",
                "partial_update",
                "destroy",
                "retrieve",
                "me",
            ],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["list"],
            "principal": ["admin", "staff"],
            "effect": "allow",
        },
    ]
