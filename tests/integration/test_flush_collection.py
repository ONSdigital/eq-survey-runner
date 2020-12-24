class TestFlushCollection(IntegrationTestCase):

    def test_no_token:
        """GIVEN the endpoint is called,
        WHEN the application tries to find
        the expected token in the request
        query parameters
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        Could not find expected request argument: token
        """

        #TODO

    def test_cannot_decrypt_token:
        """GIVEN the endpoint is called,
        AND a token is given,
        WHEN the application tries to decrypt it
        AND fails
        THEN the request should respond with:

        HTTP/1.1 403 Forbidden
        Failed to decrypt given token
        """

        #TODO

    def test_cannot_find_collection_id:
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        WHEN the application tries to find 
        the 'collection_exercise_id' property
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        Could not find "collection_exercise_id" in decrypted JWT
        """

        #TODO
    
    def test_successful_flush_no_fails:
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        AND the application can find the 
        'collection_exercise_id' property,
        AND there are partial responses for
        the given collection exercise
        AND the application is able to flush them 
        THEN the request should respond with:

        HTTP/1.1 200 OK
        ((JSON string as documented))
        """

        #TODO

    def test_failed_flush:
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        AND the application can find the 
        'collection_exercise_id' property,
        AND there are partial responses for
        the given collection exercise
        AND the application is not able to flush them 
        THEN the request should respond with:

        HTTP/1.1 200 OK
        ((JSON string as documented))
        """

        #TODO