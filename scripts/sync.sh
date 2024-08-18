#!/bin/bash

echo "Current working directory: $(pwd)"
# => Path to the root of the repository
REPO_PATH="."
TEMP_PUBLIC_DIR="tmp-public-repo"              # name of the folder of temporary repo
TEMP_PUBLIC_PATH="$REPO_PATH/$TEMP_PUBLIC_DIR" # Path to temporary directory

# => Make tmp directory
rm -rf "$TEMP_PUBLIC_PATH"    # force delete first if exists
mkdir -p "$TEMP_PUBLIC_PATH"  # recreating

# => Ensuring tmp repo is ignored when publishing to private repo
echo "$TEMP_PUBLIC_DIR/" >> "$TEMP_PUBLIC_PATH/.gitignore"

# ========================= Public Repo Processing =============================
# \( \) is necessary for grouping conditions
# => copy files to be shown in the public repo
find "$REPO_PATH" \
  -name "*.py" \
  ! -path "$REPO_PATH/apps/linkedin_houdini/*.py" \
  ! -path "$REPO_PATH/apps/youtube_viewers.py" \
  ! -path "$REPO_PATH/apps/obfuscatefile.py" \
  ! -path "$REPO_PATH/apps/serve_justice.py" \
  ! -path "$REPO_PATH/netweaver/netweaver.py" \
  ! -path "$REPO_PATH/netweaver/_enhancedwebelement.py" \
  ! -path "$REPO_PATH/netweaver/script.py" \
  -exec cp --parents {} "$TEMP_PUBLIC_PATH" \;
# => copy images to the public repo
find "$REPO_PATH" \( \
  -regex ".*\.\(png\|gif\|jpg\|jpeg\)" \
  -o -name "README.md" \
  -o -name "LICENSE" \
  -o -name ".gitignore" \
  -o -name ".gitmodules" \
  -o -name "requirements.txt" \
  \) \
  -exec cp --parents {} "$TEMP_PUBLIC_PATH" \;
# => copy the entire samples folder to temp public folder
cp -r "$REPO_PATH/samples" "$TEMP_PUBLIC_PATH"

mkdir -p "$TEMP_PUBLIC_PATH/config/templates"
cp -r "$REPO_PATH/config/templates" "$TEMP_PUBLIC_PATH/config"

mkdir -p "$TEMP_PUBLIC_PATH/drivers/chrome"
cp -r "$REPO_PATH/drivers/chrome" "$TEMP_PUBLIC_PATH/drivers"