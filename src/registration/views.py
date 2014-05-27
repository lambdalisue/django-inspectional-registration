# coding=utf-8
"""
Class based views for django-inspectional-registration
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.text import ugettext_lazy as _

from registration.backends import get_backend
from registration.models import RegistrationProfile


class RegistrationCompleteView(TemplateView):
    """A simple template view for registration complete"""
    template_name = r'registration/registration_complete.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationCompleteView,
                        self).get_context_data(**kwargs)
        # get registration_profile instance from the session
        if 'registration_profile_pk' in self.request.session:
            profile_pk = self.request.session.pop('registration_profile_pk')
            profile = RegistrationProfile.objects.get(pk=profile_pk)
        else:
            profile = None
        context['registration_profile'] = profile
        return context


class RegistrationClosedView(TemplateView):
    """A simple template view for registraion closed

    This view is called when user accessed to RegistrationView
    with REGISTRATION_OPEN = False
    """
    template_name = r'registration/registration_closed.html'


class ActivationCompleteView(TemplateView):
    """A simple template view for activation complete"""
    template_name = r'registration/activation_complete.html'


class ActivationView(TemplateResponseMixin, FormMixin,
                     SingleObjectMixin, ProcessFormView):
    """A complex view for activation

    GET:
        Display an ActivationForm which has ``password1`` and ``password2``
        for activation user who has ``activation_key``
        ``password1`` and ``password2`` should be equal to prepend typo

    POST:
        Activate the user who has ``activation_key`` with passed ``password1``
    """
    template_name = r'registration/activation_form.html'
    model = RegistrationProfile

    def __init__(self, *args, **kwargs):
        self.backend = get_backend()
        super(ActivationView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """get ``RegistrationProfile`` queryset which status is 'accepted'"""
        return self.model.objects.filter(_status='accepted')

    def get_object(self, queryset=None):
        """get ``RegistrationProfile`` instance by ``activation_key``
        
        ``activation_key`` should be passed by URL
        """
        queryset = queryset or self.get_queryset()
        try:
            obj = queryset.get(activation_key=self.kwargs['activation_key'])
            if obj.activation_key_expired():
                raise Http404(_('Activation key has expired'))
        except self.model.DoesNotExist:
            raise Http404(_('An invalid activation key has passed'))
        return obj

    def get_success_url(self):
        """get activation complete url via backend"""
        return self.backend.get_activation_complete_url(self.activated_user)

    def get_form_class(self):
        """get activation form class via backend"""
        return self.backend.get_activation_form_class()

    def form_valid(self, form):
        """activate user who has ``activation_key`` with ``password1``
        
        this method is called when form validation has successed.
        """
        profile = self.get_object()
        password = form.cleaned_data['password1']
        self.activated_user = self.backend.activate(
            profile.activation_key, self.request, password=password)
        return super(ActivationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        # self.object have to be set
        self.object = self.get_object()
        return super(ActivationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # self.object have to be set
        self.object = self.get_object()
        return super(ActivationView, self).post(request, *args, **kwargs)


class RegistrationView(FormMixin, TemplateResponseMixin, ProcessFormView):
    """A complex view for registration

    GET:
        Display an RegistrationForm which has ``username``, ``email1`` and ``email2``
        for registration.
        ``email1`` and ``email2`` should be equal to prepend typo.

        ``form`` and ``supplement_form`` is in context to display these form.

    POST:
        Register the user with passed ``username`` and ``email1``
    """
    template_name = r'registration/registration_form.html'

    def __init__(self, *args, **kwargs):
        self.backend = get_backend()
        super(RegistrationView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        """get registration complete url via backend"""
        return self.backend.get_registration_complete_url(self.new_user)

    def get_disallowed_url(self):
        """get registration closed url via backend"""
        return self.backend.get_registration_closed_url()

    def get_form_class(self):
        """get registration form class via backend"""
        return self.backend.get_registration_form_class()

    def get_supplement_form_class(self):
        """get registration supplement form class via backend"""
        return self.backend.get_supplement_form_class()
    
    def get_supplement_form(self, supplement_form_class):
        """get registration supplement form instance"""
        if not supplement_form_class:
            return None
        return supplement_form_class(**self.get_form_kwargs())

    def form_valid(self, form, supplement_form=None):
        """register user with ``username`` and ``email1``
        
        this method is called when form validation has successed.
        """
        username = form.cleaned_data['username']
        email = form.cleaned_data['email1']
        self.new_user = self.backend.register(username, email, self.request)
        profile = self.new_user.registration_profile
        if supplement_form:
            supplement = supplement_form.save(commit=False)
            supplement.registration_profile = profile
            supplement.save()
        # save the profile on the session so that the RegistrationCompleteView
        # can refer the profile instance.
        # this instance is automatically removed when the user accessed
        # RegistrationCompleteView
        self.request.session['registration_profile_pk'] = profile.pk
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form, supplement_form=None):
        context = self.get_context_data(
                form=form, supplement_form=supplement_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        supplement_form_class = self.get_supplement_form_class()
        supplement_form = self.get_supplement_form(supplement_form_class)
        context = self.get_context_data(
                form=form, supplement_form=supplement_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        supplement_form_class = self.get_supplement_form_class()
        supplement_form = self.get_supplement_form(supplement_form_class)
        if form.is_valid() and (not supplement_form or supplement_form.is_valid()):
            return self.form_valid(form, supplement_form)
        else:
            return self.form_invalid(form, supplement_form)


    def dispatch(self, request, *args, **kwargs):
        if not self.backend.registration_allowed():
            # registraion has closed
            return redirect(self.get_disallowed_url())
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)
