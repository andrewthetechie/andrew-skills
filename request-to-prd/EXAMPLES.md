# Examples

## Compact Bug Example

Input:

```text
Users say archived projects still show up in the active project picker after refresh. They should only appear in archive search.
```

Output shape:

```md
# Hide Archived Projects From Active Project Picker

## Intake Summary
Type: bug
Source request: Archived projects appear in a picker intended for active projects.
Evidence reviewed: Project glossary and picker/search code paths when available.

## Problem Statement
Users cannot trust the active project picker because archived projects remain selectable after refresh.

## Proposed Solution
The active project picker should filter to active projects only. Archived projects remain discoverable through archive search.

## Functional Requirements
- Given an archived project, when a user opens or refreshes the active project picker, then that project must not appear.
- Given an archived project, when a user searches archive results, then that project remains visible there.
- Existing direct links to archived projects must keep their current behavior unless human input says otherwise.

## Assumptions
- Direct links should not be changed by this fix - Basis: picker visibility is narrower than access policy. Confidence: medium.

## Open Questions Requiring Human Input
- Should users lose all access to archived projects from active workflows? - Why human input is required: this changes product access semantics beyond the reported picker bug.
```

## Compact Feature Example

Input:

```text
Let admins resend pending invites from the team page because people miss the first email.
```

Output shape:

```md
# Resend Pending Team Invites

## Intake Summary
Type: feature
Source request: Admins need a way to resend pending team invitations from the team page.
Evidence reviewed: Team role vocabulary, invitation lifecycle, email job behavior, and existing team page patterns when available.

## Problem Statement
Admins cannot recover when invitees miss the original invitation email, which forces manual support or invite recreation.

## Proposed Solution
Admins can resend an invitation while it is pending. Resend uses the existing invitation lifecycle and email delivery path, preserves the invitation target and role, and records the resend for audit or troubleshooting when the repo has an audit pattern.

## Functional Requirements
- Admins can resend only pending invitations.
- The system rejects resend attempts for accepted, expired, revoked, or unknown invitations with stable user-visible errors.
- Duplicate resend actions are rate-limited or safely idempotent.

## Assumptions
- Resend should reuse the existing invite token until expiration - Basis: avoids changing invite lifecycle unless repo evidence prefers token rotation. Confidence: low.

## Open Questions Requiring Human Input
- Should resending rotate the invitation token? - Why human input is required: this is a security and product trade-off if the repo has no established policy.
```

