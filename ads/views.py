from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AdSerializers
from .models import Ad
from .pagination import StandardPagination
from rest_framework.parsers import MultiPartParser
from .permissionss import IsUserAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter


class AdView(APIView, StandardPagination):
    serializer_class = AdSerializers

    def get(self, request):
        queryset = Ad.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializers(instance=result, many=True)
        return self.get_paginated_response(serializer.data)


class CreatedView(APIView):
    serializer_class = AdSerializers
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AdSerializers(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailAdView(APIView):
    serializer_class = AdSerializers
    permission_classes = (IsAuthenticated, IsUserAuthenticated)
    parser_classes = [MultiPartParser]

    def get(self, request, pk):
        query = Ad.objects.get(id=pk)
        serializer = AdSerializers(instance=query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Ad.objects.get(id=pk)
        self.check_object_permissions(request, query)
        serializer = AdSerializers(data=request.data, instance=query)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = Ad.objects.get(id=pk)
        self.check_object_permissions(request, query)
        query.delete()
        return Response({query.title: 'deleted'})


class AdSearchView(APIView, StandardPagination):
    serializer_class = AdSerializers

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='q',
                type=str,
                location=OpenApiParameter.QUERY,
                description='جستجو در عنوان و توضیحات آگهی',
                required=True
            )
        ]
    )
    def get(self, request):
        q = request.GET.get('q')
        queryset = Ad.objects.filter(Q(title=q) | Q(caption=q))
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializers(instance=result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
