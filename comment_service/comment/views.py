from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
import requests
from rest_framework import status


def update_product_score(category, product_id):
    comments = Comment.objects.filter(category=category, product_id=product_id)

    total_confidence = 0.0
    for c in comments:
        if c.confidence is not None:
            if c.sentiment == "Tích cực":
                total_confidence += c.confidence
            elif c.sentiment == "Tiêu cực":
                total_confidence -= c.confidence
            # Trung tính thì không làm gì

    if category == "books":
        url = f"http://localhost:8002/api/books/{product_id}/update-score/"
    elif category == "phones":
        url = f"http://localhost:8008/api/phones/{product_id}/update-score/"
    else:
        url = f"http://localhost:8004/api/clothes/{product_id}/update-score/"

    try:
        requests.post(url, json={"score": total_confidence}, timeout=3)
    except requests.exceptions.RequestException:
        pass  # không ảnh hưởng đến việc tạo comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        data = self.request.data
        content = data.get("content", "")
        sentiment = None
        confidence = None

        if content:
            try:
                response = requests.post(
                    "http://localhost:8009/analyze/",
                    json={"text": content},
                    timeout=3,
                )
                if response.status_code == 200:
                    result = response.json()
                    sentiment = result.get("sentiment")
                    confidence = result.get("confidence")
            except requests.exceptions.RequestException:
                pass

        comment = serializer.save(
            user_id=data.get("user_id"),
            username=data.get("username"),
            product_id=data.get("product_id"),
            category=data.get("category"),
            content=content,
            sentiment=sentiment,
            confidence=confidence,
        )

        update_product_score(comment.category, comment.product_id)

    @action(
        detail=False,
        methods=["get"],
        url_path="by-product/(?P<category>[^/.]+)/(?P<product_id>[^/.]+)",
    )
    def get_by_product(self, request, category=None, product_id=None):
        comments = Comment.objects.filter(product_id=product_id, category=category)
        serializer = self.get_serializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
