'''
@author: FangSun
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.vm_operations as vm_ops
import time

_config_ = {
        'timeout' : 1000,
        'noparallel' : True
        }

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()


def test():
    new_offering = test_lib.lib_create_instance_offering(cpuNum = 1,\
            cpuSpeed = 111, memorySize = 1024 * 1024 * 1024)
    test_obj_dict.add_instance_offering(new_offering)
    vm = test_stub.create_vm(vm_name = 'ckvmoffering-u12-64', image_name = "imageName_i_u12", instance_offering_uuid=new_offering.uuid)
    test_obj_dict.add_vm(vm)
    vm.check()

    (available_cpu_before, available_memory_before, vm_outer_cpu_before, vm_outer_mem_before,
     vm_interal_cpu_before, vm_interal_mem_before) = test_stub.check_cpu_mem(vm)

    vm_instance_offering = test_lib.lib_get_instance_offering_by_uuid(vm.get_vm().instanceOfferingUuid)
    MEMchange = 126*1024*1024
    AlignedMemChange = 128*1024*1024
    vm_ops.update_vm(vm.get_vm().uuid, vm_instance_offering.cpuNum + 1, vm_instance_offering.memorySize + MEMchange)
    vm.update()
    time.sleep(10)
    test_stub.online_hotplug_cpu_memory(vm)
    vm.check()

    (available_cpu_after, available_memory_after, vm_outer_cpu_after, vm_outer_mem_after,
     vm_interal_cpu_after, vm_internal_mem_after) = test_stub.check_cpu_mem(vm)

    assert available_cpu_before == available_cpu_after + 1
    assert available_memory_after + AlignedMemChange / int(test_lib.lib_get_provision_memory_rate()) in range(available_memory_before-1, available_memory_before+1)
    assert vm_outer_cpu_before == vm_outer_cpu_after - 1
    assert vm_outer_mem_before == vm_outer_mem_after - AlignedMemChange
    assert vm_interal_cpu_before == vm_interal_cpu_after - 1
    assert vm_interal_mem_before == vm_internal_mem_after - AlignedMemChange/1024/1024
    test_lib.lib_error_cleanup(test_obj_dict)
    test_util.test_pass('VM online change instance offering Test Pass')


def error_cleanup():
    test_lib.lib_error_cleanup(test_obj_dict)
