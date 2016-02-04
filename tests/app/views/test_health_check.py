def test_healthcheck(survey_runner):
    response = survey_runner.test_client().get('/healthcheck')
    # health check will fail as rabbit mq won't be running
    assert response.status_code, 500
    assert "failure" in response.get_data(as_text=True)


def test_errors_404(survey_runner):
    response = survey_runner.test_client().get('/hfjdskahfjdkashfsa')
    assert response.status_code == 404
    assert "Page could not be found" in response.get_data(as_text=True)
