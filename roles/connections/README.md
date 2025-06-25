Role: opennebula.deploy.connections
====================================

A role that manages bonds, vlans, and bridges

Requirements
------------

N/A

Role Variables
--------------

| Name                     | Type     | Default        | Example                            | Description                                   |
|--------------------------|----------|----------------|------------------------------------|-----------------------------------------------|
| `apply_network_change`  | `bool`   | `true`         | `apply_network_change: true`      | When set, will apply network changes if there are any. |
| `fail_on_netplan_change`  | `bool`   | `true`         | `fail_on_netplan_change: true`      | When set, will fail on any changes to any netplan config |
| `fail_on_nm_bond_change`    | `bool`   | `true`         | `fail_on_nm_bond_change: true`        | When set, will fail on any changes to bonds   |
| `fail_on_nm_ethernet_change`   | `bool`   | `true`         | `fail_on_nm_ethernet_change: true`       | When set, will fail on any changes to slaves  |
| `fail_on_nm_vlan_change`    | `bool`   | `true`         | `fail_on_nm_vlan_change: true`        | When set, will fail on any changes to vlans   |
| `fail_on_nm_bridge_change`  | `bool`   | `true`         | `fail_on_nm_bridge_change: true`      | When set, will fail on any changes to bridges |
| `bridge_change_override`  | `bool`   | `true`         | `bridge_change_override: true`      | When set, will not fail out on bridge change based on condition that no vms are running behind the bridge|
| `network_type`           | `str`    | `<os_default>` | `<netplan \| networkmanager>`      | Network type to use                           |
| `skip_network_node_role` | `str`    | `false`        | `true`                             | Determines to skip built in network node role to avoid conflict with this role |
| `netplan_config` | `dict`    | `{}`        | `{}`                             | Sets config for netplan, see below for details |
| `networkmanager_config` | `dict`    | `{}`        | `{}`                             | Sets config for networkmanager, see below for details |
| `dns_test_host`           | `str`    | `google.com` | `dns_test_host: example.com`      | Host to test against to verify dns is currently up |
| `dns_test_retries`         | `int`    | `12` |       | Number of retries to verify dns is working  |  
| `dns_test_delay`           | `str`    | `5` |       | Delay between each retry |  
Dependencies
------------

N/A

Reference
------------
```
netplan_config:
  update_type: <generate | apply> # Determines what type of update to do when there is an update.  Default: generate
  connections: # Dictionary on netplan settings where key is the name of the file that will be created/updated and value is dict of netplan settings
    <file_name> # Filename minus .yaml
      # Netplan settings content

networkmanager_config:
  bridges:
  bonds:
  vlans:
  ethernets:
    <file_name> # Filename/interface name minus .nmconnection

      # Networkmanager ini setting where outer key is section and the value is dict of key/value for section
      connection: # Section name of file
        # Key/values for section
        id: br0
        type: bridge
        uuid: cc785cac-dd31-4084-9e91-07d88913022b
        interface-name: br0
      
      # Another section
      ipv4:
        method: manual
        address1: 10.0.68.111/24,10.0.68.1
        dns: 10.0.81.11;10.0.81.12
```

Notes
------------
The `fail_on_nm_<connection_type>_change` and `fail_on_netplan_change` variables are used to block users from editing a `.nmconnection` and netplan `.yaml` respectively.  The reason for this is that when a user updates a nmcli or netplan connection, there can be weird side effects that cause things to go down, depending on what connection type was edited.  Example is if you edit a bridge connection, the vms connected to that bridge through their nics lose the `master` settings when viewing interface with `ip a` which causes all vms to lose connection.  In this case, you can bring it back up with `ip link set <vm_nic_name> master <bridge_name>` and waiting a few seconds for it to come up.  It seems that there are many edge cases for each connection type so it is up to the user to know if their changes will break things and to manually override the `fail_on_nm_<connection_type>_change` variables or override the `fail_on_netplan_change` if using netplan.

When it comes to `networkmanager_config`, user should set all values within section header as string, meaning if a value is purely a number, you must wrap it in quotes (ie. "1").  Reason for this is when we extract the file contents, it converts everything to string in the background. When we go to compare against current config settings, it compares string to int value, which is considered different and forces a restart of that connection type when nothing has changed and could cause temporary outages
License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
