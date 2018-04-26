# -*- coding: utf-8 -*-
from server.bones import recordBone, stringBone, selectOneBone

class urlBone(recordBone):
	type = "record.url"
	validProtocols = ["http://", "https://"]

	def __init__(self, enforceProtocol="//", *args, **kwargs):
		from server import skeleton

		class urlSkel(skeleton.RelSkel):
			url = stringBone(descr=u"URL")
			target = selectOneBone(descr=u"Target", values=["_blank", "_parent"])

		super(urlBone, self).__init__(using = urlSkel, *args, **kwargs)
		self.enforceProtocol = enforceProtocol

	def _adjustProtocol(self, value):
		url = value["url"]

		if not url.startswith(self.enforceProtocol):
			for prot in self.validProtocols:
				if url.startswith(prot):
					url = url[len(prot):]
					break

			value["url"] = self.enforceProtocol + url

		return None


	def fromClient(self, valuesCache, name, data):
		res = super(urlBone, self).fromClient(valuesCache, name, data)
		if res is not None:
			return res

		if valuesCache[name]:
			if self.multiple:
				for item in valuesCache[name]:
					self._adjustProtocol(item)
			else:
				self._adjustProtocol(valuesCache[name])

		return None
