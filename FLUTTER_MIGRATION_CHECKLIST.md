# Flutter Project Migration Checklist

This guide helps you migrate your existing Flutter code from `mobile/` to a new project with the correct Gradle setup.

---

## Phase 1: Prepare for Migration

- [ ] **Backup current project**
  ```bash
  cp -r mobile mobile_backup
  git add -A && git commit -m "Backup mobile project before Gradle migration"
  ```

- [ ] **Review current pubspec.yaml**
  - [ ] Note all dependencies and their versions
  - [ ] Check for custom build configurations
  - [ ] Document any pubspec-level overrides or features

- [ ] **Verify current code structure**
  - [ ] List all files in `lib/`
  - [ ] Check if there are custom `assets/` folders
  - [ ] Look for custom build scripts in `android/` or `ios/`
  - [ ] Identify any Windows/Web/Linux-specific code (if applicable)

---

## Phase 2: Create New Project

- [ ] **Generate fresh Flutter project**
  ```bash
  flutter create -t app mobile_new
  ```

- [ ] **Verify new project builds successfully**
  ```bash
  cd mobile_new
  flutter pub get
  flutter build apk --debug  # Quick validation (or use --analyze-size)
  cd ..
  ```

- [ ] **Check Gradle versions in new project**
  - [ ] Review `mobile_new/android/gradle/wrapper/gradle-wrapper.properties`
  - [ ] Verify `mobile_new/android/build.gradle` structure
  - [ ] Check `mobile_new/pubspec.yaml` has correct Flutter version

---

## Phase 3: Migrate Dart Code

- [ ] **Copy lib/ folder**
  ```bash
  rm -rf mobile_new/lib/*
  cp -r mobile/lib/* mobile_new/lib/
  ```

- [ ] **Review and merge main.dart**
  - [ ] Compare `mobile/lib/main.dart` with `mobile_new/lib/main.dart` template
  - [ ] Ensure Material/Cupertino imports are correct
  - [ ] Keep any custom initialization code from your original

- [ ] **Copy test files** (if present)
  ```bash
  rm -rf mobile_new/test/*
  cp -r mobile/test/* mobile_new/test/
  ```

- [ ] **Verify Dart code compiles**
  ```bash
  cd mobile_new
  flutter analyze
  cd ..
  ```

---

## Phase 4: Update Dependencies

- [ ] **Update pubspec.yaml**
  - [ ] Compare `mobile/pubspec.yaml` with the new `mobile_new/pubspec.yaml`
  - [ ] Copy all custom dependencies to new `pubspec.yaml`
  - [ ] Update dependency versions:
    ```bash
    cd mobile_new
    flutter pub outdated
    flutter pub upgrade
    cd ..
    ```

- [ ] **Test dependency resolution**
  ```bash
  cd mobile_new
  flutter pub get
  flutter pub upgrade --offline  # Validate offline too
  cd ..
  ```

- [ ] **Resolve any conflicts**
  - [ ] Check for SDK version constraints
  - [ ] Verify minimum Flutter version requirements

---

## Phase 5: Migrate Assets and Resources

- [ ] **Copy assets folder**
  ```bash
  mkdir -p mobile_new/assets
  cp -r mobile/assets/* mobile_new/assets/ 2>/dev/null || true
  ```

- [ ] **Verify assets in pubspec.yaml**
  - [ ] Compare `mobile/pubspec.yaml` assets section
  - [ ] Add the same asset declarations to `mobile_new/pubspec.yaml`
  - [ ] Test that assets load correctly

- [ ] **Copy icons/images if separate**
  ```bash
  # If applicable
  cp -r mobile/android/app/src/main/res/* mobile_new/android/app/src/main/res/ 2>/dev/null || true
  ```

---

## Phase 6: Configure Android Build (if needed)

