from django.urls import path
from goods.views import ResourceView

app_name = 'goods'

urlpatterns = [
    path('products/', ResourceView.as_view()),
    path('products/<int:product_id>/', ResourceView.as_view()),
]