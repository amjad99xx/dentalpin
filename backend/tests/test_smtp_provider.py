"""Tests for the SMTP email provider's message construction."""

from app.core.email.providers.base import EmailMessage
from app.core.email.providers.smtp import SMTPProvider


def _provider(**overrides):
    kwargs = dict(
        host="smtp.example.com",
        port=587,
        default_from_email="noreply@dentalpin.com",
        default_from_name="DentalPin",
    )
    kwargs.update(overrides)
    return SMTPProvider(**kwargs)


def test_message_id_domain_is_the_sender_domain_not_the_container_hostname():
    """``make_msgid()`` with no ``domain`` falls back to ``socket.getfqdn()``,
    which inside a container resolves to the raw container id (e.g.
    ``<...@70c12637617f>``) rather than a real domain. A non-routable
    domain in Message-ID is a well-known spam signal: some receivers
    accept the message (250 OK, "queued") and then silently discard it
    rather than bounce, which looks identical to a successful send from
    here but never arrives.
    """
    provider = _provider()
    msg = provider._build_message(
        EmailMessage(
            to_email="patient@example.com",
            subject="Hola",
            body_html="<p>Hola</p>",
            from_email="info@dental-heights.com",
        )
    )
    assert msg["Message-ID"].endswith("@dental-heights.com>")


def test_message_id_domain_falls_back_to_the_provider_default_sender():
    """No per-message ``from_email`` — falls back to the provider's own
    default sender domain, still never the container hostname."""
    provider = _provider(default_from_email="noreply@dentalpin.com")
    msg = provider._build_message(
        EmailMessage(to_email="patient@example.com", subject="Hola", body_html="<p>Hola</p>")
    )
    assert msg["Message-ID"].endswith("@dentalpin.com>")
