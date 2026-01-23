import os
import logging
from openai import OpenAI
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_hotel_sentiment(api_key: str, nom_hotel: str, marque: str, reviews: list[dict]) -> dict:
    if not api_key:
        logger.error("OPENAI_API_KEY is missing")
        raise ValueError("OPENAI_API_KEY is missing")
    
    if not reviews:
        logger.warning("No reviews provided for analysis")
        raise ValueError("Aucun avis fourni pour l'analyse")
    
    client = OpenAI(api_key=api_key)
    
    # Prepare review data
    review_texts = [
        {
            "titre": review["title"],
            "texte": review["text"],
            "note": review["rating"],
            "date_publication": review["published_date"].isoformat(),
            "type_voyage": review["trip_type"] or "Non spécifié"
        }
        for review in reviews
    ]
    
    # Construct prompt in French
    prompt = f"""
Vous êtes un expert en analyse de sentiments pour des hôtels en France. Analysez les données suivantes pour l'hôtel "{nom_hotel}" de la marque "{marque}":

Données des {len(review_texts)} derniers avis :
{review_texts}

Fournissez une réponse structurée en français avec les sections suivantes, marquées clairement avec des en-têtes :
**Note Globale** : Calculez la moyenne des notes des avis (sur 5).
**Analyse des Sentiments** : Pour chaque avis, indiquez si le sentiment est positif, négatif ou neutre, et résumez le sentiment global.
**Insights** : Identifiez les thèmes récurrents (par exemple, points forts comme le service, points faibles comme la propreté).
**Conclusion** : Résumez la performance de l'hôtel et donnez une recommandation.

La réponse doit être claire, concise et en français. Utilisez les en-têtes exacts ci-dessus.
"""
    
    try:
        logger.info(f"Sending request to OpenAI for hotel {nom_hotel} with {len(reviews)} reviews")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Vous êtes un analyste expert en hôtellerie."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse response
        analysis_text = response.choices[0].message.content.strip()
        logger.info(f"Received OpenAI response for {nom_hotel}: {analysis_text[:100]}...")
        
        # Structure the response
        sections = {
            "note_globale": "",
            "analyse_des_sentiments": "",
            "insights": "",
            "conclusion": ""
        }
        
        current_section = None
        for line in analysis_text.split("\n"):
            line = line.strip()
            if line.startswith("**Note Globale**"):
                current_section = "note_globale"
            elif line.startswith("**Analyse des Sentiments**"):
                current_section = "analyse_des_sentiments"
            elif line.startswith("**Insights**"):
                current_section = "insights"
            elif line.startswith("**Conclusion**"):
                current_section = "conclusion"
            elif current_section and line:
                sections[current_section] += line + "\n"
        
        # Check if sections are populated
        if not any(sections.values()):
            logger.warning(f"OpenAI response parsing failed for {nom_hotel}. Raw response: {analysis_text}")
            raise ValueError("Échec de l'analyse de la réponse OpenAI : format inattendu")
        
        return {
            "nom_hotel": nom_hotel,
            "marque": marque,
            "note_globale": sections["note_globale"].strip(),
            "analyse_des_sentiments": sections["analyse_des_sentiments"].strip(),
            "insights": sections["insights"].strip(),
            "conclusion": sections["conclusion"].strip()
        }
    
    except Exception as e:
        logger.error(f"OpenAI API error for {nom_hotel}: {str(e)}")
        raise Exception(f"Erreur lors de l'analyse des sentiments : {str(e)}")