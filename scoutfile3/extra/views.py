# Create your views here.
from django.views.generic.base import TemplateView

class EnciclopedieEntry(object):
    timestamp = None
    categoriecuriozitate = None
    aprobat = None
    numesiprenume = None
    sursadeinformare = None
    curiozitate = None

class EnciclopedieEntries(TemplateView):
    template_name = "extra/enciclopedie.html"
    
    def get_context_data(self, **kwargs):
        username = 'andrei.avram@gmail.com'
        passwd = 'yetiRulz1_'
        doc_name = 'adaugare curiozitate enciclopedie (Responses)'
        
        import gdata.docs
        import gdata.docs.service
        import gdata.spreadsheet.service
        
        # Connect to Google
        gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gd_client.email = username
        gd_client.password = passwd
        gd_client.source = 'scoutfile.albascout.ro'
        gd_client.ProgrammaticLogin()
        
        q = gdata.spreadsheet.service.DocumentQuery()
        q['title'] = doc_name
        q['title-exact'] = 'true'
        feed = gd_client.GetSpreadsheetsFeed(query=q)
        spreadsheet_id = feed.entry[0].id.text.rsplit('/', 1)[1]
        feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
        worksheet_id = feed.entry[0].id.text.rsplit('/', 1)[1]
        
        rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
        
        entries = []
        for row in rows:
            entry = EnciclopedieEntry()
            for key in row.custom:
                print " %s: %s" % (key, row.custom[key].text)
                setattr(entry, key, row.custom[key].text)
            entries.append(entry)
            
        
        return {"entries" : entries}