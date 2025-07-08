"""
Self-Improving Learning System for Nexus AI Assistant
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from ..utils.logger import nexus_logger
from ..core.config import config


class LearningDatabase:
    """Manages persistent learning data"""
    
    def __init__(self, db_path: str = "nexus_learning.db"):
        self.db_path = Path(db_path)
        self.logger = nexus_logger
        self.init_database()
    
    def init_database(self):
        """Initialize the learning database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                user_feedback INTEGER, -- 1: positive, 0: neutral, -1: negative
                context_quality REAL,
                response_time REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Knowledge patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Learning insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                insight_data TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                validation_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_conversation(self, user_input: str, assistant_response: str, 
                          user_feedback: Optional[int] = None,
                          context_quality: Optional[float] = None,
                          response_time: Optional[float] = None):
        """Store conversation for learning analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations 
            (user_input, assistant_response, user_feedback, context_quality, response_time)
            VALUES (?, ?, ?, ?, ?)
        """, (user_input, assistant_response, user_feedback, context_quality, response_time))
        
        conn.commit()
        conn.close()
    
    def store_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Store learned patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO knowledge_patterns 
            (pattern_type, pattern_data, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (pattern_type, json.dumps(pattern_data)))
        
        conn.commit()
        conn.close()
    
    def get_patterns(self, pattern_type: str) -> List[Dict[str, Any]]:
        """Retrieve patterns by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT pattern_data, success_rate, usage_count 
            FROM knowledge_patterns 
            WHERE pattern_type = ?
            ORDER BY success_rate DESC
        """, (pattern_type,))
        
        results = []
        for row in cursor.fetchall():
            pattern_data = json.loads(row[0])
            pattern_data['success_rate'] = row[1]
            pattern_data['usage_count'] = row[2]
            results.append(pattern_data)
        
        conn.close()
        return results


