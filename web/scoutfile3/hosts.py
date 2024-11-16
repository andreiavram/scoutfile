from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'centru', 'scoutfile3.urls.wagtail_urls', name='centru'),
    host(r'knowledge', 'scoutfile3.urls.wagtail_urls', name='knowledge'),
    host(r'scoutfile', 'scoutfile3.urls.scoutfile', name='scoutfile'),
)
