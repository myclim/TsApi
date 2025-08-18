from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.permissions import UserCustomPermission

from goods.models import ProductModel
from goods.serializers import ProductSerializer


class ResourceView(APIView):
    permission_classes = [UserCustomPermission]

    def get_required_permission(self):
        method_permission_map = {
            "GET": "view",
            "POST": "create",
            "PUT": "update",
            "DELETE": "delete",
        }
        return method_permission_map.get(self.request.method)

    def check_permissions(self, request):
        self.required_permission = self.get_required_permission()
        super().check_permissions(request)

    def get(self, request):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({"id": product.id}, status=200)
        return Response(serializer.errors, status=400)

    def put(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        product.delete()
        return Response(status=200)
