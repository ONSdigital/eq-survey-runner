import unittest

from tests.app.authentication import TEST_DO_NOT_USE_SR_PRIVATE_PEM_PASSWORD
from app.authentication.jwt_decoder import JWTDecryptor

# Not used in this test, but needed for the Decoder constructor
private_pem = '''-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,40D25DD8AB64238D

rDTKZI9J0Tfu2gyIcjfXuwrJvF3C28w44EFO/u8Es37EMK7V+wozhxO40wKs57DV
0DgCT+oEsQpfyipe+1JGtn54uGoWgo4/mtbsxES6+igJAWyDfBYN8ylYjSs8EgvN
OoVEoevn23SqIX9mbNKhkXStDimPBckP149r137KPktL5tbvIJnOhos7bVZ1X3rK
JRr0mEgxzDk4TUuwBnGE+YuiE5PSpK7DZgLlG2gNOaPf9X3CL6iRBzUlE8md+t6/
GBDv3G7pNe7Ml9aRzKoYtcKSXpDX3Msu63EWoEGcAG6zXAXrD9HRgAlxwZHJS3lH
VSEhxXLeCzYzktNxOb0QCOjenU/FY4X0GndMg6gnPIRBjwFNB48URw6mkPwfhXi3
9Sl2gImssGjV1oa8CeS9n/Q5huRL0H97jjJFoPyqRTTAwcxnTHrek7A9iHAAZDls
D+LrYas8J2F+8PrT3UZfEFw81b6V1To1R32wFChj9VE4vX3PpNdJtFrrFuIKL16S
YGk0n+mBH+koWQfT7gCd5jERXkB1R1bZ20vd4QhtHkXytQFqDnC+FK4A8SuGYz9h
uEgulVHEFbgyVsCryGf6gXx6/Rfsq7KGz1rmG2pDTSzUBWz22XSyOOGyKKp88uQa
AcWjeb0R3nFdGcdkC+ZXL6wrAQ5otoZbO8nGxzxOoNzaxhV+qrshz/B4larYKCTM
0aXVuhTOAoMkvmxRw4xSxRDeP1p8XOe6svBr5+PHfwsRukh+yvnhfIHBmW1UsPGb
0PQnCFhpbxI1xXflbavcTSPvQwz5zrfF5eI44YMI7qX0lxy8E7hB/E+SXCmzdajC
+1sR5OlBlu7wwqntbhdnREqCqCkieNViSJLCf2Bwusqzz2ALpjgwt13N5oRIcTH8
H96JbJu3HMM3JtW8kcAmMYcGGVymPIjy9mee7IJ1fzsW7xM6YJi3n1Vfw1A7nWh8
QNtV8vjG0KPRx7Cvz+qKPDPJxJRo9cJVPeyBFyE24JV+xMRrjNGYuE8DNtU/bW2w
J59//mKVgS4xWXQ4ss8ovq8XgTqkGMZEbpL9UPW81tIqwduwQvQYES2/NssY6HXZ
+uHakYmuZLe9a+zKwjFV3UwbIJFLYAGn+Y/I9aV0Prjirf/tBYhsanyvkElC/evj
KFXbnb3fEfVnuAZhTLiRzl1EnNoovEfmnmd35cwvGlIf02vpV59oCfUO7Xbm7kEQ
Z7ljfdopMY3NYFbvy8vmCRk6X2f4Uo8q7xZecBrg85xXmZRr+N1nrQucxZfzUu39
GRlqurRApamDAE4M5pXYNFwwrlNcf3tUaau1c8TJWdcFQrJW+FfasBf/G7aBFdlh
339+aAmfA4xDAdXRWeaUT3se8YBR+Q9VfoXyBV0W/eUHN+I1HB7EzWXk3EaWLayv
82UIrKicNnG/5PPV8+U/fXjaibMcaknfe1DX+xXDvZKzE/iB2T3R0aTVjEh4iSmN
WETAbEOxkaQ44l8yvJiLAUsj4ln2k8jCF4EeMk6KQ5zUnJh40e9qvEW6DI8glA+3
LdD++NLwVKevmxl3XfFKKHNcEriebzboAWs1dlkm75zqdNuUcDCXVA==
-----END RSA PRIVATE KEY-----'''


