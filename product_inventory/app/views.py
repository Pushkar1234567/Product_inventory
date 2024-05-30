from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status


class CreateProduct(APIView):

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request):
        try:
            data = request.data
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "message": "Product created successfully",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductRetrieveUpdateDestroy(APIView):

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            if not product:
                response_data = {"message": "Provide the id"}
                response_status = status.HTTP_401_BAD_REQUEST
            else:
                serializer = ProductSerializer(product)
                response_data = {"message": "Product found", "data": serializer.data}
                response_status = status.HTTP_200_OK
            return Response(response_data, status=response_status)
        except Product.DoesNotExist:
            response_data = {"message": "Product not found"}
            response_status = status.HTTP_404_NOT_FOUND
            return Response(response_data, status=response_status)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            if not product:
                response_data = {"message": "Product not found"}
                response_status = status.HTTP_404_NOT_FOUND
                return Response(response_data, status=response_status)
            
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {"message": "Product updated successfully", "data": serializer.data}
                response_status = status.HTTP_200_OK
            else:
                response_data = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
            
            return Response(response_data, status=response_status)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            if not product:
                response_data = {"message": "Product not found"}
                response_status = status.HTTP_404_NOT_FOUND
                return Response(response_data, status=response_status)
            
            product.delete()
            response_data = {"message": "Product DELETED"}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
