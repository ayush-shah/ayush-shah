# Ayush Shah GitHub profile: public-source research

Researched 2026-09-26 and updated with Ayush's corrections on 2026-09-27 for a profile README at `github.com/ayush-shah`. Sources below are Ayush's public GitHub profile, public repositories, public upstream pull requests, and experience supplied directly by Ayush. PR totals are a dated snapshot; individual merged PRs are better durable evidence for README claims. Employment wording reflects Ayush's subsequent clarification that Deuex is his employer and Collate is its client.

## Identity and positioning

- [The GitHub profile](https://github.com/ayush-shah) identifies the account as **Ayush Shah** and lists **Mumbai, India**. Ayush clarified that his employer is **Deuex**, where his title is **Solutions Engineer**; he works with client **Collate** as a **Software Engineer** on OpenMetadata. His Deuex company field is therefore correct, while the old bio was outdated. The public PR record does not establish an OpenMetadata maintainer or founder title.
- The current lead is **backend and data platform engineer working on OpenMetadata since 2021**, with work across metadata ingestion, data quality, connectors, Python SDK, documentation, and the broader data platform. The technical contribution themes are supported by the [merged PR record](https://github.com/search?q=is%3Apr+author%3Aayush-shah+org%3Aopen-metadata+is%3Apublic+is%3Amerged&type=pullrequests); employer, client role, and platform scope come from Ayush's direct account.
- Public contributions to the main repository reach back to [PR #16, created August 2021 and merged August 2021](https://github.com/open-metadata/OpenMetadata/pull/16). The recent merged work includes [ingestion validation and migration PR #29566](https://github.com/open-metadata/OpenMetadata/pull/29566), merged September 2026. “Contributing to OpenMetadata since 2021” is supported.

## Public contribution footprint

The user's [commit-search URL](https://github.com/search?q=author%3Aayush-shah+org%3Aopen-metadata&type=commits&ref=advsearch) is useful for browsing but does not distinguish merged feature scope. GitHub's issue/PR search gives this auditable snapshot (2026-09-26):

| Query | Public results | Source |
| --- | ---: | --- |
| Authored PRs in `open-metadata` public repositories | 749 | [GitHub PR search](https://github.com/search?q=is%3Apr+author%3Aayush-shah+org%3Aopen-metadata+is%3Apublic&type=pullrequests), [API query](https://api.github.com/search/issues?q=is%3Apr%20author%3Aayush-shah%20org%3Aopen-metadata%20is%3Apublic&per_page=1) |
| Of those, merged | 672 | [GitHub merged-PR search](https://github.com/search?q=is%3Apr+author%3Aayush-shah+org%3Aopen-metadata+is%3Apublic+is%3Amerged&type=pullrequests), [API query](https://api.github.com/search/issues?q=is%3Apr%20author%3Aayush-shah%20org%3Aopen-metadata%20is%3Apublic%20is%3Amerged&per_page=1) |
| In public `open-metadata/OpenMetadata` alone | 663 authored, 591 merged | [All PRs](https://github.com/search?q=is%3Apr+author%3Aayush-shah+repo%3Aopen-metadata%2FOpenMetadata&type=pullrequests), [merged PRs](https://github.com/search?q=is%3Apr+author%3Aayush-shah+repo%3Aopen-metadata%2FOpenMetadata+is%3Amerged&type=pullrequests) |

Merged public PRs are concentrated in `OpenMetadata` (591), followed by public documentation repositories (`docs-v1-legacy` 26; `docs-om` 22), `openmetadata-demo` (9), and smaller supporting repos. These were counted from the public-only GitHub API query above.

**README guidance:** “Hundreds of merged OpenMetadata pull requests” is durable. If using the exact 672 figure, label it “as of September 2026” and link the public-only query. These are PR counts, not lines of code, active-user impact, or independent project ownership.

## Strong public work to feature

### Connectors and lineage

- **Early dashboard ingestion connectors:** Ayush authored merged connector PRs for [Looker #351](https://github.com/open-metadata/OpenMetadata/pull/351), [Tableau #468](https://github.com/open-metadata/OpenMetadata/pull/468), [Metabase #1726](https://github.com/open-metadata/OpenMetadata/pull/1726), and [Power BI #3019](https://github.com/open-metadata/OpenMetadata/pull/3019). The files changed show Python ingestion source modules for each. The [Metabase PR description](https://github.com/open-metadata/OpenMetadata/pull/1726) specifically covers dashboards, metrics, and lineage between tables and dashboards. Link two or three examples in the README instead of a long product-logo wall.
- **More connector and lineage work:** [AWS Glue ingestion #1124](https://github.com/open-metadata/OpenMetadata/pull/1124), [Superset lineage #2659](https://github.com/open-metadata/OpenMetadata/pull/2659), and [Tableau lineage #2850](https://github.com/open-metadata/OpenMetadata/pull/2850) are merged public examples. Scope these as contributions to the connectors, not sole ownership of each integration's present implementation.

### Ingestion, profiling, and cloud credentials

- **RDS IAM authentication:** [PR #11937](https://github.com/open-metadata/OpenMetadata/pull/11937) added IAM-based authentication for MySQL and PostgreSQL metadata ingestion on AWS RDS. The change spans Python connection code, schema, Java service conversion, tests, and connector docs; it is a strong cross-layer example.
- **Data lake ingestion and profiling:** [PR #13017](https://github.com/open-metadata/OpenMetadata/pull/13017) added `openmetadata.json` manifest support for ingesting files without extensions and improved data lake profiler metrics and array/JSON column handling. Changed files include Python readers for S3, GCS, and ADLS plus Pandas profiler code and tests.
- **Data quality and Databricks:** [PR #14424](https://github.com/open-metadata/OpenMetadata/pull/14424) added data-quality and profiler support for Databricks Unity Catalog. [PR #21612](https://github.com/open-metadata/OpenMetadata/pull/21612) added a Databricks sampler and refactored the Unity Catalog sampler.
- **BigQuery credentials and nested metadata:** [PR #20085](https://github.com/open-metadata/OpenMetadata/pull/20085) improved project-ID discovery and Application Default Credentials, including nested column handling. This supports “BigQuery ingestion” as a work area; avoid a claim of owning the whole connector.

### SDK and service reliability

- **Data contracts:** [PR #26082](https://github.com/open-metadata/OpenMetadata/pull/26082) exposed Python client/SDK methods to retrieve and validate data contracts by entity, validate request/ODCS YAML, parse ODCS YAML, and delete old results. This extends the Python SDK/client surface; the PR does **not** show that Ayush created new server endpoints.
- **Ingestion pipeline validation and migration:** [PR #29566](https://github.com/open-metadata/OpenMetadata/pull/29566) rejects persisted ingestion pipeline source configs without a valid `type`, conservatively repairs identifiable legacy records during a database migration, and makes Python workflow self-registration serialize the discriminator. Changed files span Java repository/migrations, Python ingestion, Playwright fixture, and tests. This is a strong recent example of backend reliability work.
- **SQL query safety:** [PR #24902](https://github.com/open-metadata/OpenMetadata/pull/24902) changed Java `ListFilter` query construction to use parameters and added a SQL injection regression test. Say “improved query safety,” not “secured all of OpenMetadata.”

### Documentation and example catalog

- [OpenMetadata Demo PR #73](https://github.com/open-metadata/openmetadata-demo/pull/73) revamped the public repository into an OpenMetadata **2.0 RC1** example catalog with six Python SDK facade scenarios, API lineage, and CSV update examples. Its PR description explicitly scopes version compatibility and validation. This is a substantial, recent, public example project to link, while noting the RC1 version.
- [docs-om PR #349](https://github.com/open-metadata/docs-om/pull/349) updated the current Python SDK documentation and redirects; [docs-om PR #401](https://github.com/open-metadata/docs-om/pull/401) clarified Context Center MCP coverage; [docs-om PR #382](https://github.com/open-metadata/docs-om/pull/382) expanded the search settings guide. [OpenMetadata PR #30631](https://github.com/open-metadata/OpenMetadata/pull/30631) adjusted the release-branch GitHub Actions workflow to use an app token. These support docs and release engineering as profile themes. Ayush also reports extensive work on Collate documentation; the current `docs-collate` repository was not publicly available at the guessed `open-metadata/docs-collate` path when checked.

## Technologies supported by code

| Area | Evidence | Good README wording |
| --- | --- | --- |
| Python, ingestion frameworks, SDKs | Connector sources in [Looker #351](https://github.com/open-metadata/OpenMetadata/pull/351), data lake/profiler work in [#13017](https://github.com/open-metadata/OpenMetadata/pull/13017), SDK methods in [#26082](https://github.com/open-metadata/OpenMetadata/pull/26082) | “Python · metadata ingestion · SDKs” |
| Java service code, SQL, database migrations | [Parameterized queries #24902](https://github.com/open-metadata/OpenMetadata/pull/24902), [Java repository and MySQL/Postgres migration #29566](https://github.com/open-metadata/OpenMetadata/pull/29566) | “Java services · SQL · migrations” |
| Data quality, profiling, Pandas, SQLAlchemy | [Data lake profiler #13017](https://github.com/open-metadata/OpenMetadata/pull/13017), [Unity Catalog DQ/profiler #14424](https://github.com/open-metadata/OpenMetadata/pull/14424) | “Data quality · profiling” |
| AWS RDS/Glue, GCP BigQuery, Databricks/Unity Catalog | [Glue #1124](https://github.com/open-metadata/OpenMetadata/pull/1124), [RDS IAM #11937](https://github.com/open-metadata/OpenMetadata/pull/11937), [BigQuery #20085](https://github.com/open-metadata/OpenMetadata/pull/20085), [Unity Catalog #14424](https://github.com/open-metadata/OpenMetadata/pull/14424) | “Connectors across AWS, GCP, and Databricks” |
| JavaScript, Node.js, Svelte, Vue/Nuxt | Original [HousieGame-Tambola](https://github.com/ayush-shah/HousieGame-Tambola) uses Svelte, Express, Socket.IO; original [link-shortener](https://github.com/ayush-shah/link-shortener) uses Nuxt/Vue and Express; original [cms-frontend](https://github.com/ayush-shah/cms-frontend) and [cms-backend](https://github.com/ayush-shah/cms-backend) use Svelte, Express, MongoDB/Mongoose | “Earlier side projects: Svelte and Vue/Nuxt with Node.js” |
| GitHub Actions / release workflows | [Release branch workflow #30631](https://github.com/open-metadata/OpenMetadata/pull/30631) and [demo catalog CI in #73](https://github.com/open-metadata/openmetadata-demo/pull/73) | “CI and developer workflows” as a secondary theme |

Do not infer React or TypeScript expertise from the upstream repository's primary language or a Playwright fixture. The Deuex employment and Collate client assignment are based on Ayush's direct clarification, not inferred from the PRs.

## Personal repositories: original work versus forks

The [owner-repositories listing](https://github.com/ayush-shah?tab=repositories) shows 36 public repositories; GitHub API marks 12 as non-forks and 24 as forks at the time of research. Most original projects date from 2019–2023. The strongest candidates are:

| Repository | GitHub `fork` flag | What code supports | README use |
| --- | --- | --- | --- |
| [HousieGame-Tambola](https://github.com/ayush-shah/HousieGame-Tambola) | `false` | [Svelte client](https://github.com/ayush-shah/HousieGame-Tambola/blob/master/src/App.svelte) and [Express/Socket.IO server](https://github.com/ayush-shah/HousieGame-Tambola/blob/master/main.js) implement multiplayer rooms, numbered ticket/game flow, and chat; [README](https://github.com/ayush-shah/HousieGame-Tambola/blob/master/README.md) explains the rules. | Best original side-project link; label as an earlier experiment. Last pushed 2022. |
| [link-shortener](https://github.com/ayush-shah/link-shortener) | `false` | [Nuxt/Vue UI](https://github.com/ayush-shah/link-shortener/blob/master/pages/index.vue) and [Express server](https://github.com/ayush-shah/link-shortener/blob/master/server/index.js) create named URL mappings stored in a JSON file. | Optional earlier full-stack example. Do not imply production deployment or scalable persistence. Last pushed 2023. |
| [cms-frontend](https://github.com/ayush-shah/cms-frontend) + [cms-backend](https://github.com/ayush-shah/cms-backend) | Both `false` | [Svelte routes](https://github.com/ayush-shah/cms-frontend/blob/master/src/App.svelte) for products/login and [Express/Mongoose backend](https://github.com/ayush-shah/cms-backend/blob/master/main.js) for products. | Optional; code is small and READMEs do not document a polished product. Last pushed 2021. |

`ayush-shah/OpenMetadata`, `ayush-shah/openmetadata-demo`, `ayush-shah/docs-v1`, and other mirrored repositories are **forks**. Do not present them as Ayush-created projects. Feature links to merged upstream PRs and upstream public repositories instead. [GitHub's own repository page](https://github.com/ayush-shah/OpenMetadata) labels the OpenMetadata repository as forked from `open-metadata/OpenMetadata`.

## README-safe summary draft

> I'm Ayush Shah, a Solutions Engineer at Deuex working as a Software Engineer with client Collate on OpenMetadata since 2021. Based in Mumbai, I work on metadata ingestion, data governance, lineage, observability, discovery, data quality, Python SDK, backend reliability, and documentation. My public work includes [RDS IAM authentication](https://github.com/open-metadata/OpenMetadata/pull/11937), [data lake profiling](https://github.com/open-metadata/OpenMetadata/pull/13017), [Databricks Unity Catalog quality support](https://github.com/open-metadata/OpenMetadata/pull/14424), and [pipeline validation/migration](https://github.com/open-metadata/OpenMetadata/pull/29566).

This draft is intentionally short; the README can use separate, linked cards for the PR examples.

## Experience added by Ayush (2026-09-27)

Ayush supplied these experience statements directly for the profile. They are self-reported; the linked PRs above document the public contribution examples.

- Okta and SSO integration.
- Deep Snowflake experience; Databricks, BigQuery, data lakes, Redshift, Power BI metadata, and Tableau metadata.
- AWS Secrets Manager, EC2, Application Load Balancer, Glue, RDS, and [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).
- Docker, Kubernetes, and Django.
- Preferred tools: Claude Code, Codex, VS Code, and IntelliJ IDEA.
- Current employer and title: Deuex, Solutions Engineer. Client assignment: Collate, working as a Software Engineer on OpenMetadata since 2021.
- Work areas: data governance, lineage, observability, discovery, Context Center, root cause analysis, debugging, and bug fixes.
- Coordinates five teammates: four in support and one in documentation; contributed extensively to `docs-om` and `docs-collate`.
- GitHub Actions, Java, Dropwizard, OpenSearch, Elasticsearch, and OpenSearch Dashboards.
- Identity integrations with Google, OAuth, and Keycloak in addition to Okta and SSO.
- Metadata integration work with Tableau, Airflow, Fivetran pipelines, Kafka bootstrap servers, Schema Registry, and other sources.
- Ayush provided these contact links: [X](https://x.com/aidevatwork), [LinkedIn](https://www.linkedin.com/in/shahayushp/), [GitHub](https://github.com/ayush-shah), and [DEV.to](https://dev.to/ayushshah).

## Caveats

- GitHub bio/company/location are self-reported and may change. Ayush directly supplied his Deuex employer and title, Collate client role, OpenMetadata tenure, experience, team scope, and contact links. No public email, speaking history, degree, headshot, endorsements, or impact metrics were verified; do not invent them.
- A merged PR proves an accepted contribution at merge time, not exclusive or ongoing ownership of a connector, subsystem, or employer role. Some PRs include generated review summaries; the examples above were checked against merge status and changed file paths.
- The exact PR count is a point-in-time search result. The `is:public` qualifier keeps the count scoped to publicly accessible repositories.
- Original personal repositories are generally older and smaller than the upstream OpenMetadata work. Lead with upstream merged contributions; show one or two original side projects only if a personal-project section helps the design.

## Profile implementation and verification (2026-09-27)

- The profile positions Ayush as a **Backend & Data Platform Engineer** while stating the employment relationship precisely: **Solutions Engineer at Deuex; working as a Software Engineer with client Collate on OpenMetadata since 2021**. The README keeps LinkedIn as the main contact, X lower, and DEV.to off the page until its existing bio is refreshed.
- The desktop banner follows the approved preview composition, including its subtitle and source → ingest → context network. A separate mobile SVG wraps Ayush's name as in the preview. GitHub's supported `<picture>` markup selects the mobile asset; the essential role text remains below the art in Markdown. Brave renders were checked at desktop and 350-pixel mobile widths.
- The two local cards are generated by [the refresh script](./scripts/update_profile_stats.py) and [daily workflow](./.github/workflows/update-profile-stats.yml). The PR card queries public merged PRs in `open-metadata`. The activity heatmap reads only the [publicly visible GitHub contribution calendar](https://github.com/users/ayush-shah/contributions), then counts days with a nonzero contribution level over the previous six calendar months. Failed or incomplete responses leave the existing cards intact; an unchanged activity signature causes no commit. Manual workflow dispatch is available.
- Snapshot on 2026-09-27: **672** merged public PRs and **120 days with contributions** shown in the public calendar from 2026-03-27 through 2026-09-27. The PR number comes from [GitHub search](https://github.com/search?q=is%3Apr+author%3Aayush-shah+org%3Aopen-metadata+is%3Apublic+is%3Amerged&type=pullrequests). The heatmap reflects GitHub's profile contribution rules and can include [anonymized private activity](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference) if that visibility setting is enabled; it must not be described as 120 days of public code or OpenMetadata work.
- All **15** PR links in the rewritten README returned a non-null `merged_at` from GitHub's public pull-request API on 2026-09-27. The linked examples span OpenMetadata, `docs-om`, and `openmetadata-demo`.
