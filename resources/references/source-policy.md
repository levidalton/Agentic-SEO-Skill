<!-- Updated: 2026-08-14 -->

# Evidence and Source Policy

Use this policy before turning audit observations into recommendations.

## Authority order

1. Direct evidence from the target: rendered behavior, response headers, HTML, robots directives, structured data, logs, Search Console, CrUX, and analytics.
2. Current first-party documentation from the relevant search engine, platform, schema vocabulary, or browser standard.
3. Reproducible measurements from documented tools.
4. Named third-party research with a checked publication date, method, sample, and limitations.
5. Practitioner heuristics and bundled thresholds.

Do not let a lower-authority source override a higher-authority source.

## Claim classes

Label recommendations when the distinction matters:

- `Requirement`: documented technical requirement or policy.
- `Measured`: observed value from a named tool and run.
- `Supported practice`: recommendation grounded in current first-party guidance.
- `Heuristic`: useful review prompt without proven causal ranking effect.
- `Experimental`: emerging practice whose benefit is unconfirmed.

Never convert a correlation into a requirement or predicted ranking gain.

## Current Google guardrails

- Google says there is no preferred word count. Judge completeness relative to the user and query, not a numeric floor.
- Google says `llms.txt` is unnecessary for Google Search and is ignored for ranking and generative-search visibility. Mention it only as optional metadata for another service that documents support.
- Structured data can establish eligibility for supported search features; it does not guarantee display, ranking, or AI citation.
- Search Quality Rater Guidelines help evaluate search-system performance. Rater assessments do not directly set page rankings.
- Generative or assisted authorship is not itself a quality failure. Evaluate accuracy, originality, usefulness, transparency where appropriate, and scaled-content-abuse risk.

Primary references:

- Google AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google people-first content guidance: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google generative-AI content guidance: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Google structured-data policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google third-party SEO guidance: https://developers.google.com/search/docs/fundamentals/third-party-seo

## Operational boundaries

- Audit read-only unless implementation is explicitly requested.
- Respect authentication boundaries, rate limits, terms of service, and user-defined crawl scope.
- Do not claim Search Console, analytics, production deployment, or browser evidence that was not actually observed.
- Record fetch, rendering, API, and rate-limit failures as limitations rather than site defects.
- Recheck time-sensitive claims before every material recommendation. If a claim cannot be verified efficiently, omit it or label it `Experimental`.
