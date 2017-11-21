import re

from commander import Response


class Commander():
    def call(self, cmd: str) -> Response:
        raise NotImplementedError()

    def slugify(self, value) -> str:
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        # value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        # value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        # value = unicode(re.sub('[-\s]+', '_', value))

        value = re.sub('[\s]+', '_', value)

        value = "".join(x for x in value if x.isalnum() or x in "_-")

        return value
