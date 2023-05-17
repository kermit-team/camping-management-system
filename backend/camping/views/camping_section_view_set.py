from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import CampingSection
from camping.serializers import CampingSectionRequestSerializer, CampingSectionResponseSerializer
from camping.services import CampingSectionService


class CampingSectionViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not CampingSection.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if CampingSection.field_exists(k) if '__' not in k else CampingSection.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_camping_sections = CampingSectionService.get_camping_sections(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        camping_sections_list_serializer = CampingSectionResponseSerializer(
            queryset_of_camping_sections, 
            many = True,
            context = serializer_context,
        )

        return Response(camping_sections_list_serializer.data)

    def create(self, request):        
        camping_section_serializer = CampingSectionRequestSerializer(data=request.data)
        camping_section_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_camping_section = CampingSectionService.create_camping_section(camping_section_serializer.validated_data)
        if created_camping_section:
            
            response_camping_section_serializer = CampingSectionResponseSerializer(
                created_camping_section,
                context = serializer_context,
            )

            return Response(
                response_camping_section_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        camping_section = CampingSectionService.get_camping_section(pk)
        if not camping_section:
            raise Http404
        self.check_object_permissions(self.request, camping_section)
        serializer_context = {
            'request': request,
        }

        response_camping_section_serializer = CampingSectionResponseSerializer(
            camping_section,
            context = serializer_context,
        )

        return Response(response_camping_section_serializer.data)

    def update(self, request, pk=None):
        camping_section = CampingSectionService.get_camping_section(pk)
        if not camping_section:
            raise Http404
        self.check_object_permissions(self.request, camping_section)
        serializer_context = {
            'request': request,
        }
        
        camping_section_serializer = CampingSectionRequestSerializer(
            camping_section, 
            data = request.data,
        )
        camping_section_serializer.is_valid(raise_exception=True)

        updated_camping_section = CampingSectionService.update_camping_section(pk, camping_section_serializer.validated_data)
        response_camping_section_serializer = CampingSectionResponseSerializer(
            updated_camping_section,
            context = serializer_context,
        )

        return Response(
            response_camping_section_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        camping_section = CampingSectionService.get_camping_section(pk)
        if not camping_section:
            raise Http404
        self.check_object_permissions(self.request, camping_section)
        serializer_context = {
            'request': request,
        }        

        camping_section_serializer = CampingSectionRequestSerializer(
            camping_section, 
            data = request.data,
            partial = True,
        )
        camping_section_serializer.is_valid(raise_exception=True)

        updated_camping_section = CampingSectionService.update_camping_section(pk, camping_section_serializer.validated_data)
        response_camping_section_serializer = CampingSectionResponseSerializer(
            updated_camping_section,
            context = serializer_context,
        )

        return Response(
            response_camping_section_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        camping_section = CampingSectionService.get_camping_section(pk)
        if not camping_section:
            raise Http404
        self.check_object_permissions(self.request, camping_section)

        if CampingSectionService.delete_camping_section(pk):
            return Response(
                {'message': _('Camping section has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        