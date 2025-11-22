from django.urls import path
from vendedor import views

app_name = 'vendedor'

urlpatterns = [
    path("cadastro_produto/", views.CadastroProduto.as_view(), name="cadastro_produto"),
    path("cadastro_produto/<int:user_id>/", views.CadastroProduto.as_view(), name="cadastro_produto_user"),
    path("cadastro_produto/<int:user_id>/<int:produto_id>/", views.CadastroProduto.as_view(), name="atualiza_produto_user"),
    path("meus_produtos/<int:user_id>/", views.MeusProdutos.as_view(), name="meus_produtos"),
]