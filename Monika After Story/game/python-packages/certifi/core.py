# -*- coding: utf-8 -*-

"""
certifi.py
~~~~~~~~~~

This module returns the installation location of cacert.pem.
"""
import os
import hashlib


__CERT_URL = "raw.githubusercontent.com"
__CERT_PATH = "certifi/python-certifi/master/certifi/cacert.pem"


### return values
RV_SUCCESS = 0
RV_NO_UPDATE = 1

RV_ERR_BAD_SSL = -1
RV_ERR_BAD_SSL_LIB = -2
RV_ERR = -5


def where():
    f = os.path.dirname(__file__)

    return os.path.join(f, 'cacert.pem')


def ssl_ctx():
    """
    Gets the SSLContext object using our certs.

    Raises SSLError if the cert chain is bad.

    RETURNS: tuple of the following format:
        [0] - RV_SUCCESS if success
              RV_ERR_BAD_SSL if cert error
              RV_ERR_BAD_SSL_LIB if no SSL lib
        [1] - SSLContext if success, None otherwise
    """
    try:
        return _ssl_ctx()
    except (ImportError, AttributeError):
        return RV_ERR_BAD_SSL_LIB, None


def _ssl_ctx():
    """
    This is so import errors can be caught.

    REUTRNS: see ssl_ctx
    """
    import ssl # must be here because may not hve ssl on start

    try:

        ctx = ssl.create_default_context()
        ctx.load_cert_chain(where())
        return RV_SUCCESS, ctx

    except ssl.SSLError:
        return RV_ERR_BAD_SSL, None


def has_cert():
    """
    Checks if we have a cert. does NOT check if cert is valid or anything.

    RETURNS: True if we have a cert, False if not
    """
    return os.access(where(), os.F_OK)


def check_update():
    """
    Checks for a cert update, dls it, and saves it if updated.

    ONLY CALL THIS IN RUNTIME

    RETURNS: tuple:
        [0] - RV_SUCCESS if success
              RV_NO_UPDATE if no update
              RV_ERR if some error occured
              RV_ERR_BAD_SSL if an SSL error occured 
              RV_ERR_BAD_SSL_LIB if no SSL library
        [1] - server response if [0] is RV_ERR, otherwise None
    """
    try:
        return _check_update()
    except (ImportError, AttributeError):
        # no ssl lib or ssl not loaded
        return RV_ERR_BAD_SSL_LIB, None


def _check_update():
    """
    Internal check_update. This is import errors can be caught

    RETURNS: see check_update
    """
    # the imports are here since we may not have ssl on start
    import ssl
    import httplib

    h_conn = httplib.HTTPSConnection(__CERT_URL)

    try:
        # may fail if no SSL and site demands it
        h_conn.connect()

        h_conn.request("GET", "/" + __CERT_PATH)
        server_response = h_conn.getresponse()

        if server_response.status != 200: 
            # unexpected respponses
            return RV_ERR, server_response

        # read data
        cert_data = server_response.read()

        if has_cert():
            new_cert_hash = hashlib.sha256(cert_data)

            with open(where(), "r") as curr_cert:
                curr_cert_hash = hashlib.sha256(curr_cert.read())

                if new_cert_hash.hexdigest() == curr_cert_hash.hexdigest():
                    # current file is exact same so no need to save
                    return RV_NO_UPDATE, None

        # save the cert to our location
        with open(where(), "w") as new_cert:
            new_cert.write(cert_data)

        return RV_SUCCESS, None

    except ssl.SSLError:
        # site demanded SSL but no cert
        return RV_ERR_BAD_SSL, None

    except httplib.HTTPException:
        # unknown http exception
        return RV_ERR, server_response

    finally:
        h_conn.close()

