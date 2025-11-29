"""GraphQL schema for Todo application including User and Todo models with JWT authentication.

author: tonipat047@gmail.com
"""

import graphene
import graphql_jwt
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Todo


# User List Schema
class UserType(DjangoObjectType):
    """GraphQL type for User model"""
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CreateUser(graphene.Mutation):
    """Create a new user"""
    user = graphene.Field(UserType)

    class Arguments:
        """Arguments for creating a new user"""
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    """Update an existing user"""
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, id, username=None, email=None, password=None):
        user = User.objects.get(pk=id)
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    """Delete an existing user"""
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(success=True)


# Todo List Schema
class TodoType(DjangoObjectType):
    """GraphQL type for Todo model"""
    class Meta:
        model = Todo
        fields = ("id", "text", "completed", "created_at", "owner")


class Query(graphene.ObjectType):
    """GraphQL query schema"""
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, id=graphene.Int())
    me = graphene.Field(UserType)

    @login_required
    def resolve_todos(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Todo.objects.filter(owner=user).order_by("-created_at").all()

    @login_required
    def resolve_todo(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Todo.objects.get(pk=id, owner=user)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user


class CreateTodo(graphene.Mutation):
    """Create a new todo"""
    todo = graphene.Field(TodoType)

    class Arguments:
        text = graphene.String(required=True)

    @login_required
    def mutate(self, info, text):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        todo = Todo.objects.create(text=text, owner=user)
        return CreateTodo(todo=todo)


class UpdateTodo(graphene.Mutation):
    """Update an existing todo"""
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String()
        completed = graphene.Boolean()

    @login_required
    def mutate(self, info, id, text=None, completed=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        todo = Todo.objects.get(pk=id, owner=user)
        if text is not None:
            todo.text = text
        if completed is not None:
            todo.completed = completed
        todo.save()
        return UpdateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    """Delete an existing todo"""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        todo = Todo.objects.get(pk=id, owner=user)
        todo.delete()
        return DeleteTodo(ok=True)


class Mutation(graphene.ObjectType):
    """GraphQL mutation schema"""
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

    # users
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    # jwt token handling
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
