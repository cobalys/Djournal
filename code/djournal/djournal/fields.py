from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import Widget, SelectMultiple, MultipleHiddenInput
from django.utils.encoding import force_text
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
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        print data
        print name
        return data.get(name, None)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ()
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        print list(self.choices)
        if value != '':
            final_attrs['value'] = ', '.join([v for k, v in self.choices if k in value])
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
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the'
                            ' available choices.'),
        'invalid_pk_value': _('"%(pk)s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset, cache_choices=None, required=True,
                 widget=None, label=None, initial=None,
                 help_text='', *args, **kwargs):
        super(TagsField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,
            *args, **kwargs)


    def clean(self, value):
        print "clean " + value
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        elif not self.required and not value:
            return self.queryset.none()
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'], code='list')
        print "clean check"
        qs = self._check_values(value)
        # Since this overrides the inherited ModelChoiceField.clean
        # we run custom validators here
        print "clean validators"
        self.run_validators(value)
        return qs


    def _check_values(self, value):
        """
        Given a list of possible PK values, returns a QuerySet of the
        corresponding objects. Raises a ValidationError if a given value is
        invalid (not a valid PK, not in the queryset, etc.)
        """
        print "_check_values " 
        key = 'name'
        tags_list = []
        if value.strip():
            tags = value.lower().split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if len(tag_name):
                    tag = Tag.objects.get_or_create(name=tag_name)
                    tags_list.append(tag)
        value = tags_list
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages['list'],
                code='list',
            )
        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
            except (ValueError, TypeError):
                raise ValidationError(
                    self.error_messages['invalid_pk_value'],
                    code='invalid_pk_value',
                    params={'pk': pk},
                )
        qs = self.queryset.filter(**{'%s__in' % key: value})
        pks = set(force_text(getattr(o, key)) for o in qs)
        for val in value:
            if force_text(val) not in pks:
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )
        print "_check_values " + qs
        return qs


    def to_python(self, value):
        print "to_python"
        if isinstance(value, list):
            return value

        if value is None:
            return value

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

