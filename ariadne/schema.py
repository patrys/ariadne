from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLScalarType,
    build_ast_schema,
    parse,
)

from .default_resolver import default_resolver


def make_executable_schema(typedefs: str, resolvers: dict) -> GraphQLSchema:
    ast_schema = parse(typedefs)
    schema = build_ast_schema(ast_schema)
    attach_field_resolvers(schema, resolvers)
    return schema


def attach_field_resolvers(schema: GraphQLSchema, resolvers: dict) -> None:
    for type_name, type_object in schema.get_type_map().items():
        if isinstance(type_object, GraphQLScalarType):
            serializer = resolvers.get(type_name, type_object.serialize)
            type_object.serialize = serializer
        if isinstance(type_object, GraphQLObjectType):
            type_resolver = resolvers.get(type_name, {})
            for field_name, field_object in type_object.fields.items():
                field_resolver = type_resolver.get(field_name) or default_resolver
                field_object.resolver = field_resolver
