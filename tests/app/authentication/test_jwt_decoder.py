from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException

import unittest

sr_private_pem = b'-----BEGIN RSA PRIVATE KEY-----\n' \
                 b'Proc-Type: 4,ENCRYPTED\n' \
                 b'DEK-Info: DES-EDE3-CBC,40D25DD8AB64238D\n' \
                 b'\n' \
                 b'rDTKZI9J0Tfu2gyIcjfXuwrJvF3C28w44EFO/u8Es37EMK7V+wozhxO40wKs57DV\n' \
                 b'0DgCT+oEsQpfyipe+1JGtn54uGoWgo4/mtbsxES6+igJAWyDfBYN8ylYjSs8EgvN\n' \
                 b'OoVEoevn23SqIX9mbNKhkXStDimPBckP149r137KPktL5tbvIJnOhos7bVZ1X3rK\n' \
                 b'JRr0mEgxzDk4TUuwBnGE+YuiE5PSpK7DZgLlG2gNOaPf9X3CL6iRBzUlE8md+t6/\n' \
                 b'GBDv3G7pNe7Ml9aRzKoYtcKSXpDX3Msu63EWoEGcAG6zXAXrD9HRgAlxwZHJS3lH\n' \
                 b'VSEhxXLeCzYzktNxOb0QCOjenU/FY4X0GndMg6gnPIRBjwFNB48URw6mkPwfhXi3\n' \
                 b'9Sl2gImssGjV1oa8CeS9n/Q5huRL0H97jjJFoPyqRTTAwcxnTHrek7A9iHAAZDls\n' \
                 b'D+LrYas8J2F+8PrT3UZfEFw81b6V1To1R32wFChj9VE4vX3PpNdJtFrrFuIKL16S\n' \
                 b'YGk0n+mBH+koWQfT7gCd5jERXkB1R1bZ20vd4QhtHkXytQFqDnC+FK4A8SuGYz9h\n' \
                 b'uEgulVHEFbgyVsCryGf6gXx6/Rfsq7KGz1rmG2pDTSzUBWz22XSyOOGyKKp88uQa\n' \
                 b'AcWjeb0R3nFdGcdkC+ZXL6wrAQ5otoZbO8nGxzxOoNzaxhV+qrshz/B4larYKCTM\n' \
                 b'0aXVuhTOAoMkvmxRw4xSxRDeP1p8XOe6svBr5+PHfwsRukh+yvnhfIHBmW1UsPGb\n' \
                 b'0PQnCFhpbxI1xXflbavcTSPvQwz5zrfF5eI44YMI7qX0lxy8E7hB/E+SXCmzdajC\n' \
                 b'+1sR5OlBlu7wwqntbhdnREqCqCkieNViSJLCf2Bwusqzz2ALpjgwt13N5oRIcTH8\n' \
                 b'H96JbJu3HMM3JtW8kcAmMYcGGVymPIjy9mee7IJ1fzsW7xM6YJi3n1Vfw1A7nWh8\n' \
                 b'QNtV8vjG0KPRx7Cvz+qKPDPJxJRo9cJVPeyBFyE24JV+xMRrjNGYuE8DNtU/bW2w\n' \
                 b'J59//mKVgS4xWXQ4ss8ovq8XgTqkGMZEbpL9UPW81tIqwduwQvQYES2/NssY6HXZ\n' \
                 b'+uHakYmuZLe9a+zKwjFV3UwbIJFLYAGn+Y/I9aV0Prjirf/tBYhsanyvkElC/evj\n' \
                 b'KFXbnb3fEfVnuAZhTLiRzl1EnNoovEfmnmd35cwvGlIf02vpV59oCfUO7Xbm7kEQ\n' \
                 b'Z7ljfdopMY3NYFbvy8vmCRk6X2f4Uo8q7xZecBrg85xXmZRr+N1nrQucxZfzUu39\n' \
                 b'GRlqurRApamDAE4M5pXYNFwwrlNcf3tUaau1c8TJWdcFQrJW+FfasBf/G7aBFdlh\n' \
                 b'339+aAmfA4xDAdXRWeaUT3se8YBR+Q9VfoXyBV0W/eUHN+I1HB7EzWXk3EaWLayv\n' \
                 b'82UIrKicNnG/5PPV8+U/fXjaibMcaknfe1DX+xXDvZKzE/iB2T3R0aTVjEh4iSmN\n' \
                 b'WETAbEOxkaQ44l8yvJiLAUsj4ln2k8jCF4EeMk6KQ5zUnJh40e9qvEW6DI8glA+3\n' \
                 b'LdD++NLwVKevmxl3XfFKKHNcEriebzboAWs1dlkm75zqdNuUcDCXVA==\n' \
                 b'-----END RSA PRIVATE KEY-----\n'


rrm_public_pem = b'-----BEGIN PUBLIC KEY-----\n' \
                 b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvZzMraB96Wd1zfHS3vW3\n' \
                 b'z//Nkqz+9HfwViNje2Y5L6m3K/7raA0kUsWD1f6X7/LIJfkCEctCEj9q19+cX30h\n' \
                 b'0pi6IOu92MlIwdH/L6CTuzYnG4PACKT8FZonLw0NYBqh8p4vWS8xtNHNjTWua/FF\n' \
                 b'TlxdtYnEb9HbUZkg7dXAtnikozlE/ZZSponq7K00h3Uh9goxQIavcK1QI8pw5V+T\n' \
                 b'8V8Ue7k98W8LpbYQWm7FPOZayu1EoJWUZefdOlYAdeVbDS4tjrVF+3za+VX3q73z\n' \
                 b'JEfyLEM0zKrkQQ796gfYpkzDYwJvkiW7fb2Yh1teNHpFR5tozzMwUxkREl/TQ4U1\n' \
                 b'kwIDAQAB\n' \
                 b'-----END PUBLIC KEY-----\n'


