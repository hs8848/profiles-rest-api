from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """Serializes a name field ffor testing our API View"""

    name = serializers.CharField(max_length=10)
