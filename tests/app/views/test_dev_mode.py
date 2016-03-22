def test_dev_mode(survey_runner):
    response = survey_runner.test_client().get('/dev')
    assert response.status_code == 200

