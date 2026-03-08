# How to Contribute to dbdemos

Source: https://databricks.atlassian.net/wiki/spaces/HUB/pages/5034082566/How+to+Contribute+to+dbdemos

## Repos

1. **dbdemos** (https://github.com/databricks-demos/dbdemos) — packaging project, what customers `pip install`
2. **dbdemos-notebooks** (https://github.com/databricks-demos/dbdemos-notebooks) — the actual demo notebooks (primary contribution target)
3. **dbdemos-resources** (https://github.com/databricks-demos/dbdemos-resources) — static image assets (GIFs, images, icons)
4. **dbdemos-dataset** (https://github.com/databricks-demos/dbdemos-dataset) — datasets published with demos (bronze/raw tables, syncs to public S3)

## Prerequisites

1. GitHub Account (non-Databricks email) — all repos are public/open source
2. FE-IP JIRA ticket assigned to yourself — tracks contributions for PERF
3. Demo Review Document (template: https://docs.google.com/document/d/1idHpQKXPyjOqHbhSg1UDpmshiqOzDZT1cFiedsWXHKY/edit)

## Steps

1. Fork `dbdemos-notebooks`
2. Clone forked repo into Databricks Workspace (new branch recommended)
3. Make changes:
   - Industry demos → relevant industry folder
   - Product demos → `product_demos/` subfolder
4. (Optional) Fork `dbdemos-resources` for images, `dbdemos-dataset` for datasets
5. Submit PR
6. Maintainer reviews and reaches out

## Demo Ideas

Submit as a ticket at go/feip/board
