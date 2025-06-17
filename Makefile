# Makefile for registry-core/
# Assumes maven_parser.py is in registry-core/maven_parser/
# and pom.xml is in registry-core/

.PHONY: dep dep-jsonld dep-turtle

dep: dep-jsonld dep-turtle

dep-jsonld: target/dependencies.txt
	python3 maven_parser/maven_parser.py --depfile target/dependencies.txt --format jsonld --output maven_dependencies

dep-turtle: target/dependencies.txt
	python3 maven_parser/maven_parser.py --depfile target/dependencies.txt --format turtle --output maven_dependencies

target/dependencies.txt:
	mvn dependency:tree -DoutputFile=target/dependencies.txt