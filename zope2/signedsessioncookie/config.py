from zope.interface import implementer

try:
    from Crypto import Random
except ImportError:
    _HAS_CRYPTO = False
else:
    _HAS_CRYPTO = True
    from Crypto.Cipher import Blowfish
    BLOCK_SIZE = Blowfish.block_size
    IV = Random.new().read(BLOCK_SIZE)

from .interfaces import ISignedSessionCookieConfig


@implementer(ISignedSessionCookieConfig)
class SignedSessionCookieConfig(object):

    def __init__(self, 
                 secret,
                 salt=None,
                 cookie_name='session',
                 max_age=None,
                 path=None,
                 domain=None,
                 secure=True,
                 http_only=True,
                 hash_algorithm=None,
                 timeout=None,
                 reissue_time=None,
                 encrypt=False,
                ):
        self.secret = secret
        self.salt = salt
        self.cookie_name = cookie_name
        self.max_age = max_age
        self.path = path
        self.domain = domain
        self.secure = secure
        self.http_only = http_only
        self.hash_algorithm = hash_algorithm
        self.timeout = timeout
        self.reissue_time = reissue_time
        if encrypt and not _HAS_CRYPTO:
            raise ValueError('Install pycrypto!')
        self.encrypt = encrypt

    def getCookieAttrs(self):
        """-> dict for configuring the Pyramid session cookie class."""
        result = dict([(key, value) for key, value in self.__dict__.items()
                       if value is not None])
        if result.pop('encrypt'):
            result['serializer'] = object()  # Replace w/ serializer
        result['httponly'] = result.pop('http_only')
        if 'hash_algorithm' in result:
            result['hashalg'] = result.pop('hash_algorithm')
        return result
