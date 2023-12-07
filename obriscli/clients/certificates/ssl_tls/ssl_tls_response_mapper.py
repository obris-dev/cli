from obriscli.clients.response_mappers import SSLTLSCertficate


class SSLTLSCertficateResponseMapper:

    @classmethod
    def certificates(cls, response_json):
        formatted_certificates = []
        for formatted_certificate in response_json:
            formatted_certificate = cls.certificate(formatted_certificate)
            formatted_certificates.append(formatted_certificate)
        return formatted_certificates

    @staticmethod
    def certificate(response_json):
        unformatted_certificate = response_json
        domains = response_json["domains"]
        flatten_domains = [d["domain"] for d in domains]
        return SSLTLSCertficate(
            unformatted_certificate["id"],
            unformatted_certificate["commonName"],
            flatten_domains,
            unformatted_certificate["signatureAlgorithm"],
            unformatted_certificate["serialNumber"],
            unformatted_certificate["notBefore"],
            unformatted_certificate["notAfter"],
            unformatted_certificate["updated"],
            unformatted_certificate["created"]
        )