class SelfImprovementEngine:
    """Core engine for self-improvement and learning"""
    
    def __init__(self):
        self.db = LearningDatabase()
        self.logger = nexus_logger
        self.learning_patterns = {}
        self.adaptation_rules = {}
        self.load_learning_patterns()
    
    def load_learning_patterns(self):
        """Load existing learning patterns from database"""
        pattern_types = ['response_quality', 'topic_expertise', 'user_preferences', 'conversation_flow']
        
        for pattern_type in pattern_types:
            patterns = self.db.get_patterns(pattern_type)
            self.learning_patterns[pattern_type] = patterns
    
    def analyze_conversation_quality(self, user_input: str, assistant_response: str) -> Dict[str, float]:
        """Analyze the quality of a conversation"""
        analysis = {
            'relevance_score': 0.0,
            'completeness_score': 0.0,
            'clarity_score': 0.0,
            'engagement_score': 0.0,
            'technical_accuracy': 0.0
        }
        
        # Simple heuristic analysis (can be enhanced with ML models)
        user_length = len(user_input.split())
        response_length = len(assistant_response.split())
        
        # Relevance: Basic keyword matching
        user_keywords = set(user_input.lower().split())
        response_keywords = set(assistant_response.lower().split())
        keyword_overlap = len(user_keywords & response_keywords)
        analysis['relevance_score'] = min(1.0, keyword_overlap / max(len(user_keywords), 1))
        
        # Completeness: Response length relative to question complexity
        analysis['completeness_score'] = min(1.0, response_length / max(user_length * 2, 10))
        
        # Clarity: Sentence structure and readability
        sentences = assistant_response.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        analysis['clarity_score'] = max(0.0, 1.0 - (avg_sentence_length - 15) / 20)
        
        # Engagement: Presence of questions, examples, or creative elements
        engagement_markers = ['?', 'example', 'imagine', 'consider', 'let me', 'here\'s']
        engagement_count = sum(1 for marker in engagement_markers if marker in assistant_response.lower())
        analysis['engagement_score'] = min(1.0, engagement_count / 3)
        
        # Technical accuracy: Presence of specific technical terms when appropriate
        technical_terms = ['function', 'algorithm', 'data', 'system', 'process', 'method']
        tech_question = any(term in user_input.lower() for term in technical_terms)
        tech_response = any(term in assistant_response.lower() for term in technical_terms)
        analysis['technical_accuracy'] = 1.0 if (tech_question and tech_response) or not tech_question else 0.5
        
        return analysis
    
    def extract_conversation_insights(self, user_input: str, assistant_response: str) -> Dict[str, Any]:
        """Extract learning insights from conversation"""
        insights = {
            'topics': [],
            'user_intent': '',
            'response_style': '',
            'improvement_suggestions': []
        }
        
        # Topic extraction (simple keyword-based)
        topics = []
        topic_keywords = {
            'programming': ['code', 'function', 'python', 'javascript', 'algorithm', 'debug'],
            'science': ['research', 'experiment', 'hypothesis', 'data', 'analysis'],
            'creative': ['write', 'poem', 'story', 'creative', 'art', 'design'],
            'technical': ['system', 'network', 'server', 'database', 'API'],
            'learning': ['learn', 'understand', 'explain', 'teach', 'how']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                topics.append(topic)
        
        insights['topics'] = topics
        
        # User intent analysis
        if '?' in user_input:
            insights['user_intent'] = 'question'
        elif any(word in user_input.lower() for word in ['help', 'assist', 'support']):
            insights['user_intent'] = 'help_request'
        elif any(word in user_input.lower() for word in ['create', 'make', 'build']):
            insights['user_intent'] = 'creation_request'
        else:
            insights['user_intent'] = 'general_interaction'
        
        # Response style analysis
        if len(assistant_response) > 200:
            insights['response_style'] = 'detailed'
        elif '```' in assistant_response:
            insights['response_style'] = 'code_focused'
        elif any(char in assistant_response for char in ['!', '?', '...']):
            insights['response_style'] = 'conversational'
        else:
            insights['response_style'] = 'concise'
        
        return insights
    
    def generate_improvement_suggestions(self, analysis: Dict[str, float], 
                                       insights: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improvement"""
        suggestions = []
        
        if analysis['relevance_score'] < 0.6:
            suggestions.append("Improve response relevance by focusing more on user keywords")
        
        if analysis['completeness_score'] < 0.5:
            suggestions.append("Provide more comprehensive answers")
        
        if analysis['clarity_score'] < 0.6:
            suggestions.append("Use simpler sentence structures for better clarity")
        
        if analysis['engagement_score'] < 0.4:
            suggestions.append("Add more engaging elements like examples or questions")
        
        if insights['user_intent'] == 'question' and '?' not in insights.get('last_response', ''):
            suggestions.append("Consider asking clarifying questions for better understanding")
        
        return suggestions
    
    def learn_from_feedback(self, user_input: str, assistant_response: str, 
                          feedback: int, context: Dict[str, Any] = None):
        """Learn from user feedback"""
        # Analyze conversation quality
        analysis = self.analyze_conversation_quality(user_input, assistant_response)
        insights = self.extract_conversation_insights(user_input, assistant_response)
        
        # Calculate overall quality score
        quality_score = sum(analysis.values()) / len(analysis)
        
        # Store conversation with feedback
        self.db.store_conversation(
            user_input=user_input,
            assistant_response=assistant_response,
            user_feedback=feedback,
            context_quality=quality_score,
            response_time=context.get('response_time', 0) if context else 0
        )
        
        # Update learning patterns based on feedback
        self.update_learning_patterns(insights, feedback, quality_score)
        
        # Generate improvement suggestions
        suggestions = self.generate_improvement_suggestions(analysis, insights)
        
        self.logger.info(f"Learning from feedback: {feedback}, Quality: {quality_score:.2f}")
        if suggestions:
            self.logger.info(f"Improvement suggestions: {suggestions}")
        
        return {
            'quality_analysis': analysis,
            'insights': insights,
            'suggestions': suggestions,
            'overall_quality': quality_score
        }
    
    def update_learning_patterns(self, insights: Dict[str, Any], 
                               feedback: int, quality_score: float):
        """Update learning patterns based on new data"""
        # Update topic expertise patterns
        for topic in insights['topics']:
            pattern_data = {
                'topic': topic,
                'feedback': feedback,
                'quality_score': quality_score,
                'response_style': insights['response_style']
            }
            self.db.store_pattern('topic_expertise', pattern_data)
        
        # Update response style patterns
        style_pattern = {
            'style': insights['response_style'],
            'intent': insights['user_intent'],
            'feedback': feedback,
            'quality_score': quality_score
        }
        self.db.store_pattern('response_quality', style_pattern)
    
    def get_adaptive_prompt_enhancement(self, user_input: str, 
                                      base_prompt: str) -> str:
        """Enhance the system prompt based on learned patterns"""
        # Get relevant patterns
        topic_patterns = self.db.get_patterns('topic_expertise')
        style_patterns = self.db.get_patterns('response_quality')
        
        # Analyze user input to determine relevant enhancements
        user_topics = []
        topic_keywords = {
            'programming': ['code', 'function', 'python', 'javascript', 'algorithm'],
            'science': ['research', 'experiment', 'data', 'analysis'],
            'creative': ['write', 'poem', 'story', 'creative', 'art'],
            'technical': ['system', 'network', 'server', 'database']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                user_topics.append(topic)
        
        # Build enhancement based on successful patterns
        enhancement = "\n\nLearned Adaptations:\n"
        
        # Add topic-specific enhancements
        for topic in user_topics:
            relevant_patterns = [p for p in topic_patterns if p.get('topic') == topic and p.get('success_rate', 0) > 0.7]
            if relevant_patterns:
                best_pattern = max(relevant_patterns, key=lambda x: x.get('success_rate', 0))
                enhancement += f"- For {topic} topics: Use {best_pattern.get('response_style', 'detailed')} style\n"
        
        # Add general style enhancements
        successful_styles = [p for p in style_patterns if p.get('success_rate', 0) > 0.7]
        if successful_styles:
            best_style = max(successful_styles, key=lambda x: x.get('success_rate', 0))
            enhancement += f"- Preferred response style: {best_style.get('style', 'conversational')}\n"
        
        return base_prompt + enhancement
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning and improvement statistics"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Get conversation statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_conversations,
                AVG(CASE WHEN user_feedback = 1 THEN 1.0 ELSE 0.0 END) as positive_feedback_rate,
                AVG(context_quality) as avg_quality,
                AVG(response_time) as avg_response_time
            FROM conversations
        """)
        
        stats = cursor.fetchone()
        
        # Get learning pattern counts
        cursor.execute("SELECT pattern_type, COUNT(*) FROM knowledge_patterns GROUP BY pattern_type")
        pattern_counts = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_conversations': stats[0] if stats[0] else 0,
            'positive_feedback_rate': stats[1] if stats[1] else 0.0,
            'avg_quality_score': stats[2] if stats[2] else 0.0,
            'avg_response_time': stats[3] if stats[3] else 0.0,
            'learned_patterns': pattern_counts
        }
