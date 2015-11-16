__FILENAME__ = conf
# -*- coding: utf-8 -*-
#
# django-faq documentation build configuration file, created by
# sphinx-quickstart on Sat Sep 17 13:09:21 2011.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']

intersphinx_mapping = {
  'python': ('http://python.readthedocs.org/en/latest/', None),
  'django': ('http://django.readthedocs.org/en/latest/', None),
  'sphinx': ('http://sphinx.readthedocs.org/en/latest/', None),
    }

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'django-faq'
copyright = u'2012, Ben Spaulding'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.8'
# The full version, including alpha/beta/rc tags.
release = '0.8.3'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'django-faqdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'django-faq.tex', u'django-faq Documentation',
   u'Ben Spaulding', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'django-faq', u'django-faq Documentation',
     [u'Ben Spaulding'], 1)
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}

########NEW FILE########
__FILENAME__ = admin
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop, ungettext

from faq.settings import DRAFTED, PUBLISHED, REMOVED, STATUS_CHOICES
from faq.models import Topic, Question
from faq.forms import QuestionForm


# Actions.

def update_status(modeladmin, request, queryset, status):
    """The workhorse function for the admin action functions that follow."""
    # We loop over the objects here rather than use queryset.update() for
    # two reasons:
    #
    #  1. No one should ever be updating zillions of Topics or Questions, so
    #     performance is not an issue.
    #  2. To be tidy, we want to log what the user has done.
    #
    for obj in queryset:
        obj.status = status
        obj.save()
        # Now log what happened.
        # Use ugettext_noop() 'cause this is going straight into the db.
        log_message = ugettext_noop(u'Changed status to \'%s\'.' %
            obj.get_status_display())
        modeladmin.log_change(request, obj, log_message)

    # Send a message to the user telling them what has happened.
    message_dict = {
        'count': queryset.count(),
        'object': modeladmin.model._meta.verbose_name,
        'verb': dict(STATUS_CHOICES)[status],
    }
    if not message_dict['count'] == 1:
        message_dict['object'] = modeladmin.model._meta.verbose_name_plural
    user_message = ungettext(
        u'%(count)s %(object)s was successfully %(verb)s.',
        u'%(count)s  %(object)s were successfully %(verb)s.',
        message_dict['count']) % message_dict
    modeladmin.message_user(request, user_message)

    # Return None to display the change list page again and allow the user
    # to reload the page without getting that nasty "Send the form again ..."
    # warning from their browser.
    return None


