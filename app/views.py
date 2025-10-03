from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializer import ProductSerializer


class ProductVerifyView(APIView):
	"""POST /api/verify/ with JSON {"identifier": "0851234567890"}
	Searches barcode, product_id, and batch_code for a match and returns product data.
	"""

	def post(self, request, *args, **kwargs):
		identifier = request.data.get('identifier')
		if not identifier:
			return Response({"detail": "identifier is required"}, status=status.HTTP_400_BAD_REQUEST)

		# Try exact barcode match first
		try:
			product = Product.objects.filter(barcode=identifier).first()
			if not product:
				product = Product.objects.filter(product_id=identifier).first()
			if not product:
				product = Product.objects.filter(batch_code=identifier).first()

			if not product:
				return Response({
					"registered": False,
					"message": "Not Registered: No matching product found. Please contact FDA."
				}, status=status.HTTP_200_OK)

			serializer = ProductSerializer(product)
			data = serializer.data
			data.update({
				"registered": True,
				"message": "Approved" if product.approved else "Not Approved"
			})
			return Response(data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
