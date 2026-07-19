import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Comment

def populate():
    print("Populating initial blog data...")
    
    # 1. Create Superuser if it doesn't exist
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword'
    
    if not User.objects.filter(username=username).exists():
        admin_user = User.objects.create_superuser(username, email, password)
        admin_user.first_name = 'Alex'
        admin_user.last_name = 'Dev'
        admin_user.save()
        print(f"Created superuser: {username} (password: {password})")
    else:
        admin_user = User.objects.get(username=username)
        print(f"Superuser '{username}' already exists.")

    # 2. Create Categories
    categories_data = [
        {'name': 'Web Development', 'slug': 'web-development'},
        {'name': 'Design Systems', 'slug': 'design-systems'},
        {'name': 'Artificial Intelligence', 'slug': 'artificial-intelligence'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data['name'], 
            defaults={'slug': cat_data['slug']}
        )
        categories[cat.name] = cat
        if created:
            print(f"Created category: {cat.name}")

    # 3. Create Sample Posts
    posts_data = [
        {
            'title': 'Mastering Grid Layouts in CSS',
            'slug': 'mastering-grid-layouts-css',
            'category': categories['Web Development'],
            'excerpt': 'Explore the power of CSS Grids to create responsive, complex, and beautiful web interfaces with minimal code.',
            'content': """CSS Grid Layout is one of the most powerful tools available to web designers and developers today. It introduces a two-dimensional grid system that can completely change the way we design user interfaces.

Unlike Flexbox, which is primarily one-dimensional (dealing with either columns or rows), CSS Grid lets you align elements in both dimensions simultaneously. This control allows for complex page layouts that adapt dynamically to different screen sizes.

Let's look at a simple example of defining a grid:

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}
```

This simple snippet achieves a highly responsive grid layout that automatically adjusts the number of columns based on the available width of the screen.

### Why CSS Grid is the Future

1. **True Two-Dimensional Control**: Position elements vertically and horizontally without complex wrappers.
2. **Simplified Layout Logic**: Reduce reliance on third-party frameworks like Bootstrap or Tailwind for standard structural needs.
3. **Implicit Grid Generation**: Items are placed automatically in rows or columns as needed.

Start incorporating CSS Grid in your next project to see how it simplifies your styling pipeline and results in cleaner, more maintainable codebases!""",
            'status': 1 # Published
        },
        {
            'title': 'Designing the Perfect Dark Mode',
            'slug': 'designing-perfect-dark-mode',
            'category': categories['Design Systems'],
            'excerpt': 'Dark mode is more than just swapping white for black. Learn the nuances of color harmony, contrast ratios, and user preference management.',
            'content': """Implementing a dark mode toggle has become a standard feature for modern web applications. However, designing an excellent dark mode experience requires careful consideration beyond a simple color inversion.

Pure black backgrounds (#000000) with pure white text (#ffffff) can create high-contrast harshness that strains the eyes. Instead, modern interfaces utilize deep slate colors or charcoal tones to provide a soft, comfortable workspace.

### Key Considerations for Dark Themes

- **Use Off-Black Backgrounds**: Use values like `#0b0f19` or `#121212`. They soften the screen and allow for subtle shadows.
- **Maintain Contrast Ratios**: Check contrast using WCAG guidelines (aim for at least 4.5:1 for body text).
- **Tone Down Accents**: High-vibrancy accent colors that look great on light backgrounds can bleed and look neon or blurry on dark backgrounds. Use slightly desaturated variations.

For state persistence, leveraging CSS custom variables alongside Javascript local storage ensures a smooth, flicker-free rendering sequence:

```javascript
// Toggle and persist theme
const toggleTheme = () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
};
```

By putting usability first, you can deliver an interface that users will love to read day and night.""",
            'status': 1 # Published
        },
        {
            'title': 'Building Agentic Workflows with Large Language Models',
            'slug': 'building-agentic-workflows-llm',
            'category': categories['Artificial Intelligence'],
            'excerpt': 'Understand the shift from static prompts to autonomous agents that can plan, execute tools, and adapt to feedback.',
            'content': """The field of AI is shifting rapidly from simple question-answering systems to autonomous agents capable of performing complex tasks. This evolution is driven by agentic workflows.

An agentic workflow is one where the LLM is not just a passive model responding to a single prompt, but an active decision-maker that executes loops of thinking, planning, tool usage, and evaluation.

### Core Architecture of AI Agents

1. **Planning**: Breaking down a complex objective into sequential tasks.
2. **Tool Execution**: Reading and writing files, searching the web, executing code, or querying databases.
3. **Self-Correction**: Evaluating output quality and correcting errors in real-time.

For example, when an agent runs code that produces a syntax error, it reads the traceback error logs, updates its codebase, and tries again. This loop enables solving multi-step tasks without human intervention.

As AI models get faster and reasoning capabilities improve, agentic architectures will become the backbone of automation in modern software engineering.""",
            'status': 1 # Published
        },
        {
            'title': 'A Draft Post for the Future',
            'slug': 'draft-post-future',
            'category': categories['Web Development'],
            'excerpt': 'This post is a draft and should not appear on the home screen until published.',
            'content': 'This is confidential content only visible to admin staff inside the admin panel.',
            'status': 0 # Draft
        }
    ]

    for p_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=p_data['title'],
            defaults={
                'slug': p_data['slug'],
                'author': admin_user,
                'category': p_data['category'],
                'excerpt': p_data['excerpt'],
                'content': p_data['content'],
                'status': p_data['status']
            }
        )
        if created:
            print(f"Created post: {post.title}")

        # 4. Add a sample comment to the first post
        if created and p_data['title'] == 'Mastering Grid Layouts in CSS':
            Comment.objects.create(
                post=post,
                name='Sarah Connor',
                email='sarah@example.com',
                body='This is an incredibly helpful article! CSS Grid always felt intimidating, but the minmax example makes total sense.',
                active=True
            )
            Comment.objects.create(
                post=post,
                name='John Doe',
                email='john@example.com',
                body='Great guide. Do you recommend combining Grid with Flexbox inside cards?',
                active=True
            )
            Comment.objects.create(
                post=post,
                name='Pending Tester',
                email='tester@example.com',
                body='This comment is pending and should not display until approved in the admin site.',
                active=False
            )
            print("Added comments to the CSS Grid post.")

    print("Data population completed successfully!")

if __name__ == '__main__':
    populate()