def draft(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'drafted'."""
    return update_status(modeladmin, request, queryset, DRAFTED)
draft.short_description = _(u'Draft selected %(verbose_name_plural)s')


def publish(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'published'."""
    return update_status(modeladmin, request, queryset, PUBLISHED)
publish.short_description = _(u'Publish selected %(verbose_name_plural)s')


def remove(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'removed'."""
    return update_status(modeladmin, request, queryset, REMOVED)
remove.short_description = _(u'Remove selected %(verbose_name_plural)s')


# Inlines.

class QuestionInline(admin.TabularInline):
    extra = 1
    form = QuestionForm
    model = Question


# Admins.

class FAQAdminBase(admin.ModelAdmin):
    actions = (draft, publish, remove)
    actions_on_top = True
    actions_on_bottom = True
    list_per_page = 50


class TopicAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'status', 'sites')}),
    )
    inlines = (QuestionInline, )
    list_display = ('title', 'description', 'status', 'question_count')
    list_filter = ('status', 'sites', 'modified', 'created')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')

    def question_count(self, obj):
        """Returns the total number of Questions for this topic."""
        return obj.questions.count()
    question_count.short_description = _(u'No. of Questions')


class QuestionAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': ('topic', 'question', 'slug', 'answer', 'status',
                'ordering')}),
    )
    list_display = ('question', 'topic', 'status', 'ordering')
    list_filter = ('status', 'topic', 'modified', 'created')
    prepopulated_fields = {'slug': ('question', )}
    search_fields = ('question', 'answer')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)

########NEW FILE########
__FILENAME__ = forms
# -*- coding: utf-8 -*-

from django import forms

from faq.models import Question


class QuestionForm(forms.ModelForm):
    """A form whose only purpose is to manage fields for the QuestionInline."""

    class Meta:
        # InlineModelAdmin does not support ``fields``, so if we want to order
        # the fields in an InlineModelAdmin, we must do so with a custom
        # ModelForm. This is not ideal, but at least it gets the job done.
        #
        # Note that ``slug`` is left out of the fields list. This is because
        # we don't show the slug when adding an Question as an inline to a
        # topic because InlineModelAdmin does not support
        # ``prepopulated_fields`` either, and it's evil to expect the user
        # supply a slug by hand.
        #
        # If the user really wants to edit the slug, they can do so on the
        # Question change page.
        fields = ('question', 'answer', 'ordering', 'status')
        model = Question

########NEW FILE########
__FILENAME__ = models
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from faq.settings import DRAFTED, PUBLISHED, REMOVED, STATUS_CHOICES


# Managers.

def _field_lookups(model, status=None):
    """
    Abstraction of field lookups for managers.

    Returns a dictionary of field lookups for a queryset. The lookups
    will always filter by site. Optionally, if ``status`` is passed to
    the function the objects will also be filtered by the given status.

    This function saves from having to make two different on-site and
    published Managers each for `Topic` and `Question`, and having to move
    Managers out of the `FAQBase` model and into each of the `Topic`
    and `Question` models.

    """
    # Import models here to avoid circular import fail.
    from faq.models import Topic, Question

    field_lookups = {}

    if model == Topic:
        field_lookups['sites__pk'] = settings.SITE_ID

    if model == Question:
        field_lookups['topic__sites__pk'] = settings.SITE_ID
        if status:
            field_lookups['topic__status'] = status

    # Both Topic & Question have a status field.
    if status:
        field_lookups['status'] = status

    return field_lookups


class OnSiteManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def on_site(self):
        """Returns only items related to the current site."""
        return self.get_query_set().filter(**_field_lookups(self.model))

    def drafted(self):
        """Returns only on-site items with a status of 'drafted'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, DRAFTED))

    def published(self):
        """Returns only on-site items with a status of 'published'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, PUBLISHED))

    def removed(self):
        """Returns only on-site items with a status of 'removed'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, REMOVED))


# Models.

class FAQBase(models.Model):
    """A model holding information common to Topics and Questions."""

    created = models.DateTimeField(_(u'date created'), auto_now_add=True)
    modified = models.DateTimeField(_(u'date modified'), auto_now=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES,
        # TODO: Genericize/fix the help_text.
        db_index=True, default=DRAFTED, help_text=_(u'Only objects with \
            "published" status will be displayed publicly.'))

    objects = OnSiteManager()

    class Meta:
        abstract = True
        get_latest_by = 'modified'


