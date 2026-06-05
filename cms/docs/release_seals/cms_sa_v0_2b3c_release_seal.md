# CMS-SA v0.2b3c Release Seal

Version: v0.2b3c
Name: Root-Anchored Stable Public Sync Repair

Release condition:

- validator writes stable public-sync reports,
- volatile commit hashes omitted from committed reports,
- runtime HEAD/origin/tag checks active,
- v0.2b3c tag exists,
- final public-sync rerun does not dirty the repo.

Non-claim lock: this release seal confirms repository-state governance only.