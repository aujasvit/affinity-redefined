import secp256k1


class Key:
    def __init__(self, priv_key = None):
        if priv_key is not None:
            #Load existing private key which is provided as a hex
            self.__private_key = secp256k1.PrivateKey(privkey = priv_key, raw = False)
            self.__private_key_hex = self.__private_key.serialize()
            assert self.__private_key_hex.deserialize() == self.__private_key
        else:
            #Generate new private key
            self.__private_key = secp256k1.PrivateKey()
            self.__private_key_hex = self.__private_key.serialize()
            assert self.__private_key_hex.deserialize() == self.__private_key

        #get rid of odd/even prefix in line with BIP340 Schnorr signature implementation protocol
        self.public_key_hex = self.__private_key.pubkey.serialize(compressed=True).hex()[2:]
        self.public_key = bytearray.fromhex(self.public_key_hex)

        #return public and private key as hex
        return {"private key": self.__private_key_hex, "public key": self.public_key_hex}


    def sign(self, message):
        # Message will be 32-byte SHA256 hash as specified in NIP-01
        signature = self.__private_key.schnorr_sign(message, raw = True)
        assert self.public_key.schnorr_verify(message, signature, raw = True)
        return signature

    def validate_signature(self, message, signature):
        assert self.public_key.schnorr_verify(message, signature, raw = True)