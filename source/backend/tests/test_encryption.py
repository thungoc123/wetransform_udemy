from app.shared.encryption import DataEncryptor


def test_encrypt_decrypt():
    encryptor = DataEncryptor()
    original_text = "my_super_secret_client_id"

    encrypted = encryptor.encrypt(original_text)
    assert encrypted != original_text
    assert len(encrypted) > len(original_text)

    decrypted = encryptor.decrypt(encrypted)
    assert decrypted == original_text


def test_encrypt_empty_string():
    encryptor = DataEncryptor()
    assert encryptor.encrypt("") == ""
    assert encryptor.decrypt("") == ""
