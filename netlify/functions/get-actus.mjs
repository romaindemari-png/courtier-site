// Lecture publique des actualités (PAS d'auth — palier 1, lecture seule).
// Store SITE-WIDE "content" (getStore, pas getDeployStore), clé "actus" = tableau JSON.
import { getStore } from "@netlify/blobs";

export default async () => {
  let actus = [];
  try {
    const store = getStore("content");
    const data = await store.get("actus", { type: "json" });
    if (Array.isArray(data)) actus = data;
  } catch (e) {
    // clé absente / store vide / erreur lecture → tableau vide, jamais d'erreur 500
    actus = [];
  }

  // Ne renvoyer QUE les brèves publiées
  actus = actus.filter((a) => a && a.publie === true);

  // Tri : épinglées d'abord, puis date décroissante (ISO YYYY-MM-DD se trie lexicalement)
  actus.sort((a, b) => {
    const pa = a.epingle ? 1 : 0, pb = b.epingle ? 1 : 0;
    if (pa !== pb) return pb - pa;
    return String(b.date || "").localeCompare(String(a.date || ""));
  });

  return new Response(JSON.stringify(actus), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=60",
    },
  });
};
