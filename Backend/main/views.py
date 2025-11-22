from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from produto.models import Produto, Categoria
from produto.serializers import ProdutoSerializer
from drf_yasg.utils import swagger_auto_schema


class HomePage(APIView):
    '''
        Resposta para a homepage do site.
    '''

    # TODO Adicionar @swagger_auto_schema
    @swagger_auto_schema(
        operation_description="Retorna uma mensagem de boas-vindas e a lista de produtos disponíveis.",
        responses={
            200: ProdutoSerializer(many=True),
            404: 'Not Found'
        }
    )
    def get(self, request):
        vendas_produtos = Produto.objects.all()
        categoria_choices = Categoria.choices
        categorias = []
        for choice in categoria_choices:
            categorias.append(choice[1])
        serializer = ProdutoSerializer(vendas_produtos, many=True)
        print("Vendas Produtos:", vendas_produtos)
        print("Serializer Data:", serializer.data)
        print("Categorias:", categorias)
        return Response({"msg": "Welcome to the Comprador Home Page",
                            "data": serializer.data,
                            "categories": categorias
                            },
                        status=status.HTTP_200_OK)
       