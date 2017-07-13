# 4. Use kid to identify key pair

Date: 11/07/2017

## Status

Proposed

## Context

We need the ability to identify which keys are used to sign and encrypt messages so that we can support multiple keys

## Decision

We will use the kid value in the header of the JWE and JWT tokens to identify the key that was used to sign or encrypt the message payload.

The kid value will be a SHA1 hash of the digest of the Public Key

## Consequences

Multiple keys are able to be used by upstream systems. This means that the process of rotating keys should be a zero downtime operation.

This change should be a breaking change to any upstream system that does not pass a valid kid. 
So during the crossover period the previous value of EDCRRM will be valid for the JWT header and a default key will be used if no kid is passed in the JWE header.  
