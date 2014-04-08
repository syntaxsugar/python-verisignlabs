import json
from time import sleep
import urllib
import urllib2
import datetime


class BetterHTTPErrorProcessor(urllib2.BaseHandler):
    def http_error_400(self, request, response, code, msg, hdrs):
        return response


class DomainScore(object):
    def __init__(self):
        self.DETAILS_API_URL = "https://api-domainscore.verisign-grs.com/v2/domain/"
        self.API_KEY = "SECRET-API-KEY"

    @staticmethod
    def _setTimeout(headers):
        print "DEBUG SetTimeout"

        limit = int(headers.getheader('x-ratelimit-limit'))

        remaining_limit = int(headers.getheader('x-ratelimit-remaining'))
        print "Limit %s from %s" % (remaining_limit, limit)

        if remaining_limit == 1:
            resetms = int(headers.getheader('x-ratelimit-resetms'))
            reset_datetime = datetime.datetime.fromtimestamp(resetms / 1000)
            current_datetime = datetime.datetime.now()
            print "Reset in ", reset_datetime
            print "Current Time", current_datetime
            rozdil = reset_datetime - current_datetime
            sec_rozdil = rozdil.seconds + 1
            if sec_rozdil > 150:
                sec_rozdil = 60
            print "Je nutne pockat %s sekund" % sec_rozdil
            sleep(sec_rozdil)

    def getDetails(self, domain_name):
        url = "%s%s" % (self.DETAILS_API_URL, domain_name)
        req = urllib2.Request(url)
        req.add_header('X-DOMAINSCORE-APIKEY', self.API_KEY)
        req.add_header('Accept', 'application/json')

        status_code = None
        try:
            response = urllib2.urlopen(req)
            self._setTimeout(response.info())
        except urllib2.HTTPError, e:
            status_code = e.code
        else:
            status_code = response.getcode()

            return status_code, json.loads(response.read())

        return status_code, ""

    def search(self, keywords, limit=None):
        url = 'https://api-domainscore.verisign-grs.com/v2/search'

        values = {'q': keywords}
        #params = urllib.urlencode({'q': keywords, 'max': 60})
        if limit is not None:
            values['max'] = limit
        params = urllib.urlencode(values)

        req = urllib2.Request(url)
        req.add_header('X-DOMAINSCORE-APIKEY', self.API_KEY)
        req.add_header('Accept', 'application/json')
        status_code = None
        try:
            response = urllib2.urlopen(req, params)
            self._setTimeout(response.info())
        except urllib2.HTTPError, e:
            status_code = e.code
        else:
            status_code = response.getcode()

            return (status_code, json.loads(response.read()))

        return (status_code, "")

        return None