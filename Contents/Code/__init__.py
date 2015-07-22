PLUGIN_PREFIX = '/video/disneyjunior'
NAME = 'Disney Junior'
JSON_URL = 'http://disneyjunior.disney.com/_grill/json/'
SHOWS_URL = JSON_URL + 'video'
ICON = 'icon-default.jpg'
ART = 'art-default.jpg'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME

####################################################################################################
@handler(PLUGIN_PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():

	return Shows()

####################################################################################################
@route(PLUGIN_PREFIX + '/shows')
def Shows():

	oc = ObjectContainer()
	json_obj = JSON.ObjectFromURL(SHOWS_URL)

	for show in json_obj['stack'][0]['data']:

		title = show['title']
		thumb = show['thumb']
		slug = show['slug']

		oc.add(DirectoryObject(
			key = Callback(Videos, title=title, thumb=thumb, slug=slug),
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(thumb)
		))

	return oc

####################################################################################################
@route(PLUGIN_PREFIX + '/videos')
def Videos(title, thumb, slug):

	oc = ObjectContainer(title2=title)
	json_obj = JSON.ObjectFromURL(JSON_URL + slug)

	for group in json_obj['stack']:

		if group['type'] == 'video':

			for clip in group['data']:

				if 'live stream' in clip['title'].lower():
					continue

				title = clip['title']
				summary = clip['description'] if 'description' in clip else None
				thumb = clip['thumb']

				try:
					duration = int(clip['duration_sec'])*1000
				except:
					duration = None

				url = clip['href']

				if not url.startswith('http://'):
					url = 'http://disneyjunior.com%s' % (url)

				oc.add(VideoClipObject(
					url = url,
					title = title,
					summary = summary,
					duration = duration,
					thumb = Resource.ContentsOfURLWithFallback(thumb)
				))

	return oc
