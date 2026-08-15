<!-- Updated: 2026-03-02 -->
# Blog Post SEO Strategy Template

## Content Structure & Best Practices

### Essential Elements
- **Title Tag**: 50-60 characters, front-load main keyword, include numbers/brackets (e.g., "[2026 Guide]")
- **Meta Description**: 140-160 characters, natural language, clear value proposition
- **H1 Heading**: Only ONE per page, closely matching title tag
- **Introduction**: Orient the reader, state the problem, and explain what they will learn; name the topic early when natural.
- **Body**: Use H2s for main sections, H3s for subsections
- **Conclusion**: Summarize key points, clear Call To Action (CTA)

### Content requirements
- **Coverage**: Answer the reader's query completely without padding; record length only as descriptive evidence.
- **Paragraphs**: Use readable paragraph breaks that match the subject and audience.
- **Images**: Add a hero or explanatory visuals only when they improve understanding.
- **Image Alt Text**: Descriptive, naturally include keywords where relevant

## Internal & External Linking

- **Internal Links**: Link to relevant supporting content using descriptive anchor text where it helps the reader.
- **External Links**: Cite authoritative primary sources for material claims when available.

## Keyword Optimization Strategy

1. **Primary Keyword**:
   - URL slug
   - Title tag
   - H1 heading
   - Opening where natural
   - Descriptive headings where relevant
   - Natural terminology in the body; never target keyword density

2. **LSI / Secondary Keywords**:
   - Include in H2/H3 subheadings
   - Use naturally where the terms improve precision
   - Use in image alt text

## E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

- Include Author Name, Bio, and Photo
- Link to author's social profiles/portfolio (sameAs)
- Date published and Date modified clearly visible
- Cite sources and link to data

## Required Schema Markup

Use `BlogPosting` or `Article` schema.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/blog/your-post-url"
  },
  "headline": "Your Post Headline",
  "description": "Your meta description here.",
  "image": "https://example.com/featured-image.jpg",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author-bio"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Your Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2026-03-02T08:00:00+08:00",
  "dateModified": "2026-03-02T08:00:00+08:00"
}
```