# Converted from JWK to PEM format
public_pem = '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAoahUIoWw0K0usKNuOR6H4wkf4oBUXHTxRvgb48E+BVvxkeDNjbC4
he8rUWcJoZmds2h7M70imEVhRU5djINXtqllXI4DFqcI1DgjT9LewND8MW2Krf3S
psk/ZkoFnilakGygTwpZ3uesH+PFABNIUYpOiN15dsQRkgr0vEhxN92i2asbOenS
ZeyaxziK72UwxrrKoExv6kc5twXTq4h+QChLOln0/mtUZwfsRaMStPs6mS6Xrgxn
xbWhojf663tuEQueGC+FCMfra36C9knDFGzKsNa7LZK2djYgyD3JR/MB/4NUJW/T
qOQtwHYbxevoJArm+L5StowjzGy+/bq6GwIDAQAB
-----END RSA PUBLIC KEY-----'''


plaintext = "The true sign of intelligence is not knowledge but imagination."
plaintext_in_ascii = [84, 104, 101, 32, 116, 114, 117, 101, 32, 115, 105, 103, 110, 32,
                      111, 102, 32, 105, 110, 116, 101, 108, 108, 105, 103, 101, 110,
                      99, 101, 32, 105, 115, 32, 110, 111, 116, 32, 107, 110, 111, 119,
                      108, 101, 100, 103, 101, 32, 98, 117, 116, 32, 105, 109, 97, 103,
                      105, 110, 97, 116, 105, 111, 110, 46]

jwe_protected_header = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ"
cek = bytes([177, 161, 244, 128, 84, 143, 225, 115, 63, 180, 3, 255, 107, 154, 212, 246, 138,
             7, 110, 91, 112, 46, 34, 105, 47, 130, 203, 46, 122, 234, 64, 252])

iv = bytes([227, 197, 117, 252, 2, 219, 233, 68, 180, 225, 77, 219])


# encrypted token from the example
encrypted_jwt = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ.OKOawDo13gRp2ojaHV7LFpZcg" \
                "V7T6DVZKTyKOMTYUmKoTCVJRgckCL9kiMT03JGeipsEdY3mx_etLbbWSrFr05kLzcSr4qKAq7" \
                "YN7e9jwQRb23nfa6c9d-StnImGyFDbSv04uVuxIp5Zms1gNxKKK2Da14B8S4rzVRltdYwam_l" \
                "Dp5XnZAYpQdb76FdIKLaVmqgfwX7XWRxv2322i-vDxRfqNzo_tETKzpVLzfiwQyeyPGLBIO56" \
                "YJ7eObdv0je81860ppamavo35UgoRdbYaBcoh9QcfylQr66oc6vFWXRcZ_ZT2LawVCWTIy3br" \
                "GPi6UklfCpIMfIjf7iGdXKHzg.48V1_ALb6US04U3b.5eym8TW_c8SuK0ltJ3rpYIzOeDQz7T" \
                "ALvtu6UG9oMo4vpzs9tX_EFShS8iB7j6jiSdiwkIr3ajwQzaBtQD_A.XFBoMYUZodetZdvTiFvSkQ"


# Unit test based of Example A.1 in RFC 7516 (https://tools.ietf.org/html/rfc7516#appendix-A.1)
class JWTDecoderRFCTest(unittest.TestCase):
    def setUp(self):
        self.decryptor_args = (
            private_pem,
            TEST_DO_NOT_USE_SR_PRIVATE_PEM_PASSWORD,
            public_pem
        )

        self.leeway = 120

    def test_plaintext_conversion(self):
        self.assertEqual(plaintext, ''.join(chr(i) for i in plaintext_in_ascii))

    def test_decrypt(self):
        decoder = JWTDecryptor(*self.decryptor_args)

        tokens = encrypted_jwt.split('.')

        self.assertEqual(jwe_protected_header, tokens[0])

        cipher_text = decoder._base64_decode(tokens[3])  # pylint: disable=protected-access
        tag = bytes(decoder._base64_decode(tokens[4]))  # pylint: disable=protected-access

        decrypted_token = decoder._decrypt_cipher_text(cipher_text, iv, cek, tag, jwe_protected_header)  # pylint: disable=protected-access
        self.assertEqual(plaintext, decrypted_token.decode())


if __name__ == '__main__':
    unittest.main()
