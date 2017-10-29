from django.db import models

from constants import TEXT,ITEM_VALUE_PLACE_HOLDER, PAGE_NUMBER_PLACE_HOLDER

# Create your models here.
class Site(models.Model):
    name=models.CharField(max_length=256)
    url=models.CharField(max_length=1000,help_text="Use " + PAGE_NUMBER_PLACE_HOLDER + " as page number place holder")
    site_top_url=models.CharField(max_length=1000,null=True,blank=True)
    is_active=models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_matching_rules(self):
        return self.matchingrule_set.all()

class MatchingRule(models.Model):
    # ITEM_NAME_CHOICE_LIST=['title','venue','organizer','time','link']
    # ITEM_NAME_CHOICES=[(a,a) for a in ITEM_NAME_CHOICE_LIST]
    site=models.ForeignKey(Site)
    item_name=models.CharField(max_length=1000)
    is_container=models.BooleanField()
    tag_name=models.CharField(max_length=1000)
    value_format=models.CharField(max_length=1000,default=ITEM_VALUE_PLACE_HOLDER)
    attr_to_extract=models.CharField(max_length=200,default=TEXT)
    # if attr_to_extract is 'text', engine will extract the text only in the element

    def __unicode__(self):
        return "Matching rule for site: " + str(self.site) + " item: " + self.item_name

    def get_attrs(self):
        return {(a.attr_name):(a.attr_value) for a in self.attributepairs_set.all()}

class AttributePairs(models.Model):
    matching_rule=models.ForeignKey(MatchingRule)
    attr_name=models.CharField(max_length=100)
    attr_value=models.CharField(max_length=1000)
