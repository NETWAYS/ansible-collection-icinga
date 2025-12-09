def test_string(host):
    i2_file = host.file("/tmp/string")
    print(i2_file.content_string)
    assert i2_file.is_file
    assert i2_file.content_string == '\n[section]\ntest = "string"\n'

def test_number(host):
    i2_file = host.file("/tmp/number")
    print(i2_file.content_string)
    assert i2_file.is_file
    assert i2_file.content_string == '\n[section]\ntest = "10"\n'

def test_list(host):
    i2_file = host.file("/tmp/list")
    print(i2_file.content_string)
    assert i2_file.is_file
    assert i2_file.content_string == '\n[section]\ntest = "foo, bar, baz"\n'

def test_advanced_filter(host):
    i2_file = host.file("/tmp/advanced_filter")
    print(i2_file.content_string)
    assert i2_file.is_file
    assert i2_file.content_string == '\n[section]\ntest = "!(objectClass=user)"\ntest2 = "!(objectClass=user)"\ntest3 = "!attribute"\n'

def test_equal_sign(host):
    i2_file = host.file("/tmp/equal_sign")
    print(i2_file.content_string)
    assert i2_file.is_file
    assert i2_file.content_string == '\n[section]\ntest = "equal=sign"\n'