- [ ] **Review package name and app ID**
  - [ ] Check `mobile/android/app/build.gradle` for applicationId
  - [ ] Verify `mobile_new/android/app/build.gradle` has matching or desired ID
  - [ ] Update if necessary (e.g., for release builds)

- [ ] **Copy custom Gradle configurations** (if any)
  - [ ] Check for custom signing configs in `mobile/android/app/build.gradle`
  - [ ] Check for custom build types or flavors
  - [ ] Add to `mobile_new/android/app/build.gradle` if needed

- [ ] **Verify iOS setup** (if building for iOS)
  - [ ] Confirm `mobile_new/ios/` is present and valid
  - [ ] Copy any custom iOS configs from `mobile/ios/` if applicable

---

## Phase 7: Build and Test

- [ ] **Clean and rebuild new project**
  ```bash
  cd mobile_new
  flutter clean
  flutter pub get
  flutter build apk --debug
  # or for iOS:
  # flutter build ios --debug
  cd ..
  ```

- [ ] **Run on emulator/device**
  ```bash
  cd mobile_new
  flutter run
  ```

- [ ] **Verify app functionality**
  - [ ] Check all main features work
  - [ ] Test asset loading
  - [ ] Verify package/plugin integration

---

## Phase 8: Replace Old Project

- [ ] **Remove old mobile folder**
  ```bash
  rm -rf mobile
  mv mobile_new mobile
  ```

- [ ] **Update git**
  ```bash
  git add -A
  git commit -m "Migrate to new Flutter project structure (Gradle fix)"
  ```

- [ ] **Verify GitHub Actions workflow runs**
  - [ ] Push to a test branch
  - [ ] Monitor workflow execution
  - [ ] Confirm APK/artifact builds successfully

---

## Phase 9: Clean Up

- [ ] **Remove backup** (only after confirming everything works)
  ```bash
  rm -rf mobile_backup
  ```

- [ ] **Update documentation**
  - [ ] Update [README.md](README.md) with new Flutter version/setup info
  - [ ] Document any custom build steps

- [ ] **Final verification**
  - [ ] Local build successful: `flutter build apk --release`
  - [ ] Tests pass: `flutter test`
  - [ ] CI/CD pipeline passes

---

## Troubleshooting

### Issue: "Gradle build fails even after migration"
- [ ] Run `flutter doctor -v` to check environment
- [ ] Clear Gradle cache: `cd mobile_new/android && ./gradlew clean && cd ../..`
- [ ] Verify Java version: `java -version` (Should be 11+)

### Issue: "Dependencies conflict after update"
- [ ] Check `pubspec.lock` for conflicting versions
- [ ] Run `flutter pub upgrade --major-versions` cautiously
- [ ] Test incrementally after each dependency update

### Issue: "Assets not loading"
- [ ] Verify asset paths in `pubspec.yaml` are correct
- [ ] Run `flutter pub get` after adding assets
- [ ] Rebuild the app, don't just hot-reload

### Issue: "App crashes on startup"
- [ ] Check `flutter logs` for detailed error messages
- [ ] Verify main() entry point is correct
- [ ] Check for missing plugins or initialization code

---

## Quick Migration Command (All-in-One)

If you're confident, run this after creating `mobile_new`:

```bash
# Copy code, tests, and assets
rm -rf mobile_new/lib/* && cp -r mobile/lib/* mobile_new/lib/
rm -rf mobile_new/test/* && cp -r mobile/test/* mobile_new/test/
mkdir -p mobile_new/assets && cp -r mobile/assets/* mobile_new/assets/ 2>/dev/null || true

# Get dependencies
cd mobile_new && flutter pub get && cd ..

# Build and test
cd mobile_new && flutter build apk --debug && cd ..
```

---

## Rollback Plan

If something goes wrong:
```bash
rm -rf mobile
mv mobile_backup mobile
git reset --hard HEAD~1  # Undo the commit
```

---

**Estimated Time**: 15-30 minutes  
**Difficulty**: Low to Medium  
**Risk**: Low (backup exists)
