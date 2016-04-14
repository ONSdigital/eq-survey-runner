from flask_analytics.providers.googleanalytics import GoogleAnalytics


class CustomGoogleAnalytics(GoogleAnalytics):
    account = None

    def __init__(self, account=None):
        self.account = account

    @property
    def template(self):
            return """<!-- Google Analytics -->
<script>
window.ga=window.ga||function(){(ga.q=ga.q||[]).push(arguments)};ga.l=+new Date;
ga('create', '{account}', 'auto');
ga('set', 'anonymizeIp', true);
ga('send', 'pageview');
</script>
<script async src='https://www.google-analytics.com/analytics.js'></script>
<!-- End Google Analytics -->"""

    @property
    def source(self):
        if self.account is None:
            return None
        return self.template.format(account=self.account)
