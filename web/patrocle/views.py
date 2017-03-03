# coding: utf-8
import datetime
import logging

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView

from patrocle import SMSMessage, Credit
from patrocle import SendSMSForm, AsociereCreditForm

logger = logging.getLogger(__name__)

class SendSMS(FormView):
    form_class = SendSMSForm
    template_name = "patrocle/send_form.html"
    
    @method_decorator(user_passes_test(lambda u : u.utilizator.membru.is_lider() or u.utilizator.membru.is_membru_ccl()))
    def dispatch(self, request, *args, **kwargs):
        self.destinatar = None
        if "destinatar" in request.GET and request.GET['destinatar']:
            self.destinatar = request.GET['destinatar']
        return super(SendSMS, self).dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(SendSMS, self).get_initial()
        if self.destinatar:
            initial.update({"telefon" : self.destinatar})
            
        return initial
    
    def get_form_kwargs(self):
        data = super(SendSMS, self).get_form_kwargs()
        data.update({"request" : self.request})
        return data
    
    def form_valid(self, form):
#         if DEBUG:
#             messages.warning(self.request, u"Suntem în modul DEBUG, nu trimit niciun mesaj!")
#             return HttpResponseRedirect(reverse("patrocle:home"))

        import hashlib
        grup_id = None
        if len(form.cleaned_data['destinatari']) > 1:
            grup_id = "%d-%s" % (self.request.user.utilizator.id, hashlib.md5("%s" % datetime.datetime.now()).hexdigest())
            
            
        for d in form.cleaned_data['destinatari']:
            try:
                SMSMessage.send_message("sms",
                                        expeditor = self.request.user.utilizator,
                                        destinatar = d[0], 
                                        mesaj_text = "P: %s" % form.cleaned_data["mesaj"],
                                        credit = d[1][0].elibereaza_credit(),
                                        grup_id = grup_id)            
            except Exception, e:
                d[1][0].elibereaza_credit()
                messages.error(self.request, e)
                return HttpResponseRedirect(reverse("patrocle:send_sms"))
        messages.success(self.request, u"Mesajul a fost trimis!")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("patrocle:home")
    
    
class ConfirmSMS(View):
    def get(self, request, *args, **kwargs):
        try:
            mesaj = SMSMessage.objects.get(cod_referinta_smslink = int(request.GET['message_id']))
        except SMSMessage.DoesNotExist:
            logger.error("%s: Am primit o confirmare pentru un mesaj care nu exista (%s)" % (self.__class__.__name__, request.GET['message_id']))
        except Exception, e:
            logger.error("%s: Eroare la obtinerea mesajului de confirmare: %s" % (self.__class__.__name__, e))
        
        if (request.GET['status'] == "1"):
            mesaj.confirmat = True
        else:
            mesaj.eroare_confirmare = request.GET['status'] 
        
        mesaj.timestamp_confirmare = datetime.datetime.fromtimestamp(int(request.GET['timestamp']))
        mesaj.save()
        
        return HttpResponse("OK")
        
class ListConfirmations(ListView):
    template_name = "patrocle/list_confirms.html"
    model = SMSMessage
    
    def get_queryset(self):
        return super(ListConfirmations, self).get_queryset().filter(expeditor = self.request.user.utilizator).order_by("confirmat", "-timestamp_trimitere")
    
class ListGrupConfirmations(ListView):
    template_name = "patrocle/list_grup_confirms.html"
    model = SMSMessage
    
    def get_queryset(self):
        filter_kwargs = { 'expeditor' : self.request.user.utilizator,
                          'cod_grup' : self.kwargs.get('cod') } 
        
        qs = super(ListGrupConfirmations, self).get_queryset().filter(**filter_kwargs)
        qs = qs.order_by("confirmat", "-timestamp_trimitere")
        return qs
    
class PatrocleStats(TemplateView):
    template_name = "patrocle/system_stats.html"
    
    @method_decorator(user_passes_test(lambda x : x.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(PatrocleStats, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super(PatrocleStats, self).get_context_data(**kwargs)
        data.update({"current_credit" : Credit.get_system_credit(), 
                     "total_transmise" : SMSMessage.objects.filter(confirmat = True, eroare_confirmare__isnull = True)})
        
        return data
    
class AsociazaCredit(CreateView):
    template_name = "patrocle/asociaza_credit_form.html"
    form_class = AsociereCreditForm
    model = Credit
    
    @method_decorator(user_passes_test(lambda x : x.is_staff))
    def dispatch(self, request, *args, **kwargs):
        self.get_credit_status()
        return super(AsociazaCredit, self).dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        data = super(AsociazaCredit, self).get_form_kwargs()
        data.update({"credit_maxim" : self.credit_sistem_nealocat})
        return data
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.creat_de = self.request.user.utilizator
        self.object.tip = 2
        self.object.save()
        
        messages.success(self.request, u"Asocierea a fost salvată. %s SMS-uri au fost adăugate contului selctat" % self.object.credit)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("patrocle:credit_lista")

    def get_credit_status(self):
        self.credit_curent_sistem = Credit.get_system_credit()
        credit_total_liber = 0
        credite_active = Credit.objects.filter(epuizat = False, content_type__isnull = False, tip = 2)
        for credit in credite_active:
            credit_total_liber += credit.credit_ramas()
        self.credit_sistem_nealocat = self.credit_curent_sistem - credit_total_liber        

    
    def get_context_data(self, **kwargs):
        data = super(AsociazaCredit, self).get_context_data(**kwargs)
        
        data.update({"credit_curent_sistem" : self.credit_curent_sistem, 
                     "credit_sistem_nealocat" : self.credit_sistem_nealocat})
        return data
        
class ListaCredite(ListView):
    template_name = "patrocle/lista_credite.html"
    model = Credit
    
    @method_decorator(user_passes_test(lambda x : x.is_staff))
    def dispatch(self, request, *args, **kwargs):
        self.tip = 2
        if "tip" in request.GET and request.GET['tip']:
            self.tip = int(request.GET['tip'])
        self.get_credit_status()
        return super(ListaCredite, self).dispatch(request, *args, **kwargs)
    
    def get_credit_status(self):
        self.credit_curent_sistem = Credit.get_system_credit()
        credit_total_liber = 0
        credite_active = Credit.objects.filter(epuizat = False, content_type__isnull = False, tip = 2)
        for credit in credite_active:
            credit_total_liber += credit.credit_ramas()
        self.credit_sistem_nealocat = self.credit_curent_sistem - credit_total_liber        
    
    def get_queryset(self):
        qs = super(ListaCredite, self).get_queryset().filter(tip = self.tip, content_type__isnull = False)
        qs = qs.order_by("-timestamp")
        return qs

    def get_context_data(self, **kwargs):
        data = super(ListaCredite, self).get_context_data(**kwargs)
                    
        data.update({"credit_curent_sistem" : self.credit_curent_sistem, 
                     "credit_sistem_nealocat" : self.credit_sistem_nealocat})
        return data
        