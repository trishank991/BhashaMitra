"""Views for Classroom model."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.curriculum.models.classroom import Classroom
from apps.curriculum.models.level import CurriculumLevel
from apps.curriculum.serializers.classroom import ClassroomSerializer, ClassroomDetailSerializer


class ClassroomListView(APIView):
    """List all active classrooms."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classrooms = Classroom.objects.filter(is_active=True).select_related('level')
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomDetailView(APIView):
    """Retrieve details of a specific classroom."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        classroom = get_object_or_404(
            Classroom.objects.select_related('level'), pk=pk, is_active=True
        )
        serializer = ClassroomDetailSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomByLevelView(APIView):
    """Get classroom for a specific level."""
    permission_classes = [IsAuthenticated]

    def get(self, request, level_code):
        level = get_object_or_404(CurriculumLevel, code=level_code, is_active=True)
        try:
            classroom = level.classroom
        except Classroom.DoesNotExist:
            return Response({'detail': 'No classroom found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomDetailSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)
