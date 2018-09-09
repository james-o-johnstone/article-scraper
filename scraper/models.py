class Article(object):
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def jsonify(self):
        return {
            'body': self.body,
            'title': self.title,
            'url': self.url,
        }