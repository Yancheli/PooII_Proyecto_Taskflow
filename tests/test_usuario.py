import pytest
from src.domain.usuario import Usuario


class TestUsuario:

    def test_crear_usuario_valido(self, usuario_ejemplo):
        assert usuario_ejemplo.username == "testuser"
        assert usuario_ejemplo.email == "test@example.com"
        assert usuario_ejemplo.activo is True


    @pytest.mark.parametrize("username", [
        "ab",
        "",
        "user@name"
    ])
    def test_username_invalido(self, username):
        with pytest.raises(ValueError):
            Usuario(username=username, email="test@test.com")


    @pytest.mark.parametrize("email", [
        "emailinvalido",
        "email.com",
        "email@"
    ])
    def test_email_invalido(self, email):
        with pytest.raises(ValueError):
            Usuario(username="usuario123", email=email)


    def test_desactivar_usuario(self, usuario_ejemplo):
        usuario_ejemplo.desactivar()
        assert usuario_ejemplo.activo is False


    def test_activar_usuario(self, usuario_ejemplo):
        usuario_ejemplo.desactivar()
        usuario_ejemplo.activar()
        assert usuario_ejemplo.activo is True