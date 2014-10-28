from questionnaire.models.base import BaseModel

class SkipQuestion(BaseModel):
	test= "hello"
	# root-question = models.ForeignKey(Question, blank=False, null=False, related_name="root-question")