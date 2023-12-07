from enum import Enum


class SSLTLSCertificatePath(Enum):
    CERTIFICATES_TMPL = "/certificates/{}"
    CERTIFICATE_TMPL = "/certificates/{}/{}"
