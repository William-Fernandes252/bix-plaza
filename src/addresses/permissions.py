from rest_access_policy import AccessPolicy


class AddressAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": [
                "create",
                "update",
                "partial_update",
                "destroy",
            ],
            "principal": ["admin", "staff"],
            "effect": "allow",
        },
        {
            "action": [
                "list",
                "retrieve",
            ],
            "principal": "*",
            "effect": "allow",
        },
    ]
