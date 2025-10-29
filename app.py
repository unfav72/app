from flask import Flask, render_template_string, request, jsonify, send_file
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import os

app = Flask(__name__)

# Configuration for OpenAI (set your API key)
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);

# HTML Template with enhanced features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Builder Pro</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header-banner {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        .header-banner h1 {
            font-size: 36px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .panel {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-height: 85vh;
            overflow-y: auto;
        }
        h1 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 28px;
        }
        h2 {
            color: #444;
            margin: 20px 0 10px 0;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 600;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            min-height: 80px;
            resize: vertical;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
            margin-top: 5px;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .ai-btn {
            background: #764ba2;
        }
        .ai-btn:hover:not(:disabled) {
            background: #653a8a;
        }
        .section-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            position: relative;
        }
        .resume-preview {
            background: white;
            padding: 40px;
            border: 1px solid #ddd;
        }
        .resume-header {
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        .resume-name {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }
        .resume-contact {
            color: #666;
            font-size: 14px;
        }
        .resume-section {
            margin-bottom: 25px;
        }
        .resume-section h3 {
            color: #667eea;
            font-size: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }
        .resume-item {
            margin-bottom: 15px;
        }
        .resume-item-title {
            font-weight: bold;
            color: #333;
            font-size: 16px;
        }
        .resume-item-subtitle {
            color: #666;
            font-style: italic;
            margin-bottom: 5px;
        }
        .resume-item-description {
            color: #555;
            line-height: 1.6;
            white-space: pre-line;
        }
        .ai-suggestion {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #764ba2;
        }
        .download-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 20px;
        }
        .download-btn {
            background: #28a745;
            width: 100%;
        }
        .download-btn:hover {
            background: #218838;
        }
        .pdf-btn {
            background: #dc3545;
        }
        .pdf-btn:hover {
            background: #c82333;
        }
        .ai-features {
            background: #f0e6ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #764ba2;
        }
        .ai-features h3 {
            color: #764ba2;
            margin-bottom: 10px;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .template-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .template-option {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }
        .template-option:hover {
            border-color: #667eea;
        }
        .template-option.active {
            border-color: #667eea;
            background: #f0f4ff;
        }
        @media (max-width: 968px) {
            .container {
                grid-template-columns: 1fr;
            }
            .download-section {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>🚀 AI Resume Builder Pro</h1>
        <p>Create professional resumes with AI-powered suggestions</p>
    </div>
    
    <div class="container">
        <div class="panel">
            <h1>✨ Build Your Resume</h1>
            
            <div class="ai-features">
                <h3>🤖 AI Features Available</h3>
                <p>• Smart content enhancement • Job-specific suggestions • Grammar & tone optimization • Skill recommendations • Achievement quantification</p>
            </div>
            
            <h2>Resume Template</h2>
            <div class="template-selector">
                <div class="template-option active" onclick="selectTemplate('professional')" id="template-professional">
                    📄 Professional
                </div>
                <div class="template-option" onclick="selectTemplate('modern')" id="template-modern">
                    ✨ Modern
                </div>
                <div class="template-option" onclick="selectTemplate('minimal')" id="template-minimal">
                    📝 Minimal
                </div>
            </div>
            
            <h2>Personal Information</h2>
            <div class="form-group">
                <label>Full Name *</label>
                <input type="text" id="fullName" placeholder="John Doe">
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" id="email" placeholder="john@example.com">
            </div>
            <div class="form-group">
                <label>Phone</label>
                <input type="tel" id="phone" placeholder="+1 234 567 8900">
            </div>
            <div class="form-group">
                <label>Location</label>
                <input type="text" id="location" placeholder="New York, NY">
            </div>
            <div class="form-group">
                <label>LinkedIn</label>
                <input type="text" id="linkedin" placeholder="linkedin.com/in/johndoe">
            </div>
            <div class="form-group">
                <label>Website/Portfolio</label>
                <input type="text" id="website" placeholder="johndoe.com">
            </div>
            
            <h2>Professional Summary</h2>
            <div class="form-group">
                <label>Summary</label>
                <textarea id="summary" placeholder="Brief professional summary..."></textarea>
                <button class="ai-btn" onclick="aiEnhance('summary')" id="enhanceSummaryBtn">✨ AI Enhance Summary</button>
                <button class="ai-btn" onclick="aiRewriteTone('summary')" id="rewriteSummaryBtn">🎯 Change Tone</button>
            </div>
            
            <h2>Work Experience</h2>
            <div id="experienceList"></div>
            <div class="form-group">
                <label>Job Title *</label>
                <input type="text" id="jobTitle" placeholder="Software Engineer">
            </div>
            <div class="form-group">
                <label>Company *</label>
                <input type="text" id="company" placeholder="Tech Corp">
            </div>
            <div class="form-group">
                <label>Duration</label>
                <input type="text" id="duration" placeholder="Jan 2020 - Present">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="jobDescription" placeholder="Key responsibilities and achievements..."></textarea>
            </div>
            <button onclick="addExperience()">Add Experience</button>
            <button class="ai-btn" onclick="aiSuggestDescription()">✨ AI Generate Description</button>
            <button class="ai-btn" onclick="aiQuantifyAchievements()">📊 Quantify Achievements</button>
            
            <h2>Education</h2>
            <div id="educationList"></div>
            <div class="form-group">
                <label>Degree *</label>
                <input type="text" id="degree" placeholder="Bachelor of Science in Computer Science">
            </div>
            <div class="form-group">
                <label>Institution *</label>
                <input type="text" id="institution" placeholder="University Name">
            </div>
            <div class="form-group">
                <label>Year</label>
                <input type="text" id="year" placeholder="2016 - 2020">
            </div>
            <div class="form-group">
                <label>GPA (Optional)</label>
                <input type="text" id="gpa" placeholder="3.8/4.0">
            </div>
            <button onclick="addEducation()">Add Education</button>
            
            <h2>Skills</h2>
            <div class="form-group">
                <label>Skills (comma separated)</label>
                <input type="text" id="skills" placeholder="Python, JavaScript, React, Node.js">
                <button class="ai-btn" onclick="aiSuggestSkills()">✨ AI Suggest Skills</button>
                <button class="ai-btn" onclick="aiOptimizeSkills()">🎯 Optimize for ATS</button>
            </div>
            
            <h2>Certifications (Optional)</h2>
            <div class="form-group">
                <textarea id="certifications" placeholder="AWS Certified Solutions Architect&#10;Google Cloud Professional"></textarea>
            </div>
            
            <h2>Languages (Optional)</h2>
            <div class="form-group">
                <input type="text" id="languages" placeholder="English (Native), Spanish (Fluent)">
            </div>
            
            <div class="download-section">
                <button class="download-btn" onclick="downloadJSON()">📥 Download JSON</button>
                <button class="pdf-btn" onclick="downloadPDF()">📄 Download PDF</button>
            </div>
        </div>
        
        <div class="panel">
            <h1>📄 Resume Preview</h1>
            <div class="resume-preview" id="resumePreview">
                <div class="resume-header">
                    <div class="resume-name" id="previewName">Your Name</div>
                    <div class="resume-contact">
                        <span id="previewEmail">email@example.com</span> | 
                        <span id="previewPhone">+1 234 567 8900</span> | 
                        <span id="previewLocation">Location</span>
                    </div>
                    <div class="resume-contact" id="previewLinks" style="margin-top:5px;display:none;">
                        <span id="previewLinkedin"></span>
                        <span id="previewWebsite"></span>
                    </div>
                </div>
                
                <div class="resume-section" id="summarySection" style="display:none;">
                    <h3>Professional Summary</h3>
                    <p id="previewSummary"></p>
                </div>
                
                <div class="resume-section" id="experienceSection" style="display:none;">
                    <h3>Work Experience</h3>
                    <div id="previewExperience"></div>
                </div>
                
                <div class="resume-section" id="educationSection" style="display:none;">
                    <h3>Education</h3>
                    <div id="previewEducation"></div>
                </div>
                
                <div class="resume-section" id="skillsSection" style="display:none;">
                    <h3>Skills</h3>
                    <p id="previewSkills"></p>
                </div>
                
                <div class="resume-section" id="certificationsSection" style="display:none;">
                    <h3>Certifications</h3>
                    <p id="previewCertifications" style="white-space: pre-line;"></p>
                </div>
                
                <div class="resume-section" id="languagesSection" style="display:none;">
                    <h3>Languages</h3>
                    <p id="previewLanguages"></p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let experiences = [];
        let education = [];
        let currentTemplate = 'professional';
        
        function selectTemplate(template) {
            currentTemplate = template;
            document.querySelectorAll('.template-option').forEach(el => el.classList.remove('active'));
            document.getElementById('template-' + template).classList.add('active');
        }
        
        function updatePreview() {
            document.getElementById('previewName').textContent = 
                document.getElementById('fullName').value || 'Your Name';
            document.getElementById('previewEmail').textContent = 
                document.getElementById('email').value || 'email@example.com';
            document.getElementById('previewPhone').textContent = 
                document.getElementById('phone').value || '+1 234 567 8900';
            document.getElementById('previewLocation').textContent = 
                document.getElementById('location').value || 'Location';
            
            const linkedin = document.getElementById('linkedin').value;
            const website = document.getElementById('website').value;
            if (linkedin || website) {
                document.getElementById('previewLinks').style.display = 'block';
                document.getElementById('previewLinkedin').textContent = linkedin ? linkedin : '';
                document.getElementById('previewWebsite').textContent = website ? (linkedin ? ' | ' : '') + website : '';
            } else {
                document.getElementById('previewLinks').style.display = 'none';
            }
            
            const summary = document.getElementById('summary').value;
            if (summary) {
                document.getElementById('summarySection').style.display = 'block';
                document.getElementById('previewSummary').textContent = summary;
            } else {
                document.getElementById('summarySection').style.display = 'none';
            }
            
            if (experiences.length > 0) {
                document.getElementById('experienceSection').style.display = 'block';
                document.getElementById('previewExperience').innerHTML = experiences.map(exp => `
                    <div class="resume-item">
                        <div class="resume-item-title">${exp.title}</div>
                        <div class="resume-item-subtitle">${exp.company} | ${exp.duration}</div>
                        <div class="resume-item-description">${exp.description}</div>
                    </div>
                `).join('');
            } else {
                document.getElementById('experienceSection').style.display = 'none';
            }
            
            if (education.length > 0) {
                document.getElementById('educationSection').style.display = 'block';
                document.getElementById('previewEducation').innerHTML = education.map(edu => `
                    <div class="resume-item">
                        <div class="resume-item-title">${edu.degree}</div>
                        <div class="resume-item-subtitle">${edu.institution} | ${edu.year}</div>
                        ${edu.gpa ? '<div class="resume-item-description">GPA: ' + edu.gpa + '</div>' : ''}
                    </div>
                `).join('');
            } else {
                document.getElementById('educationSection').style.display = 'none';
            }
            
            const skills = document.getElementById('skills').value;
            if (skills) {
                document.getElementById('skillsSection').style.display = 'block';
                document.getElementById('previewSkills').textContent = skills;
            } else {
                document.getElementById('skillsSection').style.display = 'none';
            }
            
            const certifications = document.getElementById('certifications').value;
            if (certifications) {
                document.getElementById('certificationsSection').style.display = 'block';
                document.getElementById('previewCertifications').textContent = certifications;
            } else {
                document.getElementById('certificationsSection').style.display = 'none';
            }
            
            const languages = document.getElementById('languages').value;
            if (languages) {
                document.getElementById('languagesSection').style.display = 'block';
                document.getElementById('previewLanguages').textContent = languages;
            } else {
                document.getElementById('languagesSection').style.display = 'none';
            }
        }
        
        document.querySelectorAll('input, textarea').forEach(el => {
            el.addEventListener('input', updatePreview);
        });
        
        function addExperience() {
            const title = document.getElementById('jobTitle').value;
            const company = document.getElementById('company').value;
            const duration = document.getElementById('duration').value;
            const description = document.getElementById('jobDescription').value;
            
            if (title && company) {
                experiences.push({title, company, duration, description});
                document.getElementById('jobTitle').value = '';
                document.getElementById('company').value = '';
                document.getElementById('duration').value = '';
                document.getElementById('jobDescription').value = '';
                updateExperienceList();
                updatePreview();
            } else {
                alert('Please fill in Job Title and Company');
            }
        }
        
        function updateExperienceList() {
            document.getElementById('experienceList').innerHTML = experiences.map((exp, i) => `
                <div class="section-item">
                    <strong>${exp.title}</strong> at ${exp.company}
                    <button onclick="removeExperience(${i})" style="float:right;background:#dc3545;">Remove</button>
                </div>
            `).join('');
        }
        
        function removeExperience(index) {
            experiences.splice(index, 1);
            updateExperienceList();
            updatePreview();
        }
        
        function addEducation() {
            const degree = document.getElementById('degree').value;
            const institution = document.getElementById('institution').value;
            const year = document.getElementById('year').value;
            const gpa = document.getElementById('gpa').value;
            
            if (degree && institution) {
                education.push({degree, institution, year, gpa});
                document.getElementById('degree').value = '';
                document.getElementById('institution').value = '';
                document.getElementById('year').value = '';
                document.getElementById('gpa').value = '';
                updateEducationList();
                updatePreview();
            } else {
                alert('Please fill in Degree and Institution');
            }
        }
        
        function updateEducationList() {
            document.getElementById('educationList').innerHTML = education.map((edu, i) => `
                <div class="section-item">
                    <strong>${edu.degree}</strong> - ${edu.institution}
                    <button onclick="removeEducation(${i})" style="float:right;background:#dc3545;">Remove</button>
                </div>
            `).join('');
        }
        
        function removeEducation(index) {
            education.splice(index, 1);
            updateEducationList();
            updatePreview();
        }
        
        async function callAI(endpoint, data, buttonId) {
            const button = document.getElementById(buttonId);
            const originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<span class="loading"></span> Processing...';
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                button.disabled = false;
                button.innerHTML = originalText;
                return result;
            } catch (error) {
                button.disabled = false;
                button.innerHTML = originalText;
                alert('Error: ' + error.message);
                return null;
            }
        }
        
        async function aiEnhance(field) {
            const text = document.getElementById(field).value;
            if (!text) {
                alert('Please enter some text first!');
                return;
            }
            
            const result = await callAI('/ai-enhance', {text, field}, 'enhanceSummaryBtn');
            if (result) {
                document.getElementById(field).value = result.enhanced;
                updatePreview();
            }
        }
        
        async function aiRewriteTone(field) {
            const text = document.getElementById(field).value;
            if (!text) {
                alert('Please enter some text first!');
                return;
            }
            
            const result = await callAI('/ai-rewrite-tone', {text}, 'rewriteSummaryBtn');
            if (result) {
                document.getElementById(field).value = result.rewritten;
                updatePreview();
            }
        }
        
        async function aiSuggestDescription() {
            const title = document.getElementById('jobTitle').value;
            const company = document.getElementById('company').value;
            if (!title) {
                alert('Please enter a job title first!');
                return;
            }
            
            const result = await callAI('/ai-suggest-description', 
                {title, company}, 'enhanceSummaryBtn');
            if (result) {
                document.getElementById('jobDescription').value = result.description;
            }
        }
        
        async function aiQuantifyAchievements() {
            const description = document.getElementById('jobDescription').value;
            if (!description) {
                alert('Please enter job description first!');
                return;
            }
            
            const result = await callAI('/ai-quantify', {description}, 'enhanceSummaryBtn');
            if (result) {
                document.getElementById('jobDescription').value = result.quantified;
            }
        }
        
        async function aiSuggestSkills() {
            const title = document.getElementById('jobTitle').value || 'software developer';
            const experience = experiences.map(e => e.title).join(', ');
            
            const result = await callAI('/ai-suggest-skills', 
                {title, experience}, 'enhanceSummaryBtn');
            if (result) {
                document.getElementById('skills').value = result.skills;
                updatePreview();
            }
        }
        
        async function aiOptimizeSkills() {
            const skills = document.getElementById('skills').value;
            if (!skills) {
                alert('Please enter skills first!');
                return;
            }
            
            const result = await callAI('/ai-optimize-ats', {skills}, 'enhanceSummaryBtn');
            if (result) {
                document.getElementById('skills').value = result.optimized;
                updatePreview();
            }
        }
        
        function downloadJSON() {
            const resume = {
                template: currentTemplate,
                personalInfo: {
                    name: document.getElementById('fullName').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    location: document.getElementById('location').value,
                    linkedin: document.getElementById('linkedin').value,
                    website: document.getElementById('website').value
                },
                summary: document.getElementById('summary').value,
                experience: experiences,
                education: education,
                skills: document.getElementById('skills').value,
                certifications: document.getElementById('certifications').value,
                languages: document.getElementById('languages').value
            };
            
            const blob = new Blob([JSON.stringify(resume, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'resume_' + new Date().getTime() + '.json';
            a.click();
        }
        
        async function downloadPDF() {
            const resume = {
                template: currentTemplate,
                personalInfo: {
                    name: document.getElementById('fullName').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    location: document.getElementById('location').value,
                    linkedin: document.getElementById('linkedin').value,
                    website: document.getElementById('website').value
                },
                summary: document.getElementById('summary').value,
                experience: experiences,
                education: education,
                skills: document.getElementById('skills').value,
                certifications: document.getElementById('certifications').value,
                languages: document.getElementById('languages').value
            };
            
            if (!resume.personalInfo.name || !resume.personalInfo.email) {
                alert('Please fill in at least Name and Email');
                return;
            }
            
            try {
                const response = await fetch('/generate-pdf', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(resume)
                });
                
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = resume.personalInfo.name.replace(/\s+/g, '_') + '_Resume.pdf';
                a.click();
            } catch (error) {
                alert('Error generating PDF: ' + error.message);
            }
        }
    </script>
</body>
</html>
'''

# AI Enhancement functions using OpenAI API
def call_openai(prompt, max_tokens=500):
    """Call OpenAI API - replace with actual implementation"""
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to simulated responses if OpenAI not configured
        return simulate_ai_response(prompt)

def simulate_ai_response(prompt):
    """Simulated AI responses for demo purposes"""
    if "enhance" in prompt.lower() and "summary" in prompt.lower():
        return "Results-driven professional with proven track record of delivering high-impact solutions. Expertise in driving organizational success through innovative approaches, strategic thinking, and collaborative leadership. Demonstrated ability to exceed targets and create measurable business value."
    elif "job description" in prompt.lower():
        return "• Designed and implemented scalable solutions that improved system performance by 40%\n• Led cross-functional team of 5 engineers in agile development environment\n• Collaborated with stakeholders to define requirements and deliver features on schedule\n• Mentored junior developers and conducted code reviews to ensure quality standards"
    elif "quantify" in prompt.lower():
        return "• Increased system performance by 40% through optimization initiatives\n• Reduced deployment time by 60% by implementing CI/CD pipeline\n• Managed team of 5 engineers, delivering 15+ features per quarter\n• Improved code quality, reducing bugs by 30% through rigorous testing"
    elif "skills" in prompt.lower():
        return "Python, JavaScript, React, Node.js, SQL, AWS, Docker, Kubernetes, Git, CI/CD, Agile/Scrum, REST APIs, Microservices"
    elif "tone" in prompt.lower():
        return "Dynamic professional with passion for innovation and excellence. Proven ability to drive results through creative problem-solving and strategic collaboration. Committed to continuous learning and delivering exceptional outcomes."
    elif "ats" in prompt.lower() or "optimize" in prompt.lower():
        return "Python, JavaScript, React.js, Node.js, SQL, PostgreSQL, MongoDB, AWS, Azure, Docker, Kubernetes, CI/CD, Git, Agile, Scrum, REST APIs, Microservices Architecture"
    return "AI-enhanced content with professional language and impact-focused messaging."

def enhance_text(text, field):
    """Enhanced text using AI"""
    prompt = f"Enhance this professional {field} for a resume. Make it impactful, concise, and achievement-focused. Original text: {text}"
    return call_openai(prompt, max_tokens=300)

def rewrite_tone(text):
    """Rewrite text in different professional tone"""
    prompt = f"Rewrite this resume summary in a confident, dynamic professional tone that showcases leadership and results: {text}"
    return call_openai(prompt, max_tokens=300)

def suggest_job_description(title, company=""):
    """Generate job description based on title and company"""
    company_context = f" at {company}" if company else ""
    prompt = f"Generate a professional job description with 4-5 bullet points for a {title}{company_context} role. Focus on achievements, quantifiable results, and impact. Use action verbs and be specific."
    
    # Simulated responses for common roles
    descriptions = {
        'software engineer': "• Architected and deployed microservices-based application serving 2M+ daily active users\n• Optimized database queries and caching strategies, reducing API response time by 45%\n• Led team of 4 developers using Agile methodologies to deliver 20+ features per quarter\n• Implemented automated testing pipeline, increasing code coverage from 60% to 95%\n• Mentored 3 junior engineers and conducted technical interviews for new hires",
        
        'product manager': "• Defined and executed product strategy for flagship SaaS platform, growing revenue by $5M annually\n• Conducted extensive user research with 100+ customers to identify pain points and opportunities\n• Prioritized product roadmap based on data analysis, increasing user retention by 30%\n• Collaborated with engineering, design, and marketing teams to launch 15+ features on schedule\n• Presented quarterly business reviews to C-level executives and key stakeholders",
        
        'data scientist': "• Built machine learning models achieving 94% accuracy for customer churn prediction, saving $2M annually\n• Analyzed 10TB+ of customer data using Python, SQL, and Spark to derive actionable insights\n• Developed real-time dashboards in Tableau used by 50+ stakeholders across organization\n• Collaborated with product team to implement A/B testing framework, improving conversion by 25%\n• Published research findings and presented at 3 industry conferences",
        
        'marketing manager': "• Developed and executed integrated marketing campaigns generating 5,000+ qualified leads quarterly\n• Managed $500K annual budget across digital, content, and event marketing channels\n• Increased organic website traffic by 150% through SEO optimization and content strategy\n• Led team of 6 marketing professionals and coordinated with external agencies\n• Improved email engagement rates by 40% through segmentation and personalization",
        
        'business analyst': "• Analyzed business processes and identified $3M in annual cost savings opportunities\n• Gathered requirements from 15+ stakeholders and translated into technical specifications\n• Created data visualizations and reports using SQL, Excel, and Power BI for executive team\n• Facilitated workshops with cross-functional teams to define project scope and deliverables\n• Documented business requirements for 10+ enterprise software implementations"
    }
    
    for key in descriptions:
        if key in title.lower():
            return descriptions[key]
    
    return call_openai(prompt, max_tokens=400)

def quantify_achievements(description):
    """Add quantifiable metrics to achievements"""
    prompt = f"Rewrite these job responsibilities to include specific quantifiable metrics, percentages, and numbers where possible. Focus on impact and results: {description}"
    return call_openai(prompt, max_tokens=400)

def suggest_skills(title, experience=""):
    """Suggest relevant skills based on role and experience"""
    context = f" with experience in {experience}" if experience else ""
    prompt = f"List 12-15 relevant technical and soft skills for a {title}{context} role, separated by commas. Include both hard skills and soft skills."
    
    skills_map = {
        'software engineer': "Python, JavaScript, TypeScript, React, Node.js, SQL, PostgreSQL, MongoDB, AWS, Docker, Kubernetes, Git, CI/CD, REST APIs, GraphQL, Agile/Scrum, Problem Solving, Team Collaboration",
        
        'data scientist': "Python, R, SQL, Machine Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Data Visualization, Tableau, Power BI, Statistics, A/B Testing, Big Data, Spark, Communication, Critical Thinking",
        
        'product manager': "Product Strategy, Roadmap Planning, User Research, Agile/Scrum, Data Analysis, A/B Testing, Wireframing, Jira, SQL, Market Analysis, Stakeholder Management, Leadership, Communication, Prioritization",
        
        'marketing manager': "Digital Marketing, SEO/SEM, Content Strategy, Google Analytics, Social Media Marketing, Email Marketing, Campaign Management, Budget Management, Marketing Automation, HubSpot, Salesforce, Analytics, Leadership, Creativity",
        
        'designer': "Figma, Adobe Creative Suite, Sketch, UI/UX Design, Prototyping, User Research, Wireframing, Design Systems, HTML/CSS, Responsive Design, Visual Design, Typography, Collaboration, Problem Solving",
        
        'business analyst': "Business Analysis, Requirements Gathering, Process Modeling, SQL, Data Analysis, Excel, Power BI, Tableau, Project Management, Agile, SDLC, Stakeholder Management, Communication, Critical Thinking"
    }
    
    for key in skills_map:
        if key in title.lower():
            return skills_map[key]
    
    return call_openai(prompt, max_tokens=300)

def optimize_for_ats(skills):
    """Optimize skills for ATS (Applicant Tracking Systems)"""
    prompt = f"Optimize this list of skills for ATS systems. Use full names and common variations, expand acronyms where helpful, and organize logically: {skills}"
    return call_openai(prompt, max_tokens=300)

def generate_pdf(resume_data):
    """Generate PDF resume using ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#667eea'),
        borderPadding=0,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        leading=14
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4,
        fontName='Helvetica-Oblique'
    )
    
    # Header
    personal_info = resume_data.get('personalInfo', {})
    story.append(Paragraph(personal_info.get('name', 'Your Name'), title_style))
    
    contact_parts = []
    if personal_info.get('email'):
        contact_parts.append(personal_info['email'])
    if personal_info.get('phone'):
        contact_parts.append(personal_info['phone'])
    if personal_info.get('location'):
        contact_parts.append(personal_info['location'])
    
    if contact_parts:
        story.append(Paragraph(' | '.join(contact_parts), contact_style))
    
    links_parts = []
    if personal_info.get('linkedin'):
        links_parts.append(personal_info['linkedin'])
    if personal_info.get('website'):
        links_parts.append(personal_info['website'])
    
    if links_parts:
        story.append(Paragraph(' | '.join(links_parts), contact_style))
    
    # Add horizontal line
    story.append(Spacer(1, 0.1*inch))
    
    # Professional Summary
    if resume_data.get('summary'):
        story.append(Paragraph('PROFESSIONAL SUMMARY', heading_style))
        story.append(Paragraph(resume_data['summary'], normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Work Experience
    if resume_data.get('experience'):
        story.append(Paragraph('WORK EXPERIENCE', heading_style))
        for exp in resume_data['experience']:
            story.append(Paragraph(f"<b>{exp.get('title', '')}</b>", normal_style))
            subtitle_text = f"{exp.get('company', '')}"
            if exp.get('duration'):
                subtitle_text += f" | {exp['duration']}"
            story.append(Paragraph(subtitle_text, subtitle_style))
            if exp.get('description'):
                story.append(Paragraph(exp['description'].replace('\n', '<br/>'), normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Education
    if resume_data.get('education'):
        story.append(Paragraph('EDUCATION', heading_style))
        for edu in resume_data['education']:
            story.append(Paragraph(f"<b>{edu.get('degree', '')}</b>", normal_style))
            subtitle_text = f"{edu.get('institution', '')}"
            if edu.get('year'):
                subtitle_text += f" | {edu['year']}"
            story.append(Paragraph(subtitle_text, subtitle_style))
            if edu.get('gpa'):
                story.append(Paragraph(f"GPA: {edu['gpa']}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Skills
    if resume_data.get('skills'):
        story.append(Paragraph('SKILLS', heading_style))
        story.append(Paragraph(resume_data['skills'], normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Certifications
    if resume_data.get('certifications'):
        story.append(Paragraph('CERTIFICATIONS', heading_style))
        story.append(Paragraph(resume_data['certifications'].replace('\n', '<br/>'), normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Languages
    if resume_data.get('languages'):
        story.append(Paragraph('LANGUAGES', heading_style))
        story.append(Paragraph(resume_data['languages'], normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Flask routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ai-enhance', methods=['POST'])
def ai_enhance():
    data = request.json
    enhanced = enhance_text(data['text'], data['field'])
    return jsonify({'enhanced': enhanced})

@app.route('/ai-rewrite-tone', methods=['POST'])
def ai_rewrite_tone():
    data = request.json
    rewritten = rewrite_tone(data['text'])
    return jsonify({'rewritten': rewritten})

@app.route('/ai-suggest-description', methods=['POST'])
def ai_suggest_description():
    data = request.json
    description = suggest_job_description(data['title'], data.get('company', ''))
    return jsonify({'description': description})

@app.route('/ai-quantify', methods=['POST'])
def ai_quantify():
    data = request.json
    quantified = quantify_achievements(data['description'])
    return jsonify({'quantified': quantified})

@app.route('/ai-suggest-skills', methods=['POST'])
def ai_suggest_skills():
    data = request.json
    skills = suggest_skills(data['title'], data.get('experience', ''))
    return jsonify({'skills': skills})

@app.route('/ai-optimize-ats', methods=['POST'])
def ai_optimize_ats():
    data = request.json
    optimized = optimize_for_ats(data['skills'])
    return jsonify({'optimized': optimized})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf_route():
    resume_data = request.json
    pdf_buffer = generate_pdf(resume_data)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume.pdf'
    )

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI Resume Builder Pro")
    print("=" * 60)
    print("\n📦 Required packages:")
    print("   pip install flask reportlab openai")
    print("\n🔑 OpenAI API Key Setup:")
    print("   export OPENAI_API_KEY='your-key-here'")
    print("   Or edit OPENAI_API_KEY variable in the code")
    print("\n🌐 Starting server at http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)

    if _name_ == '_main_':
    # Get port from environment variable (required for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Get host from environment (0.0.0.0 for production, 127.0.0.1 for local)
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Debug mode from environment
    debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    
    print("=" * 60)
    print("🚀 Resume Builder Server")
    print("=" * 60)
    print(f"Environment: {'Development' if debug else 'Production'}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("=" * 60)