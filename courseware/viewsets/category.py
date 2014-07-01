"""
    This file contains viewsets for ParentCategory and Category models.

    Functionality Provided:
    ParentCategory:
        + Add, Update, PartialUpdate, Delete - (IsAdminUser)
        + List, Retrieve - (everyone allowed)

    Category:
        + Add, Update, PartialUpdate, Delete - (IsAdminUser)
        + List, Retrieve - (everyone allowed)

"""

from courseware.models import ParentCategory, Category
from courseware.vsserializers.category import ParentCategorySerializer, CategorySerializer
from courseware import permissions

from rest_framework import viewsets


class ParentCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ParentCategory. All operations permitted.
    """
    model = ParentCategory
    serializer_class = ParentCategorySerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category Model. All operations permitted.
    """
    model = Category
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned categories to a given parentcategory.
        """
        queryset = Category.objects.all()
        parent = self.request.QUERY_PARAMS.get('parent', None)
        if parent is not None:
            queryset = queryset.filter(parent__id=parent)
        return queryset
