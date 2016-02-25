#!/usr/bin/env python

import cherrypy
import os.path
import json
import traceback


config = {
 '/': {},
}


from cherrypy.process import servers
def fake_wait_for_occupied_port(host, port): return
servers.wait_for_occupied_port = fake_wait_for_occupied_port


class SMMock:

    @cherrypy.expose
    def default(self, *args, **params):
        #*args is list of any paths after /sodapi/
        #**params is map of query parameters

        uriPathTuple = repr(args)
        queryParamMap = repr(params)
        requestURLInfo = "Extra path info: %s, query param map =%s" % (uriPathTuple, queryParamMap)
        try:
            print 'Json decoding . . . '
            print requestURLInfo
            print queryParamMap.replace("u'","'").replace("'",'"')
            #queryParamMap = json.loads(queryParamMap.replace("u'","'").replace("'",'"'))

        except:
            print traceback.format_exc()
            pass

        cmd = None
        sn = None
        ai = None



    def loadFile(self, filename):
        fHandle = open( filename, 'r' )
        fileContents = fHandle.read()
        try:
            json.loads(fileContents)
            print 'Loaded JSON ' + filename


            json.dumps(fileContents, indent=3)
        except:
            pass

        return fileContents

class Root:
    """ Sample request handler class. """
    #bss = SMMock()

    @cherrypy.expose
    def index(self):
        # Let's link to another method here.
        return 'Server is up!'
    #index.exposed = True

    @cherrypy.expose
    def showMessage(self):
        # Here's the important message!
        return "showing message . .  !"


    @cherrypy.expose
    def default(self, *args, **params):
        #*args is list of any paths after /sscapi/
        #**params is map of query parameters
        uriPathTuple = repr(args)
        queryParamMap = repr(params)
        queryParamMap = params

        requestURLInfo = "Extra path info: %s, query param map =%s" % (uriPathTuple, queryParamMap)
        cmd = None
        sn = None
        ainfo = None
        rsurl = None
        ai = None

        try:

            #http://<host>:<port>/<app_server>/register?cmd=start&sn=123456&rsurl=<server>:<port>/esam/esamservice&ainfo=<activation code>
            if 'register' in uriPathTuple:

                cmd = None
                sn = None
                ainfo = None
                rsurl = None

                if queryParamMap.has_key('cmd'):
                    cmd = queryParamMap['cmd']
                    print 'cmd = ' + cmd

                if queryParamMap.has_key('sn'):
                    sn = queryParamMap['sn']
                    print 'sn = ' + sn

                if queryParamMap.has_key('ainfo'):
                    ainfo = queryParamMap['ainfo']
                    print 'ainfo = ' + ainfo

                if queryParamMap.has_key('rsurl'):
                    rsurl = queryParamMap['rsurl']
                    print 'rsurl = ' + rsurl


            elif 'bsauthorize' in uriPathTuple:
                #/bss/bsauthorize?cmd=start&sn=<device_identifier>
                #return self.loadFile('./metadata/metadata-placeholder.jpg')
                okResponse = """<rpksmsresp>
 <rc>0</rc>
 <msg>OK</msg>
</rpksmsresp>"""

                missingParameterResponse = """<rpksmsresp>
 <rc>1100</rc>
 <msg>Missing parameter: @param</msg>
</rpksmsresp>"""

                entitlementResponse = okResponse


                if queryParamMap.has_key('cmd'):
                    cmd = queryParamMap['cmd']
                    print 'cmd = ' + cmd

                if queryParamMap.has_key('sn'):
                    sn = queryParamMap['sn']
                    print 'sn = ' + sn

                if queryParamMap.has_key('ai'):
                    ai = queryParamMap['ai']
                    print 'ai = ' + ai


                if cmd == None:
                    entitlementResponse =  missingParameterResponse.replace('@param', 'cmd')
                    return entitlementResponse

                elif cmd == 'reg-start':
                    if sn == None:
                        entitlementResponse =  missingParameterResponse.replace('@param', 'sn')
                        return entitlementResponse
                    if ai == None:
                        entitlementResponse =  missingParameterResponse.replace('@param', 'ai')
                        return entitlementResponse
                elif cmd == 'reg-stop':
                    if sn == None:
                        entitlementResponse =  missingParameterResponse.replace('@param', 'sn')
                        return entitlementResponse
                else:
                    entitlementResponse =  missingParameterResponse.replace('@param', 'cmd')
                    return entitlementResponse

                return entitlementResponse



        except:
            print requestURLInfo
            raise

        return requestURLInfo


tutconf = os.path.join(os.path.dirname(__file__), 'smmock.conf')



if __name__ == '__main__':
    cherrypy.quickstart(Root(), config=tutconf)





