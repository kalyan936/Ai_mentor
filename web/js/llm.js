/* ==============================================
   AI Mentor - LLM API Client
   Supports: HuggingFace (FREE), DeepSeek (FREE)
   Best models: Qwen2.5-72B, DeepSeek-V3, Llama-3.3
   ============================================== */

const LLM_MODELS = {
    'Qwen/Qwen2.5-72B-Instruct': 'Qwen 2.5 72B (Best Chinese, rivals GPT-4o)',
    'Qwen/Qwen2.5-Coder-32B-Instruct': 'Qwen 2.5 Coder 32B (Best for Code)',
    'meta-llama/Llama-3.3-70B-Instruct': 'Llama 3.3 70B (Best Open Model)',
    'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B': 'DeepSeek R1 32B (Reasoning)',
    'mistralai/Mistral-Small-24B-Instruct-2501': 'Mistral Small 24B (Fast)',
    'microsoft/phi-4': 'Phi-4 14B (Compact)',
};

const FALLBACK_MODELS = [
    'Qwen/Qwen2.5-72B-Instruct',
    'meta-llama/Llama-3.3-70B-Instruct',
    'Qwen/Qwen2.5-Coder-32B-Instruct',
    'mistralai/Mistral-Small-24B-Instruct-2501',
];

async function callLLM(systemPrompt, userMessage, options = {}) {
    const settings = Storage.getSettings();
    const provider = settings.provider || 'huggingface';

    if (provider === 'deepseek' && settings.deepseekKey) {
        return callDeepSeek(systemPrompt, userMessage, settings, options);
    } else if (provider === 'gemini' && settings.geminiKey) {
        return callGemini(systemPrompt, userMessage, settings, options);
    }
    return callHuggingFace(systemPrompt, userMessage, settings, options);
}

async function callHuggingFace(systemPrompt, userMessage, settings, options = {}) {
    const token = settings.hfToken;
    if (!token || token === 'your_hf_token_here') {
        throw new Error('Please add your free HuggingFace API token in Settings. Get one at huggingface.co/settings/tokens');
    }

    const model = options.model || settings.model || 'Qwen/Qwen2.5-72B-Instruct';
    const maxTokens = options.maxTokens || 3000;

    const messages = [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userMessage }
    ];

    // Try the selected model first, then fallbacks
    const modelsToTry = [model, ...FALLBACK_MODELS.filter(m => m !== model)];

    for (const m of modelsToTry) {
        try {
            const url = `https://api-inference.huggingface.co/models/${m}/v1/chat/completions`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: m,
                    messages: messages,
                    max_tokens: maxTokens,
                    temperature: options.temperature || 0.7,
                    stream: false,
                })
            });

            if (response.status === 200) {
                const data = await response.json();
                if (data.choices && data.choices[0]) {
                    return data.choices[0].message.content;
                }
            }

            // If 503 (model loading) or 429 (rate limit), try next model
            if (response.status === 503 || response.status === 429) {
                console.warn(`Model ${m} unavailable (${response.status}), trying next...`);
                continue;
            }

            const errText = await response.text();
            console.error(`HuggingFace error with ${m}: ${response.status}`, errText);
            continue;

        } catch (e) {
            console.error(`Error with model ${m}:`, e);
            continue;
        }
    }

    throw new Error('All models failed. Please check your HuggingFace token and try again.');
}

async function callDeepSeek(systemPrompt, userMessage, settings, options = {}) {
    const key = settings.deepseekKey;
    if (!key) {
        throw new Error('Please add your DeepSeek API key in Settings.');
    }

    const response = await fetch('https://api.deepseek.com/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${key}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'deepseek-chat',
            messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userMessage }
            ],
            max_tokens: options.maxTokens || 3000,
            temperature: options.temperature || 0.7,
        })
    });

    if (!response.ok) {
        throw new Error(`DeepSeek API error: ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
}

async function callGemini(systemPrompt, userMessage, settings, options = {}) {
    const key = settings.geminiKey;
    if (!key) {
        throw new Error('Please add your Gemini API key in Settings.');
    }

    const model = options.model || 'gemini-1.5-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            systemInstruction: {
                parts: [{ text: systemPrompt }]
            },
            contents: [{
                parts: [{ text: userMessage }]
            }],
            generationConfig: {
                temperature: options.temperature || 0.7,
                maxOutputTokens: options.maxTokens || 3000,
            }
        })
    });

    if (!response.ok) {
        const err = await response.text();
        throw new Error(`Gemini API error: ${response.status} - ${err}`);
    }

    const data = await response.json();
    if (data.candidates && data.candidates.length > 0) {
        return data.candidates[0].content.parts[0].text;
    }
    throw new Error('Invalid response from Gemini');
}


function parseJSONResponse(text) {
    // Try direct parse
    try { return JSON.parse(text); } catch (e) {}

    // Extract from markdown code blocks
    const match = text.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
    if (match) {
        try { return JSON.parse(match[1].trim()); } catch (e) {}
    }

    // Find JSON object or array
    const objMatch = text.match(/(\{[\s\S]*\})/);
    if (objMatch) {
        try { return JSON.parse(objMatch[1]); } catch (e) {}
    }

    const arrMatch = text.match(/(\[[\s\S]*\])/);
    if (arrMatch) {
        try { return JSON.parse(arrMatch[1]); } catch (e) {}
    }

    return { raw: text, error: 'Could not parse JSON' };
}

async function callAgent(systemPrompt, userMessage, parseJSON = true) {
    const response = await callLLM(systemPrompt, userMessage);
    if (parseJSON) {
        return parseJSONResponse(response);
    }
    return response;
}
