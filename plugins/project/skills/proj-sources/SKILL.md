---
name: proj-sources
description: Find and inventory relevant sources for a named project across connected workspace tools, with explicit coverage and access gaps. Use when the user gives a project, initiative, feature, launch, customer, or code name and asks for source links, context, docs, meetings, meeting notes, Slack channels, Notion pages, Google Docs, Google Calendar/Meet events, or other related resource URLs.
metadata:
  owner: jay1803
  family: project
  maturity: stable
  distribution: project
---

# Project Sources

## Overview

Collect a source map for a project from connected workspace systems. Return only evidence-backed links and clearly report which systems were searched, unavailable, or blocked.

## Workflow

1. Bind the project and discovery scope from the request. Start from supplied
   links and verified aliases; ask only when the target is ambiguous.
2. Discover available workspace tools. Do not use public web search to discover
   private workspace sources or invent connector access.
3. For a specific missing decision/document, search only relevant systems and
   follow high-signal links until the question is answered or coverage is exhausted.
   For an explicit full inventory, search each available category and report the
   exact scope and any omissions. Use a stated time window relevant to the request.
4. Deduplicate by canonical URL, retain relevance and source provenance, and
   distinguish strong matches from ambiguous namesakes.
5. Return the inventory and searched/unavailable/unchecked coverage. Do not
   create project records, contact people or start downstream work as a side effect.

## Search Targets

Search these categories when connectors are available:

- **Notion**: pages, databases, project hubs, specs, decision logs, task pages, meeting-note pages, backlinks, and linked child pages.
- **Slack**: channels with matching names or topics, channel bookmarks, canvases, pinned files, high-signal threads, and messages containing resource URLs.
- **Google Drive/Docs**: Docs, Sheets, Slides, folders, shortcuts, shared files, specs, PRDs, design docs, spreadsheets, and documents linked from Slack, Notion, or Calendar.
- **Google Calendar/Meet**: project meetings, recurring events, Meet links, attachments, agenda docs, meeting notes docs, and event descriptions. Use the project period or requested time window and state the dates searched.
- **Other resources**: Linear issues, GitHub repos or PRs, Figma files, Looms, dashboards, customer notes, vendor docs, or other URLs found inside the searched systems.

If Gmail or another workspace connector is available and the search surface appears relevant, use it only to find additional project resource URLs unless the user asks for email analysis.

## Evidence Rules

- Include only URLs, channel names, and event references returned by tools or found inside retrieved source content.
- Do not invent or reconstruct private URLs from names alone.
- Prefer source-of-record pages over secondary mentions, but keep secondary links when they reveal useful resources.
- Capture why each item is related: title match, body mention, linked from a meeting, shared in a project channel, attached to an event, or referenced by another source.
- Track access gaps. If a connector is unavailable, auth fails, or a search cannot be performed, list that limitation in the final output.

## Output Format

Start with a short coverage line:

`Searched: Notion, Slack, Google Drive/Docs, Google Calendar from <start date> to <end date>. Not searched: <blocked or unavailable systems>.`

Then provide grouped lists:

## Notion Pages
- `<title>` - `<url>` - `<why it is related>`

## Slack Channels
- `#channel-name` - `<channel url if available>` - `<why it is related>`

## Google Docs and Drive Files
- `<title>` - `<url>` - `<doc/sheet/slide/folder>` - `<why it is related>`

## Google Meetings and Meeting Notes
- `<event title>` - `<event or meet url>` - `<date>` - `Notes: <notes doc url if available>` - `<why it is related>`

## Other Related Resources
- `<title or resource type>` - `<url>` - `<source where found>` - `<why it is related>`

End with a brief `Gaps` section when anything important was unavailable, ambiguous, or low confidence.

## Quality Bar

- Prefer a compact inventory over a narrative summary.
- Keep snippets short; use them only when they explain relevance.
- Separate strong matches from weak matches if the project name collides with generic terms.
- If the source map is large, list the most authoritative items first within each group and mention how many additional low-signal matches were omitted.
