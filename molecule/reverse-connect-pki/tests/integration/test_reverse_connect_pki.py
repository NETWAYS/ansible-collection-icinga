import time


def _openssl_subject(host, path):
    cmd = host.run(f"openssl x509 -noout -subject -in {path}")
    assert cmd.rc == 0
    return cmd.stdout.strip()


def _openssl_issuer(host, path):
    cmd = host.run(f"openssl x509 -noout -issuer -in {path}")
    assert cmd.rc == 0
    return cmd.stdout.strip()


def _x509_identity(value):
    # Convert "subject=CN = Icinga CA" / "issuer=CN = Icinga CA" to "CN = Icinga CA"
    return value.split("=", 1)[1].strip()


def _wait_for_ca_signed_cert(agent_host, master_host, retries=30, sleep_s=2):
    ca_subject = _x509_identity(_openssl_subject(master_host, "/var/lib/icinga2/ca/ca.crt"))

    for _ in range(retries):
        crt = agent_host.file("/var/lib/icinga2/certs/icinga-agent.crt")
        if crt.exists:
            issuer = _x509_identity(_openssl_issuer(agent_host, "/var/lib/icinga2/certs/icinga-agent.crt"))
            if issuer == ca_subject:
                return
        time.sleep(sleep_s)

    issuer = _x509_identity(_openssl_issuer(agent_host, "/var/lib/icinga2/certs/icinga-agent.crt"))
    raise AssertionError(f"Agent certificate not signed by CA. issuer={issuer!r} ca_subject={ca_subject!r}")


def test_delegate_pki_artifacts(host):
    if host.backend.get_hostname() != "icinga-agent":
        return

    ca = host.file("/var/lib/icinga2/certs/ca.crt")
    assert ca.is_file

    # Ticket may be consumed/removed after successful enrollment.
    ticket = host.file("/var/lib/icinga2/certs/ticket")
    if ticket.is_file:
        assert ticket.content_string.strip() != ""

    key = host.file("/var/lib/icinga2/certs/icinga-agent.key")
    assert key.is_file

    crt = host.file("/var/lib/icinga2/certs/icinga-agent.crt")
    assert crt.is_file


def test_reverse_connect_auto_signing(host):
    if host.backend.get_hostname() != "icinga-agent":
        return

    agent_host = host
    master_host = host.get_host("docker://icinga-master")

    _wait_for_ca_signed_cert(agent_host, master_host)

