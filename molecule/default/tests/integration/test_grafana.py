def test_grafana_module(host):
    module_package = host.package("icinga-grafana")
    module_dir = host.file("/usr/share/icingaweb2/modules/grafana")
    enabled_module = host.file("/etc/icingaweb2/enabledModules/grafana")
    config = host.file("/etc/icingaweb2/modules/grafana/config.ini")
    graphs = host.file("/etc/icingaweb2/modules/grafana/graphs.ini")

    assert module_package.is_installed
    assert module_dir.is_directory
    assert enabled_module.linked_to == "/usr/share/icingaweb2/modules/grafana"

    assert config.is_file
    assert config.contains("[grafana]")
    assert config.contains('host = "grafana.example.org:3000"')
    assert config.contains('protocol = "https"')
    assert config.contains('datasource = "influxdb"')
    assert config.contains('accessmode = "iframe"')
    assert config.contains('defaultdashboard = "icinga2-default"')
    assert config.contains('defaultdashboarduid = "ad5bxjg"')

    assert graphs.is_file
    assert graphs.contains("[load]")
    assert graphs.contains('dashboarduid = "ad5pjfp"')
    assert graphs.contains('panelId = "1,2,3"')
