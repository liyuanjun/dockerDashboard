from django.conf.urls import patterns, include, url
from django.contrib import admin
from dockerDashboard.settings import STATICFILES_DIRS

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       )
urlpatterns += patterns('',
                        url(r'', include('dockerDashboard.web.urls')),
                        )

# 1.For close debug mode, configure static file access,
#
# 2.Another method is to run the service, add the "--insecure" parameter,
# and needn't config anything ,So you can comment on the following configuration
urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': STATICFILES_DIRS[0]}),
                        )
