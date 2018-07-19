from typing import Any

from graphql import GraphQLSchema, graphql, parse


def execute_request(
    schema: GraphQLSchema,
    query: str,
    variable_values: dict = None,
    root_value: Any = None,
):
    query_ast = parse(query)
    return graphql(
        schema, query_ast, variable_values=variable_values, root_value=root_value
    )
