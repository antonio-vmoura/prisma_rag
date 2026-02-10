from pathlib import Path

# pasta onde estão os .bib
bib_dir = Path("/home/avmoura_linux/Documents/unb/prisma_rag/vm_utils/sistematic_review/bibtex")

# arquivo final
output_file = Path("all_references.bib")

with output_file.open("w", encoding="utf-8") as out:
    for bib_file in sorted(bib_dir.glob("*.bib")):
        with bib_file.open("r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                out.write(content)
                out.write("\n\n")

print(f"Arquivo gerado: {output_file}")