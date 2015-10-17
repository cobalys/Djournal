from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import Widget, SelectMultiple, MultipleHiddenInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django.forms.utils import flatatt
from djournal.models import Tag


class TagsWidget(Widget):
    input_type = "text"

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(TagsWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return getattr(data, 'name', None)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ()
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            final_attrs['value'] = ', '.join([v  for k, v in self.choices if k in value])
        choices_json = str([str(v) for k, v in self.choices])
        html_template = '''
                        <input%s />
                        <script type="text/javascript">
                            function split(val) {
                                return val.split(/,\s*/);
                            }
                            function extractLast(term) {
                                return split(term).pop();
                            }
                            jQuery(function() {
                                var availableTags = %s;
                                jQuery("#%s").bind("keydown", function(event){
                                    if(event.keyCode === jQuery.ui.keyCode.TAB && jQuery(this).data("autocomplete").menu.active) {
                                        event.preventDefault();
                                    }
                                }).autocomplete({
                                    minLength : 0,
                                    source : function(request, response) {
                                        response(jQuery.ui.autocomplete.filter(availableTags, extractLast(request.term)));
                                    },
                                    focus : function() {
                                        return false;
                                    },
                                    select : function(event, ui) {
                                        var terms = split(this.value);
                                        terms.pop();
                                        terms.push(ui.item.value);
                                        terms.push("");
                                        this.value = terms.join(", ");
                                        return false;
                                    }
                                    });
                                });
                        </script>
                        ''' % (flatatt(final_attrs), choices_json, final_attrs['id'])
        return  mark_safe(html_template)


class TagsField(ModelMultipleChoiceField):
    """A MultipleChoiceField whose choices are a model QuerySet."""
    widget = SelectMultiple
    hidden_widget = MultipleHiddenInput
    default_error_messages = {
        'list': _('Enter a list of values.'),
        'invalid_choice': _('Select a valid choice. %s is not one of the'
                            ' available choices.'),
        'invalid_pk_value': _('"%s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset, cache_choices=None, required=True,
                 widget=None, label=None, initial=None,
                 help_text='', *args, **kwargs):
        super(TagsField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,
            *args, **kwargs)


    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        elif not self.required and not value:
            return self.queryset.none()
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'], code='list')
        qs = self._check_values(value)
        # Since this overrides the inherited ModelChoiceField.clean
        # we run custom validators here
        self.run_validators(value)
        key = 'name'
        val = value.replace(', ', ',').split(',')
        qs = self.queryset.all().filter(**{'%s__in' % key: val})
        print "clean " + qs 
        return qs

    def to_python(self, value):
        tags_list = []
        if value.strip():
            tags = value.lower().split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if len(tag_name):
                    tag = Tag.objects.get_or_create(name=tag_name)
                    tags_list.append(tag)
        print "tags_list " + tags_list
        return tags_list


