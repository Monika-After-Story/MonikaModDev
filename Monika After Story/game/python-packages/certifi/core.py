# -*- coding: utf-8 -*-

"""
certifi.py
~~~~~~~~~~

This module returns the installation location of cacert.pem.
"""
import os


__CERT_URL = "raw.githubusercontent.com"
__CERT_PATH = "certifi/python-certifi/master/certifi/cacert.pem"


def where():
    f = os.path.dirname(__file__)

    return os.path.join(f, 'cacert.pem')


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
        [0] - 0 if success
              1 if no update
              -1 if some error occured
              -2 if an SSL error occured 
              -3 if no SSL library
        [1] - server response if [0] is -1, otherwise None
    """
    try:
        return _check_update_internal()
    except (ImportError, AttributeError):
        # no ssl lib or ssl not loaded
        return -3, None

def _check_update_internal():
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
            return -1, server_response

        # read data
        cert_data = server_response.read()

        if has_cert():
            with open(where(), "r") as curr_cert:
                

    except ssl.SSLError:
        # site demanded SSL but no cert
        return -2, None

    except httplib.HTTPException:
        # unknown http exception
        return -1, server_response

    finally:
        h_conn.close()

