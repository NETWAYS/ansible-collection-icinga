def test_icingaweb2_module_fileshipper(host):
    import textwrap

    # imports.ini
    imports_conf = host.file('/etc/icingaweb2/modules/fileshipper/imports.ini')
    print(imports_conf.content_string)
    assert imports_conf.is_file
    assert imports_conf.content_string == textwrap.dedent('''
        [a_bunch_of_files]
        basedir = "bunch"

        [a_bunch_of_files_no_purge]
        basedir = "bunch_no_purge"
    ''')
    if host.system_info.distribution == 'centos':
      assert imports_conf.user == 'apache'
      assert imports_conf.group == 'icingaweb2'
      assert imports_conf.mode == 0o660
    if host.system_info.distribution == 'debian':
      assert imports_conf.user == 'www-data'
      assert imports_conf.group == 'icingaweb2'
      assert imports_conf.mode == 0o660


    # directories.ini
    directories_conf = host.file('/etc/icingaweb2/modules/fileshipper/directories.ini')
    print(directories_conf.content_string)
    assert directories_conf.is_file
    assert directories_conf.content_string == textwrap.dedent('''
        [custom_rules]
        source = "custom_rules"
        target = "zones.d/director-global/custom_rules"
        extensions = ".conf"

        [custom_rules_no_purge]
        source = "custom_rules_no_purge"
        target = "zones.d/director-global/custom_rules"
        extensions = ".conf"
    ''')

    if host.system_info.distribution == 'centos':
      assert directories_conf.user == 'apache'
      assert directories_conf.group == 'icingaweb2'
      assert directories_conf.mode == 0o660
    if host.system_info.distribution == 'debian':
      assert directories_conf.user == 'www-data'
      assert directories_conf.group == 'icingaweb2'
      assert directories_conf.mode == 0o660

    # Deployed files
    for file in [
        '/var/tmp/icingaweb/fileshipper/imports/bunch/file_01.yml',
        '/var/tmp/icingaweb/fileshipper/imports/bunch/file_02.yml',
        '/var/tmp/icingaweb/fileshipper/imports/bunch_no_purge/file_01.yml',
        '/var/tmp/icingaweb/fileshipper/imports/bunch_no_purge/file_02.yml',
        '/var/tmp/icingaweb/fileshipper/directories/custom_rules/file_03.conf',
        '/var/tmp/icingaweb/fileshipper/directories/custom_rules/file_04.conf',
        '/var/tmp/icingaweb/fileshipper/directories/custom_rules_no_purge/file_03.conf',
        '/var/tmp/icingaweb/fileshipper/directories/custom_rules_no_purge/file_04.conf',
    ]:
        assert host.file(file).is_file

