#!/usr/bin/env python3
"""Convert CustomResourceDefinitions in a rendered manifest into JSON schemas.

kubeconform never reads CRDs from its input, so a chart shipping both a CRD and
a custom resource of it would have that resource silently skipped for want of a
schema. Writing each CRD's own openAPIV3Schema out to

    <out>/<group>/<kind lowercased>_<version>.json

matches the layout kubeconform expands from
'-schema-location <out>/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json',
so in-house custom resources get validated against the definitions the chart
itself ships, with no network access at all.

Usage: crd2schema.py <rendered-manifests.yaml> <output-dir>
"""
import json
import os
import sys

import yaml

# Kubernetes structural-schema extensions that mean nothing to a JSON Schema
# validator. Unknown keywords are ignored rather than rejected, but dropping
# them keeps the generated schemas honest about what is actually enforced.
_DROP = (
    "x-kubernetes-list-type",
    "x-kubernetes-list-map-keys",
    "x-kubernetes-map-type",
    "x-kubernetes-validations",
    "x-kubernetes-embedded-resource",
    "x-kubernetes-preserve-unknown-fields",
)


def sanitise(node):
    """Strip Kubernetes-specific keywords from a schema fragment."""
    if isinstance(node, list):
        return [sanitise(item) for item in node]
    if not isinstance(node, dict):
        return node

    # An int-or-string field genuinely accepts both. Leaving the declared type
    # in place would fail every manifest that picks the other form.
    if node.get("x-kubernetes-int-or-string"):
        return {"anyOf": [{"type": "integer"}, {"type": "string"}]}

    return {
        key: sanitise(value)
        for key, value in node.items()
        if key not in _DROP and key != "x-kubernetes-int-or-string"
    }


def schema_for(raw):
    """Wrap a CRD's openAPIV3Schema so a whole manifest validates against it.

    Deliberately emits no "$schema" key, matching the shape of the schemas in
    datreeio/CRDs-catalog that kubeconform is known to work with. kubeconform
    compiles with DefaultDraft(Draft4) and its own resource loader, so declaring
    a draft here makes the compiler resolve that meta-schema through a loader
    that only knows kubeconform's own schema locations. Doing so produced a
    schema that compiled but stopped enforcing "type", silently passing a string
    where the CRD declared an integer.
    """
    schema = sanitise(raw)
    schema.setdefault("type", "object")

    # A CRD schema normally describes only spec/status, but the manifest also
    # carries apiVersion/kind/metadata. Without these an additionalProperties
    # of false would reject perfectly valid resources.
    properties = schema.setdefault("properties", {})
    if isinstance(properties, dict):
        properties.setdefault("apiVersion", {"type": "string"})
        properties.setdefault("kind", {"type": "string"})
        properties.setdefault("metadata", {"type": "object"})

    return schema


def versions_of(spec):
    """Yield (version, openAPIV3Schema) pairs for v1 and legacy v1beta1 CRDs."""
    if spec.get("versions"):
        for version in spec["versions"]:
            if not isinstance(version, dict) or not version.get("name"):
                continue
            raw = (version.get("schema") or {}).get("openAPIV3Schema")
            # v1beta1 allowed one spec.validation shared across all versions.
            if raw is None:
                raw = (spec.get("validation") or {}).get("openAPIV3Schema")
            yield version["name"], raw
    elif spec.get("version"):
        yield spec["version"], (spec.get("validation") or {}).get("openAPIV3Schema")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)

    manifests, out_dir = sys.argv[1], sys.argv[2]

    with open(manifests, encoding="utf-8") as handle:
        docs = list(yaml.safe_load_all(handle))

    written = []
    skipped = []

    for doc in docs:
        if not isinstance(doc, dict) or doc.get("kind") != "CustomResourceDefinition":
            continue

        spec = doc.get("spec") or {}
        group = spec.get("group")
        kind = (spec.get("names") or {}).get("kind")
        if not group or not kind:
            continue

        for version, raw in versions_of(spec):
            if raw is None:
                skipped.append(f"{group}/{version} {kind} (no openAPIV3Schema)")
                continue

            group_dir = os.path.join(out_dir, group)
            os.makedirs(group_dir, exist_ok=True)
            # kubeconform lowercases {{.ResourceKind}} when expanding the path.
            path = os.path.join(group_dir, f"{kind.lower()}_{version}.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(schema_for(raw), handle, indent=2)
            written.append(os.path.relpath(path, out_dir).replace(os.sep, "/"))

    if written:
        print(f"generated {len(written)} schema(s) from the chart's own CRDs:")
        for item in sorted(written):
            print(f"  {item}")
    else:
        print("no schemas generated from chart CRDs")

    for item in skipped:
        print(f"  no schema available for {item}")


if __name__ == "__main__":
    main()
