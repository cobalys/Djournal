from django import template

register = template.Library()


@register.inclusion_tag('admin/djournal/entry/submit_line.html', takes_context=True)
def submit_row_entry(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    publish = context['publish']
    change = context['change']
    is_popup = context['is_popup']
    ctx = {
        'publish': publish,
        'change': change,
        'opts': opts,
        'show_delete_link': (not is_popup and context['has_delete_permission']
                             and change and context.get('show_delete', True)),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'preserved_filters': context.get('preserved_filters'),
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx
