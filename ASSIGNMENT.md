# MiniCRM Take-Home Assessment: Build Your Feature

## Overview
Welcome! This is a practical coding assessment designed to evaluate your full-stack development skills, creativity, and decision-making. You'll be adding **a feature of your choice** to our existing MiniCRM application.

## Time Limit
**48 hours** from the time you receive this assignment.

---

## Background
MiniCRM is a simple customer relationship management application that currently manages Leads, Contacts, and Reminders. Your task is to extend this system by implementing a feature that you believe would add significant value to a CRM system.

---

## Your Task

**Choose ONE feature to implement** that demonstrates your technical skills and product thinking. You have complete freedom in your choice, but it should:

1. **Add meaningful value** to the CRM system
2. **Include both backend and frontend** components
3. **Integrate with existing models** (Leads, Contacts, or Reminders)
4. **Be completable within 48 hours** (scope appropriately)
5. **Demonstrate your technical strengths**

---

## Core Requirements

Regardless of which feature you choose, your implementation must include:

### 1. Backend (Django REST Framework)
- **Data Model(s):** At least one new model with proper fields and relationships
- **API Endpoints:** RESTful endpoints for your feature (minimum: list, create, retrieve, update, delete)
- **Data Validation:** Proper validation and error handling
- **Integration:** Connect with existing models (Lead, Contact, or Reminder)
- **Testing:** Minimum of 5 unit tests covering key functionality

### 2. Frontend (Vue 3 + Vuetify)
- **New Page/Component:** Dedicated UI for your feature
- **CRUD Operations:** Create, read, update, delete functionality
- **User Experience:** Loading states, error handling, form validation
- **Integration:** Update existing pages to show/link to your feature
- **Responsive Design:** Should work on desktop and tablet

### 3. Code Quality
- Clean, readable, maintainable code
- Follow existing project patterns and conventions
- Meaningful variable/function names
- Comments for complex logic
- Proper error handling

### 4. Testing
- At least 5 meaningful tests
- Cover both positive and negative cases
- Test business logic and edge cases

---

## Submission Requirements

### What to Submit

#### Submission Method: Fork & Pull Request

1. **Fork the Repository:**
   - Fork this repository to your own GitHub account.
   - Clone your fork locally to work on it.
   - Follow the instructions in `README.md` to set up both backend and frontend.

2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Work:**
   - Make commits with clear, descriptive messages.
   - Push to your fork: `git push origin feature/your-feature-name`.

4. **Documentation:**
   Create a file named `SOLUTION.md` in the root directory containing:
   - **Feature Choice:** Which feature you chose and why
   - **Product Rationale:** Why this feature adds value to the CRM
   - **Technical Overview:** Architecture and approach
   - **Design Decisions:** Key technical decisions and justifications
   - **Implementation Details:** What you built and how it works
   - **Challenges:** Problems you encountered and solutions
   - **Time Breakdown:** Approximate time spent on each major task
   - **Setup Instructions:** Clear steps to run your code locally
   - **Testing Instructions:** How to run your tests
   - **Future Improvements:** What you would add/change with more time
   - **Trade-offs:** What you prioritized and what you deferred

5. **Database Migration:**
   - Include all migration files.
   - Ensure migrations run successfully on a fresh database.

6. **Create a Pull Request:**
   - When ready, create a Pull Request from your fork back to the original repository.
   - Title: `[Your Name] - [Feature Name]`.
   - In the PR description, include a brief summary and a link to your `SOLUTION.md`.

### How We'll Review Your Submission

We will:
1. Check out your Pull Request
2. Review your code changes
3. Read your `SOLUTION.md` documentation
4. Follow your setup instructions to run the application
5. Test your feature functionality
6. Run your test suite

Make sure your code runs successfully by following your own setup instructions on a fresh checkout!

---

## Evaluation Criteria

**What we're looking for:**
- **Thoughtful scope** - Can you choose and complete an appropriately-sized feature?
- **Full-stack skills** - Backend and frontend implementation quality
- **Product sense** - Does the feature solve a real problem?
- **Code craftsmanship** - Is your code production-ready?
- **Problem-solving** - How do you handle challenges and constraints?
- **Communication** - Can you explain your decisions clearly?

---

## Technical Guidelines

### Backend Best Practices
- Follow Django conventions and DRF patterns
- Use serializers properly (separate read/write serializers if needed)
- Add appropriate model methods and properties
- Write meaningful docstrings for complex logic

### Frontend Best Practices
- Follow Vue 3 Composition API patterns
- Create reusable components where appropriate
- Use Vuetify components effectively
- Handle loading and error states
- Write clean, maintainable JavaScript/Vue code

### Testing Best Practices
- Test business logic, not just CRUD operations
- Use meaningful test names that describe what is being tested
- Include positive and negative test cases
- Mock external dependencies appropriately

---

## Questions & Clarifications

If you have questions about the requirements:
1. Make reasonable assumptions and document them in your `SOLUTION.md`
2. If something is truly blocking, you may email dev@smartstaffingsupport.com
 for clarification
3. We value your ability to make good technical decisions independently

---

## Important Notes

- **Scope appropriately** - Choose a feature you can complete well in 48 hours
- **Code must run successfully** - We will test your submission
- **Original work only** - Don't copy solutions from the internet
- **Quality over quantity** - a well-implemented focused feature beats a half-finished ambitious one
- **Show your strengths** - Choose a feature that lets you demonstrate what you're good at
- **It's okay to be creative** - We value innovation and original thinking

---

## Submission Deadline

Please submit your Pull Request within **48 hours** of receiving this assignment.

**Note:** Your PR should be created by the deadline.

---

Good luck! We're excited to see your solution. 

# Happy Coding 🚀
