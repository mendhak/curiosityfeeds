Google app engine project.  The plan is to provide RSS feeds for

* MSL Curiosity Raw Images
* MSL Curiosity Images
* MSL Curiosity Multimedia
* MSL Curiosity News

TODO:

* Move getfeeds.py work to the background using the [Task Queue API](https://developers.google.com/appengine/docs/python/taskqueue/)
	* Inform client via [Channel API](https://developers.google.com/appengine/docs/python/channel/overview)
	* Or just make another datastore entity
* Create AJAX interface for getfeeds.py to get realistic progress
* Generate RSS feed for Images