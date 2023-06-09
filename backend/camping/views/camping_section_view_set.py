from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from camping.models import CampingSection
from camping.serializers import CampingSectionRequestSerializer, CampingSectionResponseSerializer
from camping.services import CampingSectionService


class CampingSectionViewSet(ViewSet):
    queryset = CampingSection.objects.none()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not CampingSection.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if CampingSection.field_exists(field_name):
                if '__in' in k or k[-1] == 's':
                    filters[k] = [
                        int(string) if string.isdigit() else string.strip()
                        for string in v.split(',')
                    ]
                else:
                    filters[k] = v
            else:
                filters_errors[k] = _('Field does not exist')

        if filters_errors:
            return Response(filters_errors, status.HTTP_400_BAD_REQUEST)

        service_response = CampingSectionService.get_camping_sections(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        camping_sections_list_serializer = CampingSectionResponseSerializer(service_response['content'], many=True)
        return Response(camping_sections_list_serializer.data)

    @staticmethod
    def create(request):
        camping_section_serializer = CampingSectionRequestSerializer(data=request.data)
        camping_section_serializer.is_valid(raise_exception=True)

        service_response = CampingSectionService.create_camping_section(camping_section_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_section_serializer = CampingSectionResponseSerializer(service_response['content'])
        return Response(
            response_camping_section_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = CampingSectionService.get_camping_section(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_section = service_response['content']
        self.check_object_permissions(request, camping_section)
        response_camping_section_serializer = CampingSectionResponseSerializer(camping_section)

        return Response(response_camping_section_serializer.data)

    def update(self, request, pk=None):
        service_response = CampingSectionService.get_camping_section(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_section = service_response['content']
        self.check_object_permissions(request, camping_section)

        camping_section_serializer = CampingSectionRequestSerializer(
            camping_section,
            data=request.data,
        )
        camping_section_serializer.is_valid(raise_exception=True)

        service_response = CampingSectionService.update_camping_section(pk, camping_section_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_section_serializer = CampingSectionResponseSerializer(service_response['content'])
        return Response(
            response_camping_section_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = CampingSectionService.get_camping_section(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_section = service_response['content']
        self.check_object_permissions(request, camping_section)

        camping_section_serializer = CampingSectionRequestSerializer(
            camping_section,
            data=request.data,
            partial=True,
        )
        camping_section_serializer.is_valid(raise_exception=True)

        service_response = CampingSectionService.update_camping_section(pk, camping_section_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_section_serializer = CampingSectionResponseSerializer(service_response['content'])
        return Response(
            response_camping_section_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = CampingSectionService.get_camping_section(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_section = service_response['content']
        self.check_object_permissions(request, camping_section)

        service_response = CampingSectionService.delete_camping_section(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': _('Camping section has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
