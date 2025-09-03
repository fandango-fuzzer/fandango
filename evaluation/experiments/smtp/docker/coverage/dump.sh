#!/bin/bash
set -euo pipefail

JACOCO_VERSION="0.8.12"
JACOCO_CLI="jacococli.jar"
JACOCO_URL="https://repo1.maven.org/maven2/org/jacoco/org.jacoco.cli/${JACOCO_VERSION}/org.jacoco.cli-${JACOCO_VERSION}-nodeps.jar"
COVERAGE_DIR="./coverage"
LIBS_DIR="./build/libs"
FAT_JAR="fake-smtp-server.jar"
APP_CLASSES_DIR="./build/classes_only"
SRC_DIR="./src/main/java"
FIRST_DUMP_FILE="${COVERAGE_DIR}/first_dump_time.txt"

# Ensure coverage dir exists
mkdir -p "${COVERAGE_DIR}"
mkdir -p "${APP_CLASSES_DIR}"

# Download jacococli if not present
if [ ! -f "${JACOCO_CLI}" ]; then
  echo "Downloading JaCoCo CLI ${JACOCO_VERSION}..."
  curl -L -o "${JACOCO_CLI}" "${JACOCO_URL}"
fi

# Extract application classes from fat JAR (once)
echo "Extracting application classes from fat JAR..."
rm -rf "${APP_CLASSES_DIR:?}"/*
mkdir -p "${APP_CLASSES_DIR}"
cd "${LIBS_DIR}"
jar -xf "${FAT_JAR}"
cd - > /dev/null
cp -r "${LIBS_DIR}/BOOT-INF/classes/"* "${APP_CLASSES_DIR}/"
rm -r "${LIBS_DIR}/BOOT-INF"
rm -r "${LIBS_DIR}/META-INF"
rm -r "${LIBS_DIR}/org"

echo "Starting high-resolution continuous coverage dump..."
START_TIME=$(date +%s.%N)  # high-resolution timestamp

# Save the first dump time immediately

echo "$START_TIME" > "coverage/first_dump_time.txt"

while true; do
  NOW=$(date +%s.%N)
  ELAPSED=$(awk "BEGIN {print $NOW - $START_TIME}")  # elapsed in seconds with decimals
  ELAPSED_FILENAME=$(awk "BEGIN {printf \"%.3f\", $ELAPSED}")
  CSVFILE="${COVERAGE_DIR}/jacoco_${ELAPSED_FILENAME}s.csv"
  DESTFILE="${COVERAGE_DIR}/jacoco_${ELAPSED_FILENAME}s.exec"

  # Dump coverage from JaCoCo agent
  java -jar "${JACOCO_CLI}" dump \
    --address localhost \
    --port 6300 \
    --destfile "${DESTFILE}"

  # Generate CSV report
  java -jar "${JACOCO_CLI}" report "${DESTFILE}" \
    --classfiles "${APP_CLASSES_DIR}" \
    --sourcefiles "${SRC_DIR}" \
    --csv "${CSVFILE}"

  echo "[$ELAPSED_FILENAME s] CSV coverage report written to ${CSVFILE}"

  sleep 0.333
done