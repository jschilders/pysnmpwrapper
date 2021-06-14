import os
hostname = os.getenv('snmp_hostname')
community = os.getenv('snmp_community')



from pysnmpwrapper import SnmpWrapper

print('\n==> START of snmp test')
snmp = SnmpWrapper(hostname=hostname, community=community)

print('\n==> snmp GET - Test 1')
result = snmp.get('SNMPv2-MIB', 'sysUpTime', 0)
print(result)

print('\n==> snmp GET - Test 2')
result = snmp.get(['SNMPv2-MIB', 'sysDescr', 0])
print(result)

print('\n==> snmp GET - Test 3')
results = snmp.next(('IF-MIB', 'ifInOctets'), ('IF-MIB', 'ifOutOctets'))
for result in results:
    print(result)

print('\n==> snmp NEXT - Test 1')
oidlist = [
    ('IF-MIB', 'ifInOctets'),
    ('IF-MIB', 'ifOutOctets')
]
results = snmp.next(oidlist)
for result in results:
    print(result)

print('\n==> snmp NEXT - Test 2')
results = snmp.next(*oidlist)
for result in results:
    print(result)

print('\n==> snmp NEXT - Test 3')
results = snmp.next('1.3.6.1.2.1.1.1')
for result in results:
    print(result)

print('\n==> snmp BULK - Test 1')
oid = ('IF-MIB', 'ifTable')
results = snmp.walk(oid)
for result in results:
    print(result)

print('\n==> snmp BULK - Test 2')
results = snmp.walk('SNMPv2-MIB')
for result in results:
    print(result)

print('\n==> END of tests')


