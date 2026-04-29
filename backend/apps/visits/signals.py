"""
Signal: protsedura yoki konsultatsiya o'zgarganda Visit summasi avto-yangilanadi.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import VisitProcedure, VisitConsultation


@receiver([post_save, post_delete], sender=VisitProcedure)
def recalc_on_procedure_change(sender, instance, **kwargs):
    instance.visit.recalculate()


@receiver([post_save, post_delete], sender=VisitConsultation)
def recalc_on_consultation_change(sender, instance, **kwargs):
    instance.visit.recalculate()
