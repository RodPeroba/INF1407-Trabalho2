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
    def get(self, request, categoria=None):
        vendas_produtos = Produto.objects.all()
        categoria_choices = Categoria.choices
        categorias = []
        for choice in categoria_choices:
            categorias.append(choice[1])
        serializer = ProdutoSerializer(vendas_produtos, many=True)
        data = {
            "produtos": serializer.data,
            "categorias": categorias
        }
        print("Vendas Produtos:", vendas_produtos)
        print("Serializer Data:", serializer.data)
        print("Categorias:", categorias)
        return Response(
                        data,
                        status=status.HTTP_200_OK
                        )

class PaginaCategoria(APIView):
    '''
        Resposta para a página de categoria do site.
    '''

    @swagger_auto_schema(
        operation_description="Retorna a lista de produtos filtrados por categoria.",
        responses={
            200: ProdutoSerializer,
            404: 'Not Found'
        }
    )
    def get(self, request, categoria):
        vendas_produtos = Produto.objects.filter(categoria=categoria)
        categoria_choices = Categoria.choices
        categorias = []
        for choice in categoria_choices:
            categorias.append(choice[1])
        serializer = ProdutoSerializer(vendas_produtos, many=True)
        data = {
            "produtos": serializer.data,
            "categorias": categorias,
            "categoria": categoria
        }
        if serializer.is_valid:
            return Response(
                            data,
                            status=status.HTTP_200_OK
                            )
        else:
            return Response(
                            serializer.errors,
                            status=status.HTTP_404_NOT_FOUND
                            )

class PaginaProduto(APIView):
    '''
        Resposta para a página de detalhes do produto.
    '''

    @swagger_auto_schema(
        operation_description="Retorna os detalhes de um produto específico.",
        responses={
            200: ProdutoSerializer(many=True),
            400: ProdutoSerializer,
            404: 'Not Found'
        }
    )
    def get(self, request, produto_id):
        try:
            produto = Produto.objects.get(id=produto_id)
            serializer = ProdutoSerializer(produto)
            if serializer.is_valid:
                return Response(
                                serializer.data,
                                status=status.HTTP_200_OK
                                )
            else:
                return Response(
                                serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )
        except Produto.DoesNotExist:
            return Response(
                            {"msg": "Produto não encontrado."},
                            status=status.HTTP_404_NOT_FOUND
                            )
        
    def delete(self, request, produto_id):
        '''
            Apaga um produto específico.
        '''
        try:
            produto = Produto.objects.get(id=produto_id)
            produto.delete()
            return Response(
                            {"msg": "Produto deletado com sucesso."},
                            status=status.HTTP_200_OK
                            )
        except Produto.DoesNotExist:
            return Response(
                            {"msg": "Produto não encontrado."},
                            status=status.HTTP_404_NOT_FOUND
                            )