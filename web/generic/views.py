#coding: utf-8
import datetime
import json
import logging
import traceback
import urllib
import urllib2

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, FormView
from goodies.forms import CrispyBaseDeleteForm

from generic.forms import LoginForm, IssueCreateForm
from utils.views import FacebookLoginView

logger = logging.getLogger(__file__)


class GenericDeleteView(DeleteView):
    template_name = "generic/delete_form.html"
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, u"Obiectul a fost șters")
        return super(GenericDeleteView, self).delete(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        current = super(GenericDeleteView, self).get_context_data(**kwargs)
        current.update({"form" : CrispyBaseDeleteForm(instance = self.object)})
        return current
    
class Login(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    
    def dispatch(self, request, *args, **kwargs):
        #    daca utilizatorul este deja autentificat, redirecteaza catre pagina lui
        #    astfel se poate folosi view-ul pentru un dispatch-er pentru utilizatori
        if request.user.is_authenticated() and "err" not in request.GET:
            return HttpResponseRedirect(request.user.utilizator.membru.get_home_link())
        
        return super(Login, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        login(self.request, user)
        messages.success(self.request, "User și parolă corecte, bine ai venit!")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return self.request.user.utilizator.membru.get_home_link()

    def get_context_data(self, **kwargs):
        data = super(Login, self).get_context_data(**kwargs)
        data['facebook_connect_url'] = FacebookLoginView.get_facebook_endpoint(self.request)
        return data
    
class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, u"Sesiunea a fost terminată. Utilizatorul tău nu mai este conectat.")
        return HttpResponseRedirect(reverse("index"))


class IndexView(TemplateView):
    template_name = "home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        response = self.loggedin_dispatcher(request)
        if response:
            return response
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def loggedin_dispatcher(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(request.user.utilizator.membru.get_home_link())
        return None

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data(**kwargs)

        values = {"project_id" : 1,
                  "status_id" : "closed",
                  "limit" : 10,
                  "key" : settings.REDMINE_API_KEY}

        data = urllib.urlencode(values)
        url_to_send = "http://yeti.albascout.ro/redmine/issues.json" + "?" + data + "&sort=updated_on:desc"
        logger.debug(url_to_send)

        json_object = None
        try:
            response = urllib2.urlopen(url_to_send)
            json_object = json.loads(response.read())
        except Exception, e:
            logger.error("%s: eroare la obtinerea bug-urilor: %s" % (self.__class__.__name__, e))

        if json_object:
            for issue in json_object["issues"]:
                issue["updated_on"] = datetime.datetime.strptime(issue["updated_on"], "%Y-%m-%dT%H:%M:%SZ")

            context_data.update({"issues" : json_object})
        return context_data
    
class Issues(TemplateView):
    template_name = "issues.html"    
    
    def dispatch(self, request, *args, **kwargs):
        self.status = "closed"
        if "status" in request.GET and request.GET['status'] in ("*", "open", "closed"):
            self.status = request.GET['status']
            
        self.tracker = None
        if "tracker" in request.GET and request.GET['tracker'] in ("1", "2"):
            self.tracker = request.GET['tracker']
        
        return TemplateView.dispatch(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context_data = super(Issues, self).get_context_data(**kwargs)
        
        values = {"project_id" : 1,
                  "status_id" : self.status,
                  "limit" : 50,
                  "key" : settings.REDMINE_API_KEY}
        
        if self.tracker:
            values.update({"tracker_id" : self.tracker})
        
        data = urllib.urlencode(values)
        url_to_send = "http://yeti.albascout.ro/redmine/issues.json" + "?" + data + "&sort=updated_on:desc"
        logger.debug(url_to_send)
        try:
            response = urllib2.urlopen(url_to_send)
            json_object = json.loads(response.read())
        except Exception, e:
            logger.error("%s: eroare la obtinerea bug-urilor: %s" % (self.__class__.__name__, e))
        
        
        for issue in json_object["issues"]:
            issue["updated_on"] = datetime.datetime.strptime(issue["updated_on"], "%Y-%m-%dT%H:%M:%SZ")
        
        context_data.update({"issues" : json_object})
        return context_data

class CreateIssue(FormView):
    form_class = IssueCreateForm
    template_name = "generic/issue_create_form.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super(CreateIssue, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # titlu, aplicatie, descriere, user
        post_data = {"issue" : { "project_id" : 1, 
                     "subject" : form.cleaned_data['subject'], 
                     "status_id" : 1, 
                     "tracker_id" : 3 }}
        
        if form.cleaned_data['category']:
            post_data["issue"]["category_id"] = form.cleaned_data['category']
            
        if form.cleaned_data['description']:
            post_data["issue"]["description"] =  form.cleaned_data['description']
        else:
            post_data['issue']['description'] = ""
            
        if self.request.user.is_authenticated():
            post_data["issue"]["description"] = "(%s) %s" % (self.request.user.username, post_data['issue']['description'])
        
        data = json.dumps(post_data)
        logger.debug("%s: %s" % (self.__class__.__name__, data))
        
        url_to_send = 'http://yeti.albascout.ro/redmine/issues.json?key=%s' % settings.REDMINE_API_KEY
        try:
            req = urllib2.Request(url_to_send, data, {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            #response = f.read()
            f.close()
        except Exception, e:
            logger.error("%s: eroare la adaugarea unui bug nou: %s : %s" % (self.__class__.__name__, e, traceback.format_exc()))
        
        messages.success(self.request, u"Problema a fost înregistrată, și va apărea în această pagină când va fi preluată pentru rezolvare")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("issues")


class ScoutFileAjaxException(Exception):
    def __init__(self, *args, **kwargs):
        self.original_exception = kwargs.get('exception', None)
        self.extra_message = kwargs.get("extra_message", None)
    
    def to_response(self):
        json_dict = {"original_exception" : "%s" % self.original_exception, "extra_message" : "%s" % self.extra_message}
        return HttpResponse(json.dumps(json_dict), status = 500, content_type = "text/json")
    
    @classmethod
    def validation_compose(self, missing = {}, errors = {}, call = ""):
        return ScoutFileAjaxException(extra_message = "%s: Validation error, missing required params: %s, params that errored out %s" % (call, missing, errors))
        
    @classmethod
    def generic_response(cls, e, stack_trace):
        json_dict = {"status" : "error", "exception" : "%s" % e, "trace" : "%s" % stack_trace}
        return HttpResponse(json.dumps(json_dict), status = 500, content_type = "text/json")
    
    def __unicode__(self):
        return "Error: $s, %s" % (self.original_exception, self.extra_message)

class JSONView(View):
    """ Generic abstract view for API calls
    """
    _params = {}
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(JSONView, self).dispatch(request, *args, **kwargs)
        except ScoutFileAjaxException, e:
            return e.to_response()
        except Exception, e:
            return ScoutFileAjaxException.generic_response(e, traceback.format_exc())
    
    @property
    def params(self):
        return self._params
    
    def parse_json_data(self):
        try:
            json_dict = json.loads(self.request.body)
        except ValueError, e:
            json_dict = self.request.body.dict()
        except Exception, e:
            json_dict = {}
        
        return json_dict
       
    def validate(self, use_global_kwargs = True, **kwargs):
        error_dict = {}
        error_dict['missing'] = []
        error_dict['error'] = []
        
        if use_global_kwargs:
            kwargs.update(self.kwargs)
        
        self.cleaned_data = {}
        #   checking and cleaning required params
        for param in self.params:
            if not kwargs.has_key(param):
                if self.params.get(param).get("type", "optional") == "required":
                    error_dict['missing'].append(param)
                continue
            
            validator = getattr(self, "clean_%s" % param, self.default_cleaner)
            try:
                # ISSUE on len(INT) 
                #if self.params.get(param).get("type", "optional") == "optional" and len(kwargs.get(param, "")) == 0:
                if self.params.get(param).get("type", "optional") == "optional" and (kwargs.get(param) in ['', None]):
                    continue
                self.cleaned_data[param] = validator(kwargs.get(param))
            except ScoutFileAjaxException, e:
                error_dict['error'].append((param, e))
                
        if len(error_dict['missing']) + len(error_dict['error']):
            raise ScoutFileAjaxException.validation_compose(missing = error_dict['missing'], 
                                                          errors = error_dict['error'], call = self.__class__.__name__)
        
    def default_cleaner(self, value):
        """ This is the default cleaner, by default it simply returns the value as
        it got it """ 
        return value
    
    def construct_json_response(self, **kwargs):
        json_dict = {}
        return json.dumps(json_dict)


def custom_500(request, template_name="500.html"):
    return render_to_response(template_name, {"exception_str": traceback.format_exc()}, context_instance = RequestContext(request))