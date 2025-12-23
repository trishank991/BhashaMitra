"""Views for Songs."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.curriculum.models import Song, CurriculumLevel
from apps.curriculum.serializers.songs import SongSerializer, SongListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def song_list(request):
    """Get list of songs, optionally filtered by level."""
    level_id = request.query_params.get('level')
    category = request.query_params.get('category')

    queryset = Song.objects.filter(is_active=True).select_related('level')

    if level_id:
        queryset = queryset.filter(level_id=level_id)

    if category:
        queryset = queryset.filter(category=category)

    serializer = SongListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def song_detail(request, song_id):
    """Get a single song with full details."""
    song = get_object_or_404(Song.objects.select_related('level'), id=song_id, is_active=True)
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def songs_by_level(request, level_code):
    """Get all songs for a specific level."""
    level = get_object_or_404(CurriculumLevel, code=level_code)
    songs = Song.objects.filter(level=level, is_active=True).order_by('order')
    serializer = SongListSerializer(songs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
