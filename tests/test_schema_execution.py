from ariadne import execute_request, make_executable_schema


TEST_TYPEDEFS = """
    schema {
        query: Query
        mutation: Mutation
    }

    type Query {
        hello: String
        person: Person
    }

    type Mutation {
        concatStrings(bits: [String]!): String
    }

    type Person {
        firstName: String
        lastName: String
        fullName: String
    }
"""


def resolve_hello(*_):
    return "world"


def resolve_person(*_):
    return {"firstName": "John", "lastName": "Doe"}


def resolve_person_fullname(person, *_):
    return "%s %s" % (person["firstName"], person["lastName"])


def resolve_concat_strings(*_, bits=None):
    return "".join(bits)


TEST_RESOLVERS = {
    "Query": {"hello": resolve_hello, "person": resolve_person},
    "Mutation": {"concatStrings": resolve_concat_strings},
    "Person": {"fullName": resolve_person_fullname},
}


TEST_QUERY = """
    query {
        hello
        person {
            fullName
        }
    }
"""


TEST_MUTATION = """
    mutation ConcatStrings($bits: [String]!) {
        concatStrings(bits: $bits)
    }
"""


def test_schema_query():
    schema = make_executable_schema(TEST_TYPEDEFS, resolvers=TEST_RESOLVERS)
    result = execute_request(schema, TEST_QUERY)
    assert result.data == {"hello": "world", "person": {"fullName": "John Doe"}}


def test_schema_mutation():
    schema = make_executable_schema(TEST_TYPEDEFS, resolvers=TEST_RESOLVERS)
    result = execute_request(
        schema, TEST_MUTATION, variable_values={"bits": ["a", "b", "c"]}
    )
    assert result.data == {"concatStrings": "abc"}
