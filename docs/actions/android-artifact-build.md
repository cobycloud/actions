# Android Artifact Build

`actions/android-artifact-build` sets up Java and Gradle, runs an Android build command, and uploads APK or AAB outputs.

## Purpose

- Build Android release artifacts from Gradle projects.
- Support caller-specific setup and Gradle commands.
- Upload APK/AAB outputs for release, signing, or attestation lanes.

## Dependencies

- `actions/setup-java`
- `gradle/actions/setup-gradle`
- Gradle wrapper or Gradle project tooling

## Reusable Workflow

- `.github/workflows/reusable-build-android-artifact.yml`

## Example

```yaml
jobs:
  android:
    uses: cobycloud/actions/.github/workflows/reusable-build-android-artifact.yml@main
    with:
      working-directory: apps/mobile
      gradle-command: ./gradlew bundleRelease
      artifact-path: "**/build/outputs/**/*.aab"
```
