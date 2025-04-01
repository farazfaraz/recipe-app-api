"""
This code defines a Django REST framework (DRF) API for managing recipes and tags.
Converts model instances into JSON responses.
Defines how data is received and validated in API requests.
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields  = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False) # by default nested serializers are read_only, so we have to override the create functionality
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id'] # meaning it cannot be changed by users.

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', []) # Extract tags from request data
        recipe = Recipe.objects.create(**validated_data) # Create the recipe
        auth_user = self.context['request'].user # Get the authenticated user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user, # Ensure the tag is associated with the user
                **tag, # Create or get the tag based on the name
            )
            recipe.tags.add(tag_obj) # Add the tag to the recipe

        return recipe

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
