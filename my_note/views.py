from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from my_note.models import MyNote
from my_note.serializers import MyNoteSerializer


class MyNoteListView(APIView):
    """
    Create new note or list all notes.
    """

    def get(self, request, format=None):
        notes = MyNote.objects.all()
        serializer = MyNoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyNoteDetailView(APIView):
    """
    Retrieve, update or delete a note instance.
    """
    def get_object(self, pk):
        try:
            return MyNote.objects.get(pk=pk)
        except MyNote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = MyNoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = MyNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def favourite(self, request, pk, format=None):
        return Response({"message": "Added to favourite"})


@api_view(['GET'])
def set_favourite(request, pk):
    try:
        note = MyNote.objects.get(pk=pk)
    except MyNote.DoesNotExist:
        raise Http404

    if note.is_favourite:
        return Response({"message": "Already marked as favourite"})

    total_favourite_notes = MyNote.objects.filter(is_favourite=True).count()
    if total_favourite_notes >= 3:
        return Response({"message": "Cannot mark more than 3 notes as favourite"})

    note.is_favourite = True
    note.save()
    return Response({"message": "Marked as favourite"})
