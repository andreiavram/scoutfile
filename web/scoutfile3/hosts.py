from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'centru', 'scoutfile3.wagtail_urls', name='centru'),
    host(r'knowledge', 'scoutfile3.wagtail_urls', name='knowledge'),
    host(r'scoutfile', 'scoutfile3.urls', name='scoutfile'),
)
