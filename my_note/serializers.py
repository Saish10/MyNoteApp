from rest_framework import serializers

from my_note.models import MyNote


class MyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyNote
        fields = ['id', 'created_by', 'description', 'is_favourite', 'date_added', 'date_modified', 'is_active']
