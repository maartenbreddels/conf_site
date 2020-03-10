from django import forms

from constance import config

from .models import Proposal, ProposalKeyword


class ModelMultipleTagChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom form field to allow multiple tag selection.

    See https://stackoverflow.com/a/34207440/113527self.

    """
    widget = forms.CheckboxSelectMultiple

    def prepare_value(self, value):
        if hasattr(value, "tag_id"):
            return value.tag_id
        elif (hasattr(value, "__iter__")
                and not isinstance(value, str)
                and not hasattr(value, "_meta")):
            return [self.prepare_value(v) for v in value]
        else:
            return super(ModelMultipleTagChoiceField,
                         self).prepare_value(value)


class ProposalForm(forms.ModelForm):
    official_keywords = ModelMultipleTagChoiceField(
        label="Official Keywords",
        queryset=ProposalKeyword.objects.filter(official=True).order_by("name"))    # noqa: E501

    class Meta:
        model = Proposal
        fields = [
            "title",
            "audience_level",
            "description",
            "abstract",
            "affiliation",
            "additional_notes",
            "first_time_at_jupytercon",
            "requests",
            "gender",
            "referral",
            "under_represented_group",
            "accomodation_needs",
            "recording_release",
            "phone_number",
            "slides_url",
            "code_url",
            "official_keywords",
            "user_keywords",
        ]

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)

        # Don't display keyword fields if keyword support is disabled.
        if not config.PROPOSAL_KEYWORDS:
            del self.fields["official_keywords"]
            del self.fields["user_keywords"]
        # Don't display slide and code repo fields if support is disabled.
        if not config.PROPOSAL_URL_FIELDS:
            del self.fields["slides_url"]
            del self.fields["code_url"]

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value
