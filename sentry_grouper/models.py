"""
sentry_grouper.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import sentry_grouper
import pickle
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.formsets import formset_factory
from sentry.plugins import Plugin, register

RULES_DATA_KEY = '__data'

class GroupRuleForm(forms.Form):
    groups = {
        'Group name': ['group_name'],
        'Match condition (regex)': ['logger', 'culprit', 'message']
    }

    group_name = forms.CharField(max_length=255)
    logger = forms.CharField(max_length=255, required=False)
    culprit = forms.CharField(max_length=255, required=False)
    message = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(GroupRuleForm, self).__init__(*args, **kwargs)
        for group, fields in self.groups.iteritems():
            for field_name in fields:
                field = self.fields[field_name]
                field.widget.attrs['group_name'] = group

    def clean(self):
        cleaned_data = super(GroupRuleForm, self).clean()
        logger = cleaned_data.get("logger")
        culprit = cleaned_data.get("culprit")
        message = cleaned_data.get("message")
        if not any((logger,culprit,message)):
            raise forms.ValidationError(_("At least one condition field must be filled in"))
        return cleaned_data

GroupRuleFormSet = formset_factory(GroupRuleForm, extra=1, can_delete=True)

class PatchedGroupRuleFormSet(GroupRuleFormSet):
    """
    Hacked FormSet that mimics a single field form, it pickles every form
    cleaned_data and takes care of the unpickling (it expects __init__ initial
    parameter to be empty or the [cleaned_data] pickle)

    """
    base_fields = [RULES_DATA_KEY]

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {}).get(RULES_DATA_KEY)
        if initial:
            kwargs['initial'] = pickle.loads(initial)
        super(PatchedGroupRuleFormSet, self).__init__(*args, **kwargs)

    @property
    def cleaned_data(self):
        data = getattr(super(PatchedGroupRuleFormSet, self), 'cleaned_data', {})
        return {RULES_DATA_KEY: pickle.dumps(data)}

class GrouperPlugin(Plugin):
    slug = 'group_rules'
    conf_key = 'group_rules'
    conf_key_rules = RULES_DATA_KEY
    title = _('Grouping Rules')
    version = sentry_grouper.VERSION
    author = "Tommaso Barbugli"
    author_url = "https://github.com/tbarbugli/sentry_grouper"
    project_conf_template = 'sentry/plugins/sentry_grouper/project_configuration.html'
    project_conf_form = PatchedGroupRuleFormSet

    def get_project_rules(self, project):
        rules = self.get_option(RULES_DATA_KEY, project)
        unpickled = rules and pickle.loads(rules) or {RULES_DATA_KEY: []}
        return unpickled

register(GrouperPlugin)
