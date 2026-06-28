// Lecture ADMIN des actualités — Identity-gated (PALIER 2a : LECTURE SEULE).
// Handler v1 OBLIGATOIRE : context.clientContext.user n'est peuplé qu'en v1 (signature event/context).
import { connectLambda, getStore } from "@netlify/blobs";

export const handler = async (event, context) => {
  // Les Functions v1 (handler classique) ne reçoivent PAS le contexte Blobs auto-injecté
  // (contrairement aux v2 `export default`). connectLambda(event) l'extrait de l'event
  // → getStore("content") fonctionne ensuite en lecture ET écriture (sinon MissingBlobsEnvironmentError).
  connectLambda(event);
  // Garde d'authentification : sans utilisateur Identity validé → 401, aucune donnée.
  const user = context.clientContext && context.clientContext.user;
  if (!user) {
    return { statusCode: 401, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "Unauthorized" }) };
  }

  // Écriture (POST/PUT/DELETE) → palier 2b. Non implémentée ici.
  if (event.httpMethod !== "GET") {
    return { statusCode: 501, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "Not implemented (palier 2b)" }) };
  }

  // GET (loggé) → tableau COMPLET, brouillons inclus, AUCUN filtrage (vue admin).
  let actus = [];
  try {
    const store = getStore("content");
    const data = await store.get("actus", { type: "json" });
    if (Array.isArray(data)) actus = data;
  } catch (e) {
    actus = []; // clé absente / store vide
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
    body: JSON.stringify(actus),
  };
};
