/* ==============================================
   AI Mentor - Curriculum Data
   7 subjects × 8-11 subtopics each
   ============================================== */

const CURRICULUM = {
    python: {
        name: "Python Programming",
        icon: "🐍",
        color: "#3B82F6",
        subtopics: [
            "syntax_and_data_types", "control_flow", "functions_and_scope",
            "data_structures", "oop", "file_handling",
            "error_handling", "modules_and_packages", "decorators_and_generators",
            "comprehensions_and_lambdas", "real_world_projects"
        ]
    },
    mysql: {
        name: "MySQL & SQL",
        icon: "🗄️",
        color: "#06B6D4",
        subtopics: [
            "basic_queries", "filtering_and_sorting", "joins",
            "aggregation_and_grouping", "subqueries", "indexes_and_optimization",
            "stored_procedures", "window_functions", "cte_and_views",
            "database_design"
        ]
    },
    ml: {
        name: "Machine Learning",
        icon: "🤖",
        color: "#10B981",
        subtopics: [
            "supervised_learning_basics", "linear_regression", "classification",
            "decision_trees_and_forests", "svm_and_knn", "clustering",
            "feature_engineering", "model_evaluation", "ensemble_methods",
            "ml_pipelines"
        ]
    },
    dl: {
        name: "Deep Learning",
        icon: "🧠",
        color: "#8B5CF6",
        subtopics: [
            "neural_network_basics", "activation_and_loss_functions",
            "backpropagation", "cnn", "rnn_and_lstm",
            "regularization_and_optimization", "transfer_learning",
            "autoencoders", "transformers_architecture"
        ]
    },
    nlp: {
        name: "Natural Language Processing",
        icon: "💬",
        color: "#EC4899",
        subtopics: [
            "text_preprocessing", "tokenization_and_embeddings",
            "bag_of_words_tfidf", "sentiment_analysis", "ner_and_pos",
            "seq2seq_models", "attention_mechanism", "transformers_for_nlp",
            "nlp_projects"
        ]
    },
    genai: {
        name: "Generative AI",
        icon: "✨",
        color: "#F59E0B",
        subtopics: [
            "llm_fundamentals", "prompt_engineering", "rag_basics",
            "vector_databases", "langchain_basics", "fine_tuning",
            "multimodal_ai", "ai_safety_and_ethics", "genai_app_design"
        ]
    },
    agentic: {
        name: "Agentic AI",
        icon: "🤝",
        color: "#EF4444",
        subtopics: [
            "agent_fundamentals", "tool_use_and_function_calling",
            "react_pattern", "memory_systems", "planning_and_reasoning",
            "multi_agent_systems", "human_in_the_loop", "agent_evaluation",
            "agent_frameworks", "production_agents"
        ]
    }
};

const TOPIC_LIST = Object.keys(CURRICULUM);

function getTopicName(slug) {
    return CURRICULUM[slug]?.name || slug.replace(/_/g, ' ');
}

function getSubtopicName(slug) {
    return slug.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function getTopicIcon(slug) {
    return CURRICULUM[slug]?.icon || '📖';
}

function getTopicColor(slug) {
    return CURRICULUM[slug]?.color || '#6366F1';
}
