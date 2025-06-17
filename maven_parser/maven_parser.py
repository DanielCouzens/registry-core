#!/usr/bin/env python3
import json
import argparse
import re
import os

def parse_maven_dependencies(file_path="../target/dependencies.txt"):
    dependencies = []
    # Regular expression to remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Remove ANSI escape codes from the line
                clean_line = ansi_escape.sub('', line)
                match = re.match(r'\s*([^:]+):([^:]+):[^:]+:([^:]+):([^:]+)', clean_line)
                if match:
                    group_id, artifact_id, version, scope = match.groups()
                    dependencies.append({
                        'groupId': group_id,
                        'artifactId': artifact_id,
                        'version': version,
                        'scope': scope
                    })
    else:
        print(f"Error: Dependencies file not found at {file_path}")

    return dependencies

def generate_jsonld(maven_deps):
    jsonld = {
        "@context": "https://schema.org",
        "@graph": []
    }

    for dep in maven_deps:
        jsonld["@graph"].append({
            "@type": "SoftwareApplication",
            "name": f"{dep['groupId']}:{dep['artifactId']}",
            "version": dep['version'],
            "description": f"Maven dependency from pom.xml with scope {dep['scope']}"
        })

    return jsonld

def generate_turtle(maven_deps):
    turtle = "@prefix schema: <https://schema.org/> .\n\n"

    for dep in maven_deps:
        safe_id = f"{dep['groupId'].replace('.', '_')}_{dep['artifactId']}"
        turtle += f"""<urn:maven:{safe_id}> a schema:SoftwareApplication ;
    schema:name "{dep['groupId']}:{dep['artifactId']}" ;
    schema:version "{dep['version']}" ;
    schema:description "Maven dependency from pom.xml with scope {dep['scope']}" .\n\n"""

    return turtle

def main():
    parser = argparse.ArgumentParser(description="Generate Maven dependency information")
    parser.add_argument("--depfile", default="../target/dependencies.txt", help="Path to Maven dependencies file")
    parser.add_argument("--format", choices=["jsonld", "turtle"], default="jsonld", help="Output format")
    parser.add_argument("--output", default="../maven_dependencies", help="Output file prefix")
    args = parser.parse_args()

    maven_deps = parse_maven_dependencies(args.depfile)

    if args.format == "jsonld":
        jsonld = generate_jsonld(maven_deps)
        with open(f"{args.output}.jsonld", "w") as f:
            json.dump(jsonld, f, indent=2)
        print(f"Maven dependencies written to {args.output}.jsonld")
    else:
        turtle = generate_turtle(maven_deps)
        with open(f"{args.output}.ttl", "w") as f:
            f.write(turtle)
        print(f"Maven dependencies written to {args.output}.ttl")

if __name__ == "__main__":
    main()