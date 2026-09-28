# GitHub 업로드 경로

ZIP 압축 해제 후 일반 파일을 저장소 루트에 업로드합니다.

- `github_workflows/update_dart.yml` → `.github/workflows/update_dart.yml`
- 나머지 파일/폴더 → 동일 경로

GitHub에서 `.github/workflows`는 숨김 경로이지만 GitHub Actions가 인식하려면 정확히 이 경로여야 합니다.
