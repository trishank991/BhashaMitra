"""Views for Teacher model."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.curriculum.models.teacher import Teacher
from apps.curriculum.serializers.teacher import TeacherSerializer, TeacherDetailSerializer


class TeacherListView(APIView):
    """List all active teachers."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers = Teacher.objects.filter(is_active=True)
        character_type = request.query_params.get('character_type')
        if character_type:
            teachers = teachers.filter(character_type=character_type)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherDetailView(APIView):
    """Retrieve details of a specific teacher."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk, is_active=True)
        serializer = TeacherDetailSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherByCharacterView(APIView):
    """Get teacher by character type (CAT for Peppi, OWL for Gyan)."""
    permission_classes = [IsAuthenticated]

    def get(self, request, character_type):
        teacher = get_object_or_404(
            Teacher,
            character_type=character_type.upper(),
            is_active=True
        )
        serializer = TeacherDetailSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
