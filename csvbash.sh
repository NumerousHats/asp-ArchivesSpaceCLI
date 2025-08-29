while IFS=',' read -r cid barcode nbarcode indicator profid; do
  uv run containers.py edit $cid --repo 3 --profile $profid
done < <(tail -n +2 new-profiles.csv)  # skips header row
