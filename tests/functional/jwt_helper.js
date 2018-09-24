const KJUR = require('jsrsasign');
const fs = require('fs');
const uuid = require('uuid/v1');
const JSONWebKey = require('json-web-key');
const jose = require('node-jose');
const JWK = jose.JWK;
const JWE = jose.JWE;

const crypto = require('crypto');

const signingKey = './tests/functional/sdc-user-authentication-signing-rrm-private-key.pem';
const encryptionKey = './tests/functional/sdc-user-authentication-encryption-sr-public-key.pem';

const signingKeyString = fs.readFileSync(signingKey, 'utf8');  // get private key
const encryptionKeyString = fs.readFileSync(encryptionKey, 'utf8');  // get public key

const schemaRegEx = /^([a-z0-9]+)_(\w+)\.json/;

module.exports = function generateToken(schema, userId, collectionId, periodId = '201605', periodStr = 'May 2016', regionCode = 'GB-ENG', languageCode = 'en', sexualIdentity = false) {
  let schemaParts = schemaRegEx.exec(schema);

  // Header
  let oHeader = {
    alg: 'RS256',
    typ: 'JWT',
    kid: '709eb42cfee5570058ce0711f730bfbb7d4c8ade'
  };

  // Payload
  let oPayload = {
    tx_id: uuid(),
    jti: uuid(),
    iat: KJUR.jws.IntDate.get('now'),
    exp: KJUR.jws.IntDate.get('now') + 1800,
    user_id: userId,
    case_id: uuid(),
    ru_ref: '12346789012A',
    ru_name: 'Apple',
    trad_as: 'Apple',
    eq_id: schemaParts[1],
    collection_exercise_sid: collectionId,
    period_id: periodId,
    period_str: periodStr,
    ref_p_start_date: '2017-01-01',
    ref_p_end_date: '2017-02-01',
    employment_date: '2016-06-10',
    form_type: schemaParts[2],
    return_by: '2017-03-01',
    region_code: regionCode,
    language_code: languageCode,
    sexual_identity: sexualIdentity,
    account_service_url: 'http://localhost:8000'
  };

  // Sign JWT, password=616161
  let sHeader = JSON.stringify(oHeader);
  let sPayload = JSON.stringify(oPayload);

  let prvKey = KJUR.KEYUTIL.getKey(signingKeyString, 'digitaleq');

  let sJWT = KJUR.jws.JWS.sign('RS256', sHeader, sPayload, prvKey);

  let webKey = JSONWebKey.fromPEM(encryptionKeyString);

  let shasum = crypto.createHash('sha1');
  shasum.update(encryptionKeyString);
  let encryptionKeyKid = shasum.digest('hex');

  return JWK.asKey(webKey.toJSON())
    .then(function(jwk) {
      let cfg = {
        contentAlg: 'A256GCM'
      };
      let recipient = {
        key: jwk,
        header: {
          alg: 'RSA-OAEP',
          kid: encryptionKeyKid
        }
      };
      let jwe = JWE.createEncrypt(cfg, recipient);
      return jwe.update(sJWT).final();
    })
    .then(function(result) {
      let token = result.protected + '.' +
          result.recipients[0].encrypted_key + '.' +
          result.iv + '.' +
          result.ciphertext + '.' +
          result.tag;

      return token;
    });
};
