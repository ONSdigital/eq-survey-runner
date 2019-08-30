if grep -Er "@watch|@focus|\.only" tests/functional/spec; then
    exit 1
else
    # No watch statements found
    exit 0
fi
