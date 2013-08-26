.. djournal documentation master file, created by
   sphinx-quickstart on Mon Jul  1 16:36:52 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to djournal's documentation!
====================================
.. toctree::
   :maxdepth: 2

   readme
   installation
   configuration
   roadmap

Introduction
------------
Djournal is an blog engine based in Django released under GPL 3 License. 
It offers all the functionalities to implement a weblog and aims to be extensible so developers could override existing functions and templates, and implement new ones in a easy and clean way.

Features
---------

**Entries**
	From the backend staff users can create, edit, list, delete and publish entries. Final users can list and read the published entries. 
  
**Tag**
	Entries can be tagged.

**Syndication**
	RSS feed for all the published entries and additional RSS feeds for every tag. 
 
**Easy to change entry widget**
	The backend widget for the Entry edition can be configured from the settings.py. It gives to the developer the power to transparently add custom editors widget like Markdown, WYSIWYG, reStructuredText, etc.

**Cache**
	The database queries that are repeated to often are cached in order to speed the system and reduce the overhead. For the moment it includes the Tag list and the post by date sidebar. Cached objects are reloaded every time the staff changes information in the backend. 

**Templatetags for the Tags and Posts-by-date**
	It is an easy way to add a sidebar to the blog.
	
**Default template theme and application**
	Djournal aims to be included in any existing project, it includes by default in a separate module an already implemented and configured Weblog with a pretty theme.

Future
------
**Sitemap**
	Automatic generation of the sitemap of the weblog for the web robots.

**Multi-user support (Authors)**
	Different users will be able to post their entries in the same blog. Profile support and different roles able to edit and publish global entries. 
	
**Default editor widgets**
	Offer default editor widgets (To be confirmed)

**SEO**
	Tools to manage the keywords and description metatags, sitemap ping, robots.txt, Google Analytics, etc.

**Comments**
	Comments support.

**Translations**
	Add translations for different languages.

**Social network tools**
	Add social network buttons like share in Facebook, Google Plus, etc. 

**Code optimization**
	Improve the code to make it faster
	
**Responsible design**
	Make the default theme able to change according to the browser and device capabilities.
