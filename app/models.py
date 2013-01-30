from django.db import models
import panex_web.config
import re

# Create your models here.

class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=400)
    version = models.CharField(max_length=10, default="1.0.0")
    author = models.CharField(max_length=200)
    downloads = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name + "\n" + self.description

    def is_updated(self, inputVersion):
    	if self.version_checker(self.version, inputVersion) > 0:
    		return True
    	return False

    def version_checker(self, version1, version2):
    	def normalize(v):
    		return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    	return cmp(normalize(version1), normalize(version2))

# 
# Small test suite to check the version checker function
# 
if __name__ == '__main__':
	assert version_checker('1.1.1.1', '1.1.1.1') == 0
	assert version_checker('1.1.1.2', '1.1.1.1') == 1