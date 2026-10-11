# {{account_name}} — Deal Tracker

## Current Status
Deal Health: {{deal_health}}
Last Updated: {{date}}

{{rolling_bluf}}

<!-- BLUF is the ONLY section that gets overwritten on each update. Everything below is append-only. -->

{{#each workstreams}}
## {{workstream_name}}
<!-- Entries appear in reverse chronological order. Newest at top. -->

{{/each}}
## General / Cross-Cutting
<!-- Entries that span multiple workstreams or don't fit a specific one. -->
