# 3. Generate Schema variants from a data source + manifest

Date: 04/07/2017

## Status

Accepted

## Context

Form variations are tackled through a mixture of routing rules (go here if...), skip conditions (skip this if...) and splitting of schemas into "form types" (e.g. Retail Sales Index (RSI) form types 0102, 0112 are survey runner schemas 1_0102.json and 1_0112.json). Compared to existing surveys Monthly Business Survey (MBS) has a large number of form types which makes splitting and maintaining them by hand too onerous. The Author service is the long term solution but we need something more manageable in the interim for the MBS.

We need a solution that lightens the load of authoring form variations.

## Decision

We will spilt schemas into manifests and blocks and generate the survey runner JSON at build time.

- Each manifest file will represent a form type. A manifest will define the survey metadata, one or more groups and the block ids that each group composes. Manifests will be stored in YAML.

- A block file will define a single survey runner block and the question it contains. Blocks which have different metadata but contain the same question will duplicate the question. Blocks which contain the same question should have the same file name with a suffix that makes identifying potential duplicate/similar questions easy, e.g. for RSI `total-internet-sales-0102`, `total-internet-sales-0112`. Blocks will be stored in YAML.

- The following directory structure will be used

```
data/
  sources/
    blocks/
      rsi/
        introduction-0102.yaml
        introduction-0112.yaml
        summary.yaml
        ...
      mci/
        introduction-0203.yaml
        internet-sales.yaml
        ...
      ...
    manifests/
      rsi/
        0102.manifest.yaml
        0112.manifest.yaml
        ...
      mci/
        0203.manifest.yaml
        0213.manifest.yaml
        ...
      ...
```

- The scripts which aid the build process and other useful tasks will live in the `scripts/` folder.

- The json files produced by the manifests will continue to be tested by the test_schema_validation.py suite.

- This solution is temporary and will be superseded once Author goes live.

## Consequences

Authors will switch from creating a whole schema for each form type to creating a manifest for each form type and any blocks they require.

Block definitions will no longer be duplicated across multiple form variations/types.

Questions do not have a single source of truth. A question can appear in many blocks, where typically the blocks have different routing and/or skip conditions. As questions are embedded in block files they are effectively duplicated. Authors who are updating a question, e.g. a guidance change, will have to bear this in mind. They will have to identify the blocks that contain the question and update each of them.

Authors will need to remember to run the build and the schemas unit test suite (test_schema_validation.py) before they submit a pull request to make sure any changes they have made don't violate Runners schema. If they don't the Travis build will fail.

No impact on survey runner code, it doesn't care where the json comes from as long as it conforms to its schema.
