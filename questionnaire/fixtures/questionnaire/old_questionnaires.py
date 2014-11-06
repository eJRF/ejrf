from questionnaire.models import Questionnaire, Section

questionnaire1 = Questionnaire.objects.create(name="JRF 2011 Core English",
                                              description="From dropbox as given by Rouslan",
                                              year=2011, finalized=True)
questionnaire2 = Questionnaire.objects.create(name="JRF 2010 Core English",
                                              description="From dropbox as given by Rouslan",
                                              year=2010, finalized=True)
questionnaire3 = Questionnaire.objects.create(name="JRF 2009 Core English",
                                              description="From dropbox as given by Rouslan",
                                              year=2009, finalized=True)
questionnaire4 = Questionnaire.objects.create(name="JRF 2012 Core English",
                                              description="From dropbox as given by Rouslan",
                                              year=2012, finalized=True)

Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                       questionnaire=questionnaire1, name="Reported Cases")

Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                       questionnaire=questionnaire2, name="Reported Cases")
Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                       questionnaire=questionnaire3, name="Reported Cases")
Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                       questionnaire=questionnaire4, name="Reported Cases")