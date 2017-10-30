from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.contexthelpers.WeakContextHelper import WeakContextHelper

LEVEL = 1
print("{}, {} Level Correlation3".format("EntryLevelCorrelator", LEVEL))
#The context should be unique, it's better add the class name since we know it's unique
context_id = "{}Layer{}Correlation3".format("EntryLevelCorrelator", LEVEL)

class EntryLevelCorrelator13(Plugin):
    def run(self, idmef):
        #Receive only simple alerts, not correlation alerts
        if idmef.get("alert.correlation_alert.name") is not None:
         return

        ctx = WeakContextHelper(context_id, { "expire": 1, "threshold": 5 ,"alert_on_expire": False }, update = True, idmef=idmef)
        #Create a context that:
        #- expires after 1 seconds of inactivity
        #- generates a correlation alert after 5 msg received
        if ctx.getUpdateCount() == 0:
         ctx.set("alert.correlation_alert.name", "Layer {} Correlation".format(LEVEL))
         ctx.set("alert.classification.text", "MyFirstEntryLevelScan13")
         ctx.set("alert.assessment.impact.severity", "high")

        if ctx.checkCorrelationAlert():
          print("Hello from {}".format(self.__class__.__name__))
          print(ctx.get("alert.classification.text"))
          ctx.alert()
          print("{} Alert finished".format(self.__class__.__name__))