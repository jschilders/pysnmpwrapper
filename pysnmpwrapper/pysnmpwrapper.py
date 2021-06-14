from pysnmp.hlapi import SnmpEngine, CommunityData, UsmUserData, UdpTransportTarget, Udp6TransportTarget, ContextData
from pysnmp.hlapi import getCmd, nextCmd, bulkCmd, setCmd
from pysnmp.hlapi import SnmpEngine
from pysnmp.hlapi import ObjectIdentity, ObjectType
from pysnmp.hlapi import varbinds

class SnmpWrapper:
    def __init__(self, hostname, community='public', port=161, timeout=30, retries=3, **kwargs):

        snmpengine = kwargs.get(
            'SnmpEngine', SnmpEngine()
        )
        #
        # Hier ergens SNMPv3 infreubelen
        #
        communitydata = kwargs.get(
            'CommunityData', CommunityData(
                community,
                mpModel = 1
            )
        )
        #
        # Hier ergens IPv6 transport infreubelen.
        #
        transport = kwargs.get(
            'TransportTarget', UdpTransportTarget(
                (
                    hostname,
                    port
                ),
                timeout = timeout,
                retries = retries
            )
        )
        contextdata = kwargs.get(
            'ContextData', ContextData()
        )
        self.snmpSessionParam = [
            snmpengine,
            communitydata,
            transport,
            contextdata
        ]
        self.snmpExtraParam = [
            kwargs.get('nonRepeaters', 0),
            kwargs.get('maxRepetitions', 100)
        ]
        self.snmpFlags= {
            'lookupMib':              kwargs.get('lookupMib', True),
            'lexicographicMode':      kwargs.get('lexicographicMode', False),
            'ignoreNonIncreasingOid': kwargs.get('ignoreNonIncreasingOid', False),
            'maxRows':                kwargs.get('maxRows'),
            'maxCalls':               kwargs.get('lexicographicMode')
        }
        self.mibViewController = varbinds.AbstractVarBinds.getMibViewController(SnmpEngine())


    def _get(self, oid):
        snmpSessionParam = self.snmpSessionParam
        snmpFlags = self.snmpFlags
        typeObject = self.oidlistToObjects(oid)
        iterator = getCmd(
            *snmpSessionParam,
            *typeObject,
            **snmpFlags
            )
        return iterator

    def _set(self, oid, value):
        snmpSessionParam = self.snmpSessionParam,
        snmpFlags = self.snmpFlags
        typeObject = self.oidToObject(oid=oid, val=value)
        iterator = setCmd(
            *snmpSessionParam,
            typeObject,
            **snmpFlags
            )
        return iterator

    def _next(self, oidlist):
        snmpSessionParam = self.snmpSessionParam
        snmpFlags = self.snmpFlags
        typeObject = self.oidlistToObjects(oidlist)
        iterator = nextCmd(
            *snmpSessionParam,
            *typeObject, 
            **snmpFlags
            )
        return iterator

    def _bulk(self, oidlist):
        snmpSessionParam = self.snmpSessionParam
        snmpFlags = self.snmpFlags
        snmpExtraParam = self.snmpExtraParam
        typeObject = self.oidlistToObjects(oidlist)
        iterator = bulkCmd(
            *snmpSessionParam,
            *snmpExtraParam,
            *typeObject,
            **snmpFlags
            )
        return iterator

    def _fetch_one(self, iterator):
        result = None
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        except StopIteration:
            print('Iterator exhausted')
        else:
            if errorIndication or errorStatus:
                self._handle_error(errorIndication, errorStatus, errorIndex, varBinds)
            else:
                result = varBinds[0]
        finally:
            return result

    def _fetch_all(self, iterator):
        results_list = []
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication or errorStatus:
                self._handle_error(errorIndication, errorStatus, errorIndex, varBinds)
            else:
                results_list.extend(
                    [varBind for varBind in varBinds]
                )
        return results_list

    def _handle_error(self, errorIndication, errorStatus, errorIndex, varBinds):
        # TODO
        if errorIndication:
            print (f'SNMP Engine error: {errorIndication}')
        elif errorStatus:
            if errorIndex:
                errorIndex -= 1
                errorObject = varBinds[errorIndex].prettyPrint()
                print(f'{errorStatus} at index {errorIndex} with object "{errorObject}"')
            else:
                print(f'{errorStatus}')
        

    @staticmethod
    def oidToObject(oid, value=None):
        #
        # Takes a string, or a list of strings and integers, and returns an ObjectType object
        #
        identityObject = ObjectIdentity(oid) if isinstance(oid, str) else ObjectIdentity(*oid)
        typeObject = ObjectType(identityObject, value) if value else ObjectType(identityObject)
        return typeObject

    @staticmethod
    def oidlistToObjects(*oid):
        #
        # oid will always be a tuple, even if only 1 argument was specified.
        # In case the tuple has only 1 argument (this can also be a list or tuple)
        # get that single item from the tuple and process further.
        # Example case: you specify a list of tuples
        #
        while len(oid) == 1 and not isinstance(oid[0], str):
            oid = oid[0]
        #
        # Create a list from all strings and integers in oid, use that to create oid object and return as single-item list.
        # => ('IF-MIB', 'ifInOctets') <= or => ['SNMPv2-MIB', 'sysDescr', 0] <=
        #
        params = [ param for param in oid if isinstance(param, (str, int)) ]
        if params:
            return [ ObjectType(ObjectIdentity(*params)) ]
        #
        # for each list-like item in oid, create an oid object with the contents of that list-like item, and return a list of oid objects.
        # => [ ('IF-MIB', 'ifInOctets'), ['SNMPv2-MIB', 'sysDescr', 0] ] <=
        #
        return [ ObjectType(ObjectIdentity(*params)) for params in oid if isinstance(params, (tuple, list)) ]



    def get(self, *oid):
        iter = self._get(oid)
        result = self._fetch_one(iter)
        return result.prettyPrint()

    def set(self, oid, value):
        iter = self._set(oid, value)
        result = self._fetch_one(iter)
        return result.prettyPrint()

    def next(self, *oidlist):
        iter = self._next(oidlist)
        results = self._fetch_all(iter)
        return [ result.prettyPrint() for result in results ]

    def walk(self, oidlist):
        iter = self._bulk(oidlist)
        results = self._fetch_all(iter)
        return [ result.prettyPrint() for result in results ]

