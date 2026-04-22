from ansible_collections.opennebula.deploy.plugins.module_utils.main import to_one, recursive_stringify, diff_shared_keys

class FilterModule(object):
    def filters(self):
        return dict(
            to_one=to_one,
            recursive_stringify=recursive_stringify,
            diff_shared_keys=diff_shared_keys,
        )

