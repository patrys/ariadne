from datetime import date

from graphql import graphql

from ariadne import make_executable_schema


def test_query_default_scalar():
    type_defs = """
        schema {
            query: Query
        }

        type Query {
            test: String
        }
    """

    resolvers = {"Query": {"test": lambda *_: "success"}}

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test }")
    assert result.errors is None
    assert result.data == {"test": "success"}


def test_query_custom_scalar():
    type_defs = """
        schema {
            query: Query
        }

        scalar Date

        type Query {
            test: Date
        }
    """

    resolvers = {
        "Query": {"test": lambda *_: date.today()},
        "Date": lambda date: date.strftime("%Y-%m-%d"),
    }

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test }")
    assert result.errors is None
    assert result.data == {"test": date.today().strftime("%Y-%m-%d")}


def test_query_custom_type_default_resolver():
    type_defs = """
        schema {
            query: Query
        }

        type Query {
            test: Custom
        }

        type Custom {
            node: String
        }
    """

    resolvers = {"Query": {"test": lambda *_: {"node": "custom"}}}

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test { node } }")
    assert result.errors is None
    assert result.data == {"test": {"node": "custom"}}


def test_query_custom_type_custom_resolver():
    type_defs = """
        schema {
            query: Query
        }

        type Query {
            test: Custom
        }

        type Custom {
            node: String
        }
    """

    resolvers = {
        "Query": {"test": lambda *_: {"node": "custom"}},
        "Custom": {"node": lambda *_: "deep"},
    }

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test { node } }")
    assert result.errors is None
    assert result.data == {"test": {"node": "deep"}}


def test_query_custom_type_merged_custom_default_resolvers():
    type_defs = """
        schema {
            query: Query
        }

        type Query {
            test: Custom
        }

        type Custom {
            node: String
            default: String
        }
    """

    resolvers = {
        "Query": {"test": lambda *_: {"node": "custom", "default": "ok"}},
        "Custom": {"node": lambda *_: "deep"},
    }

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test { node default } }")
    assert result.errors is None
    assert result.data == {"test": {"node": "deep", "default": "ok"}}


def test_query_with_argument():
    type_defs = """
        schema {
            query: Query
        }

        type Query {
            test(returnValue: Int!): Int
        }
    """

    def resolve_test(*_, returnValue):
        assert returnValue == 4
        return "42"

    resolvers = {"Query": {"test": resolve_test}}

    schema = make_executable_schema(type_defs, resolvers)

    result = graphql(schema, "{ test(returnValue: 4) }")
    assert result.errors is None
    assert result.data == {"test": 42}
