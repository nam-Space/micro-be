from rest_framework import viewsets
from .models import Clothes
from .serializers import ClothesSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer

    def get_queryset(self):
        return Clothes.objects.all().order_by("-score")  # Sắp xếp theo score giảm dần

    @action(detail=True, methods=["post"], url_path="update-score")
    def update_score(self, request, pk=None):
        try:
            clothes = self.get_object()
            score = request.data.get("score")

            if score is None:
                return Response(
                    {"error": "Missing 'score'"}, status=status.HTTP_400_BAD_REQUEST
                )

            clothes.score = float(score)
            clothes.save()
            return Response(
                {"success": True, "score": clothes.score}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
