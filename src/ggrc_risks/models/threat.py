# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import CustomAttributable, BusinessObject, Timeboxed
from ggrc.models.object_document import Documentable
from ggrc.models.object_person import Personable
from ggrc.models.object_owner import Ownable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState, track_state_for_class


class Threat(
    HasObjectState, CustomAttributable, Documentable, Personable,
    Relatable, Timeboxed, Ownable, BusinessObject, db.Model):
  __tablename__ = 'threats'

  _aliases = {
      "contact": {
          "display_name": "Contact",
          "filter_by": "_filter_by_contact",
      },
      "secondary_contact": None,
      "url": "Threat URL",
  }
