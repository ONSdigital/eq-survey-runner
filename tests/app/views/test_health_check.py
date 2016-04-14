def test_healthcheck(survey_runner):
    response = survey_runner.test_client().get('/healthcheck')
    assert response.status_code == 200
    assert "success" in response.get_data(as_text=True)


def test_errors_404(survey_runner):
    response = survey_runner.test_client().get('/hfjdskahfjdkashfsa')
    assert response.status_code == 404
    assert '<title>Error</title' in response.get_data(True)
