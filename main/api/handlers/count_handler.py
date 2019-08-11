from main.app import db
from main.models import Counter


class CountHandler(object):
	@staticmethod
	def get_count():
		counter = Counter.query.all()
		if len(counter):
			c = counter[0]
			c.count += 1
			db.session.commit()
			return c.count
		else:
			c = Counter(count=0)
			db.session.add(c)
			db.session.commit()
			return c.count

	@staticmethod
	def serialize(c):
		counter = {}
		counter.update(c.__dict__)
		counter.pop('_sa_instance_state', -1)
		return counter
