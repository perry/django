import os

from django.forms.renderers import (
    DjangoTemplateRenderer, Jinja2TemplateRenderer, ProjectTemplateRenderer,
)
from django.forms.widgets import Input
from django.test import SimpleTestCase, modify_settings
from django.utils._os import upath


class SharedTests(object):

    def test_installed_apps_template_found(self):
        """Can find a custom template in INSTALLED_APPS."""
        renderer = self.renderer()
        # Found because forms_tests is .
        tpl = renderer.get_template('forms_tests/custom_widget.html')
        expected_path = os.path.abspath(
            os.path.join(
                upath(os.path.dirname(__file__)),
                '..',
                getattr(self, 'expected_widget_dir', 'templates') + '/forms_tests/custom_widget.html',
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)

    @modify_settings(INSTALLED_APPS={'append': 'forms_tests.extra_templates_app'})
    def test_override_builtin_template(self):
        renderer = self.renderer()
        tpl = renderer.get_template(Input.template_name)
        widget_dir = getattr(self, 'expected_widget_dir', 'templates')
        expected_path = os.path.abspath(
            os.path.join(
                upath(os.path.dirname(__file__)),
                '..',
                'extra_templates_app/' + widget_dir + '/django/forms/widgets/input.html',
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)


class DjangoTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = DjangoTemplateRenderer


class Jinja2TemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = Jinja2TemplateRenderer
    expected_widget_dir = 'jinja2'


class ProjectTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = ProjectTemplateRenderer
