from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field ffor testing our API View"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    # Use this Meta class to configure the serializer to point to a specific model in our project
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        
        # uses a dictionary to provide additional arguments to each field
        # style is used by the browsable API to render the password input correctly i.e. not show the password 
        # but show dots instead
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""

        # This create function overrides the default create function of the ModelSerializer
        # which would just create the user with the password as plain text.
        # Instead, we use the create_user method we created in the model (refer to models.py file)
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""

        # If the password is included in the update, we need to handle it specially
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        # Call the superclass method to handle the rest of the updates
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}

        