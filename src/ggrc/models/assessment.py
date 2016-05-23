# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Module for Assessment object"""

from ggrc import db
from ggrc.models import mixins_reminderable
from ggrc.models import mixins_statusable
from ggrc.models import reflection
from ggrc.models.comment import Commentable
from ggrc.models.mixin_autostatuschangable import AutoStatusChangable
from ggrc.models.mixins import BusinessObject
from ggrc.models.mixins import CustomAttributable
from ggrc.models.mixins import FinishedDate
from ggrc.models.mixins import TestPlanned
from ggrc.models.mixins import Timeboxed
from ggrc.models.mixins import VerifiedDate
from ggrc.models.mixins_assignable import Assignable
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.reflection import PublishOnly
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState
from ggrc.models.track_object_state import track_state_for_class


class Assessment(mixins_statusable.Statusable,
                 AutoStatusChangable, Assignable, HasObjectState, TestPlanned,
                 CustomAttributable, Documentable, Commentable, Personable,
                 mixins_reminderable.Reminderable, Timeboxed,
                 Ownable, Relatable, FinishedDate, VerifiedDate,
                 BusinessObject, db.Model):
  """Class representing Assessment.

  Assessment is an object representing an individual assessment performed on
  a specific object during an audit to ascertain whether or not
  certain conditions were met for that object.
  """

  __tablename__ = 'assessments'

  ASSIGNEE_TYPES = (u"Creator", u"Assessor", u"Verifier")

  REMINDERABLE_HANDLERS = {
      "statusToPerson": {
          "handler":
              mixins_reminderable.Reminderable.handle_state_to_person_reminder,
          "data": {
              mixins_statusable.Statusable.START_STATE: "Assessor",
              "In Progress": "Assessor"
          },
          "reminders": {"assessment_assessor_reminder", }
      }
  }

  object = {}  # we add this for the sake of client side error checking
  audit = {}

  # REST properties
  _publish_attrs = [
      PublishOnly('audit'),
      PublishOnly('object')
  ]

  _tracked_attrs = {
      'contact_id',
      'description',
      'notes',
      'reference_url',
      'secondary_contact_id',
      'test_plan',
      'title',
      'url',
      'start_date',
      'end_date'
  }

  _aliases = {
      "audit": {
          "display_name": "Audit",
          "mandatory": True,
      },
      "url": "Assessment URL",
      "related_creators": {
          "display_name": "Creator",
          "mandatory": True,
          "filter_by": "_filter_by_related_creators",
          "type": reflection.AttributeInfo.Type.MAPPING,
      },
      "related_assessors": {
          "display_name": "Assessor",
          "mandatory": True,
          "filter_by": "_filter_by_related_assessors",
          "type": reflection.AttributeInfo.Type.MAPPING,
      },
      "related_verifiers": {
          "display_name": "Verifier",
          "filter_by": "_filter_by_related_verifiers",
          "type": reflection.AttributeInfo.Type.MAPPING,
      },
  }

  @classmethod
  def _filter_by_related_creators(cls, predicate):
    return cls._get_relate_filter(predicate, "Creator")

  @classmethod
  def _filter_by_related_assessors(cls, predicate):
    return cls._get_relate_filter(predicate, "Assessor")

  @classmethod
  def _filter_by_related_verifiers(cls, predicate):
    return cls._get_relate_filter(predicate, "Verifier")

track_state_for_class(Assessment)
