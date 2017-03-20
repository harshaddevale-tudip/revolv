from django.conf.urls import patterns, url
from revolv.base.users import is_ambassador, is_logged_in
from revolv.project.views import (CreateProjectView, EditProjectUpdateView,
                                  PostProjectUpdateView, ProjectView,ProjectReinvestView,
                                  ReviewProjectView, SubmitDonationView,
                                  UpdateProjectView, ProjectListReinvestmentView,
                                  stripe_payment, stripe_operation_donation)

urlpatterns = patterns(
    '',
    url(r'^create$', is_ambassador(CreateProjectView.as_view()), name='new'),
    url(r'^(?P<pk>\d+)/stripe/$', stripe_payment, name='stripe_payment'),
    url(r'^stripe_operation_donation/$', stripe_operation_donation, name='stripe_operation_donation'),
    url(r'^(?P<pk>\d+)/edit$', is_ambassador(UpdateProjectView.as_view()), name='edit'),
    #url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/reinvest_page/$', ProjectReinvestView.as_view(), name='project_reinvest'),
    url(r'^(?P<pk>\d+)/reinvest/$', 'revolv.project.views.reinvest', name='reinvest'),
    url(r'^(?P<pk>\d+)/review$', is_ambassador(ReviewProjectView.as_view()), name='review'),
    url(r'reinvest_list/$', is_logged_in(ProjectListReinvestmentView.as_view()), name='reinvest_list'),
    url(r'^(?P<pk>\d+)/donation/submit$', SubmitDonationView.as_view(), name="donation_submit"),
    url(r'^(?P<pk>\d+)/update$', is_ambassador(PostProjectUpdateView.as_view()), name='update'),
    url(r'^editupdate/(?P<pk>\d+)$', is_ambassador(EditProjectUpdateView.as_view()), name='edit_project_update'),
    url(r'^(?P<title>[^/]+)/$', ProjectView.as_view(), name='view'),
)

