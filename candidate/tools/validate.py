#!/usr/bin/env python3
"""Validate a pipeline output pair against the exercise schemas.

Usage:
    python3 tools/validate.py <config.json> <audit_log.json>

Uses the `jsonschema` package if installed; otherwise falls back to a built-in
minimal checker covering the subset of JSON Schema these schemas use
(type, required, enum, properties, items, additionalProperties, $ref into $defs).
Exit code 0 = both valid.
"""
import json
import os
import sys

VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(os.path.dirname(HERE), "schemas")


def _mini_validate(instance, schema, root, path="$"):
    errors = []
    if "$ref" in schema:
        ref = schema["$ref"]
        assert ref.startswith("#/$defs/"), ref
        schema = root["$defs"][ref.split("/")[-1]]
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        ok = any(
            (x == "object" and isinstance(instance, dict))
            or (x == "array" and isinstance(instance, list))
            or (x == "string" and isinstance(instance, str))
            or (x == "integer" and isinstance(instance, int) and not isinstance(instance, bool))
            or (x == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool))
            or (x == "boolean" and isinstance(instance, bool))
            or (x == "null" and instance is None)
            for x in types
        )
        if not ok:
            errors.append(f"{path}: expected type {t}, got {type(instance).__name__}")
            return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")
    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in instance:
                if k not in props:
                    errors.append(f"{path}: unexpected property '{k}'")
        for k, v in instance.items():
            if k in props:
                errors.extend(_mini_validate(v, props[k], root, f"{path}.{k}"))
    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors.extend(_mini_validate(item, schema["items"], root, f"{path}[{i}]"))
    return errors


def validate(instance_path, schema_name):
    with open(os.path.join(SCHEMA_DIR, schema_name)) as f:
        schema = json.load(f)
    with open(instance_path) as f:
        instance = json.load(f)
    try:
        import jsonschema  # type: ignore
        v = jsonschema.Draft202012Validator(schema)
        return [f"$.{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in v.iter_errors(instance)]
    except ImportError:
        return _mini_validate(instance, schema, schema)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    failed = False
    for inst, schema_name in [(sys.argv[1], "ramp_config_schema.json"), (sys.argv[2], "audit_log_schema.json")]:
        errs = validate(inst, schema_name)
        label = os.path.basename(inst)
        if errs:
            failed = True
            print(f"FAIL {label} ({len(errs)} error{'s' if len(errs) != 1 else ''}):")
            for e in errs[:25]:
                print(f"  - {e}")
            if len(errs) > 25:
                print(f"  ... and {len(errs) - 25} more")
        else:
            print(f"OK   {label}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
