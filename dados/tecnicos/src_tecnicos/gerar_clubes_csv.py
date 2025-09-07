
import pandas as pd
from pathlib import Path

def normalizar_para_slug(nome: str) -> str:
    import re, unicodedata
    s = unicodedata.normalize("NFKD", nome)
    s = "".join([c for c in s if not unicodedata.combining(c)])
    s = s.replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_]", "", s)
    return s

def sugestao_wiki_treinadores(clube: str) -> str:
    slug = normalizar_para_slug(clube)
    bases = [
        f"https://pt.wikipedia.org/wiki/Treinadores_do_{slug}",
        f"https://pt.wikipedia.org/wiki/Treinadores_da_{slug}",
        f"https://pt.wikipedia.org/wiki/Treinadores_de_{slug}",
    ]
    return " | ".join(bases)

def construir_clubes_csv(
    path_a=(
        r"dados\times\serie_a"
        r"\clubes_serie_a_2018_2025.csv"
    ),
    path_b=(
        r"dados\times\serie_b"
        r"\clubes_serie_b_2018_2025.csv"
    ),
    saida=r"dados\times\clubes_consolidados\clubes.csv"
):
    
    pa, pb = Path(path_a), Path(path_b)
    if not pa.exists() or not pb.exists():
        raise SystemExit("Arquivos dos times não encontrados. Rode os notebooks de clubes (A e B) primeiro.")
    da = pd.read_csv(pa)
    db = pd.read_csv(pb)
    unificados = pd.concat([da, db], ignore_index=True).drop_duplicates()
    clubes_unicos = sorted(unificados["clube"].dropna().unique())

    linhas = []
    for clube in clubes_unicos:
        linhas.append({
            "clube": clube,
            "wiki_pt_url": "",            # deixar vazio para curadoria manual
            "transfermarkt_url": "",      # idem
            "ogol_url": "",               # idem
            "sugestao_wikipedia": sugestao_wiki_treinadores(clube)
        })

    df_out = pd.DataFrame(linhas, columns=["clube","wiki_pt_url","transfermarkt_url","ogol_url","sugestao_wikipedia"])
    df_out.to_csv(saida, index=False, encoding="utf-8")
    print(f"Gerado {saida} com {len(df_out)} clubes. Preencha as URLs conforme necessário.")
    return df_out

if __name__ == "__main__":
    construir_clubes_csv()
