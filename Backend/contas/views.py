# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import logout
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer


class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_summary="Obter username pelo Token",
        operation_description='''
            Endpoint para obter o username associado a um token de autenticação.
            Forneça o token no cabeçalho Authorization para receber o nome de usuário.
            Retorna 200 OK com o nome de usuário em caso de sucesso ou 404 Not Found se o token for inválido.
        ''',
        security=[{'Token': []}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token de autenticação no formato: Token <seu_token_aqui>",
                type=openapi.TYPE_STRING,
                required=True,
                default='Token ',
            ),
        ],
        responses={
            status.HTTP_200_OK: "Nome de usuário obtido com sucesso",
            status.HTTP_404_NOT_FOUND: "Token inválido",
        },
    )
    def get(self, request, *args, **kwargs):
        '''
        Endpoint que recebe um token e retorna o username
        '''
        token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            return Response({'username': user.username}, status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response({'username': 'visitante'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Obter Token de Autenticação",
        operation_description='''
            Endpoint para autenticar um usuário e obter um token de autenticação.
            Forneça o nome de usuário e a senha para receber um token.
            Retorna 200 OK com o token em caso de sucesso ou 401 Unauthorized em caso de falha.
        ''',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password'],
        ),
        responses={
            status.HTTP_200_OK: "Token gerado com sucesso",
            status.HTTP_401_UNAUTHORIZED: "Credenciais inválidas",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'token': token.key,
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Realiza logout do usuário, apagando o seu token',
        operation_summary='Realiza logout',
        security=[{'Token': []}],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              type=openapi.TYPE_STRING, default='token ',
                              description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                              ),
        ],
        request_body=None,
        responses={
            status.HTTP_200_OK: 'User logged out',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated',
            status.HTTP_403_FORBIDDEN: 'User not authorized to logout',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Erro no servidor',
        },
    )
    def delete(self, request):
        '''
        Endpoint para realizar logout do usuário, apagando o seu token.
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            tokenObject = Token.objects.get(key=token)
        except (Token.DoesNotExist, IndexError):
            return Response(
                {"msg": "Token inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = tokenObject.user
        if user.is_authenticated:
            request.user = user
            logout(request)
            token = Token.objects.get(user=user)
            token.delete()
            return Response(
                {"msg": "Logout realizado com sucesso."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"msg": "Usuário não autenticado."},
                status=status.HTTP_403_FORBIDDEN
            )
        
    @swagger_auto_schema(
        operation_description='Troca a senha do usuário, atualiza o token em caso de sucesso',
        operation_summary='Troca a senha do usuário',
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                default='token ',
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['old_password', 'new_password'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Senha alterada com sucesso.",
                examples={
                    "application/json": {"message": "Senha alterada com sucesso."}}
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na solicitação.",
                examples={
                    "application/json": {"old_password": ["Senha atual incorreta."]}}
            ),
            status.HTTP_401_UNAUTHORIZED: "Usuário não autenticado.",
        },
    )
    def put(self, request):
        '''
        Endpoint para trocar a senha do usuário autenticado.
        '''
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  # token
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        oldPassword = request.data.get('old_password')
        newPassword = request.data.get('new_password')

        # Verificar se a senha atual está correta
        if user.check_password(oldPassword):
            # Alterar a senha e atualizar o token
            user.set_password(newPassword)
            user.save()
            # Atualizar token
            try:
                token = Token.objects.get(user=user)
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                pass
            return Response({'token': token.key, "message": "Senha alterada com sucesso."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)
        



class CreateAccountView(APIView):
    @swagger_auto_schema(
        operation_summary="Criar nova conta",
        operation_description="Cria uma nova conta de usuário.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Nome de usuário desejado',
                    example='joao_silva'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Senha desejada',
                    example='senha123'
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Email do usuário',
                    example='joao@example.com'
                ),
                "group": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Grupo do usuário: 1 para Vendedor, 2 para Comprador',
                    example='2'
                ),
            },
            required=['username', 'password'],
        ),
        responses={
            201: openapi.Response(
                description='Conta criada com sucesso',
                examples={
                    'application/json': {
                        'id': 1,
                        'username': 'joao_silva',
                        'email': 'joao@example.com'
                    }
                }
            ),
            400: 'Dados inválidos ou nome de usuário já existe',
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Retorna dados do usuário sem a senha
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Conta criada com sucesso!'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
