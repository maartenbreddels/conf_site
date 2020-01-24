# -*- coding: utf-8 -*-
from django.urls import reverse

from constance.test import override_config

from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.tests import ReviewingTestCase

from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.tests.factories import (
    ProposalFeedbackFactory,
    ProposalVoteFactory,
)


class ProposalDetailViewAccessTestCase(ReviewingTestCase, AccountsTestCase):
    reverse_view_name = "review_proposal_detail"

    def setUp(self):
        super(ProposalDetailViewAccessTestCase, self).setUp()
        self.proposal = ProposalFactory()
        self.reverse_view_args = [self.proposal.pk]

    def test_blind_reviewing_types_as_author(self):
        """Verify whether BLIND_AUTHORS setting works properly."""
        self._i_am_the_speaker_now()

        # Create a feedback comment, otherwise this test will pass
        # when it should fail.
        ProposalFeedbackFactory(
            proposal=self.proposal, author=self.reviewer.user
        )

        with override_config(BLIND_AUTHORS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertNotContains(response, self.reviewer.name)
            self.assertNotContains(response, self.reviewer.user.username)
            self.assertNotContains(response, self.reviewer.email)

    def test_blind_reviewing_means_no_notes_section(self):
        """
        Verify that the Notes section does not appear if BLIND_REVIEWERS is on.
        """
        self._add_to_reviewers_group()
        # Set this proposal's notes field to something memorable.
        self.proposal.additional_notes = "xyzzy"
        self.proposal.save()

        with override_config(BLIND_REVIEWERS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertNotContains(response, "Notes")
            self.assertNotContains(response, self.proposal.additional_notes)

    def test_primary_speaker_cannot_view_votes_tab(self):
        """Verify that proposal speakers cannot view their proposal's votes."""
        self._i_am_the_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "proposal-reviews")

    def test_additional_speakers_cannot_view_votes_tab(self):
        """
        Verify that additional speakers cannot view their proposal's votes.
        """
        self._i_am_also_a_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "proposal-reviews")

    def test_reviewer_can_view_votes_tab(self):
        """Verify that a reviewer can view a proposal's votes."""
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(response, "proposal-reviews")

    def test_primary_speaker_cannot_view_result_buttons(self):
        """Verify that proposal speakers cannot view result buttons section."""
        self._i_am_the_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_additional_speakers_cannot_view_result_buttons(self):
        """Verify that additional speakers cannot view result buttons."""
        self._i_am_also_a_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_reviewer_cannot_view_result_buttons(self):
        """
        Verify that proposal reviewers cannot view result buttons section.
        """
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_superuser_can_view_result_buttons(self):
        """Verify that superusers can view result buttons section."""
        self._become_superuser()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(response, "div-proposal-result-buttons")

    def test_reviewer_cannot_view_other_reviewers_names(self):
        """Verify that a reviewer cannot view other reviewers' names."""
        other_vote = ProposalVoteFactory(proposal=self.proposal)
        other_feedback = ProposalFeedbackFactory.create(proposal=self.proposal)

        self._add_to_reviewers_group()
        with override_config(BLIND_REVIEWERS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertContains(response, "Anonymous")

            self.assertNotContains(response, other_vote.voter.username)
            self.assertNotContains(response, other_vote.voter.email)

            self.assertNotContains(response, other_feedback.author.username)
            self.assertNotContains(response, other_feedback.author.email)
