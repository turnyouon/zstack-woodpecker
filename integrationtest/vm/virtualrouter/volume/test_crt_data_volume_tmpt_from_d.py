'''

Create Volume Template from Data Volume

@author: Youyk
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import os

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()

def test():
    test_util.test_dsc('Create test vm and check')
    vm = test_stub.create_vlan_vm()
    test_obj_dict.add_vm(vm)

    test_util.test_dsc('Create volume and check')
    disk_offering = test_lib.lib_get_disk_offering_by_name(os.environ.get('smallDiskOfferingName'))
    volume_creation_option = test_util.VolumeOption()
    volume_creation_option.set_disk_offering_uuid(disk_offering.uuid)

    volume = test_stub.create_volume(volume_creation_option)
    test_obj_dict.add_volume(volume)

    test_util.test_dsc('Attach volume and check')
    #vm.check()
    volume.attach(vm)

    test_util.test_dsc('Detach volume and check')
    volume.detach()

    test_util.test_dsc('Create volume template and check')
    bs_list = test_lib.lib_get_backup_storage_list_by_vm(vm.get_vm())
    bs_uuid_list = []
    for bs in bs_list:
        bs_uuid_list.append(bs.uuid)
    vol_tmpt = volume.create_template(bs_uuid_list, 'new_data_template')
    test_obj_dict.add_image(vol_tmpt)
    vol_tmpt.check()
    volume.check()
    volume.delete()
    test_obj_dict.rm_volume(volume)

    test_util.test_dsc('Create volume from template and check')
    ps_uuid = vm.get_vm().allVolumes[0].primaryStorageUuid
    volume2 = vol_tmpt.create_data_volume(ps_uuid, 'new_volume_from_template')
    test_obj_dict.add_volume(volume2)
    vol_tmpt.delete()
    test_obj_dict.rm_image(vol_tmpt)

    volume2.check()
    volume2.attach(vm)
    vm.check()
    volume2.check()
    volume2.detach()
    volume2.delete()
    test_obj_dict.rm_volume(volume2)

    vm.destroy()
    test_util.test_pass('Create Data Volume Template from Data Volume Success')

#Will be called only if exception happens in test().
def error_cleanup():
    test_lib.lib_error_cleanup(test_obj_dict)
