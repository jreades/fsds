---
name: curriculum-reviewer
description: Comprehensively reviews curriculum materials for quality, consistency, and effectiveness. Use when the user asks to review content, check quality, audit materials, or ensure curriculum meets standards. Provides detailed feedback and improvement recommendations.
allowed-tools: Read, Edit, Glob, Task
---

# Curriculum Reviewer Skill

This skill comprehensively reviews educational materials for quality, pedagogical soundness, and consistency.

## When to Use

Use this skill when the user:
- Asks to review curriculum or lesson materials
- Wants quality assurance on educational content
- Requests feedback on teaching materials
- Needs consistency check across multiple lessons
- Wants to audit materials before publishing
- Asks for improvement recommendations

## What This Skill Does

1. **Identifies Scope** of review:
   - Entire curriculum
   - Specific class or lesson
   - Specific material type (lessons, slides, assessments)
   - Particular aspects (pedagogy, formatting, alignment)

2. **Invokes Multiple Subagents** for comprehensive review:

   **lesson-planner subagent** reviews:
   - Learning objectives alignment
   - Pedagogical soundness
   - Timing and pacing realism
   - Differentiation strategies
   - Hands-on activity quality
   - Assessment alignment with objectives

   **slide-designer subagent** reviews:
   - Slide clarity and visual design
   - One-idea-per-slide principle
   - Formatting consistency
   - Engagement elements
   - Presenter notes quality

   **assessment-builder subagent** reviews:
   - Rubric clarity and fairness
   - Criteria alignment with objectives
   - Performance level descriptions
   - Example quality and usefulness
   - Student-friendly language

   **github-stylist subagent** reviews:
   - Markdown formatting consistency
   - Professional appearance
   - Navigation and linking
   - README completeness
   - Overall polish

3. **Creates Comprehensive Review Report** with:
   - **Strengths Identified**: What's working well
   - **Areas for Improvement**: Specific issues found
   - **Recommendations**: Concrete suggestions for fixes
   - **Priority Levels**: Critical vs. nice-to-have improvements
   - **Consistency Issues**: Patterns across materials
   - **Alignment Check**: Objectives → content → assessment

4. **Offers Action Plan**:
   - Prioritized list of improvements
   - Option to apply automated fixes
   - Suggestions for manual edits

## Review Criteria

**Pedagogical Quality:**
- Clear, measurable learning objectives
- Age-appropriate content and examples
- Effective differentiation strategies
- Authentic, hands-on activities
- Aligned assessments

**Content Quality:**
- Accurate information
- Relevant, current examples
- Clear explanations
- Logical progression
- Complete materials

**Consistency:**
- Formatting uniformity
- Style consistency
- Voice and tone
- Terminology usage
- Visual presentation

**Usability:**
- Ready-to-teach materials
- Clear instructions
- Appropriate timing
- Necessary resources listed
- Student-facing clarity

## Output Structure

Review reports include:
- **Executive Summary**: Overview of findings
- **Detailed Findings** by category
- **Specific Examples** of issues
- **Recommendations** with priority
- **Consistency Analysis** across materials
- **Action Items** checklist

## Example Usage

User: "Review all the Class 1 materials and make sure everything is high quality"

This skill will conduct a comprehensive review and provide detailed feedback with recommendations.