jwt = "eyJhbGciOiJub25lIn0.eyJleHAiOiIyMDc1Mjk3MTQ4IiwiaWF0IjoiMTQ1NDkzNzAyMyIsInVzZXIiOiJqaW1teSJ9."

signed_jwt = "eyJraWQiOiJFRENSUk0iLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiIyMDc1Mjk3MTQ4IiwiaWF0IjoiMTQ1NDkzN" \
             "zAyMyIsInVzZXIiOiJqaW1teSJ9.gXARjhMIgthJahF60YHD4KEMifLw6TX8m6YpoYWekXqr76Sw86pyb-qA3R-0fWqqaqRNAgx4au" \
             "9t4uk9P5f3XMIXayPWpXhv7Iqqae7K-LIiRYz_7Jvim9fgO5JAsAp1qRWYkw2J92qhO87OUTacVLIXibHT4G2-W7Zr5bHlzr3E4uJS" \
             "TxJ1uYm3sCyYSh17MTvE8whXYkXny33SKVqKT2HY2EAEhIaDAZJ7ewjTMxCpwyHWGnJg5NFuaPY_CyZeZFNE17rRlin2ThdydAWeyE" \
             "pm5ffuH3uLhR6LyxTyyOP9AyCRBP50VR6xwJ3xYEmQis-4CCS3gKD-aAUn2yGl_g"

encrypted_jwt = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.YfYdaxwHqcHrAUy3cMlOglZqGEv48bEfPse1" \
                "-Pd8DUfo5Kg_nWEoP8NgCzfWP862dr6B7UAUUlbs-JLFmua4OlXBHCJG4IcQMxzJUjkoGxQIli8N59kwynyqdVvf22j5zggMokK" \
                "IwACidPBzgu7aHdRq2PvtpjkZRE0Ga4Q6iF4BDSwtsI0zXn0nQsXXfTpz_uIlwPnCLUgMydg478U5t9qe24TsHfq-mimCFQ0Hon" \
                "H0b086VHoTESwTuiJ_0Kv9S-JiflZHmdAt_Xx0V0n7Lo9q97Q64gVWW8OKDrvLFQyMaUenFo0ONWpbtOgJlSm-xWrG7SIrm-uDM" \
                "VeYm5lI2A.SNq_54mmzqYjp0y7.sHbanOmfxBsO-JOS-6nZ0HsgouMWary34i0Czx9VjCiB7tNig7nEib8nIHqRSs2ljubEhATG" \
                "JXiptumZ4RoBHJSUQrp_vZBeR_EnKFXE8e45jz4CfBmuQo2W5lJoj2QvaVPBNrbCUsN62NIKb8n1Tr9JL0fnA6IQIByc8zR3Tbr" \
                "mnDYVEtgbY4IPRDsFI14Dm2cWaTYkj3c0A_4vPAhHsZEiGLQiKsy8WSoi8NC-CNs6FTqYrqcB4V77umi5XRU_JcdE_mqxcMkIHY" \
                "UsUBDCqSMSA8xQgD56OOo41K4-vFMh99fU1u5zSbdqhqLtNeYTepJkOnCFi5aSjFPrtpfbvk9YPDJERJzEXAJkYbkUplmNudtOb" \
                "ZY2IDmZglC5waGsTOq62tpudGPNb5B_FEq0s8ezAtMtf-C3hBslOcCLtAlGdRsptS6-L4YHxaGEAvwXD1heQADoAabjGCA-BZGP" \
                "dc6h8A6y1QR7m2P33KEz83h141X4Ftyd9kTGxgjQ8-UrIGvu9b1wbmcjTWK3hiiyC3o0guBbzBq0SflX-RG9_zyK4sAIksiXj9m" \
                "NRah1IUjUT5zr9cs1c5i4WwJdpJ28IzKvczgQ63B_t1xEpGsb6A35EhxzRkG7BQ.I9WExvUvZVXdwjxz8EPtCg"


class JWTDecodeTest(unittest.TestCase):

    def test_decode(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = decoder.decode_jwt_token(jwt)
        self.assertEquals("jimmy", token.get("user"))

    def test_decode_with_no_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        self.assertRaises(NoTokenException, decoder.decode_jwt_token, None)

    def test_decode_with_invalid_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_jwt_token, token)

    def test_decode_signed_jwt_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = decoder.decode_signed_jwt_token(signed_jwt)
        self.assertEquals("jimmy", token.get("user"))

    def test_decode_signed_jwt_token_with_no_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        self.assertRaises(NoTokenException, decoder.decode_signed_jwt_token, None)

    def test_decode_signed_jwt_token_with_invalid_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_signed_jwt_token, token)

    def test_decrypt_jwt_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = decoder.decrypt_jwt_token(encrypted_jwt)
        self.assertEquals("jimmy", token.get("user"))

    def test_decrypt_jwt_token_with_no_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        self.assertRaises(NoTokenException, decoder.decrypt_jwt_token, None)

    def test_decrypt_jwt_token_with_invalid_token(self):
        decoder = Decoder(rrm_public_pem, sr_private_pem, "digitaleq")
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decrypt_jwt_token, token)


if __name__ == '__main__':
    unittest.main()
