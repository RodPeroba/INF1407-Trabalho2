from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from produto.serializers import ProdutoSerializer
from produto.models import Produto

class CadastroProduto(APIView):
    '''
        View para cadastro de produtos pelo vendedor.
    '''

    @swagger_auto_schema(
        operation_description="Endpoint para cadastro de novos produtos pelo vendedor.",
        responses={
            200: 'OK',
            201:  ProdutoSerializer,
            400: 'Bad Request'
        }
    )
    def get(self, request, user_id, produto_id=None):
        '''
            Retorna uma página para cadastrar ou atualizar o produto.
        '''
        produto = self.getProduto(produto_id)
        if produto_id:
            serializer = ProdutoSerializer(produto)
            return Response({"msg": f"Detalhes do produto {produto_id} para o vendedor {user_id}.",
                             "data": serializer.data
                             },
                            status=status.HTTP_200_OK)
        else:
            return Response({"msg": f"Cadastro de produto para o vendedor {user_id}."},
                        status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
            Cadastra um novo produto.
        '''
        serializer = ProdutoSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, user_id, produto_id):
        '''
            Atualiza os dados de um produto existente.
        '''
        produto = self.getProduto(produto_id)
        if not produto:
            return Response({"msg": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def getProduto(self, produto_id):
        try:
            return Produto.objects.get(id=produto_id)
        except Produto.DoesNotExist:
            return None

class MeusProdutos(APIView):
    '''
        View para listar os produtos do vendedor.
    '''

    @swagger_auto_schema(
        operation_description="Retorna a lista de produtos cadastrados pelo vendedor.",
        responses={
            200: ProdutoSerializer(many=True),
            404: 'Not Found'
        }
    )
    def get(self, request, user_id):
        produtos = Produto.objects.filter(vendedor__id=user_id)
        serializer = ProdutoSerializer(produtos, many=True)
        if produtos and serializer.data:
            return Response({"msg": f"Lista de produtos do vendedor {user_id}.",
                             "data": serializer.data
                             },
                            status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Nenhum produto encontrado."}, status=status.HTTP_404_NOT_FOUND)