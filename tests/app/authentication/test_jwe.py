import unittest
from tests.app.authentication import RRM_PUBLIC_PEM, SR_PRIVATE_PEM
from tests.app.authentication.encoder import Encoder
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
import os

valid_signed_jwt = "eyJraWQiOiJFRENSUk0iLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiIyMDc1Mjk3MTQ4IiwiaWF0IjoiMTQ1N" \
                   "DkzNzAyMyIsInVzZXIiOiJqaW1teSJ9.gXARjhMIgthJahF60YHD4KEMifLw6TX8m6YpoYWekXqr76Sw86pyb-qA3R-0fWqqaq" \
                   "RNAgx4au9t4uk9P5f3XMIXayPWpXhv7Iqqae7K-LIiRYz_7Jvim9fgO5JAsAp1qRWYkw2J92qhO87OUTacVLIXibHT4G2-W7Zr" \
                   "5bHlzr3E4uJSTxJ1uYm3sCyYSh17MTvE8whXYkXny33SKVqKT2HY2EAEhIaDAZJ7ewjTMxCpwyHWGnJg5NFuaPY_CyZeZFNE17" \
                   "rRlin2ThdydAWeyEpm5ffuH3uLhR6LyxTyyOP9AyCRBP50VR6xwJ3xYEmQis-4CCS3gKD-aAUn2yGl_g"

valid_jwe = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.YfYdaxwHqcHrAUy3cMlOglZqGEv48bEfPse1-Pd8DU" \
            "fo5Kg_nWEoP8NgCzfWP862dr6B7UAUUlbs-JLFmua4OlXBHCJG4IcQMxzJUjkoGxQIli8N59kwynyqdVvf22j5zggMokKIwACidPBzgu7" \
            "aHdRq2PvtpjkZRE0Ga4Q6iF4BDSwtsI0zXn0nQsXXfTpz_uIlwPnCLUgMydg478U5t9qe24TsHfq-mimCFQ0HonH0b086VHoTESwTuiJ_" \
            "0Kv9S-JiflZHmdAt_Xx0V0n7Lo9q97Q64gVWW8OKDrvLFQyMaUenFo0ONWpbtOgJlSm-xWrG7SIrm-uDMVeYm5lI2A.SNq_54mmzqYjp0" \
            "y7.sHbanOmfxBsO-JOS-6nZ0HsgouMWary34i0Czx9VjCiB7tNig7nEib8nIHqRSs2ljubEhATGJXiptumZ4RoBHJSUQrp_vZBeR_EnKF" \
            "XE8e45jz4CfBmuQo2W5lJoj2QvaVPBNrbCUsN62NIKb8n1Tr9JL0fnA6IQIByc8zR3TbrmnDYVEtgbY4IPRDsFI14Dm2cWaTYkj3c0A_4" \
            "vPAhHsZEiGLQiKsy8WSoi8NC-CNs6FTqYrqcB4V77umi5XRU_JcdE_mqxcMkIHYUsUBDCqSMSA8xQgD56OOo41K4-vFMh99fU1u5zSbdq" \
            "hqLtNeYTepJkOnCFi5aSjFPrtpfbvk9YPDJERJzEXAJkYbkUplmNudtObZY2IDmZglC5waGsTOq62tpudGPNb5B_FEq0s8ezAtMtf-C3h" \
            "BslOcCLtAlGdRsptS6-L4YHxaGEAvwXD1heQADoAabjGCA-BZGPdc6h8A6y1QR7m2P33KEz83h141X4Ftyd9kTGxgjQ8-UrIGvu9b1wbm" \
            "cjTWK3hiiyC3o0guBbzBq0SflX-RG9_zyK4sAIksiXj9mNRah1IUjUT5zr9cs1c5i4WwJdpJ28IzKvczgQ63B_t1xEpGsb6A35EhxzRkG" \
            "7BQ.I9WExvUvZVXdwjxz8EPtCg"


class JWETest(unittest.TestCase):
    def test_valid_jwe(self):
        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        token = decoder.decrypt_jwt_token(valid_jwe)
        self.assertEquals("jimmy", token.get("user"))

    def test_does_not_contain_four_instances_of_full_stop(self):
        jwe = valid_jwe.replace('.', '', 1)
        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe)
        self.assertIn("Incorrect size", ite.exception.value)

    def test_missing_algorithm(self):
        jwe_protected_header = b'{"enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Missing Algorithm", ite.exception.value)

    def test_invalid_algorithm(self):
        jwe_protected_header = b'{"alg":"PBES2_HS256_A128KW","enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Invalid Algorithm", ite.exception.value)

    def test_enc_missing(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP"}'

        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Missing Encoding", ite.exception.value)

    def test_invalid_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A128GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Invalid Encoding", ite.exception.value)

    def test_jwe_header_contains_alg_twice(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","alg":"RSA-OAEP","enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("InvalidTag", ite.exception.value)

    def test_jwe_header_only_contains_alg_and_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A256GCM", "test":"test"}'
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), jwe_protected_header=encoder.base_64_encode(jwe_protected_header))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("InvalidTag", ite.exception.value)

    def test_jwe_key_not_2048_bits(self):
        cek = os.urandom(32)

        encoder = Encoder()
        encrypted_key = encoder._encrypted_key(cek)
        encrypted_key = encrypted_key[0:len(encrypted_key) - 2]
        jwe = encoder.encrypt(valid_signed_jwt.encode(), cek=cek, encrypted_key=encrypted_key)

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("ValueError", ite.exception.value)

    def test_cek_not_256_bits(self):
        cek = os.urandom(24)

        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), cek=cek)

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("CEK incorrect length", ite.exception.value)

    def test_iv_not_96_bits(self):
        iv = os.urandom(45)

        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), iv=iv)

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
            self.assertIn("IV incorrect length", ite.exception.value)

    def test_authentication_tag_not_128_bits(self):
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), tag=os.urandom(10))

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("'Authentication tag must be 16 bytes or longer", ite.exception.value)

    def test_authentication_tag_corrupted(self):
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode(), tag=b'adssadsadsadsadasdasdasads')

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())

    def test_cipher_text_corrupted(self):
        encoder = Encoder()
        jwe = encoder.encrypt(valid_signed_jwt.encode())

        tokens = jwe.decode().split('.')
        jwe_protected_header = tokens[0]
        encrypted_key = tokens[1]
        encoded_iv = tokens[2]
        encoded_cipher_text = tokens[3]
        encoded_tag = tokens[4]

        corrupted_cipher = encoded_cipher_text[0:len(encoded_cipher_text) - 1]
        reassembled = jwe_protected_header + "." + encrypted_key + "." + encoded_iv + "." + corrupted_cipher + "." + encoded_tag

        decoder = Decoder(RRM_PUBLIC_PEM, SR_PRIVATE_PEM, "digitaleq")
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(reassembled)

if __name__ == '__main__':
    unittest.main()
