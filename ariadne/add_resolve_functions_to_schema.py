from graphql import GraphQLObjectType, GraphQLScalarType, GraphQLSchema

from .default_resolver import default_resolver


def add_resolve_functions_to_schema(schema: GraphQLSchema, resolvers: dict):
    for type_name, type_object in schema.get_type_map().items():
        if isinstance(type_object, GraphQLObjectType):
            add_resolve_functions_to_object(type_name, type_object, resolvers)
        if isinstance(type_object, GraphQLScalarType):
            add_resolve_function_to_scalar(type_name, type_object, resolvers)


def add_resolve_functions_to_object(name: str, obj: GraphQLObjectType, resolvers: dict):
    type_resolver = resolvers.get(name, {})
    for field_name, field_object in obj.fields.items():
        field_resolver = type_resolver.get(field_name, default_resolver)
        field_object.resolver = field_resolver


def add_resolve_function_to_scalar(name: str, obj: GraphQLObjectType, resolvers: dict):
    serializer = resolvers.get(name, obj.serialize)
    obj.serialize = serializer
