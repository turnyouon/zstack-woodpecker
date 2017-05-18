'''

New Integration Test for Simple VM stop/start scheduler create.

@author: quarkonics
'''

import os
import time
import zstackwoodpecker.operations.vm_operations as vm_ops
import zstackwoodpecker.operations.scheduler_operations as schd_ops
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
test_stub = test_lib.lib_get_test_stub()
vm = None
schd = None

def test():
    global vm
    global schd
    vm = test_stub.create_vlan_vm(os.environ.get('l3VlanNetworkName1'))
    start_date = int(time.time())
    test_util.test_logger('Setup stop and start VM scheduler')
    schd = vm_ops.start_vm_scheduler(vm.get_vm().uuid, 'simple', 'simple_start_vm_scheduler', 0, 1)
    actual_startDate = time.mktime(time.strptime(schd.startTime, '%b %d, %Y %I:%M:%S %p'))
    if actual_startDate != start_date and actual_startDate != start_date + 1.0:
        test_util.test_fail('startDate is expectd to set to now, which should be around %s' % (start_date))
    test_stub.sleep_util(start_date+58)

    start_msg_mismatch = 0
    for i in range(1, 58):
        if not test_lib.lib_find_in_local_management_server_log(start_date+i, '[msg send]: {"org.zstack.header.vm.StartVmInstanceMsg', vm.get_vm().uuid):
            start_msg_mismatch += 1
            test_util.test_warn('StopVmInstanceMsg is expected to execute at %s' % (start_date+i))

    if start_msg_mismatch > 5:
        test_util.test_fail('%s of 58 StartVmInstanceMsg not executed at expected timestamp' % (start_msg_mismatch))

    schd_ops.delete_scheduler(schd.uuid)
    try:
        vm.destroy()
    except:
	test_util.test_logger('expected exception when destroy VM since too many queued task')
    test_util.test_pass('Create Simple VM Start Scheduler Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global vm
    global schd

    if vm:
        try:
            vm.destroy()
	except:
            test_util.test_logger('expected exception when destroy VM since too many queued task')

    if schd:
	schd_ops.delete_scheduler(schd.uuid)
