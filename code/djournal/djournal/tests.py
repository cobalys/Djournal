#===============================================================================
# >>> 
# >>> c = Client()
# >>> response = c.post('/login/', {'username': 'john', 'password': 'smith'})
# >>> response.status_code
# 200
# >>> response = c.get('/customer/details/')
# >>> response.content
#===============================================================================

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from djournal.admin import EntryAdmin
from djournal.models import Entry
from django.contrib.admin.sites import AdminSite

request = None
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean "\
        "vitae pharetra erat, eget posuere eros. Nunc eleifend risus mi, "\
        "ut auctor augue consequat sit amet. Nunc eget porta ligula. "\
        "Curabitur nec mi augue. Fusce fringilla neque arcu, id lobortis "\
        "risus dictum mollis. Suspendisse vehicula est purus, id semper "\
        "urna fermentum at. Suspendisse mattis tristique dui et interdum. "\
        "Suspendisse vel arcu at arcu lobortis fermentum vitae id justo. "\
        "Duis eleifend tellus nulla, eu pulvinar dolor sodales in. Donec "\
        "id mattis dolor, id sollicitudin justo. Nulla facilisi. Quisque "\
        "id elit ac magna malesuada rutrum. Quisque suscipit lectus sed "\
        "elementum euismod. In hac habitasse platea dictumst. "\
        "Suspendisse potenti."
        
        
class EntryCase(TestCase):

    def setUp(self):
        password = 'admin' 
        my_admin = User.objects.create_superuser('admin', 'admin@example.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)
        self.site = AdminSite()

    def test_default_fields(self):
        ma = EntryAdmin(Entry, self.site)
        fields = {key: value.required for key, value in ma.get_form(request).base_fields.iteritems()}
        expected_fields = {'tags': False, 'title': True, 'excerpt': False, 'content': True, 'published': False, 'slug': False}
        self.assertEqual(fields, expected_fields)


    def test_entries_creation(self):
        #Create draft Entry
        response = self.client.post('/admin/djournal/entry/add/', 
                                    {
                                     'title': 'Test entry',
                                     'content': lorem,
                                     '_save': 'Save draft'
                                     }
                                    )
        entry = Entry.objects.get(title='Test entry')
        self.assertEqual(entry.title, 'Test entry')
        self.assertEqual(entry.content, lorem)
        self.assertEqual(entry.excerpt, '')
        self.assertEqual(entry.published, False)
        
        #Create published Entry
        response = self.client.post('/admin/djournal/entry/add/', 
                                    {
                                     'title': 'Test published entry',
                                     'content': lorem,
                                     '_publish': 'Publish'
                                     }
                                    )
        entry_2 = Entry.objects.get(title='Test published entry')
        self.assertEqual(entry_2.title, 'Test published entry')
        self.assertEqual(entry_2.content, lorem)
        self.assertEqual(entry_2.excerpt, '')
        self.assertEqual(entry_2.published, True)

        #Update published Entry
        response = self.client.post('/admin/djournal/entry/%i/'% entry_2.id, 
                                    {
                                     'title': 'Title Change',
                                     'content': lorem,
                                     '_save': 'Publish'
                                     }
                                    )
        entry_2 = Entry.objects.get(pk=entry_2.id)
        self.assertEqual(entry_2.title, 'Title Change')
        self.assertEqual(entry_2.content, lorem)
        self.assertEqual(entry_2.excerpt, '')
        self.assertEqual(entry_2.published, True)

        #Revert Entry to draft
        response = self.client.post('/admin/djournal/entry/%i/'% entry_2.id, 
                                    {
                                     'title': 'Title Change',
                                     'content': lorem,
                                     '_unpublish': 'Revert to draft and save'
                                     }
                                    )
        entry_2 = Entry.objects.get(pk=entry_2.id)
        self.assertEqual(entry_2.title, 'Title Change')
        self.assertEqual(entry_2.content, lorem)
        self.assertEqual(entry_2.excerpt, '')
        self.assertEqual(entry_2.published, False)
        #Update draft
        response = self.client.post('/admin/djournal/entry/%i/'% entry_2.id, 
                                    {
                                     'title': 'Title Change',
                                     'content': lorem,
                                     '_update': 'Update draft'
                                     }
                                    )
        entry_2 = Entry.objects.get(pk=entry_2.id)
        self.assertEqual(entry_2.title, 'Title Change')
        self.assertEqual(entry_2.content, lorem)
        self.assertEqual(entry_2.excerpt, '')
        self.assertEqual(entry_2.published, False)
        #Update draft
        
        #Publish Back.
        response = self.client.post('/admin/djournal/entry/%i/'% entry_2.id, 
                                    {
                                     'title': 'Title Change',
                                     'content': lorem,
                                     '_publish': 'Publish'
                                     }
                                    )
        entry_2 = Entry.objects.get(pk=entry_2.id)
        self.assertEqual(entry_2.title, 'Title Change')
        self.assertEqual(entry_2.content, lorem)
        self.assertEqual(entry_2.excerpt, '')
        self.assertEqual(entry_2.published, False)
        #Assign existing tag
        #Assign new tag
        #Listed tags
        #Delete entry.
        response = self.client.post('/admin/djournal/entry/%i/'% entry_2.id, 
                                    {
                                     'post': 'yes',
                                     }
                                    )
        Entry.objects.get(pk=entry_2.id)


    def test_entries_list(self):
        c = Client()
        #List entries
        #Batch delete
        #Batch publish

# 
# class TagCase(TestCase):
#     def test_tag_creation(self):
#         
#     def test_tag_listing(self):
#         
