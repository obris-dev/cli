from pathlib import Path

from ...base_client import BaseRESTClient
from .routes import SSLTLSCertificatePath
from .ssl_tls_response_mapper import SSLTLSCertficateResponseMapper


class SSLTLSCertificateClient(BaseRESTClient):

    @staticmethod
    def __file_contents(file_path):
        expanded_path = Path(file_path).expanduser()
        if not expanded_path.exists():
            raise ValueError(f"file does not exist at{expanded_path}")

        return expanded_path.read_text()

    @staticmethod
    def __check_passed_cert_paths(cert_body_file_path, cert_private_key_file_path):
        if cert_body_file_path is None:
            raise ValueError("missing cert_body_file_path")
        if cert_private_key_file_path is None:
            raise ValueError("missing cert_private_key_file_path")
        return True

    def list(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = SSLTLSCertificatePath.CERTIFICATES_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        certificates = response_json["certificates"]
        formatted_response = SSLTLSCertficateResponseMapper.certificates(certificates)
        return formatted_response

    def create(
            self,
            application_id=None,
            cert_body_file_path=None,
            cert_private_key_file_path=None,
            cert_chain_file_path=None
    ):
        if application_id is None:
            raise ValueError("missing application_id")
        self.__check_passed_cert_paths(cert_body_file_path, cert_private_key_file_path)

        data = {
            "certificate": self.__file_contents(cert_body_file_path),
            "private_key": self.__file_contents(cert_private_key_file_path)
        }
        if cert_chain_file_path is not None:
            data["chain"] = self.__file_contents(cert_chain_file_path)

        command_path = SSLTLSCertificatePath.CERTIFICATES_TMPL.value.format(application_id)
        response_json = self.post(command_path, data)
        certificate = response_json["certificate"]
        formatted_response = SSLTLSCertficateResponseMapper.certificate(certificate)
        return formatted_response

    def update(
        self,
        pk=None,
        application_id=None,
        cert_body_file_path=None,
        cert_private_key_file_path=None,
        cert_chain_file_path=None
    ):
        if pk is None:
            raise ValueError("missing id")
        if application_id is None:
            raise ValueError("missing application_id")

        self.__check_passed_cert_paths(cert_body_file_path, cert_private_key_file_path)

        data = {
            "certificate": self.__file_contents(cert_body_file_path),
            "private_key": self.__file_contents(cert_private_key_file_path)
        }
        if cert_chain_file_path is not None:
            data["chain"] = self.__file_contents(cert_chain_file_path)

        command_path = SSLTLSCertificatePath.CERTIFICATE_TMPL.value.format(application_id, pk)
        response_json = self.put(command_path, data)
        certificate = response_json["certificate"]
        formatted_response = SSLTLSCertficateResponseMapper.certificate(certificate)
        return formatted_response

    def delete(
            self,
            pk=None,
            application_id=None
    ):
        if application_id is None:
            raise ValueError("missing application_id")
        if pk is None:
            raise ValueError("missing id")

        command_path = SSLTLSCertificatePath.CERTIFICATE_TMPL.value.format(application_id, pk)
        return super().delete(command_path)
