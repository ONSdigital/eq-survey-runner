# These keys have to be a bytes strings due to an oddity in the underlying cryptography library

SR_PUBLIC_PEM = b'-----BEGIN PUBLIC KEY-----\n' \
                b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt8LZnIhuOdL/BC029GOa\n' \
                b'JkVUAqgp2PcmbFr2Qwhf/514DUUQ9sKJ1rvwvbmmW2zE8JRtdY3ey0RXGtMn5UZH\n' \
                b's8NReHzMxvsmHN4VuaGEnFmPwO821Tkvg0LpKsLkotcw793FD/fut44N2lhpTSW2\n' \
                b'Sc82uG0p9A+Kud8HCIaWaluosghk9rbMGYDzZQk8cA91GtKJRmIOED4PorB/dexD\n' \
                b'f37qhuWNQgzyNyTti1DTDUIWyzQQJp926vLbkOip6Fc2R13hOFNETe68Rrw/h3hX\n' \
                b'EFS17uPFZHsxvm9PFXX9KZMS25ohqbNh97I94LL4o4wybl6LaE6lJEHiD6docD0B\n' \
                b'6wIDAQAB\n' \
                b'-----END PUBLIC KEY-----\n'


SR_PRIVATE_PEM = b'-----BEGIN RSA PRIVATE KEY-----\n' \
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


RRM_PUBLIC_PEM = b'-----BEGIN PUBLIC KEY-----\n' \
                 b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvZzMraB96Wd1zfHS3vW3\n' \
                 b'z//Nkqz+9HfwViNje2Y5L6m3K/7raA0kUsWD1f6X7/LIJfkCEctCEj9q19+cX30h\n' \
                 b'0pi6IOu92MlIwdH/L6CTuzYnG4PACKT8FZonLw0NYBqh8p4vWS8xtNHNjTWua/FF\n' \
                 b'TlxdtYnEb9HbUZkg7dXAtnikozlE/ZZSponq7K00h3Uh9goxQIavcK1QI8pw5V+T\n' \
                 b'8V8Ue7k98W8LpbYQWm7FPOZayu1EoJWUZefdOlYAdeVbDS4tjrVF+3za+VX3q73z\n' \
                 b'JEfyLEM0zKrkQQ796gfYpkzDYwJvkiW7fb2Yh1teNHpFR5tozzMwUxkREl/TQ4U1\n' \
                 b'kwIDAQAB\n' \
                 b'-----END PUBLIC KEY-----\n'

RRM_PRIVATE_PEM = b'-----BEGIN RSA PRIVATE KEY-----\n' \
                  b'Proc-Type: 4,ENCRYPTED\n' \
                  b'DEK-Info: AES-256-CBC,C2C5740E6DA1DD915CA90CFFCBDFA5B2\n' \
                  b'\n' \
                  b'nlAOzfOUcrksZS2H0WLE27ME/wpuDo8rimRBxA++EHe+2HJsXyiNz+PRPHPOIvcW\n' \
                  b'lGtPgLcfwT9A+pwico0s1u0N8/XQC21640r30xBQSW6Y+msPLoibnvl6bkDO0z/z\n' \
                  b'x+mqCQvPTQEpJwwbtE8wFbrs74P0y6EUFIu8m8yPBg9Fmt8noAuR227l5tg/TLga\n' \
                  b'HMFYT5mFO7g+oJvtJhOxXcCNf3EcoRQOlap9PHq2daVSTXy+qCTVe5AVDIlufidp\n' \
                  b'fl4qGAqu5z2JbI8dsm+WJGtvqGacNoLOHsKHFGx/Qgy5em/NPAf9ak5fgjxQrrK1\n' \
                  b'UWh+EymVsSQKN8MXPWYSzthSdoYAUuWu1iaDbcJw8CWU2vfmgXMxjTPUvsx0wRUX\n' \
                  b'4tUfNtgqxcIsh1bH3MtcCeqxtyUOG96f2TGCx6gofUiKxwMoBzk3HqdgwexvZW1L\n' \
                  b'64xgbY02AvztjxD8KFNWXQgji9mKorplqCIugpj67oRIwVOwdzfebiLk5eFb31Jj\n' \
                  b'RZumElCCo2UtQe/fAqebBAC2CtaMuSBTozmHNPx9DDEGVQH6i/ZZHTHCvFG1+MJS\n' \
                  b'PyTRQZnS4qnj+b7ObBNvAhSPsUD6hKI0yV3k1I3P+Hi1syMMIFKUwahzUReLF5le\n' \
                  b'CdT4rMgrpHDyw5QUH5IjHzc0AXxoomM5UaUkk65E+MHU3nq37E7ExE6AFTdqmP4t\n' \
                  b'I67Ed+bHNe6qxweDtuuc84Ok24k8OxRoZchrhFytWpk1lkijGUb/fRdmS4/6HiKJ\n' \
                  b'RgkZ+VHi/FQN3/fedzfHouWYKaGKI51MEQfB7cSL8g13MchhGVOmu9TG6+F1/qRc\n' \
                  b'dNil/8PE/cafxFEImW1v//ycLx0k/njfXyi/U2Vk8+WEDEtPe1fsF0F+vdnRH+l3\n' \
                  b'zWsPtgqRqVAWZxn28xN8xNA9+iaoKH869/OVRDbmeU1tNQaSnCE3Ltkrg5Qoc8r5\n' \
                  b'nPEviH812mnKkS299NVQFHbBSN2WDrf27gYKDn0ajSBo9GBeQJQOPTGWkMlHnOFB\n' \
                  b'ALphV1Ul2APJih7rgcHh6RubgN6X3EfFCL5VzSlpqGnYp9Ov1+U0iLjyfMWgLOd8\n' \
                  b'pXyIOl9qMJUZchjLsFXCj2u/SGuAu2ojMnG+0UFxYnx+f9l6UcUvEAYJIJop6XS9\n' \
                  b'tB5rgsqQwYAB3N7yQ/C12fVc6qITffRxqBaGEe9yPFZO5XmUgn/oNtJuArSPBAIe\n' \
                  b'InZI1TWbvAeVYfDQEJDsM1ND0X17MAPghQXH4nVavJydGbUY5sg9QJF2BBP6sT9Y\n' \
                  b'zvgYUD5RZfzwuZOfdy46fv3VmqR2fYKuj1zVXFqGiINFsQb6airDt/11NJ0p8avo\n' \
                  b'9X/eR20/uU6gtk5ABF2U3zepa3NheMhZJUmHysmYKiYwO6sJ1XTpAjNhmmLcOsEI\n' \
                  b'XXCtQwd8uNYVzxSlbCSB3EQ841Ix9Z1+z/qUsFM01dX882It7qP/M7AdhogEYaPR\n' \
                  b'ZNMk0igVzh9T+6ErSOngoug0nLRqZsKlMhC7RNskMpIqt8iGLGnjLRT+4adwvCUW\n' \
                  b'ERd/A2RoDdedhgV49v9mYUWtENxGOr1VmOG98FzdmfUqwxNpukfhF9fz7iCB+Bnk\n' \
                  b'-----END RSA PRIVATE KEY-----\n'
