from django.template import Library, Node
from django.utils.safestring import mark_safe
from django.core import urlresolvers
from django import forms

register = Library()

@register.simple_tag
def render_field(bound, label=None, single_input=False):
    # shortcut for hidden fields
#    if bound.is_hidden:
#        return '<li id="li_%(name)s" class="hidden">%(widget)s</li>' % {'name': bound.name, 'widget': bound}


    classes = ['control-group']
    if bound.errors:
        classes.append('error')
    # setup the required indicator
    if bound.field.required and bound.label:
        required_indicator =  '<span class="required-indicator" title="This Field is Required">*</span>'
    else:
        required_indicator =  '<span class="required-indicator">&nbsp;</span>'

    # setup the label
    if bound.label:
        if isinstance(bound.field.widget, forms.widgets.CheckboxInput):
            final_label = "%s%s" % ((label or bound.label), required_indicator)
        else:
            final_label = "%s:%s" % ((label or bound.label), required_indicator)
    else:
        final_label = ""

    # render the row
    ctx = {
        'name' : bound.name,
        'label': final_label,
        'classes': ' '.join(classes),
        'widget': bound,
        'error':bound.errors,
        }

    template='<div class="control-group %(classes)s"><label class="control-label" for="id_%(name)s">%(label)s</label><div class="controls">%(widget)s<span class="help-inline">%(error)s</span></div></div>'
    checkbox_template='<div class="control-group %(classes)s"><div class="controls"><label class="checkbox">%(widget)s%(label)s</label></div></div>'
    if isinstance(bound.field.widget, forms.widgets.CheckboxInput):
        return mark_safe(checkbox_template % ctx)

    return mark_safe(template % ctx)


@register.simple_tag
def render_form(form):
    #helper for determining visible fields
    def get_visible_inputs(form):
        visible_inputs = []
        for name, field in form.fields.items():
            if not isinstance(field.widget, field.hidden_widget):
                visible_inputs.append(field)
        return visible_inputs

    # helper for rendering a list of fields
    def get_fields_html(field_names, form, single_input):
        fields_html = []
        for field_name in field_names:
            if field_name in form.fields:
                fields_html.append(render_field(form[field_name], single_input=single_input))
        return ''.join(fields_html)

    errors = render_form_errors_helper(form)
    single_input = len(get_visible_inputs(form)) == 1
    legend = '' #TODO: implement later for form headings.

    # get the field list and remove the excluded fields
    field_names = form.fields.keys()
    return mark_safe('%s%s%s' % (errors, legend, get_fields_html(field_names, form, single_input)))


@register.simple_tag
def render_form_errors(form):
    return mark_safe(render_form_errors_helper(form))


def render_form_errors_helper(form):
    rendered_form_errors = ''
    error_base = "<div class=\"alert alert-error\">There were errors with your form submission. Please correct to continue. %s </div>"

    if hasattr(form, 'show_no_base_error'):
        rendered_form_errors = "<div class=\"error_notice_dialog\">%s</div>" % unicode(form.non_field_errors())
    elif form.non_field_errors():
        error_messages = unicode(form.non_field_errors())
        rendered_form_errors = error_base %  error_messages
    elif form.errors:
        rendered_form_errors = error_base % ""
    return rendered_form_errors
