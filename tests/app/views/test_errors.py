def test_errors_404(survey_runner):
    response = survey_runner.test_client().get('/hfjdskahfjdkashfsa')
    assert response.status_code == 404
    assert "An error has occurred" in response.get_data(as_text=True)
