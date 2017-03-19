#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
import memcache
import base64
import sys


class Memcache_example(object):

    def __init__(self):
        """Initialisation"""
        # Populated in set_client()
        self.client = None
        # Populated in gen_keys()
        self.privkey = None
        self.pubkey = None
        self.sentinel = {"error": True}
        self.keys = []

    def main(self):
        self.set_client()
        self.gen_keys()
        if not self.set_some_values():
            return []
        res = self.get_some_values()
        return res

    def set_client(self):
        """Memcached client initialisation"""
        self.client = memcache.Client(['127.0.0.1:11211'], debug=0)

    def gen_keys(self):
        """Generates and sets a pair of certificates"""
        key = RSA.generate(1024)
        self.privkey = key.exportKey('DER')
        self.pubkey = key.publickey().exportKey('DER')

    def encrypt(self, key, value):
        """
        Encrypts given key, value

        :param key: plain key
        :param value: plain value

        :returns: Encrypted values
        """
        rsa_key = RSA.importKey(self.pubkey)
        pub_cipher = PKCS1_v1_5.new(rsa_key)
        key, value = pub_cipher.encrypt(key), pub_cipher.encrypt(value)
        key, value = base64.b32encode(key), base64.b32encode(value)
        return key, value

    def decrypt(self, key, value):
        """
        Decrypts given key, value

        :param key: encrypted key
        :param value: encrypted value

        :returns: Decrypted values
        """
        rsa_key = RSA.importKey(self.privkey)
        priv_cipher = PKCS1_v1_5.new(rsa_key)
        key, value = base64.b32decode(key), base64.b32decode(value)
        key = priv_cipher.decrypt(key, self.sentinel)
        value = priv_cipher.decrypt(value, self.sentinel)
        return key, value

    def set_some_values(self):
        """
        Writes 100 keys into memcached

        :returns: True if success or False if not
        """
        res = True
        for i in xrange(100):
            k, v = self.encrypt(str(i), str(i) * 5)
            res = res and self.client.set(k, v)
            self.keys.append(k)
            if res is False:
                return res
        return res

    def get_some_values(self):
        """
        Writes 100 keys into memcached

        :returns: a list of key-values
        """
        res = []
        for k in self.keys:
            v = self.client.get(k)
            res.append(self.decrypt(k, v))
        return res


if __name__ == '__main__':
    try:
        m = Memcache_example()
        result = m.main()
        if not result:
            print "Something went wrong during fulling it in"
        for i in result:
            print i[0], i[1]
    except KeyboardInterrupt:
        print "Execution was interrupted by user"
        sys.exit(1)
