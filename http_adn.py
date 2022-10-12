import http.client as request
import uuid, json, ssl

import conf


def http_request(origin, path, method, ty, bodyString):
    headers= {
        'Accept' : 'application/' + conf.conf['ae']['bodytype'],
        'X-M2M-RI' : str(uuid.uuid1()),
        'X-M2M-Origin' : origin,
        'Locale' : 'en'
    }

    if len(bodyString) > 0:
        headers['Content-Length'] = len(bodyString)

    if method == 'POST':
        if ty == '':
            a = ''
        else:
            a = '; ty={}'.format(ty)
        headers['Content-Type'] = 'application/vnd.onem2m-res+' + conf.conf['ae']['bodytype'] + a
    elif method == 'PUT':
        headers['Content-Type'] = 'application/vnd.onem2m-res+' + conf.conf['ae']['bodytype']

    jsonObj = {}

    try:
        if conf.conf['usesecure'] == 'enable':
            # ca = open('./ca-crt.pem')
            # rejectUnauthorized = False
            context = ssl.SSLContext().load_verify_locations(cafile='./ca-crt.pem')
            http = request.HTTPSConnection(conf.conf['cse']['host'], conf.conf['cse']['port'], context=context)
        else:
            http = request.HTTPConnection(conf.conf['cse']['host'], conf.conf['cse']['port'])

        http.request(method, path, bodyString, headers)
        response = http.getresponse()
        res_status = response.getheader('x-m2m-rsc')
        res_body = (response.read()).decode('utf-8')
        if conf.conf['ae']['bodytype'] == 'xml':
            pass
        elif conf.conf['ae']['bodytype'] == 'cbor':
            pass
        else:
            try:
                if res_body == '':
                    jsonObj = {}
                else:
                    jsonObj = json.loads(res_body)

                return int(res_status), jsonObj
            except:
                jsonObj = {}
                jsonObj['dbg'] = res_body

                return 9999, jsonObj
    except Exception as e:
        jsonObj = {}
        jsonObj['dbg'] = e
        return 9999, jsonObj


def crtae(parent, rn, api):
    results_ae = {}

    bodyString = ''

    if conf.conf['ae']['bodytype'] == 'xml':
        pass
    elif conf.conf['ae']['bodytype'] == 'cbor':
        pass
    else:
        results_ae['m2m:ae'] = {}
        results_ae['m2m:ae']['api'] = api
        results_ae['m2m:ae']['rn'] = rn
        results_ae['m2m:ae']['rr'] = True

        bodyString = json.dumps(results_ae)

    rsc, res_body = http_request(conf.conf['ae']['id'], parent, 'POST', '2', bodyString)

    return rsc, res_body


def crtct(parent, rn, count):
    results_ct = {}

    bodyString = ''
    if conf.conf['ae']['bodytype'] == 'xml':
        pass
    elif conf.conf['ae']['bodytype'] == 'cbor':
        pass
    else:
        results_ct['m2m:cnt'] = {}
        results_ct['m2m:cnt']['rn'] = rn
        results_ct['m2m:cnt']['lbl'] = [rn]
        bodyString = json.dumps(results_ct)
        print(bodyString)

    rsc, res_body = http_request(conf.conf['ae']['id'], parent, 'POST', '3', bodyString)
    print(str(count) + ' - ' + parent + '/' + rn + ' - x-m2m-rsc : ' + str(rsc) + ' <----')
    print(res_body)

    return rsc, res_body, count


def crtsub(parent, rn, nu, count):
    bodyString = ''
    results_ss = {}
    if conf.conf['ae']['bodytype'] == 'xml':
        pass
    elif conf.conf['ae']['bodytype'] == 'cbor':
        pass
    else:
        results_ss['m2m:sub'] = {}
        results_ss['m2m:sub']['rn'] = rn
        results_ss['m2m:sub']['enc'] = {"net": [1,2,3,4]}
        results_ss['m2m:sub']['nu'] = [nu]
        results_ss['m2m:sub']['nct'] = 2
        bodyString = json.dumps(results_ss)
        print(bodyString)

    rsc, res_body = http_request(conf.conf["ae"]["id"], parent, 'POST', '23', bodyString)
    print(str(count) + ' - ' + parent + '/' + rn + ' - x-m2m-rsc : ' + str(rsc) + ' <----')
    print(json.dumps(res_body))

    return rsc, res_body, count


def delsub(target, count):
    rsc, res_body = http_request('Superman', target, 'DELETE', '', '')
    print(str(count) + ' - ' + target + ' - x-m2m-rsc : ' + str(rsc) + ' <----')
    print(res_body)

    return rsc, res_body, count


def crtci(parent, content_obj, socket):
    results_ci = {}
    bodyString = ''
    if conf.conf['ae']['bodytype'] == 'xml':
        pass
    elif conf.conf['ae']['bodytype'] == 'cbor':
        pass
    else:
        results_ci['m2m:cin'] = {}
        results_ci['m2m:cin']['con'] = content_obj
        bodyString = json.dumps(results_ci)

    rsc, res_body = http_request(conf.conf['ae']['id'], parent, 'POST', '4', bodyString)

    return rsc, res_body, parent, socket