class Topic(FAQBase):
    """A topic that a Question can belong to."""

    title = models.CharField(_(u'title'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the topic. Must be unique.'))
    description = models.TextField(_(u'description'), blank=True,
        help_text=_(u'A short description of this topic.'))
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
        related_name='faq_topics')

    class Meta(FAQBase.Meta):
        ordering = ('title', 'slug')
        verbose_name = _(u'topic')
        verbose_name_plural = _(u'topics')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('faq-topic-detail', (), {'slug': self.slug})


class Question(FAQBase):
    """A frequently asked question."""

    question = models.CharField(_(u'question'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the Question. Must be unique.'))
    answer = models.TextField(_(u'answer'))
    topic = models.ForeignKey(Topic, verbose_name=_(u'topic'),
        related_name='questions')
    ordering = models.PositiveSmallIntegerField(_(u'ordering'), blank=True,
        db_index=True, help_text=_(u'An integer used to order the question \
            amongst others related to the same topic. If not given this \
            question will be last in the list.'))

    class Meta(FAQBase.Meta):
        ordering = ('ordering', 'question', 'slug')
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            # We populate the slug here because the common case for adding an
            # Question is as an inline to a Topic and InlineModelAdmin does not
            # currently support ``prepopulated_fields`` and it's mean to make
            # the user supply a slug by hand.
            self.slug = slugify(self.question)[:50]
        if not self.ordering:
            # When adding an Question to a Topic, it's easy to overlook the
            # ordering. We don't want to throw an error if it's left blank,
            # so to be nice we'll just put it at the end of the list.
            try:
                # Find the highest ordering value for all other Questions
                # related to the same topic and add 1.
                ordering = self.topic.questions.exclude(pk=self.pk).aggregate(
                    models.Max('ordering'))['ordering__max'] + 1
            except TypeError:
                # There are no other related Questions, so let's set this
                # as no. 1.
                ordering = 1
            self.ordering = ordering
        super(Question, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('faq-question-detail', (), {'topic_slug': self.topic.slug,
            'slug': self.slug})

########NEW FILE########
__FILENAME__ = search_indexes
# -*- coding: utf-8 -*-

"""
Haystack SearchIndexes for FAQ objects.

Note that these are compatible with both Haystack 1.0 and Haystack 2.0-beta.

The super class for these indexes can be customized by using the
``FAQ_SEARCH_INDEX`` setting.

"""

from haystack import indexes

from faq.settings import SEARCH_INDEX
from faq.models import Topic, Question


# Haystack 2.0 (commit 070d46d72f92) requires that concrete SearchIndex classes
# use the indexes.Indexable mixin. Here we workaround that so our SearchIndex
# classes also work for Haystack 1.X.
try:
    mixin = indexes.Indexable
except AttributeError:
    mixin = object


class FAQIndexBase(SEARCH_INDEX):

    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQIndexBase, mixin):

    # Required method for Haystack 2.0, but harmless on 1.X.
    def get_model(self):
        return Topic

    # ``get_queryset`` is deprecated in Haystack v2, and ``index_queryset``
    # ought to be used instead. But we must use the former to support
    # Haystack < 1.2.4. Support for such older version is likely to be dropped
    # in the near future.
    def get_queryset(self):
        return Topic.objects.published()


class QuestionIndex(FAQIndexBase, mixin):

    # Required method for Haystack 2.0, but harmless on 1.X.
    def get_model(self):
        return Question

    # ``get_queryset`` is deprecated in Haystack v2, and ``index_queryset``
    # ought to be used instead. But we must use the former to support
    # Haystack < 1.2.4. Support for such older version is likely to be dropped
    # in the near future.
    def get_queryset(self):
        return Question.objects.published()


# try/except in order to register search indexes with site for Haystack 1.X
# without throwing exceptions with Haystack 2.0.
try:
    from haystack.sites import site
    site.register(Topic, TopicIndex)
    site.register(Question, QuestionIndex)
except ImportError:
    pass

########NEW FILE########
__FILENAME__ = settings
# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Status settings.
# It's unlikely that you should need to change these. But if
# you do, here you go.

DRAFTED = getattr(settings, 'FAQ_DRAFTED', 1)
PUBLISHED = getattr(settings, 'FAQ_PUBLISHED', 2)
REMOVED = getattr(settings, 'FAQ_REMOVED', 3)

STATUS_CHOICES = (
    (DRAFTED, _(u'drafted')),
    (PUBLISHED, _(u'published')),
    (REMOVED, _(u'removed')),
)
STATUS_CHOICES = getattr(settings, 'FAQ_STATUS_CHOICES', STATUS_CHOICES)


# Haystack settings.
# The default search index used for the app is the default haystack index.
# But possibly you want to use haystack.indexes.RealTimeSearchIndex, or another
# of your own making. Go ahead.
try:
    from haystack.indexes import SearchIndex
    SEARCH_INDEX = getattr(settings, 'FAQ_SEARCH_INDEX', SearchIndex)
except ImportError:
    SEARCH_INDEX = None

########NEW FILE########
__FILENAME__ = deep
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from faq.views.shallow import topic_list
from faq.views.normal import topic_detail
from faq.views.deep import question_detail


# Include these patterns if you want URLs like:
#
#   /faq/
#   /faq/topic/
#   /faq/topic/question/
#

urlpatterns = patterns('',
    url(r'^$', topic_list, name='faq-topic-list'),
    url(r'^(?P<slug>[-\w]+)/$', topic_detail, name='faq-topic-detail'),
    url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', question_detail,
        name='faq-question-detail'),
)

########NEW FILE########
__FILENAME__ = normal
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from faq.views.shallow import topic_list
from faq.views.normal import topic_detail, question_detail


# Include these patterns if you want URLs like:
#
#   /faq/
#   /faq/topic/
#   /faq/topic/#question
#

urlpatterns = patterns('',
    url(r'^$', topic_list, name='faq-topic-list'),
    url(r'^(?P<slug>[-\w]+)/$', topic_detail, name='faq-topic-detail'),
    url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', question_detail,
        name='faq-question-detail'),
)

########NEW FILE########
__FILENAME__ = shallow
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from faq.views.shallow import topic_list, topic_detail, question_detail


# Include these patterns if you want URLs like:
#
#   /faq/
#   /faq/#topic
#   /faq/#question
#

urlpatterns = patterns('',
    url(r'^$', topic_list, name='faq-topic-list'),
    url(r'^(?P<slug>[-\w]+)/$', topic_detail, name='faq-topic-detail'),
    url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', question_detail,
        name='faq-question-detail'),
)

