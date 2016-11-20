from flask_analytics.providers.googleanalytics import GoogleAnalytics


class CustomGoogleAnalytics(GoogleAnalytics):
    account = None

    def __init__(self, account=None):
        super().__init__(account)

    @property
    def template(self):
        return """<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', '%s', 'auto');
ga('set', 'anonymizeIp', true);
ga('send', 'pageview');
</script>"""

    @property
    def source(self):
        if self.account is None:
            return None
        return self.template % self.account
