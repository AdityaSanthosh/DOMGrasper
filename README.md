# DOMGrasper

Parse a webpage to make it simple for an LLM to understand
If the solution has to be generic enough to be able to apply to most of the webpages on Internet, that's great

### The Solution:

How can we dimensionally reduce the DOM to something simple?
1. `<textarea>` `<input>` can be `<ip>`
2. Remove all meta tags except opengraph tags `<meta property="og:xxx">` and `<meta name="description">`
3. Remove all divs and classes which are just placeholders. Only Native HTML tags should remain
4. Remove all Styles
5. Keep all the aria-labelledby, aria-label, aria-describedby tags
6. Remove all static assets like css, images, javascript

Even if you do all of this, the resulting webpage is still massive which will cross the input character limit for a prompt. 
So I am going with second approach

_What's the useful information we can find from the page?_

There are 2 kinds of information. 

1. What's this Page about?
2. What's the content of this Page?

The first Information can be found from
1. Title (from `<title>` tag in `<head>`)
2. `<meta name="description" content="xxxx">`
3. `<og: title>` `<og:site_name>` `<og:url>`

All these can be extracted via code and passed as prompt to GPT Model.
(I am going to use Beautiful Soup to extract the HTML elements)

The content of the page is a little tricky, but we can
1. Get all headings `<h1 to h6>`
2. Convert `<li>` tags into list
3. Get all the content inside `<nav>`

#### **Limitations**:
1. This Dimension reducer removes all the stylistic html elements like css because no publicly available
LLM understands text from Image (at least not easily)
2. If the HTML is badly formatted or doesn't follow standard Practices (no meta tags, no og tags),
the parser cannot really do a good job, and it is really hard for the model to understand the content of this page