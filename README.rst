Djournal
========
**Django weblogging application and platform.**

Djournal is a weblog application for Django released under GPLv3. It is composed by an application pluggable into other django projects and a platform to run a standalone weblog application.



Components
----------

djournal:
	The engine. It is a Django Application. It doesn't run by itself, 
	it must be imported into another project. Djournalsite is a specific 
	Django project already configured to run djournal.

djournalsite:
	It is a project configured to run djournal. If you plan to run
	only a Weblog with djournal use djournalsite, otherwise if you
	plan to plug djournal into an existent Django project you can 
	delete the djournalsite package.   
