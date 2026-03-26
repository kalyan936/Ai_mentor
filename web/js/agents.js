/* ==============================================
   AI Mentor - AI Agent Implementations
   6 Specialized Agents with structured prompts
   ============================================== */

const Agents = {

    // ── PLANNER AGENT ──
    async generateRoadmap(topic, level, goals) {
        const subtopics = CURRICULUM[topic]?.subtopics || [];
        const prompt = `You are an expert learning path planner. Create a structured learning roadmap.

Topic: ${getTopicName(topic)}
Current Level: ${level}
Learner Goals: ${goals || 'Master the topic'}
Available Subtopics: ${subtopics.join(', ')}

Return a JSON object with this EXACT structure:
{
    "title": "Roadmap title",
    "estimated_weeks": 4,
    "modules": [
        {
            "module_id": 1,
            "title": "Module title",
            "description": "What the learner will master",
            "subtopics": ["subtopic_slug_1", "subtopic_slug_2"],
            "difficulty": "beginner",
            "estimated_hours": 3,
            "status": "available"
        }
    ],
    "tips": ["Study tip 1", "Study tip 2"]
}

Create 4-6 progressive modules using ONLY the subtopics from the Available Subtopics list. First module status should be "available", rest "locked".`;

        return callAgent(prompt, `Generate a ${level}-level roadmap for ${getTopicName(topic)}. Goals: ${goals || 'Complete mastery'}`);
    },

    // ── TUTOR AGENT ──
    async teachLesson(topic, subtopic, level) {
        const prompt = `You are the world's best AI tutor. Teach this topic in a clear, engaging way.
Adapt your teaching to a ${level} level learner.

IMPORTANT: Return ONLY a JSON object with this structure:
{
    "title": "Lesson title",
    "content": "Full lesson content in markdown format with headers, code blocks, examples, and explanations. Make it detailed (500+ words). Use ## for sections, \`\`\`python for code, **bold** for key terms.",
    "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"],
    "practice_tasks": ["Task 1 description", "Task 2 description"],
    "next_topic": "Suggested next topic"
}`;

        return callAgent(prompt, `Teach me about "${getSubtopicName(subtopic)}" in ${getTopicName(topic)}. I am a ${level} learner. Give a comprehensive lesson with real code examples.`);
    },

    // ── TUTOR CHAT ──
    async chatWithTutor(message, topic, subtopic, chatContext) {
        const contextStr = chatContext ? `\nRecent chat context:\n${chatContext}` : '';
        const prompt = `You are a friendly, adaptive AI tutor specializing in ${getTopicName(topic || 'programming')}.
${subtopic ? `Current subtopic: ${getSubtopicName(subtopic)}` : ''}
${contextStr}

Answer questions clearly with code examples when relevant. Be encouraging but honest.
Use markdown formatting: **bold**, \`code\`, \`\`\`python for code blocks.

Return a JSON object:
{
    "response": "Your detailed answer in markdown",
    "suggested_followup": ["Follow-up question 1", "Follow-up question 2"]
}`;

        return callAgent(prompt, message);
    },

    // ── EVALUATOR AGENT (Quiz) ──
    async generateQuiz(topic, subtopic, difficulty, numQuestions) {
        const prompt = `You are an expert quiz creator for ${getTopicName(topic)}.
${subtopic ? `Subtopic: ${getSubtopicName(subtopic)}` : `Topic: ${getTopicName(topic)}`}
Difficulty: ${difficulty}

Create exactly ${numQuestions} questions. Mix MCQ, true/false, and short answer.

Return a JSON object:
{
    "questions": [
        {
            "id": 1,
            "type": "mcq",
            "question": "Question text?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A",
            "explanation": "Why A is correct",
            "points": 10
        },
        {
            "id": 2,
            "type": "true_false",
            "question": "Statement to evaluate?",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Why it's true",
            "points": 5
        },
        {
            "id": 3,
            "type": "short_answer",
            "question": "Explain concept X?",
            "correct_answer": "Expected key points",
            "explanation": "Full explanation",
            "points": 15
        }
    ]
}`;

        return callAgent(prompt, `Generate a ${difficulty} ${numQuestions}-question quiz on ${getTopicName(topic)}${subtopic ? ' - ' + getSubtopicName(subtopic) : ''}.`);
    },

    // ── EVALUATOR AGENT (Score Quiz) ──
    async scoreQuiz(questions, userAnswers, topic) {
        const prompt = `You are an expert evaluator. Score each answer and provide detailed feedback.

Return a JSON object:
{
    "score": 75,
    "correct_count": 3,
    "total": 4,
    "results": [
        {
            "question_id": 1,
            "correct": true,
            "user_answer": "A",
            "correct_answer": "A",
            "feedback": "Correct! Good understanding."
        }
    ],
    "overall_feedback": "Good performance. Focus on...",
    "weak_areas": ["area1", "area2"],
    "suggestions": ["Study suggestion 1"]
}`;

        const questionsStr = questions.map((q, i) =>
            `Q${i+1}: ${q.question}\nCorrect: ${q.correct_answer}\nUser answered: ${userAnswers[i] || '(no answer)'}`
        ).join('\n\n');

        return callAgent(prompt, `Topic: ${getTopicName(topic)}\n\n${questionsStr}\n\nScore all answers and provide feedback.`);
    },

    // ── EVALUATOR AGENT (Code) ──
    async evaluateCode(topic, prompt, code) {
        const systemPrompt = `You are a senior code reviewer for ${getTopicName(topic)}.
Evaluate the submitted code against the requirements.

Return a JSON object:
{
    "score": 80,
    "correctness": 8,
    "style": 7,
    "efficiency": 8,
    "feedback": "Overall feedback on the code",
    "issues": ["Issue 1", "Issue 2"],
    "suggestions": ["Improvement 1", "Improvement 2"],
    "corrected_code": "# Improved version if needed\\ncode here"
}`;

        return callAgent(systemPrompt, `Challenge: ${prompt}\n\nSubmitted Code:\n\`\`\`python\n${code}\n\`\`\`\n\nEvaluate this code.`);
    },

    // ── CODE CHALLENGE GENERATOR ──
    async generateChallenge(topic, subtopic, difficulty) {
        const prompt = `You are a coding challenge creator for ${getTopicName(topic)}.
${subtopic ? `Subtopic: ${getSubtopicName(subtopic)}` : ''}
Difficulty: ${difficulty}

Return a JSON object:
{
    "title": "Challenge title",
    "description": "Detailed problem description",
    "requirements": ["Requirement 1", "Requirement 2", "Requirement 3"],
    "starter_code": "# Starter code template\\ndef solution():\\n    # Your code here\\n    pass",
    "hints": ["Hint 1", "Hint 2"],
    "test_cases": "# Test your solution\\nprint(solution())",
    "difficulty": "${difficulty}"
}`;

        return callAgent(prompt, `Create a ${difficulty} ${getTopicName(topic)} coding challenge${subtopic ? ' about ' + getSubtopicName(subtopic) : ''}.`);
    },

    // ── DEBUGGER AGENT ──
    async debugCode(code, error, expected, topic) {
        const prompt = `You are an expert debugging assistant for ${getTopicName(topic || 'Python')}.
Analyze the bug, find root cause, and provide a fix.

Return a JSON object:
{
    "issue_summary": "Brief description of the bug",
    "root_cause": "Why this bug occurs",
    "corrected_code": "# Fixed code here\\ncorrected version",
    "explanation": "Step-by-step explanation of the fix in markdown",
    "best_practices": ["Best practice 1", "Best practice 2"],
    "related_concepts": ["Concept to review 1", "Concept 2"]
}`;

        let userMsg = `Code:\n\`\`\`\n${code}\n\`\`\``;
        if (error) userMsg += `\n\nError: ${error}`;
        if (expected) userMsg += `\n\nExpected behavior: ${expected}`;

        return callAgent(prompt, userMsg);
    },

    // ── PROJECT MENTOR AGENT ──
    async suggestProject(topic, difficulty, skills) {
        const prompt = `You are a project mentor for ${getTopicName(topic)}.
Suggest a practical, portfolio-worthy project.

Return a JSON object:
{
    "title": "Project title",
    "description": "Detailed project description",
    "difficulty": "${difficulty || 'intermediate'}",
    "estimated_hours": 8,
    "requirements": ["Requirement 1", "Requirement 2", "Requirement 3"],
    "learning_outcomes": ["Outcome 1", "Outcome 2"],
    "tech_stack": ["Technology 1", "Technology 2"],
    "milestones": [
        {"step": 1, "task": "Task description", "hours": 2}
    ],
    "starter_guidance": "How to get started guide in markdown"
}`;

        return callAgent(prompt, `Suggest a ${difficulty || 'intermediate'} project for ${getTopicName(topic)}. Skills to practice: ${skills || 'all fundamentals'}.`);
    },

    // ── PROJECT MENTOR (Review) ──
    async reviewProject(title, description, code, topic) {
        const prompt = `You are a senior project reviewer for ${getTopicName(topic)}.
Evaluate this project submission.

Return a JSON object:
{
    "score": 75,
    "feedback": "Detailed feedback on the project",
    "strengths": ["Strength 1", "Strength 2"],
    "improvements": ["Improvement 1", "Improvement 2"],
    "grade": "B+",
    "next_steps": ["Next step 1", "Next step 2"]
}`;

        let userMsg = `Project: ${title}\nDescription: ${description}`;
        if (code) userMsg += `\n\nCode:\n\`\`\`\n${code}\n\`\`\``;

        return callAgent(prompt, userMsg);
    },
};