########NEW FILE########
__FILENAME__ = deep
# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_detail

from faq.models import Topic, Question


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    Templates:
        :template:`faq/question_detail.html`
    Context:
        question
            A :model:`faq.Question`.
        topic
            The :model:`faq.Topic` object related to ``question``.

    """
    extra_context = {
        'topic': Topic.objects.published().get(slug=topic_slug),
    }

    return object_detail(request, queryset=Question.objects.published(),
        extra_context=extra_context, template_object_name='question',
        slug=slug)

########NEW FILE########
__FILENAME__ = normal
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_detail

from faq.models import Topic, Question
from faq.views.shallow import _fragmentify


def topic_detail(request, slug):
    """
    A detail view of a Topic

    Templates:
        :template:`faq/topic_detail.html`
    Context:
        topic
            An :model:`faq.Topic` object.
        question_list
            A list of all published :model:`faq.Question` objects that relate
            to the given :model:`faq.Topic`.

    """
    extra_context = {
        'question_list': Question.objects.published().filter(topic__slug=slug),
    }

    return object_detail(request, queryset=Topic.objects.published(),
        extra_context=extra_context, template_object_name='topic', slug=slug)


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    Simply redirects to a detail page for the related :model:`faq.Topic`
    (:view:`faq.views.topic_detail`) with the addition of a fragment
    identifier that links to the given :model:`faq.Question`.
    E.g. ``/faq/topic-slug/#question-slug``.

    """
    url = reverse('faq-topic-detail', kwargs={'slug': topic_slug})
    return _fragmentify(Question, slug, url)

########NEW FILE########
__FILENAME__ = shallow
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list

from faq.models import Topic, Question


def _fragmentify(model, slug, url=None):
    get_object_or_404(model.objects.published().filter(slug=slug))
    url = url or reverse('faq-topic-list')
    fragment = '#%s' % slug

    return redirect(url + fragment, permanent=True)


def topic_list(request):
    """
    A list view of all published Topics

    Templates:
        :template:`faq/topic_list.html`
    Context:
        topic_list
            A list of all published :model:`faq.Topic` objects that
            relate to the current :model:`sites.Site`.

    """
    return object_list(request, queryset=Topic.objects.published(),
        template_object_name='topic')


def topic_detail(request, slug):
    """
    A detail view of a Topic

    Simply redirects to :view:`faq.views.topic_list` with the addition of
    a fragment identifier that links to the given :model:`faq.Topic`.
    E.g., ``/faq/#topic-slug``.

    """
    return _fragmentify(Topic, slug)


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    Simply redirects to :view:`faq.views.topic_list` with the addition of
    a fragment identifier that links to the given :model:`faq.Question`.
    E.g. ``/faq/#question-slug``.

    """
    return _fragmentify(Question, slug)

########NEW FILE########