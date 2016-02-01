from f5.common import iapp_parser as ip

import pytest


good_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

no_open_brace_templ = '''sys application template no_open_brace_templ {
  actions {
    definition {
      html-help
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

no_close_brace_templ = '''sys application template no_close_brace_template {
  actions {
    definition {
      html-help {
        # HTML Help for the template
        # Missing closing braces
      implementation {
        # TMSH implementation code
      '''

no_pres_templ = '''sys application template no_pres_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

no_name_templ = '''sys application template  {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

bad_name_templ = '''sys application template bad><{\#updown {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

good_attr_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {}
      implementation {}
      presentation {}
    }
  }
  description <template description>
  partition just_a_partition name
}'''

good_templ_dict = {
    'name': 'good_templ',
    'html-help': '# HTML Help for the template',
    'description': '<template description>',
    'role-acl': '',
    'implementation': '# TMSH implementation code',
    'partition': '<partition name>',
    'presentation': '# APL presentation language'
}


def test__init__():
    prsr = ip.IappParser(good_templ)
    assert prsr.template_str == good_templ


def test__init__error():
    prsr = None
    with pytest.raises(ip.EmptyTemplateException):
        prsr = ip.IappParser(u'')
    assert prsr is None


def test_get_section_end():
    prsr = ip.IappParser(good_templ)
    impl_start = prsr.get_section_start(u'implementation')
    impl_end = prsr.get_section_end(u'implementation', impl_start)
    templ_impl = unicode('''{
        # TMSH implementation code
      }''')
    assert good_templ[impl_start:impl_end+1] == templ_impl


def test_get_section_start_no_open_brace_error():
    prsr = ip.IappParser(no_open_brace_templ)
    with pytest.raises(ip.NonextantSectionException):
        prsr.get_section_start(u'html-help')


def test_get_section_end_no_close_brace_error():
    prsr = ip.IappParser(no_close_brace_templ)
    with pytest.raises(ip.CurlyBraceMismatchException):
        help_start = prsr.get_section_start(u'html-help')
        prsr.get_section_end(u'html_help', help_start)


def test_get_template_name():
    prsr = ip.IappParser(good_templ)
    assert prsr.get_template_name() == u'good_templ'


def test_get_template_name_error():
    prsr = ip.IappParser(no_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException):
        prsr.get_template_name()


def test_get_template_name_bad_name_error():
    prsr = ip.IappParser(bad_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException):
        prsr.get_template_name()


def test_parse_template():
    prsr = ip.IappParser(good_templ)
    assert prsr.parse_template() == good_templ_dict


def test_get_template_attr():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr.get_template_attr(u'partition')
    assert attr == u'just_a_partition name'


def test_get_template_attr_attr_not_exists():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr.get_template_attr(u'bad_attr')
    assert attr is None
