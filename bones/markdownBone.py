# -*- coding: utf-8 -*-
from server.bones import baseBone
from server.bones.stringBone import LanguageWrapper

import logging

class markdownBone(baseBone):
	type = "str.markdown"

	def __init__(self, indexed=False, languages=None, *args, **kwargs):
		baseBone.__init__(self, *args, **kwargs)

		if indexed:
			raise NotImplementedError("indexed=True is not supported on markdownBones")

		if self.multiple:
			raise NotImplementedError("multiple=True is not supported on markdownBones")

		if not (languages is None
		        or (isinstance(languages, list)
		            and len(languages) > 0
		            and all([isinstance(x,basestring) for x in languages]))):
			raise ValueError("languages must be None or a list of strings ")

		self.languages = languages

		if self.languages:
			self.defaultValue = LanguageWrapper(self.languages)

	def serialize(self, valuesCache, name, entity):
		if self.languages:
			for k in entity.keys(): #Remove any old data
				if k.startswith("%s." % name ):
					del entity[k]

			for lang in self.languages:
				if isinstance(valuesCache[name], dict) and lang in valuesCache[name].keys():
					val = valuesCache[name][ lang ]

					if not val:
						#This text is empty (ie. it might contain only an empty <p> tag
						continue

					entity["%s.%s" % (name, lang)] = val
		else:
			entity.set(name, valuesCache[name], self.indexed)

		return entity

	def unserialize(self, valuesCache, name, expando):
		if not self.languages:
			if name in expando.keys():
				valuesCache[name] = expando[ name ]

		else:
			valuesCache[name] = LanguageWrapper(self.languages)

			for lang in self.languages:
				if "%s.%s" % (name, lang) in expando.keys():
					valuesCache[name][ lang ] = expando["%s.%s" % (name, lang)]

			if not valuesCache[name].keys(): #Got nothing

				if name in expando.keys(): #Old (non-multi-lang) format
					valuesCache[name][self.languages[0]] = expando[name]

				for lang in self.languages:
					if (not lang in valuesCache[name].keys()
					    and "%s_%s" % (name, lang) in expando.keys()):
						valuesCache[name][lang] = expando["%s_%s" % (name, lang)]

		return True

	def fromClient( self, valuesCache, name, data ):
		if self.languages:
			lastError = None
			valuesCache[name] = LanguageWrapper(self.languages)

			for lang in self.languages:
				if "%s.%s" % (name,lang) in data.keys():
					val = data["%s.%s" % (name,lang)]
					err = self.isInvalid(val)
					if not err:
						valuesCache[name][lang] = val
					else:
						lastError = err

			if not any(valuesCache[name].values()) and not lastError:
				lastError = "No or invalid values entered"

			return lastError

		else:
			if name in data.keys():
				value = data[name]
			else:
				value = None

			if not value:
				valuesCache[name] = ""
				return "No value entered"

			if not isinstance(value, str) and not isinstance(value, unicode):
				value = unicode(value)

			err = self.isInvalid(value)
			if not err:
				valuesCache[name] = value

			return err

	def getReferencedBlobs(self, valuesCache, name):
		logging.debug("TODO")
		return super(markdownBone, self).getReferencedBlobs(valuesCache, name)

		'''
		newFileKeys = []
		if self.languages:
			if valuesCache[name]:
				for lng in self.languages:
					if lng in valuesCache[name].keys():
						val = valuesCache[name][ lng ]
						if not val:
							continue
						idx = val.find("/file/download/")
						while idx!=-1:
							idx += 15
							seperatorIdx = min( [ x for x in [val.find("/",idx), val.find("\"",idx)] if x!=-1] )
							fk = val[ idx:seperatorIdx]
							if not fk in newFileKeys:
								newFileKeys.append( fk )
							idx = val.find("/file/download/", seperatorIdx)
		else:
			if valuesCache[name]:
				idx = valuesCache[name].find("/file/download/")
				while idx!=-1:
					idx += 15
					seperatorIdx = min( [ x for x in [valuesCache[name].find("/",idx), valuesCache[name].find("\"",idx)] if x!=-1] )
					fk = valuesCache[name][ idx:seperatorIdx]
					if not fk in newFileKeys:
						newFileKeys.append( fk )
					idx = valuesCache[name].find("/file/download/", seperatorIdx)
		return( newFileKeys )
		'''


	def getSearchTags(self, valuesCache, name):
		res = []
		logging.debug("TODO")

		'''
		if not valuesCache[name]:
			return( res )
		if self.languages:
			for v in valuesCache[name].values():
				value = HtmlSerializer( None ).santinize( v.lower() )
				for line in unicode(value).splitlines():
					for key in line.split(" "):
						key = "".join( [ c for c in key if c.lower() in conf["viur.searchValidChars"]  ] )
						if key and key not in res and len(key)>3:
							res.append( key.lower() )
		else:
			value = HtmlSerializer( None ).santinize( valuesCache[name].lower() )
			for line in unicode(value).splitlines():
				for key in line.split(" "):
					key = "".join( [ c for c in key if c.lower() in conf["viur.searchValidChars"]  ] )
					if key and key not in res and len(key)>3:
						res.append( key.lower() )			
		'''
		return res

	def getSearchDocumentFields(self, valuesCache, name):

		logging.debug("TODO")
		return []

		'''
		if self.languages:
			assert isinstance(valuesCache[name], dict), "The value shall already contain a dict, something is wrong here."

			if self.validHtml:
				return [search.HtmlField(name=name, value=unicode( valuesCache[name].get(lang, "")), language=lang)
				        for lang in self.languages]
			else:
				return [search.TextField(name=name, value=unicode( valuesCache[name].get(lang, "")), language=lang)
				        for lang in self.languages]
		else:
			if self.validHtml:
				return [search.HtmlField( name=name, value=unicode(valuesCache[name]))]
			else:
				return [search.TextField( name=name, value=unicode(valuesCache[name]))]
		'''
