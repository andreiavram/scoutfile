from goodies.forms import CrispyBaseModelForm
from locuri.models import GPXTrack


class GPXTrackForm(CrispyBaseModelForm):
    class Meta:
        model = GPXTrack
        fields = ["title", "gpx_file", "source_url"]
