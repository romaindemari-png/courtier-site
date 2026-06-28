// Écriture des actualités — Identity-gated (PALIER 2b). Handler v1 (context.clientContext.user).
// Reçoit le TABLEAU COMPLET, le valide côté serveur, écrit en bloc (last-write-wins, éditeur unique).
import { connectLambda, getStore } from "@netlify/blobs";

const TYPES = ["intervention", "publication", "media", "decision"];
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const URL_RE = /^https?:\/\/[^\s]+$/i;

export function clean(arr) {  // exportée pour les tests unitaires (Netlify n'utilise que `handler`)
  if (!Array.isArray(arr)) return { error: "Le contenu doit être un tableau de brèves." };
  const out = [];
  for (let i = 0; i < arr.length; i++) {
    const b = arr[i] || {};
    const pos = i + 1;
    const titre = typeof b.titre === "string" ? b.titre.trim() : "";
    const corps = typeof b.corps === "string" ? b.corps.trim() : "";
    const lien = typeof b.lien === "string" ? b.lien.trim() : "";

    if (!TYPES.includes(b.type)) return { error: `Type invalide (brève ${pos}).` };
    if (!titre) return { error: `Titre obligatoire (brève ${pos}).` };
    if (titre.length > 140) return { error: `Titre trop long (brève ${pos}, max 140 caractères).` };
    if (corps.length > 600) return { error: `Corps trop long (brève ${pos}, max 600 caractères).` };
    if (typeof b.date !== "string" || !DATE_RE.test(b.date)) return { error: `Date invalide (brève ${pos}, format AAAA-MM-JJ).` };
    if (lien && !URL_RE.test(lien)) return { error: `Lien invalide (brève ${pos}, http/https requis).` };

    out.push({
      id: (b.id !== undefined && b.id !== null && String(b.id)) || `${Date.now()}-${i}`, // généré si absent, conservé sinon
      date: b.date,
      type: b.type,
      titre,
      corps,
      lien,
      epingle: !!b.epingle,
      publie: !!b.publie,
    });
  }
  return { value: out };
}

export const handler = async (event, context) => {
  // Les Functions v1 (handler classique) ne reçoivent PAS le contexte Blobs auto-injecté
  // (contrairement aux v2 `export default`). connectLambda(event) l'extrait de l'event
  // → getStore("content") fonctionne ensuite en lecture ET écriture (sinon MissingBlobsEnvironmentError).
  connectLambda(event);
  const user = context.clientContext && context.clientContext.user;
  if (!user) {
    return { statusCode: 401, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "Unauthorized" }) };
  }
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers: { "Content-Type": "application/json", Allow: "POST" }, body: JSON.stringify({ error: "Méthode non autorisée." }) };
  }

  let payload;
  try { payload = JSON.parse(event.body || "null"); }
  catch (e) { return { statusCode: 400, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "JSON invalide." }) }; }

  const { value, error } = clean(payload);
  if (error) {
    return { statusCode: 400, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error }) };
  }

  try {
    const store = getStore("content");
    await store.setJSON("actus", value);
  } catch (e) {
    return { statusCode: 500, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "Écriture impossible." }) };
  }

  // On renvoie le tableau nettoyé exact qui vient d'être écrit : le client met sa liste à
  // jour avec ÇA (source de vérité = écriture confirmée), sans dépendre d'une relecture eventual.
  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
    body: JSON.stringify({ ok: true, count: value.length, actus: value }),
  };
};
