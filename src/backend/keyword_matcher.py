import re
import spacy
from typing import List, Dict, Any, Optional

class AdvancedKeywordMatcher:
    """
    Advanced keyword matching algorithm with semantic understanding and 
    configurable matching strategies.
    """
    def __init__(self, language_model: str = 'es_core_news_md'):
        """
        Initialize the matcher with a spaCy language model.

        :param language_model: Spacy language model to use
        """
        try:
            self.nlp = spacy.load(language_model)
        except OSError:
            print(f"Language model {language_model} not found. Downloading...")
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "spacy", "download", language_model], check=True)
            self.nlp = spacy.load(language_model)

        # Predefined synonym and semantic mapping
        self.semantic_mapping = {
            'ventas': ['comercial', 'comercialización', 'account executive', 'representante', 'vendedor'],
            'tecnología': ['tech', 'it', 'software', 'tecnologico', 'digital'],
            'experiencia': ['años', 'trayectoria', 'carrera', 'background'],
            'b2b': ['business to business', 'empresa a empresa', 'inter-empresarial']
        }

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for matching: lowercase, remove punctuation.

        :param text: Input text
        :return: Preprocessed text
        """
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text

    def _extract_semantic_keywords(self, text: str) -> List[str]:
        """
        Extract semantically meaningful keywords using spaCy.

        :param text: Input text
        :return: List of semantic keywords
        """
        doc = self.nlp(text)
        
        # Extract nouns, proper nouns, and verbs
        semantic_keywords = [
            token.lemma_ 
            for token in doc 
            if token.pos_ in ['NOUN', 'PROPN', 'VERB'] 
            and len(token.lemma_) > 2
        ]
        
        return list(set(semantic_keywords))

    def _expand_keywords(self, keywords: List[str]) -> List[str]:
        """
        Expand keywords using predefined semantic mapping.

        :param keywords: Original keywords
        :return: Expanded list of keywords
        """
        expanded_keywords = set(keywords)
        
        for keyword in keywords:
            for key, synonyms in self.semantic_mapping.items():
                if keyword in synonyms or key == keyword:
                    expanded_keywords.update(synonyms)
        
        return list(expanded_keywords)

    def match_job_description(
        self, 
        cv_text: str, 
        job_description: str, 
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Advanced semantic matching between CV and job description.

        :param cv_text: Candidate's CV text
        :param job_description: Job description text
        :param threshold: Matching threshold (0-1)
        :return: Matching result dictionary
        """
        # Preprocess texts
        cv_processed = self._preprocess_text(cv_text)
        job_desc_processed = self._preprocess_text(job_description)

        # Extract semantic keywords
        cv_keywords = self._extract_semantic_keywords(cv_processed)
        job_keywords = self._extract_semantic_keywords(job_desc_processed)

        # Expand keywords
        cv_keywords_expanded = self._expand_keywords(cv_keywords)
        job_keywords_expanded = self._expand_keywords(job_keywords)

        # Calculate matching score
        matches = set(cv_keywords_expanded) & set(job_keywords_expanded)
        total_keywords = set(job_keywords_expanded)
        
        match_percentage = len(matches) / len(total_keywords) if total_keywords else 0
        match_percentage = min(match_percentage * 100, 100)  # Convert to percentage, cap at 100

        # Determine suitability
        is_suitable = match_percentage >= (threshold * 100)

        return {
            'puntuacion': int(match_percentage),
            'apto': 'SI' if is_suitable else 'NO',
            'motivo': f"Semantic match based on {len(matches)} keywords out of {len(total_keywords)} job requirements",
            'matched_keywords': list(matches)
        }

    def add_custom_semantic_mapping(self, key: str, synonyms: List[str]):
        """
        Allow dynamic addition of semantic mappings.

        :param key: Primary keyword
        :param synonyms: List of synonyms
        """
        self.semantic_mapping[key] = synonyms