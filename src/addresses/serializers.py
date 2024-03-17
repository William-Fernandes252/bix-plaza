from rest_framework import serializers


from addresses import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
        read_only_fields = ("id",)
