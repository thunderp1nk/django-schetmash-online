

class SchetmashJsonError(Exception):

    def __init__(self, response, url):
        self.response = response
        self.url = url
        super().__init__('{0}: {1}, url: {2}'.format(
            self.response.status_code, self.response.text, self.url)
        )
