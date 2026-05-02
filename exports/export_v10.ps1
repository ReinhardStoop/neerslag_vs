$ErrorActionPreference = "Stop"

$Notebook = "src\analyse 10 dagen_V10_layout.ipynb"
$OutputBase = "neerslag_rapport_v10"
$ExportDir = "exports"
$Markdown = Join-Path $ExportDir "$OutputBase.md"
$Docx = Join-Path $ExportDir "$OutputBase.docx"
$Pdf = Join-Path $ExportDir "$OutputBase.pdf"

New-Item -ItemType Directory -Force $ExportDir | Out-Null

.\.venv\Scripts\python -m jupyter nbconvert `
  --execute `
  --to markdown `
  --no-input `
  --output-dir $ExportDir `
  --output $OutputBase `
  $Notebook

pandoc $Markdown `
  --from markdown+tex_math_dollars+pipe_tables+raw_tex `
  --metadata-file "$ExportDir\pandoc_metadata.yaml" `
  --resource-path="$ExportDir;$ExportDir\${OutputBase}_files;data;src" `
  --reference-doc "$ExportDir\reference.docx" `
  -o $Docx

pandoc $Markdown `
  --from markdown+tex_math_dollars+pipe_tables+raw_tex `
  --metadata-file "$ExportDir\pandoc_metadata.yaml" `
  --resource-path="$ExportDir;$ExportDir\${OutputBase}_files;data;src" `
  --pdf-engine=xelatex `
  --include-in-header "$ExportDir\preamble.tex" `
  -o $Pdf

Write-Host "Gemaakt:"
Write-Host " - $Docx"
Write-Host " - $Pdf"
