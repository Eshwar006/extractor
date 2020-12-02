import logging
import requests


class HttpClient(object):

    def __init__(self, timeout=60):
        self.__timeout = timeout

    def get(self, **kwargs):

        logging.info("GET URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.get(**kwargs)
        r.raise_for_status()
        return r

    def post(self, **kwargs):

        logging.info("POST URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.post(**kwargs)
        r.raise_for_status()
        return r

    def put(self, **kwargs):

        logging.info("PUTT URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.put(**kwargs)
        r.raise_for_status()
        return r

    def delete(self, **kwargs):

        logging.info("DELETE URL: {url}, HEADERS: {headers}".format(url=kwargs.get("url", ""), headers=kwargs.get("headers", "")))
        kwargs["timeout"] = self.__timeout
        r = requests.delete(**kwargs)
        r.raise_for_status()
        return r