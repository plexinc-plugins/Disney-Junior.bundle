PLUGIN_PREFIX = '/video/disneyjunior'
NAME = 'Disney Junior'
JSON_URL = 'http://disneyjunior.com/_grill/json/'
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
	json_obj = JSON.ObjectFromURL(JSON_URL)

	for show in json_obj['stack'][0]['data']:

		url = show['href']
		title = show['title']
		thumb = show['logo']

		oc.add(DirectoryObject(
			key = Callback(Videos, title=title, thumb=thumb, url=url),
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(thumb)
		))

	return oc

####################################################################################################
@route(PLUGIN_PREFIX + '/videos')
def Videos(title, thumb, url):

	oc = ObjectContainer(title2=title)
	json_url = '%s%s/video' % (JSON_URL, url.split('/')[-1])
	json_obj = JSON.ObjectFromURL(json_url)

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
