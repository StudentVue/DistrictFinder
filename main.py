import requests
import html
import re

s = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ProcessWebServiceRequest xmlns="http://edupoint.com/webservices/"><userID>EdupointDistrictInfo</userID><password>Edup01nt</password><skipLoginLog>1</skipLoginLog><parent>0</parent><webServiceHandleName>HDInfoServices</webServiceHandleName><methodName>GetMatchingDistrictList</methodName><paramStr>&lt;Parms&gt;&lt;Key&gt;5E4B7859-B805-474B-A833-FDB15D205D40&lt;/Key&gt;&lt;MatchToDistrictZipCode&gt;{0}&lt;/MatchToDistrictZipCode&gt;&lt;/Parms&gt;</paramStr></ProcessWebServiceRequest></soap:Body></soap:Envelope>'''

headers = {
    'SOAPAction': 'http://edupoint.com/webservices/ProcessWebServiceRequest',
    'Content-Type': 'text/xml; charset=utf-8'
}


def get_schools_by_zip_code(zip_code):
    r = requests.post('https://support.edupoint.com/Service/HDInfoCommunication.asmx',
                      data=s.format(zip_code),
                      headers=headers)

    districts = re.findall(r'<DistrictInfo (.+)/>', html.unescape(r.text))
    return [
        {
            k: v for (k, v) in ((prop[:prop.index('=')], prop[prop.index('=') + 2: len(prop)])
                                for prop in re.split(r'" ', district)[:-1])
        } for district in districts
    ]


if __name__ == '__main__':
    print(get_schools_by_zip_code(94127))
